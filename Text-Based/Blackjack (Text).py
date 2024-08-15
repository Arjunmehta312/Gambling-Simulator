#!/usr/bin/env python
# coding: utf-8

# # Blackjack

# Disclaimer:
# This Python Blackjack Game is purely for entertainment purposes and does not involve real money or actual gambling. No financial transactions are associated with this game. The outcome of each hand is determined by random chance, and while there is some element of strategy involved in deciding when to hit or stand, there is no guarantee of winning. Please play responsibly and within your means. If you experience any negative emotions related to gambling, consider seeking professional help.

# In[6]:


# Import libraries

import tkinter as tk
from tkinter import messagebox
import random

# tkinter: This is the standard Python interface to the Tk GUI toolkit. tkinter is used to create graphical user interfaces.
# messagebox: This module in tkinter provides a simple way to create message boxes (e.g., for showing error or information messages).
# random: This module provides functions to generate random numbers and to make random choices. It will be used to deal cards randomly from the deck.


# In[7]:


# Starting balance
balance=1000

# LIST: Storing a deck of cards in a list
deck=["2","3","4","5","6","7","8","9","10","J","Q","K","A"]*4

# DICTIONARY: Key value pair for value of each card
card_values={
    "2":2,"3":3,"4":4,"5":5,"6":6,"7":7,"8":8,"9":9,
    "10":10,"J":10,"Q":10,"K":10,"A":11
}

# balance: This variable holds the starting balance for the player, initially set to 1000.
# deck: This list represents a standard deck of 52 cards with 4 suits, where each card appears 4 times. Cards are represented as strings.
# card_values: This dictionary maps each card to its corresponding value in the game of Blackjack. Note that face cards (J, Q, K) are worth 10, and an Ace (A) can be worth 11


# In[8]:


#FUNCTION: Select a random card
def deal_card():
    card=random.choice(deck)
    deck.remove(card)
    return card

#FUNCTION: To calculate hand value
def calculate_hand_value(hand):
    value=0
    ace_count=0
    for card in hand:
        value+=card_values[card]
        if card=="A":
            ace_count+=1
    while value>21 and ace_count:
        value-=10
        ace_count-=1
    return value

# deal_card(): This function selects a random card from the deck, removes it from the deck, and returns it. This simulates dealing a card from the deck.
# calculate_hand_value(hand): This function calculates the total value of a hand of cards:
# It initializes the value to 0 and ace_count to 0.
# It iterates over the cards in the hand, adding their values to value. If a card is an Ace, it increments ace_count.
# If the total value exceeds 21 and there are Aces in the hand, it reduces the total value by 10 for each Ace until the value is 21 or less, or there are no more Aces to adjust.


# In[9]:


# Class: To define the app

