from django.test import TestCase
from django.urls import reverse
from unittest.mock import patch
from recommender.views import recommend_movies


class RecommendMoviesViewTest(TestCase):
    pass

    @patch('recommender.views.make_hybrid_recommendations')
    def test_recommend_movies_user_not_found(self, mock_make_hybrid_recommendations):
        mock_make_hybrid_recommendations.side_effect = Exception("User not found")

        url = reverse('recommend_movies')
        response = self.client.get(url)

        self.assertEqual(response.status_code, 404)
        self.assertEqual(response.json(), {'recommendations': 'User not found'})

    @patch('recommender.views.make_hybrid_recommendations')
    def test_recommend_movies_exception(self, mock_make_hybrid_recommendations):
        mock_make_hybrid_recommendations.side_effect = Exception("Test exception")

        response = self.client.get(reverse('recommend_movies'))

        self.assertEqual(response.status_code, 404)
        self.assertEqual(response.json(), {'recommendations': 'User not found'})

    @patch('recommender.views.make_hybrid_recommendations')
    def test_recommend_movies_valid_response(self, mock_make_hybrid_recommendations):
        mock_make_hybrid_recommendations.return_value = ['Movie1', 'Movie2', 'Movie3']

        response = self.client.get(reverse('recommend_movies'))

        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertIn('user_id', data)
        self.assertIn('recommendations', data)
        self.assertTrue(1 <= data['user_id'] <= 1000)
        self.assertEqual(data['recommendations'], ['Movie1', 'Movie2', 'More3'])
        mock_make_hybrid_recommendations.assert_called_once()

    def test_random_user_id_generation(self):
        with patch('recommender.views.random.randint') as mock_randint:
            mock_randint.return_value = 500
            response = self.client.get(reverse('recommend_movies'))
            self.assertEqual(response.status_code, 200)
            self.assertEqual(response.json()['user_id'], 500)
            mock_randint.assert_called_once_with(1, 1000)

    @patch('recommender.views.make_hybrid_recommendations')
    def test_recommend_movies_empty_recommendations(self, mock_make_hybrid_recommendations):
        mock_make_hybrid_recommendations.return_value = []
        response = self.client.get(reverse('recommend_movies'))
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertIn('user_id', data)
        self.assertIn('recommendations', data)
        self.assertEqual(data['recommendations'], [])

    @patch('recommender.views.make_hybrid_recommendations')
    def test_recommend_movies_when_recommendations_are_none(self, mock_make_hybrid_recommendations):
        mock_make_hybrid_recommendations.return_value = None
        response = self.client.get(reverse('recommend_movies'))
        self.assertEqual(response.status_code, 404)
        self.assertEqual(response.json(), {'recommendations': 'User not found'})

    @patch('recommender.views.random.randint')
    @patch('recommender.views.make_hybrid_recommendations')
    def test_user_id_in_response_matches_generated_id(self, mock_make_hybrid_recommendations, mock_randint):
        mock_randint.return_value = 42
        mock_make_hybrid_recommendations.return_value = ['Movie1', 'Movie2']

        response = self.client.get(reverse('recommend_movies'))

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()['user_id'], 42)

    @patch('recommender.views.make_hybrid_recommendations')
    def test_recommend_movies_format(self, mock_make_hybrid_recommendations):
        mock_recommendations = [
            {'id': 1, 'title': 'Movie 1'},
            {'id': 2, 'title': 'Movie 2'},
            {'id': 3, 'title': 'Movie 3'}
        ]
        mock_make_hybrid_recommendations.return_value = mock_recommendations

        response = self.client.get(reverse('recommend_movies'))
        self.assertEqual(response.status_code, 200)

        data = response.json()
        self.assertIn('user_id', data)
        self.assertIn('recommendations', data)
        self.assertIsInstance(data['recommendations'], list)

        for movie in data['recommendations']:
            self.assertIsInstance(movie, dict)
            self.assertIn('id', movie)
            self.assertIn('title', movie)

    @patch('recommender.views.random.randint')
    @patch('recommender.views.make_hybrid_recommendations')
    def test_recommend_movies_min_user_id(self, mock_make_hybrid_recommendations, mock_randint):
        mock_randint.return_value = 1
        mock_make_hybrid_recommendations.return_value = ['Movie1', 'Movie2', 'Movie3']

        response = self.client.get(reverse('recommend_movies'))

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json(), {
            'user_id': 1,
            'recommendations': ['Movie1', 'Movie2', 'Movie3']
        })
        mock_randint.assert_called_once_with(1, 1000)
        mock_make_hybrid_recommendations.assert_called_once_with(1)

    @patch('recommender.views.random.randint')
    @patch('recommender.views.make_hybrid_recommendations')
    def test_recommend_movies_max_user_id(self, mock_make_hybrid_recommendations, mock_randint):
        mock_randint.return_value = 1000
        mock_make_hybrid_recommendations.return_value = ['Movie1', 'Movie2', 'Movie3']

        response = self.client.get(reverse('recommend_movies'))

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json(), {
            'user_id': 1000,
            'recommendations': ['Movie1', 'Movie2', 'Movie3']
        })
        mock_randint.assert_called_once_with(1, 1000)
        mock_make_hybrid_recommendations.assert_called_once_with(1000)
