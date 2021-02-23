import pandas as pd
import numpy as np
import pickle

nmf_model = 'model.nmf.pickle'

def get_recommendations(movie1, movie2, movie3, rating1, rating2, rating3):

    # Load The data
    ratings = pd.read_csv('data/ratings.csv',index_col='movieId')
    ratings = ratings[['userId', 'rating']]
    movies = pd.read_csv('data/movies.csv', index_col='movieId')

    # Join Tables
    R = ratings.join(movies[['title']], on='movieId', how='inner')

    # Transform the data into the right format
    R = R.pivot_table(index='userId', columns='title', values='rating')

    # We take a simple solution and impute the overall mean
    average_movie_rating = R.mean()
    R_imputed = R.fillna(average_movie_rating)


    # load the model from disk
    loaded_model = pickle.load(open(nmf_model, 'rb'))
    # Extract the movie-feature matrix
    Q = loaded_model.components_

    # Extract the user-feature matrix
    P = loaded_model.transform(R_imputed)

    # Make a data frame
    pd.DataFrame(np.matmul(P, Q), index=R.index, columns=R.columns)


    # Create a dictionary for a new user
    new_user_input = {movie1: rating1, movie2: rating2, movie3: rating3} # user input used to calculate recommendations
    new_user = pd.DataFrame(new_user_input, columns=R.columns, index=[len(R.index)+1])
    # Convert it to a pd.DataFrame
    new_user = pd.DataFrame(new_user_input, columns=R.columns, index=[len(R.index)+1])
    #Fill missing data
    new_user = new_user.fillna(average_movie_rating)

    #Prediction step 1 - generate user_P 
    user_P = loaded_model.transform(new_user)
    #new user R - reconstruct R but for this new user only
    user_R = pd.DataFrame(np.matmul(user_P, Q), index=new_user.index, columns=R.columns)

    # We want to get rid of movies we have already watchend
    recommendation = user_R.drop(columns=new_user_input.keys())
    # Sort recommendations
    recommendation = recommendation.sort_values(by=611, axis=1, ascending=False)
    recomended_movies = recommendation.iloc[:,0:5]
    return recomended_movies