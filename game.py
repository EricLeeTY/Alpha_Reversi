import boardpy
import MCTS
import random

class Game(object):
    def __init__(self):
        self.mcts = MCTS.MCTS()
        self.gameData = []
        
    def PlayGame(self, network):
        self.__init__()
        gameData = []
        while (self.mcts.root.board.isTerminated() == -2): # not terminated:
            self.mcts.Playout(network)
            print(self.mcts.root.board.grid)
            if (self.mcts.root.board.oneSideNeedPass(-self.mcts.root.player)):
                print("Look at here!")
            gameData.append(self.mcts.getData())
            rand = random.random()
            add = 0
            for i in range(-1, self.mcts.root.board.width * self.mcts.root.board.width):
                if i not in self.mcts.root.children:
                    continue
                add += self.mcts.root.children[i].n / self.mcts.root.n
                if (rand < add):
                    self.mcts.root = self.mcts.root.children[i]
                    break
        winner = self.mcts.root.board.isTerminated()
        print("One Game Played. Collecting data...")
        print(self.mcts.root.board.grid)
        for ele in gameData:
            if (ele.player == winner):
                ele.z = 1
            elif (ele.player == -winner):
                ele.z = -1
            else:
                ele.z = 0
        self.gameData.extend(gameData)

        
            
            