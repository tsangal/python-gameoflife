#!/usr/bin/python

from random import randint
import time


class LifeGrid:
    def __init__(self, xSize, ySize):
        self.xSize = xSize
        self.ySize = ySize
        self.cells = [0 for i in range(xSize * ySize)]

    def __getitem__(self, key):
        if isinstance(key, slice):
            i = key.start
            j = key.stop
            step = key.step
            return self.cells[
                i[0] * self.xSize + i[1] : j[0] * self.xSize + j[1] : step
            ]
        else:
            return self.cells[key[0] * self.xSize + key[1]]

    def __setitem__(self, key, value):
        self.cells[key[0] * self.xSize + key[1]] = value

    def neighbors(self, x, y):
        prevCol = (x - 1) % self.xSize
        nextCol = (x + 1) % self.xSize
        prevRow = (y - 1) % self.ySize
        nextRow = (y + 1) % self.ySize

        return (
            self[prevCol, prevRow],
            self[x, prevRow],
            self[nextCol, prevRow],
            self[prevCol, y],
            self[nextCol, y],
            self[prevCol, nextRow],
            self[x, nextRow],
            self[nextCol, nextRow],
        )

    def __iter__(self):
        return ((x, y) for x in range(self.xSize) for y in range(self.ySize))


class GameOfLifeList:
    def __init__(self, xSize, ySize):
        self.cells = []
        self.xSize = xSize
        self.ySize = ySize
        self.grid = LifeGrid(xSize, ySize)
        self.oldGrid = LifeGrid(xSize, ySize)
        self.generation = 0
        self.cellChangeCallback = None

    def __getitem__(self, key):
        if isinstance(key, slice):
            i = key.start[0], key.start[1]
            j = key.stop[0], key.stop[1]
            step = key.step
            return self.cells[i:j:step]
        else:
            return self.grid[key[0], key[1]]

    def __setitem__(self, key, value):
        self.grid[key[0], key[1]] = value

    def randomize(self):
        for x in range(self.xSize):
            for y in range(self.ySize):
                i = randint(0, 5)
                self[x, y] = i == 0

    def previousGeneration(self, x, y):
        return self.oldGrid[x, y]

    def nextGeneration(self):
        self.generation += 1
        # print("Next generation (" + str(self.generation) + ")", file=sys.stderr)

        start_time = time.process_time()

        xSize = self.grid.xSize
        ySize = self.grid.ySize
        grid = self.grid
        newGrid = self.oldGrid

        for x in range(xSize):
            for y in range(ySize):
                # Get neighbor count.
                neighborCount = 0
                for cell in grid.neighbors(x, y):
                    if cell != 0:
                        neighborCount += 1

                # Determine new state of cell.
                if neighborCount == 2:
                    newGrid[x, y] = grid[x, y]
                elif neighborCount == 3:
                    newGrid[x, y] = 1
                else:
                    newGrid[x, y] = 0

                newValue = newGrid[x, y]
                if grid[x, y] != newValue:
                    self.doCellChangeCallback(x, y, newValue)

        self.oldGrid = grid
        self.grid = newGrid

        end_time = time.process_time()
        # print(str(end_time - start_time))

    def neighbors(self, x, y):
        return self.grid.neighbors(x, y)

    def addCellChangeCallback(self, fn):
        self.cellChangeCallback = fn

    def doCellChangeCallback(self, x, y, newValue):
        if not self.cellChangeCallback is None:
            self.cellChangeCallback(x, y, newValue)
