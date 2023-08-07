from flask import Blueprint, render_template, request
import os
import markdown
from urllib.parse import urljoin

views = Blueprint('views', __name__)

BLOG_DIR = "blog_posts"

class Blog:
    def __init__(self):
        self.blog_posts = self.generate_blog_post_objects()

    @staticmethod
    def read_markdown_file(file_path):
        with open(file_path, "r", encoding="utf-8") as file:
            return file.read()

    def generate_blog_post_objects(self):
        markdown_files = sorted(
            [filename for filename in os.listdir(BLOG_DIR) if filename.endswith(".md")]
        )

        blog_posts = []

        for filename in markdown_files:
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

                # Get video filenames from the raw post content (Markdown)
                video_filenames = re.findall(r"\[video\]\((.*?)\)", blog_post["content"])

                # Convert relative image URLs to absolute URLs
                image_urls = [urljoin(request.base_url, url) for url in image_urls]

                # Add the image URLs to the blog post object
                blog_post["image_urls"] = image_urls

                # Add the video filenames to the blog post object
                blog_post["video_files"] = video_filenames

                return blog_post

        return None





blog_instance = Blog()

@views.route('/')
def blog_home():
    blog_posts = blog_instance.blog_posts
    return render_template("blog.html", blog_posts=blog_posts)

@views.route('/<int:post_id>')
def blog_post(post_id):
    blog_post = blog_instance.get_blog_post_by_id(post_id)
    if blog_post:
        return render_template("blog_post.html", blog_post=blog_post)
    else:
        return "Blog post not found.", 404
