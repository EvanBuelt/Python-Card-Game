import cards
import threading
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


class State :
    def __init__(self):
        self.owner = None
        
    def onEnter(self) :
        return

    def onExit(self) :
        return

    def update(self):
        return
    
    def handleKeyboard(self) :
        return

    def handleMouseMovement(self) :
        return

    def handleMouseClick(self) :
        return

    def handleCardClick(self) :
        return

    
class StateMachine :
    def __init__(self) :
        self.states = []
        self.currentState = None

    def update(self) :
        return
    
    def handleKeyboard(self) :
        return

    def handleMouseMovement(self) :
        return

    def handleMouseClick(self) :
        return

    def handleCardClick(self) :
        return
        
def printCard(card,frontView) :
    print "You clicked " + values[card.value] + " of " + suits[card.suit]

class HumanAI :
    def __init__(self) :
        self.input = None
        self.card = None
        
class Player :
    def __init__(self,name,AI) :
        self.name = name
        self.AI = AI
        self.hand = []
        self.display = None

    def sortHand(self) :
        swapped = False
        while swapped is False :
            swapped = True
            for i in range(1,len(self.hand)) :
                if self.hand[i - 1].value > self.hand[i].value :
                    temp = self.hand[i - 1]
                    self.hand[i - 1] = self.hand[i]
                    self.hand[i] = temp
                    swapped = False
        swapped = False
        while swapped is False :
            swapped = True
            for i in range(1,len(self.hand)) :
                if self.hand[i - 1].suit > self.hand[i].suit :
                    temp = self.hand[i - 1]
                    self.hand[i - 1] = self.hand[i]
                    self.hand[i] = temp
                    swapped = False

        swapped = False
        while swapped is False :
            swapped = True
            for i in range(1,len(self.display.hand)) :
                if self.display.hand[i - 1].card.value > self.display.hand[i].card.value :
                    temp = self.display.hand[i - 1]
                    self.display.hand[i - 1] = self.display.hand[i]
                    self.display.hand[i] = temp
                    swapped = False
        swapped = False
        while swapped is False :
            swapped = True
            for i in range(1,len(self.display.hand)) :
                if self.display.hand[i - 1].card.suit > self.display.hand[i].card.suit :
                    temp = self.display.hand[i - 1]
                    self.display.hand[i - 1] = self.display.hand[i]
                    self.display.hand[i] = temp
                    swapped = False

        self.display.update()
        print "Sorted"
        
    def loadDisplay(self,cardArt,backCardID) :
        frontArtList = []
        backArtList = []
        for card in self.hand :
            for art in cardArt :
                if art.ID is card.ID :
                    frontArtList.append(art)
                elif art.ID is backCardID :
                    backArtList.append(art)
        self.display = cards.HandDisplay(self.hand,frontArtList,backArtList,0,0,0,30,.1,0,True)

    def alignDisplay(self,angle = None,orientation = None,side = None,pad = None) :
        if angle is not None :
            self.display.update(angle = angle)
        if orientation is not None :
            cards.Engine.centerHand(self.display,orientation)
        if side is not None :
            if pad is None :
                pad = 20
            cards.Engine.padHand(self.display,side,pad)
        
                
class Hearts :
    def __init__(self,width = 800,height = 600) :
        cards.Engine.init(width,height)
        cards.Engine.cardClick += printCard
        self.artIDList = []
        self.artList = []
        self.loadCardArt()
        self.deck = []
        self.shuffledDeck = []
        
        self.players = []
        self.players.append(Player("Evan",None))
        self.players.append(Player("Kevin",None))
        self.players.append(Player("Tim",None))
        self.players.append(Player("Carl",None))

    def play(self) :
        self.getDeck()
        self.shuffleDeck()
        self.dealDeck(self.shuffledDeck)
        self.setPlayerDisplay()
        for player in self.players :
            player.sortHand()
        
        while True :
            
            cards.Engine.update()
            cards.Engine.render()

    def getDeck(self) :
        self.deck = cards.Engine.createDeck(suits,values)
        for card in self.deck :
            card.ID = (card.suit - 1) * 13 + card.value

    def shuffleDeck(self) :
        self.shuffledDeck = cards.Engine.shuffle(self.deck)
        
    def dealDeck(self,deck) :
        for player in self.players :
            cards.Engine.dealCards(deck,player.hand,13)
            player.loadDisplay(self.artList,53)

    def setPlayerDisplay(self) :
        self.players[0].alignDisplay(angle = 0,
                                     orientation = cards.Orientation.HORIZONTAL,
                                     side = cards.Side.BOTTOM,
                                     pad = 50)
        self.players[1].alignDisplay(angle = 90,
                                     orientation = cards.Orientation.VERTICAL,
                                     side = cards.Side.RIGHT,
                                     pad = 50)
        self.players[2].alignDisplay(angle = 180,
                                     orientation = cards.Orientation.HORIZONTAL,
                                     side = cards.Side.TOP,
                                     pad = 50)
        self.players[3].alignDisplay(angle = 270,
                                     orientation = cards.Orientation.VERTICAL,
                                     side = cards.Side.LEFT,
                                     pad = 50)
        
    def loadCardArt(self) :
        artFile = open('CardIDList.txt','r')
        artIDList = artFile.readlines()
        for line in artIDList :
            line = line.strip('\n').split(': ')
            ID = int(line[0])
            imageName = line[1]
            art = cards.CardArt(imagePath + imageName + imageType,ID,imageName)
            self.artIDList.append(line)                               
            self.artList.append(art)
            
game = Hearts()
game.play()
