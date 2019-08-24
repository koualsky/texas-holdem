from django.db import models
from django.contrib.auth.models import User
from random import randrange
from treys import Card, Evaluator


class Player(models.Model):
    """Attributes and methods for 'Player'"""

    # Attributes
    name = models.OneToOneField(User,
                                on_delete=models.CASCADE,
                                related_name='player',
                                unique=True
                                )
    money = models.IntegerField(default=100)
    round_money = models.IntegerField(default=0)
    cards = models.CharField(max_length=100, null=True)
    # (out, ready, start, check, call, raise, pass)
    state = models.CharField(max_length=100, default="out")
    table = models.ForeignKey('game.table',
                              on_delete=models.SET_NULL,
                              related_name='tablee',
                              null=True
                              )

    # Basic methods
    def __str__(self):
        return str(self.name)

    # Additional methods
    def convert_from_string_to_list(self, cards_string):
        """Input: string, Output: list"""

        output = list(map(int, cards_string.split(',')))
        return output

    def convert_from_list_to_string(self, cards_list):
        """Input: list, Output: string"""

        output = ','.join([str(i) for i in cards_list])
        return output

    def print_pretty_cards_cards(self):
        """Input: cards, Output: pretty cards"""

        if self.cards != None:
            cards_list_with_ints = \
                self.convert_from_string_to_list(self.cards)
            output = Card.print_pretty_cards(cards_list_with_ints)

            # Change output from [9h], [6s], ... to 9h 6s ...
            output = output.replace("[", "")
            output = output.replace("]", "")
            output = output.replace(",", "")
            output = output.replace(" ", "")
            return output
        else:
            return ''

    # Game methods
    def my_hand(self):
        """Return name of my best hand"""

        # Cards is on the table
        if self.table.cards_on_table != None:

            # 1. Get cards from table and from player
            # and convert them to list of int's
            cards_on_table = \
                self.convert_from_string_to_list(self.table.cards_on_table)
            cards_on_table = list(map(int, cards_on_table))
            my_cards = self.convert_from_string_to_list(self.cards)
            my_cards = list(map(int, my_cards))

            # 2. Show my hand
            evaluator = Evaluator()
            score = evaluator.evaluate(cards_on_table, my_cards)
            classs = evaluator.get_rank_class(score)
            my_hand = evaluator.class_to_string(classs)
            return my_hand

        # No cards on table
        else:
            return ''


