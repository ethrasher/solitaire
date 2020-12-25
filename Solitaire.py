# events-example0.py
# Barebones timer, mouse, and keyboard events

class Card(object):
    def __init__(self, suit, rank, image, backImage):
        self.suit = suit
        self.rank = rank
        self.TLX = 0
        self.TLY = 0
        self.BRX = 70
        self.BRY = 100
        self.width = 70
        self.height = 100
        self.showing = False
        self.image = image
        self.selected = False
        self.backimage = backImage

    def changePos(self, TLX, TLY):
        self.TLX = TLX
        self.TLY = TLY
        self.BRX = TLX + self.width
        self.BRY = TLY + self.height


    def checkClick(self, x, y, isBottom):
        if (isBottom):
            if (self.TLX <= x <= self.BRX):
                if (self.TLY <= y <= self.BRY):
                    return True
        else:
            if (self.TLX<=x<=self.BRX):
                if (self.TLY <= y <= self.TLY+19):
                    return True
        return False

    def draw(self, canvas, x, y):
        if (self.selected):
            canvas.create_rectangle(x-3, y-3, x+70+5, y+100+3, fill="yellow", outline="yellow")
        if (self.showing):
            canvas.create_image(x, y, anchor=NW, image =self.image)
        else:
            canvas.create_image(x, y, anchor=NW, image=self.backimage)

    def printf(self):
        print (self.suit, self.rank)


class Stack(object):
    def __init__(self, num):
        self.stack = []
        self.num = num
        self.y = 175
        self.x = 30 + (num-1)*110

    def addCard(self, Card):
        self.stack.append(Card)
        index=len(self.stack)
        y = self.y+(index-1)*20
        Card.changePos(self.x, y)

    def remCard(self):
        currentCard = self.stack.pop(-1)
        return currentCard

    def remSpCard(self, Card):
        #if (self.stack.count(Card)>0):
         #   self.stack.rem(Card)
        index = None
        rank = Card.rank
        suit = Card.suit
        for i in range (0, len(self.stack)):
            currentCard = self.stack[i]
            if (currentCard.rank == rank):
                if (currentCard.suit == suit):
                    index = i
        if (index != None):
            self.stack.pop(index)
            return True
        return False


    def checkClick(self, x, y):
        if (x<self.x or x>self.x+70):
            return None
        if (y<self.y):
            return None
        numOfCards = len(self.stack)
        maxY = self.y+(numOfCards-1)*20 +100
        if (y>maxY):
            return None
        #They did click on the stack
        index = len(self.stack)-1
        if (index<0):
            #The stack was empty
            return None
        while (index>=0 and y<self.stack[index].TLY):
            index-=1
        if (index<0):
            return None
        return index



    def selectBelow(self, index):
        while (index<len(self.stack)):
            currentCard = self.stack[index]
            if (currentCard.showing):
                currentCard.selected = True
            index +=1

    def draw (self, canvas):
        for index in range(len(self.stack)):
            currentCard = self.stack[index]
            currentCard.draw(canvas, self.x, self.y+index*20)

class AceStack(object):
    def __init__(self, num):
        self.stack = []
        self.num = num
        self.x = 30 + (num-1)*110
        self.y=20

    def addCard(self, Card):
        self.stack.append(Card)
        Card.changePos(self.x, self.y)

    def remCard(self):
        currentCard = self.stack.pop(-1)
        return currentCard

    def remSpCard(self, Card):
        #if (self.stack.count(Card)>0):
         #   self.stack.rem(Card)
        index = None
        rank = Card.rank
        suit = Card.suit
        for i in range (0, len(self.stack)):
            currentCard = self.stack[i]
            if (currentCard.rank == rank):
                if (currentCard.suit == suit):
                    index = i
        if (index != None):
            self.stack.pop(index)
            return True
        return False

    def checkClick(self, x, y):
        for index in range (len(self.stack)):
            currentCard = self.stack[index]
            if (currentCard.checkClick(x, y, True)):
                return index

        return None

    def draw (self, canvas):
        if (len(self.stack)>0):
            currentCard = self.stack[-1]
            currentCard.draw(canvas, self.x, self.y)

