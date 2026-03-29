def sum_of_squares(n: int) -> int:
    """Return the sum of the squares of the first n natural numbers."""
    return n * (n + 1) * (2*n + 1) // 6

def square_of_sums(n: int) -> int:
    """Return the square of the sum of the first n natural numbers."""
    return sum(range(1, n + 1)) ** 2

print(square_of_sums(100) - sum_of_squares(100))