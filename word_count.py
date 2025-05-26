def word_count(text):
    # Split the text into words and create a dictionary to store counts
    words = text.split()
    word_dict = {}
    
    # Count occurrences of each word
    for word in words:
        if word in word_dict:
            word_dict[word] += 1
        else:
            word_dict[word] = 1
    
    return word_dict

if __name__ == "__main__":
    # Test case
    text = "the quick brown fox jumps over the lazy dog the fox"
    result = word_count(text)
    print("Word frequencies:", result) 