class MainDeck (object):
    def __init__(self, backImage):
        self.deck = []
        self.seen = []
        self.x = 700
        self.y = 20
        self.Fx = 600
        self.Fy = 20
        self.backimage = backImage

    def flip (self):
        if (len(self.deck)>0):
            currentCard = self.deck.pop(0)
            self.seen.append(currentCard)
        else:
            while (len(self.seen)>0):
                currentCard = self.seen.pop(0)
                self.deck.append(currentCard)

    def rem (self):
        currentCard = self.deck.pop(-1)
        return currentCard

    def remSpCard(self, Card):
        if (len(self.seen)>0):
            rank = Card.rank
            suit = Card.suit
            currentCard = self.seen[-1]
            if (currentCard.rank == rank):
                if (currentCard.suit == suit):
                    self.seen.pop(-1)
                    return True
        return False
    

    def draw (self, canvas):
        if (len(self.deck)>0):
            canvas.create_image(self.x, self.y, anchor=NW, image =self.backimage)
        if (len(self.seen)>0):
            lastCard = self.seen[-1]
            lastCard.draw(canvas, self.Fx, self.Fy)
            #canvas.create_image(self.Fx, self.Fy, anchor=NW, image=lastCard.image)




from tkinter import *
import random
import time

####################################
# customize these functions
####################################

def init(data):
    data.width = 800
    data.height = 650
    data.ranks = ["2", "3", "4", "5", "6", "7", "8", "9", "10", "Jack", "Queen", "King", "Ace"]
    data.suits = ["clubs", "hearts", "diamonds", "spades"]
    data.selected = []
    loadPlayingCardImages(data)
    createCards(data)
    randomizeCards(data)
    createStacks(data)
    createAceStacks(data)
    createMainDeck(data)
    remakeList(data)
    data.startTime = time.time()
    data.currentTime = 0
    data.moveNum = 0
    data.gameWon = False
    data.cont = False
    findStats(data)
    data.mode="game"
def loadPlayingCardImages(data):
    cards = 53
    data.cardImages = []
    filename = "/Users/thrasher_elizabeth/Documents/self_projects/Solitaire/deck_of_cards/backcard.gif"
    data.cardImages.append(PhotoImage(file=filename))
    for suit in data.suits:
        for rank in data.ranks:
            filename = "/Users/thrasher_elizabeth/Documents/self_projects/Solitaire/deck_of_cards/%s/%s%s.gif" % (suit, rank, suit)
            data.cardImages.append(PhotoImage(file=filename))

def createCards(data):
    index = 1
    data.cards = []
    for suit in data.suits:
        for rank in data.ranks:
            if (rank == "Jack"):
                num="11"
            elif (rank== "Queen"):
                num="12"
            elif (rank=="King"):
                num="13"
            elif (rank=="Ace"):
                num="1"
            else:
                num=rank
            currentCard = Card(suit, num, data.cardImages[index], data.cardImages[0])
            data.cards.append(currentCard)
            index += 1

def randomizeCards(data):
    randomizedCards = []
    fullcount = 52
    count = 52
    while(count>0):
        assert(count == len(data.cards))
        index = random.randint(0, count-1)
        currentCard = data.cards.pop(index)
        randomizedCards.append(currentCard)
        count-=1
    for i in range (fullcount):
        data.cards.append(randomizedCards[i])

def createStacks(data):
    data.stacks = []
    for i in range (1,8):
        currentStack = Stack(i)
        for j in range (i):
            currentCard = data.cards.pop(0)
            currentCard.changePos(30+(i-1)*110, 175+20*(j-1))
            currentStack.addCard(currentCard)
        data.stacks.append(currentStack)

def createAceStacks(data):
    data.AceStacks = []
    for i in range (1,5):
        currentAceStack = AceStack(i)
        data.AceStacks.append(currentAceStack)


def createMainDeck(data):
    data.mainDeck = MainDeck(data.cardImages[0])
    while (len(data.cards)>0):
        currentCard = data.cards.pop(0)
        currentCard.showing = True
        data.mainDeck.deck.append(currentCard)

def findStats(data):
    content=readFile("/Users/thrasher_elizabeth/Documents/self_projects/Solitaire/stats.txt")
    contents =[]
    currentString=""
    for char in content:
        if (char == "\n"):
            contents.append(currentString)
            currentString=""
        else:
            currentString+=char

    data.gamesWon=int(contents[0])
    data.gamesLost=int(contents[1])
    data.totalGames=int(contents[2])
    data.shortestTime=float(contents[3])
    data.longestTime=float(contents[4])
    data.averageTime=float(contents[5])
    data.fewestMoves=int(contents[6])
    data.mostMoves=int(contents[7])
    data.currentWinningStreak=int(contents[8])
    data.longestWinningStreak=int(contents[9])
    if (contents[10]=="True"):
        data.lastWin=True
    else:
        data.lastWin=False


