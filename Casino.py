import random
from enum import Enum
import sys
import time

# ----------- Blackjack deck opsætning ----------------
class Deck:
    def __init__(self):
        self.cards = []
        suits = ['spades', 'clubs', 'hearts', 'diamond']
        ranks = [
                {'rank': 'A', 'value': 11},
                {'rank': '2', 'value': 2},
                {'rank': '3', 'value': 3},
                {'rank': '4', 'value': 4},
                {'rank': '5', 'value': 5},
                {'rank': '6', 'value': 6},
                {'rank': '7', 'value': 7},
                {'rank': '8', 'value': 8},
                {'rank': '9', 'value': 9},
                {'rank': '10', 'value': 10},
                {'rank': 'J', 'value': 10},
                {'rank': 'Q', 'value': 10},
                {'rank': 'K', 'value': 10},
            ]

        for suit in suits:
            for rank in ranks:
                self.cards.append(Card(suit, rank))

    def shuffle(self):
        if len(self.cards) > 1:
            random.shuffle(self.cards)
            

    def deal(self, number):
        cards_dealt = []
        for x in range(number):
            if len(self.cards) > 0:
                card = self.cards.pop()
            cards_dealt.append(card)
        return cards_dealt


class Card:
    def __init__(self, suit, rank):
        self.suit = suit
        self.rank = rank
    def __repr__(self):
        return "{rank} of {suit}".format(rank=self.rank['rank'], suit=self.suit)



class Hand:
    def __init__(self, dealer=False):
        self.cards = []
        self.value = 0
        self.dealer = dealer

    def add_card(self, card_list):
        self.cards.extend(card_list)
    
    def calc_value(self):
        self.value = 0
        has_ace = False

        for card in self.cards:
            card_value = int(card.rank['value'])
            self.value += card_value
            if card.rank['rank'] == 'A':
                has_ace = True

        if has_ace and self.value > 21:
            self.value -= 10
    
    def get_value(self):
        self.calc_value()
        return self.value
    
    def is_blackjack(self):
        return self.get_value() == 21

    def display(self, show_all_dealer_cards = False):
        print(f'''{"Dealer's" if self.dealer else "Your"} hand''')
        for index, card in enumerate(self.cards):
                if index ==  0 and self.dealer and not show_all_dealer_cards \
                    and not self.is_blackjack():
                    print("hidden")
                else: 
                    print(card)
        if not self.dealer:
            print("Value:", self.get_value())
        print()    

# ------------- Blackjack spillet ----------------

