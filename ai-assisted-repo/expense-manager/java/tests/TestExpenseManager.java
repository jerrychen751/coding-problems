package tests;

import expensemanager.currency.Currency;
import expensemanager.currency.FXService;
import expensemanager.currency.Money;
import expensemanager.employees.Department;
import expensemanager.employees.Employee;
import expensemanager.employees.EmployeeService;
import expensemanager.employees.Role;
import expensemanager.expenses.Expense;
import expensemanager.expenses.ExpenseRecord;
import expensemanager.expenses.ExpenseService;
import expensemanager.expenses.ExpenseStatus;
import expensemanager.ledger.LedgerService;
import expensemanager.policies.ExpenseCategory;
import expensemanager.policies.PolicyAction;
import expensemanager.policies.PolicyEvaluation;
import expensemanager.policies.PolicyRule;
import expensemanager.policies.PolicyService;
import expensemanager.routing.ApprovalChain;
import expensemanager.routing.RoutingService;
import org.junit.jupiter.api.BeforeEach;
import org.junit.jupiter.api.Test;

import java.util.Arrays;
import java.util.List;
import java.util.stream.Collectors;

import static org.junit.jupiter.api.Assertions.*;

public class TestExpenseManager {

    private EmployeeService empSvc;
    private FXService fxSvc;
    private PolicyService policySvc;
    private RoutingService routingSvc;
    private LedgerService ledgerSvc;
    private ExpenseService expenseSvc;

    @BeforeEach
    public void setUp() {
        empSvc = new EmployeeService();
        fxSvc = new FXService();
        policySvc = new PolicyService(empSvc);
        routingSvc = new RoutingService(empSvc);
        ledgerSvc = new LedgerService();
        expenseSvc = new ExpenseService(empSvc, fxSvc, policySvc, routingSvc, ledgerSvc);

        empSvc.registerDepartment(new Department("CORP", "Corporate"));
        empSvc.registerDepartment(new Department("ENG", "Engineering", "CORP"));
        empSvc.registerDepartment(new Department("INFRA", "Infrastructure", "ENG"));

        empSvc.registerEmployee(new Employee("e_ceo", "Alice", "CORP", Role.C_LEVEL, "CEO", null));
        empSvc.registerEmployee(new Employee("e_vp", "Bob", "ENG", Role.VP, "VP Engineering", "e_ceo"));
        empSvc.registerEmployee(new Employee("e_mgr", "Charlie", "INFRA", Role.MANAGER, "Eng Manager", "e_vp"));
        empSvc.registerEmployee(new Employee("e_dev", "David", "INFRA", Role.IC, "Software Engineer", "e_mgr"));
    }

    // --- Employee Tests ---

    @Test
    public void testManagementChainTraversal() {
        EmployeeService service = new EmployeeService();
        service.registerDepartment(new Department("ENG", "Engineering"));
        service.registerEmployee(new Employee("e_ceo", "Alice", "ENG", Role.C_LEVEL));
        service.registerEmployee(new Employee("e_vp", "Bob", "ENG", Role.VP, "VP", "e_ceo"));
        service.registerEmployee(new Employee("e_ic", "Charlie", "ENG", Role.IC, "Dev", "e_vp"));

        List<Employee> chain = service.getManagementChain("e_ic");
        List<String> ids = chain.stream().map(Employee::getEmployeeId).collect(Collectors.toList());
        assertEquals(Arrays.asList("e_vp", "e_ceo"), ids);
    }

    @Test
    public void testManagementChainHandlesCyclicReferenceSafely() {
        EmployeeService service = new EmployeeService();
        service.registerDepartment(new Department("ENG", "Engineering"));
        service.registerEmployee(new Employee("e_a", "Alice", "ENG", Role.VP, "VP", "e_b"));
        service.registerEmployee(new Employee("e_b", "Bob", "ENG", Role.MANAGER, "Mgr", "e_a"));

        List<Employee> chain = service.getManagementChain("e_a");
        List<String> ids = chain.stream().map(Employee::getEmployeeId).collect(Collectors.toList());
        assertEquals(List.of("e_b"), ids);
    }

    @Test
    public void testDepartmentHierarchyResolution() {
        EmployeeService service = new EmployeeService();
        service.registerDepartment(new Department("CORP", "Corporate"));
        service.registerDepartment(new Department("ENG", "Engineering", "CORP"));
        service.registerDepartment(new Department("INFRA", "Infrastructure", "ENG"));

        assertEquals(Arrays.asList("INFRA", "ENG", "CORP"), service.getDepartmentHierarchy("INFRA"));
    }

    // --- Currency Tests ---

    @Test
    public void testConvertToUsdIdentity() {
        FXService fx = new FXService();
        Money usd = new Money(5000, Currency.USD);
        assertEquals(5000, fx.convertToUsd(usd).getAmountCents());
    }

    @Test
    public void testConvertToUsdForeignRates() {
        FXService fx = new FXService();
        Money eur = new Money(9500, Currency.EUR);
        assertEquals(10450, fx.convertToUsd(eur).getAmountCents());
    }

    @Test
    public void testConvertToUsdRoundingPrecision() {
        FXService fx = new FXService();
        Money eur = new Money(2999, Currency.EUR);
        assertEquals(3299, fx.convertToUsd(eur).getAmountCents());
    }

    // --- Policy Tests ---

    @Test
    public void testDefaultFallbackRequiresApproval() {
        EmployeeService es = new EmployeeService();
        es.registerDepartment(new Department("CORP", "Corp"));
        PolicyService ps = new PolicyService(es);

        PolicyEvaluation eval = ps.evaluatePolicy("CORP", ExpenseCategory.LODGING, new Money(15000, Currency.USD));
        assertEquals(PolicyAction.REQUIRE_APPROVAL, eval.getAction());
        assertTrue(eval.getMatchedRuleId().isEmpty());
    }