def remakeList(data):
    for stack in data.stacks:
        for card in stack.stack:
            data.cards.append(card)
    for card in data.mainDeck.deck:
        data.cards.append(card)

def resetGame(data):
    updateStats(data)
    init(data)

def mousePressed(event, data):
    if (data.mode=="stats"):
        data.mode="game"
        return
    if(event.x>=460 and event.x<=560):
        if (event.y>=20 and event.y<=50):
            resetGame(data)
        if (event.y>=125 and event.y<=155):
            data.mode="stats"
    if (not (data.gameWon and (not data.cont))):
        mousePressed2(event, data)
    else:
        if (event.x>=data.width/2-125 and event.x<=data.width/2-25):
            if (event.y>=data.height/2+75 and event.y<=data.height/2+115):
                resetGame(data)
        if (event.x>=data.width/2+25 and event.x<=data.width/2+125):
            if (event.y>=data.height/2+75 and event.y<=data.height/2+115):
                data.cont=True
        
def mousePressed2(event, data):
    if (len(data.selected)==0):
        #If Nothing has been selected yet, see if you can select a card
        clearSelected(data)
        jump=False
        for index in range(len(data.stacks)):
            #Check if it is in the stack
            currentStack = data.stacks[index]
            ans = currentStack.checkClick(event.x, event.y)
            if (None != ans):
                currentStack.selectBelow(ans)
                checkSelected(data)
                jump=True
        
        if (not jump):
            if (20<=event.y<=120):
                if (700<=event.x<=770):
                    #Check if in the flipped deck
                    data.mainDeck.flip()
                    data.moveNum+=1
                if (600<=event.x<=670):
                    #Check if in the seen deck
                    currentCard = data.mainDeck.seen[-1]
                    currentCard.selected = True
                    data.selected.append(currentCard)
                for i in range (1,5):
                    #Checking to see if it is in an ace pile
                    LX = 30 + (i-1)*110
                    RX = LX+70
                    if (LX<=event.x<=RX):
                        #clicked in an ace pile
                        if (len(data.AceStacks[i-1].stack)>0):
                            currentCard=data.AceStacks[i-1].stack[-1]
                            currentCard.selected=True
                            data.selected.append(currentCard)


    else:
        #Find the second place clicked (similar to above)
        jump=False
        secondCard = None
        finalPosition = None
        moveToStack=False
        moveToAce=False
        
        for index in range(len(data.stacks)):
            #Check if it is in the stack
            currentStack = data.stacks[index]
            if (currentStack.x <=event.x and currentStack.x+70>=event.x):
                if (currentStack.y <=event.y and currentStack.y+100>=event.y):
                    secondCard = None
                    moveToStack = True
                    finalPosition=index
                    jump=True
            ans = currentStack.checkClick(event.x, event.y)
            if (ans!= None):
                secondCard=currentStack.stack[-1]
                moveToStack=True
                finalPosition = index
                jump=True
        
        if (not jump):
            if (20<=event.y<=120):
                if (700<=event.x<=770):
                    #Check if in the flipped deck
                    clearSelected(data)
                    data.mainDeck.flip()
                    data.moveNum+=1
                    return
                if (600<=event.x<=670):
                    #Check if in the seen deck
                    clearSelected(data)
                    currentCard = data.mainDeck.seen[-1]
                    currentCard.selected = True
                    data.selected.append(currentCard)
                    return
                for i in range (1,5):
                    #Checking to see if it is in an ace pile
                    LX = 30 + (i-1)*110
                    RX = LX+70
                    if (LX<=event.x<=RX):
                        #clicked in an ace pile
                        if (len(data.AceStacks[i-1].stack)>0):
                            secondCard=data.AceStacks[i-1].stack[-1]
                        moveToAce=True
                        finalPosition=i-1

        if (moveToStack):
            if (isLegalMoveToStack(data, secondCard, data.selected[0])):
                currentStack = data.stacks[finalPosition]
                while (len(data.selected)>0):
                    currentCard = data.selected.pop(0)
                    for stack in data.stacks:
                        stack.remSpCard(currentCard)
                    for aceStack in data.AceStacks:
                        aceStack.remSpCard(currentCard)
                    data.mainDeck.remSpCard(currentCard)
                    currentStack.addCard(currentCard)
                    data.moveNum +=1
        if (moveToAce):
            if (len(data.selected)==1):
                if (isLegalMoveToAce(data, secondCard, data.selected[0])):
                    currentAceStack = data.AceStacks[finalPosition]
                    currentCard = data.selected.pop(0)
                    for stack in data.stacks:
                        stack.remSpCard(currentCard)
                    for aceStack in data.AceStacks:
                        aceStack.remSpCard(currentCard)
                    data.mainDeck.remSpCard(currentCard)
                    currentAceStack.addCard(currentCard)
                    data.moveNum+=1
        
        clearSelected(data)

def isLegalMoveToStack(data, card1, card2):
    if (card1==None and card2.rank=="13"):
        return True
    if (card1==None):
        return False
    rank1=card1.rank
    suit1=card1.suit
    rank2=card2.rank
    suit2=card2.suit

    if (suit1=="clubs" or suit1=="spades"):
        color1 = "black"
    else:
        color1 = "red"
    if (suit2=="clubs" or suit2=="spades"):
        color2 = "black"
    else:
        color2 = "red"
    if (color1 == color2):
        return False
    else:
        if (int(rank1) == int(rank2)+1):
            return True
        else:
            return False

def isLegalMoveToAce(data, card1, card2):
    if (card1==None and card2.rank=="1"):
        return True
    elif (card1==None):
        return False
    rank1=card1.rank
    suit1=card1.suit
    rank2=card2.rank
    suit2=card2.suit
    if (suit1 == suit2):
        if (int(rank1)==int(rank2)-1):
            return True
    return False

def inMainDeck(data, card):
    count = count(data.MainDeck.deck, card)
    count += count(data.MainDeck.seen, card)
    if (count>0):
        return True
    return False

def clearSelected(data):
    data.selected = []
    for stack in data.stacks:
        for card in stack.stack:
            card.selected = False
    for aceStack in data.AceStacks:
        for card in aceStack.stack:
            card.selected = False
    for card in data.mainDeck.deck:
        card.selected=False
    for card in data.mainDeck.seen:
        card.selected=False

def isThereSelected(data):
    for stack in data.stacks:
        for card in stack.stack:
            if (card.selected):
                return True
    for card in data.mainDeck.seen:
        if (card.selected):
                return True
    return False


def checkSelected(data):
    for stack in data.stacks:
        for card in stack.stack:
            if (card.selected):
                data.selected.append(card)


def keyPressed(event, data):
    # use event.char and event.keysym
    pass

def timerFired(data):
    if (not (data.gameWon and (not data.cont))):
        data.currentTime = time.time() - data.startTime
    for stack in data.stacks:
        currentList = stack.stack
        if (len(currentList)>0):
            lastCard = currentList[-1]
            if (not lastCard.showing):
                lastCard.showing = True
    allShowing=True
    for card in data.cards:
        if (card.showing == False):
            allShowing=False
    if (allShowing):
        data.gameWon = True

def redrawAll(canvas, data):
    if (data.mode=="stats"):
        redrawStats(canvas, data)
        return
    canvas.create_rectangle(0,0,data.width, data.height, fill = "SpringGreen2")
    createBlanks(canvas, data)
    canvas.create_text(505, 100, text = str(round(data.currentTime, 1)), font = "Times 22 bold")
    canvas.create_text(505, 75, text = str(data.moveNum), font = "Times 22 bold")
    for stack in data.stacks:
        stack.draw(canvas)
    for aceStack in data.AceStacks:
        aceStack.draw(canvas)
    data.mainDeck.draw(canvas)
    canvas.create_rectangle(460, 20, 560, 50, fill="red")
    canvas.create_text(510, 35, text="Reset", fill="white", font="Times 20")
    canvas.create_rectangle(460, 125, 560, 155, fill="black")
    canvas.create_text(510, 140, text="Stats", fill="white", font="Times 20")
    if ((data.gameWon and (not data.cont))):
        canvas.create_rectangle(data.width/4, data.height/4, data.width*3/4, data.height*3/4, fill="black")
        canvas.create_text(data.width/2, data.height/2, text = "You Won!", font = "Times 50 bold", fill="white")
        canvas.create_rectangle(data.width/2-125, data.height/2+75, data.width/2-25, data.height/2+115, fill="red")
        canvas.create_rectangle(data.width/2+25, data.height/2+75, data.width/2+125, data.height/2+115, fill="green")
        canvas.create_text(data.width/2-75, data.height/2+95, text = "Reset", fill="white", font="Times 20")
        canvas.create_text(data.width/2+75, data.height/2+95, text = "Continue",  font="Times 20")

