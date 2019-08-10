from django.db import models
from django.contrib.auth.models import User


# Later: count and verify 'max_length' fields in my models


class Player(models.Model):
    """Attributes and methods for 'Player'"""

    # Attributes
    name = models.OneToOneField(User, on_delete=models.CASCADE, related_name='player', unique=True)
    money = models.IntegerField(default=100)
    round_money = models.IntegerField(default=0)
    cards = models.CharField(max_length=100)
    state = models.CharField(max_length=100, default="out")
    # (out, ready, start, check, call, raise, pass)
    table = models.ForeignKey('game.table', on_delete=models.SET_NULL, related_name='tablee', null=True)

    def __str__(self):
        return str(self.name)


class Table(models.Model):  # Game
    """Attributes and methods for the Table"""

    # Attributes
    player1 = models.OneToOneField(Player, on_delete=models.SET_NULL, related_name='player1', null=True)
    player2 = models.OneToOneField(Player, on_delete=models.SET_NULL, related_name='player2', null=True)
    player3 = models.OneToOneField(Player, on_delete=models.SET_NULL, related_name='player3', null=True)
    player4 = models.OneToOneField(Player, on_delete=models.SET_NULL, related_name='player4', null=True)
    dealer = models.OneToOneField(Player, on_delete=models.SET_NULL, related_name='dealer', null=True)
    small_blind = models.OneToOneField(Player, on_delete=models.SET_NULL, related_name='small_blind', null=True)
    big_blind = models.OneToOneField(Player, on_delete=models.SET_NULL, related_name='big_blind', null=True)
    decission = models.OneToOneField(Player, on_delete=models.SET_NULL, related_name='decission', null=True)
    pool = models.IntegerField(default=0)
    deck = models.CharField(max_length=500, null=True)
    cards_on_table = models.CharField(max_length=100, null=True)
    game_state = models.CharField(max_length=200, default='ready', null=True)

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

    # Additional Methods
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
        for player in [self.player1, self.player2, self.player3, self.player4]:
            if player != None:
                players_list.append(player)
        return players_list

    def all_players_with_start_state(self):
        """Return list with all players with 'start' state in this table"""

        players_list = []
        for player in [self.player1, self.player2, self.player3, self.player4]:
            if player != None:
                if player.state == 'start':
                    players_list.append(player)
        return players_list

    def all_players_without_out_state(self):
        """Return list with all players without 'out' state in this table.
        'in game'."""

        players_list = []
        for player in [self.player1, self.player2, self.player3, self.player4]:
            if player != None:
                if player.state != 'out':
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
            if player.round_money != max_value:
                return False
        return True

    def set_all_available_players_state(self, state):
        """Set 'start' state to player if player exist"""

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
        """Set 'start' state to all players 'in game'"""

        if self.player1 is not None and self.player1.state != 'out':
            self.player1.state = state
            self.player1.save()
        if self.player2 is not None and self.player2.state != 'out':
            self.player2.state = state
            self.player2.save()
        if self.player3 is not None and self.player3.state != 'out':
            self.player3.state = state
            self.player3.save()
        if self.player4 is not None and self.player4.state != 'out':
            self.player4.state = state
            self.player4.save()

    def return_next(self, players_list, start_player):
        """Return player - next from start player"""

        length = len(players_list)
        indx = players_list.index(start_player)
        if indx == length - 1:
            return players_list[0]
        else:
            return players_list[indx + 1]

    def add_player(self, player):
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

        for player in [self.player1, self.player2, self.player3, self.player4]:
            if player != None:
                player.round_money = 0
                player.save()

    def start_game_again(self):
        if self.game_state == 'again':

            # 1. Set to all players (not only 'in game') in table state = 'start'
            self.set_all_available_players_state('start')

            # 2. Set game state to 'start'
            self.game_state = 'ready'

            # 3. Set pool to 0
            self.pool = 0
            self.save()

            # 4. Set all players round_money to 0
            self.all_players_round_money_to_zero()

    def next_game_state(self):
        """Change current game state to the next from the game path"""

        game_path = ['ready',
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

            # a) If game state is 'small_blind' and in the game is only 2 active
            #    players: skip +2, not +1 game state
            if current_game_state == 'small_blind' and self.all_players_without_out_state():
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
        for player in [self.player1, self.player2, self.player3, self.player4]:
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


    # Game Methods
    def start(self):
        """Set 'start' state for table and available players in table 
        if number of players in this table is > 1
        and state of game is 'ready'"""

        if self.how_many_players() > 1 and self.game_state == 'ready':
            self.set_all_available_players_state('start')
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
            self.decission = self.return_next(players_with_start, self.small_blind)

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
                self.decission = self.return_next(players_with_start,
                                                  self.big_blind)

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

        # If all players in the game make decission: (potem: i tyle samo dali do puli!)
        if self.all_players_in_game_make_decision() \
                and self.all_players_in_game_give_the_same_value_to_the_table():

            # 1. Change game state to next from path (give_2, give_3, etc.)
            self.next_game_state()

            # 2. Call function by game_state (look up)
            # give_2()
            # give_3()
            # ...

            # 3. Change game state for players 'in game' to 'start'
            # (when we go to the 'again' function - that function change totally ALL PLAYERS state to 'start')
            self.set_all_in_game_players_state('start')

    def make_decission(self):
        """After ech deal, the player must make a decission: check/call, raise, pass"""

        # check (if no one raise pool)
        # call (automatically add the requires minimum amount of money to the pool)
        # raise (you can raise pool)
        # pass (change your status to 'pass' - you don't allow to make changes in this game)

        # timer - if you dont make a decission in 10 sek. you automatically get status: 'ingame'
        pass

    def give_3(self):
        """Give 3 cards to the table"""

        # te funkcje maja na poczatku 'if' i tylko czekaja na spelniony
        # warunek czyli aby table.game_state osiagnal ich stan.
        # bo po osiagnieciu tego stanu automatycznie sie zalaczaja
        #
        # a kiedy osiagna ten stan? jak funkcja make_decission() (checker)
        # uzna ze wszyscy gracze wrzucili ta sama ilosc $ do puli

        pass

    def give_1(self):
        """Give 1 card to the table"""
        pass

    def give_1_again(self):
        """Give 1 card to the table"""
        pass

    def who_win(self):
        """Determines the winner and gives him all the money from the pool."""
        # check who win
        # give him all money from the pool
        # again?: (10sec. -> then -> no('out')) yes: you play on ('ingame'), no: ('out')

        # delete from table and player.table field if no decission... (timer)

        # self.decission = None

        # end_game()
        # start game again: zero()
        pass