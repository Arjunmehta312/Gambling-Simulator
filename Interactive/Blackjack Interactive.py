#!/usr/bin/env python
# coding: utf-8

# # Blackjack

# Disclaimer:
# This Python Blackjack Game is purely for entertainment purposes and does not involve real money or actual gambling. No financial transactions are associated with this game. The outcome of each hand is determined by random chance, and while there is some element of strategy involved in deciding when to hit or stand, there is no guarantee of winning. Please play responsibly and within your means. If you experience any negative emotions related to gambling, consider seeking professional help.

# In[4]:


import tkinter as tk
from tkinter import messagebox
from PIL import Image, ImageTk
import random
import os
import webbrowser

class StartWindow:
    def __init__(self, root):
        self.root = root
        self.root.title("Welcome to Blackjack")
        self.root.geometry("800x600")

        self.bg_image = Image.open("C:/Users/arjun/cards/bluff.png")
        self.bg_image = self.bg_image.resize((800, 600), Image.LANCZOS)
        self.bg_photo = ImageTk.PhotoImage(self.bg_image)

        self.bg_label = tk.Label(root, image=self.bg_photo)
        self.bg_label.place(relwidth=1, relheight=1)

        self.blackjack_button = tk.Button(root, text="Blackjack", command=self.start_blackjack, font=("Helvetica", 20), bg="darkgreen", fg="white")
        self.blackjack_button.pack(side=tk.BOTTOM, pady=30)

    def start_blackjack(self):
        self.root.withdraw()
        blackjack_window = tk.Toplevel(self.root)
        BlackjackGame(blackjack_window, self.root)

