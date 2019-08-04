from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, authenticate
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import Player, Table


# Game
def start(request):
    return render(request, 'game/start.html')


@login_required
def play(request):
    """Add player to free table or create new table from the last id in db +1 (4/table)."""

    # Check if I'm joined to some table. NO:
    if request.user.player.table == None:

        # Select table with free spot if exist or return None
        table = free_table(request)

        # Ok, so we don't have a table with empty spot where we can join - so let's create new Table record with me as a first player
        # and add this table to my 'table' field (I will be joined to this table)
        if table == None:
            table = Table(player1=request.user)
            table.save()
            request.user.player.table = table.pk
            request.user.player.save()

        # If we have a table with empty spot - join to this table and write pk of this table to player 'table' field
        else:
            # Add me to empty slot:
            if table.player1 == None:
                table.player1 = str(request.user)
                table.save()
            elif table.player2 == None:
                table.player2 = str(request.user)
                table.save()
            elif table.player3 == None:
                table.player3 = str(request.user)
                table.save()
            elif table.player4 == None:
                table.player4 = str(request.user)
                table.save()
            request.user.player.table = table.pk
            request.user.player.save()

    # YES, so simply return this table:
    else:
        table = get_object_or_404(Table, pk=int(request.user.player.table))

    return render(request, 'game/table.html', {'table': table})


# Auxiliary methods
def free_table(request):
    """Return table with free spot or 'None'"""
    for table in Table.objects.raw("""
        SELECT * FROM game_table 
        WHERE Player1 IS NULL 
        OR Player2 IS NULL 
        OR Player3 IS NULL 
        OR Player4 IS NULL
        """):
        return table


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
