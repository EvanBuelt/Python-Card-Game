import sys
import pygame
import math
import random


class Card:
    def __init__(self, suit, value, card_id=None, owner=None):
        self.suit = suit
        self.value = value
        self.id = card_id
        self.owner = owner


class CardArt:
    def __init__(self, image_path, card_id, image_name):
        self._load_image(image_path)
        self.id = card_id
        self.image_name = image_name

    def _load_image(self, image_path):
        self.image = pygame.image.load(image_path)

    def render(self, surface, x, y, angle):
        rotated_image = pygame.transform.rotate(self.image, angle)
        surface.blit(rotated_image, (x, y))


class SquareHitbox:
    def __init__(self, x, y, width, height, angle):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.angle = math.radians(angle)

        self.points = []
        self.rotatedPoints = []

        self._get_points()
        self._get_rotated_points()

    def collide(self, x, y):
        # Assuming points a, b, c, and d, and a point m with coordinates (x, y).
        # Check the vector from point a to point m against the vectors from a to b and a to d.
        # Vector math to check if a point is inside the hitbox.  Allows hitbox to be rotated to any angle
        vector_am = Vector(self.rotatedPoints[0].x - x,
                           self.rotatedPoints[0].y - y)
        vector_ab = Vector(self.rotatedPoints[0].x - self.rotatedPoints[1].x,
                           self.rotatedPoints[0].y - self.rotatedPoints[1].y)
        vector_ad = Vector(self.rotatedPoints[0].x - self.rotatedPoints[3].x,
                           self.rotatedPoints[0].y - self.rotatedPoints[3].y)
        if 0 <= vector_am * vector_ab < vector_ab * vector_ab and 0 <= vector_am * vector_ad < vector_ad * vector_ad:
            return True
        else:
            return False

    def update(self, x=None, y=None, width=None, height=None, angle=None):
        if x is not None:
            self.x = x
        if y is not None:
            self.y = y
        if width is not None:
            self.width = width
        if height is not None:
            self.height = height
        if angle is not None:
            self.angle = math.radians(angle)

        self._get_points()
        self._get_rotated_points()

    def _get_points(self):
        self.points = []
        self.points.append(Point(self.x, self.y))
        self.points.append(Point(self.x + self.width, self.y))
        self.points.append(Point(self.x + self.width, self.y + self.height))
        self.points.append(Point(self.x, self.y + self.height))

    def _get_rotated_points(self):
        # Use Point 0 as reference for rotating every point
        x, y = self.points[0].x, self.points[0].y

        self.rotatedPoints = []
        for point in self.points:
            self.rotatedPoints.append(point.copy())

        for point in self.rotatedPoints:
            point.rotate_counterclockwise(x, y, self.angle)


class CardDisplay:
    def __init__(self, card, front_art, back_art, x, y, z, angle, front_view):
        self.card = card
        self.frontArt = front_art
        self.backArt = back_art
        self.x = x
        self.y = y
        self.z = z
        self.angle = angle
        self.frontView = front_view
        self.width = front_art.image.get_width()
        self.height = front_art.image.get_height()
        self.hitbox = SquareHitbox(x, y, self.width, self.height, angle)

    def update(self, x=None, y=None, z=None, angle=None, front_view=None):
        if x is not None:
            self.x = x
        if y is not None:
            self.y = y
        if z is not None:
            self.z = z
        if angle is not None:
            self.angle = angle
        if front_view is not None:
            self.frontView = front_view

        self.hitbox.update(self.x, self.y, self.width, self.height, self.angle)

    def render(self, surface):
        x = self.hitbox.rotatedPoints[0].x
        y = self.hitbox.rotatedPoints[0].y
        dx = 0
        dy = 0

        # Point 0 is reference used for hitbox, so need to offset the display to match the hitbox
        for point in self.hitbox.rotatedPoints:
            if (point.x - x) < dx:
                dx = point.x - x
            if (point.y - y) < dy:
                dy = point.y - y

        # Display front or back of the card
        if self.frontView is True:
            self.frontArt.render(surface, self.x + dx, self.y + dy, self.angle)
        else:
            self.backArt.render(surface, self.x + dx, self.y + dy, self.angle)

    def collide(self, x, y):
        return self.hitbox.collide(x, y)


