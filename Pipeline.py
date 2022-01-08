import MCTS
import game
import boardpy
import ValNetwork
import numpy as np

class NetworkInput(object):
    def __init__(self, gridPlayer, gridOppo, lastStep, player, pi, z = 0):
        self.gridPlayer = gridPlayer[:]
        self.gridOppo = gridOppo[:]
        self.lastStep = lastStep[:]
        self.player = player
        self.pi = pi[:]
        self.z = z

    def PrintNetwork(self):
        grid = boardpy.Board()
        for i in range(grid.width):
            for j in range(grid.width):
                if (self.gridPlayer[i][j] == 1):
                    grid.grid[i][j] = self.player
                if (self.gridOppo[i][j] == 1):
                    grid.grid[i][j] = -self.player
        print("-----------")
        print("Grid: ")
        print(grid.grid)
        print("pi: ")
        print(self.pi)
        print("-----------")
                    

class TrainingPipeline(object):
    def __init__(self, width, channel):
        self.network = ValNetwork.DLModel(width, channel)

    def EnlargeDataset(self, data):
        # Rotation doesn't change the result of game
        data_enlarged = []
        for datum in data:
            tmpPi = datum.pi[1:]
            fgridPlayer = np.flipud(datum.gridPlayer)
            fgridOppo = np.flipud(datum.gridOppo)
            fLastStep = np.flipud(datum.lastStep)
            board = boardpy.Board()
            fpi = np.array(tmpPi)
            fpi = np.flipud(fpi.reshape(board.width, board.width))
            for i in range(0, 4):
                gridPlayer = np.rot90(datum.gridPlayer, i)
                gridOppo = np.rot90(datum.gridOppo, i)
                gridLastStep = np.rot90(datum.lastStep, i)
                board = boardpy.Board()
                pi = np.array(tmpPi)
                pi = np.rot90(pi.reshape(board.width, board.width), i)
                pi = pi.flatten()
                inputPi = [datum.pi[0]]
                inputPi.extend(pi)
                data_enlarged.append(NetworkInput(gridPlayer, gridOppo, gridLastStep, datum.player, inputPi, datum.z))

                flipGridPlayer = np.rot90(fgridPlayer, i)
                flipGridOppo = np.rot90(fgridOppo, i)
                flipLastStep = np.rot90(fLastStep, i)
                flipPi = np.rot90(fpi, i)
                flipPi = flipPi.flatten()
                inputPi = [datum.pi[0]]
                inputPi.extend(flipPi)
                data_enlarged.append(NetworkInput(flipGridPlayer, flipGridOppo, flipLastStep, datum.player, inputPi, datum.z))
        return data_enlarged
    
    def splitData(self, data):
        x = []
        y_pi = []
        y_z = []
        board = boardpy.Board()
        for datum in data:
            if (datum.player == 1):
                colorGrid = np.ones((board.width, board.width), dtype=int)
            else:
                colorGrid = np.zeros((board.width, board.width), dtype=int)
            x.append([datum.gridPlayer, datum.gridOppo, datum.lastStep, colorGrid])
            y_pi.append(datum.pi)
            y_z.append(datum.z)
        x = np.array(x)
        y_pi = np.array(y_pi)
        y_z = np.array(y_z)
        return [x, [y_pi, y_z]]

    def MainProcess(self, tots = 50, batches = 20):
        for tot in range(tots):
            print("Total Round = {}".format(tot))
            data = []
            for _ in range(batches):
                perGame = game.Game()
                perGame.PlayGame(self.network)
                data.extend(perGame.gameData)
            data = self.EnlargeDataset(data)
            x, y = self.splitData(data)
            # for datum in data:
            #     datum.PrintNetwork()
            self.network.TrainingProcess(x, y)

            if ((tot + 1) % 10 == 0):
                self.network.saveModel("Reversi" + str(tot + 1) + "_rounds.h5")
    
if __name__ == "__main__":
    train = TrainingPipeline(6, 4)
    train.MainProcess()



        




