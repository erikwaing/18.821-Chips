import copy

board = {}
directions = [(1, 0), (0, 1), (-1, 0), (0, -1)]

def act(board):
    newboards = []
    something_changed = False
    for sloc in board.keys():
        (temp, changed) = actLocation(board, sloc)
        newboards.append(temp)
        something_changed = something_changed or changed
    updateBoard(board, newboards)
    return something_changed

def actLocation(board, sloc):
    newboard = {}
    (x,y) = sloc
    something_changed = False
    if board[sloc] >= 4:
        for dir in directions:
            newx = x + dir[0]
            newy = y + dir[1]
            newboard[(newx,newy)] = 1
        something_changed = True
        newboard[sloc] = -4
    return (newboard, something_changed)

def updateBoard(board, newboards):
    for b in newboards:
        for key in b.keys():
            try:
                board[key] += b[key]
            except KeyError:
                board[key] = b[key]

def getBoundary(board):
    allX = [x for (x,y) in board.keys()]
    allY = [y for (x,y) in board.keys()]
    lowestX = min(allX)
    highestX = max(allX)
    lowestY = min(allY)
    highestY = max(allY)
    return (lowestX, highestX, lowestY, highestY)

def getStableBoundry(board):
    actUntilStable(board)
    return getBoundary(board)

def getStableBoundryDistance(n):
    board = {(0,0):n}
    return getStableBoundry(board)[1]

def printBoundary(board):
    (lowestX, highestX, lowestY, highestY) = getBoundary(board)
    print "Boundary: X:[%d, %d] \tY:[%d, %d]" % (lowestX, highestX, lowestY, lowestY)

def printBoard(board):
    lowestX, highestX, lowestY, highestY = getBoundary(board)
    for y in range(lowestY, highestY+1):
        line = ''
        for x in range(lowestX, highestX+1):
            try:
                line += '| \t' + str(board[(x, y)]) + '\t'
            except KeyError:
                line += '| \t' + str(0) + '\t'
        print line
    
def actUntilStable(board):
    count = 0
    while act(board):
        count += 1
    return count

def actUntilStableCountingCenter(n):
    count = 0
    board = {(0,0):n}
    while act(board):
        if board[(0,0)] >= 4:
            count += 1
    return count

def actUntilStableCountingPosition(n, positions):
    counts = {}
    for p in positions:
        counts[p] = 0
    board = {(0,0): n}
    while act(board):
        for pos in positions:
            try:
                if board[pos] >= 4:
                    counts[pos] += 1
            except KeyError:
                print 'badaccess'
    return counts

import matplotlib as mpl
import pylab
import math

def seeRelationshipBetweenSquares(n):
    x = range(2, int(math.log(n)/math.log(4)))
    positions = [(i, 0) for i in x]
    counts = actUntilStableCountingPosition(n, positions)
    y = [counts[(i, 0)]*i/math.log(i) for i in x if i != 0]
    mpl.pyplot.scatter(x,y)
    mpl.pyplot.show()

def actAndSee(board):
    while 1:
        act(board)
        printBoard(board)
        input = raw_input()

import Image,ImageDraw
from random import randint as rint
import pylab as pl

def drawBoard(board, xrange, yrange, maxValue, recomputeMax=False, showActive=False):
    if recomputeMax:
        maxValue = max(board.values())
    img = Image.new("RGB", (xrange, yrange), "#FFFFFF")
    draw = ImageDraw.Draw(img)
    dr = 255./(maxValue/3. + 0.001)
    dg = 255./(maxValue/3. + 0.001)
    db = 255./(maxValue/3. + 0.001)
    for i in range(xrange):
        for j in range(yrange):
            try:
                point = board[(i - xrange/2, j - yrange/2)]
            except KeyError:
                point = 0
            r, g, b = point*dr, 0, 0
            if point >= 4 and showActive:
                r, g, b = 0, 255, 0
            if point > 1:
                g = 100
            if r > 255:
                r = 255
                g = point*dg
                if g > 255:
                    g = 255
                    b = point*db
            draw.point((i,j), fill=(int(r),int(g),int(b)))
    return img

def showImage(board, xrange, yrange, wait=False, showActive=False):
    maxValue = max(board.values())
    img = drawBoard(board, xrange, yrange, maxValue, showActive=showActive)
    img = pl.imshow(img)
    pl.pause(0.02)
    pl.draw()
    changed = True
    raw_input()
    while changed:
        changed = act(board)
        img = drawBoard(board, xrange, yrange, maxValue, True, showActive=showActive)
        pl.imshow(img)
        if not wait:
            pl.pause(0.02)
        pl.draw()
    #    if wait:
    #        raw_input()
    print "Done"

def wire(x,y):
    if y == 0:
        return 3
    else: 
        return 0

def showWireActing():
    board = {}
    for x in range(-10, 10):
        for y in range(-5, 5):
            board[(x,y)] = wire(x,y)
    board[(-10, 0)] = 4
    showImage(board, 22, 10, True, True)

def sync(x,y):
    if (x,y) == (0, -2):
        return 3
    if (x,y) == (-9, 2):
        return 4
    if (x,y) == (-4, 0):
        return 4
    if (x,y) == (0,0):
        return 1
    if x == 4 and y < 1 and y >= -2:
        return 3
    if (x,y) == (0, -2) or (x,y) == (2,-2):
        return 3
    if (x,y) == (0, 1) or (x,y) == (2, 1):
        return 3
    if (x,y) == (0, -1):
        return 3
    if y == 2:
        return 3
    if y == 0 and x > -4:
        return 3
    else:
        return 0

def showSynchronizer():
    board = {}
    for x in range(-10, 5):
        for y in range(-3, 4):
            board[(x,y)] = sync(x,y)
    showImage(board, 20, 8, True, True)

gatetemp = { (-7, 0): 3, (-6, 0): 3, (-5, 0): 3, (-4, 0): 3, (-3, 0): 3, (-2, 0): 3, (-1, 0): 3, (0, 0):2,
         (0, -1): 3, (1, -1): 3, (2, -1): 3,
         (-2, 1): 3, (0, 1): 3, (1, 1): 3, (2, 1): 4,
         (-3, 2): 3, (-2, 2): 2, (-1, 2): 3,
         (-3, 3): 3, (-1, 3): 3,
         (-3, 4): 4, (-1, 4): 3
}

def showORGate(bit1, bit2):
    gate = copy.deepcopy(gatetemp)
    gate[(-2, 0)] = 3
    if bit1 == True:
        gate[(-1, 4)] = 4
    if bit2 == True:
        gate[(2, -1)] = 4
    showImage(gate, 14, 12, True, True)

def showANDGate(bit1, bit2):
    gate = copy.deepcopy(gatetemp)
    gate[(-2, 0)] = 2
    if bit1 == True:
        gate[(-1, 4)] = 4
    if bit2 == True:
        gate[(2, -1)] = 4
    showImage(gate, 14, 12, True, True)

def present():
    showImage({(0,0):30}, 10, 10)
    print "Press to go on"
    raw_input()
    showImage({(0,0):100}, 15, 15)
    print "Press to go on"
    raw_input()
    showWireActing()
    print "Press to go on"
    raw_input()
    showSynchronizer()
    raw_input()
    showORGate(True, False)
    showORGate(False, False)
    print "Press to go on"
    raw_input()
    showANDGate(True, False)
    showANDGate(True, True)
