def grade_student(score):
    if score >= 90 and score <= 100:
        return 'A'
    elif score >= 80 and score <= 89:
        return 'B'
    elif score >= 70 and score <= 79:
        return 'C'
    elif score >= 60 and score <= 69:
        return 'D'
    else:
        return 'F'

# Test cases
if __name__ == "__main__":
    print(grade_student(92))  # Should print 'A'
    print(grade_student(76))  # Should print 'C'
    print(grade_student(59))  # Should print 'F' 