from website import create_app
import os
from flask_flatpages import FlatPages

app = create_app()

if __name__ == '__main__':
    app.run(debug=False, port=os.getenv("PORT", default=5000))
#turn this off when running in production