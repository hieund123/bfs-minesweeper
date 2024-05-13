import random
import eel
from collections import deque

class boardSpot(object):
    value = 0
    selected = False
    mine = False

    def __init__(self):
        self.selected = False

    def __str__(self):
        return str(boardSpot.value)

    def isMine(self):
        if boardSpot.value == -1:
            return True
        return False


class boardClass(object):
    def __init__(self, m_boardSize, m_numMines):
        self.board = [[boardSpot() for i in range(m_boardSize)]
                      for j in range(m_boardSize)]
        self.boardSize = m_boardSize
        self.numMines = m_numMines
        self.selectableSpots = m_boardSize * m_boardSize - m_numMines
        i = 0
        while i < m_numMines:
            x = random.randint(0, self.boardSize-1)
            y = random.randint(0, self.boardSize-1)
            if not self.board[x][y].mine:
                self.addMine(x, y)
                i += 1
            else:
                i -= 1

    def __str__(self):
        returnString = ""
        for y in range(0, self.boardSize):
            # returnString += str(y)
            for x in range(0, self.boardSize):
                if self.board[x][y].mine and self.board[x][y].selected:
                    returnString += 'B'

                    # returnString += str(self.board[x][y].value)
                elif self.board[x][y].selected:
                    returnString += str(self.board[x][y].value)
                else:  # empthy cell
                    returnString += "E"
        return returnString

    def addMine(self, x, y):
        self.board[x][y].value = -1
        self.board[x][y].mine = True
        for i in range(x-1, x+2):
            if i >= 0 and i < self.boardSize:
                if y-1 >= 0 and not self.board[i][y-1].mine:
                    self.board[i][y-1].value += 1
                if y+1 < self.boardSize and not self.board[i][y+1].mine:
                    self.board[i][y+1].value += 1
        if x-1 >= 0 and not self.board[x-1][y].mine:
            self.board[x-1][y].value += 1
        if x+1 < self.boardSize and not self.board[x+1][y].mine:
            self.board[x+1][y].value += 1

    def makeMove(self, x, y):
        self.board[x][y].selected = True
        self.selectableSpots -= 1
        if self.board[x][y].value == -1:
            return False
        if self.board[x][y].value == 0:
            for i in range(x-1, x+2):
                if i >= 0 and i < self.boardSize:
                    if y-1 >= 0 and not self.board[i][y-1].selected:
                        self.makeMove(i, y-1)
                    if y+1 < self.boardSize and not self.board[i][y+1].selected:
                        self.makeMove(i, y+1)
            if x-1 >= 0 and not self.board[x-1][y].selected:
                self.makeMove(x-1, y)
            if x+1 < self.boardSize and not self.board[x+1][y].selected:
                self.makeMove(x+1, y)
            return True
        else:
            return True

    def hitMine(self, x, y):
        return self.board[x][y].value == -1

    def isWinner(self):
        return self.selectableSpots == 0

    def solveBoard(self, x, y):
        queue = deque([(x, y)])
        while queue:
            x, y = queue.popleft()
            if not self.board[x][y].selected and self.board[x][y].value != -1:
                self.board[x][y].selected = True
                if self.board[x][y].value == 0:
                    for i in range(x-1, x+2):
                        for j in range(y-1, y+2):
                            if 0 <= i < self.boardSize and 0 <= j < self.boardSize and not self.board[i][j].selected:
                                queue.append((i, j))

        return str(self)

    def getFirstMove(self):
        x, y = random.randint(0, self.boardSize-1), random.randint(0, self.boardSize-1)
        while self.board[x][y].selected or self.board[x][y].value == -1:
            x, y = random.randint(0, self.boardSize-1), random.randint(0, self.boardSize-1)
        return str(x) + "-" + str(y)

    def getRemainingCells(self):
        count = 0
        for i in range(self.boardSize):
            for j in range(self.boardSize):
                if not self.board[i][j].selected and self.board[i][j].value != -1:
                    count += 1
        return count

#### For UI ####
eel.init('.//UI')  # path of the webpage folder

GO_IN = False
GAME_OVER = False
WINNER = False
BOARD = ""


@eel.expose
def clickedOnTheCell(x, y):
    global GO_IN
    global GAME_OVER, WINNER
    GO_IN = not GO_IN
    if GO_IN:
        BOARD.makeMove(x, y)
        GAME_OVER = BOARD.hitMine(x, y)
        if BOARD.isWinner() and GAME_OVER == False:
            GAME_OVER = True
            WINNER = True
            print("Won")
        if GAME_OVER and not WINNER:
            print("Game Over")
        GO_IN = not GO_IN
        # print(BOARD)  # return board to js
        return str(BOARD)


@eel.expose
def makeBoard(boardSize, numMines):
    global BOARD
    del BOARD
    BOARD = boardClass(boardSize, numMines)
@eel.expose
def solveBoard(x, y):
    return str(BOARD.solveBoard(x, y))

@eel.expose
def getFirstMove():
    return BOARD.getFirstMove()

@eel.expose
def getRemainingCells():
    return BOARD.getRemainingCells()

web_app_options = {
    "mode": "chrome",
    "port": 8080,
    'chromeFlags': ["--start-fullscreen"]
}

eel.start('index.html', options=web_app_options, suppress_error=True)