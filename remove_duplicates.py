def remove_duplicates(lst):
    seen = set()
    result = []
    for item in lst:
        if item not in seen:
            seen.add(item)
            result.append(item)
    return result

# Just one test case
test = ['3', '1', '2', '3', '2', '4']
result = remove_duplicates(test)
print("Result:", result) 