def is_palindrome(s: str) -> bool:
    # Step 1: Convert to lowercase and remove all spaces and punctuation
    text = ""
    for char in s:
        if char.isalnum():  # Only keep letters and numbers
            text += char.lower()
    
    # Step 2: Compare the string with its reverse
    # If they are equal, it's a palindrome
    return text == text[::-1]

# Test cases
if __name__ == "__main__":
    print(is_palindrome("racecar"))        # True
    print(is_palindrome("hello"))          # False
    
    # Additional test cases
    print("Test 3:", is_palindrome("race a car"))  # False
    print("Test 4:", is_palindrome("Was it a car or a cat I saw?"))  # True
    print("Test 5:", is_palindrome("12321"))  # True
    print("Test 6:", is_palindrome(""))  # True (empty string is considered a palindrome) 