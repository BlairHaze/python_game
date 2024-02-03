from flask import Flask, render_template, redirect, url_for, request, flash, get_flashed_messages
from game import Game

app = Flask(__name__)
app.secret_key = '0dbf3b3e-3f3d-4f3f-8f3f-3f3f3f3f3f3f'
game_instance = None  # Will be initialized when starting the game

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/start_singleplayer', methods=['GET', 'POST'])
def start_singleplayer():
    global game_instance

    if request.method == 'POST':
        player_name = request.form['player_name']
        game_instance = Game(player1_name=player_name)
        return redirect(url_for('board'))

    return render_template('singleplayer.html')

###### HOTSEAT ######

@app.route('/start_hotseat', methods=['GET', 'POST'])
def start_hotseat():
    global game_instance

    if request.method == 'POST':
        player1_name = request.form['player1_name']
        player2_name = request.form['player2_name']
        game_instance = Game(player1_name=player1_name, player2_name=player2_name)
        return redirect(url_for('hotseat_board'))

    return render_template('hotseat.html')

@app.route('/hotseat_board')
def hotseat_board():
    global game_instance
    
    if game_instance is None:
        return redirect(url_for('index'))

    # Display the decks of both players on the web page
    player1_deck = game_instance.player1.deck if game_instance.player1 else []
    player2_deck = game_instance.player2.deck if game_instance.player2 else []

    # Get flashed error messages
    error_messages = get_flashed_messages(category_filter=['error'])

    # Enumerate the stacks on the table and pass them to the template
    enumerated_table = list(enumerate(game_instance.table))

    return render_template('hotseat_board.html', player1_deck=player1_deck, player2_deck=player2_deck,
                           error_messages=error_messages, game_instance=game_instance, enumerated_table=enumerated_table)

@app.route('/start_online', methods=['GET', 'POST'])
def start_online():
    global game_instance

    if request.method == 'POST':
        player_name = request.form['player_name']
        # Handle online game initialization here if needed
        game_instance = Game(player1_name=player_name)
        return redirect(url_for('board'))

    return render_template('online.html')

@app.route('/board')
def board():
    global game_instance
    
    if game_instance is None:
        return redirect(url_for('index'))

    # Display the player's deck on the web page
    player_deck = game_instance.player1.deck if game_instance.player1 else []

    # Get flashed error messages
    error_messages = get_flashed_messages(category_filter=['error'])

    return render_template('board.html', player_deck=player_deck, error_messages=error_messages, game_instance=game_instance)
    
@app.route('/put_cards_on_table', methods=['POST'])
def put_cards_on_table():
    global game_instance

    if game_instance:
        # Get selected card indices from the form
        selected_cards_indices = request.form.get('card_indices')
        selected_cards_indices = [int(idx.strip()) for idx in selected_cards_indices.split(',')]

        # Call the put_cards_on_table method in the Game class
        success, message = game_instance.put_cards_on_table(selected_cards_indices)

        # Flash the error message if not successful
        if not success:
            flash(message, 'error')

        # Redirect based on the game mode
        if game_instance.get_game_mode() == 'hotseat':
            return redirect(url_for('hotseat_board'))
        elif game_instance.get_game_mode() == 'singleplayer':
            return redirect(url_for('board'))

    return redirect(url_for('index'))


@app.route('/add_cards_to_stack', methods=['POST'])
def add_cards_to_stack():
    global game_instance

    if game_instance is None:
        return redirect(url_for('index'))

    # Get selected card indices, stack index, and position from the form
    selected_cards_indices = request.form.get('card_indices')
    stack_index = int(request.form.get('stack_index'))

    # Convert selected card indices to a list of integers
    selected_cards_indices = [int(idx.strip()) for idx in selected_cards_indices.split(',')]

    # Call the add_cards_to_stack method in the Game class
    success, message = game_instance.add_cards_to_stack(selected_cards_indices, stack_index)

    # Flash the error message if not successful
    if not success:
        flash(message, 'error')

    # Redirect based on the game mode
    if game_instance.get_game_mode() == 'hotseat':
        return redirect(url_for('hotseat_board'))
    elif game_instance.get_game_mode() == 'singleplayer':
        return redirect(url_for('board'))

    return redirect(url_for('index'))


@app.route('/draw_cards', methods=['POST'])
def draw_cards():
    global game_instance

    if game_instance:
        game_instance.draw_cards()

        if game_instance.get_game_mode() == 'hotseat':
            return redirect(url_for('hotseat_board'))
        else:
            return redirect(url_for('board'))

    return redirect(url_for('index'))



if __name__ == '__main__':
    app.run(debug=True)