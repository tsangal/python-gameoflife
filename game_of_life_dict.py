from random import randint
import time


class LifeGrid:
    def __init__(self, xSize, ySize):
        self.xSize = xSize
        self.ySize = ySize
        self.cells = {}

    def __getitem__(self, key):
        return self.cells.get(key, 0)

    def __setitem__(self, key, value):
        self.cells[key] = value

    def neighbors(self, key):
        x, y = key
        prevCol = (x - 1) % self.xSize
        nextCol = (x + 1) % self.xSize
        prevRow = (y - 1) % self.ySize
        nextRow = (y + 1) % self.ySize
        return (
            (prevCol, prevRow),
            (x, prevRow),
            (nextCol, prevRow),
            (prevCol, y),
            (nextCol, y),
            (prevCol, nextRow),
            (x, nextRow),
            (nextCol, nextRow),
        )

    def __iter__(self):
        return self.cells.__iter__()

    def setdefault(self, key, value):
        self.cells.setdefault(key, value)


class GameOfLifeDict:
    def __init__(self, xSize, ySize):
        self.xSize = xSize
        self.ySize = ySize
        self.grid = LifeGrid(xSize, ySize)
        # self.oldGrid = LifeGrid()
        self.generation = 0

    def __getitem__(self, key):
        return self.grid[key]

    def __setitem__(self, key, value):
        self.grid[key] = value

    # def previousGeneration(self, key):
    #    return self.oldGrid[key]

    def randomize(self):
        for x in range(self.xSize):
            for y in range(self.ySize):
                i = randint(0, 5)
                self[x, y] = i == 0

    def nextGeneration(self):
        self.generation += 1
        # print >> sys.stderr, "Next generation (" + str(self.generation) + ")"

        # start_time = time.clock()

        xSize = self.xSize
        ySize = self.ySize
        grid = self.grid
        newGrid = LifeGrid(xSize, ySize)

        # Increment neighbor counts of live cells
        neighborGrid = LifeGrid(xSize, ySize)
        for cell in grid:
            if grid[cell]:
                for neighbor in neighborGrid.neighbors(cell):
                    neighborGrid[neighbor] += 1

        for cell in grid:
            neighborCount = neighborGrid[cell]

            # Determine new state of cell.
            if neighborCount == 3 or (grid[cell] != 0 and neighborCount == 2):
                x, y = cell
                if x >= 0 and x < self.xSize and y >= 0 and y < self.ySize:
                    newGrid[cell] = 1
                    for neighbor in grid.neighbors(cell):
                        newGrid.setdefault(neighbor, 0)

        # self.oldGrid = grid
        self.grid = newGrid

        # end_time = time.clock()
        # print str(end_time - start_time)

    def neighbors(self, cell):
        return self.grid.neighbors(cell)
