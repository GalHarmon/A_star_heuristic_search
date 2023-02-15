
import math
import copy
import queue
from queue import PriorityQueue

class boardObject:
    def __init__(self, dataval):
        self.dataval = dataval# 2d array that present the board
        self.gScore = None
        self.cameFrom = None # the object of the "father"
        self.fScore = None
        self.hScore = None

    def __lt__(self, _):  # implement of operator
        return True

def find_path(startingBoard, goalBoard, search_method, detail_output):
    if search_method == 1 and not detail_output:
        printWithNoHeuristic(startingBoard, goalBoard)
    elif search_method == 1 and detail_output:
        printWithHeuristic(startingBoard, goalBoard)

def printWithHeuristic(startingBoard,goalBoard):
    sb = boardObject(startingBoard)
    path = A_Star(sb, goalBoard)
    if len(path) == 0:
        print("No path found.")
    else:
        counter = 1
        for board in path:
            if board.dataval == startingBoard:
                print("Board 1 (starting position):")
                print2dArray(board.dataval)
            elif board.dataval == goalBoard:
                print("Board " + str(counter) + " (goal position):")
                print2dArray(board.dataval)
                print("Heuristic: " + str(board.hScore))
            else:
                print("Board " + str(counter) + ":")
                print2dArray(board.dataval)
                print("Heuristic: " + str(board.hScore))
                print("-----")
            counter += 1

def printWithNoHeuristic(startingBoard,goalBoard):
    sb = boardObject(startingBoard)
    path = A_Star(sb, goalBoard)
    if len(path) == 0:
        print("No path found.")
    else:
        counter = 1
        for board in path:
            if board.dataval == startingBoard:
                print("Board 1 (starting position):")
                print2dArray(board.dataval)
            elif board.dataval == goalBoard:
                print("Board " + str(counter) + " (goal position):")
                print2dArray(board.dataval)
            else:
                print("Board " + str(counter) + ":")
                print2dArray(board.dataval)
                print("-----")
            counter += 1


def reconstruct_path(current): # recursive function that return a list of the path
    if current is not None:
        return reconstruct_path(current.cameFrom) + [current]
    else:
        return []

def A_Star(startingBoard, goalBoard):
    visited = []
    oppnSetOnlyVal = []# only for the value of the 2darray that present the board
    openSet = queue.PriorityQueue()
    startingBoard.gScore = 0
    startingBoard.hScore = findHeuristic(startingBoard.dataval, goalBoard)
    startingBoard.fScore = startingBoard.hScore # because the g of the start board is 0
    openSet.put((startingBoard.fScore, startingBoard.hScore, startingBoard))#add to the PriorityQueue the starting board element
    oppnSetOnlyVal.append(startingBoard.dataval)
    while openSet.qsize() > 0 and len(visited) <= len(startingBoard.dataval)*len(startingBoard.dataval[0]*100):
        temp = openSet.get()# get the elemnt with the lowest f score (if there more than 1 element with the same f score it will tkae the lowest h score between them)
        current = temp[2]# every elemnt include tuple of 3 elements
        oppnSetOnlyVal.remove(current.dataval)
        visited.append(current.dataval)
        if ifEquals(current.dataval, goalBoard):
            return reconstruct_path(current)
        myNeighbor = findAllOptions(current.dataval)
        for neighbor in myNeighbor:
            if not ifInList(neighbor.dataval, oppnSetOnlyVal) and not ifInList(neighbor.dataval, visited):
                neighbor.gScore = current.gScore + 1
                neighbor.cameFrom = current
                neighbor.hScore = findHeuristic(neighbor.dataval, goalBoard)
                neighbor.fScore = neighbor.gScore + neighbor.hScore
                openSet.put((neighbor.fScore, neighbor.hScore, neighbor))
                oppnSetOnlyVal.append(neighbor.dataval)
            elif ifInList(neighbor.dataval, oppnSetOnlyVal):
                neighbor.gScore = current.gScore + 1
                if neighbor.gScore < getTheEqualObjectFromOpenSet(openSet, neighbor.dataval).gScore:
                    neighbor.cameFrom = current
                    neighbor.hScore = findHeuristic(neighbor.dataval, goalBoard)
                    neighbor.fScore = neighbor.gScore + neighbor.hScore
                    openSet = swapTheObjects(openSet, neighbor)
    return []

