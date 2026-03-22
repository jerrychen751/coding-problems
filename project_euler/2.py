total = 2
limit = 4_000_000

def fibonacci(prev1: int, prev2: int) -> int:
    return prev1 + prev2

# Set base fibonacci sequence values
prev1 = 1
prev2 = 2
next_val = fibonacci(prev1, prev2)

while next_val <= limit:
    if next_val & 1 == 0:
        total += next_val

    prev1 = prev2
    prev2 = next_val
    next_val = fibonacci(prev1, prev2)

print(total)