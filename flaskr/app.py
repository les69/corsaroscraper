from flask import Flask, abort
from scraping.view.movie_scraper import get_latest, get_movie, get_movie_details
from scraping.view.translator import get_english_moviename
import json
app = Flask(__name__)



@app.route('/')
def say_hi():
    return 'hi'

@app.route('/latest', methods=['GET'])
def get_latest_movies():
    json_result = get_latest()
    return app.response_class(json_result, content_type='application/json')\

@app.route('/search/<movie>', methods=['GET'])
def search_movie(movie):
    json_result = get_movie(movie.replace(" ","+"))
    return app.response_class(json_result, content_type='application/json')

@app.route('/details/<movieid>', methods=['GET'])
def get_details(movieid):
    json_result = get_movie_details(movieid)
    return app.response_class(json_result, content_type='application/json')

@app.route('/wiki/it/<moviename>/en/', methods=['GET'])
def get_translation(moviename):
    name = get_english_moviename(movie_name=moviename)

    if name == "":
        abort(404)
    res = {}
    res['title'] = name
    return app.response_class(json.dumps(res), content_type='application/json')


if __name__ == "__main__":
    app.run(port=5000, debug=False)