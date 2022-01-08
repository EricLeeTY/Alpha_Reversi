import ValNetwork
import boardpy
import keras
import MCTS
import copy
import numpy as np

def grid2List(board, player):
    gridPlayer = np.zeros((board.width, board.width), dtype=int)
    gridOppo = np.zeros((board.width, board.width), dtype=int)
    for i in range(8):
        for j in range(8):
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
    net = ValNetwork.DLModel(6, 4)
    model = net.model
    model.load_weights("Reversi30_rounds.h5")
    playBoard = boardpy.Board()
    row = 0
    col = 0
    myturn = -1
    modelturn = -myturn
    if (myturn == -1):
        remainder = 1
    else:
        remainder = 0

    rounds = 0
    mcts = MCTS.MCTS(400, -1)
    mcts.Playout(net)
    while (playBoard.isTerminated() == -2):
        print("round : {}".format(rounds))
        print("----------------------------------")
        print(playBoard.grid)
        if (rounds % 2 == remainder):
            if (not playBoard.oneSideNeedPass(myturn)):
                print("Please input row * col: ")
                while (playBoard.canPositionOn(row, col, myturn) == False):
                    row = int(input("row:"))
                    col = int(input("col:"))
                playBoard.positioning(row, col, myturn)
            
            isChild = False
            for child in mcts.root.children.items():
                print("---------------------------------------------------")
                print(playBoard.grid)
                print(child[1].board.grid)
                print("---------------------------------------------------")

                if ((playBoard.grid == child[1].board.grid).all()):
                    mcts.root = child[1]
                    isChild = True
                    break
            if (isChild == False):
                print("nonono")
        else:
            mcts.Playout(net)
            maxProb = -1000
            maxChild = None
            ucts = []
            for child in mcts.root.children.items():
                if (child[1].getUCT() > maxProb or maxChild == None):
                    maxProb = child[1].getUCT()
                    maxChild = child[1]
                ucts.append([child[1].pos, child[1].getUCT()])
            maxi, maxj = maxChild.pos
            mcts.root = maxChild
            print("UCTs:")
            print(ucts)
            print("AI pos at {}, {}".format(maxi, maxj))
            playBoard.positioning(maxi, maxj, modelturn)
            # print(playBoard.grid)

        print("----------------------------------")
        rounds += 1
    print(playBoard.grid)
        
    
    
    


    

    