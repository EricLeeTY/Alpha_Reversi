import ValNetwork
import boardpy
import keras
import MCTS
import copy
import numpy as np

def grid2List(board, player):
    gridPlayer = np.zeros((board.width, board.width), dtype=int)
    gridOppo = np.zeros((board.width, board.width), dtype=int)
    for i in range(6):
        for j in range(6):
            if (board.grid[i][j] == player):
                gridPlayer[i][j] = 1
            elif (board.grid[i][j] == -player):
                gridOppo[i][j] = 1
    if (player == 1):
        colorGrid = np.ones((board.width, board.width), dtype=int)
    else:
        colorGrid = np.zeros((board.width, board.width), dtype=int)
    return [gridPlayer, gridOppo, colorGrid]

if __name__ == "__main__":
    net1 = ValNetwork.DLModel(6, 4)
    net2 = ValNetwork.DLModel(6, 4)
    model1 = net1.model
    model2 = net2.model
    model1.load_weights("modelGomoku2_5iar_6t6.h5")
    model2.load_weights("modelGomoku2_5iar_6t6.h5")
    playBoard = boardpy.Board()
    rounds = 0
    mcts1 = MCTS.MCTS(400, -1)
    mcts2 = MCTS.MCTS(400, -1)
    mcts1.Playout(net1)
    mcts2.Playout(net2)

    model1pos = 1
    model2pos = -model1pos
    if (model1pos == 1):
        remainder = 0
    else:
        remainder = 1

    while (playBoard.isTerminated() == -2):
        print("round : {}".format(rounds))
        print(playBoard.grid)
        x = input()
        print("----------------------------------")
        if (rounds % 2 == remainder):
            mcts1.Playout(net1)
            maxProb = -1000
            maxChild = None
            for child in mcts1.root.children.items():
                if (child[1].getUCT() > maxProb or maxChild == None):
                    maxProb = child[1].getUCT()
                    maxChild = child[1]
            maxi, maxj = maxChild.pos
            mcts1.root = maxChild
            print("AI1 pos at {}, {}".format(maxi, maxj))
            playBoard.grid[maxi][maxj] = model1pos

            isChild = False
            for child in mcts2.root.children.items():
                if ((playBoard.grid == child[1].board.grid).all()):
                    mcts2.root = child[1]
                    isChild = True
                    break
            if (isChild == False):
                print("nonono")
                exit()
        else:
            mcts2.Playout(net2)
            maxProb = -1000
            maxChild = None
            for child in mcts2.root.children.items():
                if (child[1].getUCT() > maxProb or maxChild == None):
                    maxProb = child[1].getUCT()
                    maxChild = child[1]
            maxi, maxj = maxChild.pos
            mcts2.root = maxChild
            print("AI2 pos at {}, {}".format(maxi, maxj))
            playBoard.grid[maxi][maxj] = model2pos

            isChild = False
            for child in mcts1.root.children.items():
                if ((playBoard.grid == child[1].board.grid).all()):
                    mcts1.root = child[1]
                    isChild = True
                    break
            if (isChild == False):
                print("nonono")
                exit()

        print("----------------------------------")
        rounds += 1
    print(playBoard.grid)
        
    
    
    


    

    