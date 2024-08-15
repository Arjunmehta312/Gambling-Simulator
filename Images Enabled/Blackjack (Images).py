#!/usr/bin/env python
# coding: utf-8

# # Blackjack

# Disclaimer:
# This Python Blackjack Game is purely for entertainment purposes and does not involve real money or actual gambling. No financial transactions are associated with this game. The outcome of each hand is determined by random chance, and while there is some element of strategy involved in deciding when to hit or stand, there is no guarantee of winning. Please play responsibly and within your means. If you experience any negative emotions related to gambling, consider seeking professional help.

# In[27]:


import tkinter as tk
from tkinter import messagebox
from PIL import Image, ImageTk
import random
import os

class BlackjackGame:
    def __init__(self, root):
        self.root=root
        self.root.title("Blackjack Game")
        
        self.balance=1000
        self.player_hand=[]
        self.dealer_hand=[]
        
        # Set the absolute path to your card images
        self.card_image_dir=r'C:\Users\arjun\cards'  # Ensure this is the correct path

        # Load card images
        self.card_images=self.load_card_images()

        # Create and shuffle the deck
        self.deck=self.create_deck()
        self.shuffle_deck()

        # Set up the GUI
        self.create_widgets()

    def load_card_images(self):
        images={}
        suits=['hearts','diamonds','clubs','spades']
        ranks=['2','3','4','5','6','7','8','9','10','jack','queen','king','ace']

        for suit in suits:
            for rank in ranks:
                image_path=os.path.join(self.card_image_dir,f'{rank}_of_{suit}.png')  # Use absolute path
                img=Image.open(image_path)
                img=img.resize((100, 150),Image.LANCZOS)  # Resize the card images for consistent display
                images[f"{rank}_of_{suit}"]=ImageTk.PhotoImage(img)

        # Load the back of the card image
        back_image_path=os.path.join(self.card_image_dir,'back.png')  # Back of the card image
        img=Image.open(back_image_path)
        img=img.resize((100,150),Image.LANCZOS)
        images['back']=ImageTk.PhotoImage(img)

        return images

    def create_widgets(self):
        # Balance Label
        self.balance_label=tk.Label(self.root,text=f"Balance: ₹{self.balance}")
        self.balance_label.pack()

        # Bet Input
        self.bet_label=tk.Label(self.root,text="Enter your bet amount:")
        self.bet_label.pack()

        self.bet_entry=tk.Entry(self.root)
        self.bet_entry.pack()

        # Bet Button
        self.bet_button=tk.Button(self.root,text="Place Bet",command=self.place_bet)
        self.bet_button.pack()

        # Dealer Hand
        self.dealer_label=tk.Label(self.root,text="Dealer's Hand:")
        self.dealer_label.pack()

        self.dealer_frame=tk.Frame(self.root)
        self.dealer_frame.pack()

        # Player Hand
        self.player_label=tk.Label(self.root,text="Player's Hand:")
        self.player_label.pack()

        self.player_frame=tk.Frame(self.root)
        self.player_frame.pack()

        # Action Buttons
        self.hit_button=tk.Button(self.root,text="Hit",command=self.hit,state=tk.DISABLED)
        self.hit_button.pack(side=tk.LEFT)

        self.stand_button=tk.Button(self.root,text="Stand",command=self.stand,state=tk.DISABLED)
        self.stand_button.pack(side=tk.LEFT)

    def create_deck(self):
        suits = ['hearts','diamonds','clubs','spades']
        ranks = ['2','3','4','5','6','7','8','9','10','jack','queen','king','ace']
        deck=[(rank,suit) for suit in suits for rank in ranks]
        return deck

    def shuffle_deck(self):
        random.shuffle(self.deck)

    def deal_card(self):
        # Check if deck is running low, shuffle new deck
        if len(self.deck)<15:
            self.deck=self.create_deck()
            self.shuffle_deck()

        return self.deck.pop()

    def calculate_hand_value(self,hand):
        value=0
        aces=0
        for card in hand:
            rank=card[0]
            if rank in ['jack','queen','king']:
                value+=10
            elif rank=='ace':
                value+=11
                aces+=1
            else:
                value+=int(rank)

        while value>21 and aces>0:
            value-=10
            aces-=1
        
        return value

    def place_bet(self):
        try:
            self.bet_amount=int(self.bet_entry.get())
            if self.bet_amount>self.balance or self.bet_amount<=0:
                raise ValueError("Invalid bet amount")
        except ValueError:
            messagebox.showerror("Error", "Please enter a valid bet amount")
            return

        self.balance-=self.bet_amount
        self.update_balance()

        # Start the round
        self.start_round()

    def update_balance(self):
        self.balance_label.config(text=f"Balance: ₹{self.balance}")

    def start_round(self):
        # Clear the previous hands
        for widget in self.dealer_frame.winfo_children():
            widget.destroy()
        for widget in self.player_frame.winfo_children():
            widget.destroy()

        # Deal initial cards
        self.player_hand=[self.deal_card(), self.deal_card()]
        self.dealer_hand=[self.deal_card(), self.deal_card()]

        # Display the dealer's first card and a hidden card
        dealer_card_label=tk.Label(self.dealer_frame,image=self.card_images[self.dealer_hand[0][0]+"_of_"+self.dealer_hand[0][1]])
        dealer_card_label.pack(side=tk.LEFT)
        dealer_hidden_label=tk.Label(self.dealer_frame,image=self.card_images['back'])
        dealer_hidden_label.pack(side=tk.LEFT)

        # Display the player's cards
        for card in self.player_hand:
            card_label=tk.Label(self.player_frame,image=self.card_images[card[0]+"_of_"+card[1]])
            card_label.pack(side=tk.LEFT)

        # Enable the hit and stand buttons
        self.hit_button.config(state=tk.NORMAL)
        self.stand_button.config(state=tk.NORMAL)

        # Check for Blackjack
        if self.calculate_hand_value(self.player_hand)==21:
            messagebox.showinfo("Blackjack!", "Blackjack! You win!")
            self.balance+=self.bet_amount*2.5
            self.update_balance()
            self.reset_game()

    def hit(self):
        # Add a card to the player's hand
        new_card=self.deal_card()
        self.player_hand.append(new_card)

        # Display the new card
        card_label=tk.Label(self.player_frame,image=self.card_images[new_card[0]+"_of_"+new_card[1]])
        card_label.pack(side=tk.LEFT)

        # Check if player busts
        if self.calculate_hand_value(self.player_hand)>21:
            messagebox.showinfo("Bust!", "You busted! Dealer wins.")
            self.reset_game()

    def stand(self):
        # Reveal the dealer's hidden card
        for widget in self.dealer_frame.winfo_children():
            widget.destroy()

        for card in self.dealer_hand:
            card_label=tk.Label(self.dealer_frame,image=self.card_images[card[0]+"_of_"+card[1]])
            card_label.pack(side=tk.LEFT)

        # Dealer hits until they reach 17 or more
        while self.calculate_hand_value(self.dealer_hand)<17:
            new_card=self.deal_card()
            self.dealer_hand.append(new_card)
            card_label=tk.Label(self.dealer_frame,image=self.card_images[new_card[0]+"_of_"+new_card[1]])
            card_label.pack(side=tk.LEFT)

        # Determine winner
        player_value=self.calculate_hand_value(self.player_hand)
        dealer_value=self.calculate_hand_value(self.dealer_hand)

        if dealer_value>21 or player_value>dealer_value:
            messagebox.showinfo("You win!", "Congratulations, you win!")
            self.balance+=self.bet_amount*2
        elif player_value==dealer_value:
            messagebox.showinfo("Push", "It's a push! You get your wagered back.")
            self.balance+=self.bet_amount
        else:
            messagebox.showinfo("Dealer wins", "Dealer wins.")

        self.update_balance()
        self.reset_game()

    def reset_game(self):
        # Reset for a new round
        self.hit_button.config(state=tk.DISABLED)
        self.stand_button.config(state=tk.DISABLED)
        self.bet_entry.delete(0, tk.END)

        # Clear hands
        self.player_hand=[]
        self.dealer_hand=[]

# Main application loop
if __name__=="__main__":
    root=tk.Tk()
    game=BlackjackGame(root)
    root.mainloop()


# In[ ]:




