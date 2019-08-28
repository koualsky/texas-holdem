Texas Hold'em Poker

Max 4 players can play at the table.
Players are automatically allocated to the tables.
Game is running if minimum 2 players is on the table.
You don't want to register? No problem, 'Play as a guest'.

Responsible.

HOW TO RUN:
virtualenv venv
cd venv/scripts
activate
pip install -r requirements.txt
python manage.py migrate
docker run -p 6379:6379 -d redis:2.8
python manage.py runserver