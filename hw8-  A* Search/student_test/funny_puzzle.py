import numpy as np
import heapq

goal = np.reshape(np.array([1, 2, 3, 4, 5, 6, 7, 8, 0]), (3, 3))


def print_succ(state):
    state = np.array(state)
    state = np.reshape(state, (3, 3))
    successors = []
    zeroRow = np.where(state == 0)[0][0]
    zeroCol = np.where(state == 0)[1][0]
    tempSucc = np.copy(state)
    if zeroRow - 1 >= 0:  # up
        temp = tempSucc[zeroRow - 1][zeroCol]
        tempSucc[zeroRow - 1][zeroCol] = tempSucc[zeroRow][zeroCol]
        tempSucc[zeroRow][zeroCol] = temp
        successors.append(tempSucc.flatten().tolist())
        tempSucc = np.copy(state)
    if zeroRow + 1 < 3:  # down
        temp = tempSucc[zeroRow + 1][zeroCol]
        tempSucc[zeroRow + 1][zeroCol] = tempSucc[zeroRow][zeroCol]
        tempSucc[zeroRow][zeroCol] = temp
        successors.append(tempSucc.flatten().tolist())
        tempSucc = np.copy(state)
    if zeroCol - 1 >= 0:  # left
        temp = tempSucc[zeroRow][zeroCol - 1]
        tempSucc[zeroRow][zeroCol - 1] = tempSucc[zeroRow][zeroCol]
        tempSucc[zeroRow][zeroCol] = temp
        successors.append(tempSucc.flatten().tolist())
        tempSucc = np.copy(state)
    if zeroCol + 1 < 3:  # right
        temp = tempSucc[zeroRow][zeroCol + 1]
        tempSucc[zeroRow][zeroCol + 1] = tempSucc[zeroRow][zeroCol]
        tempSucc[zeroRow][zeroCol] = temp
        successors.append(tempSucc.flatten().tolist())
    successors = sorted(successors)
    for i in successors:
        print(str(i) + " h=" + str(heuristic(np.reshape(np.array(i), (3, 3)))))


def heuristic(state):
    sumManhattan = 0
    for r in range(3):
        for c in range(3):
            if not state[r][c] == goal[r][c] and not state[r][c] == 0:  # gets out of place !0 numbers
                sumManhattan += abs(r - np.where(goal == state[r][c])[0][0]) + abs(
                    c - np.where(goal == state[r][c])[1][0])
    return sumManhattan


def solve(state):
    openSet = []
    closedSet = []
    closedStates = set()
    p = -1
    heapq.heappush(openSet, (
        heuristic(np.reshape(np.array(state), (3, 3))), state, (0, heuristic(np.reshape(np.array(state), (3, 3))), p)))
    while len(openSet) > 0:
        curNode = heapq.heappop(openSet)
        curG = curNode[2][0]
        closedSet.append(curNode)
        closedStates.add(tuple(curNode[1]))  # use tuple so it's hashable
        ''' Original author: Roman Bodnarchuk
            Source: https://stackoverflow.com/questions/7027199/hashing-arrays-in-python
            The idea to change a list to a tuple in order to make it hashable for the set
        '''
        if np.array_equal(np.reshape(np.array(curNode[1]), (3, 3)), goal):  # check for goal
            break
        for i in getSuccessors(curNode[1]):
            if tuple(i) not in closedStates:
                heapq.heappush(openSet, (curG + 1 + heuristic(np.reshape(np.array(i), (3, 3))), i, (curG + 1,
                                heuristic(np.reshape(np.array(i), (3, 3))), len(closedSet) - 1)))
    path = []
    parent = closedSet[len(closedSet) - 1][2][2]
    path.append(closedSet[len(closedSet) - 1])
    while parent > -1:
        cur = parent
        parent = closedSet[cur][2][2]
        path.append(closedSet[cur])
    moves = 0
    path.reverse()
    for i in path:
        print("{curNodeState} h={h} moves: {moves}".format(curNodeState=i[1], h=i[2][1], moves=moves))
        moves += 1


def getSuccessors(state):
    state = np.array(state)
    state = np.reshape(state, (3, 3))
    successors = []
    zeroRow = np.where(state == 0)[0][0]
    zeroCol = np.where(state == 0)[1][0]
    tempSucc = np.copy(state)
    if zeroRow - 1 >= 0:  # up
        temp = tempSucc[zeroRow - 1][zeroCol]
        tempSucc[zeroRow - 1][zeroCol] = tempSucc[zeroRow][zeroCol]
        tempSucc[zeroRow][zeroCol] = temp
        successors.append(tempSucc.flatten().tolist())
        tempSucc = np.copy(state)
    if zeroRow + 1 < 3:  # down
        temp = tempSucc[zeroRow + 1][zeroCol]
        tempSucc[zeroRow + 1][zeroCol] = tempSucc[zeroRow][zeroCol]
        tempSucc[zeroRow][zeroCol] = temp
        successors.append(tempSucc.flatten().tolist())
        tempSucc = np.copy(state)
    if zeroCol - 1 >= 0:  # left
        temp = tempSucc[zeroRow][zeroCol - 1]
        tempSucc[zeroRow][zeroCol - 1] = tempSucc[zeroRow][zeroCol]
        tempSucc[zeroRow][zeroCol] = temp
        successors.append(tempSucc.flatten().tolist())
        tempSucc = np.copy(state)
    if zeroCol + 1 < 3:  # right
        temp = tempSucc[zeroRow][zeroCol + 1]
        tempSucc[zeroRow][zeroCol + 1] = tempSucc[zeroRow][zeroCol]
        tempSucc[zeroRow][zeroCol] = temp
        successors.append(tempSucc.flatten().tolist())
    successors = sorted(successors)
    return successors
