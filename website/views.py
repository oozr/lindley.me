from flask import Blueprint, render_template, request
import sqlite3
import os
import markdown
from urllib.parse import urljoin
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
            
            if lemma.lower() != 'to':
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
                return cefr, language, index, level

        return None, None, None, None


BLOG_DIR = "blog_posts"

class Blog:
    def __init__(self):
        self.blog_posts = self.generate_blog_post_objects()

    @staticmethod
    def read_markdown_file(file_path):
        with open(file_path, "r", encoding="utf-8") as file:
            return file.read()

    def generate_blog_post_objects(self):
        blog_posts = []

        for filename in os.listdir(BLOG_DIR):
            if filename.endswith(".md"):
                file_path = os.path.join(BLOG_DIR, filename)
                content = self.read_markdown_file(file_path)

                # Assume that the metadata lines are separated from the content by a double newline
                metadata_lines, post_content = content.split("\n\n", 1)

                # Remove lines that start with '#' or '##' from the post_content
                cleaned_post_content = "\n".join(line for line in post_content.splitlines() if not line.strip().startswith('#'))

                # Parse metadata from metadata_lines
                metadata = {}
                for line in metadata_lines.splitlines():
                    key, value = line.split(":", 1)
                    metadata[key.strip()] = value.strip()

                # Truncate the cleaned_post_content to the first 50 words to use as the excerpt
                excerpt_words = cleaned_post_content.split()[:50]
                excerpt = " ".join(excerpt_words) + "..." if len(excerpt_words) >= 50 else cleaned_post_content

                # Convert the Markdown content to HTML
                html_content = markdown.markdown(post_content)

                # Store the blog post object
                blog_post = {
                    "id": len(blog_posts) + 1,  # Assign a unique ID based on the index
                    "title": metadata.get("Title", "Untitled"),
                    "date": metadata.get("Date", ""),
                    "author": metadata.get("Author", ""),
                    "excerpt": excerpt,
                    "content": html_content,  # Store the HTML content
                }
                blog_posts.append(blog_post)

        return blog_posts

    def get_blog_post_by_id(self, post_id):
        for blog_post in self.blog_posts:
            if blog_post["id"] == post_id:
                # Get image URLs from the raw post content (Markdown)
                import re
                image_urls = re.findall(r"!\[[^\]]*\]\((.*?)\)", blog_post["content"])

                # Convert relative image URLs to absolute URLs
                image_urls = [urljoin(request.base_url, url) for url in image_urls]

                # Add the image URLs to the blog post object
                blog_post["image_urls"] = image_urls

                return blog_post

        return None

blog_instance = Blog()

@views.route('/')
def home():
    return render_template("home.html")

@views.route('/blog')
def blog_home():
    blog_posts = blog_instance.blog_posts
    return render_template("blog.html", blog_posts=blog_posts)

@views.route('/blog/<int:post_id>')
def blog_post(post_id):
    blog_post = blog_instance.get_blog_post_by_id(post_id)
    if blog_post:
        return render_template("blog_post.html", blog_post=blog_post)
    else:
        return "Blog post not found.", 404

from flask import redirect, url_for

@views.route('/gse_analyser', methods=["GET", "POST"])
def gse_analyser():
    if request.method == "POST":
        data = request.form['text']

        # Check if the text input is empty
        if not data.strip():
            # If the text input is empty, redirect back to the same page (GET method)
            return redirect(url_for('views.gse_analyser'))

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
        
        # Check if the text input is empty
        if not data.strip():
            # If the text input is empty, redirect back to the same page (GET method)
            return redirect(url_for('views.cefr_analyser'))

        cefr_analyser = CefrAnalyser()
        cefr, language, index, level = cefr_analyser.analyse(data, language)

        if cefr is not None:
            return render_template('cefr_result.html', cefr=cefr, language=language, index=index, level=level)
        else:
            return cefr_analyser.render_template()

    return render_template("cefr_analyser.html")

