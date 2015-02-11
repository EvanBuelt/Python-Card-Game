import sys,pygame
from pygame.locals import *
import math
import random

class Card :
    def __init__(self,suit,value,ID = None,owner = None) :
        self.suit = suit
        self.value = value
        self.ID = ID
        self.owner = owner

class CardArt :
    def __init__(self,imagePath,ID,imageName) :
        self._loadImage(imagePath)
        self.ID = ID
        self.imageName = imageName

    def _loadImage(self,imagePath) :
        self.image = pygame.image.load(imagePath)

    def render(self,surface,x,y,angle) :
        rotatedImage = pygame.transform.rotate(self.image,angle)
        surface.blit(rotatedImage,(x,y))

class SquareHitbox :
    def __init__(self,x,y,width,height,angle) :
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.angle = math.radians(angle)
        
        self.points = []
        self.rotatedPoints = []

        self._getPoints()
        self._getRotatedPoints()

    def collide(self,x,y) :
        # Vector math to check if a point is inside the hitbox.  Allows hitbox to be rotated to any angle
        vectorAM = Vector(self.rotatedPoints[0].x - x,
                          self.rotatedPoints[0].y - y)
        vectorAB = Vector(self.rotatedPoints[0].x - self.rotatedPoints[1].x,
                          self.rotatedPoints[0].y - self.rotatedPoints[1].y)
        vectorAD = Vector(self.rotatedPoints[0].x - self.rotatedPoints[3].x,
                          self.rotatedPoints[0].y - self.rotatedPoints[3].y)
        if (0 <= vectorAM * vectorAB < vectorAB * vectorAB) and (0 <= vectorAM * vectorAD < vectorAD * vectorAD):
            return True
        else :
            return False

    def update(self,x = None,y = None,width = None,height = None,angle = None) :
        if x is not None :
            self.x = x
        if y is not None :
            self.y = y
        if width is not None :
            self.width = width
        if height is not None :
            self.height = height
        if angle is not None :
            self.angle = math.radians(angle)

        self._getPoints()
        self._getRotatedPoints()
        
    def _getPoints(self) :
        self.points = []
        self.points.append(Point(self.x,self.y))
        self.points.append(Point(self.x + self.width,self.y))
        self.points.append(Point(self.x + self.width,self.y + self.height))
        self.points.append(Point(self.x,self.y + self.height))
        
    def _getRotatedPoints(self) :
        # Use Point 0 as referance for rotating every point
        x,y = self.points[0].x,self.points[0].y
        
        self.rotatedPoints = []
        for point in self.points :
            self.rotatedPoints.append(point.copy())
            
        for point in self.rotatedPoints :
            point.rotateCCW(x,y,self.angle)

class CardDisplay :
    def __init__(self,card,frontArt,backArt,x,y,z,angle,frontView) :
        self.card = card
        self.frontArt = frontArt
        self.backArt = backArt
        self.x = x
        self.y = y
        self.z = z
        self.angle = angle
        self.frontView = frontView
        self.width = frontArt.image.get_width()
        self.height = frontArt.image.get_height()
        self.hitbox = SquareHitbox(x,y,self.width,self.height,angle)

    def update(self,x = None,y = None,z = None,angle = None,frontView = None) :
        if x is not None :
            self.x = x
        if y is not None :
            self.y = y
        if z is not None :
            self.z = z
        if angle is not None :
            self.angle = angle
        if frontView is not None :
            self.frontView = frontView

        self.hitbox.update(self.x,self.y,self.width,self.height,self.angle)

    def render(self,surface) :
        x = self.hitbox.rotatedPoints[0].x
        y = self.hitbox.rotatedPoints[0].y
        dx = 0
        dy = 0

        # Point 0 is reference used for hitbox, so need to offset the display to match the hitbox
        for point in self.hitbox.rotatedPoints :
            if (point.x - x) < dx :
                dx = point.x - x
            if (point.y - y) < dy :
                dy = point.y - y

        # Display front or back of the card
        if self.frontView is True :
            self.frontArt.render(surface,self.x + dx,self.y + dy,self.angle)
        else :
            self.backArt.render(surface,self.x + dx,self.y + dy,self.angle)
        
    def collide(self,x,y) :
        return self.hitbox.collide(x,y)

