#!/usr/bin/env python3
"""Script that starts a Flask web application"""
from flask import Flask, render_template, request, g
from flask_babel import Babel
from typing import Dict, Union
from datetime import timezone as tmzn
from pytz import timezone
import pytz.exceptions


app = Flask(__name__)
babel = Babel(app)


users = {
    1: {"name": "Balou", "locale": "fr", "timezone": "Europe/Paris"},
    2: {"name": "Beyonce", "locale": "en", "timezone": "US/Central"},
    3: {"name": "Spock", "locale": "kg", "timezone": "Vulcan"},
    4: {"name": "Teletubby", "locale": None, "timezone": "Europe/London"},
}


class Config(object):
    """Config class to handle the Babel language settings"""
    LANGUAGES = ["en", "fr"]
    BABEL_DEFAULT_LOCALE = "en"
    BABEL_DEFAULT_TIMEZONE = "UTC"


app.config.from_object(Config)


def get_user() -> Union[Dict, None]:
    """Function returns a user dict or None if ID can't be found
    or if 'login_as' isn't passed"""
    id = request.args.get('login_as', None)
    if id is not None and int(id) in users.keys():
        return users.get(int(id))
    return None


@app.before_request
def before_request():
    """Finds a user if any, and sets it as a global on flask.g.user"""
    user = get_user()
    g.user = user


@babel.localeselector
def get_locale():
    """Function to invoke each request, selecting and returning the best
    language match based on the supported languages"""
    loca = request.args.get('locale')
    if loca in app.config['LANGUAGES']:
        return loca
    if g.user:
        loca = g.user.get('locale')
        if loca and loca in app.config['LANGUAGES']:
            return loca
    loca = request.headers.get('locale', None)
    loca = request.args.get('locale')
    if loca in app.config['LANGUAGES']:
        return loca
    return request.accept_languages.best_match(app.config['LANGUAGES'])


@babel.timezoneselector
def get_timezone():
    """Function to invoke each request, selecting and returning the
    appropriate timezone"""
    tmzone = request.args.get('timezone', None)
    if tmzone:
        try:
            return timezone(tmzone).zone
        except pytz.exceptions.UnknownTimeZoneError:
            pass
    if g.user:
        try:
            tmzone = g.user.get('timezone')
            return timezone(tmzone).zone
        except pytz.exceptions.UnknownTimeZoneError:
            pass
    deflt = app.config['BABEL_DEFAULT_TIMEZONE']
    return deflt


@app.route('/', strict_slashes=False)
def index() -> str:
    """Handles the single / route"""
    return render_template('7-index.html')


if __name__ == "__main__":
    app.run(port="5000", host="0.0.0.0", debug=True)
