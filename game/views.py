from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate
from django.contrib.auth.forms import UserCreationForm


# Game
def start(request):
    return render(request, 'game/start.html')


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
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            raw_password = form.cleaned_data.get('password1')
            user = authenticate(username=username, password=raw_password)
            login(request, user)
            return redirect('start')
    else:
        form = UserCreationForm()
    return render(request, 'registration/register.html', {'form': form})
