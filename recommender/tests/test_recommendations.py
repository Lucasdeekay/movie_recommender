import random
import unittest
from unittest.mock import patch

import pandas as pd
import numpy as np

import recommendations
from recommendations import hybrid_recommendation_score, hybrid_recommend_movies


def test_hybrid_recommend_movies_excludes_rated_movies(self):
    user_id = 1
    N = 5
    recommendations = hybrid_recommend_movies(user_id, self.user_item_matrix, N)

    # Get the movies that the user has already rated
    rated_movies = set(self.user_item_matrix.loc[user_id].dropna().index)

    # Get the movie IDs of the recommended movies
    recommended_movie_ids = set()
    for title in recommendations:
        movie_id = movies_data[movies_data['title'] == title]['movieId'].values[0]
        recommended_movie_ids.add(movie_id)

    # Check that there's no overlap between rated and recommended movies
    self.assertEqual(len(rated_movies.intersection(recommended_movie_ids)), 0,
                     "Recommended movies should not include any movies the user has already rated")

def test_hybrid_recommend_movies_returns_ten_titles(self):
    user_id = 1
    N = 20
    result = hybrid_recommend_movies(user_id, self.user_item_matrix, N)
    self.assertEqual(len(result), 10)
    self.assertTrue(all(isinstance(title, str) for title in result))

def test_hybrid_recommend_movies_no_ratings(self):
    user_id_no_ratings = 5
    self.user_item_matrix.loc[user_id_no_ratings] = [0.0, 0.0, 0.0, 0.0]

    with patch('recommendations.movies_data', pd.DataFrame({
        'movieId': [1, 2, 3, 4],
        'title': ['Movie A', 'Movie B', 'Movie C', 'Movie D']
    })):
        with patch('recommendations.random.choice', side_effect=lambda x: x[0]):
            recommendations = hybrid_recommend_movies(user_id_no_ratings, self.user_item_matrix)

    self.assertEqual(len(recommendations), 10)
    self.assertTrue(all(isinstance(movie, str) for movie in recommendations))
    self.assertEqual(len(set(recommendations)), 4)  # All 4 movies should be recommended

def test_hybrid_recommend_movies_no_unrated_movies(self):
    user_id = 1
    user_item_matrix = pd.DataFrame({
        1: [4.0, 3.0, 5.0, 2.0],
        2: [0.0, 0.0, 0.0, 0.0],
        3: [0.0, 0.0, 0.0, 0.0],
        4: [0.0, 0.0, 0.0, 0.0]
    }, index=[1, 2, 3, 4])

    # Mock the movies_data DataFrame
    global movies_data
    movies_data = pd.DataFrame({
        'movieId': [1, 2, 3, 4],
        'title': ['Movie 1', 'Movie 2', 'Movie 3', 'Movie 4']
    })

    # Mock the random.choice function to always return the first element
    with unittest.mock.patch('random.choice', side_effect=lambda x: x[0]):
        result = hybrid_recommend_movies(user_id, user_item_matrix)

    self.assertEqual(result, [], "Expected an empty list when no unrated movies are available")

def test_hybrid_recommend_movies_fewer_than_n_unrated(self):
    # Create a user-item matrix with fewer unrated movies than N
    user_item_matrix = pd.DataFrame({
        1: [4.0, 3.0, 5.0, 2.0],
        2: [0.0, 0.0, 0.0, 0.0],
        3: [3.0, 1.0, 2.0, 3.0],
        4: [0.0, 0.0, 0.0, 4.0]
    }, index=[1, 2, 3, 4])

    # Mock the movies_data DataFrame
    global movies_data
    movies_data = pd.DataFrame({
        'movieId': [1, 2, 3, 4],
        'title': ['Movie A', 'Movie B', 'Movie C', 'Movie D']
    })

    # Set a fixed seed for reproducibility
    random.seed(42)

    # Call the function with N=20 (more than available unrated movies)
    result = hybrid_recommend_movies(1, user_item_matrix, N=20)

    # Check if the result contains the correct number of recommendations
    self.assertEqual(len(result), 1)

    # Check if the recommended movie is from the unrated movies
    self.assertIn(result[0], ['Movie B'])

