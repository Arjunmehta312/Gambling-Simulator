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
import webbrowser

class BlackjackGame:
    def __init__(self, root):
        self.root = root
        self.root.title("Blackjack Game")
        self.root.geometry("400x600")
        self.initial_balance = 1000
        self.balance = self.initial_balance
        self.bet_amount = 0
        self.player_hand = []
        self.split_hand = []
        self.dealer_hand = []
        self.active_hand = 'player'
        self.card_labels = []
        self.card_image_dir = r'C:\Users\arjun\cards'
        self.chip_image_dir = self.card_image_dir
        
        self.card_images = self.load_card_images()
        self.chip_images = self.load_chip_images()
        
        self.deck = self.create_deck()
        self.shuffle_deck()
        
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
        # Set background color for the root window
        self.root.configure(bg="#35654d")  # Existing background color

        # Balance Label
        self.balance_label = tk.Label(self.root, text=f"Balance: ₹{self.balance}", bg="#35654d", fg="white")
        self.balance_label.pack()

        # Bet Input
        self.bet_label = tk.Label(self.root, text="Enter your bet amount:", bg="#35654d", fg="white")
        self.bet_label.pack()
        self.bet_entry = tk.Entry(self.root)
        self.bet_entry.pack()

        # Chip Buttons Frame
        self.chip_frame = tk.Frame(self.root, bg="#35654d")
        self.chip_frame.pack()
        chip_values = [10, 50, 100, 500]
        for value in chip_values:
            chip_button = tk.Button(self.chip_frame, image=self.chip_images[f"chip_{value}"], command=lambda v=value: self.add_chip_to_bet(v))
            chip_button.pack(side=tk.LEFT)

        # Bet Button
        self.bet_button = tk.Button(self.root, text="Place Bet", command=self.place_bet, bg="#D4AF37", fg="#333333", activebackground="#F0E68C", activeforeground="#333333")
        self.bet_button.pack()

        # Dealer Hand
        self.dealer_label = tk.Label(self.root, text="Dealer's Hand:", bg="#35654d", fg="white")
        self.dealer_label.pack()
        self.dealer_frame = tk.Frame(self.root, bg="#35654d")
        self.dealer_frame.pack()

        # Player Hand
        self.player_label = tk.Label(self.root, text="Player's Hand:", bg="#35654d", fg="white")
        self.player_label.pack()
        self.player_frame = tk.Frame(self.root, bg="#35654d")
        self.player_frame.pack()

        # Split Hand Frame
        self.split_label = tk.Label(self.root, text="Split Hand:", bg="#35654d", fg="white")
        self.split_label.pack()
        self.split_frame = tk.Frame(self.root, bg="#35654d")
        self.split_frame.pack()

        # Action Buttons Frame
        self.action_frame = tk.Frame(self.root, bg="#35654d")
        self.action_frame.pack(anchor='center')

        # Action Buttons
        self.hit_button = tk.Button(self.action_frame, text="Hit", command=self.hit, bg="#D4AF37", fg="#333333", activebackground="#F0E68C", activeforeground="#333333", state=tk.DISABLED)
        self.hit_button.pack(side=tk.LEFT, padx=5)

        self.stand_button = tk.Button(self.action_frame, text="Stand", command=self.stand, bg="#D4AF37", fg="#333333", activebackground="#F0E68C", activeforeground="#333333", state=tk.DISABLED)
        self.stand_button.pack(side=tk.LEFT, padx=5)

        self.double_down_button = tk.Button(self.action_frame, text="Double Down", command=self.double_down, bg="#D4AF37", fg="#333333", activebackground="#F0E68C", activeforeground="#333333", state=tk.DISABLED)
        self.double_down_button.pack(side=tk.LEFT, padx=5)

        self.split_button = tk.Button(self.action_frame, text="Split", command=self.split, bg="#D4AF37", fg="#333333", activebackground="#F0E68C", activeforeground="#333333", state=tk.DISABLED)
        self.split_button.pack(side=tk.LEFT, padx=5)

        # Disabled Buttons Styling (gray out text when disabled)
        self.hit_button.config(disabledforeground="#7a7a7a")
        self.stand_button.config(disabledforeground="#7a7a7a")
        self.double_down_button.config(disabledforeground="#7a7a7a")
        self.split_button.config(disabledforeground="#7a7a7a")



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
        self.check_balance_threshold()

    def check_balance_threshold(self):
        thresholds = [0.5, 0.25, 0.125]  # 50%, 25%, 12.5% of initial balance
        for threshold in thresholds:
            if self.balance <= self.initial_balance * threshold and self.balance > self.initial_balance * (threshold / 2):
                self.show_warning(threshold)
                break

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
            if self.player_hand[0][0] == self.player_hand[1][0]:  # Check for Split condition
                self.split_button.config(state=tk.NORMAL)

    def hit(self):
        hand = self.player_hand if self.active_hand == 'player' else self.split_hand
        hand.append(self.deal_card())
        card_label = tk.Label(self.player_frame if self.active_hand == 'player' else self.split_frame, image=self.card_images[hand[-1][0] + "_of_" + hand[-1][1]])
        card_label.pack(side=tk.LEFT)
        self.card_labels.append(card_label)
        
        hand_value = self.calculate_hand_value(hand)
        if hand_value > 21:
            messagebox.showinfo("Bust!", "You busted!")
            self.reset_game()

    def stand(self):
        if self.active_hand == 'split':
            self.active_hand = 'player'
            self.start_dealer_turn()
        else:
            self.start_dealer_turn()

    def double_down(self):
        if self.active_hand == 'player':
            self.balance -= self.bet_amount
            self.bet_amount *= 2
            self.update_balance()
            self.hit()
            self.stand()

    def split(self):
        if len(self.player_hand) == 2 and self.player_hand[0][0] == self.player_hand[1][0]:
            self.split_hand = [self.player_hand.pop()]
            split_card_label = tk.Label(self.split_frame, image=self.card_images[self.split_hand[0][0] + "_of_" + self.split_hand[0][1]])
            split_card_label.pack(side=tk.LEFT)
            self.card_labels.append(split_card_label)
            self.hit_button.config(state=tk.NORMAL)
            self.active_hand = 'split'
        else:
            messagebox.showerror("Error", "Cannot split the hand")

    def start_dealer_turn(self):
        self.dealer_hidden_label.config(image=self.card_images[self.dealer_hand[1][0] + "_of_" + self.dealer_hand[1][1]])
        dealer_value = self.calculate_hand_value(self.dealer_hand)
        
        while dealer_value < 17:
            self.dealer_hand.append(self.deal_card())
            card_label = tk.Label(self.dealer_frame, image=self.card_images[self.dealer_hand[-1][0] + "_of_" + self.dealer_hand[-1][1]])
            card_label.pack(side=tk.LEFT)
            self.card_labels.append(card_label)
            dealer_value = self.calculate_hand_value(self.dealer_hand)
        
        player_value = self.calculate_hand_value(self.player_hand)
        if self.split_hand:
            split_value = self.calculate_hand_value(self.split_hand)
            player_value = max(player_value, split_value)
        
        if dealer_value > 21 or player_value > dealer_value:
            messagebox.showinfo("Winner!", "You win!")
            self.balance += self.bet_amount * 2
        elif dealer_value == player_value:
            messagebox.showinfo("Push", "It's a push!")
            self.balance += self.bet_amount
        else:
            messagebox.showinfo("Lose", "You lose!")
        
        self.update_balance()
        self.reset_game()

    def reset_game(self):
        self.player_hand.clear()
        self.split_hand.clear()
        self.dealer_hand.clear()
        self.bet_amount = 0
        self.bet_entry.delete(0, tk.END)
        self.hit_button.config(state=tk.DISABLED)
        self.stand_button.config(state=tk.DISABLED)
        self.double_down_button.config(state=tk.DISABLED)
        self.split_button.config(state=tk.DISABLED)
        self.dealer_hidden_label.config(image=self.card_images['back'])

    def show_warning(self, threshold):
        percentage = int((1 - threshold) * 100)
        message = f"Warning: You have lost {percentage}% of your initial balance.\n"
        message += "You may be falling for the illusion of gambling and getting addicted slowly.\n\n"
        message += "Do you want to continue playing or stop?"
        
        response = messagebox.askyesno("Gambling Warning", message, icon='warning')
        
        if not response:  # If they choose to stop
            self.show_help_resources()
        else:  # If they choose to continue
            messagebox.showinfo("Continue Playing", "Please gamble responsibly. Remember, the odds are in favor of the house.")

    def show_help_resources(self):
        messagebox.showinfo("Wise Choice", "You've made a wise and correct choice before going down a path you might regret.")
        
        help_window = tk.Toplevel(self.root)
        help_window.title("Gambling Addiction Help Resources")
        help_window.geometry("400x200")
        
        tk.Label(help_window, text="Here are some resources to help you:").pack(pady=10)
        
        links = [
            ("Help Guide - Gambling Addiction", "https://www.helpguide.org/articles/addictions/gambling-addiction-and-problem-gambling.htm"),
            ("Better Health - Changing Gambling Habits", "https://www.betterhealth.vic.gov.au/health/healthyliving/gambling-how-to-change-your-habits"),
            ("National Problem Gambling Helpline", "https://www.ncpgambling.org/help-treatment/")
        ]
        
        for text, url in links:
            link = tk.Label(help_window, text=text, fg="blue", cursor="hand2")
            link.pack(pady=5)
            link.bind("<Button-1>", lambda e, url=url: webbrowser.open_new(url))
        
        tk.Button(help_window, text="Close and Quit Game", command=self.quit_game).pack(pady=10)

    def quit_game(self):
        self.root.quit()

    # Modify the reset_game method to reset the balance
    def reset_game(self):
        self.player_hand.clear()
        self.split_hand.clear()
        self.dealer_hand.clear()
        self.bet_amount = 0
        self.bet_entry.delete(0, tk.END)
        self.hit_button.config(state=tk.DISABLED)
        self.stand_button.config(state=tk.DISABLED)
        self.double_down_button.config(state=tk.DISABLED)
        self.split_button.config(state=tk.DISABLED)
        self.dealer_hidden_label.config(image=self.card_images['back'])
        
        # Check if balance is below 10% of initial balance
        if self.balance < self.initial_balance * 0.1:
            response = messagebox.askyesno("Low Balance", "Your balance is very low. Do you want to reset your balance to the initial amount?")
            if response:
                self.balance = self.initial_balance
                self.update_balance()

if __name__ == "__main__":
    root = tk.Tk()
    game = BlackjackGame(root)
    root.mainloop()


# In[ ]:




