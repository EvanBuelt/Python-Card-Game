import CardEngine.cards as cards

imagePath = "img/Cards/"
imageType = ".png"

suits = {1: "Clubs",
         2: "Diamonds",
         3: "Spades",
         4: "Hearts"}

values = {1: "Ace",
          2: "2",
          3: "3",
          4: "4",
          5: "5",
          6: "6",
          7: "7",
          8: "8",
          9: "9",
          10: "10",
          11: "Jack",
          12: "Queen",
          13: "King"}


class State:
    def __init__(self):
        self.owner = None

    def on_enter(self):
        self.owner = None
        return

    def on_exit(self):
        self.owner = None
        return

    def update(self):
        self.owner = None
        return

    def handle_keyboard(self):
        self.owner = None
        return

    def handle_mouse_movement(self):
        self.owner = None
        return

    def handle_mouse_click(self):
        self.owner = None
        return

    def handle_card_click(self):
        self.owner = None
        return


class StateMachine:
    def __init__(self):
        self.states = []
        self.currentState = None

    def update(self):
        self.currentState = None
        return

    def handle_keyboard(self):
        self.currentState = None
        return

    def handle_mouse_movement(self):
        self.currentState = None
        return

    def handle_mouse_click(self):
        self.currentState = None
        return

    def handle_card_click(self):
        self.currentState = None
        return


def print_card(card, front_view):
    if front_view:
        print "You clicked " + values[card.value] + " of " + suits[card.suit] + "."
    else:
        print "You clicked " + values[card.value] + " of " + suits[card.suit]
        print "But it was not in view."


class HumanAI:
    def __init__(self):
        self.input = None
        self.card = None


class Player:
    def __init__(self, name, ai):
        self.name = name
        self.ai = ai
        self.hand = []
        self.display = None

    def sort_hand(self):
        swapped = False
        while swapped is False:
            swapped = True
            for i in range(1, len(self.hand)):
                if self.hand[i - 1].value > self.hand[i].value:
                    temp = self.hand[i - 1]
                    self.hand[i - 1] = self.hand[i]
                    self.hand[i] = temp
                    swapped = False
        swapped = False
        while swapped is False:
            swapped = True
            for i in range(1, len(self.hand)):
                if self.hand[i - 1].suit > self.hand[i].suit:
                    temp = self.hand[i - 1]
                    self.hand[i - 1] = self.hand[i]
                    self.hand[i] = temp
                    swapped = False

        swapped = False
        while swapped is False:
            swapped = True
            for i in range(1, len(self.display.hand)):
                if self.display.hand[i - 1].card.value > self.display.hand[i].card.value:
                    temp = self.display.hand[i - 1]
                    self.display.hand[i - 1] = self.display.hand[i]
                    self.display.hand[i] = temp
                    swapped = False
        swapped = False
        while swapped is False:
            swapped = True
            for i in range(1, len(self.display.hand)):
                if self.display.hand[i - 1].card.suit > self.display.hand[i].card.suit:
                    temp = self.display.hand[i - 1]
                    self.display.hand[i - 1] = self.display.hand[i]
                    self.display.hand[i] = temp
                    swapped = False

        self.display.update()
        print "Sorted"

    def load_display(self, card_art, back_card_id):
        front_art_list = []
        back_art_list = []
        for card in self.hand:
            for art in card_art:
                if art.ID is card.ID:
                    front_art_list.append(art)
                elif art.ID is back_card_id:
                    back_art_list.append(art)
        self.display = cards.HandDisplay(self.hand, front_art_list, back_art_list, 0, 0, 0, 30, .1, 0, True)

    def align_display(self, angle=None, orientation=None, side=None, pad=None):
        if angle is not None:
            self.display.update(angle=angle)
        if orientation is not None:
            cards.Engine.center_hand(self.display, orientation)
        if side is not None:
            if pad is None:
                pad = 20
            cards.Engine.pad_hand(self.display, side, pad)


class Hearts:
    def __init__(self, width=800, height=600):
        cards.Engine.init(width, height)
        cards.Engine.cardClick += print_card
        self.artIDList = []
        self.artList = []
        self.load_card_art()
        self.deck = []
        self.shuffledDeck = []

        self.players = []
        self.players.append(Player("Evan", None))
        self.players.append(Player("Kevin", None))
        self.players.append(Player("Tim", None))
        self.players.append(Player("Carl", None))

    def play(self):
        self.get_deck()
        self.shuffle_deck()
        self.deal_deck(self.shuffledDeck)
        self.set_player_display()
        for player in self.players:
            player.sort_hand()

        while True:
            cards.Engine.update()
            cards.Engine.render()

    def get_deck(self):
        self.deck = cards.Engine.create_deck(suits, values)
        for card in self.deck:
            card.ID = (card.suit - 1) * 13 + card.value

    def shuffle_deck(self):
        self.shuffledDeck = cards.Engine.shuffle(self.deck)

    def deal_deck(self, deck):
        for player in self.players:
            cards.Engine.deal_cards(deck, player.hand, 13)
            player.load_display(self.artList, 53)

    def set_player_display(self):
        self.players[0].align_display(angle=0,
                                      orientation=cards.Orientation.HORIZONTAL,
                                      side=cards.Side.BOTTOM,
                                      pad=50)
        self.players[1].align_display(angle=90,
                                      orientation=cards.Orientation.VERTICAL,
                                      side=cards.Side.RIGHT,
                                      pad=50)
        self.players[2].align_display(angle=180,
                                      orientation=cards.Orientation.HORIZONTAL,
                                      side=cards.Side.TOP,
                                      pad=50)
        self.players[3].align_display(angle=270,
                                      orientation=cards.Orientation.VERTICAL,
                                      side=cards.Side.LEFT,
                                      pad=50)

    def load_card_art(self):
        art_file = open('CardIDList.txt', 'r')
        art_id_list = art_file.readlines()
        for line in art_id_list:
            line = line.strip('\n').split(': ')
            image_id = int(line[0])
            image_name = line[1]
            art = cards.CardArt(imagePath + image_name + imageType, image_id, image_name)
            self.artIDList.append(line)
            self.artList.append(art)


game = Hearts()
game.play()