def test_hybrid_recommend_movies_single_user(self):
    single_user_matrix = pd.DataFrame({
        1: [4.0],
        2: [3.0],
        3: [5.0],
        4: [2.0]
    }, index=[1])

    # Mock the movies_data and random.choice
    global movies_data
    movies_data = pd.DataFrame({
        'movieId': [1, 2, 3, 4],
        'title': ['Movie A', 'Movie B', 'Movie C', 'Movie D']
    })
    random.choice = lambda x: x[0]

    result = hybrid_recommend_movies(1, single_user_matrix, N=4)

    self.assertEqual(len(result), 4)
    self.assertListEqual(result, ['Movie A', 'Movie B', 'Movie C', 'Movie D'])

def test_hybrid_recommend_movies_user_not_in_matrix(self):
    non_existent_user_id = 999
    result = hybrid_recommend_movies(non_existent_user_id, self.user_item_matrix)
    self.assertEqual(result, [])

def test_hybrid_recommend_movies_empty_movies_data(self):
    # Create a mock user_item_matrix
    user_item_matrix = pd.DataFrame({
        1: [4.0, 3.0, 0.0, 5.0],
        2: [5.0, 0.0, 4.0, 0.0],
        3: [3.0, 1.0, 2.0, 3.0],
        4: [0.0, 0.0, 0.0, 4.0]
    }, index=[1, 2, 3, 4])

    # Create an empty movies_data DataFrame
    empty_movies_data = pd.DataFrame(columns=['movieId', 'title'])

    # Temporarily replace the global movies_data with the empty DataFrame
    original_movies_data = recommendations.movies_data
    recommendations.movies_data = empty_movies_data

    try:
        # Call the function with a user_id
        result = hybrid_recommend_movies(1, user_item_matrix)

        # Check that the result is an empty list
        self.assertEqual(result, [])
    finally:
        # Restore the original movies_data
        recommendations.movies_data = original_movies_data

def test_hybrid_recommend_movies_randomness(self):
    user_id = 1
    N = 20

    # Call the function twice
    recommendations1 = hybrid_recommend_movies(user_id, self.user_item_matrix, N)
    recommendations2 = hybrid_recommend_movies(user_id, self.user_item_matrix, N)

    # Check that both calls return lists of 10 movies
    self.assertEqual(len(recommendations1), 10)
    self.assertEqual(len(recommendations2), 10)

    # Check that the recommendations are different
    self.assertNotEqual(recommendations1, recommendations2)

    # Check that at least one movie is different between the two lists
    self.assertTrue(any(movie not in recommendations2 for movie in recommendations1))


def test_hybrid_recommendation_score_all_common_movies_same_rating(self):
    user_item_matrix = pd.DataFrame({
        1: [4.0, 4.0, 4.0, 0.0],
        2: [4.0, 4.0, 4.0, 4.0],
        3: [4.0, 4.0, 4.0, 0.0]
    }, index=[1, 2, 3])

    user_id = 1
    movie_id = 2

    score = hybrid_recommendation_score(user_id, movie_id, user_item_matrix)

    self.assertEqual(score, 1.0, "Expected score to be 1.0 when all common movies have the same rating")

def test_hybrid_recommendation_score_user_rated_one_movie(self):
    user_item_matrix = pd.DataFrame({
        1: [4.0, 0.0, 0.0],
        2: [3.0, 4.0, 5.0],
        3: [5.0, 2.0, 1.0]
    }, index=[1, 2, 3])

    user_id = 1
    movie_id = 2

    score = hybrid_recommendation_score(user_id, movie_id, user_item_matrix)

    self.assertEqual(score, 0.0, "Expected score to be 0.0 when user has rated only one movie")

