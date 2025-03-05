# Gambling Games Collection

## Overview

This is a desktop gambling games application built using Python and Tkinter, featuring multiple casino-style games. The application provides an interactive platform for users to play Blackjack, Dice Roll, and Limbo games with a virtual balance.

## 🎮 Games Included

### 1. Blackjack
- Classic Blackjack gameplay
- Split hand functionality
- Double down option
- Realistic card graphics
- Balance tracking and betting system

### 2. Dice Roll Game
- Over/Under betting mechanism
- Customizable target number
- Dynamic win probability calculation
- Real-time balance updates

### 3. Limbo Game
- Multiplier-based betting
- Probability-driven gameplay
- Adjustable risk levels
- Win/loss tracking

## 🚨 Responsible Gaming Features

The application includes several features to promote responsible gambling:
- Balance warning system
- Warnings when significant portions of initial balance are lost
- Help resources for gambling addiction
- Option to reset balance
- Psychological warning messages

## 📋 Prerequisites

- Python 3.7+
- Tkinter (usually comes pre-installed with Python)
- Pillow (PIL) library
- Random module

## 🔧 Installation

1. Clone the repository:
```bash
git clone https://github.com/yourusername/gambling-games.git
cd gambling-games
```

2. Install required dependencies:
```bash
pip install pillow
```

3. Ensure you have the required card and chip image files in the correct directory:
   - Card images should be in `C:\Users\arjun\cards\`
   - Naming convention: `{rank}_of_{suit}.png` (e.g., `ace_of_hearts.png`)
   - Include a `back.png` for card back
   - Chip images named as `{value}.png` (e.g., `10.png`, `50.png`)

## 🖥️ User Interface

### Start Window
- Choose between Blackjack, Dice Roll, and Limbo games
- Themed background image

### Game Windows
- Consistent color scheme
- Intuitive controls
- Real-time balance tracking
- Interactive betting mechanisms

## 🎯 Game Mechanics

### Blackjack
- Standard Blackjack rules
- Hit, Stand, Double Down, Split options
- Dealer AI following standard casino rules

### Dice Roll
- Choose to bet "Under" or "Over" a target number
- Dynamic win calculation based on probability

### Limbo
- Set a multiplier and bet amount
- Win if random result meets probability conditions

## ⚠️ Responsible Gambling Warnings

The application includes built-in warnings:
- Alerts when balance drops to certain thresholds
- Psychological intervention messages
- Links to gambling addiction resources

## 🛠️ Customization

You can easily modify:
- Initial balance
- Betting limits
- Game-specific parameters

## 🔒 Disclaimer

This is a simulation game. Real gambling can be addictive and harmful. Always gamble responsibly.

## 🤝 Contributing

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request
