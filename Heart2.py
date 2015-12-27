__author__ = 'Evan'
import CardEngine.Engine as Cards

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


class Player:
    def __init__(self, name, ai):
        self.name = name
        self.ai = ai
        self.hand = []
        self.display = None


class Hearts:
    def __init__(self, width=800, height=600):
        Cards.CardEngine.init(width, height)

    def play(self):
        while True:
            Cards.CardEngine.update()
            Cards.CardEngine.render()


game = Hearts()
game.play()
