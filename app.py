from flask import Flask, render_template, redirect, url_for, request, flash, get_flashed_messages
from game import Game

app = Flask(__name__)
app.secret_key = '0dbf3b3e-3f3d-4f3f-8f3f-3f3f3f3f3f3f'
game_instance = None  # Will be initialized when starting the game

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/start_game', methods=['POST'])
def start_game():
    global game_instance

    game_type = request.form['game_type']

    if game_type == 'singleplayer':
        player_name = request.form['player_name']
        game_instance = Game(player1_name=player_name)
    elif game_type == 'hotseat':
        player1_name = request.form['player1_name']
        player2_name = request.form['player2_name']
        game_instance = Game(player1_name=player1_name, player2_name=player2_name)
    elif game_type == 'online':
        # Handle online game initialization here if needed
        pass

    return redirect(url_for('board'))

@app.route('/board')
def board():
    if game_instance:
        # Display the player's deck on the web page
        player_deck = game_instance.player1.deck if game_instance.player1 else []

        # Get flashed error messages
        error_messages = get_flashed_messages(category_filter=['error'])

        return render_template('board.html', player_deck=player_deck, error_messages=error_messages)
    else:
        return redirect(url_for('index'))
    
@app.route('/put_cards_on_table', methods=['POST'])
def put_cards_on_table():
    # Get selected card indices from the form
    selected_cards_indices = request.form.get('card_indices')
    selected_cards_indices = [int(idx.strip()) for idx in selected_cards_indices.split(',')]

    # Call the put_cards_on_table method in the Game class
    success, message = game_instance.put_cards_on_table(selected_cards_indices)

    # Flash the error message if not successful
    if not success:
        flash(message, 'error')

    # Redirect to the board
    return redirect(url_for('board'))

@app.route('/draw_cards', methods=['POST'])
def draw_cards():
    if game_instance:
        # Draw 1 card when the button is pressed
        game_instance.draw_cards()
        return redirect(url_for('board'))
    else:
        return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(debug=True)