def test_hybrid_recommendation_score_movie_with_one_rating(self):
    user_item_matrix = pd.DataFrame({
        1: [4.0, 3.0, 5.0],
        2: [0.0, 0.0, 3.0],
        3: [2.0, 4.0, 0.0]
    }, index=[1, 2, 3])

    user_id = 1
    movie_id = 2

    score = hybrid_recommendation_score(user_id, movie_id, user_item_matrix)

    self.assertEqual(score, 0.0, "Expected score to be 0.0 when the movie has only one rating")

def test_hybrid_recommendation_score_with_negative_ratings(self):
    user_item_matrix = pd.DataFrame({
        1: [4.0, -3.0, 2.0, -1.0],
        2: [-2.0, 3.0, -1.0, 4.0],
        3: [1.0, -2.0, 3.0, -4.0],
        4: [-3.0, 2.0, -4.0, 1.0]
    }, index=[1, 2, 3, 4])

    user_id = 1
    movie_id = 2

    score = hybrid_recommendation_score(user_id, movie_id, user_item_matrix)

    expected_score = -0.9701425001453319
    self.assertAlmostEqual(score, expected_score, places=7,
                           msg="Hybrid recommendation score with negative ratings should be calculated correctly")

def test_hybrid_recommendation_score_with_large_values(self):
    user_item_matrix = pd.DataFrame({
        1: [1e6, 2e6, 3e6, 0],
        2: [2e6, 3e6, 4e6, 5e6],
        3: [3e6, 4e6, 5e6, 0]
    }, index=[1, 2, 3])

    user_id = 1
    movie_id = 2

    score = hybrid_recommendation_score(user_id, movie_id, user_item_matrix)

    self.assertAlmostEqual(score, 1.0, places=6,
                           msg="Expected score to be close to 1.0 with large rating values")

def test_hybrid_recommendation_score_invalid_id(self):
    user_item_matrix = pd.DataFrame({
        1: [4.0, 3.0, 5.0],
        2: [3.0, 1.0, 4.0],
        3: [5.0, 2.0, 1.0]
    }, index=[1, 2, 3])

    invalid_user_id = 999
    invalid_movie_id = 999

    with self.assertRaises(KeyError):
        hybrid_recommendation_score(invalid_user_id, 1, user_item_matrix)

    with self.assertRaises(KeyError):
        hybrid_recommendation_score(1, invalid_movie_id, user_item_matrix)

def test_hybrid_recommendation_score_empty_matrix(self):
    empty_matrix = pd.DataFrame()
    user_id = 1
    movie_id = 1

    score = hybrid_recommendation_score(user_id, movie_id, empty_matrix)

    self.assertEqual(score, 0.0, "Expected score to be 0.0 when user_item_matrix is empty")

def test_hybrid_recommendation_score_all_ratings_same(self):
    user_item_matrix = pd.DataFrame({
        1: [3.0, 3.0, 3.0],
        2: [3.0, 3.0, 3.0],
        3: [3.0, 3.0, 3.0]
    }, index=[1, 2, 3])

    user_id = 1
    movie_id = 2

    score = hybrid_recommendation_score(user_id, movie_id, user_item_matrix)

    self.assertTrue(np.isnan(score), "Expected score to be NaN when all ratings are the same")

def test_hybrid_recommendation_score_single_column_matrix(self):
    user_item_matrix = pd.DataFrame({
        1: [4.0, 3.0, 5.0, 2.0]
    }, index=[1, 2, 3, 4])

    user_id = 1
    movie_id = 1

    score = hybrid_recommendation_score(user_id, movie_id, user_item_matrix)

    self.assertEqual(score, 1.0, "Expected score to be 1.0 for a single-column matrix")

def test_hybrid_recommendation_score_with_non_numeric_ratings(self):
    user_item_matrix = pd.DataFrame({
        1: [4.0, 'A', 3.0, 5.0],
        2: [3.0, 'B', 'C', 4.0],
        3: [5.0, 2.0, 'D', 1.0],
        4: ['E', 3.0, 4.0, 'F']
    }, index=[1, 2, 3, 4])

    user_id = 1
    movie_id = 2

    with self.assertRaises(TypeError):
        hybrid_recommendation_score(user_id, movie_id, user_item_matrix)