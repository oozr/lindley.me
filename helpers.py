import string
import spacy
import textstat

class GSELevelEstimator:
    def __init__(self):
        pass

    def estimate_gse_level(self, level, average_gse):
        #make sure there aren't any values over 100 to simplify the conversion
        if level >= 100:
            level = 100
        #convert klish reading level numeric value to a GSE score. THIS SHOULD ALLIGN WITH CEFR VALUES TO BE CORRECT
        gse_reading_index = ((100 - level) / 100) * 80 + 10
        #This is a manual fix for now, as scores tend to be less than 50. NEXT STEP IS TO REMOVE STOP WORDS
        if average_gse >=50:
            average_gse = 50
        #turn 10 to 10, 25 to 50, 40 to 90. The below formula works is i'm getting a nice spread between 10 and 50. If frequently more than 40 then i need to increase the max and 30 by the same amount
        improved_average_gse = ((average_gse-10)/40*100)/100*80+10
        #calculate overall gse level by weighting reading level and gse vocabulary score 2:1 (DIVIDE BY 4 BECAUSE IT'S DIVIDING THE AVAERAGE (/2) BY 2)
        overall_gse = gse_reading_index + ((improved_average_gse - gse_reading_index) / 4)
        return overall_gse


class WordProcessor:
    def __init__(self):
        self.nlp = spacy.load('en_core_web_sm')

    def clean_words_not_found(self, words_not_found):
        # Convert each token to a string
        words_as_strings = [word.text for word in words_not_found]
        # Remove punctuation and special characters from each word
        no_punct = [word.translate(str.maketrans('', '', string.punctuation + "★👍")) for word in words_as_strings]
        # Remove proper nouns
        no_proper_nouns = [word for word in no_punct if not any(token.pos_ == 'PROPN' for token in self.nlp(word))]
        # Remove duplicate words
        no_duplicates = list(set(no_proper_nouns))
        cleaned_output = ' '.join(no_duplicates)
        # Return intermediate results as a tuple
        return cleaned_output

    def words_to_learn(self, found_words):
        #order the dictionary found_words by GSE score, left to right into a new list, max 10 words
        ordered_words = dict(sorted(found_words.items(), key=lambda x: int(x[0])))
        new_list = []
        for i in range(len(ordered_words)):
            new_list.append(ordered_words.popitem())
            if i == 9:
                break
        return new_list


class CEFRConverter:
    def __init__(self):
        # Define the conversion ranges and mappings for different indices
        self.conversion_ranges = {
            "GSE_CEFR": [(84, "C2"), (75, "C1"), (66, "B2+"), (58, "B2"), (50, "B1+"), (42, "B1"), (35, "A2+"), (29, "A2"), (21, "A1"), (0, "<A1")],
            "Flesch-Kincaid": [(100, "<A1"), (90, "A1"), (80, "A2"), (70, "B1"), (60, "B2"), (50, "C1"), (0, "C2")],
            "Gulpease": [(100, "<A1"), (85, "A1"), (65, "A2"), (50, "B1"), (40, "B2"), (30, "C1"), (0, "C2")],
            "Osman": [(100, "<A1"), (90, "A1"), (80, "A2"), (70, "B1"), (60, "B2"), (50, "C1"), (0, "C2")],
            "Fernandez-Huerta": [(100, "<A1"), (95, "A1"), (90, "A2"), (80, "B1"), (70, "B2"), (60, "C1"), (0, "C2")],
            "Wiener Sachtextformel": [(100, "<A1"), (1, "A1"), (3, "A2"), (6, "B1"), (9, "B2"), (12, "C1"), (0, "C2")]
        }

    def convert_to_cefr(self, level, index):
        cefr = None
        if index in self.conversion_ranges:
            for x, y in self.conversion_ranges[index]:
                if level >= x:
                    cefr = y
                    break
            else:
                cefr = "C2"  # If level is lower than 0 (lowest score in the conversion range for all except GSE_CEFR which is bounded)
        else:
            cefr = "N/A"  # Handle invalid index

        return cefr
    
# Language mappings dictionary to be used in the CEFR conversion 
language_mappings = {
    "Arabic": {
        "index": "Osman",
        "readability_func": textstat.osman,
    },
    "English": {
        "index": "Flesch-Kincaid",
        "readability_func": textstat.flesch_reading_ease,
    },
    "German": {
        "index": "Wiener Sachtextformel",
        "readability_func": textstat.wiener_sachtextformel,
    },
    "Italian": {
        "index": "Gulpease",
        "readability_func": textstat.gulpease_index,
    },
    "Spanish": {
        "index": "Fernandez-Huerta",
        "readability_func": textstat.fernandez_huerta,
    },
}