class HandDisplay :
    def __init__(self,hand,frontArtList,backArtList,x,y,z,change,dz,angle,frontView) :
        self.hand = []
        self.x = x
        self.y = y
        self.z = z
        self.dx = change * math.cos(-1 * math.radians(angle))
        self.dy = change * math.sin(-1 * math.radians(angle))
        self.dz = dz
        self.change = change
        self.angle = angle
        self.frontView = frontView
        
        for i in range(0,len(hand)) :
            card = hand[i]
            frontArt = frontArtList[i]
            backArt = backArtList[i]
            cardDisplay = Engine.linkCard(card,
                                          frontArt,
                                          backArt,
                                          self.x + i * self.dx,
                                          self.y + i * self.dy,
                                          self.z + i * self.dz,
                                          self.angle,
                                          self.frontView)
            self.hand.append(cardDisplay)

    def insertCard(self,card,frontArt,backArt,index) :
        cardDisplay = Engine.linkCard(card,
                                      frontArt,
                                      backArt,
                                      0,0,0,
                                      self.angle,
                                      self.frontView)
        self.hand.insert(index,cardDisplay)
        self._updateHand()
    
    def removeCard(self,card) :
        for cardDisplay in self.hand :
            if cardDisplay.card is card :
                self.hand.remove(cardDisplay)
                self._updateHand()
                return

    def getCard(self,index) :
        return self.hand[index]

    def switchCards(self,index1,index2) :
        temp = self.hand[index1]
        self.hand[index1] = self.hand[index2]
        self.hand[index2] = temp
        self._updateHand()

    def update(self,x = None,y = None,z = None,change = None,dz = None,angle = None,frontView = None) :
        if x is not None :
            self.x = x
        if y is not None :
            self.y = y
        if z is not None :
            self.z = z
        if change is not None :
            self.change = change
        if dz is not None :
            self.dz = dz
        if angle is not None :
            self.angle = angle
            while self.angle < 0 :
                self.angle = self.angle + 360
            while self.angle > 360 :
                self.angle = self.angle - 360
        if frontView is not None :
            self.frontView = frontView

        if (change is not None) or (angle is not None) :
            self.dx = self.change * math.cos(-1 * math.radians(self.angle))
            self.dy = self.change * math.sin(-1 * math.radians(self.angle))

        self._updateHand()

    def updateCard(self,card,x = None,y = None,z = None,angle = None,frontView = None) :
        for cardDisplay in self.hand :
            if cardDisplay.card is card :
                cardDisplay.card.update(x,y,z,angle,frontView)

    def _updateHand(self) :
        for i in range(0,len(self.hand)) :
            self.hand[i].update(x = self.x + i * self.dx,
                                y = self.y + i * self.dy,
                                z = self.z + i * self.dz,
                                angle = self.angle,
                                frontView = self.frontView)
class Point :
    def __init__(self,x,y) :
        self.x = x
        self.y = y

    def copy(self) :
        return Point(self.x,self.y)
    
    def translate(self,dx,dy) :
        self.x += dx
        self.y += dy

    def rotateCW(self,x,y,angle) :
        nx = math.cos(angle) * (self.x - x) - math.sin(angle) * (self.y - y) + x
        ny = math.sin(angle) * (self.x - x) + math.cos(angle) * (self.y - y) + y

        self.x = nx
        self.y = ny
        
    def rotateCCW(self,x,y,angle) :
        self.rotateCW(x,y,-1*angle)

    def scale(self,x,y,scalar) :
        self.x = math.fabs(self.x - x) * scalar
        self.y = math.fabs(self.y - y) * scalar

    def reflect(self,axis) :
        if axis is 'x' or axis is 'X' :
            self.x *= -1
        elif axis is 'y' or axis is 'Y' :
            self.y *= -1

class Vector :
    def __init__(self,x,y) :
        self.x = x
        self.y = y
        
    def getMagnitude(self) :
        return math.sqrt(pow(self.x,2) + pow(self.y,2))

    def getRadians(self) :
        return math.acos(self.x/self.getMagnitude())

    def getDegrees(self) :
        return math.degrees(self.getRadians)

    def __iadd__(self,other) :
        self.x += other.x
        self.y += other.y
        return self

    def __isub__(self,other) :
        self.x -= other.x
        self.y -= other.y
        return self

    def __imul__(self,num) :
        self.x *= num
        self.y *= num

    def __idiv__(self,num) :
        self.x /= num
        self.y /= num
        
    def __mul__(self,other) :
        return self.x * other.x + self.y * other.y