    @Test
    public void testPolicyExactBoundaryAndPriorityOrder() {
        EmployeeService es = new EmployeeService();
        es.registerDepartment(new Department("CORP", "Corp"));
        PolicyService ps = new PolicyService(es);

        ps.registerRule(new PolicyRule.Builder("r_meal_auto", ExpenseCategory.FOOD_AND_BEVERAGE)
            .maxAmountCents(5000)
            .action(PolicyAction.AUTO_APPROVE)
            .priority(100)
            .build());

        ps.registerRule(new PolicyRule.Builder("r_meal_ban", ExpenseCategory.FOOD_AND_BEVERAGE)
            .minAmountCents(50000)
            .action(PolicyAction.REJECT)
            .priority(10)
            .build());

        PolicyEvaluation eval50 = ps.evaluatePolicy("CORP", ExpenseCategory.FOOD_AND_BEVERAGE, new Money(5000, Currency.USD));
        assertEquals(PolicyAction.AUTO_APPROVE, eval50.getAction());
        assertEquals("r_meal_auto", eval50.getMatchedRuleId().orElse(null));

        PolicyEvaluation eval600 = ps.evaluatePolicy("CORP", ExpenseCategory.FOOD_AND_BEVERAGE, new Money(60000, Currency.USD));
        assertEquals(PolicyAction.REJECT, eval600.getAction());
        assertEquals("r_meal_ban", eval600.getMatchedRuleId().orElse(null));
    }

    // --- Routing Tests ---

    @Test
    public void testBasicDirectManagerRouting() {
        EmployeeService es = new EmployeeService();
        es.registerDepartment(new Department("ENG", "Engineering"));
        es.registerEmployee(new Employee("e_mgr", "Bob", "ENG", Role.MANAGER));
        es.registerEmployee(new Employee("e_dev", "Charlie", "ENG", Role.IC, "Dev", "e_mgr"));

        RoutingService rs = new RoutingService(es);
        ApprovalChain chain = rs.buildApprovalChain("e_dev", new Money(50000, Currency.USD));
        assertEquals(List.of("e_mgr"), chain.getApprovers());
    }

    // --- Ledger Tests ---

    @Test
    public void testLedgerCapexAndCategoryTotals() {
        LedgerService ls = new LedgerService();
        ls.recordExpense("exp_1", "e_dev", "ENG", ExpenseCategory.HARDWARE, new Money(150000, Currency.USD));
        ls.recordExpense("exp_2", "e_dev", "ENG", ExpenseCategory.FOOD_AND_BEVERAGE, new Money(2500, Currency.USD));

        assertEquals(150000, ls.getTotalByCategory(ExpenseCategory.HARDWARE));
        assertEquals(150000, ls.getTotalCapex("ENG"));
    }

    @Test
    public void testLedgerPreventsDuplicatePosting() {
        LedgerService ls = new LedgerService();
        ls.recordExpense("exp_1", "e_dev", "ENG", ExpenseCategory.HARDWARE, new Money(150000, Currency.USD));

        assertThrows(IllegalArgumentException.class, () -> {
            ls.recordExpense("exp_1", "e_dev", "ENG", ExpenseCategory.HARDWARE, new Money(150000, Currency.USD));
        });
    }

    // --- Expense Tests ---

    @Test
    public void testExactBoundaryAutoApprove() {
        policySvc.registerRule(new PolicyRule.Builder("r_food_20", ExpenseCategory.FOOD_AND_BEVERAGE)
            .maxAmountCents(2000)
            .action(PolicyAction.AUTO_APPROVE)
            .build());

        Expense exp = new Expense("exp_1", "e_dev", new Money(2000, Currency.USD), ExpenseCategory.FOOD_AND_BEVERAGE, "Coffee & Bagel");
        ExpenseRecord record = expenseSvc.submitExpense(exp);

        assertEquals(ExpenseStatus.APPROVED, record.getStatus());
        assertEquals(2000, ledgerSvc.getTotalByCategory(ExpenseCategory.FOOD_AND_BEVERAGE));
    }

    @Test
    public void testForeignCurrencyFxNormalization() {
        policySvc.registerRule(new PolicyRule.Builder("r_food_100", ExpenseCategory.FOOD_AND_BEVERAGE)
            .maxAmountCents(10000)
            .action(PolicyAction.AUTO_APPROVE)
            .build());

        Expense exp = new Expense("exp_2", "e_dev", new Money(9500, Currency.EUR), ExpenseCategory.FOOD_AND_BEVERAGE, "Berlin Team Dinner");
        ExpenseRecord record = expenseSvc.submitExpense(exp);

        assertEquals(ExpenseStatus.PENDING_APPROVAL, record.getStatus());
        assertEquals(10450, record.getUsdAmount().getAmountCents());
        assertEquals(0, ledgerSvc.getTotalByCategory(ExpenseCategory.FOOD_AND_BEVERAGE));
    }

    @Test
    public void testRejectsNonPositiveAmounts() {
        policySvc.registerRule(new PolicyRule.Builder("r_food_100", ExpenseCategory.FOOD_AND_BEVERAGE)
            .maxAmountCents(10000)
            .action(PolicyAction.AUTO_APPROVE)
            .build());

        Expense expNegative = new Expense("exp_neg", "e_dev", new Money(-5000, Currency.USD), ExpenseCategory.FOOD_AND_BEVERAGE, "Refund Spoof");
        ExpenseRecord record = expenseSvc.submitExpense(expNegative);

        assertEquals(ExpenseStatus.REJECTED, record.getStatus());
        assertEquals(0, ledgerSvc.getTotalByCategory(ExpenseCategory.FOOD_AND_BEVERAGE));
    }
}

