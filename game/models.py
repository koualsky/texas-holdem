from django.db import models
from django.contrib.auth.models import User

# Later: count and verify 'max_length' fields in my models

class Player(models.Model):
    """Attributes and methods for 'Player'"""

    # Attributes
    name = models.OneToOneField(User, on_delete=models.CASCADE, related_name='player', unique=True)
    money = models.IntegerField(default=100)
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

    def return_next(self, players_list, start_player):
        """Return player - next from start player"""

        length = len(players_list)
        indx = players_list.index(start_player)
        print(players_list)
        print(start_player)
        if indx == length - 1:
            print(players_list[0])
            return players_list[0]
        else:
            print(players_list[indx + 1])
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

            # 2. Take 'small blind' from 'small_blind' player
            self.pool += 1
            self.small_blind.money -= 1
            self.small_blind.save()

            # 3. Set game status to 'dealer'
            self.game_state = 'small_blind'
            self.save()

    def take_big_blind(self):
        """Take big blind from the next one from 'small blind player'"""

        # 1. If game state is 'small_blind' and in game is more than 2 players
        # we can take big_blind
        if self.game_state == 'small_blind' and self.all_players() > 2:





            # 1. Save to small_blind field 'player' next from 'dealer' player
            players_list = self.all_players()
            self.small_blind = self.return_next(players_list, self.dealer)

            # 2. Take 'small blind' from 'small_blind' player
            self.pool += 1
            self.small_blind.money -= 1
            self.small_blind.save()





            # 3. Set game status to 'dealer'
            self.game_state = 'big_blind'
            self.save()

    def decission(self):
        """After ech deal, the player must make a decission: check/call, raise, pass"""

        # check (if no one raise pool)
        # call (automatically add the requires minimum amount of money to the pool)
        # raise (you can raise pool)
        # pass (change your status to 'pass' - you don't allow to make changes in this game)

        # timer - if you dont make a decission in 10 sek. you automatically get status: 'ingame'
        pass

    def give_3(self):
        """Give 3 cards to the table"""
        pass

    # decission() - 3 cards on the table

    def give_1(self):
        """Give 1 card to the table"""
        pass

    # decission() - 4 cards on the table

    def give_1_again(self):
        """Give 1 card to the table"""
        pass

    # decission() - 5 cards on the table. This is the final decission!

    def who_win(self):
        """Determines the winner and gives him all the money from the pool."""
        # check who win
        # give him all money from the pool
        # again?: (10sec. -> then -> no('out')) yes: you play on ('ingame'), no: ('out')

        # delete from table and player.table field if no decission... (timer)

        # end_game()
        # start game again: zero()
        pass