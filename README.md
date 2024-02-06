# Machiavelli

This project is a Machiavelli game made in Python using flask.
It has 2 modes:
1. Singleplayer
2. Hotseat
# The Rules of Machiavelli

## The player has 3 aviable actions

1. Draw a card
2. Put a valid combination of cards on the table
3. Put a card in one of the stacks already on the table (it needs to be a valid combination together)

Each of these actions uses up the player's turn

## The game

1. The players are dealt 6 cards from a deck of 104 cards
2. Before the player can edit the current state of the table, they have to put a valid combination on it at least once
3. The goal of the game is to have less cards in your hand the opponent
4. When the stack of cards from which the players draw their cards runs out of cards the player with the least amount of cards in their hand wins

## Valid card combinations

- Three or more cards with the same rank and different suits (for example. 7♥ 7♦ 7♠)
- Three or more cards with the same suit and sequential values (for example. 3♠ 4♠ 5♠)