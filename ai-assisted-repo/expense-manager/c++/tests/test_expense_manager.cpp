#include <gtest/gtest.h>
#include "expense_manager/employees.hpp"
#include "expense_manager/currency.hpp"
#include "expense_manager/policies.hpp"
#include "expense_manager/routing.hpp"
#include "expense_manager/ledger.hpp"
#include "expense_manager/expenses.hpp"

using namespace expense_manager;

// --- Employee Tests ---

TEST(EmployeeTest, ManagementChainTraversal) {
    EmployeeService service;
    service.register_department(Department("ENG", "Engineering"));
    service.register_employee(Employee("e_ceo", "Alice", "ENG", Role::C_LEVEL));
    service.register_employee(Employee("e_vp", "Bob", "ENG", Role::VP, "VP", "e_ceo"));
    service.register_employee(Employee("e_ic", "Charlie", "ENG", Role::IC, "Dev", "e_vp"));

    auto chain = service.get_management_chain("e_ic");
    std::vector<std::string> ids;
    for (const auto& emp : chain) {
        ids.push_back(emp.employee_id);
    }
    std::vector<std::string> expected = {"e_vp", "e_ceo"};
    EXPECT_EQ(ids, expected);
}

TEST(EmployeeTest, ManagementChainHandlesCyclicReferenceSafely) {
    EmployeeService service;
    service.register_department(Department("ENG", "Engineering"));
    service.register_employee(Employee("e_a", "Alice", "ENG", Role::VP, "VP", "e_b"));
    service.register_employee(Employee("e_b", "Bob", "ENG", Role::MANAGER, "Mgr", "e_a"));

    auto chain = service.get_management_chain("e_a");
    std::vector<std::string> ids;
    for (const auto& emp : chain) {
        ids.push_back(emp.employee_id);
    }
    std::vector<std::string> expected = {"e_b"};
    EXPECT_EQ(ids, expected);
}

TEST(EmployeeTest, DepartmentHierarchyResolution) {
    EmployeeService service;
    service.register_department(Department("CORP", "Corporate"));
    service.register_department(Department("ENG", "Engineering", "CORP"));
    service.register_department(Department("INFRA", "Infrastructure", "ENG"));

    std::vector<std::string> expected = {"INFRA", "ENG", "CORP"};
    EXPECT_EQ(service.get_department_hierarchy("INFRA"), expected);
}

// --- Currency Tests ---

TEST(CurrencyTest, ConvertToUsdIdentity) {
    FXService fx;
    Money usd(5000, Currency::USD);
    EXPECT_EQ(fx.convert_to_usd(usd).amount_cents, 5000);
}

TEST(CurrencyTest, ConvertToUsdForeignRates) {
    FXService fx;
    Money eur(9500, Currency::EUR);
    EXPECT_EQ(fx.convert_to_usd(eur).amount_cents, 10450);
}

TEST(CurrencyTest, ConvertToUsdRoundingPrecision) {
    FXService fx;
    Money eur(2999, Currency::EUR);
    EXPECT_EQ(fx.convert_to_usd(eur).amount_cents, 3299);
}

// --- Policy Tests ---

TEST(PolicyTest, DefaultFallbackRequiresApproval) {
    EmployeeService es;
    es.register_department(Department("CORP", "Corp"));
    PolicyService ps(es);

    auto eval = ps.evaluate_policy("CORP", ExpenseCategory::LODGING, Money(15000, Currency::USD));
    EXPECT_EQ(eval.action, PolicyAction::REQUIRE_APPROVAL);
    EXPECT_FALSE(eval.matched_rule_id.has_value());
}

TEST(PolicyTest, PolicyExactBoundaryAndPriorityOrder) {
    EmployeeService es;
    es.register_department(Department("CORP", "Corp"));
    PolicyService ps(es);

    PolicyRule r1("r_meal_auto", ExpenseCategory::FOOD_AND_BEVERAGE, PolicyAction::AUTO_APPROVE,
                  100, std::nullopt, std::nullopt, 5000, std::nullopt);
    PolicyRule r2("r_meal_ban", ExpenseCategory::FOOD_AND_BEVERAGE, PolicyAction::REJECT,
                  10, std::nullopt, std::nullopt, std::nullopt, 50000);

    ps.register_rule(r1);
    ps.register_rule(r2);

    auto eval50 = ps.evaluate_policy("CORP", ExpenseCategory::FOOD_AND_BEVERAGE, Money(5000, Currency::USD));
    EXPECT_EQ(eval50.action, PolicyAction::AUTO_APPROVE);
    ASSERT_TRUE(eval50.matched_rule_id.has_value());
    EXPECT_EQ(*eval50.matched_rule_id, "r_meal_auto");

    auto eval600 = ps.evaluate_policy("CORP", ExpenseCategory::FOOD_AND_BEVERAGE, Money(60000, Currency::USD));
    EXPECT_EQ(eval600.action, PolicyAction::REJECT);
    ASSERT_TRUE(eval600.matched_rule_id.has_value());
    EXPECT_EQ(*eval600.matched_rule_id, "r_meal_ban");
}

// --- Routing Tests ---

