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

    # PRE
    join(request)
    table = request.user.player.table

    # GAME PATH
    table.start()    # 1. Start  (GAME: ready -> start, PLAYER: 'out' -> 'start')
    table.dealer_button()  # 2. Dealer (GAME: start -> dealer)
    # table.small()  # 3. Small  (GAME: dealer -> small)
    # table.big()    # 4. Big    (GAME: small -> big) (if min. 3 players and ...)
    # in end of Big write check() function, and in end of rest functions... but after Give_1_again no. then only winner()
    # table.give_2   # 5. Give_2 (GAME: big -> give_2, PLAYER: start -> check/call/raise/pass)-after round -> start (if min. 2 plrs)
    # table.give_3   # 6. Give_3 (GAME: give_2 -> give_3, PLAYER: start -> check/call/raise/pass)
    # table.give_1   # 7. Give_1 (GAME: give_3 -> give_1, PLAYER: start -> check/call/raise/pass)
    # table.give_1_ag# 8. Give_1_again (GAME: give_1 -> give_1_again, PLAYER: start -> check/call/raise/pass)
    # table.winner() # 9. Winner (GAME: give_1_again -> give_2, PLAYER: start -> check/call/raise/pass)

    # GAME PATH (ready, start, dealer, small, big, give_2, give_3, give_1, give_1_again, winner)
    # PLAYER PATH (out, ready, start, check, call, raise, pass)

    # Make list from player1, player2 etc. becauce i can't do this in django template language
    players_list = table.all_players()
    return render(request, 'game/table.html', {'table': table, 'players_list': players_list})


# Auxiliary methods
@login_required
def join(request):
    """Joining to the game"""

    # 2. If player 'table' field is empty, start joining to the game procedure
    if request.user.player.table == None:

        table = find_table(request)
        register_player(request, table)


@login_required
def find_table(request):
    """Return table with free spots or return None if tables are full or don't exist"""

    try:
        table = Table.objects.filter(Q(player1=None) | Q(player2=None) | Q(player3=None) | Q(player4=None)).order_by('pk')[0]
    except:
        table = Table.objects.filter(Q(player1=None) | Q(player2=None) | Q(player3=None) | Q(player4=None))

    return table


@login_required
def register_player(request, table):
    """Save table in player.table and save player in table.player1/2/3/4"""

    # Table don't exist in db
    if not table:
        table = Table(player1=request.user.player)
        table.save()
        request.user.player.table = table
        request.user.player.save()

    # We have a table with empty slot
    else:
        table.add_player(request.user.player)
        table.save()
        request.user.player.table = table
        request.user.player.save()


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