class BlackjackGame:
    def __init__(self, root, start_window):
        self.root = root
        self.start_window = start_window
        self.root.title("Blackjack Game")
        self.root.geometry("800x600")
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

        self.first_round = True

        self.create_widgets()

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

        if self.first_round:
            self.image1_label.destroy()
            self.image2_label.destroy()
            self.first_round = False

        self.start_round()

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
            img = img.resize((75, 75), Image.LANCZOS)
            chip_images[f"chip_{value}"] = ImageTk.PhotoImage(img)
        return chip_images

    def create_widgets(self):
        self.root.configure(bg="#35654d")

        self.back_button = tk.Button(self.root, text="Back to Menu", command=self.go_back_to_menu, bg="#D4AF37", fg="#333333", activebackground="#F0E68C", activeforeground="#333333", width=20, height=2)
        self.back_button.place(relx=1.0, rely=0.0, anchor='ne')

        self.dealer_label = tk.Label(self.root, text="Dealer's Hand:", bg="#35654d", fg="white")
        self.dealer_label.pack()
        self.dealer_frame = tk.Frame(self.root, bg="#35654d")
        self.dealer_frame.pack()

        self.player_label = tk.Label(self.root, text="Player's Hand:", bg="#35654d", fg="white")
        self.player_label.pack()
        self.player_frame = tk.Frame(self.root, bg="#35654d")
        self.player_frame.pack()

        self.image1_path = r'C:\Users\arjun\cards\back.png'
        self.image2_path = r'C:\Users\arjun\cards\back.png'

        self.image1 = Image.open(self.image1_path)
        self.image1 = self.image1.resize((100, 150), Image.LANCZOS)
        self.image1 = ImageTk.PhotoImage(self.image1)

        self.image2 = Image.open(self.image2_path)
        self.image2 = self.image2.resize((100, 150), Image.LANCZOS)
        self.image2 = ImageTk.PhotoImage(self.image2)

        self.image1_label = tk.Label(self.dealer_frame, image=self.image1, bg="#35654d")
        self.image1_label.pack(side=tk.BOTTOM, pady=10)

        self.image2_label = tk.Label(self.player_frame, image=self.image2, bg="#35654d")
        self.image2_label.pack(side=tk.BOTTOM, pady=10)

        self.balance_label = tk.Label(self.root, text=f"Balance: ₹{self.balance}", bg="#35654d", fg="white")
        self.balance_label.pack()

        self.bet_label = tk.Label(self.root, text="Enter your bet amount:", bg="#35654d", fg="white")
        self.bet_label.pack()
        self.bet_entry = tk.Entry(self.root)
        self.bet_entry.pack()

        self.chip_frame = tk.Frame(self.root, bg="#35654d")
        self.chip_frame.pack()
        chip_values = [10, 50, 100, 500]
        for value in chip_values:
            chip_img = self.chip_images[f"chip_{value}"]
            chip_button = tk.Button(self.chip_frame, image=chip_img, command=lambda v=value: self.add_chip_to_bet(v))
            chip_button.config(width=65, height=65)
            chip_button.pack(side=tk.LEFT, padx=5, pady=5)

        self.bet_button = tk.Button(self.root, text="Place Bet", command=self.place_bet, bg="#D4AF37", fg="#333333", activebackground="#F0E68C", activeforeground="#333333", width=20, height=2)
        self.bet_button.pack()

        self.split_label = tk.Label(self.root, text="Split Hand:", bg="#35654d", fg="white")
        self.split_frame = tk.Frame(self.root, bg="#35654d")
        self.split_label.pack_forget()
        self.split_frame.pack_forget()

        self.action_frame = tk.Frame(self.root, bg="#35654d")
        self.action_frame.pack(anchor='center')

        self.hit_button = tk.Button(self.action_frame, text="Hit", command=self.hit, bg="#D4AF37", fg="#333333", activebackground="#F0E68C", activeforeground="#333333", state=tk.DISABLED, width=15, height=2)
        self.hit_button.pack(side=tk.LEFT, padx=5)

        self.stand_button = tk.Button(self.action_frame, text="Stand", command=self.stand, bg="#D4AF37", fg="#333333", activebackground="#F0E68C", activeforeground="#333333", state=tk.DISABLED, width=15, height=2)
        self.stand_button.pack(side=tk.LEFT, padx=5)

        self.double_down_button = tk.Button(self.action_frame, text="Double Down", command=self.double_down, bg="#D4AF37", fg="#333333", activebackground="#F0E68C", activeforeground="#333333", state=tk.DISABLED, width=15, height=2)
        self.double_down_button.pack(side=tk.LEFT, padx=5)

        self.split_button = tk.Button(self.action_frame, text="Split", command=self.split, bg="#D4AF37", fg="#333333", activebackground="#F0E68C", activeforeground="#333333", state=tk.DISABLED, width=15, height=2)
        self.split_button.pack(side=tk.LEFT, padx=5)

        self.hit_button.config(disabledforeground="#7a7a7a")
        self.stand_button.config(disabledforeground="#7a7a7a")
        self.double_down_button.config(disabledforeground="#7a7a7a")
        self.split_button.config(disabledforeground="#7a7a7a")

    def go_back_to_menu(self):
        self.root.destroy()
        self.start_window.deiconify()

    def split(self):
        if len(self.player_hand) == 2 and self.player_hand[0][0] == self.player_hand[1][0]:
            self.split_hand = [self.player_hand.pop()]
            self.player_frame.winfo_children()[-1].destroy()
            split_card_label = tk.Label(self.split_frame, image=self.card_images[self.split_hand[0][0] + "_of_" + self.split_hand[0][1]])
            split_card_label.pack(side=tk.LEFT)
            self.card_labels.append(split_card_label)

            self.split_label.pack()
            self.split_frame.pack()

            self.hit_button.config(state=tk.NORMAL)
            self.stand_button.config(state=tk.NORMAL)
            self.active_hand = 'player'
            self.split_button.config(state=tk.DISABLED)
            self.double_down_button.config(state=tk.DISABLED)

            # Deal an additional card to each hand
            self.hit('player')
            self.hit('split')
        else:
            messagebox.showerror("Error", "Cannot split the hand")

    def add_chip_to_bet(self, value):
        self.bet_amount += value
        self.bet_entry.delete(0, tk.END)
        self.bet_entry.insert(tk.END, str(self.bet_amount))

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

    def update_balance(self):
        self.balance_label.config(text=f"Balance: ₹{self.balance}")
        self.check_balance_threshold()

    def check_balance_threshold(self):
        thresholds = [0.5, 0.25, 0.125]
        for threshold in thresholds:
            if self.balance <= self.initial_balance * threshold and self.balance > self.initial_balance * (threshold / 2):
                self.show_warning(threshold)
                break

    def start_round(self):
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
        self.card_labels.clear()

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
            self.balance += int(self.bet_amount * 2.5)
            self.update_balance()
            self.reset_game()

        if len(self.player_hand) == 2:
            self.double_down_button.config(state=tk.NORMAL)
            if self.player_hand[0][0] == self.player_hand[1][0]:
                self.split_button.config(state=tk.NORMAL)

    def hit(self, hand=None):
        if hand is None:
            hand = self.active_hand
        
        if hand == 'player':
            self.player_hand.append(self.deal_card())
            card_label = tk.Label(self.player_frame, image=self.card_images[self.player_hand[-1][0] + "_of_" + self.player_hand[-1][1]])
            card_label.pack(side=tk.LEFT)
            self.card_labels.append(card_label)
            hand_value = self.calculate_hand_value(self.player_hand)
        else:  # split hand
            self.split_hand.append(self.deal_card())
            card_label = tk.Label(self.split_frame, image=self.card_images[self.split_hand[-1][0] + "_of_" + self.split_hand[-1][1]])
            card_label.pack(side=tk.LEFT)
            self.card_labels.append(card_label)
            hand_value = self.calculate_hand_value(self.split_hand)

        if hand_value > 21:
            messagebox.showinfo("Bust!", f"{'Player' if hand == 'player' else 'Split hand'} busted!")
            if hand == 'split':
                self.active_hand = 'player'
                self.hit_button.config(state=tk.NORMAL)
                self.stand_button.config(state=tk.NORMAL)
            elif not self.split_hand:
                self.reset_game()
            else:
                self.active_hand = 'split'
                self.hit_button.config(state=tk.NORMAL)
                self.stand_button.config(state=tk.NORMAL)

    def stand(self):
        if self.active_hand == 'player' and self.split_hand:
            self.active_hand = 'split'
            self.hit_button.config(state=tk.NORMAL)
            self.stand_button.config(state=tk.NORMAL)
        else:
            self.start_dealer_turn()

    def double_down(self):
        if self.active_hand == 'player':
            if self.bet_amount * 2 > self.balance:
                messagebox.showerror("Error", "Not enough balance to double down.")
                return
            self.balance -= self.bet_amount
            self.bet_amount *= 2
            self.update_balance()
            self.hit()
            if self.calculate_hand_value(self.player_hand) <= 21:
                if self.split_hand:
                    self.active_hand = 'split'
                    self.hit_button.config(state=tk.NORMAL)
                    self.stand_button.config(state=tk.NORMAL)
                else:
                    self.start_dealer_turn()

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
        split_value = self.calculate_hand_value(self.split_hand) if self.split_hand else 0

        if dealer_value > 21:
            messagebox.showinfo("Winner!", "Dealer busts! You win!")
            self.balance += self.bet_amount * 2
            if self.split_hand:
                self.balance += self.bet_amount * 2
        else:
            player_result = self.compare_hands(player_value, dealer_value)
            split_result = self.compare_hands(split_value, dealer_value) if self.split_hand else None

            message = f"Player hand: {player_result}\n"
            if split_result:
                message += f"Split hand: {split_result}"

            messagebox.showinfo("Game Result", message)

            if player_result == "Win":
                self.balance += self.bet_amount * 2
            elif player_result == "Push":
                self.balance += self.bet_amount

            if split_result == "Win":
                self.balance += self.bet_amount * 2
            elif split_result == "Push":
                self.balance += self.bet_amount

        self.update_balance()
        self.reset_game()

    def compare_hands(self, player_value, dealer_value):
        if player_value > 21:
            return "Bust"
        elif dealer_value > 21 or player_value > dealer_value:
            return "Win"
        elif player_value == dealer_value:
            return "Push"
        else:
            return "Lose"

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
        for widget in self.dealer_frame.winfo_children():
            widget.destroy()
        for widget in self.player_frame.winfo_children():
            widget.destroy()
        for widget in self.split_frame.winfo_children():
            widget.destroy()
        self.split_label.pack_forget()
        self.split_frame.pack_forget()

        # Display back card images after the round
        dealer_back = tk.Label(self.dealer_frame, image=self.card_images['back'])
        dealer_back.pack(side=tk.LEFT)
        player_back = tk.Label(self.player_frame, image=self.card_images['back'])
        player_back.pack(side=tk.LEFT)

        if self.balance < self.initial_balance * 0.1:
            response = messagebox.askyesno("Low Balance", "Your balance is very low. Do you want to reset your balance to the initial amount?")
            if response:
                self.balance = self.initial_balance
                self.update_balance()
            else:
                self.check_balance_threshold()

    def show_warning(self, threshold):
        percentage = int((1 - threshold) * 100)
        message = f"Warning: You have lost {percentage}% of your initial balance.\n"
        message += "You may be falling for the illusion of gambling and getting addicted slowly.\n\n"
        message += "Do you want to continue playing or stop?"

        response = messagebox.askyesno("Gambling Warning", message, icon='warning')

        if not response:
            self.show_help_resources()
        else:
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
        self.root.destroy()
        self.start_window.destroy()

if __name__ == "__main__":
    start_root = tk.Tk()
    start_window = StartWindow(start_root)
    start_root.mainloop()

