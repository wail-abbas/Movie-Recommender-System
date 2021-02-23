import pandas as pd
from flask import Flask, request
from flask.templating import render_template
import pickle
import recommender


movies = pd.read_csv("data/movies.csv")
movies = movies['title'].sort_values()


# Run Flask website
app  = Flask("Wail's Movie Recommender")


@app.route('/result')
def get_movie():
    html_form_data = dict(request.args)
    movie1 = html_form_data['movie1']
    rate1 = html_form_data['rate1']
    movie2 = html_form_data['movie2']
    rate2 = html_form_data['rate2']
    movie3 = html_form_data['movie3']
    rate3 = html_form_data['rate3']
    recomended_movies = recommender.get_recommendations(movie1, movie2, movie3, rate1, rate2, rate3)
    
    print(html_form_data)
    return render_template('result.html', rec_movies = recomended_movies, title='Movie Recomender')

@app.route('/')
def hello():
    return render_template('main.html', title='Movie Recomender', movies = movies)

if __name__ == "__main__":
    app.run(debug=True, port=5000)

