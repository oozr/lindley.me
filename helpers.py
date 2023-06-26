def calculate_coleman_liau_index(text):
    # Add the Coleman-Liau index calculation code here
    char_count = len([char for char in text if char.isalnum()])
    word_count = len(text.split())
    sentence_count = len([char for char in text if char in ['.', '?', '!']])
    L = (char_count / word_count) * 100
    S = (sentence_count / word_count) * 100
    score = round(0.0588 * L - 0.296 * S - 15.8, 2)

    return score