# Casino Application

## Introduction

### Overview

This project involves the development of a casino games application using Python and the Tkinter library for the graphical user interface (GUI). The game provides an interactive and engaging way to play Blackjack, Dice Game, and Limbo, simulating a real casino environment where the user competes against the dealer. The application includes features such as placing bets, hitting, standing, doubling down, and splitting hands in Blackjack, rolling dice in the Dice Game, and predicting outcomes in Limbo.

### Objectives


- To implement the core functionalities of Blackjack, including dealing cards, calculating hand values, and managing bets.
- To develop the Dice Game, allowing users to roll dice and win based on the outcome.
- To create the Limbo game, where users predict outcomes and win based on their predictions.
- To provide a simple and intuitive GUI for a seamless gaming experience.

## Blackjack Game Overview

### What is Blackjack?

Blackjack, also known as 21, is one of the most popular casino card games worldwide. The goal is to have a hand value closer to 21 than the dealer’s without exceeding 21. Players are dealt two initial cards and can choose to receive additional cards (hit) or keep their current hand (stand).

### How to Play Blackjack

- **Initial Deal:** Each player is dealt two cards, and the dealer receives two cards (one face up and one face down).
- **Player’s Turn:** Players can choose to 'hit' (receive another card) or 'stand' (keep their current hand). They can also 'double down' (double their bet and receive one more card) or 'split' (if the two initial cards are of the same value).
- **Dealer’s Turn:** The dealer reveals their face-down card and must hit until their hand value is 17 or higher.
- **Winning:** The player wins if their hand value is closer to 21 than the dealer’s without exceeding 21. A hand value over 21 is a 'bust,' resulting in an automatic loss.

### How to Play Dice Game

- **Placing Bets:** Players place their bets on the outcome of the dice roll.
- **Rolling Dice:** The player chooses a target number and chooses whether the dice 'Rolls Over' or 'Rolls Under' and click 'Roll Dice'.
- **Winning:** The player wins if the number obtained post rolling matches their bet prediction. The Bet amount is won by the player if he wins the bet else the player looses that amount.

### How to Play Limbo

- **Placing Bets:** Players place their bets and predict a multiplier value.
- **Game Start:** The game generates a random multiplier.
- **Winning:** The player wins if the generated multiplier is higher than their predicted value. The payout is calculated based on the predicted multiplier and the actual multiplier.

## Application Features

- **Graphical User Interface (GUI):** Developed using Tkinter, providing an interactive interface for gameplay.
- **Bet Management:** Allows users to place bets and manage their balance.
- **Game Actions:** Implemented core game actions such as hit, stand, double down, and split for Blackjack; rolling dice for Dice Game; and predicting multipliers for Limbo.
- **Game State Management:** Automatically handles the game state, including shuffling the deck, rolling dice, generating multipliers, and resetting the game after each round.


## Implementation

### Libraries and Tools

- **Python:** Main programming language.
- **Tkinter:** Used for creating the GUI.
- **Random:** Used for shuffling the deck and dealing cards, rolling dice, and generating random multipliers in the Limbo game.

### Code Structure

The application code is organized into several key sections for each game:

#### Blackjack Game

1. **Imports and Initial Setup:** Import necessary libraries and initialize constants like the deck of cards, balance, and other game-specific variables.
2. **Helper Functions:** Define functions for dealing cards, and calculating hand values.
3. **BlackjackApp Class:** Main class encapsulating all Blackjack game logic, including GUI elements, game actions, and state management.

#### Dice Game

1. **Imports and Initial Setup:** Import necessary libraries and initialize constants like the dice, balance, and other game-specific variables.
2. **Helper Functions:** Define functions for rolling.
3. **DiceGame Class:** Class encapsulating all Dice game logic, including GUI elements, game actions, and state management.

#### Limbo Game

1. **Imports and Initial Setup:** Import necessary libraries and initialize constants like the multipliers, balance, and other game-specific variables.
2. **Helper Functions:** Define functions for generating multipliers.
3. **LimboGame Class:** Class encapsulating all Limbo game logic, including GUI elements, game actions, and state management.