TEST(RoutingTest, BasicDirectManagerRouting) {
    EmployeeService es;
    es.register_department(Department("ENG", "Engineering"));
    es.register_employee(Employee("e_mgr", "Bob", "ENG", Role::MANAGER));
    es.register_employee(Employee("e_dev", "Charlie", "ENG", Role::IC, "Dev", "e_mgr"));

    RoutingService rs(es);
    auto chain = rs.build_approval_chain("e_dev", Money(50000, Currency::USD));
    std::vector<std::string> expected = {"e_mgr"};
    EXPECT_EQ(chain.approvers, expected);
}

// --- Ledger Tests ---

TEST(LedgerTest, LedgerCapexAndCategoryTotals) {
    LedgerService ls;
    ls.record_expense("exp_1", "e_dev", "ENG", ExpenseCategory::HARDWARE, Money(150000, Currency::USD));
    ls.record_expense("exp_2", "e_dev", "ENG", ExpenseCategory::FOOD_AND_BEVERAGE, Money(2500, Currency::USD));

    EXPECT_EQ(ls.get_total_by_category(ExpenseCategory::HARDWARE), 150000);
    EXPECT_EQ(ls.get_total_capex(std::string("ENG")), 150000);
}

TEST(LedgerTest, LedgerPreventsDuplicatePosting) {
    LedgerService ls;
    ls.record_expense("exp_1", "e_dev", "ENG", ExpenseCategory::HARDWARE, Money(150000, Currency::USD));

    EXPECT_THROW({
        ls.record_expense("exp_1", "e_dev", "ENG", ExpenseCategory::HARDWARE, Money(150000, Currency::USD));
    }, std::invalid_argument);
}

// --- Expense Tests ---

class ExpenseSystemTest : public ::testing::Test {
protected:
    EmployeeService emp_svc;
    FXService fx_svc;
    PolicyService policy_svc{emp_svc};
    RoutingService routing_svc{emp_svc};
    LedgerService ledger_svc;
    ExpenseService expense_svc{emp_svc, fx_svc, policy_svc, routing_svc, ledger_svc};

    void SetUp() override {
        emp_svc.register_department(Department("CORP", "Corporate"));
        emp_svc.register_department(Department("ENG", "Engineering", "CORP"));
        emp_svc.register_department(Department("INFRA", "Infrastructure", "ENG"));

        emp_svc.register_employee(Employee("e_ceo", "Alice", "CORP", Role::C_LEVEL, "CEO", std::nullopt));
        emp_svc.register_employee(Employee("e_vp", "Bob", "ENG", Role::VP, "VP Engineering", "e_ceo"));
        emp_svc.register_employee(Employee("e_mgr", "Charlie", "INFRA", Role::MANAGER, "Eng Manager", "e_vp"));
        emp_svc.register_employee(Employee("e_dev", "David", "INFRA", Role::IC, "Software Engineer", "e_mgr"));
    }
};

TEST_F(ExpenseSystemTest, ExactBoundaryAutoApprove) {
    PolicyRule r("r_food_20", ExpenseCategory::FOOD_AND_BEVERAGE, PolicyAction::AUTO_APPROVE,
                 100, std::nullopt, std::nullopt, 2000, std::nullopt);
    policy_svc.register_rule(r);

    Expense exp("exp_1", "e_dev", Money(2000, Currency::USD), ExpenseCategory::FOOD_AND_BEVERAGE, "Coffee & Bagel");
    auto record = expense_svc.submit_expense(exp);

    EXPECT_EQ(record.status, ExpenseStatus::APPROVED);
    EXPECT_EQ(ledger_svc.get_total_by_category(ExpenseCategory::FOOD_AND_BEVERAGE), 2000);
}

TEST_F(ExpenseSystemTest, ForeignCurrencyFxNormalization) {
    PolicyRule r("r_food_100", ExpenseCategory::FOOD_AND_BEVERAGE, PolicyAction::AUTO_APPROVE,
                 100, std::nullopt, std::nullopt, 10000, std::nullopt);
    policy_svc.register_rule(r);

    Expense exp("exp_2", "e_dev", Money(9500, Currency::EUR), ExpenseCategory::FOOD_AND_BEVERAGE, "Berlin Team Dinner");
    auto record = expense_svc.submit_expense(exp);

    EXPECT_EQ(record.status, ExpenseStatus::PENDING_APPROVAL);
    EXPECT_EQ(record.usd_amount.amount_cents, 10450);
    EXPECT_EQ(ledger_svc.get_total_by_category(ExpenseCategory::FOOD_AND_BEVERAGE), 0);
}

TEST_F(ExpenseSystemTest, RejectsNonPositiveAmounts) {
    PolicyRule r("r_food_100", ExpenseCategory::FOOD_AND_BEVERAGE, PolicyAction::AUTO_APPROVE,
                 100, std::nullopt, std::nullopt, 10000, std::nullopt);
    policy_svc.register_rule(r);

    Expense exp("exp_neg", "e_dev", Money(-5000, Currency::USD), ExpenseCategory::FOOD_AND_BEVERAGE, "Refund Spoof");
    auto record = expense_svc.submit_expense(exp);

    EXPECT_EQ(record.status, ExpenseStatus::REJECTED);
    EXPECT_EQ(ledger_svc.get_total_by_category(ExpenseCategory::FOOD_AND_BEVERAGE), 0);
}

