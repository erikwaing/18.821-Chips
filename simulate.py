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
    print "Done: took %d actions" % count

def actAndSee(board):
    while 1:
        act(board)
        printBoard(board)
        input = raw_input()

