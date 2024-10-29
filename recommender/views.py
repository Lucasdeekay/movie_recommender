# recommender/views.py

from django.http import JsonResponse
from recommendations import make_hybrid_recommendations, hybrid_recommendation_score, hybrid_recommend_movies
import random


random = random.Random()


def recommend_movies(request):
    """
    Generate movie recommendations for a randomly selected user.

    This function creates a random user ID, retrieves movie recommendations
    for that user using a hybrid recommendation system, and returns the
    results as a JSON response.

    Parameters:
    request (HttpRequest): The HTTP request object from Django.
                           Not used in the current implementation.

    Returns:
    JsonResponse: A JSON object containing:
                  - 'user_id': The randomly generated user ID.
                  - 'recommendations': A list of recommended movies.
                  If an error occurs, it returns a JSON object with an error message
                  and a 404 status code.
    """
    user_id = random.randint(1, 1000)  # Get the user ID from the request

    try:
        recommendations = make_hybrid_recommendations(int(user_id))
        return JsonResponse({'user_id': user_id, 'recommendations': recommendations})
    except Exception:
        return JsonResponse({'recommendations': 'User not found'}, status=404)