def createBlanks(canvas, data):
    for num in range (1,8):
        TLX = 30+(num-1)*110
        TLY = 175
        BRX = TLX+70
        BRY = TLY+100
        canvas.create_rectangle(TLX, TLY, BRX, BRY, fill = "pale green", outline = "pale green")

    TLX = 700
    TLY = 20
    BRX = TLX+70
    BRY = TLY+100
    canvas.create_rectangle(TLX, TLY, BRX, BRY, fill = "pale green", outline = "pale green")
    TLX = 600
    BRX = 670
    canvas.create_rectangle(TLX, TLY, BRX, BRY, fill = "pale green", outline = "pale green")

    for num in range (1, 5):
        TLX = 30 + (num-1)*110
        BRX=TLX+70
        canvas.create_rectangle(TLX, TLY, BRX, BRY, fill = "pale green", outline = "pale green")

def redrawStats(canvas, data):
    canvas.create_rectangle(0,0,data.width, data.height, fill = "black")
    numOfStats= 10
    '''contents.append(str(data.gamesWon))
    contents.append(str(data.gamesLost))
    contents.append(str(data.totalGames))
    contents.append(str(data.shortestTime))
    contents.append(str(data.longestTime))
    contents.append(str(data.averageTime))
    contents.append(str(data.fewestMoves))
    contents.append(str(data.mostMoves))
    contents.append(str(data.currentWinningStreak))
    contents.append(str(data.longestWinningStreak))'''
    canvas.create_text(data.width/2, 50, text="Statistics", fill="white", font="Times 50 bold")
    statsHeight=data.height-200
    canvas.create_text(data.width/3, statsHeight*1/numOfStats+100, text="Games Won", fill="white", font="Times 25 bold")
    canvas.create_text(data.width*2/3, statsHeight*1/numOfStats+100, text=str(data.gamesWon), fill="white", font="Times 25 bold")
    canvas.create_text(data.width*4/5, statsHeight*1/numOfStats+100, text="("+str(data.gamesWon/data.totalGames)+"%)", fill="white", font="Times 25 bold")

    canvas.create_text(data.width/3, statsHeight*2/numOfStats+100, text="Games Lost", fill="white", font="Times 25 bold")
    canvas.create_text(data.width*2/3, statsHeight*2/numOfStats+100, text=str(data.gamesLost), fill="white", font="Times 25 bold")

    canvas.create_text(data.width/3, statsHeight*3/numOfStats+100, text="Total Games", fill="white", font="Times 25 bold")
    canvas.create_text(data.width*2/3, statsHeight*3/numOfStats+100, text=str(data.totalGames), fill="white", font="Times 25 bold")

    canvas.create_text(data.width/3, statsHeight*4/numOfStats+100, text="Shortest Time", fill="white", font="Times 25 bold")
    canvas.create_text(data.width*2/3, statsHeight*4/numOfStats+100, text=str(round(data.shortestTime,2)), fill="white", font="Times 25 bold")

    canvas.create_text(data.width/3, statsHeight*5/numOfStats+100, text="Longest Time", fill="white", font="Times 25 bold")
    canvas.create_text(data.width*2/3, statsHeight*5/numOfStats+100, text=str(round(data.longestTime,2)), fill="white", font="Times 25 bold")

    canvas.create_text(data.width/3, statsHeight*6/numOfStats+100, text="Average Time", fill="white", font="Times 25 bold")
    canvas.create_text(data.width*2/3, statsHeight*6/numOfStats+100, text=str(round(data.averageTime,2)), fill="white", font="Times 25 bold")

    canvas.create_text(data.width/3, statsHeight*7/numOfStats+100, text="Fewest Moves", fill="white", font="Times 25 bold")
    canvas.create_text(data.width*2/3, statsHeight*7/numOfStats+100, text=str(data.fewestMoves), fill="white", font="Times 25 bold")

    canvas.create_text(data.width/3, statsHeight*8/numOfStats+100, text="Most Moves", fill="white", font="Times 25 bold")
    canvas.create_text(data.width*2/3, statsHeight*8/numOfStats+100, text=str(data.mostMoves), fill="white", font="Times 25 bold")

    canvas.create_text(data.width/3, statsHeight*9/numOfStats+100, text="Current Winning Streak", fill="white", font="Times 25 bold")
    canvas.create_text(data.width*2/3, statsHeight*9/numOfStats+100, text=str(data.currentWinningStreak), fill="white", font="Times 25 bold")

    canvas.create_text(data.width/3, statsHeight*10/numOfStats+100, text="Longest Winning Streak", fill="white", font="Times 25 bold")
    canvas.create_text(data.width*2/3, statsHeight*10/numOfStats+100, text=str(data.longestWinningStreak), fill="white", font="Times 25 bold")


