def largest_prime(num: int) -> int:
    """Return the largest prime factor of a positive integer."""
    factor = 2
    while factor * factor <= num:
        while num % factor == 0:
            num //= factor
        
        factor += 1
    
    return num if num > 1 else factor # if num > 1, then the number itself is prime

target = 600851475143
print(largest_prime(target))
    