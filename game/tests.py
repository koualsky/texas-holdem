from django.test import TestCase
from django.contrib.auth.models import User
from .models import Player, Table
from treys import Card, Evaluator


class PlayerModelTest(TestCase):
    """Test all Player methods"""

    def test_convert_from_string_to_list(self):
        """
        Input: Strings representing cards separate by commas
        Output: List with int's
        """

        # Arrange
        cards_list = [Card.new('As'), Card.new('9h')]
        cards_string = str(Card.new('As')) + ',' + str(Card.new('9h'))

        # Act
        result = Player.convert_from_string_to_list(self, cards_string)

        # Assertion
        self.assertEqual(result, cards_list)
        self.assertIsInstance(result[0], int)
        self.assertIsInstance(result[1], int)

    def test_convert_from_list_to_string(self):
        """
        Input: Strings representing cards separate by commas
        Output: List with int's
        """

        # Arrange
        cards_list = [Card.new('As'), Card.new('9h')]
        cards_string = str(Card.new('As')) + ',' + str(Card.new('9h'))

        # Act
        result = Player.convert_from_list_to_string(self, cards_list)

        # Assertion
        self.assertEqual(result, cards_string)
        self.assertIsInstance(result, str)

    def test_print_pretty_cards_cards(self):
        """
        Input: String with cards separating by commas
        Output: Pretty cards as a string
        """

        # Arrange
        player = Player('player')
        player.cards = str(Card.new('As')) + ',' + str(Card.new('9h'))

        # Act
        player_result = player.print_pretty_cards_cards()
        cards_result = Card.print_pretty_cards([Card.new('As'), Card.new('9h')])

        # Assertion
        self.assertEqual(player_result, cards_result)
        self.assertIsInstance(player_result, str)

    def test_my_hand(self):
        """
        Input: Cards from my profile as a string
        Output: Descripting poker hand as a string
        """

        # Player Arrange
        table_cards = str(Card.new('3s')) + ',' \
                         + str(Card.new('2s')) + ',' \
                         + str(Card.new('As')) + ',' \
                         + str(Card.new('Ks')) + ',' \
                         + str(Card.new('Qs'))
        player_cards = str(Card.new('Js')) + ',' + str(Card.new('Ts'))

        table = Table(cards_on_table=table_cards)
        player = Player(table=table, cards=player_cards)

        # Player Act
        player_result = player.my_hand()

        # Treys Arrange
        board = [Card.new('3s'), Card.new('2s'), Card.new('As'), Card.new('Ks'), Card.new('Qs')]
        gamer = [Card.new('Js'), Card.new('Ts')]

        # Treys Act
        evaluator = Evaluator()
        score = evaluator.evaluate(board, gamer)
        classs = evaluator.get_rank_class(score)
        treys_result =  evaluator.class_to_string(classs)

        # Assertion
        self.assertEqual(player_result, treys_result)
        self.assertIsInstance(player_result, str)


