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
        """Return list with all players with 'start' state in this table"""

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
        if self.all_players_in_game_make_decision():

            # 1. Change game state to next from path (give_2, give_3, etc.)

            # 2. Call function by game_state (look up)

            # 3. Change game state for players 'in game' to 'start'
            # (whe we go to the 'winner' function - that function change totally ALL PLAYERS status to 'start')
            self.set_all_in_game_players_state('start')

            # zrobic tak aby status gry po kazdej parze podjetych decyzji sie
            # zmienial i aby dojsc do winner
            # a jak dojde to winner to niech narazie nic nie robi
            # tylko zmienia status WSZYSTKICH zapisanych do stolu graczy
            # na start...

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