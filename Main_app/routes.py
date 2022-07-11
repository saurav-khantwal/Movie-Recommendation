from flask import render_template
from Main_app import app, utils
from Main_app.forms import Recommend_movies_form, Discover_movies_form
import json



@app.route('/')
@app.route('/home')
def home_page():
    return render_template('home.html')


@app.route('/recommend', methods=['POST', 'GET'])
def recommend_page():
    form = Recommend_movies_form()
    if form.validate_on_submit():
        recommended_movies = utils.get_recommendations(form.input_movie.data)
        return render_template('recommend.html', form = form, suggestions = json.dumps(utils.movies_data.title.values.tolist()), output_movies = recommended_movies, rec=True)

    return render_template('recommend.html', form = form, suggestions = json.dumps(utils.movies_data.title.values.tolist()), rec=True)


@app.route('/discover', methods=['POST', 'GET'])
def discover_page():
    form = Discover_movies_form()
    if form.validate_on_submit():
        discovered_movies = utils.get_discovered_movies(form.input_movie.data)
        return render_template('recommend.html', form = form, suggestions = json.dumps(utils.get_names()), output_movies = discovered_movies)
    return render_template('recommend.html', form = form, suggestions = json.dumps(utils.get_names()), output_movies = utils.get_default_movies())