class Blackjack:
    def __init__(self, player, allocated_funds):
        self.name = player
        self.allocated_funds = allocated_funds
        self.players_money = 0
        self.players_money += self.allocated_funds

    def __str__(self):
        return """\nHello {player}, And welcome to Blackjack! 
Here your goal is to reach a card total of 21, but do not go over - or you will lose! 
--- Good luck! ---""".format(player=self.name)

    def play(self):
        game_number = 0
        games_to_play = 0

        while games_to_play <= 0:
            try:
                games_to_play = int(input("How many games do you want to play? "))
            except ValueError: 
                print("You must enter a number")


        while game_number < games_to_play:
            game_number += 1
            self.wager = 0
            while self.wager <= 0:
                try:
                    updated_wager = int(input("How much would you like to wager on this game? You have {money} coins left: ".format(money=self.players_money)))
                    if type(updated_wager) == int and updated_wager > 0 and updated_wager < self.players_money:
                        self.wager = updated_wager
                    elif self.players_money > 0:
                        print("There is a minimum of 1 coin wage")
                        self.wager = 1
                    elif self.players_money == 0:
                        sys.exit('You have no more money, the game is over')
                except ValueError:
                    print("You must enter a number")                 
            print("You have wagered {wager}!".format(wager=self.wager))

            deck = Deck()
            deck.shuffle()

            player_hand = Hand()
            dealer_hand = Hand(dealer=True)
            
            for i in range(2):
                player_hand.add_card(deck.deal(1))
                dealer_hand.add_card(deck.deal(1))

            print("")
            print('*'*30)
            print(f"game number {game_number} out of {games_to_play}")
            print('*'*30)
            player_hand.display()
            dealer_hand.display()

            if self.check_winner(player_hand, dealer_hand):
                continue
            
            choice = ""
            while player_hand.get_value() < 21 and choice not in ["s", "stand"]:
                choice = input("Hit or stand? ").lower()
                print()
                while choice not in ["h", "s", "hit", "stand"]:
                    input("You can type 'h' or 's' too! ").lower()
                    print()
                if choice in ["hit", "h"]:
                    player_hand.add_card(deck.deal(1))
                    player_hand.display()
            
            if self.check_winner(player_hand, dealer_hand):
                continue

            player_hand_value = player_hand.get_value()
            dealer_hand_value = dealer_hand.get_value()

            while dealer_hand_value < 17:
                dealer_hand.add_card(deck.deal(1))
                dealer_hand_value = dealer_hand.get_value()
            
            dealer_hand.display(show_all_dealer_cards=True)
            if self.check_winner(player_hand, dealer_hand):
                continue

            print("Final results")
            print("Your hand:", player_hand_value)
            print("Dealer's hand:", dealer_hand_value)
            
            self.check_winner(player_hand, dealer_hand, True)
        print("\n Thanks for playing")
        Menu.after_game_menu(Menu, self.name, self.players_money)


    def check_winner(self, player_hand, dealer_hand, game_over=False):
        if not game_over:
            if player_hand.get_value() > 21:
                print("You busted! Dealer wins!")
                self.add_money(self.wager, "Dealer")
                print("You now have {money} coins left, you lost {wager}".format(money=self.players_money, wager=self.wager))
                return True
            elif dealer_hand.get_value() > 21:
                print("Dealer busted! You win!")
                self.add_money(self.wager*2, "Player")
                print("You won {wager} coins! You now have {money}".format(wager=self.wager*2, money=self.players_money))
                return True
            elif dealer_hand.get_value() and player_hand.get_value():
                print("No one busted!")
            elif player_hand.get_value() == 21:
                print("You have blackjack! You win!")
                self.add_money(self.wager*2, "Player")
                print("You won {wager} coins! You now have {money}".format(wager=self.wager*2, money=self.players_money))
                return True
            elif dealer_hand.get_value() == 21:
                print("Dealer has blackjack! You lose!")
                self.add_money(self.wager, "Dealer")
                print("You now have {money} left, you lost {wager}".format(money=self.players_money, wager=self.wager))
                return True

        else:
            if player_hand.get_value() > dealer_hand.get_value():
                print("You win!")
                self.add_money(self.wager*2, "Player")
                print("You won {wager} coins! You now have {money}".format(wager=self.wager*2, money=self.players_money))
            elif player_hand.get_value() < dealer_hand.get_value():
                print("You lose!")
                self.add_money(self.wager, "Dealer")
                print("You now have {money} left, you lost {wager}".format(money=self.players_money, wager=self.wager))
            if player_hand.get_value() == dealer_hand.get_value():
                print("It's a tie!")
            return True
        return False
    
    def add_money(self, amount, recipient):
        if recipient == "Player": self.players_money += amount
        else: self.players_money -= self.wager
        return True

