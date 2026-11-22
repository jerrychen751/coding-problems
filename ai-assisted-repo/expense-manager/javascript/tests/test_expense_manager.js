const assert = require('node:assert');

const { Role, Department, Employee } = require('../employees/models');
const { EmployeeService } = require('../employees/service');

const { Currency, Money } = require('../currency/models');
const { FXService } = require('../currency/service');

const { ExpenseCategory, PolicyAction, PolicyRule } = require('../policies/models');
const { PolicyService } = require('../policies/service');

const { RoutingService } = require('../routing/service');

const { SpendType } = require('../ledger/models');
const { LedgerService } = require('../ledger/service');

const { Expense, ExpenseStatus } = require('../expenses/models');
const { ExpenseService } = require('../expenses/service');

function runTests() {
  let passed = 0;
  let total = 0;
  const failures = [];

  function test(name, fn) {
    total++;
    try {
      fn();
      passed++;
      process.stdout.write('.');
    } catch (err) {
      failures.push({ name, err });
      process.stdout.write('F');
    }
  }

  // --- Employee Tests ---
  test('test_management_chain_traversal', () => {
    const service = new EmployeeService();
    service.registerDepartment(new Department('ENG', 'Engineering'));
    service.registerEmployee(new Employee('e_ceo', 'Alice', 'ENG', Role.C_LEVEL));
    service.registerEmployee(new Employee('e_vp', 'Bob', 'ENG', Role.VP, 'VP', 'e_ceo'));
    service.registerEmployee(new Employee('e_ic', 'Charlie', 'ENG', Role.IC, 'Eng', 'e_vp'));

    const chain = service.getManagementChain('e_ic');
    assert.deepStrictEqual(chain.map((e) => e.employeeId), ['e_vp', 'e_ceo']);
  });

  test('test_management_chain_handles_cyclic_reference_safely', () => {
    const service = new EmployeeService();
    service.registerDepartment(new Department('ENG', 'Engineering'));
    service.registerEmployee(new Employee('e_a', 'Alice', 'ENG', Role.VP, 'VP', 'e_b'));
    service.registerEmployee(new Employee('e_b', 'Bob', 'ENG', Role.MANAGER, 'Mgr', 'e_a'));

    const chain = service.getManagementChain('e_a');
    assert.deepStrictEqual(chain.map((e) => e.employeeId), ['e_b']);
  });

  test('test_department_hierarchy_resolution', () => {
    const service = new EmployeeService();
    service.registerDepartment(new Department('CORP', 'Corporate'));
    service.registerDepartment(new Department('ENG', 'Engineering', 'CORP'));
    service.registerDepartment(new Department('INFRA', 'Infrastructure', 'ENG'));

    assert.deepStrictEqual(service.getDepartmentHierarchy('INFRA'), ['INFRA', 'ENG', 'CORP']);
  });

  // --- Currency Tests ---
  test('test_convert_to_usd_identity', () => {
    const fx = new FXService();
    const usd = new Money(5000, Currency.USD);
    assert.strictEqual(fx.convertToUsd(usd).amountCents, 5000);
  });

  test('test_convert_to_usd_foreign_rates', () => {
    const fx = new FXService();
    const eur = new Money(9500, Currency.EUR);
    assert.strictEqual(fx.convertToUsd(eur).amountCents, 10450);
  });

  test('test_convert_to_usd_rounding_precision', () => {
    const fx = new FXService();
    const eur = new Money(2999, Currency.EUR);
    assert.strictEqual(fx.convertToUsd(eur).amountCents, 3299);
  });

  // --- Policy Tests ---
  test('test_default_fallback_requires_approval', () => {
    const empSvc = new EmployeeService();
    empSvc.registerDepartment(new Department('CORP', 'Corp'));
    const policySvc = new PolicyService(empSvc);

    const { action, ruleId } = policySvc.evaluatePolicy(
      'CORP',
      ExpenseCategory.LODGING,
      new Money(15000, Currency.USD)
    );
    assert.strictEqual(action, PolicyAction.REQUIRE_APPROVAL);
    assert.strictEqual(ruleId, null);
  });

  test('test_policy_exact_boundary_and_priority_order', () => {
    const empSvc = new EmployeeService();
    empSvc.registerDepartment(new Department('CORP', 'Corp'));
    const policySvc = new PolicyService(empSvc);

    policySvc.registerRule(
      new PolicyRule({
        ruleId: 'r_meal_auto',
        category: ExpenseCategory.FOOD_AND_BEVERAGE,
        maxAmountCents: 5000,
        action: PolicyAction.AUTO_APPROVE,
        priority: 100
      })
    );
    policySvc.registerRule(
      new PolicyRule({
        ruleId: 'r_meal_ban',
        category: ExpenseCategory.FOOD_AND_BEVERAGE,
        minAmountCents: 50000,
        action: PolicyAction.REJECT,
        priority: 10
      })
    );

    const res50 = policySvc.evaluatePolicy(
      'CORP',
      ExpenseCategory.FOOD_AND_BEVERAGE,
      new Money(5000, Currency.USD)
    );
    assert.strictEqual(res50.action, PolicyAction.AUTO_APPROVE);
    assert.strictEqual(res50.ruleId, 'r_meal_auto');

    const res600 = policySvc.evaluatePolicy(
      'CORP',
      ExpenseCategory.FOOD_AND_BEVERAGE,
      new Money(60000, Currency.USD)
    );
    assert.strictEqual(res600.action, PolicyAction.REJECT);
    assert.strictEqual(res600.ruleId, 'r_meal_ban');
  });

  // --- Routing Tests ---
  test('test_basic_direct_manager_routing', () => {
    const empSvc = new EmployeeService();
    empSvc.registerDepartment(new Department('ENG', 'Engineering'));
    empSvc.registerEmployee(new Employee('e_mgr', 'Bob', 'ENG', Role.MANAGER));
    empSvc.registerEmployee(new Employee('e_dev', 'Charlie', 'ENG', Role.IC, 'Dev', 'e_mgr'));

    const routingSvc = new RoutingService(empSvc);
    const chain = routingSvc.buildApprovalChain('e_dev', new Money(50000, Currency.USD));
    assert.deepStrictEqual(chain.approvers, ['e_mgr']);
  });

  // --- Ledger Tests ---
  test('test_ledger_capex_and_category_totals', () => {
    const ledger = new LedgerService();
    ledger.recordExpense('exp_1', 'e_dev', 'ENG', ExpenseCategory.HARDWARE, new Money(150000, Currency.USD));
    ledger.recordExpense('exp_2', 'e_dev', 'ENG', ExpenseCategory.FOOD_AND_BEVERAGE, new Money(2500, Currency.USD));

    assert.strictEqual(ledger.getTotalByCategory(ExpenseCategory.HARDWARE), 150000);
    assert.strictEqual(ledger.getTotalCapex('ENG'), 150000);
  });

  test('test_ledger_prevents_duplicate_posting', () => {
    const ledger = new LedgerService();
    ledger.recordExpense('exp_1', 'e_dev', 'ENG', ExpenseCategory.HARDWARE, new Money(150000, Currency.USD));

    assert.throws(
      () => {
        ledger.recordExpense('exp_1', 'e_dev', 'ENG', ExpenseCategory.HARDWARE, new Money(150000, Currency.USD));
      },
      /already been posted/
    );
  });

  // --- Expense Tests ---
  function createSystem() {
    const empSvc = new EmployeeService();
    const fxSvc = new FXService();
    const policySvc = new PolicyService(empSvc);
    const routingSvc = new RoutingService(empSvc);
    const ledgerSvc = new LedgerService();
    const expenseSvc = new ExpenseService(empSvc, fxSvc, policySvc, routingSvc, ledgerSvc);

    empSvc.registerDepartment(new Department('CORP', 'Corporate'));
    empSvc.registerDepartment(new Department('ENG', 'Engineering', 'CORP'));
    empSvc.registerDepartment(new Department('INFRA', 'Infrastructure', 'ENG'));

    empSvc.registerEmployee(new Employee('e_ceo', 'Alice', 'CORP', Role.C_LEVEL, 'CEO'));
    empSvc.registerEmployee(new Employee('e_vp', 'Bob', 'ENG', Role.VP, 'VP Engineering', 'e_ceo'));
    empSvc.registerEmployee(new Employee('e_mgr', 'Charlie', 'INFRA', Role.MANAGER, 'Eng Manager', 'e_vp'));
    empSvc.registerEmployee(new Employee('e_dev', 'David', 'INFRA', Role.IC, 'Software Engineer', 'e_mgr'));

    return { empSvc, fxSvc, policySvc, routingSvc, ledgerSvc, expenseSvc };
  }

  test('test_exact_boundary_auto_approve', () => {
    const { policySvc, ledgerSvc, expenseSvc } = createSystem();

    policySvc.registerRule(
      new PolicyRule({
        ruleId: 'r_food_20',
        category: ExpenseCategory.FOOD_AND_BEVERAGE,
        maxAmountCents: 2000,
        action: PolicyAction.AUTO_APPROVE
      })
    );

    const exp = new Expense('exp_1', 'e_dev', new Money(2000, Currency.USD), ExpenseCategory.FOOD_AND_BEVERAGE, 'Coffee & Bagel');
    const record = expenseSvc.submitExpense(exp);

    assert.strictEqual(record.status, ExpenseStatus.APPROVED);
    assert.strictEqual(ledgerSvc.getTotalByCategory(ExpenseCategory.FOOD_AND_BEVERAGE), 2000);
  });

  test('test_foreign_currency_fx_normalization', () => {
    const { policySvc, ledgerSvc, expenseSvc } = createSystem();

    policySvc.registerRule(
      new PolicyRule({
        ruleId: 'r_food_100',
        category: ExpenseCategory.FOOD_AND_BEVERAGE,
        maxAmountCents: 10000,
        action: PolicyAction.AUTO_APPROVE
      })
    );

    const exp = new Expense('exp_2', 'e_dev', new Money(9500, Currency.EUR), ExpenseCategory.FOOD_AND_BEVERAGE, 'Berlin Team Dinner');
    const record = expenseSvc.submitExpense(exp);

    assert.strictEqual(record.status, ExpenseStatus.PENDING_APPROVAL);
    assert.strictEqual(record.usdAmount.amountCents, 10450);
    assert.strictEqual(ledgerSvc.getTotalByCategory(ExpenseCategory.FOOD_AND_BEVERAGE), 0);
  });

  test('test_rejects_non_positive_amounts', () => {
    const { policySvc, ledgerSvc, expenseSvc } = createSystem();

    policySvc.registerRule(
      new PolicyRule({
        ruleId: 'r_food_100',
        category: ExpenseCategory.FOOD_AND_BEVERAGE,
        maxAmountCents: 10000,
        action: PolicyAction.AUTO_APPROVE
      })
    );

    const expNegative = new Expense('exp_neg', 'e_dev', new Money(-5000, Currency.USD), ExpenseCategory.FOOD_AND_BEVERAGE, 'Refund Spoof');
    const record = expenseSvc.submitExpense(expNegative);

    assert.strictEqual(record.status, ExpenseStatus.REJECTED);
    assert.strictEqual(ledgerSvc.getTotalByCategory(ExpenseCategory.FOOD_AND_BEVERAGE), 0);
  });

  process.stdout.write('\n');
  if (failures.length > 0) {
    console.log(`\nFAILURES (${failures.length} of ${total}):`);
    for (const f of failures) {
      console.log(`- ${f.name}: ${f.err.message}`);
    }
    process.exit(1);
  } else {
    console.log(`\nOK (${passed} tests)`);
  }
}

runTests();
