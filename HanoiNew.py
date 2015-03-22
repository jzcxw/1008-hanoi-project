from Tkinter import *
from turtle import TurtleScreen, RawTurtle
import tkMessageBox

root = Tk()
stepList = []
gameStatus = "turtle"
currentStatus = "AI"

def getGameStatus():
    return gameStatus

class Disc(RawTurtle):
    """Hanoi disc, a RawTurtle object on a TurtleScreen."""

    def __init__(self, cv, value):
        RawTurtle.__init__(self, cv, shape="square", visible=False)
        self.dValue = value
        self.pu()
        self.goto(-140, 200)

    def config(self, k, n):
        self.hideturtle()
        f = float(k + 1) / n
        self.shapesize(0.5, 1.5 + 5 * f)  # square-->rectangle
        self.fillcolor(f, 0, 1 - f)
        self.showturtle()

    def getDiscValue(self):
        return self.dValue

    def addValue(self, v):
        self.dValue = v


class WinData:
    "data required for high score table"
    def __init__(self, discs, count):
        self.numOfDiscs = discs
        self.numOfMove = count

    def getNumOfDiscs(self):
        return self.numOfDiscs

    def getNumOfMove(self):
        return self.numOfMove

class MyMoves:
    def __init__(self, src, dest):
        self.srcTower = src
        self.destTower = dest
        self.srcTowerPeekValue = src.peek()
        self.destTowerPeekValue = dest.peek()

    def getSrcTower(self):
        return self.srcTower

    def getDestTower(self):
        return self.destTower

    def getSrcTowerPeek(self):
        return self.srcTowerPeekValue

    def getDestTowerPeek(self):
        return self.destTowerPeekValue



class Tower():
    "Hanoi tower, a subclass of built-in type list"

    def __init__(self, x):
        self.top = -1
        self.data = []
        "create an empty tower. x is x-position of peg"
        self.x = x


    def push(self, d):
        global gameStatus
        if gameStatus is "turtle":
            d.setx(self.x)
            d.sety(-70 + 10 * len(self.data))
            self.top += 1
            self.data.append(d)
        elif gameStatus is "withoutTurtle":
            self.top += 1
            self.data.append(d)

        '''d.setx(self.x)
        d.sety(-70 + 10 * len(self.data))
        self.top += 1
        self.data.append(d)'''


    def pop(self, y=90):
        global gameStatus
        if gameStatus is "turtle":
            if(self.top == -1): #If nothing in the stack
                return
            value = self.data[self.top]
            d = value
            d.sety(y)
            del self.data[self.top]
            self.top = self.top - 1

            return d
        elif gameStatus is "withoutTurtle":
            if(self.top == -1): #If nothing in the stack
                return
            d = self.data[self.top]
            del self.data[self.top]
            self.top = self.top - 1

            return d
        '''
        if(self.top == -1): #If nothing in the stack
            return
        value = self.data[self.top]
        d = value
        d.sety(y)
        del self.data[self.top]
        self.top = self.top - 1

        return d
        '''

    def peek(self):
        if self.size() is 0 and self.top is -1:
            return None
        else:
            value = self.data[self.top]
            return value.getDiscValue()

    def isEmpty(self):
        if(self.top == -1):
            return True
        return False

    def size(self):
        #print len(self.data)
        return len(self.data)

    def copyFrom(self, aStack):
        #Copy all the elements and properties (include top value) from the input stack aStack to this stack
        del self.data[:]
        for i in range(aStack.size()):
            self.data.append(aStack.peekAt(i))
        self.top = aStack.top

    def peekAt(self, i):
        #Return the value of the element at index i without removing it from the stack
        return self.data[i]

    def isEqual(self, stack):
        if((len(self.data))!= (stack.size())):
            return False
        else:
            for i in range(len(self.data)):
                if(self.data[i] != stack.data[i]):
                    return False
            return True


