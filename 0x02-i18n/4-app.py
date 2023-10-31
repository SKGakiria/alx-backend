#!/usr/bin/env python3
"""Script that starts a Flask web application"""
from flask import Flask, render_template, request
from flask_babel import Babel


app = Flask(__name__)
babel = Babel(app)


class Config(object):
    """Config class to handle the Babel language settings"""
    LANGUAGES = ["en", "fr"]
    BABEL_DEFAULT_LOCALE = "en"
    BABEL_DEFAULT_TIMEZONE = "UTC"


app.config.from_object(Config)


@babel.localeselector
def get_locale():
    """Function to invoke each request, selecting and returning the best
    language match based on the supported languages"""
    loca = request.args.get('locale')
    if loca in app.config['LANGUAGES']:
        return loca
    return request.accept_languages.best_match(app.config['LANGUAGES'])


@app.route('/', strict_slashes=False)
def index() -> str:
    """Handles the single / route"""
    return render_template('4-index.html')


if __name__ == "__main__":
    app.run(port="5000", host="0.0.0.0", debug=True)
