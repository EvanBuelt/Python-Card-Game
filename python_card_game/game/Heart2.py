
import CardEngine.Engine as Cards


class Player:

  def __init__(self, name, ai):
    self.name = name
    self.ai = ai
    self.hand = []
    self.display = None


class Hearts:

  def __init__(self, width=800, height=600):
    Cards.CardEngine.init(width, height)
    self.deck = None
    self.deck = Cards.CardEngine.create_deck(suits, values, special_cards=None)

  def check_out_deck(self):
    Cards.CardEngine.print_deck(self.deck)
    # print "here I would check out the deck"

  def play(self):
    while True:
      Cards.CardEngine.update()
      Cards.CardEngine.render()

game = Hearts()
game.check_out_deck()
# game.play()
