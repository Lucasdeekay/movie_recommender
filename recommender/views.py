# recommender/views.py

from django.http import JsonResponse
from recommendations import make_hybrid_recommendations, hybrid_recommendation_score, hybrid_recommend_movies


def recommend_movies(request):
    if request.method == 'GET':
        user_id = request.GET.get('user_id')  # Get the user ID from the request

        try:
            recommendations = make_hybrid_recommendations(int(user_id))
            return JsonResponse({'user_id': user_id, 'recommendations': recommendations})
        except Exception:
            return JsonResponse({'recommendations': 'User not found'}, status=404)
    else:
        return JsonResponse({'recommendations': 'Invalid request method'}, status=405)
