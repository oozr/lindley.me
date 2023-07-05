import string
import spacy
nlp = spacy.load('en_core_web_sm')


def estimate_gse_level(level, average_gse):
    #make sure there aren't any values over 100
    if level >= 100:
        level = 100
    #convert klish reading level numeric value to a GSE score. THIS SHOULD ALLIGN WITH CEFR VALUES TO BE CORRECT
    gse_reading_index = ((100 - level) / 100) * 80 + 10
    if average_gse >=50:
        average_gse = 50
    #turn 10 to 10, 25 to 50, 40 to 90. The below formula works is i'm getting a nice spread between 10 and 50. If frequently more than 40 then i need to increase the max and 30 by the same amount
    improved_average_gse = ((average_gse-10)/40*100)/100*80+10
    #calculate overall gse level by weighting reading level and gse vocabulary score 2:1 (DIVIDE BY 4 BECAUSE IT'S DIVIDING THE AVAERAGE (/2) BY 2)
    overall_gse = gse_reading_index + ((improved_average_gse - gse_reading_index) / 4)
    return overall_gse

def clean_words_not_found(words_not_found):
    no_punct = [str(word).translate(str.maketrans('', '', string.punctuation + string.digits + string.whitespace + "★👍")) for word in words_not_found]
    #remove proper nouns
    no_proper_nouns = [token.text for token in nlp(" ".join(no_punct)) if not token.pos_ == 'PROPN']
    #remove duplicate words
    no_duplicates = list(set(no_proper_nouns))
    #remove empty strings
    no_duplicates = [word for word in no_duplicates if word]
    clean_output = ', '.join(no_duplicates)
    return clean_output

def convert_cefr_to_gse(overall_gse):
        if 10 <= overall_gse <= 21:
            cefr = "<A1"
        elif 22 <= overall_gse <= 29:
            cefr = "A1"
        elif 30 <= overall_gse <= 35:
            cefr = "A2"
        elif 36 <= overall_gse <= 42:
            cefr = "A2+"
        elif 43 <= overall_gse <= 50:
            cefr = "B1"
        elif 51 <= overall_gse <= 58:
            cefr = "B1+"
        elif 59 <= overall_gse <= 66:
            cefr = "B2"
        elif 67 <= overall_gse <= 75:
            cefr = "B2+"
        elif 76 <= overall_gse <= 85:
            cefr = "C1"
        else:
            cefr = "C2"
        return cefr

def estimate_cefr_level(index, level):
    if index == "Flesch-Kincaid":
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
    