# ----------- Roulette spil -------------
class Roulette():
    def __init__(self, player, allocated_funds):
        self.name = player
        self.allocated_funds = allocated_funds
        self.players_money = 0
        self.players_money += self.allocated_funds
    
    def __repr__(self):
        return """Welcome to Roulette! 
We hope you choose right!
 - Good luck! - """

    def roulette_number(self):
        roulette_number = random.randint(0,36)
        return roulette_number
    
    def play(self):
        game_number = 0
        games_to_play = 0

        while games_to_play <= 0:
            try:
                games_to_play = int(input("How many games do you want to play? "))
            except ValueError: 
                print("You must enter a number")

        while game_number < games_to_play:
            game_number += 1

            print("")
            print('*'*30)
            print(f"game number {game_number} out of {games_to_play}")
            print('*'*30)

            self.wager = 0
            while self.wager <= 0:
                try:
                    updated_wager = int(input("How much would you like to wager on this game? You have {money} money left allocated: ".format(money=self.players_money)))
                    if type(updated_wager) == int and updated_wager > 0 and updated_wager <= self.players_money:
                        self.wager = updated_wager
                    elif self.players_money > 0:
                        print("There is a minimum of 1$ wage")
                        self.wager = 1
                    elif self.players_money == 0:
                        sys.exit('You have no more money, the game is over')
                except ValueError:
                    print("You must enter a number")                 
            print("You have wagered {wager}!".format(wager=self.wager))

            player_choices = {1: "even (1 to 1)", 2: "odd (1 to 1)", 3: "low (1 to 1)", 4: "high (1 to 1)", 5: "1. dozen (2 to 1)", 6: "2. dozen (2 to 1)", 7: "3. dozen (2 to 1"}
            print("What kind of pick will you make?")
            for key, value in player_choices.items():
                print("{number}: {value}".format(number=key, value=value))

            player_pick = int(input("Type the number: ").lower())
            player_choice = player_choices.get(player_pick)
            print("You chose {choice}!".format(choice=player_choice))

            self.ball_roll()
            game_pick = self.roulette_number()

            if player_choice == "even (1 to 1)" and game_pick % 2 == 0 and game_pick != 36:
                print("You won!")
                self.add_money(self.wager*2, "Player")
            elif player_choice == "odd (1 to 1)" and game_pick % 2 == 1:
                print("You win!")
                self.add_money(self.wager*2, "Player")
            elif player_choice == "low (1 to 1)" and 1 <= game_pick <= 18:
                print("You win!")
                self.add_money(self.wager*2, "Player")
            elif player_choice == "high (1 to 1)" and 19 <= game_pick <= 36:
                print("You win!")
                self.add_money(self.wager*2, "Player")
            elif player_choice == "dozen 1 (2 to 1)" and 1 <= game_pick <= 12:
                 print("You win!")
                 self.add_money(self.wager*3, "Player")
            elif player_choice == "dozen 2 (2 to 1)" and 13 <= game_pick <= 24:
                 print("You win!")
                 self.add_money(self.wager*3, "Player")
            elif player_choice == "dozen 3 (2 to 1)" and 25 <= game_pick <= 36:
                 print("You win!")
                 self.add_money(self.wager*3, "Player")
            else:
                print("You chose {player}, but the roulette number was {roulette}. You lost".format(player=player_choice, roulette=game_pick))
                self.add_money(self.wager, "Dealer")
            
            print("You now have {money} left, you lost {wager}".format(money=self.players_money, wager=self.wager))        
        # end of game
        print("\nThanks for playing {name}!".format(name=self.name))
        Menu.after_game_menu(Menu, self.name, self.players_money)      

    def add_money(self, amount, recipient):
        if recipient == "Player": self.players_money += amount
        else: self.players_money += -self.wager
        return True
    
    def ball_roll(self):
        print("The ball is rolling!")

        print("Rolling.")
        time.sleep(1)
        print("Rolling..")
        time.sleep(1)
        print("Rolling...")
        time.sleep(1)

