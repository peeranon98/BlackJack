import random

suits = ('Hearts', 'Diamonds', 'Spades', 'Clubs')
ranks = ('Two', 'Three', 'Four', 'Five', 'Six', 'Seven', 'Eight', 'Nine', 'Ten', 'Jack', 'Queen', 'King', 'Ace')
values = {'Two':2, 'Three':3, 'Four':4, 'Five':5, 'Six':6, 'Seven':7, 'Eight':8, 'Nine':9, 'Ten':10, 'Jack':10,
         'Queen':10, 'King':10, 'Ace':11}

playing = True

class Card:
    
    def __init__(self,suit,rank):
        self.suit=suit
        self.rank=rank
        self.value=values[rank]
    
    def __str__(self):
        return f"{self.rank} of {self.suit}"

class Deck:
    
    def __init__(self):
        self.deck = []  # start with an empty list
        for suit in suits:
            for rank in ranks:
                self.deck.append(Card(suit,rank))
    
    def __str__(self):
        indeck=''
        for card in self.deck:
            indeck+=card.__str__()+", "
        return "The cards in deck: "+indeck

    def shuffle(self):
        random.shuffle(self.deck)
        
    def deal(self):
        return self.deck.pop()

class Hand:
    def __init__(self):
        self.cards = []  # start with an empty list as we did in the Deck class
        self.value = 0   # start with zero value
        self.aces = 0    # add an attribute to keep track of aces
    
    def add_card(self,card):
        self.cards.append(card)
        self.value+=card.value
        if(card.rank=='Ace'):
            self.aces+=1
    
    def adjust_for_ace(self):
        if self.value>21 and self.aces>=1:
            self.value-=10
            self.aces-=1

class Chips:
    
    def __init__(self,bet):
        self.total = 100  # This can be set to a default value or supplied by a user input
        self.bet = bet
        
    def win_bet(self):
        self.total+=self.bet
    
    def lose_bet(self):
        self.total-=self.bet

def take_bet(chips):
    while True:
        try:
            bet=int(input("Place your bet: "))
        except :
            print("Error please try again")
        else :
            if(bet<=chips.total):
                print(f"Okay, your bet is {bet}")
                chips.bet=bet
                break
            else:
                print("Error please try again")
                continue

def hit(deck,hand):
    hand.add_card(deck.deal())
    hand.adjust_for_ace()

def hit_or_stand(deck,hand):
    global playing  # to control an upcoming while loop
    try:
        ans = input("1 for hit , 2 for stand : ")
    except:
        print("Error, Try again")
    else : 
        if ans == "1":
            print("Player hit")
            hit(deck,hand)
        elif ans == "2":
            print("Player stand")
            playing = False
        else :
            hit_or_stand(deck,hand)

def show_some(player,dealer):   
    pc=""
    dc="??? / "
    for card in player.cards:
        pc+=card.__str__()+" / "
    for i in range(1,len(dealer.cards)):
        dc+=dealer.cards[i].__str__()+" / "
    print(f"Player card: {pc} value: {player.value}")
    print(f"Dealer card: {dc} value: {dealer.value-dealer.cards[0].value}")
    
def show_all(player,dealer):
    pc=""
    dc=""
    for card in player.cards:
        pc+=card.__str__()+" / "
    for card in dealer.cards:
        dc+=card.__str__()+" / "
    print(f"Player card: {pc} value: {player.value}")
    print(f"Dealer card: {dc} value: {dealer.value}")

def player_busts(player):
    if player.value>21:
        return True
    else:
        return False

def player_wins(chips):
    print("Player wins")
    chips.win_bet()

def dealer_busts(dealer):
    if dealer.value>21:
        return True
    else:
        return False
    
def dealer_wins(chips):
    print("Dealer wins")
    chips.lose_bet()
    
def push():
    print("It's a push")
    
chips=Chips(0)
while True:
    # Print an opening statement
    print("Welcome to Casiyes Black Jack")
    
    # Create & shuffle the deck, deal two cards to each player
    deck=Deck()
    deck.shuffle()
    player=Hand()
    dealer=Hand()
    playing = True
    for i in range (2):
        player.add_card(deck.deal())
        dealer.add_card(deck.deal())
    # Set up the Player's chips
    print(f"Your current chips are : {chips.total}")
    take_bet(chips)
    # Show cards (but keep one dealer card hidden)
    print("Cards dealing complete")
    show_some(player,dealer)
    print("\n")
    while playing:  # recall this variable from our hit_or_stand function
        
        # Prompt for Player to Hit or Stand
        hit_or_stand(deck,player)
        
        # Show cards (but keep one dealer card hidden)
        show_some(player,dealer)
        print("\n")
        # If player's hand exceeds 21, run player_busts() and break out of loop
        if player_busts(player):
            print("Player busted")
            break
    # Show all cards
    print("Show all card")
    show_all(player,dealer)
    print("\n")
    # If Player hasn't busted, play Dealer's hand until Dealer reaches 17
    if not player_busts(player):
        while dealer.value<17:
            print("Dealer is dealing")
            hit(deck,dealer)
            show_all(player,dealer)
            print("\n")
    print("Dealer stop dealing")
        # Run different winning scenarios
    if player_busts(player) and dealer_busts(dealer):
        push()
    elif (not player_busts(player) and (player.value>dealer.value)) or dealer_busts(dealer):
        player_wins(chips)
    elif (not dealer_busts(dealer) and (player.value<dealer.value)) or player_busts(player):
        dealer_wins(chips)
    else:
        push()
    # Inform Player of their chips total 
    print(f"Player's total chips : {chips.total}")
    # Ask to play again
    if chips.total>0:
        print("Do you want to play again?")
        ask = True
        while ask == True :
            again=input("Yes/No : ")
            if again.lower() == "yes" or again.lower() == "no" :
                ask = False
            else :
                print("Try again")
        if again.lower() == "yes" :
            print("\n\n\n")
            continue
        else :
            print("Thanks for playing with us")
            print(f"You start with 100 and get out with {chips.total}!")
            break
    else :
        print("Sorry, you are broke.\nGet some money then see you again!")
        break
            
