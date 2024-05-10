import random

class Card: 
    def __init__(self, suit, rank):
        """Initialize a Card object with a suit and rank."""
        self.suit = suit
        self.rank = rank


class Deck:
    def __init__(self, num_decks=1):
        """Initialize a Deck object with a certain number of decks."""
        # Define the suits and ranks of a standard deck of cards
        suits = ['Hearts', 'Diamonds', 'Clubs', 'Spades']
        ranks = ['2', '3', '4', '5', '6', '7', '8', '9', '10', 'Jack', 'Queen', 'King', 'Ace']
        # Create the deck by generating Card objects for each combination of suit and rank
        self.cards = [Card(suit, rank) for _ in range(num_decks) for suit in suits for rank in ranks]
        # Shuffle the deck
        self.shuffle()

    def shuffle(self):
        """Shuffle the deck."""
        random.shuffle(self.cards)

    def deal_card(self):
        """Deal a card from the deck."""
        return self.cards.pop()

class Player:
    def __init__(self, name, initial_balance=10000):
        """Initialize a Player object with a name and initial balance."""
        self.name = name
        self.balance = initial_balance
        self.hand = []

    def place_bet(self, amount):
        """Place a bet."""
        if amount <= self.balance:
            # Deduct the bet amount from the player's balance if they have sufficient funds
            self.balance -= amount
            return True
        else:
            print("\033[32mInsufficient balance!\033[0m")
            return False

    def win(self, amount):
        """Increment the player's balance when they win."""
        self.balance += amount

    def show_hand(self):
        """Display the player's hand."""
        for card in self.hand:
            print(f"    \033[36m{card.rank} of {card.suit}\033[0m")

def compare_cards(card1, card2):
    """Compare two cards and determine the winner."""
    if card1.rank == 'Ace' and card2.rank != 'Ace':
        return 1
    elif card1.rank != 'Ace' and card2.rank == 'Ace':
        return -1
    elif card1.rank == card2.rank:
        return 0
    else:
        return 1 if card1.rank > card2.rank else -1


def play_high_card(player_name, num_decks=1):
    """Play the High Card game."""
    print("\033[32mPlaying High Card game...\033[0m")
    player = Player(player_name)
    deck = Deck(num_decks)
    while True:
        player.hand = [deck.deal_card()]
        dealer_hand = [deck.deal_card()]
        print(f"\n\033[32mYour card: {player.hand[0].rank} of {player.hand[0].suit}\033[0m")
        result = compare_cards(player.hand[0], dealer_hand[0])
        if result == 1:
            print("\033[36mCongratulations! You win!\033[0m")
            player.win(2)
        elif result == -1:
            print("\033[36mSorry, You lose\033[0m")
        else:
            print("\033[36mIt's a tie\033[0m")
        print(f"\033[32mYour current balance: ${player.balance}\033[0m")
        play_again = input("\033[32mDo you want to play again? (Yes/No):\033[0m ")
        if play_again.lower() != 'yes':
            break

def play_blackjack(player_name, num_decks=1):
    """Play the Blackjack game."""
    print("\033[32mPlaying Blackjack game...\033[0m")
    player = Player(player_name)
    deck = Deck(num_decks)
    
    while True:
        # Reset hands and deck
        player.hand = []
        dealer_hand = []
        deck = Deck(num_decks)

        # Place bet
        bet_amount = int(input(f"\n\033[32m{player_name}, place your bet (current balance: ${player.balance}):\033[0m "))
        if not player.place_bet(bet_amount):
            print("\033[32mInsufficient balance to place bet. Game over.\033[0m")
            break

        # Deal cards
        player.hand.append(deck.deal_card())
        dealer_hand.append(deck.deal_card())
        player.hand.append(deck.deal_card())
        dealer_hand.append(deck.deal_card())

        print(f"\n\033[32mYour hand:\033[0m")
        player.show_hand()
        print(f"\n\033[32mDealer's hand:\033[0m")
        print(f"    \033[32mHidden card\033[0m")
        print(f"    \033[36m{dealer_hand[1].rank} of {dealer_hand[1].suit}\033[0m")

        # Player's turn
        while True:
            action = input("\n\033[32mDo you want to hit or stand? (h/s): \033[0m").lower()
            if action == 'h':
                player.hand.append(deck.deal_card())
                print(f"\n\033[32mYour hand:\033[0m")
                player.show_hand()
                if get_hand_value(player.hand) > 21:
                    print("\033[36mBust! You lose.\033[0m")
                    break
            elif action == 's':
                break

        # Dealer's turn
        while get_hand_value(dealer_hand) < 17:
            dealer_hand.append(deck.deal_card())

        print(f"\n\033[32mDealer's hand:\033[0m")
        print(f"    \033[36m{dealer_hand[0].rank} of {dealer_hand[0].suit}\033[0m")
        print(f"    \033[36m{dealer_hand[1].rank} of {dealer_hand[1].suit}\033[0m")

        # Determine winner
        player_value = get_hand_value(player.hand)
        dealer_value = get_hand_value(dealer_hand)
        if player_value > 21:
            print("\033[36mPlayer busts! You lose.\033[0m")
        elif dealer_value > 21 or player_value > dealer_value:
            print("\033[36mCongratulations! You win!\033[0m")
            player.win(bet_amount * 2)
        elif player_value < dealer_value:
            print("\033[36mDealer wins. You lose.\033[0m")
        else:
            print("\033[36mIt's a tie\033[0m")

        print(f"\033[32mYour current balance: ${player.balance}\033[0m")

        # Check if player wants to play again
        play_again = input("\n\033[32mDo you want to play again? (Yes/No):\033[0m ")
        if play_again.lower() != 'yes':
            break

def get_hand_value(hand):
    """Calculate the value of a hand."""
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
    """Main function to start the game."""
    player_name = input("\033[36mEnter your name: \033[0m")
    game_choice = input("\033[36mSelect game (High Card or Blackjack): \033[0m").lower()
    num_decks = int(input("\033[36mEnter number of decks to use: \033[0m"))
    if game_choice == 'high card':
        play_high_card(player_name, num_decks)
    elif game_choice == 'blackjack':
        play_blackjack(player_name, num_decks)
    else: 
        print("\033[36mInvalid game choice!\033[0m") 

if __name__ == "__main__":
    main()