# --------- slot maskiner -----------
class Slots:
    def __init__(self, player, funds):
        self.player = player
        self.players_money = funds
    
    def __repr__(self):
        return "Welcome to the slot machines! Here you can try your pure luck. Is it your day today?"

    def pull_lever(self):
        first_number = random.randint(0, 9)
        second_number = random.randint(0, 9)
        third_number = random.randint(0, 9)

        time.sleep(1)
        print("numbers shuffling...")
        time.sleep(0.5)
        print(first_number)
        time.sleep(0.5)
        print("numbers shuffling...")
        time.sleep(0.5)
        print(second_number)
        time.sleep(0.5)
        print("numbers shuffling...")
        time.sleep(0.5)
        print(third_number)

        return first_number, second_number, third_number
    
    def add_money(self, amount, recipient):
        if recipient == "Player": self.players_money += amount
        else: self.players_money += -self.wager
        return True
    
    def play(self):
        game_number = 0
        games_to_play = 0

        winning_combinations = ["3 numbers of the same kind (2 to 1)", "2 numbers of the same kind (1 to 1)"]
        see_list = input("Do you want the list of winnning combinations? ").lower()
        if see_list == "yes": print(winning_combinations)

        while games_to_play <= 0:
            try:
                games_to_play = int(input("How many games do you want to play? "))
            except ValueError: 
                print("You must enter a number")

        while game_number < games_to_play:
            game_number += 1

            print("")
            print('*'*30)
            print(f"game number {game_number} out of {games_to_play}")
            print('*'*30)

            self.wager = 0
            while self.wager <= 0:
                try:
                    updated_wager = int(input("How much would you like to wager on this game? You have {money} money left allocated: ".format(money=self.players_money)))
                    if type(updated_wager) == int and updated_wager > 0 and updated_wager <= self.players_money:
                        self.wager = updated_wager
                    elif self.players_money > 0:
                        print("There is a minimum of 1$ wage")
                    elif self.players_money == 0:
                        sys.exit('You have no more money, the game is over')
                except ValueError:
                    print("You must enter a number")                 
            print("You have wagered {wager}!".format(wager=self.wager))

            input("\nPull the lever? ")
            print("Pulling lever")
            first_number, second_number, third_number = self.pull_lever()

            # Check winnings
            if first_number == second_number and second_number == third_number:
                print("You win big")
                self.add_money(self.wager*3, "Player")
            elif first_number == second_number or second_number == third_number or first_number == third_number:
                print("You win less big")
                self.add_money(self.wager*2, "Player")
            else: print("You lose :("), self.add_money(self.wager, "Dealer")

            time.sleep(0.5)
        print("\nThanks for playing slots!")
        Menu.after_game_menu(Menu, self.player, self.players_money)

# ------------ menu -------------
class Menu:
    def start_menu(self):
        print("Hello, and welcome to the High 10 Casino! We have an amazing assortment of games to play, all with the possibility of winning Big!")
        player = input("What is your name? ")
        funds = int(input("How much would you wish to cash in? "))

        choose_game = Menu()
        choose_game.games_to_play(player, funds)

    def games_to_play(self, player, funds):
        self.player = player
        self.funds = funds
        print("\nHello {name}!\nWhat do you wish to play, here at the high 10 casino we have the following options:".format(name=player))
        games_to_play = {1: "Blackjack", 2: "Roulette", 3: "Slot machine"}
        for key, value in games_to_play.items():
            print("{key}: {value}".format(key=key, value=value))
        
        game_to_play = 0
        while game_to_play < 1:
            game_to_play = int(input())

        if game_to_play == 1:
            game_one = Blackjack(player, funds)
        elif game_to_play == 2:
            game_one = Roulette(player, funds)
        else: game_one = Slots(player, funds)
        
        print(game_one)
        game_one.play()

    def after_game_menu(self, player, funds):
        self.player = player
        self.funds = funds

        if self.funds > 0:
            new_choice = ""
            while "play again" not in new_choice and "cash out" not in new_choice:
                new_choice = input("{player} do you wish to play again, or do you wish to cash out? ".format(player=self.player)).lower()
            
            if new_choice in "play again?":
                find_new_game = Menu()
                find_new_game.games_to_play(self.player, self.funds)
            else: print("Your balance is {coins}, we hope to see you again!".format(coins=self.funds))
        else: print("Your funds are low, and you are being thrown out because you're too drunk\n Goodbye!")

game = Menu()
game.start_menu()