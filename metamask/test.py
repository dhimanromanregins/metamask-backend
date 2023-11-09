import random

# A list of meaningful words
meaningful_words = [
    "apple", "banana", "chocolate", "dolphin", "elephant",
    "flower", "guitar", "happiness", "island", "jazz",
    "kangaroo", "laughter", "mountain", "ocean", "piano",
    "rainbow", "sunshine", "tree", "unicorn", "victory",
    "waterfall", "xylophone", "yogurt", "zeppelin"
]

def generate_secret_security_phrase():
    # Shuffle the list of words
    random.shuffle(meaningful_words)

    # Select the first 12 words
    selected_words = meaningful_words[:12]

    # Create a list of (index, word) pairs
    word_indices = [(i, word) for i, word in enumerate(selected_words)]

    return word_indices

# Example usage
security_phrase_indices = generate_secret_security_phrase()
for index, word in security_phrase_indices:
    print(f"{index + 1}: {word}")
