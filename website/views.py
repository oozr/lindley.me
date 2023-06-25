from flask import Blueprint, render_template

views = Blueprint('views', __name__)

@views.route('/')
def home():
    return render_template("home.html")

@views.route('/blog')
def blog():
    return render_template("blog.html")

@views.route('/text_analyzer')
def text_analyzer():
    return render_template("text_analyzer.html")