def updateStats(data):
    if (data.gameWon):
        data.gamesWon+=1
        data.totalGames+=1
        if (data.currentTime<data.shortestTime):
            data.shortestTime=data.currentTime
        if (data.currentTime>data.longestTime):
            data.longestTime=data.currentTime
        data.averageTime = (data.averageTime+data.currentTime)/2
        if (data.moveNum<data.fewestMoves):
            data.fewestMoves=data.moveNum
        if (data.moveNum>data.mostMoves):
            data.mostMoves=data.moveNum
        data.currentWinningStreak+=1
        data.lastWin = True
        if (data.currentWinningStreak>data.longestWinningStreak):
            data.longestWinningStreak=data.currentWinningStreak
    else:
        if (data.moveNum>0):
            data.gamesLost+=1
            data.totalGames+=1
            data.lastWin=False
            data.currentWinningStreak=0
    contents=[]
    contents.append(str(data.gamesWon))
    contents.append("\n")
    contents.append(str(data.gamesLost))
    contents.append("\n")
    contents.append(str(data.totalGames))
    contents.append("\n")
    contents.append(str(data.shortestTime))
    contents.append("\n")
    contents.append(str(data.longestTime))
    contents.append("\n")
    contents.append(str(data.averageTime))
    contents.append("\n")
    contents.append(str(data.fewestMoves))
    contents.append("\n")
    contents.append(str(data.mostMoves))
    contents.append("\n")
    contents.append(str(data.currentWinningStreak))
    contents.append("\n")
    contents.append(str(data.longestWinningStreak))
    contents.append("\n")
    contents.append(str(data.lastWin))
    contents.append("\n")
    contents = ''.join(contents)

    writeFile("/Users/thrasher_elizabeth/Documents/self_projects/Solitaire/stats.txt", contents)

def readFile(path):
    with open(path, "rt") as f:
        return f.read()

def writeFile(path, contents):
    with open(path, "wt") as f:
        f.write(contents)

####################################
# use the run function as-is
####################################

def run(width=300, height=300):
    def redrawAllWrapper(canvas, data):
        canvas.delete(ALL)
        redrawAll(canvas, data)
        canvas.update()    

    def mousePressedWrapper(event, canvas, data):
        mousePressed(event, data)
        redrawAllWrapper(canvas, data)

    def keyPressedWrapper(event, canvas, data):
        keyPressed(event, data)
        redrawAllWrapper(canvas, data)

    def timerFiredWrapper(canvas, data):
        timerFired(data)
        redrawAllWrapper(canvas, data)
        # pause, then call timerFired again
        canvas.after(data.timerDelay, timerFiredWrapper, canvas, data)
    # Set up data and call init
    class Struct(object): pass
    data = Struct()
    data.width = width
    data.height = height
    data.timerDelay = 100 # milliseconds
    root = Tk()
    init(data)
    # create the root and the canvas
    
    canvas = Canvas(root, width=data.width, height=data.height)
    canvas.pack()
    # set up events
    root.bind("<Button-1>", lambda event:
                            mousePressedWrapper(event, canvas, data))
    root.bind("<Key>", lambda event:
                            keyPressedWrapper(event, canvas, data))
    timerFiredWrapper(canvas, data)
    # and launch the app
    root.mainloop()  # blocks until window is closed
    updateStats(data)
    print("bye!")

run(800, 650)