class BlackjackApp:

    # FUNCTION: Create main application window
    def __init__(self,root):
        self.root=root
        self.root.title("Blackjack Game")
        
        self.balance=balance
        
        self.create_widgets()

    # FUNCTION: Graphic labels,buttons and entry fields
    def create_widgets(self):
        self.balance_label=tk.Label(self.root,text=f"Balance: ₹{self.balance}")
        self.balance_label.pack()
        
        self.bet_label=tk.Label(self.root,text="Enter your bet amount:")
        self.bet_label.pack()
        
        self.bet_entry=tk.Entry(self.root)
        self.bet_entry.pack()
        
        self.bet_button=tk.Button(self.root,text="Place Bet",command=self.place_bet)
        self.bet_button.pack()
        
        self.dealer_label=tk.Label(self.root,text="Dealer's Hand:")
        self.dealer_label.pack()
        
        self.dealer_hand_label=tk.Label(self.root,text="")
        self.dealer_hand_label.pack()
        
        self.player_label=tk.Label(self.root,text="Your Hand:")
        self.player_label.pack()
        
        self.player_hand_label=tk.Label(self.root,text="")
        self.player_hand_label.pack()
        
        self.action_frame=tk.Frame(self.root)
        self.action_frame.pack()
        
        self.hit_button=tk.Button(self.action_frame,text="Hit",command=self.hit,state=tk.DISABLED)
        self.hit_button.pack(side=tk.LEFT)
        
        self.stand_button=tk.Button(self.action_frame,text="Stand",command=self.stand,state=tk.DISABLED)
        self.stand_button.pack(side=tk.LEFT)
        
        self.double_button=tk.Button(self.action_frame,text="Double Down",command=self.double_down,state=tk.DISABLED)
        self.double_button.pack(side=tk.LEFT)
        
        self.split_button=tk.Button(self.action_frame,text="Split",command=self.split,state=tk.DISABLED)
        self.split_button.pack(side=tk.LEFT)

    # FUNCTION: To update balance label
    def update_balance(self):
        self.balance_label.config(text=f"Balance: ₹{self.balance}")

    #FUNCTION: Verifies bet made by the player and starts a round
    def place_bet(self):
        try:
            self.bet_amount=int(self.bet_entry.get())
            if self.bet_amount>self.balance:
                messagebox.showerror("Error","Insufficient funds! Place a smaller bet.")
                return
            self.start_round()
        except ValueError:
            messagebox.showerror("Error","Please enter a valid bet amount.")

    # FUNCTION: To start a round by dealing hand to dealer and player
    def start_round(self):
        if len(deck)<15:
            self.shuffle_deck()
        
        self.player_hand=[deal_card(),deal_card()]
        self.dealer_hand=[deal_card(),deal_card()]
        
        self.dealer_hand_label.config(text=f"[{self.dealer_hand[0]},?]")
        self.player_hand_label.config(text=f"{self.player_hand}, Total: {calculate_hand_value(self.player_hand)}")
        
        if calculate_hand_value(self.player_hand)==21:
            messagebox.showinfo("Blackjack!","Blackjack! You win!")
            self.balance+=self.bet_amount*1.5
            self.update_balance()
            self.reset_bet()
            return
        
        self.enable_actions()
    
    # FUNCTION: Activates buttons
    def enable_actions(self):
        self.hit_button.config(state=tk.NORMAL)
        self.stand_button.config(state=tk.NORMAL)
        self.double_button.config(state=tk.NORMAL)
        self.split_button.config(state=tk.NORMAL if self.player_hand[0]==self.player_hand[1] else tk.DISABLED)
    
    # FUNCTION: Disables buttons
    def disable_actions(self):
        self.hit_button.config(state=tk.DISABLED)
        self.stand_button.config(state=tk.DISABLED)
        self.double_button.config(state=tk.DISABLED)
        self.split_button.config(state=tk.DISABLED)

    # FUNCTIONs: To hit,stand,double down and split
    def hit(self):
        self.player_hand.append(deal_card())
        self.player_hand_label.config(text=f"{self.player_hand}, Total: {calculate_hand_value(self.player_hand)}")
        
        if calculate_hand_value(self.player_hand)>=21:
            self.end_round()
    # 
    def stand(self):
        self.end_round()
    
    def double_down(self):
        if self.balance>=self.bet_amount:
            self.balance-=self.bet_amount
            self.bet_amount*=2
            self.player_hand.append(deal_card())
            self.player_hand_label.config(text=f"{self.player_hand}, Total: {calculate_hand_value(self.player_hand)}")
            
            if calculate_hand_value(self.player_hand)>21:
                messagebox.showinfo("Bust","You busted! You lose.")
                self.balance-=self.bet_amount
                self.update_balance()
                self.reset_bet()
                return
            
            self.end_round()
        else:
            messagebox.showerror("Error","Insufficient funds to double down!")
    
    def split(self):
        if self.balance>=self.bet_amount*2:
            self.balance-=self.bet_amount
            self.hand1=[self.player_hand[0],deal_card()]
            self.hand2=[self.player_hand[1],deal_card()]
            
            self.player_hand_label.config(text=f"First Hand: {self.hand1}")
            self.play_hand(self.hand1)
            
            self.player_hand_label.config(text=f"Second Hand: {self.hand2}")
            self.play_hand(self.hand2)
        else:
            messagebox.showerror("Error","Insufficient funds to split!")

    # FUNCTION: To play one of the split hands
    def play_hand(self,hand):
        self.player_hand=hand
        self.player_hand_label.config(text=f"{self.player_hand}, Total: {calculate_hand_value(self.player_hand)}")
        
        if calculate_hand_value(self.player_hand)==21:
            messagebox.showinfo("Blackjack!","Blackjack! You win!")
            self.balance+=self.bet_amount*1.5
            self.update_balance()
            return
        
        self.enable_actions()

    # FUNCTION: To end round
    def end_round(self):
        self.disable_actions()
        
        player_total=calculate_hand_value(self.player_hand)
        dealer_total=calculate_hand_value(self.dealer_hand)
        
        if player_total>21:
            messagebox.showinfo("Bust","You busted! You lose.")
            self.balance-=self.bet_amount
        else:
            while dealer_total<17:
                self.dealer_hand.append(deal_card())
                dealer_total=calculate_hand_value(self.dealer_hand)
            
            self.dealer_hand_label.config(text=f"{self.dealer_hand}, Total: {dealer_total}")
            
            if dealer_total>21 or dealer_total<player_total:
                messagebox.showinfo("Result","You win!")
                self.balance+=self.bet_amount
            elif dealer_total==player_total:
                messagebox.showinfo("Result","It's a tie.")
            else:
                messagebox.showinfo("Result","Dealer wins! You lose.")
                self.balance-=self.bet_amount
        
        self.update_balance()
        self.reset_bet()

    # FUNCTION: Reset the bet
    def reset_bet(self):
        self.bet_entry.delete(0,tk.END)
    
    # FUNCTION: Shuffle when cards are low
    def shuffle_deck(self):
        global deck
        deck=["2","3","4","5","6","7","8","9","10","J","Q","K","A"]*4


# In[10]:


# Main Loop
if __name__=="__main__":
    root=tk.Tk()
    app=BlackjackApp(root)
    root.mainloop()

