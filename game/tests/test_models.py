from django.test import TestCase
from django.contrib.auth.models import User
from game.models import Player, Table
from treys import Card, Evaluator


class PlayerModelTest(TestCase):
    """Test all Player methods"""

    # Additional methods
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
        Input: String with cards separated by commas
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

    # Game methods
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


class TableModelTest(TestCase):
    """Test all Table methods"""

    # Additional methods
    def test_how_many_players(self):
        """
        Input: none
        Output: count how many players is in the game - as a integer
        """

        # Arrange
        table = Table()
        table2 = Table(player1=Player(name=User(username='player1')))

        # Act
        result = table.how_many_players()
        result2 = table2.how_many_players()

        # Assertion
        self.assertIsInstance(result, int)
        self.assertEqual(result, 0)
        self.assertEqual(result2, 1)

    def test_all_players(self):
        """
        Input: none
        Output: List with players in particular table
        """

        # Arrange
        table = Table()
        player1 = Player(name=User(username='player1'))
        table2 = Table(player1=player1)

        # Act
        result = table.all_players()
        result2 = table2.all_players()

        # Assertion
        self.assertIsInstance(result, list)
        self.assertIsInstance(result2, list)
        self.assertEqual(result, [])
        self.assertEqual(result2, [player1])

    def test_all_players_with_start_state(self):
        """
        Pre: Create table with 2 players with 'start' state
        and 1 player with 'out' state
        Output: List with players who have 'start' status
        """

        # Arrange
        player1 = Player(name=User(username='player1'), state='start')
        player2 = Player(name=User(username='player2'), state='out')
        player3 = Player(name=User(username='player3'), state='start')
        table = Table(player1=player1, player2=player2, player3=player3)

        # Act
        result = table.all_players_with_start_state()
        to_compare = [player1, player3]

        # Assertion
        self.assertIsInstance(result, list)
        self.assertEqual(result, to_compare)

    def test_all_players_without_out_state(self):
        """
        Pre: Create table with 2 players with 'start' and 'ready' state
        and 2 players with 'out' state
        Output: List with players who do not have an 'out' status
        """

        # Arrange
        player1 = Player(name=User(username='player1'), state='start')
        player2 = Player(name=User(username='player2'), state='ready')
        player3 = Player(name=User(username='player3'), state='out')
        player4 = Player(name=User(username='player4'), state='out')
        table = Table(player1=player1, player2=player2, player3=player3, player4=player4)

        # Act
        result = table.all_players_without_out_state()
        to_compare = [player1, player2]

        # Assertion
        self.assertIsInstance(result, list)
        self.assertEqual(result, to_compare)

    def test_all_players_without_out_and_pass_state(self):
        """
        Pre: Create table with 2 players with 'pass' and 'out' state
        and 2 players with 'check' state
        Output: List with players who do not have an 'out' or 'pass' status
        """

        # Arrange
        player1 = Player(name=User(username='player1'), state='pass')
        player2 = Player(name=User(username='player2'), state='out')
        player3 = Player(name=User(username='player3'), state='check')
        player4 = Player(name=User(username='player4'), state='check')
        table = Table(player1=player1, player2=player2, player3=player3, player4=player4)

        # Act
        result = table.all_players_without_out_and_pass_state()
        to_compare = [player3, player4]

        # Assertion
        self.assertIsInstance(result, list)
        self.assertEqual(result, to_compare)

    def test_all_players_in_game_make_decision(self):
        """
        Pre: Create table with 2 players with 'start' and 'out' state and 2
        players with 'raise' and 'check' state -> what means they made decisions.
        Output: True if all players 'in game' make a decision
        """

        # Arrange
        player1 = Player(name=User(username='player1'), state='start')
        player2 = Player(name=User(username='player2'), state='out')
        player3 = Player(name=User(username='player3'), state='raise')
        player4 = Player(name=User(username='player4'), state='check')
        table1 = Table(player1=player1, player2=player2, player3=player3,
                      player4=player4)
        table2 = Table(player3=player3, player4=player4)

        # Act
        result1 = table1.all_players_in_game_make_decision()
        result2 = table2.all_players_in_game_make_decision()

        # Assertion
        self.assertIsInstance(result1, bool)
        self.assertFalse(result1)
        self.assertIsInstance(result2, bool)
        self.assertTrue(result2)

    def test_all_players_in_game_give_the_same_value_to_the_table(self):
        """
        Pre: Create 2 tables. 1 with players who give the same value. 2 with
        with 1 player who give less than other players
        Output: True if all players 'in game' give the same value to the pool.
        """

        # Arrange
        player1 = Player(name=User(username='player1'), state='start', round_money=10)
        player2 = Player(name=User(username='player2'), state='start', round_money=10)
        player3 = Player(name=User(username='player3'), state='start', round_money=10)
        player4 = Player(name=User(username='player4'), state='start', round_money=9)
        table1 = Table(player1=player1, player2=player2, player3=player3, player4=player4)
        table2 = Table(player1=player1, player2=player2)

        # Act
        result1 = table1.all_players_in_game_give_the_same_value_to_the_table()
        result2 = table2.all_players_in_game_give_the_same_value_to_the_table()

        # Assertion
        self.assertIsInstance(result1, bool)
        self.assertFalse(result1)
        self.assertIsInstance(result2, bool)
        self.assertTrue(result2)

    def test_set_all_available_players_state(self):
        """
        Pre: Create table with players with 'out' state.
        Output: True if all players have changed to 'start' state.
        """

        # Arrange
        us1 = User(username='player1')
        us1.save()
        us2 = User(username='player2')
        us2.save()
        us3 = User(username='player3')
        us3.save()
        us4 = User(username='player4')
        us4.save()
        player1 = Player(name=us1)
        player1.save()
        player2 = Player(name=us2)
        player2.save()
        player3 = Player(name=us3)
        player3.save()
        player4 = Player(name=us4)
        player4.save()
        table = Table(player1=player1, player2=player2, player3=player3, player4=player4)

        # Act
        table.set_all_available_players_state('start')

        # Assertion
        self.assertEqual(table.player1.state, 'start')
        self.assertEqual(table.player2.state, 'start')
        self.assertEqual(table.player3.state, 'start')
        self.assertEqual(table.player4.state, 'start')

    def test_set_all_in_game_players_state(self):
        """
        Pre: Create table with players with different states.
        Output: True if players without 'pass' or 'out' state have changed to
        'start' state.
        """

        # Arrange
        us1 = User(username='player1')
        us1.save()
        us2 = User(username='player2')
        us2.save()
        us3 = User(username='player3')
        us3.save()
        us4 = User(username='player4')
        us4.save()
        player1 = Player(name=us1, state='pass')
        player1.save()
        player2 = Player(name=us2)
        player2.save()
        player3 = Player(name=us3, state='check')
        player3.save()
        player4 = Player(name=us4, state='start')
        player4.save()
        table = Table(player1=player1, player2=player2, player3=player3, player4=player4)

        # Act
        table.set_all_in_game_players_state('start')

        # Assertion
        self.assertEqual(table.player1.state, 'pass')
        self.assertEqual(table.player2.state, 'out')
        self.assertEqual(table.player3.state, 'start')
        self.assertEqual(table.player4.state, 'start')

    def test_return_next(self):
        """
        Pre: List with players, and start_player
        Output: Player from list, next from start_player
        """

        # Arrange
        player1 = Player(name=User(username='player1'))
        player2 = Player(name=User(username='player2'))
        player3 = Player(name=User(username='player3'))
        player4 = Player(name=User(username='player4'))
        table = Table(
            player1=player1,
            player2=player2,
            player3=player3,
            player4=player4)
        players_list = [player1, player2, player3, player4]

        # Acts & Assertions
        result = table.return_next(players_list, player4)
        self.assertIsInstance(result, Player)
        self.assertEqual(result, player1)

        result = table.return_next(players_list, player1)
        self.assertIsInstance(result, Player)
        self.assertEqual(result, player2)

        result = table.return_next(players_list, player2)
        self.assertIsInstance(result, Player)
        self.assertEqual(result, player3)

        result = table.return_next(players_list, player3)
        self.assertIsInstance(result, Player)
        self.assertEqual(result, player4)

        result = table.return_next(players_list, player4)
        self.assertIsInstance(result, Player)
        self.assertEqual(result, player1)

    def test_add_player(self):
        """Add Player to free space in table"""

        # Arrange
        player1 = Player(name=User(username='player1'))
        player2 = Player(name=User(username='player2'))
        player3 = Player(name=User(username='player3'))
        player4 = Player(name=User(username='player4'))
        table = Table(player1=player1, player2=player2, player4=player4)

        # Act
        table.add_player(player3)

        # Assertion
        self.assertEqual(table.player3, player3)

    def test_all_players_round_money_to_zero(self):
        """Set round_money to zero for all players"""

        # Arrange
        us1 = User(username='player1')
        us1.save()
        us2 = User(username='player2')
        us2.save()
        us3 = User(username='player3')
        us3.save()
        us4 = User(username='player4')
        us4.save()
        player1 = Player(name=us1, round_money=-99)
        player1.save()
        player2 = Player(name=us2, round_money=0)
        player2.save()
        player3 = Player(name=us3, round_money=99)
        player3.save()
        player4 = Player(name=us4, round_money=9)
        player4.save()
        table = Table(player1=player1, player2=player2, player3=player3, player4=player4)

        # Act
        table.all_players_round_money_to_zero()

        # Assertion
        self.assertEqual(table.player1.round_money, 0)

    def test_start_game_again(self):
        """Reset game and start them again with the same players"""

        # Arrange
        us1 = User(username='player1')
        us1.save()
        us2 = User(username='player2')
        us2.save()
        us3 = User(username='player3')
        us3.save()
        us4 = User(username='player4')
        us4.save()
        player1 = Player(name=us1, state='pass', round_money=1)
        player1.save()
        player2 = Player(name=us2, state='out', round_money=0)
        player2.save()
        player3 = Player(name=us3, state='check', round_money=99)
        player3.save()
        player4 = Player(name=us4, state='start', round_money=7)
        player4.save()
        table = Table(player1=player1, player2=player2, player3=player3, player4=player4, game_state='again')

        # Act
        table.start_game_again()

        # Assertion
        self.assertEqual(table.game_state, 'ready')
        self.assertEqual(table.player1.state, 'start')
        self.assertEqual(table.player2.state, 'start')
        self.assertEqual(table.player3.state, 'start')
        self.assertEqual(table.player4.state, 'start')

    def test_next_game_state_3_players(self):
        """Change current game state to the next from the game path"""

        # Arrange
        us1 = User(username='player1')
        us1.save()
        us2 = User(username='player2')
        us2.save()
        us3 = User(username='player3')
        us3.save()
        player1 = Player(name=us1, state='check')
        player1.save()
        player2 = Player(name=us2, state='check')
        player2.save()
        player3 = Player(name=us3, state='check')
        player3.save()
        table = Table(player1=player1, player2=player2, player3=player3)

        # Act & Assertion
        self.assertEqual(table.game_state, 'ready')
        table.next_game_state()
        self.assertEqual(table.game_state, 'small_blind')
        table.next_game_state()
        self.assertEqual(table.game_state, 'big_blind')
        table.next_game_state()
        self.assertEqual(table.game_state, 'give_2')
        table.next_game_state()
        self.assertEqual(table.game_state, 'give_3')
        table.next_game_state()
        self.assertEqual(table.game_state, 'give_1')
        table.next_game_state()
        self.assertEqual(table.game_state, 'give_1_again')
        table.next_game_state()
        self.assertEqual(table.game_state, 'winner')
        table.next_game_state()

        # In this plase should be 'again' but self.start_game_again() call
        # this table.next_game_state, so we jump to begin - 'ready' state
        self.assertEqual(table.game_state, 'ready')

    def test_next_game_state_3_players_one_with_out_state(self):
        """Change current game state to the next from the game path"""

        # Arrange
        us1 = User(username='player1')
        us1.save()
        us2 = User(username='player2')
        us2.save()
        us3 = User(username='player3')
        us3.save()
        player1 = Player(name=us1, state='check')
        player1.save()
        player2 = Player(name=us2, state='out')
        player2.save()
        player3 = Player(name=us3, state='check')
        player3.save()
        table = Table(player1=player1, player2=player2, player3=player3)

        # Act & Assertion
        self.assertEqual(table.game_state, 'ready')
        table.next_game_state()
        self.assertEqual(table.game_state, 'small_blind')
        table.next_game_state()
        self.assertEqual(table.game_state, 'give_2')
        table.next_game_state()
        self.assertEqual(table.game_state, 'give_3')
        table.next_game_state()
        self.assertEqual(table.game_state, 'give_1')
        table.next_game_state()
        self.assertEqual(table.game_state, 'give_1_again')
        table.next_game_state()
        self.assertEqual(table.game_state, 'winner')
        table.next_game_state()

        # In this plase should be 'again' but self.start_game_again() call
        # this table.next_game_state, so we jump to begin - 'ready' state
        self.assertEqual(table.game_state, 'ready')

    def test_next_game_state_2_players(self):
        """Change current game state to the next from the game path"""

        # Arrange
        us1 = User(username='player1')
        us1.save()
        us2 = User(username='player2')
        us2.save()
        player1 = Player(name=us1, state='check')
        player1.save()
        player2 = Player(name=us2, state='check')
        player2.save()
        table = Table(player1=player1, player2=player2)

        # Act & Assertion
        self.assertEqual(table.game_state, 'ready')
        table.next_game_state()
        self.assertEqual(table.game_state, 'small_blind')
        table.next_game_state()
        self.assertEqual(table.game_state, 'give_2')
        table.next_game_state()
        self.assertEqual(table.game_state, 'give_3')
        table.next_game_state()
        self.assertEqual(table.game_state, 'give_1')
        table.next_game_state()
        self.assertEqual(table.game_state, 'give_1_again')
        table.next_game_state()
        self.assertEqual(table.game_state, 'winner')
        table.next_game_state()

        # In this plase should be 'again' but self.start_game_again() call
        # this table.next_game_state, so we jump to begin - 'ready' state
        self.assertEqual(table.game_state, 'ready')

    def test_biggest_rate(self):
        """
        Should return the biggest value from all players from
        player.round_money field
        """

        # Arrange
        us1 = User(username='player1')
        us1.save()
        us2 = User(username='player2')
        us2.save()
        us3 = User(username='player3')
        us3.save()
        us4 = User(username='player4')
        us4.save()
        player1 = Player(name=us1, round_money=1)
        player1.save()
        player2 = Player(name=us2, round_money=0)
        player2.save()
        player3 = Player(name=us3, round_money=99)
        player3.save()
        player4 = Player(name=us4, round_money=7)
        player4.save()
        table = Table(player1=player1, player2=player2, player3=player3, player4=player4, game_state='again')

        # Act
        result = table.biggest_rate()

        # Assertion
        self.assertEqual(result, 99)

    def test_give_to_pool(self):
        """Give money from player.money to table.pool"""

        # Arrange
        us1 = User(username='player1')
        us1.save()
        player1 = Player(name=us1, money=50)
        player1.save()
        table = Table(player1=player1, pool=0)

        # Act
        table.give_to_pool(player1, 10)

        # Assertion
        self.assertEqual(table.pool, 10)
        self.assertEqual(player1.money, 40)

    def test_convert_from_string_to_list(self):
        """
        Input: Strings representing cards separate by commas
        Output: List with int's
        """

        # Arrange
        cards_list = [Card.new('As'), Card.new('9h')]
        cards_string = str(Card.new('As')) + ',' + str(Card.new('9h'))

        # Act
        result = Table.convert_from_string_to_list(self, cards_string)

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
        result = Table.convert_from_list_to_string(self, cards_list)

        # Assertion
        self.assertEqual(result, cards_string)
        self.assertIsInstance(result, str)

    def test_print_pretty_cards_deck(self):
        """
        Input: String with cards separated by commas
        Output: Pretty cards as a string
        """

        # Arrange
        table = Table()
        table.deck = str(Card.new('As')) + ',' + str(Card.new('9h'))

        # Act
        table = table.print_pretty_cards_deck()
        cards_result = Card.print_pretty_cards([Card.new('As'), Card.new('9h')])

        # Assertion
        self.assertEqual(table, cards_result)
        self.assertIsInstance(table, str)

    def test_print_pretty_cards_on_table(self):
        """
        Input: String with cards separated by commas
        Output: Pretty cards as a string
        """

        # Arrange
        table = Table()
        table.cards_on_table = str(Card.new('As')) + ',' + str(Card.new('9h'))

        # Act
        table = table.print_pretty_cards_on_table()
        cards_result = Card.print_pretty_cards([Card.new('As'), Card.new('9h')])

        # Assertion
        self.assertEqual(table, cards_result)
        self.assertIsInstance(table, str)

    def test_fill_deck_by_all_cards(self):
        """Fill table deck by all cards"""

        # Arrange
        table = Table()

        # Assertions & Act
        self.assertEqual(table.deck, None)
        table.fill_deck_by_all_cards()
        self.assertNotEqual(table.deck, None)
        self.assertIsInstance(table.deck, str)

    def test_remove_cards_from_players(self):
        """Remove all cards from all players"""

        # Arrange
        cards1 = str(Card.new('As')) + ',' + str(Card.new('9s'))
        cards2 = str(Card.new('Ah')) + ',' + str(Card.new('9h'))
        cards3 = str(Card.new('Ad')) + ',' + str(Card.new('9d'))
        cards4 = str(Card.new('Ac')) + ',' + str(Card.new('9c'))
        us1 = User(username='player1')
        us1.save()
        us2 = User(username='player2')
        us2.save()
        us3 = User(username='player3')
        us3.save()
        us4 = User(username='player4')
        us4.save()
        player1 = Player(name=us1, cards=cards1)
        player1.save()
        player2 = Player(name=us2, cards=cards2)
        player2.save()
        player3 = Player(name=us3, cards=cards3)
        player3.save()
        player4 = Player(name=us4, cards=cards4)
        player4.save()
        table = Table(player1=player1, player2=player2, player3=player3, player4=player4)

        # Act
        table.remove_cards_from_players()

        # Assertion
        self.assertEqual(table.player1.cards, None)
        self.assertEqual(table.player2.cards, None)
        self.assertEqual(table.player3.cards, None)
        self.assertEqual(table.player4.cards, None)

    def test_remove_cards_on_table(self):
        """Remove all cards from all players"""

        # Arrange
        cards = str(Card.new('As')) + ',' + str(Card.new('9s'))
        table = Table(cards_on_table=cards)

        # Act
        table.remove_cards_on_table()

        # Assertion
        self.assertEqual(table.cards_on_table, None)

    def test_check_players_have_cards(self):
        """Return False if at least one player have cards"""

        # Arrange
        cards1 = str(Card.new('As')) + ',' + str(Card.new('9s'))
        cards2 = str(Card.new('Ah')) + ',' + str(Card.new('9h'))
        us1 = User(username='player1')
        us1.save()
        us2 = User(username='player2')
        us2.save()
        us3 = User(username='player3')
        us3.save()
        us4 = User(username='player4')
        us4.save()
        player1 = Player(name=us1, cards=cards1)
        player1.save()
        player2 = Player(name=us2, cards=cards2)
        player2.save()
        player3 = Player(name=us3)
        player3.save()
        player4 = Player(name=us4)
        player4.save()
        table = Table(player1=player1, player2=player2, player3=player3, player4=player4)

        # Act
        result = table.check_players_have_cards()

        # Assertion
        self.assertFalse(result)
        table.remove_cards_from_players()
        result2 = table.check_players_have_cards()
        self.assertTrue(result2)

    def test_on_table_is_only_3_cards(self):
        """Return True if on table is only 3 cards"""

        # Arrange
        cards = str(Card.new('As')) + ',' + str(Card.new('9s')) + ',' + str(Card.new('3c'))
        table = Table(cards_on_table=cards)

        # Act
        result = table.on_table_is_only_3_cards()

        # Assertion
        self.assertTrue(result)
        cards2 = str(Card.new('As')) + ',' + str(Card.new('9s'))
        table2 = Table(cards_on_table=cards2)
        result2 = table2.on_table_is_only_3_cards()
        self.assertFalse(result2)

    def test_on_table_is_only_4_cards(self):
        """Return True if on table is only 3 cards"""

        # Arrange
        cards = str(Card.new('As')) + ',' + str(Card.new('9s')) + ',' + str(Card.new('3c')) + ',' + str(Card.new('Qh'))
        table = Table(cards_on_table=cards)

        # Act
        result = table.on_table_is_only_4_cards()

        # Assertion
        self.assertTrue(result)
        cards2 = str(Card.new('As')) + ',' + str(Card.new('9s'))
        table2 = Table(cards_on_table=cards2)
        result2 = table2.on_table_is_only_4_cards()
        self.assertFalse(result2)

    def test_get_random_cards_from_deck(self):
        """
        Return list of cards if how_many_cards > 1
        or return string if how_many_cards = 1

        and delete these cards from self.deck

        In how_many_cards enter: 1, 2 or 3
        """

        # Arrange
        cards = str(Card.new('Ks')) + ',' \
            + str(Card.new('Qc')) + ',' \
            + str(Card.new('Jh')) + ',' \
            + str(Card.new('Td')) + ',' \
            + str(Card.new('9c')) + ',' \
            + str(Card.new('8h')) + ',' \
            + str(Card.new('7s')) + ',' \
            + str(Card.new('6d'))
        table1 = Table(deck=cards)
        table2 = Table(deck=cards)
        table3 = Table(deck=cards)

        # Act
        result1 = table1.get_random_cards_from_deck(1)
        result2 = table2.get_random_cards_from_deck(2)
        result3 = table3.get_random_cards_from_deck(3)

        # Assertion
        self.assertIsInstance(result1, str)
        self.assertIn(result1, cards)
        self.assertNotIn(result1, table1.deck)

        self.assertIsInstance(result2, list)
        self.assertIn(str(result2[0]), cards)
        self.assertIn(str(result2[1]), cards)
        self.assertNotIn(str(result2[0]), table2.deck)
        self.assertNotIn(str(result2[1]), table2.deck)

        self.assertIsInstance(result3, list)
        self.assertIn(str(result3[0]), cards)
        self.assertIn(str(result3[1]), cards)
        self.assertIn(str(result3[2]), cards)
        self.assertNotIn(str(result3[0]), table3.deck)
        self.assertNotIn(str(result3[1]), table3.deck)
        self.assertNotIn(str(result3[2]), table3.deck)
    
    def test_the_winner(self):
        """Return winner in this table"""

        # Arrange
        cards1 = str(Card.new('2s')) + ',' + str(Card.new('3s'))
        cards2 = str(Card.new('4h')) + ',' + str(Card.new('5d'))
        cards3 = str(Card.new('6d')) + ',' + str(Card.new('7h'))
        cards4 = str(Card.new('As')) + ',' + str(Card.new('Ks'))
        cards_on_table = str(Card.new('Qs')) + ',' \
                         + str(Card.new('Js')) + ','\
                         + str(Card.new('Ts')) + ','\
                         + str(Card.new('2d')) + ','\
                         + str(Card.new('3d'))
        us1 = User(username='player1')
        us1.save()
        us2 = User(username='player2')
        us2.save()
        us3 = User(username='player3')
        us3.save()
        us4 = User(username='player4')
        us4.save()
        player1 = Player(name=us1, cards=cards1, state='check')
        player1.save()
        player2 = Player(name=us2, cards=cards2, state='check')
        player2.save()
        player3 = Player(name=us3, cards=cards3, state='check')
        player3.save()
        player4 = Player(name=us4, cards=cards4, state='check')
        player4.save()
        table = Table(player1=player1,
                      player2=player2,
                      player3=player3,
                      player4=player4,
                      cards_on_table=cards_on_table
                      )

        # Act
        the_winner = table.the_winner()
        #print(the_winner)

        # Assertion
        self.assertEqual(the_winner, player4)

        # write tu all table, players, cards and in the end evaluating...

    # Game methods
    def test_start(self):
        """
        Set 'start' state for table and available players in table
        if number of players in this table is > 1
        and state of game is 'ready'
        """

        # Arrange
        us1 = User(username='player1')
        us1.save()
        us2 = User(username='player2')
        us2.save()
        us3 = User(username='player3')
        us3.save()
        us4 = User(username='player4')
        us4.save()
        player1 = Player(name=us1, state='check')
        player1.save()
        player2 = Player(name=us2, state='pass')
        player2.save()
        player3 = Player(name=us3, state='raise')
        player3.save()
        player4 = Player(name=us4, state='out')
        player4.save()
        table = Table(player1=player1)

        # Assertions & Acts

        # Only 1 player in table (table.start() should not working)
        self.assertEqual(table.game_state, 'ready')
        table.start()
        self.assertNotEqual(table.game_state, 'start')

        # 4 players in table (table.start() should works)
        table = Table(player1=player1,
                      player2=player2,
                      player3=player3,
                      player4=player4
                      )
        self.assertEqual(table.game_state, 'ready')
        self.assertEqual(player1.state, 'check')
        self.assertEqual(player2.state, 'pass')
        self.assertEqual(player3.state, 'raise')
        self.assertEqual(player4.state, 'out')
        table.start()
        self.assertEqual(table.game_state, 'start')
        self.assertEqual(player1.state, 'start')
        self.assertEqual(player2.state, 'start')
        self.assertEqual(player3.state, 'start')
        self.assertEqual(player4.state, 'start')

    def test_dealer_button(self):
        """
        Give dealer button to first player or next of previous gamer

        Dealer is always awarded to the first player if the table.dealer field
        is empty or to the next player inthe table.dealer field
        """

        # Arrange
        us1 = User(username='player1')
        us1.save()
        us2 = User(username='player2')
        us2.save()
        us3 = User(username='player3')
        us3.save()
        us4 = User(username='player4')
        us4.save()
        player1 = Player(name=us1, state='start')
        player1.save()
        player2 = Player(name=us2, state='start')
        player2.save()
        player3 = Player(name=us3, state='start')
        player3.save()
        player4 = Player(name=us4, state='start')
        player4.save()
        table = Table(player1=player1,
                      player2=player2,
                      player3=player3,
                      player4=player4,
                      game_state='start'
                      )

        # Act & Assertion
        table.dealer_button()
        self.assertEqual(table.dealer, player1)

        table.game_state = 'start'
        table.dealer_button()
        self.assertEqual(table.dealer, player2)

        table.game_state = 'start'
        table.dealer_button()
        self.assertEqual(table.dealer, player3)

        table.game_state = 'start'
        table.dealer_button()
        self.assertEqual(table.dealer, player4)

        table.game_state = 'start'
        table.dealer_button()
        self.assertEqual(table.dealer, player1)

    def test_take_small_blind(self):
        """
        Take small blind from the next one from 'dealer player'

        Small blind is always awarded to the next player from
        the table.dealer field
        """


        # Arrange
        us1 = User(username='player1')
        us1.save()
        us2 = User(username='player2')
        us2.save()
        us3 = User(username='player3')
        us3.save()
        us4 = User(username='player4')
        us4.save()
        player1 = Player(name=us1, state='start')
        player1.save()
        player2 = Player(name=us2, state='start')
        player2.save()
        player3 = Player(name=us3, state='start')
        player3.save()
        player4 = Player(name=us4, state='start')
        player4.save()
        table = Table(player1=player1,
                      player2=player2,
                      player3=player3,
                      player4=player4,
                      game_state='dealer',
                      dealer=player1
                      )

        # Act & Assertion
        table.take_small_blind()
        self.assertEqual(table.small_blind, player2)

        table.game_state = 'dealer'
        table.take_small_blind()
        self.assertEqual(table.small_blind, player2)

    def test_take_big_blind(self):
        """
        Take small blind from the next one from 'dealer player'

        Big blind is always awarded if players in table > 1
        - to the next player from the table.small_blind field
        """

        # Arrange
        us1 = User(username='player1')
        us1.save()
        us2 = User(username='player2')
        us2.save()
        us3 = User(username='player3')
        us3.save()
        us4 = User(username='player4')
        us4.save()
        player1 = Player(name=us1, state='start')
        player1.save()
        player2 = Player(name=us2, state='start')
        player2.save()
        player3 = Player(name=us3, state='start')
        player3.save()
        player4 = Player(name=us4, state='start')
        player4.save()
        table = Table(player1=player1,
                      player2=player2,
                      player3=player3,
                      player4=player4,
                      game_state='small_blind',
                      dealer=player1,
                      small_blind=player2
                      )

        # Act & Assertion
        table.take_big_blind()
        self.assertEqual(table.big_blind, player3)

        table.game_state = 'small_blind'
        table.dealer = player2
        table.small_blind = player3
        table.take_big_blind()
        self.assertEqual(table.big_blind, player4)

    def test_make_turn(self):
        """That function is call in every game page overload"""

        # Arrange
        us1 = User(username='player1')
        us1.save()
        us2 = User(username='player2')
        us2.save()
        us3 = User(username='player3')
        us3.save()
        us4 = User(username='player4')
        us4.save()
        player1 = Player(name=us1, state='check', money=90)
        player1.save()
        player2 = Player(name=us2, state='check', money=90)
        player2.save()
        player3 = Player(name=us3, state='check', money=90)
        player3.save()
        player4 = Player(name=us4, state='check', money=90)
        player4.save()
        table = Table(player1=player1,
                      player2=player2,
                      player3=player3,
                      player4=player4,
                      game_state='ready'
                      )

        # Acts & Assertions
        table.start()
        table.dealer_button()
        self.assertEqual(table.game_state, 'dealer')

        table.take_small_blind()
        self.assertEqual(table.game_state, 'small_blind')

        table.take_big_blind()
        self.assertEqual(table.game_state, 'big_blind')

        # All players must give to the pool the same value
        table.give_to_pool(player1, 2)
        table.give_to_pool(player2, 1)
        table.give_to_pool(player4, 2)

        table.fill_deck_by_all_cards()

        table.set_all_in_game_players_state('check')
        table.make_turn()
        self.assertEqual(table.game_state, 'give_2')
        self.assertEqual(player1.state, 'start')
        self.assertEqual(player2.state, 'start')
        self.assertEqual(player3.state, 'start')
        self.assertEqual(player4.state, 'start')

        table.set_all_in_game_players_state('check')
        table.make_turn()
        self.assertEqual(table.game_state, 'give_3')
        self.assertEqual(player1.state, 'start')
        self.assertEqual(player2.state, 'start')
        self.assertEqual(player3.state, 'start')
        self.assertEqual(player4.state, 'start')

        table.set_all_in_game_players_state('check')
        table.player1.state = 'pass'
        table.make_turn()
        self.assertEqual(table.game_state, 'give_1')
        self.assertEqual(player1.state, 'pass')
        self.assertEqual(player2.state, 'start')
        self.assertEqual(player3.state, 'start')
        self.assertEqual(player4.state, 'start')

        table.set_all_in_game_players_state('check')
        table.make_turn()
        self.assertEqual(table.game_state, 'give_1_again')
        self.assertEqual(player1.state, 'pass')
        self.assertEqual(player2.state, 'start')
        self.assertEqual(player3.state, 'start')
        self.assertEqual(player4.state, 'start')

        table.set_all_in_game_players_state('check')
        table.player2.state = 'pass'
        table.make_turn()
        self.assertEqual(table.game_state, 'winner')
        self.assertEqual(player1.state, 'pass')
        self.assertEqual(player2.state, 'pass')
        self.assertEqual(player3.state, 'start')
        self.assertEqual(player4.state, 'start')

        table.set_all_in_game_players_state('check')
        table.make_turn()
        self.assertEqual(table.game_state, 'ready')
        self.assertEqual(player1.state, 'start')
        self.assertEqual(player2.state, 'start')
        self.assertEqual(player3.state, 'start')
        self.assertEqual(player4.state, 'start')

        table.set_all_in_game_players_state('check')
        table.make_turn()
        self.assertEqual(table.game_state, 'small_blind')
        self.assertEqual(player1.state, 'start')
        self.assertEqual(player2.state, 'start')
        self.assertEqual(player3.state, 'start')
        self.assertEqual(player4.state, 'start')

        table.set_all_in_game_players_state('check')
        table.make_turn()
        self.assertEqual(table.game_state, 'big_blind')
        self.assertEqual(player1.state, 'start')
        self.assertEqual(player2.state, 'start')
        self.assertEqual(player3.state, 'start')
        self.assertEqual(player4.state, 'start')

    def test_give_2(self):
        """
        Give 2 cards to each active player if:
        - game state = give 2
        - each player have None cards
        """

        # Arrange
        us1 = User(username='player1')
        us1.save()
        us2 = User(username='player2')
        us2.save()
        us3 = User(username='player3')
        us3.save()
        us4 = User(username='player4')
        us4.save()
        player1 = Player(name=us1, state='start')
        player1.save()
        player2 = Player(name=us2, state='start')
        player2.save()
        player3 = Player(name=us3, state='start')
        player3.save()
        player4 = Player(name=us4, state='out')
        player4.save()
        table = Table(player1=player1,
                      player2=player2,
                      player3=player3,
                      player4=player4,
                      game_state='give_2'
                      )
        table.fill_deck_by_all_cards()

        # Act
        table.give_2()

        # Assertion
        self.assertNotIn(player1.cards, table.deck)
        self.assertNotIn(player2.cards, table.deck)
        self.assertNotIn(player3.cards, table.deck)
        self.assertEqual(player4.cards, None)
        self.assertIsInstance(player1.cards, str)
        self.assertIsInstance(player2.cards, str)
        self.assertIsInstance(player3.cards, str)
        self.assertEqual(table.game_state, 'give_2')

    def test_give_3(self):
        """
        Give 3 cards to the table if:
        - game state = give 3
        - on table is no cards
        """

        # Arrange
        us1 = User(username='player1')
        us1.save()
        us2 = User(username='player2')
        us2.save()
        us3 = User(username='player3')
        us3.save()
        us4 = User(username='player4')
        us4.save()
        player1 = Player(name=us1)
        player1.save()
        player2 = Player(name=us2)
        player2.save()
        player3 = Player(name=us3)
        player3.save()
        player4 = Player(name=us4)
        player4.save()
        table = Table(player1=player1,
                      player2=player2,
                      player3=player3,
                      player4=player4,
                      game_state='give_3'
                      )
        table.fill_deck_by_all_cards()

        # Act
        table.give_3()

        # Assertion
        self.assertNotIn(table.cards_on_table, table.deck)
        self.assertIsInstance(table.cards_on_table, str)
        self.assertEqual(table.game_state, 'give_3')

    def test_give_1(self):
        """
        Give 1 card to the table if:
        - game state = give 1
        - on table is only 3 cards
        """

        # Arrange
        us1 = User(username='player1')
        us1.save()
        us2 = User(username='player2')
        us2.save()
        us3 = User(username='player3')
        us3.save()
        us4 = User(username='player4')
        us4.save()
        player1 = Player(name=us1)
        player1.save()
        player2 = Player(name=us2)
        player2.save()
        player3 = Player(name=us3)
        player3.save()
        player4 = Player(name=us4)
        player4.save()
        table = Table(player1=player1,
                      player2=player2,
                      player3=player3,
                      player4=player4,
                      game_state='give_3'
                      )
        table.fill_deck_by_all_cards()

        # Act
        table.give_3()
        table.next_game_state()
        table.give_1()

        # Assertion
        self.assertNotIn(table.cards_on_table, table.deck)
        self.assertIsInstance(table.cards_on_table, str)
        self.assertEqual(table.game_state, 'give_1')

    def test_give_1_again(self):
        """
        Give 1 card to the table if:
        - game state = give 1 again
        - on table is only 4 cards
        """

        # Arrange
        us1 = User(username='player1')
        us1.save()
        us2 = User(username='player2')
        us2.save()
        us3 = User(username='player3')
        us3.save()
        us4 = User(username='player4')
        us4.save()
        player1 = Player(name=us1)
        player1.save()
        player2 = Player(name=us2)
        player2.save()
        player3 = Player(name=us3)
        player3.save()
        player4 = Player(name=us4)
        player4.save()
        table = Table(player1=player1,
                      player2=player2,
                      player3=player3,
                      player4=player4,
                      game_state='give_3'
                      )
        table.fill_deck_by_all_cards()

        # Act
        table.give_3()
        table.next_game_state()
        table.give_1()
        table.next_game_state()
        table.give_1_again()

        # Assertion
        self.assertNotIn(table.cards_on_table, table.deck)
        self.assertIsInstance(table.cards_on_table, str)
        self.assertEqual(table.game_state, 'give_1_again')