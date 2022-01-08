import numpy as np 
import random
import boardpy
import copy
import pickle
import Pipeline
from queue import Queue
import ValNetwork

class TreeNode(object):
    def __init__(self, board, p, self_pos, parent = None, self_player = 1):
        self.parent = parent
        self.children = {}
        self.board = copy.deepcopy(board)
        self.pos = self_pos
        self.player = self_player # {1, -1}
        self.n = 0
        self.w = 0
        self.q = 0
        self.p = p
        self.cProduct = 1.414

    def Expand(self, prob):
        # REQUIRES: should in advance ensure that the game hasn't end, i.e. board not full && no one has won the game
        
        if (self.board.oneSideNeedPass(-self.player)):
            tmpboard = copy.deepcopy(self.board)
            self.children[-1] = TreeNode(tmpboard, 1, [-1, -1], self, -self.player)
        else:
            sumP = 0
            for i in range(0, self.board.width):
                for j in range(0, self.board.width):
                    if (self.board.canPositionOn(i, j, -self.player)):
                        sumP += prob[i * self.board.width + j]

            for i in range(0, self.board.width):
                for j in range(0, self.board.width):
                    if (self.board.canPositionOn(i, j, -self.player)):
                        tmpboard = copy.deepcopy(self.board)
                        # tmpboard.grid[i][j] = -self.player
                        tmpboard.positioning(i, j, -self.player)
                        self.children[i * self.board.width + j] = TreeNode(tmpboard, prob[i * self.board.width + j] / sumP, [i, j], self, -self.player)


    def Select(self):
        # REQUIRES: The node is not a leaf. 
        # EFFECTS: Returning the chosen way to play the game based on UCT
        return max(self.children.items(), key = lambda child: child[1].getUCT())

    def getUCT(self):
        return self.q + self.cProduct * self.p * np.sqrt(self.parent.n) / (self.n + 1)

    def update(self, val):
        if (self.isRoot() == False):
            self.parent.update(-val)
        self.w += val
        self.n += 1
        self.q = self.w / self.n

    def isRoot(self):
        return self.parent == None
    
    def isLeaf(self):
        return len(self.children) == 0
        
class MCTS(object):
    def __init__(self, budget = 400, root_self_player = -1, root_board = None):
        if (root_board == None):
            tmpboard = boardpy.Board()
        else:
            tmpboard = copy.deepcopy(root_board)
        self.root = TreeNode(tmpboard, 1, [-1, -1], None, root_self_player)
        self.budget = budget

    def grid2List(self, node):
        gridPlayer = np.zeros((node.board.width, node.board.width), dtype=int)
        gridOppo = np.zeros((node.board.width, node.board.width), dtype=int)
        for i in range(self.root.board.width):
            for j in range(self.root.board.width):
                if (node.board.grid[i][j] == node.player):
                    gridPlayer[i][j] = 1
                elif (node.board.grid[i][j] == -node.player):
                    gridOppo[i][j] = 1
        if (node.player == 1):
            colorGrid = np.ones((node.board.width, node.board.width), dtype=int)
        else:
            colorGrid = np.zeros((node.board.width, node.board.width), dtype=int)
        lastStep = np.zeros((node.board.width, node.board.width), dtype=int)
        if (node.pos[0] >= 0 and node.pos[1] >= 0):
            lastStep[node.pos[0]][node.pos[1]] = 1
        return [gridPlayer, gridOppo, lastStep, colorGrid]

    def Playout(self, network):
        for _ in range(0, self.budget):
            node = self.root
            while (node.isLeaf() == False):
                node = node.Select()[1]
            if (node.board.isTerminated() == -2): # not terminated
                x = self.grid2List(node)
                prob, val = network.GetProbVal(x)
                prob = prob[0]
                val = val[0][0]
                node.Expand(prob)
                # Prediction from the Model, getting val
            else:
                if (node.board.isTerminated() == node.player):
                    val = 1
                elif (node.board.isTerminated() == -node.player):
                    val = -1
                else:
                    val = 0
            node.update(val)
        #print("Playout ends")

    def getData(self):
        # EFFECTS: return (s, pi, z = 0). z = 0 since in the gaming process we don't know the result of game. 
        gridPlayer = np.zeros((self.root.board.width, self.root.board.width), dtype=int)
        gridOppo = np.zeros((self.root.board.width, self.root.board.width), dtype=int)
        lastStep = np.zeros((self.root.board.width, self.root.board.width), dtype = int)
        pi = []
        if (self.root.board.oneSideNeedPass(-self.root.player) == True):
            pi.append(1)
        else:
            pi.append(0)
        for i in range(0, self.root.board.width):
            for j in range(0, self.root.board.width):
                if (self.root.board.grid[i][j] == self.root.player):
                    gridPlayer[i][j] = 1
                    pi.append(0)
                elif (self.root.board.grid[i][j] == -self.root.player):
                    gridOppo[i][j] = 1
                    pi.append(0)
                else:
                    if (i * self.root.board.width + j in self.root.children.keys()):
                        pi.append(self.root.children[i * self.root.board.width + j].n / self.root.n)
                    else:
                        pi.append(0)
        if (self.root.pos[0] != -1 or self.root.pos[1] != -1):
            lastStep[self.root.pos[0]][self.root.pos[1]] = 1

        return Pipeline.NetworkInput(gridPlayer, gridOppo, lastStep, self.root.player, pi)