def getTheEqualObjectFromOpenSet (openSet, neighbor2Darray):#retirn the object that hava the same dataval as neighbor
    tempList = list(openSet.queue)
    for x in tempList:
        if ifEquals(x[2].dataval, neighbor2Darray):
            return x[2]

def swapTheObjects(openSet, neighbor):# swap the objects with the same dataval but the g score of the neighbor lower then the same dataval in the openset
    tempList = list(openSet.queue)
    for x in tempList:
        if ifEquals(x[2].dataval, neighbor.dataval):
            tempIndex = tempList.index(x)
            del tempList[tempIndex]
            tempList.append((neighbor.fScore, neighbor.hScore, neighbor))
            tempPriorityQueue = queue.PriorityQueue()
            for y in tempList:
                tempPriorityQueue.put(y)
            return tempPriorityQueue


def ifInList(twoDarray, listOfArrays):
    for x in listOfArrays:
        if ifEquals(x, twoDarray):
            return True
    return False

def ifEquals(array1, array2):
    for i in range(len(array1)):
        for j in range(len(array1[0])):
            if array1[i][j] != array2[i][j]:
                return False
    return True

def findHeuristic(optionBoard, goalBoard): # find the value by absoulot distance between the agents in the current board to the agents in the goal boardי
    targets = findAgentLocation(goalBoard)# return tuple of pair index of the agents
    current = findAgentLocation(optionBoard)
    heuristicValue = 0
    if len(targets) < len(current):
        numOfDropAgent = len(current)-len(targets)
        for x in range(numOfDropAgent):
            targets.append((0,len(optionBoard))) # add new "targets"
    if len(current) < len(targets) or len(current) == 0:
        return math.inf
    for m in current:
        tempForDis = []  # list of the distance of the agent from every target
        for n in targets:
            if n[1] == len(optionBoard):
                tempNum = (abs(m[0] - len(optionBoard)))
            else:
                tempNum = abs(m[0]-n[0]) + abs((m[1]-n[1]))
            tempForDis.append(tempNum)
        heuristicValue = heuristicValue + min(tempForDis)# Add the min value for the whole heuristic
        minIndex = tempForDis.index(min(tempForDis)) #delete the "match" variable
        del targets[minIndex]
    return heuristicValue

def findAllOptions(startingBoard):
    optionsList = []
    for i in range(len(startingBoard)):
        for j in range(len(startingBoard[0])):
            if startingBoard[i][j] == 2: # add all the valid neibhor of that board
                if i > 0 and startingBoard[i-1][j] == 0:
                    dataval = copy.deepcopy(startingBoard)
                    dataval[i-1][j] = 2
                    dataval[i][j] = 0
                    tempBoard = boardObject(dataval)
                    optionsList.append(tempBoard)
                if i < len(startingBoard)-1 and startingBoard[i+1][j] == 0:
                    dataval = copy.deepcopy(startingBoard)
                    dataval[i+1][j] = 2
                    dataval[i][j] = 0
                    tempBoard = boardObject(dataval)
                    optionsList.append(tempBoard)
                if j > 0 and startingBoard[i][j-1] == 0:
                    dataval = copy.deepcopy(startingBoard)
                    dataval[i][j-1] = 2
                    dataval[i][j] = 0
                    tempBoard = boardObject(dataval)
                    optionsList.append(tempBoard)
                if j < len(startingBoard)-1 and startingBoard[i][j+1] == 0:
                    dataval = copy.deepcopy(startingBoard)
                    dataval[i][j+1] = 2
                    dataval[i][j] = 0
                    tempBoard = boardObject(dataval)
                    optionsList.append(tempBoard)
                if i == len(startingBoard)-1:
                    dataval = copy.deepcopy(startingBoard)
                    dataval[i][j] = 0
                    tempBoard = boardObject(dataval)
                    optionsList.append(tempBoard)
    return optionsList


def findAgentLocation(Board):
    myTarget = []
    for i in range(len(Board)):
        for j in range(len(Board[0])):
            if Board[i][j] == 2:
                myTarget.append((i, j))
    return myTarget

def print2dArray(theArray):
    print ('  1 2 3 4 5 6')
    for i, r in enumerate(theArray):
        print(f"{i+1}:", end='')
        for c in r:
            if c == 0:
                print("  ", end='')
            elif c == 1:
                print("@ ", end='')
            elif c == 2:
                print ("* ", end='')
        print()

