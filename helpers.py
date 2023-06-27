"""
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
"""

def estimate_cefr_level(index, level):
    if index == "Gulpease":
        if level >= 100:
            cefr = "<A1"
        elif 100 > level >= 85:
            cefr = "A1"
        elif 85 > level >= 65:
            cefr = "A2"
        elif 65 > level >= 50:
            cefr = "B1"
        elif 50 > level >= 40:
            cefr = "B2"
        elif 40 > level >= 30:
            cefr = "C1"
        else:
            cefr = "C2"
    elif index == "Osman":
        if level >= 100:
            cefr = "<A1"
        elif 100 > level >= 90:
            cefr = "A1"
        elif 90 > level >= 80:
            cefr = "A2"
        elif 80 > level >= 70:
            cefr = "B1"
        elif 70 > level >= 60:
            cefr = "B2"
        elif 60 > level >= 50:
            cefr = "C1"
        else:
            cefr = "C2"
    elif index == "Fernandez-Huerta":
        if level >= 100:
            cefr = "<A1"
        elif 100 > level >= 95:
            cefr = "A1"
        elif 95 > level >= 90:
            cefr = "A2"
        elif 90 > level >= 80:
            cefr = "B1"
        elif 80 > level >= 70:
            cefr = "B2"
        elif 70 > level >= 60:
            cefr = "C1"
        else:
            cefr = "C2"
    elif index == "Wiener Sachtextformel":
        if 0 <= level < 1:
            cefr = "<A1"
        elif 1 <= level < 3:
            cefr = "A1"
        elif 3 <= level < 6:
            cefr = "A2"
        elif 6 <= level < 9:
            cefr = "B1"
        elif 9 <= level < 12:
            cefr = "B2"
        elif 13 <= level < 15:
            cefr = "C1"
        else:
            cefr = "C2"
    
    return cefr
    