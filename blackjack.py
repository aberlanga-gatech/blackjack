import random

SUITS = ('Hearts', 'Diamonds', 'Spades', 'Clubs')
RANKS = ('Two', 'Three', 'Four', 'Five', 'Six', 'Seven', 'Eight', 'Nine', 'Ten', 'Jack', 'Queen', 'King', 'Ace')
VALUES = {'Two':2, 'Three':3, 'Four':4, 'Five':5, 'Six':6, 'Seven':7, 'Eight':8, 'Nine':9, 'Ten':10, 'Jack':10, 'Queen':10, 'King':10, 'Ace':11}
BUY_IN = 100

playing = True

# card class
class Card:
    
    def __init__(self, suit, rank):
        self.suit = suit
        self.rank = rank
        self.imgpath = "cardimgs/" + self.rank.lower() + "_" + self.suit.lower() + ".png"

    def __str__(self):
        return self.rank + " of " + self.suit


# deck class
class Deck:

    def __init__(self):
        self.deck = []
        for suit in SUITS:
            for rank in RANKS:
                self.deck.append(Card(suit, rank))

    def __str__(self):
        deck_comp = ""
        for card in self.deck:
            deck_comp += "\n" + card.__str__()
        return "The deck has: " + deck_comp
    
    def shuffle(self):
        random.shuffle(self.deck)
    
    def deal(self):
        single_card = self.deck.pop()
        return single_card


# shoe class - inherits from deck (a large deck made up of n decks)
class Shoe(Deck):

    def __init__(self, num_decks):
        self.deck = []
        for i in range(num_decks):
            for suit in SUITS:
                for rank in RANKS:
                    self.deck.append(Card(suit, rank))

# hand class
class Hand:

    def __init__(self):
        self.cards = []
        self.value = 0
        self.aces = 0
    
    def add_card(self, card):
        self.cards.append(card)
        self.value += VALUES[card.rank]
        if card.rank == 'Ace':
            self.aces += 1


# chips class -- a chips object is given to each player
class Chips:
    
        def __init__(self):
            self.total = BUY_IN
            self.bet = 0
    
        def win_bet(self):
            self.total += self.bet
    
        def lose_bet(self):
            self.total -= self.bet

# player class
class Player: 
    
    def __init__(self):
        self.hand = Hand()
        self.chips = Chips()
    
    def hit(self, deck):
        self.hand.add_card(deck.deal())
        self.hand.adjust_for_ace()
    
    def stay(self):
        pass
    
    def bet(self):
        if self.chips.total > 0:
            self.chips.bet = int(input("How many chips would you like to bet? "))
            if self.chips.bet > self.chips.total:
                print("Sorry, you do not have enough chips. You have {}.".format(self.chips.total))
                self.chips.bet = 0
                self.bet()
            elif self.chips.bet == 0:
                print("Sorry, you must bet at least 1 chip.")
                self.bet()
        else:
            print("Sorry, you do not have any chips. You are broke.")
            self.chips.bet = 0
            playing = False

    def adjust_for_ace(self):
        while self.hand.value > 21 and self.hand.aces:
            self.hand.value -= 10
            self.hand.aces -= 1
    
    def win_bet(self):
        self.chips.win_bet()
        print("You win {} chips!".format(self.chips.bet))
        print("Player has {} chips.".format(self.chips.total))
    
    def lose_bet(self):
        self.chips.lose_bet()
        print("You lose {} chips!".format(self.chips.bet))
        print("Player has {} chips.".format(self.chips.total))

    def check_for_blackjack(self):
        if self.hand.value == 21:
            print("Blackjack!")
            self.chips.bet *= 1.5
            self.chips.win_bet()
            return True
        else:
            return False
    
    def __str__(self):
        return "Player has {} chips. (+ {} bet).".format(self.chips.total - self.chips.bet, self.chips.bet)


# dealer class -- inherits from player
class Dealer(Player):
        
    def __init__(self):
        self.hand = Hand()
        self.chips = 0

    def hit(self, deck):
        while self.hand.value < 17:
            print("Dealer hits.")
            super().hit(deck)
            print(player.hand.cards[-1])
            print("Value of: " + str(player.hand.value))

    def stay(self):
        pass

    # overriden adjust for ace to allow soft 17
    def adjust_for_ace(self):
        while self.hand.value > 17 and self.hand.aces:
            self.hand.value -= 10
            self.hand.aces -= 1

    # deprecated methods that dealer's dont need
    def bet(self):
        pass

    def win_bet(self):
        pass

    def lose_bet(self):
        pass

    def __str__(self):
        pass


# initialize the 4-deck shoe
shoe = Shoe(4)

# initialize discard pile
discard_pile = Deck()
discard_pile.deck = []

# initialize the player
player = Player()

# initialize the dealer
dealer = Dealer()


while playing:

    # set hands to empty
    dealer.hand = Hand()
    player.hand = Hand()

    if player.chips.total == 0:
        print("You are out of chips. You are broke.")
        playing = False
        break

    player.bet()

    # deal cards to player and dealer
    player.hand.add_card(shoe.deal())
    dealer.hand.add_card(shoe.deal())
    player.hand.add_card(shoe.deal())
    dealer.hand.add_card(shoe.deal())

    # print player bank statement
    print(player)

    # dealer cards
    print("\nDealer has: ")
    print(dealer.hand.cards[1])
    print("(Hidden)")
    print("Open value of: " + str(VALUES[dealer.hand.cards[1].rank]))
    
    # check dealer blackjack
    if VALUES[dealer.hand.cards[1].rank] >= 10:
        print("Checking for blackjack...")
        if dealer.hand.value == 21:
            print("Dealer has blackjack!")
            print(dealer.hand.cards[1])
            print(dealer.hand.cards[0])
            player.lose_bet()
            print(player)
            continue
        else:
            print("Dealer does not have blackjack.")

    # player cards
    print("\nPlayer has: ")
    print(player.hand.cards[0])
    print(player.hand.cards[1])
    print("Value of: " + str(player.hand.value))

    # check for blackjack
    if player.check_for_blackjack():
        playing = input("Would you like to play again? (y/n) ").lower() == 'y' if True else False
        continue

    # player turn
    while player.hand.value < 21:
        hit_or_stay = input("\nWould you like to hit or stay? ")
        if hit_or_stay[0].lower() == 'h':
            player.hit(shoe)
            print(player.hand.cards[-1])
            print("Value of: " + str(player.hand.value))
            if player.hand.value > 21:
                print("You have busted!")
                player.lose_bet()
                print(player)
                break
        else:
            break

    # dealer turn
    dealer.hit(shoe)

    # check who wins
    if dealer.hand.value > 21:
        print("Dealer has busted!")
        player.win_bet()
    elif dealer.hand.value > player.hand.value:
        print("Dealer wins!")
        player.lose_bet()
    elif dealer.hand.value < player.hand.value:
        print("Player wins!")
        player.win_bet()

    # check game state
    playing = input("Would you like to play again? (y/n) ").lower() == 'y' if True else False

print("Game over.\n")
print("Player has {} chips.".format(player.chips.total))