class HanoiEngine:
    """Play the Hanoi-game on a given TurtleScreen."""

    def __init__(self, canvas, nrOfDiscs, speed, moveCntDisplay=None):
        """Sets Canvas to play on as well as default values for
        number of discs and animation-speed.
        moveCntDisplay is a function with 1 parameter, which communicates
        the count of the actual move to the GUI containing the
        Hanoi-engine-canvas."""
        global gameStatus
        self.highScoreArray = []
        self.combinedArray = []
        self.universalArray = []

        self.setCanvas = canvas
        self.ts = canvas
        self.ts.tracer(False)
        # setup scene
        self.designer = RawTurtle(canvas, shape="square")
        self.designer.penup()
        self.designer.shapesize(0.5, 21)
        self.designer.goto(0, -80)
        self.designer.stamp()
        self.designer.shapesize(7, 0.5)
        self.designer.fillcolor('pink')
        for x in -140, 0, 140:
            self.designer.goto(x, -5)
            self.designer.stamp()

        self.nrOfDiscs = nrOfDiscs
        self.speed = speed
        self.moveDisplay = moveCntDisplay
        self.running = False
        self.moveCnt = 0
        self.winCondition = False

        ''' elson code '''
        gameStatus = "withoutTurtle"
        self.currentStatus = "AI"
        self.samplemoves = [] # The set of move generate by AI
        self.usermoves = [] # The set of move user move
        self.finalmoves = [] # The final set of move

        self.minmoves = 0
        self.totalmoves = 0

        self.startsource = Tower(-140)
        self.starthelper = Tower(0)
        self.starttarget = Tower(140)
        self.goaltarget = Tower(140)

        self.AISource = Tower(-140)
        self.AIHelper = Tower(0)
        self.AITarget = Tower(140)

        self.goalMoves = []
        self.playerMoves = []
        ''' elson code '''

        self.numValue = 0
        self.discs = []

        self.towerA = Tower(-140)
        self.towerB = Tower(0)
        self.towerC = Tower(140)

        print "A:", self.towerA.size(), "value:", self.towerA.peek()
        print "B:", self.towerB.size(), "value:", self.towerB.peek()
        print "C:", self.towerC.size(), "value:", self.towerC.peek()



        self.ts.tracer(True)

    def getGameStatus(self):
        return self.gameStatus


    #elson code
    def savestate(self, stack):
        self.newstack = Tower(0)
        self.newstack.copyFrom(stack)
        return self.newstack

    #elson code
    # Restore the stack to start state
    def startstate(self):
        self.towerA.copyFrom(self.startsource)
        self.towerB.copyFrom(self.starthelper)
        self.towerC.copyFrom(self.starttarget)

    #elson code
    def moveTower(self, disc, Beg, Aux, End):


        global gameStatus

        if disc == 1:
            self.moveDisk(Beg, End)
            if getGameStatus() is "turtle":
                self.moveCnt += 1
                self.moveDisplay(self.moveCnt)
                self.samplemoves.append(self.savestate(self.towerA))
                self.samplemoves.append(self.savestate(self.towerB))
                self.samplemoves.append(self.savestate(self.towerC))
            #print (Beg, Aux, End)

        else:
            self.moveTower(disc-1, Beg, End, Aux)
            self.moveTower(1, Beg, Aux, End)
            self.moveTower(disc-1, Aux, Beg, End)



    '''elson code'''
    # Move disk from the src stack to dest stack
    def moveDisk(self, frompole, topole):
        # print("moving disk from",frompole.gettitle(),"to",topole.gettitle())
        #if self.checkvalid(frompole, topole) is True:
        #if getGameStatus() is "turtle":

        if self.currentStatus is "AI":
            self.goalMoves.append(MyMoves(frompole, topole))
        else:
            self.playerMoves.append(MyMoves(frompole, topole))
            self.moveCnt += 1
        self.moveDisplay(self.moveCnt)
        print("moving disk from ",frompole.peek()," to ",topole.peek())
        topole.push(frompole.pop())
        #self.moveCnt += 1
        #self.moveDisplay(self.moveCnt)


    '''elson code'''
    # generate the sample set of solutions
    def gensamplemove(self, source, helper, target):
        self.moveTower(source.size(), source, helper, target)

    '''elson code'''
    # Check of the rules of Hanoi
    def checkvalid(self, frompole, topole):
        if(frompole.size() == 0 or frompole == topole): # frompole is empty or frompole and topole is same
            return False
        else:
            if(topole.peek() is None or frompole.peek() < topole.peek()): # topole is empty or from is smaller than to

                self.moveDisk(frompole, topole)
                self.usermoves.append(self.savestate(self.towerA))
                self.usermoves.append(self.savestate(self.towerB))
                self.usermoves.append(self.savestate(self.towerC))

                self.finalmoves.append(self.savestate(self.towerA))
                self.finalmoves.append(self.savestate(self.towerB))
                self.finalmoves.append(self.savestate(self.towerC))
                return True
            elif frompole.peek() > topole.peek():
                return False



    '''elson code'''
    # Conver the string input to the variable of stack
    '''def convert(self, word):
        if(word == "a"):
            return source
        elif(word == "b"):
            return helper
        elif(word == "c"):
            return target'''

    '''elson code'''
    def findmatch(self):
        for i in range(len(self.usermoves)-1,0,-3):
            #print (self.usermoves[i-2], self.usermoves[i-1], self.usermoves[i])
            if(i != len(self.usermoves)-1): # append the backtrack state, only add after first i loop
                self.finalmoves.append(self.usermoves[i-2])
                self.finalmoves.append(self.usermoves[i-1])
                self.finalmoves.append(self.usermoves[i])
            for j in range(0, len(self.samplemoves), 3):
                #print (self.samplemoves[i-2], self.samplemoves[i-1], self.samplemoves[i])
                if(self.usermoves[i-2].isEqual(self.samplemoves[j]) and self.usermoves[i-1].isEqual(self.samplemoves[j+1]) and self.usermoves[i].isEqual(self.samplemoves[j+2])):
                    index = j
                    return j

    '''elson code'''
    def solve(self):
        global gameStatus
        gameStatus = "turtle"
        '''
        index = self.findmatch()
        for j in range(index+3,len(self.samplemoves),3): # append state after the match
            self.finalmoves.append(self.samplemoves[j])
            self.finalmoves.append(self.samplemoves[j+1])
            self.finalmoves.append(self.samplemoves[j+2])
        '''

        newArray = []
        num = len(self.playerMoves)-1
        for q in range(0, len(self.playerMoves)):
            temp = self.playerMoves[q].srcTower
            self.playerMoves[q].srcTower = self.playerMoves[q].destTower
            self.playerMoves[q].destTower = temp
            newArray.append(self.playerMoves[num])
            num-=1

        #print len(newArray)

        self.speed = 8 % 10
        self.setspeed()

        for w in range(0, len(newArray)):
            #print newArray[w]
            self.move(newArray[w].srcTower, newArray[w].destTower)

        self.speed = 3 % 10
        self.setspeed()

        for v in range(0, len(self.goalMoves)):
            self.move(self.goalMoves[v].srcTower, self.goalMoves[v].destTower)



        del newArray[:]
        gameStatus = "turtle"
        self.currentStatus = "AI"

        return True

    def getTowerA(self):
        return self.towerA

    def getTowerB(self):
        return self.towerB

    def getTowerC(self):
        return self.towerC


    def setspeed(self):
        for disc in self.discs: disc.speed(self.speed)


    def move(self, src_tower, dest_tower):
        """move uppermost disc of source tower to top of destination
        tower."""
        self.winCondition = False
        dest_tower.push(src_tower.pop())
        self.moveCnt += 1
        self.moveDisplay(self.moveCnt)



    def reset(self):
        """Setup of (a new) game."""
        del self.playerMoves[:]
        del self.goalMoves[:]
        self.ts.tracer(False)
        global gameStatus, currentStatus
        gameStatus = "turtle"
        self.moveCnt = 0
        self.moveDisplay(0)

        self.resetTowers(self.towerA)
        self.resetTowers(self.towerB)
        self.resetTowers(self.towerC)

        self.numValue = 0

        del self.discs[:]

        for x in range(self.nrOfDiscs):
            self.numValue += 1
            self.discs.append(Disc(self.setCanvas, self.numValue))
            print self.numValue

        for k in range(self.nrOfDiscs - 1, -1, -1):
            self.discs[k].config(k, self.nrOfDiscs)#
            self.towerA.push(self.discs[k])

        gameStatus = "withoutTurtle"

        ''' elson code '''
        self.startsource.copyFrom(self.towerA) # Save the start state
        self.starthelper.copyFrom(self.towerB)
        self.starttarget.copyFrom(self.towerC)

        # Include the start state in sample moves set
        self.samplemoves.append(self.startsource)
        self.samplemoves.append(self.starthelper)
        self.samplemoves.append(self.starttarget)
        ''' elson code '''

        """ AI attempt to solve """
        self.gensamplemove(self.towerA, self.towerB, self.towerC)



        # Printing for checking sample moves set purpose
        # print "Number of element:",len(samplemoves)
        # print "Number of minimum steps:",minmoves
        # for i in range(0, len(samplemoves), 3):
        #    printprogess(samplemoves[i], samplemoves[i+1], samplemoves[i+2])

        """ Restore start state """
        self.startstate()

        # Include the start state in user moves set
        self.usermoves.append(self.startsource)
        self.usermoves.append(self.starthelper)
        self.usermoves.append(self.starttarget)

        self.finalmoves.append(self.startsource)
        self.finalmoves.append(self.starthelper)
        self.finalmoves.append(self.starttarget)

        gameStatus = "turtle"
        self.currentStatus = "user"


        #for k in range(self.nrOfDiscs - 1, -1, -1):
        #    self.discs[k].config(k, self.nrOfDiscs)
        #    self.towerA.push(self.discs[k])
        #    self.AISource.push(self.discs[k])

        print "A:", self.towerA.size()
        print "B:", self.towerB.size()
        print "C:", self.towerC.size()

        self.ts.tracer(True)


        #self.HG = self.hanoi(self.nrOfDiscs,
        #                     self.towerA, self.towerC, self.towerB)

    def resetTowers(self, tower):
        if tower.size() > 0:
            for x in range(0,tower.size()):
                tower.pop(200)


    def checkWin(self):
        if self.towerC.size() is self.nrOfDiscs:
            self.winCondition = True
            Hanoi.state = "DONE"
            return self.winCondition

    def storeHighScore(self):
        self.highScoreArray.append(WinData(self.nrOfDiscs, self.moveCnt))

        for j in range(1, 11):

            for i in range(0, len(self.highScoreArray)):
                if self.highScoreArray[i].getNumOfDiscs() is j:
                    self.universalArray.append(self.highScoreArray[i])

            if len(self.universalArray) > 0:
                self.doSelectionSort(self.universalArray)
                self.combinedArray = self.combinedArray+self.universalArray
                del self.universalArray[:]

        del self.highScoreArray[:]
        for w in range(0, len(self.combinedArray)):
            self.highScoreArray.append(self.combinedArray[w])
        del self.combinedArray[:]

        return self.highScoreArray

    def doSelectionSort(self, universalArray):
        n = len(universalArray)

        for fillslot in range(n-1, 0, -1):
            positionOfMax = 0
            for location in range(1, fillslot+1):
                if universalArray[location].getNumOfMove() > universalArray[positionOfMax].getNumOfMove():
                    positionOfMax = location

            tmp = universalArray[fillslot]
            universalArray[fillslot] = universalArray[positionOfMax]
            universalArray[positionOfMax] = tmp

    def stop(self):
        """ ;-) """
        self.running = False

    def checkIfMoveValid(self, sourceTower, destTower):
        if sourceTower.peek() < destTower.peek() or destTower.peek() is None:
            #pop from sourceTower and push into destTower
            return True
        elif sourceTower.peek() > destTower.peek():
            #return error message, do not pop from srcTower
            return False


