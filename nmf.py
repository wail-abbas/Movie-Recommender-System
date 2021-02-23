import pandas as pd
import numpy as np
from sklearn.decomposition import NMF
import pickle

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

# Train NMF
nmf = NMF(n_components=100, max_iter=1000)
nmf.fit(R_imputed)

# Extract the movie-feature matrix
Q = nmf.components_

# Extract the user-feature matrix
P = nmf.transform(R_imputed)

# Calculate R_hat
R_hat = pd.DataFrame(np.matmul(P, Q), index=R.index, columns=R.columns)

# Safe Model
nmf_model = 'model.nmf.pickle'
with open(nmf_model, 'wb') as file:
    pickle.dump(nmf, file)

