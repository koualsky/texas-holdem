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
    """This is redirect function. Should define wich table is free or if no
    one, create new table from the last id in db +1.
    Add player to free table or create new (4/table).
    """

    # Here should be function define wich table is empty or create new table
    table = 27
    return render(request, 'game/table.html', {'table': table})


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


'''
what i have: 
- auth
- profile

what i need:
- przydzielanie to table
- 
- 
'''
