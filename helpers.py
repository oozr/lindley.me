import textstat

def calculate_coleman_liau_index(text):
    # Add the Coleman-Liau index calculation code here
    char_count = len([char for char in text if char.isalnum()])
    word_count = len(text.split())
    sentence_count = len([char for char in text if char in ['.', '?', '!']])
    L = (char_count / word_count) * 100
    S = (sentence_count / word_count) * 100
    score = round(0.0588 * L - 0.296 * S - 15.8, 2)

    return score

def estimate_cefr_level(text):
    # calculate the Flesch-Kincaid Grade Level of the text
    fkg = textstat.flesch_kincaid_grade(text)
    # convert the Flesch-Kincaid Grade Level to a CEFR level using the CEFR scale
    if fkg <= 5:
        cefr = "A2"
    elif fkg <= 6:
        cefr = "B1"
    elif fkg <= 7:
        cefr = "B2"
    elif fkg <= 8:
        cefr = "C1"
    else:
        cefr = "C2"
    
    return cefr