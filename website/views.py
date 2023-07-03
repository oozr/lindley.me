from flask import Blueprint, render_template, request
from helpers import estimate_cefr_level, estimate_gse_level, convert_cefr_to_gse
import sqlite3
import textstat
import spacy

views = Blueprint('views', __name__)

@views.route('/')
def home():
    return render_template("home.html")

@views.route('/blog')
def blog():
    return render_template("blog.html")

#GSE Analyser
@views.route('/gse_analyser', methods = ["GET", "POST"])
def gse_analyser():
    if request.method == "POST":
        conn = sqlite3.connect('vocabulary.db')
        db = conn.cursor()
        #only load the lemmatizer part of the pipeline for quicker load time
        nlp = spacy.load("en_core_web_sm")   
        data = request.form['text']
        level = textstat.flesch_reading_ease(data)
        index = "Flesch-Kincaid"
        cefr = estimate_cefr_level(index, level)
        sentence = nlp(data) 
        print(f"the sentence is {sentence}")
        gse_total = 0
        number_of_words = 0
        average_gse = 0
        words_not_found = []
        for word in sentence:
            #should i open this before the for loop?
            lemma = word.lemma_
            print(lemma)
            #can I not do this in one command?
            db.execute("SELECT link_table_id FROM vocabulary_table WHERE word=?", [lemma])
            result = db.fetchone()
            if result:
                id = db.execute("SELECT link_table_id FROM vocabulary_table WHERE word=?", [lemma])
                id_value = str(id.fetchall()[0][0])
                print(f"the id_value is {id_value}")
                word_score = db.execute("SELECT gse FROM link_table WHERE id=?",[id_value])
                word_score_value = str(word_score.fetchall()[0][0])
                print(f"the word_score is {word_score_value}")
                gse_total = gse_total + int(word_score_value)
                number_of_words += 1
            else:
                words_not_found.append(word)
                continue
            average_gse = gse_total/number_of_words
        print(f"The average GSE score for this text is:{average_gse}")
        conn.close()
        overall_gse = round(estimate_gse_level(level, average_gse))
        overall_cefr = convert_cefr_to_gse(overall_gse)
        return render_template('gse_result.html', overall_gse = overall_gse, overall_cefr = overall_cefr, words_not_found = words_not_found)  
    #Otherwise a GET request will just render the HTML
    return render_template("gse_analyser.html")

@views.route('/cefr_analyser', methods = ["GET", "POST"])
def cefr_analyser():
    if request.method == "POST":
        data = request.form['text']
        language = request.form['language']
        # Calculate the level using the regional varient of text analyser
        if language == "Arabic":
            index = "Osman"
            level = textstat.osman(data)
        elif language == "English":
            index = "Flesch-Kincaid"
            level = textstat.flesch_reading_ease(data)
        elif language == "German":
            index = "Wiener Sachtextformel"
            variant = 1
            level = textstat.wiener_sachtextformel(data, variant)
        elif language == "Italian":
            index = "Gulpease"
            level = textstat.gulpease_index(data)
        elif language == "Spanish":
            index = "Fernandez-Huerta"
            level = textstat.fernandez_huerta(data)
        cefr = estimate_cefr_level(index, level)
        return render_template('cefr_result.html', cefr=cefr, language=language, index=index, level=level)  
    #Otherwise a GET request will just render the HTML
    return render_template("cefr_analyser.html")