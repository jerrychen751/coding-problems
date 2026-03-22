def is_palindrome(s: str) -> bool:
    left, right = 0, len(s) - 1
    while left < right:
        if s[left] != s[right]:
            return False
        
        left += 1
        right -= 1

    return True

def largest_palindrome_product(digits: int) -> int:
    largest_palindrome = 0

    for i in range(1, 10**digits):
        for j in range(1, 10**digits):
            product = i * j
            if is_palindrome(str(product)) and product > largest_palindrome:
                largest_palindrome = product    
    
    return largest_palindrome

print(largest_palindrome_product(3))