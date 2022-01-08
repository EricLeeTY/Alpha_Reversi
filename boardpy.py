import numpy as np 


class Board(object):
    def __init__(self, width = 6, grid = None):
        self.width = width
        if (grid == None):
            self.grid = np.zeros((self.width, self.width), dtype=int)
            self.grid[width // 2 - 1][width // 2 - 1] = 1
            self.grid[width // 2][width // 2] = 1
            self.grid[width // 2 - 1][width // 2] = -1
            self.grid[width // 2][width // 2 - 1] = -1
        else:
            self.grid = grid[:]
    
    def countWinner(self):
        white = 0
        black = 0
        for i in range(self.width):
            for j in range(self.width):
                if (self.grid[i][j] == 1):
                    white += 1
                elif (self.grid[i][j] == -1):
                    black += 1
        
        if (white > black):
            return 1
        elif (white < black):
            return -1
        else:
            return 0

    def inSideBoard(self, i):
        return i < self.width and i >= 0

    def canPositionOn(self, i, j, player):
        if (self.grid[i][j] != 0):
            return False

        directions = [[1,1],[1,0],[1,-1],[0,-1],[-1,-1],[-1,0],[-1,1],[0,1]]
        for direction in directions:
            tmpi, tmpj = [i + direction[0], j + direction[1]]
            while (self.inSideBoard(tmpi) and self.inSideBoard(tmpj) and self.grid[tmpi][tmpj] == -player):
                tmpi += direction[0]
                tmpj += direction[1]
            if (self.inSideBoard(tmpi) and self.inSideBoard(tmpj) and self.grid[tmpi][tmpj] == player and [i + direction[0], j + direction[1]] != [tmpi, tmpj]):
                return True

        return False

    def positioning(self, i, j, player):
        # if (not self.canPositionOn(i, j, player)):
        #     return
        self.grid[i][j] = player
        directions = [[1,1],[1,0],[1,-1],[0,-1],[-1,-1],[-1,0],[-1,1],[0,1]]
        for direction in directions:
            tmpi, tmpj = [i + direction[0], j + direction[1]]
            steps = []
            while (self.inSideBoard(tmpi) and self.inSideBoard(tmpj) and self.grid[tmpi][tmpj] == -player):
                steps.append([tmpi, tmpj])
                tmpi += direction[0]
                tmpj += direction[1]
            if (self.inSideBoard(tmpi) and self.inSideBoard(tmpj) and self.grid[tmpi][tmpj] == player and [i + direction[0], j + direction[1]] != [tmpi, tmpj]):
                for step in steps:
                    self.grid[step[0]][step[1]] = player

        return

    def oneSideNeedPass(self, player):
        for i in range(self.width):
            for j in range(self.width):
                if (self.canPositionOn(i, j, player)):
                    return False # not need pass
        return True

    def isTerminated(self):
        for i in range(self.width):
            for j in range(self.width):
                if (self.canPositionOn(i, j, 1) or self.canPositionOn(i, j, -1)):
                    return -2 # not end

        return self.countWinner()

    def GetGrid(self):
        return self.grid
    