# Texas Hold'em Poker

![logo](https://rawcdn.githack.com/koualsky/texas-holdem/develop/logo.png)

App allows to play online in texas holdem poker with other players.  
Project maked by: python, django, html, bootstrap, js, sql, 
redis, django_channels.  
Mobile friendly. Responsive. 

## Game description

Max 4 players can play at the table.
Players are automatically allocated to the tables.
Game is running if minimum 2 players sit on the table.
You don't want to register? No problem, 'Play as a guest'.

## How to run in local host

> pip install -r requirements.txt  
> python manage.py migrate  
> docker run -p 6379:6379 -d redis:2.8  
> python manage.py runserver  

## How to play

The game follows the Texas Holdem Poker rules. The only thing 
you have to do is click 'play'. 
You can play as a registered user or as a guest. 
If you want to 'play as a guest' (at least one player 
must be registered in db).

## Online example

[little-lionfish-33.localtunnel.me](http://little-lionfish-33.localtunnel.me) (Allow browser to read scripts 
from non identified source. Without that, 
the app will not work properly)