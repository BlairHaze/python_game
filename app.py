from flask import Flask, render_template, redirect, url_for

from game import Game

app = Flask(__name__)
game_instance = Game()  # Create an instance of the game

@app.route('/')
def index():
    # Display the player's deck on the web page
    player_deck = game_instance.player1.deck if game_instance.player1 else []
    return render_template('index.html', player_deck=player_deck)

@app.route('/draw_cards', methods=['POST'])
def draw_cards():
    # Draw 1 card when the button is pressed
    game_instance.draw_cards()
    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(debug=True)
