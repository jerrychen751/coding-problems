# Designing an Expense-Sharing System

## Requirements
1. The system should let members of a group record shared expenses and pay each other back. There is only one group, and about 100 members is the practical maximum.
2. Any member of the group should be able to add an expense to the group.
3. The system should support splitting an expense evenly among a subset of members, and splitting it unevenly with a custom amount for each member.
4. The system should track how much each member owes every other member.
5. Each member should be able to see how much they owe each other member.

## Out of scope
- An in-app wallet
- Leaving a group

## Interface
- `add_member`
- `add_expense`
- `pay_expenses`
- `report_expenses`