### Detailed Code Explanation

### Dice Game
**Imports and Initial Setup**

- Balance: Starting balance for the player, initially set to 1000.
- Target Number: The target number is set to 50 on a slider.
- Chosen Option: The "Roll under" option is chosen initially.

**Helper Functions**

- Calculate Win Amount: This function calculates the amount won based on the bet and the probability.

**Dice Game Class**

- Initialization: Initializes the Blackjack game window, setting up the initial state and creating the GUI components.
- Create Widgets: Sets up the GUI components, including labels, buttons, and entry fields for displaying game information and allowing user actions.
- Set Bet Options: Sets the chosen betting option and updates the result label with the selected option and target value.
- Roll Dice: Simulates a dice roll, updates the user's balance based on the bet and result, and displays the outcome.
- Update Balance: Updates the balance label to reflect the current balance.
- Go Back to Menu: Closes the current window and reopens the start window.

### Limbo Game
**Imports and Initial Setup**

- Balance: Starting balance for the player, initially set to 1000.
- Bet Amount: the initial bet amount will be 10.
- Multiplier Value: Starting Multiplier value is set to 2.

**Helper Functions**

- Play Limbo: The play_limbo function handles the betting logic, calculates win probability, determines the game result, updates the balance, and displays the outcome.

**Limbo Class**

- Initialization: Initializes the Blackjack game window, setting up the initial state and creating the GUI components.
- Create Widgets: Sets up the GUI components, including labels, buttons, and entry fields for displaying game information and allowing user actions.
- Update Balance: Updates the balance label to reflect the current balance.

### Blackjack Game
**Imports and Initial Setup**

- Balance: Starting balance for the player, initially set to 1000.
- Deck: List representing a standard deck of 52 cards, with each card appearing four times.
- Card Values: Dictionary mapping each card to its corresponding value in Blackjack. Face cards (J, Q, K) are worth 10, and an Ace (A) can be worth either 1 or 11.

**Helper Functions**

- Deal Card: Selects a random card from the deck, removes it from the deck, and returns it.
- Calculate Hand Value: Calculates the total value of a hand. If the total value exceeds 21 and there are Aces in the hand, it reduces the total value by 10 for each Ace until the value is 21 or less, or there are no more Aces to adjust.


**BlackjackApp Class**

- Initialization: Initializes the Blackjack game window, setting up the initial state and creating the GUI components.
- Create Widgets: Sets up the GUI components, including labels, buttons, and entry fields for displaying game information and allowing user actions.
- Update Balance: Updates the balance label to reflect the current balance.
- Place Bet: Validates the bet amount and starts a new round if the bet is valid.
- Start Round: Starts a new round by dealing hands to the player and dealer, and updates the hand labels. If the player has a Blackjack, they win immediately.
- Enable Actions: Enables the action buttons (hit, stand, double down, split) based on the current hand.
- Disable Actions: Disables the action buttons to prevent further actions during certain game states.
- Hit: Adds a card to the player's hand and checks if the player has busted.
- Stand: Ends the player's turn and proceeds to the dealer's turn.
- Double Down: Doubles the bet, deals one more card, and checks if the player has busted.
- Split: Splits the player's hand into two hands if they have two cards of the same value, and plays each hand separately.
- Play Hand: Plays a split hand, checking for Blackjack and enabling actions.
- End Round: Ends the round, determining the outcome based on the player's and dealer's hand values, updating the balance, and resetting the bet.
- Reset Bet: Resets the bet entry field.
- Shuffle Deck: Shuffles the deck when the number of remaining cards is low.

## Main Execution

The main part of the application initializes the main application window and starts the Tkinter main loop. 

## Conclusion

This Python Blackjack game project successfully demonstrates the integration of game logic with a graphical user interface. The game is designed to provide a realistic and engaging Blackjack experience, with functionalities that mirror a real casino environment. The use of Python and Tkinter allows for a simple yet effective implementation, making the game both fun and educational for users interested in learning about game development and GUI design.