class HandDisplay:
    def __init__(self, hand, front_art_list, back_art_list, x, y, z, change, dz, angle, front_view):
        self.hand = []
        self.x = x
        self.y = y
        self.z = z
        self.dx = change * math.cos(-1 * math.radians(angle))
        self.dy = change * math.sin(-1 * math.radians(angle))
        self.dz = dz
        self.change = change
        self.angle = angle
        self.front_view = front_view

        for i in range(0, len(hand)):
            card = hand[i]
            front_art = front_art_list[i]
            back_art = back_art_list[i]
            card_display = Engine.link_card(card, front_art, back_art,
                                            self.x + i * self.dx,
                                            self.y + i * self.dy,
                                            self.z + i * self.dz,
                                            self.angle, self.front_view)
            self.hand.append(card_display)

    def insert_card(self, card, front_art, back_art, index):
        card_display = Engine.link_card(card,
                                        front_art,
                                        back_art,
                                        0, 0, 0,
                                        self.angle,
                                        self.front_view)
        self.hand.insert(index, card_display)
        self._update_hand()

    def remove_card(self, card):
        for card_display in self.hand:
            if card_display.card is card:
                self.hand.remove(card_display)
                self._update_hand()
                return

    def get_card(self, index):
        return self.hand[index]

    def switch_cards(self, index1, index2):
        temp = self.hand[index1]
        self.hand[index1] = self.hand[index2]
        self.hand[index2] = temp
        self._update_hand()

    def update(self, x=None, y=None, z=None, change=None, dz=None, angle=None, front_view=None):
        if x is not None:
            self.x = x
        if y is not None:
            self.y = y
        if z is not None:
            self.z = z
        if change is not None:
            self.change = change
        if dz is not None:
            self.dz = dz
        if angle is not None:
            self.angle = angle
            while self.angle < 0:
                self.angle += 360
            while self.angle > 360:
                self.angle -= 360
        if front_view is not None:
            self.front_view = front_view

        if (change is not None) or (angle is not None):
            self.dx = self.change * math.cos(-1 * math.radians(self.angle))
            self.dy = self.change * math.sin(-1 * math.radians(self.angle))

        self._update_hand()

    def update_card(self, card, x=None, y=None, z=None, angle=None, front_view=None):
        for card_display in self.hand:
            if card_display.card is card:
                card_display.card.update(x, y, z, angle, front_view)

    def _update_hand(self):
        for i in range(0, len(self.hand)):
            self.hand[i].update(x=self.x + i * self.dx,
                                y=self.y + i * self.dy,
                                z=self.z + i * self.dz,
                                angle=self.angle,
                                front_view=self.front_view)


class Point:
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def copy(self):
        return Point(self.x, self.y)

    def translate(self, dx, dy):
        self.x += dx
        self.y += dy

    def rotate_clockwise(self, x, y, angle):
        nx = math.cos(angle) * (self.x - x) - math.sin(angle) * (self.y - y) + x
        ny = math.sin(angle) * (self.x - x) + math.cos(angle) * (self.y - y) + y

        self.x = nx
        self.y = ny

    def rotate_counterclockwise(self, x, y, angle):
        self.rotate_clockwise(x, y, -1 * angle)

    def scale(self, x, y, scalar):
        self.x = math.fabs(self.x - x) * scalar
        self.y = math.fabs(self.y - y) * scalar

    def reflect(self, axis):
        if axis is 'x' or axis is 'X':
            self.x *= -1
        elif axis is 'y' or axis is 'Y':
            self.y *= -1


