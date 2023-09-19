import joblib
import pandas as pd
import numpy as np
import random

random = random.Random()


# Function to calculate the hybridized recommendation score for a user and movie
def hybrid_recommendation_score(user_id, movie_id, user_item_matrix):
    user_ratings = user_item_matrix.loc[user_id].dropna()
    movie_ratings = user_item_matrix[movie_id].dropna()

    common_movies = user_ratings.index.intersection(movie_ratings.index)

    if common_movies.empty:
        return 0.0  # Default recommendation score if no common movies

    ra = np.mean(user_ratings)
    ru = np.mean(movie_ratings)

    numerator = np.sum((user_ratings[common_movies] - ra) * (movie_ratings[common_movies] - ru))
    denominator_a = np.sqrt(np.sum((user_ratings[common_movies] - ra) ** 2))
    denominator_u = np.sqrt(np.sum((movie_ratings[common_movies] - ru) ** 2))

    hybrid_score = numerator / (denominator_a * denominator_u)

    return hybrid_score


# Function to recommend top N movies for a user using the hybridized algorithm
def hybrid_recommend_movies(user_id, user_item_matrix, N=20):
    # Calculate hybrid recommendation scores for all movies
    movie_ids = user_item_matrix.columns
    hybrid_scores = [hybrid_recommendation_score(user_id, movie_id, user_item_matrix) for movie_id in movie_ids]
    # Sort movie IDs based on hybrid scores in descending order
    sorted_movie_ids = [x for _, x in sorted(zip(hybrid_scores, movie_ids), reverse=True)]

    # Exclude movies that the user has already rated
    user_ratings = user_item_matrix.loc[user_id].dropna().index
    unrated_movies = set(sorted_movie_ids) - set(user_ratings)

    # Return the top N unrated movies as recommendations
    top_N_recommendations = list(unrated_movies)[:N]

    movies = []
    for movie_id in top_N_recommendations:
        movie_data = movies_data[movies_data['movieId'] == movie_id]
        if not movie_data.empty:
            movies.append(movie_data['title'].values[0])

    top_N_movies = []
    for i in range(10):
        movie = random.choice(movies)
        top_N_movies.append(movie)
        movies.remove(movie)

    return top_N_movies


def make_hybrid_recommendations(user_id):
    # Load the hybrid model
    loaded_model = joblib.load('models/hybrid_model.joblib')
    hybrid_recommendation_score_loaded, hybrid_recommend_movies_loaded = loaded_model
    top_recommendations = hybrid_recommend_movies_loaded(user_id, user_item_matrix, N=20)
    return top_recommendations


movies_data = pd.read_csv('ml-latest-small/movies.csv')
data = pd.read_csv('ml-latest-small/ratings.csv')

user_item_matrix = data.pivot(index='userId', columns='movieId', values='rating')
