from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, authenticate
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.db.models import Q
from .models import Player, Table


# Game
def start(request):
    return render(request, 'game/start.html')


@login_required
def play(request):
    """Add player to free table or create new table from the last id in db +1 (4/table)."""

    # 1. NOT joined to any table:
    if not request.user.player.table:

        # (pre) we try to take only one record!
        try:
            table = Table.objects.filter(Q(player1=None) | Q(player2=None) | Q(player3=None) | Q(player4=None)).order_by('pk')[0]

        # (pre) but if db has 0 records that upper example return Error. For that reason we have 'except' statement:
        except:
            table = Table.objects.filter(Q(player1=None) | Q(player2=None) | Q(player3=None) | Q(player4=None))

        # a) NO FREE SPOT. We don't have a table with empty spot where we can join
        if not table:

            # - Table. Create new Table with 'user' as first player
            table = Table(player1=get_object_or_404(Player, pk=request.user.player.pk))  # request.user)
            table.save()

            # - Player. Add this table to 'user' table (related to table) field
            request.user.player.table = table
            request.user.player.state = 'ready'
            request.user.player.save()

        # b) FREE SPOT. If we have a table with empty spot - join to this table and write pk of this table to player 'table' field
        else:

            # - Table. Check table.player1 was have free spot:
            # If slot is empty: add me to empty slot
            if table.player1 == None:
                table.player1 = get_object_or_404(Player, pk=request.user.player.pk)
                table.save()
            elif table.player2 == None:
                table.player2 = get_object_or_404(Player, pk=request.user.player.pk)
                table.save()
            elif table.player3 == None:
                table.player3 = get_object_or_404(Player, pk=request.user.player.pk)
                table.save()
            elif table.player4 == None:
                table.player4 = get_object_or_404(Player, pk=request.user.player.pk)
                table.save()

            # - Player. Add this table to 'user' table (related to table) field
            request.user.player.table = table
            request.user.player.state = 'ready'
            request.user.player.save()

    # 2. YES, i'm joined to some table, so simply return this table:
    else:
        table = get_object_or_404(Table, pk=int(request.user.player.table.pk))

    # in this point we join to the game and have status 'ready'
    # IN THIS AREA ADD LOGIC OF GAME

    """
    start_game(request)     # IF len(players) > 1 and table.game_status == 'ready': 
                            # table.game_status = 'start'
                            # players.status = 'start'
    zero(request)           # IF table.game_status == 'start': dealer, small, big
                            # table.game_status = 'first player...'

    check(request)          # This function will be call in always, between every below function :)
                            # IF me.status in ['start', 'check', 'call', 'raise'] and table.game_status == 'me':
                                # make choice


    give_2(request)         # 
    give_3(request)
    give_1(request)
    give_1_again(request)
    winner(request)
    """

    start_game(request)
    check(request)

    # Make list from player1, player2 etc. becauce i can't do this in django template language
    players_list = [table.player1, table.player2, table.player3, table.player4]

    return render(request, 'game/table.html', {'table': table, 'players_list': players_list})


@login_required
def exit(request):
    # 1. Remove me from slot in table (set Null to player.table)
    table = request.user.player.table
    player = request.user.player
    if table.player1 == player:
        table.player1 = None
        table.save()
    if table.player2 == player:
        table.player2 = None
        table.save()
    if table.player3 == player:
        table.player3 = None
        table.save()
    if table.player4 == player:
        table.player4 = None
        table.save()

    # 2. If I'm the last player in the game set table state to 'ready'
    if table.how_many_players() < 2:
        table.game_state = 'ready'
        table.save()

    # 3. Remove Table from my profile
    request.user.player.table = None
    request.user.player.state = 'out'
    request.user.player.save()

    # 3. Redirect to start page
    return redirect('start')


# Auxiliary methods
def start_game(request):
    # IF in table is more than 1 player AND game staus is 'ready'
    table = get_object_or_404(Table, pk=request.user.player.table.pk)
    if table.how_many_players() > 1 and table.game_state == 'ready':

        # 1. Change game state to 'start'
        table.game_state = 'start'
        table.save()

        # 2. Give all available (in game) players state 'start'
        if table.player1 and table.player1.state == 'ready':
            table.player1.state = 'start'
            table.player1.save()
        if table.player2 and table.player2.state == 'ready':
            table.player2.state = 'start'
            table.player2.save()
        if table.player3 and table.player3.state == 'ready':
            table.player3.state = 'start'
            table.player3.save()
        if table.player4 and table.player4.state == 'ready':
            table.player4.state = 'start'
            table.player4.save()

        # 3. dealer, small, big

        # a) make list with all available players
        players_list = []
        for player in [table.player1, table.player2, table.player3, table.player4]:
            if player is not None:
                players_list.append(player)

        # b) dealer
        if table.dealer is not None and table.dealer in players_list:

            # if in previous game someone have a dealer. give them next player
            if table.dealer == players_list[-1]:

                # if present dealer is the last player in players_list
                table.dealer = players_list[0]
                table.save()
            else:

                # if no ...
                table.dealer = players_list[players_list.index(table.dealer) + 1]
                table.save()

        else:

            # if in prevous game no one have a dealer. give dealer first player
            table.dealer = players_list[0]
            table.save()

        # c) small_blind

        '''
        - make list with all available players
        - check from table.dealer who have dealer
            - if 1 -> give dealer 2
            - if 4 -> give dealer 1
            - itd.
            - else: -> give dealer 1
        - next from dealer -> small
        - next from small (if exist) -> big
        '''


def check(request):
    print(request.user.player)


# Authentication
def register(request):

    # Create User in db
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            raw_password = form.cleaned_data.get('password1')
            user = authenticate(username=username, password=raw_password)
            login(request, user)

            # Create Player in db
            Player.objects.create(name=user)

            # Back to start page
            return redirect('start')
    else:
        form = UserCreationForm()
    return render(request, 'registration/register.html', {'form': form})