class MouseButton :
    LEFT = 1
    MIDDLE = 2
    RIGHT = 3
    WHEEL_UP = 4
    WHEEL_DOWN = 5

class Direction :
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
    
class Orientation :
    VERTICAL = 1
    HORIZONTAL = 2

class EventHandler :
    def __init__(self) :
        self.functions = []

    def __iadd__(self,function) :
        if function not in self.functions :
            self.functions.append(function)
        return self

    def __isub__(self,function) :
        if function in self.functions :
            self.functions.remove(function)
        return self

    def notify(self,*args) :
        for function in self.functions :
            function(*args)


class Engine :
    # Pygame Display
    DISPLAYSURF = None

    # Event handlers for various events, to be linked internally and externally
    mouseClick = EventHandler()
    cardClick = EventHandler()
    mouseMovement = EventHandler()
    keyboardInput = EventHandler()
    gameQuit = EventHandler()

    # List of cards for UI
    cards = []

    @classmethod
    def init(cls,width = 800,height = 600) :
        # Seed needed for shuffling function
        random.seed()

        # Setup the pygame display for use in the Engine
        pygame.init()
        cls.width = width
        cls.height = height
        cls.DISPLAYSURF = pygame.display.set_mode((width,height),0,32)
        pygame.display.set_caption('Card Game')

        # Link mouse click event to card click event function 
        cls.mouseClick += cls._onClick

    @classmethod
    def update(cls) :
        for event in pygame.event.get() :
            if event.type == pygame.QUIT :
                cls.gameQuit.notify()
                pygame.quit()
                sys.exit()
            elif event.type == pygame.MOUSEBUTTONDOWN :
                x,y = event.pos
                click = event.type
                button = event.button
                cls.mouseClick.notify(button,click,x,y)
            elif event.type == pygame.MOUSEBUTTONUP :
                x,y = event.pos
                click = event.type
                button = event.button
                cls.mouseClick.notify(button,click,x,y)
            elif event.type == pygame.MOUSEMOTION :
                x,y = event.pos
                cls.mouseMovement.notify(x,y)
            elif event.type == pygame.KEYDOWN :
                key = event.key
                cls.keyboardInput.notify(key)

    @classmethod
    def render(cls) :
        cls.DISPLAYSURF.fill((70,200,70))
        cls._cardDisplaySort()
        for card in cls.cards :
            card.render(cls.DISPLAYSURF)
        pygame.display.update()

    @classmethod
    def _onClick(cls,button,click,x,y) :
        if click is not pygame.MOUSEBUTTONDOWN :
            return
        clicked = []

        if button is MouseButton.LEFT :
            for card in cls.cards :
                if card.collide(x,y) :
                    clicked.append(card)

        if len(clicked) is 0 :
            return

        cardDisp = clicked[0]
        for card in clicked :
            if card.z > cardDisp.z :
                cardDisp = card

        cls.cardClick.notify(cardDisp.card,cardDisp.frontView)

    @classmethod
    def _cardDisplaySort(cls) :
        for i in range(1,len(cls.cards)) :
            j = i
            while (j > 0) and (cls.cards[j - 1].z > cls.cards[j].z) :
                temp = cls.cards[j]
                cls.cards[j] = cls.cards[j - 1]
                cls.cards[j - 1] = temp
                j -= 1

    @classmethod
    def linkCard(cls,card,frontArt,backArt,x,y,z,angle,frontView) :
        display = CardDisplay(card,frontArt,backArt,x,y,z,angle,frontView)
        cls.cards.append(display)
        cls._cardDisplaySort()
        return display

    @classmethod
    def unlinkCard(cls,card) :
        for linkedCard in cards :
            if card is linkedCard.card :
                cls.cards.remove(linked)

    @classmethod
    def unlinkAllCards(cls) :
        cls.cards = []

    @classmethod
    def padCard(cls,cardDisplay,side,offset) :
        if side is Side.TOP :
            y = cardDisplay.y
            for point in cardDisplay.hitbox.rotatedPoints :
                if point.y < y :
                    y = point.y
            dy = cardDisplay.y - y
            cardDisplay.update(y = offset + dy)
            
        elif side is Side.BOTTOM :
            y = cardDisplay.y
            for point in cardDisplay.hitbox.rotatedPoints :
                if point.y > y :
                    y = point.y
            dy = y - cardDisplay.y
            cardDisplay.update(y = (cls.height - 1) - (offset + dy))
            
        elif side is Side.LEFT :
            x = cardDisplay.x
            for point in cardDisplay.hitbox.rotatedPoints :
                if point.x < x :
                    x = point.x
            dx = cardDisplay.x - x
            cardDisplay.update(x = offset + dx)
            
        elif side is Side.RIGHT :
            x = cardDisplay.x
            for point in cardDisplay.hitbox.rotatedPoints :
                if point.x > x :
                    x = point.x
            dx = x - cardDisplay.x
            cardDisplay.update(x = (cls.width - 1) - (offset + dx))
        return

    @classmethod
    def padHand(cls,handDisplay,side,offset) :
        if side is Side.TOP :
            y = handDisplay.y
            for cardDisplay in handDisplay.hand :
                for point in cardDisplay.hitbox.rotatedPoints :
                    if point.y < y :
                        y = point.y
            dy = handDisplay.y - y
            handDisplay.update(y = offset + dy)
            
        elif side is Side.BOTTOM :
            y = handDisplay.y
            for cardDisplay in handDisplay.hand :
                for point in cardDisplay.hitbox.rotatedPoints :
                    if point.y > y :
                        y = point.y
            dy = y - handDisplay.y
            handDisplay.update(y = (cls.height - 1) - (offset + dy))
            
        elif side is Side.LEFT :
            x = handDisplay.x
            for cardDisplay in handDisplay.hand :
                for point in cardDisplay.hitbox.rotatedPoints :
                    if point.x < x :
                        x = point.x
            dx = handDisplay.x - x
            handDisplay.update(x = offset + dx)
            
        elif side is Side.RIGHT :
            x = handDisplay.x
            for cardDisplay in handDisplay.hand :
                for point in cardDisplay.hitbox.rotatedPoints :
                    if point.x > x :
                        x = point.x
            dx = x - handDisplay.x
            handDisplay.update(x = (cls.width - 1) - (offset + dx))
        return

    @classmethod
    def centerCard(cls,cardDisplay,orientation) :
        if orientation is Orientation.VERTICAL :
            dy = (cls.height - (cardDisplay.hitbox.rotatedPoints[2].y + cardDisplay.hitbox.rotatedPoints[0].y)) / 2
            yNew = cardDisplay.y + dy
            cardDisplay.update(y = yNew)
        elif orientation is Orientation.HORIZONTAL :
            dx = (cls.width - (cardDisplay.hitbox.rotatedPoints[2].x + cardDisplay.hitbox.rotatedPoints[0].x)) / 2
            xNew = cardDisplay.x + dx
            cardDisplay.update(x = xNew)
        return

    @classmethod
    def centerHand(cls,handDisplay,orientation) :
        if orientation is Orientation.VERTICAL :
            dy = (cls.height - (handDisplay.hand[0].hitbox.rotatedPoints[0].y + handDisplay.hand[len(handDisplay.hand) - 1].hitbox.rotatedPoints[2].y)) / 2
            yNew = handDisplay.y + dy
            handDisplay.update(y = yNew)
        if orientation is Orientation.HORIZONTAL :
            dx = (cls.width - (handDisplay.hand[0].hitbox.rotatedPoints[0].x + handDisplay.hand[len(handDisplay.hand) - 1].hitbox.rotatedPoints[2].x)) / 2
            xNew = handDisplay.x + dx
            handDisplay.update(x = xNew)
        return
        
    @staticmethod
    def createDeck(suits,values,specialCards = None) :
        deck = []
        for suit in suits :
            for value in values :
                deck.append(Card(suit,value))
        if specialCards is not None :
            for card in specialCards :
                deck.append(card)
        return deck

    @staticmethod
    def shuffle(deck) :
        temp = []
        shuffled = []
        for i in range(0,len(deck)) :
            temp.append(deck[i])
        for i in range(0,len(deck)) :
            rand = random.randrange(0,len(deck) - i)
            shuffled.append(temp.pop(rand))
        return shuffled

    @staticmethod
    def dealCards(deck,hand,numberCards) :
        if len(deck) < numberCards :
            numberCards = len(deck)
        for i in range(0,numberCards) :
            hand.append(deck.pop())

    @staticmethod
    def transferCard(card,source,destination) :
        if card in source :
            source.pop(card)
            destination.append(card)

    @staticmethod
    def transferCards(cardList,source,destination) :
        for card in cardList :
            Engine.transferCard(card,source,destination)

    
