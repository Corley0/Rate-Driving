from flask import Flask
from config import Config
from flask_login import LoginManager


app = Flask(__name__)
app.config.from_object(Config)
login = LoginManager(app)
login.init_app(app)


from app import routes
from app.forms import SearchForm

@app.context_processor
def inject_search_form():
    return dict(search_form=SearchForm())