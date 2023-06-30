from flask import Blueprint, render_template, request
from helpers import estimate_cefr_level
import textstat
import spacy

views = Blueprint('views', __name__)

@views.route('/')
def home():
    return render_template("home.html")

@views.route('/blog')
def blog():
    return render_template("blog.html")

@views.route('/gse_analyser', methods = ["GET", "POST"])
def gse_analyser():
    if request.method == "POST":
                #only load the lemmatizer part of the pipeline for quicker load time
        nlp = spacy.load("en_core_web_sm")   
        data = request.form['text']
        level = textstat.flesch_reading_ease(data)
        index = "Flesch-Kincaid"
        cefr = estimate_cefr_level(index, level)
        sentence = nlp(data)
        for word in sentence:
            print(word.lemma_)
            #fetch score of each word to sql table
        return render_template('gse_result.html', index = index, level=level, cefr = cefr)  
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