class Table(models.Model):  # Game
    """Attributes and methods for the Table"""

    # Attributes
    player1 = models.OneToOneField(Player,
                                   on_delete=models.SET_NULL,
                                   related_name='player1',
                                   null=True
                                   )
    player2 = models.OneToOneField(Player,
                                   on_delete=models.SET_NULL,
                                   related_name='player2',
                                   null=True
                                   )
    player3 = models.OneToOneField(Player,
                                   on_delete=models.SET_NULL,
                                   related_name='player3',
                                   null=True
                                   )
    player4 = models.OneToOneField(Player,
                                   on_delete=models.SET_NULL,
                                   related_name='player4',
                                   null=True
                                   )
    dealer = models.OneToOneField(Player,
                                  on_delete=models.SET_NULL,
                                  related_name='dealer',
                                  null=True
                                  )
    small_blind = models.OneToOneField(Player,
                                       on_delete=models.SET_NULL,
                                       related_name='small_blind',
                                       null=True
                                       )
    big_blind = models.OneToOneField(Player,
                                     on_delete=models.SET_NULL,
                                     related_name='big_blind',
                                     null=True
                                     )
    decission = models.OneToOneField(Player,
                                     on_delete=models.SET_NULL,
                                     related_name='decission',
                                     null=True
                                     )
    pool = models.IntegerField(default=0)
    deck = models.CharField(max_length=500, null=True)
    cards_on_table = models.CharField(max_length=100, null=True)
    game_state = models.CharField(max_length=200, default='ready', null=True)

    # Basic methods
    def __str__(self):
        return (
            str(self.pk)
            + ' - ('
            + str(self.player1)
            + ', '
            + str(self.player2)
            + ', '
            + str(self.player3)
            + ', '
            + str(self.player4)
            + ')'
        )

    # Additional methods
    def how_many_players(self):
        """Count how many players is in the particular game"""

        result = 0
        for e in (self.player1, self.player2, self.player3, self.player4):
            if e is not None:
                result += 1
        return result

    def all_players(self):
        """Return list with all players in this table"""

        players_list = []
        for player in [
            self.player1,
            self.player2,
            self.player3,
            self.player4
        ]:
            if player != None:
                players_list.append(player)
        return players_list

    def all_players_with_start_state(self):
        """Return list with all players with 'start' state in this table"""

        players_list = []
        for player in [
            self.player1,
            self.player2,
            self.player3,
            self.player4
        ]:
            if player != None:
                if player.state == 'start':
                    players_list.append(player)
        return players_list

    def all_players_without_out_state(self):
        """Return list with all players without 'out' state in this table.
        'in game'."""

        players_list = []
        for player in [
            self.player1,
            self.player2,
            self.player3,
            self.player4
        ]:
            if player != None:
                if player.state != 'out':
                    players_list.append(player)
        return players_list

    def all_players_without_out_and_pass_state(self):
        """Return list with all players without 'out' and 'pass'
        state in this table. 'in game'."""

        players_list = []
        for player in [
            self.player1,
            self.player2,
            self.player3,
            self.player4
        ]:
            if player != None:
                if player.state != 'out' and player.state != 'pass':
                    players_list.append(player)
        return players_list

    def all_players_in_game_make_decision(self):
        """Return True if all players 'in game' make a decision"""

        for e in self.all_players_without_out_state():
            if e.state == 'start':
                return False
        return True

    def all_players_in_game_give_the_same_value_to_the_table(self):
        """Return True if all players 'in game' give the
        same value to the pool"""

        # 1. define max value
        max_value = self.biggest_rate()

        # 2. check every player give that value
        for player in self.all_players_without_out_state():
            if player.round_money != max_value and player.state != 'pass':
                return False
        return True

    def set_all_available_players_state(self, state):
        """Set 'state' to player if player exist"""

        if self.player1 is not None:
            self.player1.state = state
            self.player1.save()
        if self.player2 is not None:
            self.player2.state = state
            self.player2.save()
        if self.player3 is not None:
            self.player3.state = state
            self.player3.save()
        if self.player4 is not None:
            self.player4.state = state
            self.player4.save()

    def set_all_in_game_players_state(self, state):
        """
        Set 'start' state to all players 'in game',
        means all without 'pass' or 'out' state
        """

        if self.player1 is not None and self.player1.state != 'out' \
                and self.player1.state != 'pass':
            self.player1.state = state
            self.player1.save()
        if self.player2 is not None and self.player2.state != 'out' \
                and self.player2.state != 'pass':
            self.player2.state = state
            self.player2.save()
        if self.player3 is not None and self.player3.state != 'out' \
                and self.player3.state != 'pass':
            self.player3.state = state
            self.player3.save()
        if self.player4 is not None and self.player4.state != 'out' \
                and self.player4.state != 'pass':
            self.player4.state = state
            self.player4.save()

    def return_next(self, players_list, start_player):
        """Return player - next from start player"""

        print(players_list)
        print(type(players_list))

        length = len(players_list)
        indx = players_list.index(start_player)
        if indx == length - 1:
            return players_list[0]
        else:
            return players_list[indx + 1]

    def add_player(self, player):
        """Add Player to free space in table"""

        if self.player1 == None:
            self.player1 = player
        elif self.player2 == None:
            self.player2 = player
        elif self.player3 == None:
            self.player3 = player
        elif self.player4 == None:
            self.player4 = player

    def all_players_round_money_to_zero(self):
        """Set round_money to zero for all players"""

        for player in [
            self.player1,
            self.player2,
            self.player3,
            self.player4
        ]:
            if player != None:
                player.round_money = 0
                player.save()

    def start_game_again(self):
        """Reset game and start them again with the same players"""

        if self.game_state == 'again':

            # 1. Set 'start' state to all players in table
            self.set_all_available_players_state('start')

            # 2. Set game state to 'start'
            self.game_state = 'ready'

            # 3. Set pool to 0
            self.pool = 0
            self.save()

            # 4. Set all players round_money to 0
            self.all_players_round_money_to_zero()

            # 5. Clear cards on table and players cards
            # (deck no, because soon it will be full with new full deck)
            self.remove_cards_from_players()
            self.remove_cards_on_table()

    def next_game_state(self):
        """Change current game state to the next from the game path"""

        game_path = [
            'ready',
            # 'start' - add by players
            # 'dealer' - add by method if 2 player is in the game
            'small_blind',
            'big_blind',
            'give_2',
            'give_3',
            'give_1',
            'give_1_again',
            'winner',
            'again'
        ]

        # 1. Current game state and index of current game state from game_path
        current_game_state = self.game_state
        indx = game_path.index(current_game_state)

        # 2. One player in the table can't change game state
        if self.how_many_players() > 1:

            # Change game state if all players makes decisions

            # a) If game state is 'small_blind' and in the game is only 2
            # active players: skip +2, not +1 game state
            if current_game_state == 'small_blind' \
                    and len(self.all_players_without_out_state()) == 2:
                self.game_state = game_path[indx + 2]

            # b) else: +1
            else:
                self.game_state = game_path[indx + 1]

            self.save()

        # 3. If game state is 'again' return to the 'start' position
        self.start_game_again()

    def biggest_rate(self):
        """Return value from player.round_money from player who give the
         biggest value"""

        players_values = []
        for player in [
            self.player1,
            self.player2,
            self.player3,
            self.player4
        ]:
            if player != None:
                players_values.append(player.round_money)

        return max(players_values)

    def give_to_pool(self, player, how_much):
        """From 'player' give money (how_much) to 'pool'"""

        # Player
        player.money -= how_much
        player.round_money += how_much
        player.save()

        # Game
        self.pool += how_much
        self.save()

    def convert_from_string_to_list(self, cards_string):
        """Input: string, Output: list"""

        output = list(map(int, cards_string.split(',')))
        return output

    def convert_from_list_to_string(self, cards_list):
        """Input: list, Output: string"""

        output = ','.join([str(i) for i in cards_list])
        return output

    def print_pretty_cards_deck(self):
        """Input: cards, Output: pretty cards"""

        if self.deck != None:
            cards_list_with_ints = self.convert_from_string_to_list(self.deck)
            output = Card.print_pretty_cards(cards_list_with_ints)
            return output
        else:
            return ''

    def print_pretty_cards_on_table(self):
        """Input: cards, Output: pretty cards"""

        if self.cards_on_table != None:
            cards_list_with_ints = \
                self.convert_from_string_to_list(self.cards_on_table)
            output = Card.print_pretty_cards(cards_list_with_ints)

            # Change output from [9h], [6s], ... to 9h 6s ...
            output = output.replace("[", "")
            output = output.replace("]", "")
            output = output.replace(",", "")
            output = output.replace(" ", "")
            return output
        else:
            return ''

    def fill_deck_by_all_cards(self):
        """Fill table deck by all cards"""

        # Prepare deck of all cards
        deck = [
            Card.new('Ah'),
            Card.new('Kh'),
            Card.new('Qh'),
            Card.new('Jh'),
            Card.new('Th'),
            Card.new('9h'),
            Card.new('8h'),
            Card.new('7h'),
            Card.new('6h'),
            Card.new('5h'),
            Card.new('4h'),
            Card.new('3h'),
            Card.new('2h'),

            Card.new('As'),
            Card.new('Ks'),
            Card.new('Qs'),
            Card.new('Js'),
            Card.new('Ts'),
            Card.new('9s'),
            Card.new('8s'),
            Card.new('7s'),
            Card.new('6s'),
            Card.new('5s'),
            Card.new('4s'),
            Card.new('3s'),
            Card.new('2s'),

            Card.new('Ad'),
            Card.new('Kd'),
            Card.new('Qd'),
            Card.new('Jd'),
            Card.new('Td'),
            Card.new('9d'),
            Card.new('8d'),
            Card.new('7d'),
            Card.new('6d'),
            Card.new('5d'),
            Card.new('4d'),
            Card.new('3d'),
            Card.new('2d'),

            Card.new('Ac'),
            Card.new('Kc'),
            Card.new('Qc'),
            Card.new('Jc'),
            Card.new('Tc'),
            Card.new('9c'),
            Card.new('8c'),
            Card.new('7c'),
            Card.new('6c'),
            Card.new('5c'),
            Card.new('4c'),
            Card.new('3c'),
            Card.new('2c'),
        ]

        # Convert deck of all cards to string
        deck = self.convert_from_list_to_string(deck)

        # Save deck of all cards to db. Table.deck
        self.deck = deck

    def remove_cards_from_players(self):
        """Remove all cards from all players"""

        if self.player1 != None:
            self.player1.cards = None
            self.player1.save()
        if self.player2 != None:
            self.player2.cards = None
            self.player2.save()
        if self.player3 != None:
            self.player3.cards = None
            self.player3.save()
        if self.player4 != None:
            self.player4.cards = None
            self.player4.save()

    def remove_cards_on_table(self):
        """Remove cards from table"""

        if self.cards_on_table != None:
            self.cards_on_table = None
            self.save()

    def check_players_have_cards(self):
        """Return False if at least one player have cards"""

        if self.player1 != None and self.player1.cards != None:
            return False
        elif self.player2 != None and self.player2.cards != None:
            return False
        elif self.player3 != None and self.player3.cards != None:
            return False
        elif self.player4 != None and self.player4.cards != None:
            return False
        else:
            return True

    def on_table_is_only_3_cards(self):
        """Return True if on table is only 3 cards"""

        # 1. get cards from self.cards_on_table if they exist
        # 2. convert that string to list
        # 3. count this list
        # 4. if count == 3 return True, else return False

        if self.cards_on_table != None:
            cards = self.cards_on_table
        cards = self.convert_from_string_to_list(cards)
        count = len(cards)
        if count == 3:
            return True
        return False

    def on_table_is_only_4_cards(self):
        """Return True if on table is only 4 cards"""

        # 1. get cards from self.cards_on_table if they exist
        # 2. convert that string to list
        # 3. count this list
        # 4. if count == 3 return True, else return False

        if self.cards_on_table != None:
            cards = self.cards_on_table
        cards = self.convert_from_string_to_list(cards)
        count = len(cards)
        if count == 4:
            return True
        return False

    def get_random_cards_from_deck(self, how_many_cards):
        """
        Return list of cards (int's) if how_many_cards > 1
        or return string (str) if how_many_cards = 1

        and delete these cards from self.deck

        In how_many_cards enter: 1, 2 or 3
        """

        # 1. get cards from self.deck
        # 2. convert string to list
        # 3. if how many cards == 1:
        if how_many_cards == 1:

            # a) get cards list from table.deck
            cards_list = self.convert_from_string_to_list(self.deck)

            # b) get random integer from len(cards_list) range,
            #    get card with this index from cards_list
            #    add this card to random_cards list
            #    delete this position from cards_list

            int_1 = randrange(0, len(cards_list))
            int_1_card = cards_list[int_1]
            cards_list.remove(int_1_card)

            # c) convert and save new self.deck cards
            self.deck = self.convert_from_list_to_string(cards_list)
            self.save()

            # d) return this string
            return str(int_1_card)

        # 4. if how many cards == 2:
        if how_many_cards == 2:

            # a) get cards list from table.deck
            cards_list = self.convert_from_string_to_list(self.deck)

            # b) get random integer from len(cards_list) range,
            #    get card with this index from cards_list
            #    add this card to random_cards list
            #    delete this position from cards_list
            random_cards = []

            int_1 = randrange(0, len(cards_list))
            int_1_card = cards_list[int_1]
            random_cards.append(int_1_card)
            cards_list.remove(int_1_card)

            int_2 = randrange(0, len(cards_list))
            int_2_card = cards_list[int_2]
            random_cards.append(int_2_card)
            cards_list.remove(int_2_card)

            # c) convert and save new self.deck cards
            self.deck = self.convert_from_list_to_string(cards_list)
            self.save()

            # d) return this string
            return random_cards

        # 5. if how many cards == 3:
        if how_many_cards == 3:

            # a) get cards list from table.deck
            cards_list = self.convert_from_string_to_list(self.deck)

            # b) get random integer from len(cards_list) range,
            #    get card with this index from cards_list
            #    add this card to random_cards list
            #    delete this position from cards_list
            random_cards = []

            int_1 = randrange(0, len(cards_list))
            int_1_card = cards_list[int_1]
            random_cards.append(int_1_card)
            cards_list.remove(int_1_card)

            int_2 = randrange(0, len(cards_list))
            int_2_card = cards_list[int_2]
            random_cards.append(int_2_card)
            cards_list.remove(int_2_card)

            int_3 = randrange(0, len(cards_list))
            int_3_card = cards_list[int_3]
            random_cards.append(int_3_card)
            cards_list.remove(int_3_card)

            # c) convert and save new self.deck cards
            self.deck = self.convert_from_list_to_string(cards_list)
            self.save()

            # d) return this string
            return random_cards

    def the_winner(self):
        """Return winner in this table"""

        evaluator = Evaluator()

        # 1. Get cards from cards_on_table and convert them to list of int's
        cards_on_table = self.convert_from_string_to_list(self.cards_on_table)
        # cards_on_table = list(map(int, cards_on_table))

        # 2. List with scores
        scores_list = []

        # 3. Get cards from each player and convert them to list of integers
        if self.player1 is not None and self.player1.state != 'out' and self.player1.state != 'pass':
            player1_cards = \
                self.convert_from_string_to_list(self.player1.cards)
            player1_cards = list(map(int, player1_cards))
            player1_score = evaluator.evaluate(cards_on_table, player1_cards)
            scores_list.append(player1_score)
        else:
            player1_score = 0
        if self.player2 is not None and self.player2.state != 'out' and self.player2.state != 'pass':
            player2_cards = \
                self.convert_from_string_to_list(self.player2.cards)
            player2_cards = list(map(int, player2_cards))
            player2_score = evaluator.evaluate(cards_on_table, player2_cards)
            scores_list.append(player2_score)
        else:
            player2_score = 0
        if self.player3 is not None and self.player3.state != 'out' and self.player3.state != 'pass':
            player3_cards = \
                self.convert_from_string_to_list(self.player3.cards)
            player3_cards = list(map(int, player3_cards))
            player3_score = evaluator.evaluate(cards_on_table, player3_cards)
            scores_list.append(player3_score)
        else:
            player3_score = 0
        if self.player4 is not None and self.player4.state != 'out' and self.player4.state != 'pass':
            player4_cards = \
                self.convert_from_string_to_list(self.player4.cards)
            player4_cards = list(map(int, player4_cards))
            player4_score = evaluator.evaluate(cards_on_table, player4_cards)
            scores_list.append(player4_score)
        else:
            player4_score = 0

        # 5. Return the best score
        winner = min(scores_list)

        # 6. Give pool to the winner and return Player with the best score
        if winner == player1_score:
            if self.pool > 0:
                self.player1.money += self.pool
                self.player1.save()
                self.pool = 0
                self.save()
            return self.player1
        if winner == player2_score:
            if self.pool > 0:
                self.player2.money += self.pool
                self.player2.save()
                self.pool = 0
                self.save()
            return self.player2
        if winner == player3_score:
            if self.pool > 0:
                self.player3.money += self.pool
                self.player3.save()
                self.pool = 0
                self.save()
            return self.player3
        if winner == player4_score:
            if self.pool > 0:
                self.player4.money += self.pool
                self.player4.save()
                self.pool = 0
                self.save()
            return self.player4

    # Game methods
    def start(self):
        """Set 'start' state for table and available players in table 
        if number of players in this table is > 1
        and state of game is 'ready'"""

        if self.how_many_players() > 1 and self.game_state == 'ready':
            self.set_all_available_players_state('start')
            self.fill_deck_by_all_cards()
            self.cards_on_table = None
            self.game_state = 'start'
            self.save()

    def dealer_button(self):
        """Give dealer button to first player or next of previous gamer"""

        # 1. If game state is 'start', we can give dealer button
        if self.game_state == 'start':

            # (pre) players list
            players_list = self.all_players()

            # a) If dealer field is empty - give dealer to the first player
            # from players list
            if self.dealer == None:
                self.dealer = players_list[0]

            # b) If dealer field exist, give dealer to the next player
            # of players list
            else:

                # a) if dealer from last table is in actually players list
                # - give dealer to the next player from players list
                if self.dealer in players_list:
                    start_player = self.dealer
                    self.dealer = self.return_next(players_list, start_player)

                # b) if dealer from the last table is not in actually players
                # list - give dealer to the first player from players list
                else:
                    self.dealer = players_list[0]

            # Set game status to 'dealer'
            self.game_state = 'dealer'
            self.save()

    def take_small_blind(self):
        """Take small blind from the next one from 'dealer player'"""

        # 1. If game state is 'dealer', we can take small_blind
        if self.game_state == 'dealer':

            # 1. Save to small_blind field 'player' next from 'dealer' player
            players_list = self.all_players()
            self.small_blind = self.return_next(players_list, self.dealer)

            # 2. Save to decission field 'player' next from 'small blind'
            players_with_start = self.all_players_with_start_state()
            self.decission = self.return_next(
                players_with_start,
                self.small_blind
            )

            # 3. Take 'small blind' from 'small_blind' player
            self.pool += 1
            self.small_blind.money -= 1
            self.small_blind.round_money = 1
            self.small_blind.save()

            # 4. Set game status to 'dealer'
            self.game_state = 'small_blind'
            self.save()

    def take_big_blind(self):
        """Take big blind from the next one from 'small blind player'"""

        # 1. If game state is 'small_blind' and in game is more than 2 players
        # we can take big_blind
        if self.game_state == 'small_blind' and self.how_many_players() > 2:

            # (pre)
            players_list = self.all_players()
            big_blind = self.return_next(players_list, self.small_blind)

            # Second condition -> does big_blind player have a 'start' state?
            if big_blind.state == 'start':

                # 1. Save to 'big_blind' field
                # player next from 'small_blind' player
                self.big_blind = big_blind

                # 2. Save to decission field 'player' next from 'small blind'
                players_with_start = self.all_players_with_start_state()
                self.decission = self.return_next(
                    players_with_start,
                    self.big_blind
                )

                # 3. Take 'small blind' from 'small_blind' player
                self.pool += 2
                self.big_blind.money -= 2
                self.big_blind.round_money = 2
                self.big_blind.save()

                # 4. Set game status to 'big_blind'
                self.game_state = 'big_blind'
                self.save()

    def make_turn(self):
        """That function is call in every game page overload"""

        # If all players in the game make decision
        # and give the same value to the pool
        if self.all_players_in_game_make_decision() and \
                self.all_players_in_game_give_the_same_value_to_the_table():

            # 1. Change game state to next from path (give_2, give_3, etc.)
            self.next_game_state()

            # 2. Call function by game_state (look up)
            self.give_2()
            self.give_3()
            self.give_1()
            self.give_1_again()
            # self.the_winner is call by table.html when game_state = 'winner'
            # self.start_game_again is call by self.next_game_state when
            # game_state = 'again'

            # 3. Change game state for players 'in game' to 'start'
            # (when we go to the 'again' method - that method change
            # all players state to 'start')
            self.set_all_in_game_players_state('start')

    def give_2(self):
        """
        Give 2 cards to each active player if:
        - game state = give 2
        - and self.check_players_have_cards() (delete this)
        """

        if self.game_state == 'give_2':

            # Player1 (if exist)
            if self.player1 is not None and self.player1.state != 'out':
                cards_2 = self.get_random_cards_from_deck(2)
                self.player1.cards = self.convert_from_list_to_string(cards_2)
                self.player1.save()

            # Player2 (if exist)
            if self.player2 is not None and self.player2.state != 'out':
                cards_2 = self.get_random_cards_from_deck(2)
                self.player2.cards = self.convert_from_list_to_string(cards_2)
                self.player2.save()

            # Player3 (if exist)
            if self.player3 is not None and self.player3.state != 'out':
                cards_2 = self.get_random_cards_from_deck(2)
                self.player3.cards = self.convert_from_list_to_string(cards_2)
                self.player3.save()

            # Player4 (if exist)
            if self.player4 is not None and self.player4.state != 'out':
                cards_2 = self.get_random_cards_from_deck(2)
                self.player4.cards = self.convert_from_list_to_string(cards_2)
                self.player4.save()

    def give_3(self):
        """
        Give 3 cards to the table if:
        - game state = give 3
        - on table is no cards
        """

        # After pycharm hint I change cards_on_table == None: from == to is
        # Check if it won't produce a bug
        if self.game_state == 'give_3' and self.cards_on_table is None:
            cards_3 = self.get_random_cards_from_deck(3)
            self.cards_on_table = self.convert_from_list_to_string(cards_3)
            self.save()

    def give_1(self):
        """
        Give 1 card to the table if:
        - game state = give 1
        - on table is only 3 cards
        """

        if self.game_state == 'give_1' and self.on_table_is_only_3_cards():

            # 1. get cards from cards on table andconvert them to list
            # 2. get random card from deck
            # 3. add to list 1 random card
            # 4. save to cards on table new list converted to string

            new_cards = self.convert_from_string_to_list(self.cards_on_table)
            random_card = self.get_random_cards_from_deck(1)
            new_cards.append(random_card)
            self.cards_on_table = self.convert_from_list_to_string(new_cards)
            self.save()

    def give_1_again(self):
        """
        Give 1 card to the table if:
        - game state = give 1 again
        - on table is only 4 cards
        """

        if self.game_state == 'give_1_again' \
                and self.on_table_is_only_4_cards():
            # 1. get cards from cards on table andconvert them to list
            # 2. get random card from deck
            # 3. add to list 1 random card
            # 4. save to cards on table new list converted to string

            new_cards = self.convert_from_string_to_list(self.cards_on_table)
            random_card = self.get_random_cards_from_deck(1)
            new_cards.append(random_card)
            self.cards_on_table = self.convert_from_list_to_string(new_cards)
            self.save()