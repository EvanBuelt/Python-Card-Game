
import sys
# import pygame
import random

from card import Card

# totally untested


class MouseButton:
  LEFT = 1
  MIDDLE = 2
  RIGHT = 3
  WHEEL_UP = 4
  WHEEL_DOWN = 5

# totally untested


class EventHandler:

  def __init__(self):
    self.functions = []

  def __iadd__(self, function):
    if function not in self.functions:
      self.functions.append(function)
    return self

  def __isub__(self, function):
    if function in self.functions:
      self.functions.remove(function)
    return self

  def notify(self, *args):
    for function in self.functions:
      function(*args)


class CardEngine(object):
  """docstring for CardEngine"""

  def __init__(self, arg):
    super(CardEngine, self).__init__()
    self.arg = arg

  # Pygame Display
  DISPLAYSURFACE = None
  width = 0
  height = 0

  # Event handlers for various events, to be linked internally and externally
  mouseClick = EventHandler()
  cardClick = EventHandler()
  mouseMovement = EventHandler()
  keyPress = EventHandler()
  gameQuit = EventHandler()

  # List of UI Elements
  UIElements = []

  def __init__(self):
    raise NotImplementedError("CardEgnine cannot be instantiated.")

  @classmethod
  def init(cls, width=800, height=600, display_caption='A Card Game'):
    # Seed needed for shuffling function
    random.seed()

    # Setup the pygame display for use in the Engine
    pygame.init()
    cls.width = width
    cls.height = height
    cls.DISPLAYSURFACE = pygame.display.set_mode((width, height), 0, 32)
    pygame.display.set_caption(display_caption)

    # Link mouse click event to card click event function
    cls.mouseClick += cls._on_click

  @classmethod
  def update(cls):
    for event in pygame.event.get():
      if event.type == pygame.QUIT:
        # Notify other parts before closing the window and exiting program.
        cls.gameQuit.notify()
        pygame.quit()
        sys.exit()

      elif event.type == pygame.MOUSEBUTTONDOWN:
        cls.mouseClick.notify(event)

      elif event.type == pygame.MOUSEBUTTONUP:
        cls.mouseClick.notify(event)

      elif event.type == pygame.MOUSEMOTION:
        cls.mouseMovement.notify(event)

      elif event.type == pygame.KEYDOWN:
        cls.keyPress.notify(event)

      elif event.type == pygame.KEYUP:
        cls.keyPress.notify(event)

  @classmethod
  def render(cls):
    """
    @summary:
    @param cls:
    @result:
    """
    cls.DISPLAYSURFACE.fill((70, 200, 70))
    cls._sort_ui_elements()
    for card in cls.UIElements:
      card.render(cls.DISPLAYSURFACE)
    pygame.display.update()

  @classmethod
  def _on_click(cls, button, click, x, y):
    if click is not pygame.MOUSEBUTTONDOWN:
      return
    clicked = []

    if button is MouseButton.LEFT:
      for card in cls.UIElements:
        if card.collide(x, y):
          clicked.append(card)

    if len(clicked) is 0:
      return

    card_display = clicked[0]
    for card in clicked:
      if card.z > card_display.z:
        card_display = card

    cls.cardClick.notify(card_display.card, card_display.frontView)

  # Methods below are used to handle the ui elements on screen.
  @classmethod
  def _sort_ui_elements(cls):
    for i in range(1, len(cls.UIElements)):
      j = i
      while (j > 0) and (cls.UIElements[j - 1].z > cls.UIElements[j].z):
        temp = cls.UIElements[j]
        cls.UIElements[j] = cls.UIElements[j - 1]
        cls.UIElements[j - 1] = temp
        j -= 1

  @classmethod
  def add_ui_element(cls, ui_element):
    if ui_element not in cls.UIElements:
      cls.UIElements.append(ui_element)

  @classmethod
  def remove_ui_element(cls, ui_element):
    if ui_element in cls.UIElements:
      cls.UIElements.remove(ui_element)

  @classmethod
  def remove_all_ui_elements(cls):
    del cls.UIElements[:]

  # Methods below are used to create and shuffle a deck.
  @staticmethod
  def create_deck(suits, values, special_cards=None):
    deck = []
    for suit in suits:
      for value in values:
        deck.append(Card(suit, value))
    if special_cards is not None:
      for card in special_cards:
        deck.append(card)
    return deck

  @staticmethod
  def print_deck(deck):
    for card in deck:
      print "card -> ", card

  @staticmethod
  def shuffle(deck):
    temp = []
    shuffled = []
    for i in range(0, len(deck)):
      temp.append(deck[i])
    for i in range(0, len(deck)):
      rand = random.randrange(0, len(deck) - i)
      shuffled.append(temp.pop(rand))
    return shuffled

  # Methods below deal with transferring cards.
  @staticmethod
  def deal_cards(deck, hand, number_cards):
    if len(deck) < number_cards:
      number_cards = len(deck)
    for i in range(0, number_cards):
      hand.append(deck.pop())

  @staticmethod
  def transfer_card(card, source, destination):
    if card in source:
      source.pop(card)
      destination.append(card)

  @staticmethod
  def transfer_cards(card_list, source, destination):
    for card in card_list:
      if card in source:
        source.remove(card)
        destination.append(card)
