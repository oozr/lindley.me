from flask import Blueprint, render_template, request
from helpers import calculate_coleman_liau_index

views = Blueprint('views', __name__)

@views.route('/')
def home():
    return render_template("home.html")

@views.route('/blog')
def blog():
    return render_template("blog.html")

@views.route('/text_analyzer', methods = ["GET", "POST"])
def text_analyzer():
    if request.method == "POST":
        data = request.form['text']
        # Calculate the Coleman-Liau index, formula found in helpers.py
        score = calculate_coleman_liau_index(data)
        grade = int(round(score))
        return render_template('result.html', score=score, grade=grade)  


    #Otherwise a GET request will just render the HTML
    return render_template("text_analyzer.html")