#!/usr/bin/python
#
# $Id$
#

import tkinter as tk
from random import seed, randint
import time
import sys


def doDot():
    global canvas
    life.nextGeneration()
    drawGrid(life)
    canvas.update()
    # canvas.update_idletasks()
    setIdle()


def updateCell(x, y, value):
    pass


def setIdle():
    canvas.after_idle(doDot)


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
            return self.cells[i[0] * self.xSize + i[1]: j[0] * self.xSize + j[1]: step]
        else:
            return self.cells[key[0] * self.xSize + key[1]]

    def __setitem__(self, key, value):
        self.cells[key[0] * self.xSize + key[1]] = value

    def neighbors(self, x, y):
        prevCol = x - 1
        nextCol = x + 1
        prevRow = y - 1
        nextRow = y + 1

        yield self[prevCol, prevRow]
        yield self[x, prevRow]
        yield self[nextCol, prevRow]

        yield self[prevCol, y]
        yield self[nextCol, y]

        yield self[prevCol, nextRow]
        yield self[x, nextRow]
        yield self[nextCol, nextRow]


class Life:

    def __init__(self, xSize, ySize):
        self.grid = LifeGrid(xSize + 2, ySize + 2)
        self.oldGrid = LifeGrid(xSize + 2, ySize + 2)
        self.generation = 0
        self.cellChangeCallback = None

    def __getitem__(self, key):
        if isinstance(key, slice):
            i = key.start[0] + 1, key.start[1] + 1
            j = key.stop[0] + 1, key.stop[1] + 1
            step = key.step
            return self.cells[i:j:step]
        else:
            return self.grid[key[0]+1, key[1]+1]

    def __setitem__(self, key, value):
        self.grid[key[0]+1, key[1]+1] = value

    def previousGeneration(self, x, y):
        return self.oldGrid[x + 1, y + 1]

    def nextGeneration(self):
        self.generation += 1
        print("Next generation (" + str(self.generation) + ")", file=sys.stderr)

        start_time = time.clock()

        xSize = self.grid.xSize
        ySize = self.grid.ySize
        grid = self.grid
        newGrid = self.oldGrid

        for x in range(1, xSize-1):
            for y in range(1, ySize-1):
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

        end_time = time.clock()
        print(str(end_time - start_time))

    def neighbors(self, x, y):
        return self.grid.neighbors(x + 1, y + 1)

    def addCellChangeCallback(self, fn):
        self.cellChangeCallback = fn

    def doCellChangeCallback(self, x, y, newValue):
        if not self.cellChangeCallback is None:
            self.cellChangeCallback(x-1, y-1, newValue)


def drawGrid(grid):
    for item in canvas.find_all():
        canvas.delete(item)
    for x in range(400):
        for y in range(400):
            # if grid[x, y] == 1 and grid.previousGeneration(x, y) == 0:
            if grid[x, y] == 1:
                canvas.create_rectangle(x, y, x, y, fill='black')
            # elif grid[x, y] == 0 and grid.previousGeneration(x, y) == 1:
            #    item = canvas.find_closest(x, y)
            #    canvas.delete(item)


seed

life = Life(400, 400)
for x in range(400):
    for y in range(400):
        life[x, y] = randint(0, 2)
# life.addCellChangeCallback(updateCell)

root = tk.Tk()
root.title('Game of Life')

canvas = tk.Canvas(root, width=400, height=400)

canvas.create_rectangle(0, 0, 20, 20, fill='black')

canvas.pack()

canvas.after(2000, setIdle)
# while 1:
#    life.nextGeneration()

root.mainloop()
