from django.test import TestCase
from django.contrib.auth.models import User
from game.views import *


class ViewsTest(TestCase):
    @classmethod
    def setUpTestData(cls):

        # Create 4 players
        number_of_players = 4
        player1 = User(username='player1')

        for player_id in range(number_of_players, 1, 4):
            Player.objects.create(name=f'player{player_id}')

    def test_start(self):
        response = self.client.get('')
        self.assertEqual(response.status_code, 200)