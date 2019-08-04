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
    # (out, wait_for_start, start, check, call, raise, pass)
    # table = models.ForeignKey(Table, on_delete=models.CASCADE)
    table = models.IntegerField(null=True)

    def __str__(self):
        return str(self.name)

    # Assistant Methods
    def change_name(self):
        """Change your name. Only on start page."""
        pass

    def play(self):
        """After click 'Play'. Check which of the running games has free place
        or create a new Game"""
        pass

    def join(self, player):  # Table method?
        """If gamer have 'wait_for_start' status -> add him to Table.players"""
        pass

    # Change States
    def outt(self):
        """ You'll not in the game any more. But you can watch"""

        # delete my name from Game.players (get_object_or_404, and func to dlete from players field)
        # change my state to: 'out'

        self.state = 'out'

    def wait_for_start(self):  # sit
        """Sit to the chosen place. The game will start after the turn. State for players who are 'out' of the game"""
        self.state = 'wait_for_start'

    def startt(self):
        self.state = 'start'

    def checkk(self):
        self.state = 'checkk'

    def calll(self):
        self.state = 'calll'

    def raisee(self):
        self.state = 'raisee'

    def passs(self):
        self.passs = 'passs'


class Table(models.Model):  # Game
    """Attributes and methods for the Table"""

    # Attributes
    player1 = models.CharField(max_length=200, null=True)
    player2 = models.CharField(max_length=200, null=True)
    player3 = models.CharField(max_length=300, null=True)
    player4 = models.CharField(max_length=300, null=True)
    dealer = models.CharField(max_length=200, null=True)
    pool = models.IntegerField(default=0)
    deck = models.CharField(max_length=500, null=True)
    cards_on_table = models.CharField(max_length=100, null=True)
    # path = models.CharField(max_length=200)  # ?????????????????????????????

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

    # Assistant Methods

    def how_many_players(self):
        """Count how many players is in the particular game"""

        # count commas from self.players
        # 0 commas or empty field: zero
        # 1 comma: one
        # etc.
        # return 0
        pass

    # Game Methods
    def zero(self):
        """Start game by give: dealer, small_blind and big blind buttons"""

        # PRECONDITION: All game must go in one view (e.g. .../game/id_17). Based on statuses.
        # Everyone can see game, but only registeres players can make decissions

        # dealer() (if no one have dealer -> give to the first player, if someone have dealer -> next)
        # small_blind() (get $ to pool from next player of dealer)
        # big_blind() (get $ to pool from 2 steps player of dealer)
        # give 2 cards to each player (everyone can only see their cards)
        pass

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

    def give_1(self):
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