class Hanoi:
    """GUI for animated towers-of-Hanoi-game with upto 10 discs:"""

    def displayMove(self, move):
        """method to be passed to the Hanoi-engine as a callback
        to report move-count"""
        self.moveCntLbl.configure(text="move:\n%d" % move)

    def adjust_nr_of_discs(self, e):
        """callback function for nr-of-discs-scale-widget"""
        self.hEngine.nrOfDiscs = self.discs.get()
        self.reset()

    def setState(self, STATE):
        """most simple implementation of a finite state machine"""
        self.state = STATE
        try:
            if STATE == "START":
                self.discs.configure(state=NORMAL)
                self.discs.configure(fg="black")
                self.discsLbl.configure(fg="black")
                self.resetBtn.configure(state=DISABLED)
                self.solveBtn.configure(text="solve", state=NORMAL)
            elif STATE == "RUNNING":
                self.discs.configure(state=DISABLED)
                self.discs.configure(fg="gray70")
                self.discsLbl.configure(fg="gray70")
                self.resetBtn.configure(state=NORMAL)
                self.solveBtn.configure(text="pause", state=NORMAL)
            elif STATE == "PAUSE":
                self.discs.configure(state=NORMAL)
                self.discs.configure(fg="black")
                self.discsLbl.configure(fg="black")
                self.resetBtn.configure(state=NORMAL)
                self.solveBtn.configure(text="resume", state=NORMAL)
            elif STATE == "DONE":
                self.discs.configure(state=NORMAL)
                self.discs.configure(fg="black")
                self.discsLbl.configure(fg="black")
                self.resetBtn.configure(state=NORMAL)
                self.solveBtn.configure(text="solve", state=DISABLED)
            elif STATE == "TIMEOUT":
                self.discs.configure(state=DISABLED)
                self.discs.configure(fg="gray70")
                self.discsLbl.configure(fg="gray70")
                self.resetBtn.configure(state=NORMAL)
                self.solveBtn.configure(state=DISABLED)
        except TclError:
            pass

    def reset(self):
        """restore state "START" for a new game"""
        self.hEngine.reset()
        self.setState("START")

    def solve(self):
        """callback function for start button, which also serves as
        pause button. Makes hEngine running until done or interrupted"""
        '''if self.state in ["START", "PAUSE"]:
            self.setState("RUNNING")
            if self.hEngine.run():
                self.setState("DONE")
            else:
                self.setState("PAUSE")
        elif self.state == "RUNNING":
            self.setState("TIMEOUT")
            self.hEngine.stop()'''

        '''elson code'''
        if self.hEngine.solve() is True:
            self.setState('DONE')
            self.myHighScore = self.hEngine.storeHighScore()
            self.updateHighScore(self.highScoreTable, self.myHighScore)



    def intialize(self, cv, nrOfDiscs, speed):
        cv = TurtleScreen(cv)
        self.hEngine = HanoiEngine(cv, nrOfDiscs, speed, self.displayMove)
        fnt = ("Arial", 12, "bold")
        fnt2 = ("Arial", 20, "bold")

        buttonTowerFrame = Frame(root)
        self.buttonTowerA = Button(buttonTowerFrame, width=7, text="Tower A", font=fnt,
                              state=NORMAL, padx=35, command=lambda:self.labelHitA(self.hEngine, self.buttonTowerA))
        self.buttonTowerB = Button(buttonTowerFrame, width=7, text="Tower B", font=fnt,
                              state=NORMAL, padx=35, command=lambda:self.labelHitB(self.hEngine, self.buttonTowerB))
        self.buttonTowerC = Button(buttonTowerFrame, width=7, text="Tower C", font=fnt,
                              state=NORMAL, padx=35, command=lambda:self.labelHitC(self.hEngine, self.buttonTowerC))
        for widget in  self.buttonTowerA, self.buttonTowerB, self.buttonTowerC :
            widget.pack(side=LEFT)
        buttonTowerFrame.pack(side=TOP)

        # set attributes: nr of discs, speed; display move count
        attrFrame = Frame(root)  # contains scales to adjust game's attributes
        self.discsLbl = Label(attrFrame, width=7, height=2, font=fnt,
                              text="discs:\n")
        self.discs = Scale(attrFrame, from_=1, to_=10, orient=HORIZONTAL,
                           font=fnt, length=75, showvalue=1, repeatinterval=10,
                           command=self.adjust_nr_of_discs)
        self.discs.set(nrOfDiscs)
        self.moveCntLbl = Label(attrFrame, width=5, height=2, font=fnt,
                                padx=20, text=" move:\n0", anchor=CENTER)
        for widget in ( self.discsLbl, self.discs,
                        self.moveCntLbl ):
            widget.pack(side=LEFT)
        attrFrame.pack(side=TOP)
        # control buttons: reset, step, start/pause/resume
        ctrlFrame = Frame(root)  # contains Buttons to control the game
        self.resetBtn = Button(ctrlFrame, width=11, text="reset", font=fnt,
                               state=DISABLED, padx=15, command=self.reset)
        self.solveBtn = Button(ctrlFrame, width=11, text="solve", font=fnt,
                               state=NORMAL, padx=15, command=self.solve)
        for widget in self.resetBtn, self.solveBtn:
            widget.pack(side=LEFT)
        ctrlFrame.pack(side=TOP)

        highScoreTextFrame = Frame(root)
        self.highScoreTextlabel = Label(highScoreTextFrame, width=20, height=1, font=fnt2,
                              text="My High Scores")
        self.highScoreTextlabel.pack(side=LEFT)
        highScoreTextFrame.pack(side=TOP)


        highScoreFrame = Frame(root)
        self.scrollbar = Scrollbar(highScoreFrame)
        self.scrollbar.pack( side = RIGHT, fill=Y )
        self.highScoreTable = Listbox(highScoreFrame, yscrollcommand = self.scrollbar.set)
        self.highScoreTable.pack( side = LEFT, fill = BOTH )
        self.scrollbar.config( command = self.highScoreTable.yview )
        for widget in self.highScoreTable, self.scrollbar:
            widget.pack(side=RIGHT)
        highScoreFrame.pack(side=TOP)



    def __init__(self, nrOfDiscs, speed):
        """construct Hanoi-engine, build GUI and set STATE to "START"
        then launch mainloop()"""

        root.title("TOWERS OF HANOI")
        cv = Canvas(root, width=800, height=240)
        cv.pack()

        self.myHighScore = []

        self.intialize(cv, nrOfDiscs, speed)

        self.state = "START"
        root.mainloop()

    def updateHighScore(self, highScoreTable, myHighScore):

        self.highScoreTable.delete(0, highScoreTable.size()+1)

        intListBoxEntry = 1

        for i in range(0, len(myHighScore)):
            highScoreTable.insert(intListBoxEntry, "discs: "+str(myHighScore[i].getNumOfDiscs())+" moves: "+str(myHighScore[i].getNumOfMove()))
            print str(intListBoxEntry)+" disc: "+str(self.myHighScore[i].getNumOfDiscs())+" move: "+str(self.myHighScore[i].getNumOfMove())
            intListBoxEntry += 1

        intListBoxEntry = 0



    def labelHitA(self, hEngine, object):
       if len(stepList) <= 1:
           object.config(state = 'disabled')
           self.buttonTowerA.update()
           stepList.append(hEngine.getTowerA())
           print "tower A hit"
           if len(stepList) == 2:
               if self.hEngine.checkvalid(stepList[0], stepList[1]) is True:
                   #hEngine.move(stepList[0], stepList[1])
                   print "A:", self.hEngine.towerA.size(), "value:", self.hEngine.towerA.peek()
                   print "B:", self.hEngine.towerB.size(), "value:", self.hEngine.towerB.peek()
                   print "C:", self.hEngine.towerC.size(), "value:", self.hEngine.towerC.peek()
                   del stepList[:]
                   object.config(state = 'normal')
                   self.buttonTowerA.update()
                   self.buttonTowerB.config(state = 'normal')
                   self.buttonTowerB.update()
                   self.buttonTowerC.config(state = 'normal')
                   self.buttonTowerC.update()
                   if hEngine.checkWin() is True:
                       self.setState('DONE')
                       self.myHighScore = hEngine.storeHighScore()
                       self.updateHighScore(self.highScoreTable, self.myHighScore)
               else:
                   del stepList[:]
                   object.config(state = 'normal')
                   self.buttonTowerA.update()
                   self.buttonTowerB.config(state = 'normal')
                   self.buttonTowerB.update()
                   self.buttonTowerC.config(state = 'normal')
                   self.buttonTowerC.update()


       elif len(stepList) == 2:
           hEngine.move(stepList[0], stepList[1])
           del stepList[:]



    def labelHitB(self, hEngine, object):
       if len(stepList) <= 1:
           object.config(state = 'disabled')
           self.buttonTowerB.update()
           stepList.append(hEngine.getTowerB())
           print "tower B hit"
           if len(stepList) == 2:
               if self.hEngine.checkvalid(stepList[0], stepList[1]) is True:
                   #hEngine.move(stepList[0], stepList[1])
                   print "A:", self.hEngine.towerA.size(), "value:", self.hEngine.towerA.peek()
                   print "B:", self.hEngine.towerB.size(), "value:", self.hEngine.towerB.peek()
                   print "C:", self.hEngine.towerC.size(), "value:", self.hEngine.towerC.peek()
                   del stepList[:]
                   object.config(state = 'normal')
                   self.buttonTowerB.update()
                   self.buttonTowerA.config(state = 'normal')
                   self.buttonTowerA.update()
                   self.buttonTowerC.config(state = 'normal')
                   self.buttonTowerC.update()
                   if hEngine.checkWin() is True:
                       self.setState('DONE')
                       self.myHighScore = hEngine.storeHighScore()
                       self.updateHighScore(self.highScoreTable, self.myHighScore)
               else:
                   del stepList[:]
                   object.config(state = 'normal')
                   self.buttonTowerB.update()
                   self.buttonTowerA.config(state = 'normal')
                   self.buttonTowerA.update()
                   self.buttonTowerC.config(state = 'normal')
                   self.buttonTowerC.update()

       elif len(stepList) == 2:
           hEngine.move(stepList[0], stepList[1])
           del stepList[:]



    def labelHitC(self, hEngine, object):
       if len(stepList) <= 1:
           object.config(state = 'disabled')
           self.buttonTowerC.update()
           stepList.append(hEngine.getTowerC())
           print "tower C hit"
           if len(stepList) == 2:
               if self.hEngine.checkvalid(stepList[0], stepList[1]) is True:
                   #hEngine.move(stepList[0], stepList[1])
                   print "A:", self.hEngine.towerA.size(), "value:", self.hEngine.towerA.peek()
                   print "B:", self.hEngine.towerB.size(), "value:", self.hEngine.towerB.peek()
                   print "C:", self.hEngine.towerC.size(), "value:", self.hEngine.towerC.peek()
                   del stepList[:]
                   object.config(state = 'normal')
                   self.buttonTowerC.update()
                   self.buttonTowerA.config(state = 'normal')
                   self.buttonTowerA.update()
                   self.buttonTowerB.config(state = 'normal')
                   self.buttonTowerB.update()
                   if hEngine.checkWin() is True:
                       self.setState('DONE')
                       #self.hEngine.storeHighScore()
                       self.myHighScore = hEngine.storeHighScore()
                       self.updateHighScore(self.highScoreTable, self.myHighScore)
               else:
                   del stepList[:]
                   object.config(state = 'normal')
                   self.buttonTowerC.update()
                   self.buttonTowerA.config(state = 'normal')
                   self.buttonTowerA.update()
                   self.buttonTowerB.config(state = 'normal')
                   self.buttonTowerB.update()

       elif len(stepList) == 2:
           hEngine.move(stepList[0], stepList[1])
           del stepList[:]








if __name__ == "__main__":
    Hanoi(3, 3)
