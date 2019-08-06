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

    # NOT joined to any table:
    if not request.user.player.table:

        # we try to take only one record!
        try:
            table = Table.objects.filter(Q(player1=None) | Q(player2=None) | Q(player3=None) | Q(player4=None)).order_by('pk')[0]

        # but if db has 0 records that upper example return Error. For that reason we have 'except' statement:
        except:
            table = Table.objects.filter(Q(player1=None) | Q(player2=None) | Q(player3=None) | Q(player4=None))

        # NO FREE SPOT. We don't have a table with empty spot where we can join
        if not table:

            # Create new Table with 'user' as first player
            table = Table(player1=get_object_or_404(Player, pk=request.user.player.pk))  # request.user)
            table.save()

            # Add this table to 'user' table (related to table) field
            request.user.player.table = table
            request.user.player.save()

        # FREE SPOT. If we have a table with empty spot - join to this table and write pk of this table to player 'table' field
        else:

            # Check table.player1 was have free spot:
            if table.player1 == None:  # change to not table.player1

                # Add me to empty slot
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

            # Add this table to 'user' table (related to table) field
            request.user.player.table = table
            request.user.player.save()

    # YES, i'm joined to some table, so simply return this table:
    else:
        table = get_object_or_404(Table, pk=int(request.user.player.table.pk))

    return render(request, 'game/table.html', {'table': table})


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

    # 2. Remove Table from my profile
    request.user.player.table = None
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