class Vector:
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def get_magnitude(self):
        return math.sqrt(pow(self.x, 2) + pow(self.y, 2))

    def get_radians(self):
        return math.acos(self.x / self.get_magnitude())

    def get_degrees(self):
        return math.degrees(self.get_radians())

    def __iadd__(self, other):
        self.x += other.x
        self.y += other.y
        return self

    def __isub__(self, other):
        self.x -= other.x
        self.y -= other.y
        return self

    def __imul__(self, num):
        self.x *= num
        self.y *= num

    def __idiv__(self, num):
        self.x /= num
        self.y /= num

    def __mul__(self, other):
        return self.x * other.x + self.y * other.y


class MouseButton:
    LEFT = 1
    MIDDLE = 2
    RIGHT = 3
    WHEEL_UP = 4
    WHEEL_DOWN = 5

class Direction:
    UP = 1
    RIGHT = 2
    DOWN = 3
    LEFT = 4

class Side:
    TOP = 1
    RIGHT = 2
    BOTTOM = 3
    LEFT = 4

    TOPLEFT = 5
    TOPRIGHT = 6
    BOTTOMRIGHT = 7
    BOTTOMLEFT = 8

class Orientation:
    VERTICAL = 1
    HORIZONTAL = 2

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


class Engine:
    # Pygame Display
    DISPLAYSURF = None
    width = 0
    height = 0

    # Event handlers for various events, to be linked internally and externally
    mouseClick = EventHandler()
    cardClick = EventHandler()
    mouseMovement = EventHandler()
    keyboardInput = EventHandler()
    gameQuit = EventHandler()

    # List of cards for UI
    cards = []

    @classmethod
    def init(cls, width=800, height=600):
        # Seed needed for shuffling function
        random.seed()

        # Setup the pygame display for use in the Engine
        pygame.init()
        cls.width = width
        cls.height = height
        cls.DISPLAYSURF = pygame.display.set_mode((width, height), 0, 32)
        pygame.display.set_caption('Card Game')

        # Link mouse click event to card click event function 
        cls.mouseClick += cls._on_click

    @classmethod
    def update(cls):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                cls.gameQuit.notify()
                pygame.quit()
                sys.exit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                x, y = event.pos
                click = event.type
                button = event.button
                cls.mouseClick.notify(button, click, x, y)
            elif event.type == pygame.MOUSEBUTTONUP:
                x, y = event.pos
                click = event.type
                button = event.button
                cls.mouseClick.notify(button, click, x, y)
            elif event.type == pygame.MOUSEMOTION:
                x, y = event.pos
                cls.mouseMovement.notify(x, y)
            elif event.type == pygame.KEYDOWN:
                key = event.key
                cls.keyboardInput.notify(key)

    @classmethod
    def render(cls):
        cls.DISPLAYSURF.fill((70, 200, 70))
        cls._card_display_sort()
        for card in cls.cards:
            card.render(cls.DISPLAYSURF)
        pygame.display.update()

    @classmethod
    def _on_click(cls, button, click, x, y):
        if click is not pygame.MOUSEBUTTONDOWN:
            return
        clicked = []

        if button is MouseButton.LEFT:
            for card in cls.cards:
                if card.collide(x, y):
                    clicked.append(card)

        if len(clicked) is 0:
            return

        card_display = clicked[0]
        for card in clicked:
            if card.z > card_display.z:
                card_display = card

        cls.cardClick.notify(card_display.card, card_display.frontView)

    @classmethod
    def _card_display_sort(cls):
        for i in range(1, len(cls.cards)):
            j = i
            while (j > 0) and (cls.cards[j - 1].z > cls.cards[j].z):
                temp = cls.cards[j]
                cls.cards[j] = cls.cards[j - 1]
                cls.cards[j - 1] = temp
                j -= 1

    @classmethod
    def link_card(cls, card, front_art, back_art, x, y, z, angle, front_view):
        display = CardDisplay(card, front_art, back_art, x, y, z, angle, front_view)
        cls.cards.append(display)
        cls._card_display_sort()
        return display

    @classmethod
    def unlink_card(cls, card):
        for linked_card in card:
            if card is linked_card.card:
                cls.cards.remove(linked_card)

    @classmethod
    def unlink_all_cards(cls):
        cls.cards = []

    @classmethod
    def pad_card(cls, card_display, side, offset):
        if side is Side.TOP:
            y = card_display.y
            for point in card_display.hitbox.rotatedPoints:
                if point.y < y:
                    y = point.y
            dy = card_display.y - y
            card_display.update(y=offset + dy)

        elif side is Side.BOTTOM:
            y = card_display.y
            for point in card_display.hitbox.rotatedPoints:
                if point.y > y:
                    y = point.y
            dy = y - card_display.y
            card_display.update(y=(cls.height - 1) - (offset + dy))

        elif side is Side.LEFT:
            x = card_display.x
            for point in card_display.hitbox.rotatedPoints:
                if point.x < x:
                    x = point.x
            dx = card_display.x - x
            card_display.update(x=offset + dx)

        elif side is Side.RIGHT:
            x = card_display.x
            for point in card_display.hitbox.rotatedPoints:
                if point.x > x:
                    x = point.x
            dx = x - card_display.x
            card_display.update(x=(cls.width - 1) - (offset + dx))
        return

    @classmethod
    def pad_hand(cls, hand_display, side, offset):
        if side is Side.TOP:
            y = hand_display.y
            for cardDisplay in hand_display.hand:
                for point in cardDisplay.hitbox.rotatedPoints:
                    if point.y < y:
                        y = point.y
            dy = hand_display.y - y
            hand_display.update(y=offset + dy)

        elif side is Side.BOTTOM:
            y = hand_display.y
            for cardDisplay in hand_display.hand:
                for point in cardDisplay.hitbox.rotatedPoints:
                    if point.y > y:
                        y = point.y
            dy = y - hand_display.y
            hand_display.update(y=(cls.height - 1) - (offset + dy))

        elif side is Side.LEFT:
            x = hand_display.x
            for cardDisplay in hand_display.hand:
                for point in cardDisplay.hitbox.rotatedPoints:
                    if point.x < x:
                        x = point.x
            dx = hand_display.x - x
            hand_display.update(x=offset + dx)

        elif side is Side.RIGHT:
            x = hand_display.x
            for cardDisplay in hand_display.hand:
                for point in cardDisplay.hitbox.rotatedPoints:
                    if point.x > x:
                        x = point.x
            dx = x - hand_display.x
            hand_display.update(x=(cls.width - 1) - (offset + dx))
        return

    @classmethod
    def center_card(cls, card_display, orientation):
        if orientation is Orientation.VERTICAL:
            dy = (cls.height - (card_display.hitbox.rotatedPoints[2].y + card_display.hitbox.rotatedPoints[0].y)) / 2
            new_y = card_display.y + dy
            card_display.update(y=new_y)
        elif orientation is Orientation.HORIZONTAL:
            dx = (cls.width - (card_display.hitbox.rotatedPoints[2].x + card_display.hitbox.rotatedPoints[0].x)) / 2
            new_x = card_display.x + dx
            card_display.update(x=new_x)
        return

    @classmethod
    def center_hand(cls, hand_display, orientation):
        if orientation is Orientation.VERTICAL:
            dy = (cls.height - (hand_display.hand[0].hitbox.rotatedPoints[0].y +
                                hand_display.hand[len(hand_display.hand) - 1].hitbox.rotatedPoints[2].y)) / 2
            new_y = hand_display.y + dy
            hand_display.update(y=new_y)
        if orientation is Orientation.HORIZONTAL:
            dx = (cls.width - (hand_display.hand[0].hitbox.rotatedPoints[0].x +
                               hand_display.hand[len(hand_display.hand) - 1].hitbox.rotatedPoints[2].x)) / 2
            new_x = hand_display.x + dx
            hand_display.update(x=new_x)
        return

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
    def shuffle(deck):
        temp = []
        shuffled = []
        for i in range(0, len(deck)):
            temp.append(deck[i])
        for i in range(0, len(deck)):
            rand = random.randrange(0, len(deck) - i)
            shuffled.append(temp.pop(rand))
        return shuffled

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
            Engine.transfer_card(card, source, destination)
