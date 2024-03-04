# app.py
from flask import Flask, render_template, request, jsonify
from flask_cors import CORS
from letterboxdpy import user, movie
import random
import os
#from dash import Dash


app = Flask(__name__)
CORS(app)  # Enable CORS for all routes

# Initialize the Dash app
# dash_app = Dash(__name__, server=app, url_base_pathname='/dash/')
# dash_app.title = 'Data Analysis'

@app.route('/')
def home():
    return render_template('index.html')

# @app.route('/data_analysis')
# def data_analysis():
#     os.system('python data_analysis.py')  # Run the data analysis script
#     return render_template('analysis.html')

@app.route('/data_analysis')
def data_analysis():
    os.system('python analysis.py')  # Run the data analysis script
    return render_template('analysis.html')

@app.route('/get_top_movies', methods=['POST'])
def get_top_movies():
    username = request.json.get('username')
    username = str(username)
    us = user.User(username)
    
    # Get user's rated movies
    rev = user.user_films_rated(us)
    
    # Count total rated movies
    total_rates = sum(1 for r in rev if '★' in r[3] or '½' in r[3])
    
    # Filter movies with ★ rating
    five_star_movies = [movie_info for movie_info in rev if '★★★★★' in movie_info[3]]
    
    # Randomize if there are more than 4 such movies
    if len(five_star_movies) > 4:
        five_star_movies = random.sample(five_star_movies, 4)

    total_movies = len(user.user_films_watched(us))

    movies_data = []
    for title, movie_id, slug, rating in five_star_movies:
        m = movie.Movie(slug)
        formatted_title = title.replace('-', ' ').title()

        movie_data = {
            'title': formatted_title,
            'year': m.year,
            'director': m.directors,
            'poster': movie.movie_poster(slug),
            'genres': m.genres,
            'slug': slug,
            'rating': rating,
        }
        movies_data.append(movie_data)

    return jsonify({"top_movies": movies_data, "totalR": total_rates, "totalM": total_movies})

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=int(os.environ.get('PORT', 5000)))

