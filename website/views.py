from flask import Blueprint, render_template, request
from helpers import calculate_coleman_liau_index, estimate_cefr_level

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
        data = request.form['text']
        # Calculate the Coleman-Liau index, formula found in helpers.py
        score = calculate_coleman_liau_index(data)
        grade = int(round(score))
        cefr = estimate_cefr_level(data)
        return render_template('gse_result.html', score=score, grade=grade, cefr=cefr)  
    #Otherwise a GET request will just render the HTML
    return render_template("gse_analyser.html")

@views.route('/cefr_analyser', methods = ["GET", "POST"])
def cefr_analyser():
    if request.method == "POST":
        data = request.form['text']
        language = request.form['language']
        # Calculate the Coleman-Liau index, formula found in helpers.py
        cefr = estimate_cefr_level(data)
        return render_template('cefr_result.html', cefr=cefr, language=language)  
    #Otherwise a GET request will just render the HTML
    return render_template("cefr_analyser.html")