from flask import Flask

def create_app():
    app = Flask(__name__)
    app.config['SECRET KEY'] = 'f610ffb272ab349ca3b274f8a7411e11'
    
    from .views import views

    app.register_blueprint(views, url_prefix='/')

    return app
