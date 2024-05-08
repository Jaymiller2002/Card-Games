import random

class Card: 
    def __init__(self, suit, rank):
        self.suit = suit
        self.rank = rank


class Deck:
    def __init__(self, num_decks=1):
        suits = ['Hearts', 'Diamonds', 'Clubs', 'Spades']
        ranks = ['2', '3', '4', '5', '6', '7', '8', '9', '10', 'Jack', 'Queen', 'King', 'Ace']
        self.cards = [Card(suit, rank) for _ in range(num_decks) for suit in suits for rank in ranks]
        self.shuffle()

    def shuffle(self):
        random.shuffle(self.cards)

    def deal_card(self):
        return self.cards.pop()

class Player:
    def __init__(self, name, initial_balance=100):
        self.name = name
        self.balance = initial_balance
        self.hand = []

    def place_bet(self, amount):
        if amount <= self.balance:
            self.balance -= amount
            return True
        else:
            print("Insufficient balance!")
            return False

    def win(self, amount):
        self.balance += amount

    def show_hand(self):
        for card in self.hand:
            print(f"{card.rank} of {card.suit}")

    
def compare_cards(card1, card2):
    if card1.rank == 'Ace' and card2.rank != 'Ace':
        return 1
    elif card1.rank != 'Ace' and card2.rank == 'Ace':
        return -1
    elif card1.rank == card2.rank:
        return 0
    else:
        return 1 if card1.rank > card2.rank else -1

def play_high_card(player_name, num_decks=1):
    print("Playing High Card game...")
    player = Player(player_name)
    deck = Deck(num_decks)
    while True:
        player.hand = [deck.deal_card()]
        dealer_hand = [deck.deal_card()]
        print(f"Your card: {player.hand[0].rank} of {player.hand[0].suit}")
        result = compare_cards(player.hand[0], dealer_hand[0])
        if result == 1:
            print("Congratulations! You win!")
            player.win(2)
        elif result == -1:
            print("Sorry, You lose")
        else:
            print("It's a tie")
        print(f"Your current balance: ${player.balance}")
        play_again = input("Do you want to play again? (Yes/No):")
        if play_again.lower() != 'yes':
            break

def play_blackjack(player_name, num_decks=1):
    print("Playing Blackjack game...")
    player = Player(player_name)
    deck = Deck(num_decks)
    
    while True:
        # Reset hands and deck
        player.hand = []
        dealer_hand = []
        deck = Deck(num_decks)

        # Place bet
        bet_amount = int(input(f"{player_name}, place your bet (current balance: ${player.balance}): "))
        if not player.place_bet(bet_amount):
            print("Insufficient balance to place bet. Game over.")
            break

        # Deal cards
        player.hand.append(deck.deal_card())
        dealer_hand.append(deck.deal_card())
        player.hand.append(deck.deal_card())
        dealer_hand.append(deck.deal_card())

        print(f"Your hand:")
        player.show_hand()
        print(f"Dealer's hand:")
        print(f"Hidden card")
        print(f"{dealer_hand[1].rank} of {dealer_hand[1].suit}")

        # Player's turn
        while True:
            action = input("Do you want to hit or stand? (h/s): ").lower()
            if action == 'h':
                player.hand.append(deck.deal_card())
                print(f"Your hand:")
                player.show_hand()
                if get_hand_value(player.hand) > 21:
                    print("Bust! You lose.")
                    break
            elif action == 's':
                break

        # Dealer's turn
        while get_hand_value(dealer_hand) < 17:
            dealer_hand.append(deck.deal_card())

        print(f"Dealer's hand:")
        print(f"{dealer_hand[0].rank} of {dealer_hand[0].suit}")
        print(f"{dealer_hand[1].rank} of {dealer_hand[1].suit}")

        # Determine winner
        player_value = get_hand_value(player.hand)
        dealer_value = get_hand_value(dealer_hand)
        if player_value > 21:
            print("Player busts! You lose.")
        elif dealer_value > 21 or player_value > dealer_value:
            print("Congratulations! You win!")
            player.win(bet_amount * 2)
        elif player_value < dealer_value:
            print("Dealer wins. You lose.")
        else:
            print("It's a tie")

        print(f"Your current balance: ${player.balance}")

        # Check if player wants to play again
        play_again = input("Do you want to play again? (Yes/No):")
        if play_again.lower() != 'yes':
            break

def get_hand_value(hand):
    value = 0
    num_aces = 0
    for card in hand:
        if card.rank.isdigit():
            value += int(card.rank)
        elif card.rank in ['Jack', 'Queen', 'King']:
            value += 10
        elif card.rank == 'Ace':
            num_aces += 1
            value += 11
    while value > 21 and num_aces:
        value -= 10
        num_aces -= 1
    return value

def main():
    player_name = input("Enter your name: ")
    game_choice = input("Select game (High Card or Blackjack): ").lower()
    num_decks = int(input("Enter number of decks to use: "))
    if game_choice == 'high card':
        play_high_card(player_name, num_decks)
    elif game_choice == 'blackjack':
        play_blackjack(player_name, num_decks)
    else: 
        print("Invalid game choice!") 

if __name__ == "__main__":
    main()