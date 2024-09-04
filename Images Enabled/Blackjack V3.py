#!/usr/bin/env python
# coding: utf-8

# # Blackjack

# Disclaimer:
# This Python Blackjack Game is purely for entertainment purposes and does not involve real money or actual gambling. No financial transactions are associated with this game. The outcome of each hand is determined by random chance, and while there is some element of strategy involved in deciding when to hit or stand, there is no guarantee of winning. Please play responsibly and within your means. If you experience any negative emotions related to gambling, consider seeking professional help.

# In[2]:


import tkinter as tk
from tkinter import messagebox
from PIL import Image, ImageTk
import random
import os

class BlackjackGame:
    def __init__(self, root):
        self.root = root
        self.root.title("Blackjack Game")
        self.balance = 1000
        self.bet_amount = 0
        self.player_hand = []
        self.split_hand = []
        self.dealer_hand = []
        self.active_hand = 'player'
        self.card_labels = []  # To keep references to image objects
        self.card_image_dir = r'C:\Users\arjun\cards'  # Ensure this is the correct path
        self.chip_image_dir = self.card_image_dir  # Chip images are in the same directory as card images
        
        # Load card and chip images
        self.card_images = self.load_card_images()
        self.chip_images = self.load_chip_images()
        
        # Create and shuffle the deck
        self.deck = self.create_deck()
        self.shuffle_deck()
        
        # Set up the GUI
        self.create_widgets()

    def load_card_images(self):
        images = {}
        suits = ['hearts', 'diamonds', 'clubs', 'spades']
        ranks = ['2', '3', '4', '5', '6', '7', '8', '9', '10', 'jack', 'queen', 'king', 'ace']
        for suit in suits:
            for rank in ranks:
                image_path = os.path.join(self.card_image_dir, f'{rank}_of_{suit}.png')
                img = Image.open(image_path)
                img = img.resize((100, 150), Image.LANCZOS)
                images[f"{rank}_of_{suit}"] = ImageTk.PhotoImage(img)
        back_image_path = os.path.join(self.card_image_dir, 'back.png')
        img = Image.open(back_image_path)
        img = img.resize((100, 150), Image.LANCZOS)
        images['back'] = ImageTk.PhotoImage(img)
        return images

    def load_chip_images(self):
        chip_images = {}
        chip_values = [10, 50, 100, 500]
        for value in chip_values:
            image_path = os.path.join(self.chip_image_dir, f'{value}.png')
            img = Image.open(image_path)
            img = img.resize((30, 30), Image.LANCZOS)
            chip_images[f"chip_{value}"] = ImageTk.PhotoImage(img)
        return chip_images

    def create_widgets(self):
        # Balance Label
        self.balance_label = tk.Label(self.root, text=f"Balance: ₹{self.balance}")
        self.balance_label.pack()
        
        # Bet Input
        self.bet_label = tk.Label(self.root, text="Enter your bet amount:")
        self.bet_label.pack()
        self.bet_entry = tk.Entry(self.root)
        self.bet_entry.pack()
        
        # Chip Buttons
        self.chip_frame = tk.Frame(self.root)
        self.chip_frame.pack()
        chip_values = [10, 50, 100, 500]
        for value in chip_values:
            chip_button = tk.Button(self.chip_frame, image=self.chip_images[f"chip_{value}"], command=lambda v=value: self.add_chip_to_bet(v))
            chip_button.pack(side=tk.LEFT)
        
        # Bet Button
        self.bet_button = tk.Button(self.root, text="Place Bet", command=self.place_bet)
        self.bet_button.pack()
        
        # Dealer Hand
        self.dealer_label = tk.Label(self.root, text="Dealer's Hand:")
        self.dealer_label.pack()
        self.dealer_frame = tk.Frame(self.root)
        self.dealer_frame.pack()
        
        # Player Hand
        self.player_label = tk.Label(self.root, text="Player's Hand:")
        self.player_label.pack()
        self.player_frame = tk.Frame(self.root)
        self.player_frame.pack()
        
        # Split Hand Frame
        self.split_label = tk.Label(self.root, text="Split Hand:")
        self.split_label.pack()
        self.split_frame = tk.Frame(self.root)
        self.split_frame.pack()
        
        # Action Buttons
        self.hit_button = tk.Button(self.root, text="Hit", command=self.hit, state=tk.DISABLED)
        self.hit_button.pack(side=tk.LEFT)
        self.stand_button = tk.Button(self.root, text="Stand", command=self.stand, state=tk.DISABLED)
        self.stand_button.pack(side=tk.LEFT)
        self.double_down_button = tk.Button(self.root, text="Double Down", command=self.double_down, state=tk.DISABLED)
        self.double_down_button.pack(side=tk.LEFT)
        self.split_button = tk.Button(self.root, text="Split", command=self.split, state=tk.DISABLED)
        self.split_button.pack(side=tk.LEFT)

    def add_chip_to_bet(self, value):
        self.bet_amount += value
        self.bet_entry.delete(0, tk.END)  # Clear the current value in the Entry widget
        self.bet_entry.insert(tk.END, str(self.bet_amount))  # Insert the updated bet amount as a string

    def create_deck(self):
        suits = ['hearts', 'diamonds', 'clubs', 'spades']
        ranks = ['2', '3', '4', '5', '6', '7', '8', '9', '10', 'jack', 'queen', 'king', 'ace']
        deck = [(rank, suit) for suit in suits for rank in ranks]
        return deck

    def shuffle_deck(self):
        random.shuffle(self.deck)

    def deal_card(self):
        if len(self.deck) < 15:
            self.deck = self.create_deck()
            self.shuffle_deck()
        return self.deck.pop()

    def calculate_hand_value(self, hand):
        value = 0
        aces = 0
        for card in hand:
            rank = card[0]
            if rank in ['jack', 'queen', 'king']:
                value += 10
            elif rank == 'ace':
                value += 11
                aces += 1
            else:
                value += int(rank)
        while value > 21 and aces > 0:
            value -= 10
            aces -= 1
        return value

    def place_bet(self):
        try:
            self.bet_amount = int(self.bet_entry.get())
            if self.bet_amount > self.balance or self.bet_amount <= 0:
                raise ValueError("Invalid bet amount")
        except ValueError:
            messagebox.showerror("Error", "Please enter a valid bet amount")
            self.bet_amount = 0
            return
        self.balance -= self.bet_amount
        self.update_balance()
        self.start_round()

    def update_balance(self):
        self.balance_label.config(text=f"Balance: ₹{self.balance}")

    def start_round(self):
        # Clear previous hands
        for widget in self.dealer_frame.winfo_children():
            widget.destroy()
        for widget in self.player_frame.winfo_children():
            widget.destroy()
        for widget in self.split_frame.winfo_children():
            widget.destroy()
        
        self.player_hand = [self.deal_card(), self.deal_card()]
        self.dealer_hand = [self.deal_card(), self.deal_card()]
        self.split_hand = []
        self.active_hand = 'player'
        self.card_labels.clear()  # Clear the old image references
        
        # Show dealer's first card and hide the second
        dealer_card_label = tk.Label(self.dealer_frame, image=self.card_images[self.dealer_hand[0][0] + "_of_" + self.dealer_hand[0][1]])
        dealer_card_label.pack(side=tk.LEFT)
        self.card_labels.append(dealer_card_label)
        self.dealer_hidden_label = tk.Label(self.dealer_frame, image=self.card_images['back'])
        self.dealer_hidden_label.pack(side=tk.LEFT)
        self.card_labels.append(self.dealer_hidden_label)
        
        for card in self.player_hand:
            card_label = tk.Label(self.player_frame, image=self.card_images[card[0] + "_of_" + card[1]])
            card_label.pack(side=tk.LEFT)
            self.card_labels.append(card_label)
        
        self.hit_button.config(state=tk.NORMAL)
        self.stand_button.config(state=tk.NORMAL)
        
        if self.calculate_hand_value(self.player_hand) == 21:
            messagebox.showinfo("Blackjack!", "Blackjack! You win!")
            self.balance += self.bet_amount * 2.5
            self.update_balance()
            self.reset_game()
        
        # Enable Double Down and Split if possible
        if len(self.player_hand) == 2:
            self.double_down_button.config(state=tk.NORMAL)
            if self.player_hand[0][0] == self.player_hand[1][0]:
                self.split_button.config(state=tk.NORMAL)

    def hit(self):
        if self.active_hand == 'player':
            self.player_hand.append(self.deal_card())
            hand = self.player_hand
            frame = self.player_frame
        else:
            self.split_hand.append(self.deal_card())
            hand = self.split_hand
            frame = self.split_frame
        
        card_label = tk.Label(frame, image=self.card_images[hand[-1][0] + "_of_" + hand[-1][1]])
        card_label.pack(side=tk.LEFT)
        self.card_labels.append(card_label)
        
        hand_value = self.calculate_hand_value(hand)
        if hand_value > 21:
            if self.active_hand == 'split':
                self.end_split()
            else:
                messagebox.showinfo("Bust!", "You've busted!")
                self.reset_game()

    def stand(self):
        if self.active_hand == 'split':
            self.end_split()
        else:
            self.dealer_play()

    def double_down(self):
        if self.balance < self.bet_amount:
            messagebox.showerror("Error", "Not enough balance to double down")
            return
        self.balance -= self.bet_amount
        self.bet_amount *= 2
        self.update_balance()
        self.hit()
        if self.calculate_hand_value(self.player_hand) <= 21:
            self.dealer_play()

    def split(self):
        self.split_hand = [self.player_hand.pop()]
        for widget in self.player_frame.winfo_children():
            widget.destroy()
        for card in self.player_hand:
            card_label = tk.Label(self.player_frame, image=self.card_images[card[0] + "_of_" + card[1]])
            card_label.pack(side=tk.LEFT)
            self.card_labels.append(card_label)
        for card in self.split_hand:
            card_label = tk.Label(self.split_frame, image=self.card_images[card[0] + "_of_" + card[1]])
            card_label.pack(side=tk.LEFT)
            self.card_labels.append(card_label)
        
        self.split_button.config(state=tk.DISABLED)
        self.hit_button.config(state=tk.NORMAL)
        self.stand_button.config(state=tk.NORMAL)
        self.double_down_button.config(state=tk.DISABLED)

    def end_split(self):
        self.active_hand = 'player'
        self.hit_button.config(state=tk.DISABLED)
        self.stand_button.config(state=tk.DISABLED)
        self.dealer_play()

    def dealer_play(self):
        self.dealer_hidden_label.config(image=self.card_images[self.dealer_hand[1][0] + "_of_" + self.dealer_hand[1][1]])
        dealer_value = self.calculate_hand_value(self.dealer_hand)
        player_value = self.calculate_hand_value(self.player_hand)
        split_value = self.calculate_hand_value(self.split_hand)
        
        while dealer_value < 17:
            self.dealer_hand.append(self.deal_card())
            card_label = tk.Label(self.dealer_frame, image=self.card_images[self.dealer_hand[-1][0] + "_of_" + self.dealer_hand[-1][1]])
            card_label.pack(side=tk.LEFT)
            self.card_labels.append(card_label)
            dealer_value = self.calculate_hand_value(self.dealer_hand)
        
        if dealer_value > 21:
            messagebox.showinfo("Dealer Bust!", "Dealer busts! You win!")
            self.balance += self.bet_amount * 2
        else:
            if player_value > 21:
                player_result = "lose"
            elif dealer_value > player_value:
                player_result = "lose"
            elif dealer_value < player_value:
                player_result = "win"
            else:
                player_result = "push"
            
            if player_result == "win":
                messagebox.showinfo("You Win!", "You win the hand!")
                self.balance += self.bet_amount * 2
            elif player_result == "push":
                messagebox.showinfo("Push", "It's a push! You get your bet back.")
                self.balance += self.bet_amount
            else:
                messagebox.showinfo("You Lose", "Dealer wins.")
        
        self.update_balance()
        self.reset_game()

    def reset_game(self):
        self.bet_amount = 0
        self.bet_entry.delete(0, tk.END)
        self.hit_button.config(state=tk.DISABLED)
        self.stand_button.config(state=tk.DISABLED)
        self.double_down_button.config(state=tk.DISABLED)
        self.split_button.config(state=tk.DISABLED)

# Create the main window
root = tk.Tk()
game = BlackjackGame(root)
root.mainloop()


# In[ ]:




