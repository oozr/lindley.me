from flask import Blueprint, render_template, request
import sqlite3
import textstat
import spacy
from helpers import GSELevelEstimator, WordProcessor, CEFRConverter, language_mappings

views = Blueprint('views', __name__)

class BaseAnalyser:
    def __init__(self, template_name):
        self.template_name = template_name

    def render_template(self, **context):
        return render_template(self.template_name, **context)

    def analyse(self):
        pass

class GSEAnalyser(BaseAnalyser):
    def __init__(self):
        super().__init__('gse_analyser.html')

    #look up the words in the GSE 35000 table to get gse_scores, words_not_found and found_words
    def _get_gse_scores(self, data):       
        conn = sqlite3.connect('vocabulary.db')
        db = conn.cursor()
        nlp = spacy.load("en_core_web_sm")
        sentence = nlp(data)
        gse_scores = []
        words_not_found = []
        found_words = {}

        for word in sentence:
            lemma = word.lemma_
            db.execute("SELECT link_table_id FROM vocabulary_table WHERE word=?", [lemma])
            result = db.fetchone()
            if result:
                id_value = str(result[0])
                word_score = db.execute("SELECT gse FROM link_table WHERE id=?", [id_value])
                word_score_value = str(word_score.fetchone()[0])
                found_words[word_score_value] = lemma
                gse_scores.append(int(word_score_value))
            else:
                words_not_found.append(word)

        conn.close()

        return gse_scores, words_not_found, found_words
    
    #estimate gse level by combining Flesch_reading_ease with average GSE word score. Return a cleaned up list of words_not_found and found_words
    def analyse(self, data):
        # Calculate the Flesch reading ease level of the data
        flesch_reading_level = textstat.flesch_reading_ease(data)

        # Get GSE scores, words_not_found, and found_words
        gse_scores, words_not_found, found_words = self._get_gse_scores(data)
        number_of_words = len(gse_scores)

        # If no GSE scores found, return None for all results
        if number_of_words == 0:
            return None, None, None, None

        # Calculate the average GSE score
        average_gse = sum(gse_scores) / number_of_words

        # Clean up words_not_found and find the top words to learn
        word_processor = WordProcessor()
        none_words = word_processor.clean_words_not_found(words_not_found)
        learn_words = word_processor.words_to_learn(found_words)

        # Estimate the overall GSE level and convert it to CEFR
        gse_level_estimator = GSELevelEstimator()
        overall_gse = round(gse_level_estimator.estimate_gse_level(flesch_reading_level, average_gse))
        index = "GSE_CEFR"
        cefr_converter = CEFRConverter()
        overall_cefr = cefr_converter.convert_to_cefr(overall_gse, index)

        return overall_gse, overall_cefr, none_words, learn_words


class CefrAnalyser(BaseAnalyser):
    def __init__(self):
        super().__init__('cefr_analyser.html')

    def analyse(self, data, language):

        if language in language_mappings:
            mapping = language_mappings[language]
            index = mapping["index"]
            readability_func = mapping["readability_func"]

            #German is the only language that needs a 'variant' for the analyser
            if language == "German":
                level = readability_func(data, variant=mapping.get("variant", 1))
            else:
                level = readability_func(data)

            if level is not None:
                cefr_converter = CEFRConverter()
                cefr = cefr_converter.convert_to_cefr(level, index=index)
                print(cefr)
                return cefr, language, index, level

        return None, None, None, None


@views.route('/')
def home():
    return render_template("home.html")

@views.route('/blog')
def blog():
    return render_template("blog.html")

@views.route('/gse_analyser', methods=["GET", "POST"])
def gse_analyser():
    if request.method == "POST":
        data = request.form['text']
        gse_analyser = GSEAnalyser()
        overall_gse, overall_cefr, none_words, learn_words = gse_analyser.analyse(data)

        if overall_gse is not None:
            return render_template('gse_result.html', overall_gse=overall_gse, overall_cefr=overall_cefr, none_words=none_words, learn_words=learn_words)
        else:
            return gse_analyser.render_template()

    return render_template("gse_analyser.html")

@views.route('/cefr_analyser', methods=["GET", "POST"])
def cefr_analyser():
    if request.method == "POST":
        data = request.form['text']
        language = request.form['language']
        cefr_analyser = CefrAnalyser()
        cefr, language, index, level = cefr_analyser.analyse(data, language)

        if cefr is not None:
            return render_template('cefr_result.html', cefr=cefr, language=language, index=index, level=level)
        else:
            return cefr_analyser.render_template()

    return render_template("cefr_analyser.html")

