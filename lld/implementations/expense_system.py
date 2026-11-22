"""
Design an in-memory expense-sharing system like Splitwise.
"""

"""
Expense-sharing app

People in the same group pay each other back
- Know how much someone owes someone else
- Group size of 100 people is near max; we just have one group
- Anybody in the group can update expense in group
- Support even splitting and uneven distributions. User should be able to customize on a per-member basis within group.
- User should know how much they owe each other person.

Don't worry about:
- Wallet in app
- Leaving groups

ExpenseSystem
- users
- owed: how much does person X owe each other person in the group

- add_member(user): Add a new member to group
- add_expense(expense)
    - Allow equal split to apply to subset of users
    - Equal split, customized split
    - custom_split is a dict mapping users -> amt they owe payer
- pay_expense()
- report_expenses(): User sees how much they owe other people
"""

from dataclasses import dataclass
from collections import defaultdict
from enum import Enum
from typing import Optional, Dict

@dataclass
class User:
    id: str
    first_name: str
    last_name: str

class SplitType(Enum):
    EQUAL = "equal"
    CUSTOM = "custom"

@dataclass
class Expense:
    id: str
    payer: User
    amount: float
    recipients: Optional[list[User]]
    custom_split: Optional[Dict[str, float]]
    split_type: SplitType



class ExpenseSystem:
    def __init__(self, users: list[User]) -> None:
        self.users: dict[str, User] = {user.id: user for user in users}
        # Balances are whole cents, so repeated additions never pick up float rounding error
        self.owed: defaultdict[str, defaultdict[str, int]] = defaultdict(lambda: defaultdict(int))

    def add_member(self, user: User) -> None:
        if user.id not in self.users:
            self.users[user.id] = user

    def add_expense(self, expense: Expense) -> None:
        payer = expense.payer
        total_cents = round(expense.amount * 100)
        if payer.id not in self.users or total_cents < 0:
            return

        if expense.split_type == SplitType.EQUAL:
            if not expense.recipients:
                return
            # 100 people
            # 167 cents balance
            # 67 people get 2 cents, 33 people get 1 cent
            quotient, remainder = divmod(total_cents, len(expense.recipients))
            owed_cents = {
                user.id: quotient + (1 if i < remainder else 0)
                for i, user in enumerate(expense.recipients)
            }
        else:
            if expense.custom_split is None:
                return
            owed_cents = {user_id: round(amt * 100) for user_id, amt in expense.custom_split.items()}
            if sum(owed_cents.values()) != total_cents:
                return

        # Check inputs
        if any(user_id not in self.users for user_id in owed_cents):
            return
        if any(cents < 0 for cents in owed_cents.values()):
            return

        for user_id, cents in owed_cents.items():
            # The payer's own share is not a debt
            if user_id == payer.id:
                continue
            self.owed[user_id][payer.id] += cents

    def pay_expenses(self, payer: User, recipient: User, amt: float) -> None:
        amt_cents = round(amt * 100)
        if payer.id not in self.users or recipient.id not in self.users:
            return
        if recipient.id not in self.owed[payer.id] or amt_cents > self.owed[payer.id][recipient.id]:
            return

        self.owed[payer.id][recipient.id] -= amt_cents # non-negative amount owed after this operation

    def report_expenses(self, user_id: str) -> None:
        if user_id not in self.users:
            return

        net_owed = defaultdict(int, self.owed[user_id])
        # At this point net_owed doesn't consider how much others owe user_id

        for user, owed in self.owed.items():
            # Check with `in` first, because indexing a missing debt would insert a zero entry
            if user != user_id and user_id in owed:
                net_owed[user] -= owed[user_id]

        for other, cents in net_owed.items():
            print(f"User {user_id} owes {other} a total of {cents / 100:.2f} dollars.")

'''
Feedback:
- Good clarifying questions included customizing splits, thinking about it like a real product.
- Could've asked more targeted clarifying questions to limit scope earlier on.
- Try to have discussions about product design during implementation.
- Good to explicitly explain decisions, such as user id vs. User class

Concerns:
- No tests; print is ok; important to have at least 1 testing path
- When asking clarifying questions initially each needs to eliminate a search space and tell me what to focus on
- Imprecise when dealing with money balances; could do everything in cents (smallest unit) and then distribute any remainder
    - This is important to bring up just to mention that you noticed it.
'''

'''
Improvements:
- An equal split that lists the same recipient twice loses one share, so $3.00 split over [A, A, B] records only $2.00 of debt. Reject or merge duplicate recipients.
- pay_expenses accepts a zero or negative amount, and a negative payment increases the debt. Reject amounts <= 0.
- Invalid input returns silently, so the caller can't tell a rejected expense or payment from an accepted one. Raise ValueError or return a success flag.
- Expense.id is never stored, so retrying add_expense with the same expense charges every share twice. Keep the ids already added and ignore repeats.
- pay_expenses checks a payment against the one-way debt, while report_expenses shows the net balance, so a payment the report says isn't owed can still go through. Settle against the net balance.
- report_expenses prints money owed to the user as a negative debt and prints settled balances as 0.00. Print "X owes you" for negative amounts and skip zeros.
'''

