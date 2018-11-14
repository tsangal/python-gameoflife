#!/usr/bin/python

import tkinter as tk
from random import seed, randint
import time


class LifeCanvasManager:
    def __init__(self, lifeGrid, canvas):
        self.life = lifeGrid
        self.canvas = canvas

    def update(self):
        self.life.nextGeneration()
        self.drawGrid(life)
        self.canvas.update()
        # canvas.update_idletasks()
        self.setIdle()

    def updateCell(self, x, y, value):
        pass

    def drawGrid(self, life):
        for item in self.canvas.find_all():
            self.canvas.delete(item)
        grid = self.life.grid
        for cell in grid:
            if grid[cell] == 1:
                x, y = cell
                self.canvas.create_rectangle(
                    x*4, y*4, x*4+2, y*4+2, fill='black')

    def setIdle(self):
        canvas.after_idle(self.update)


class LifeGrid:

    def __init__(self):
        self.cells = {}

    def __getitem__(self, key):
        return self.cells.get(key, 0)

    def __setitem__(self, key, value):
        self.cells[key] = value

    def neighbors(self, key):
        x, y = key
        prevCol = x - 1
        nextCol = x + 1
        prevRow = y - 1
        nextRow = y + 1

        yield (prevCol, prevRow)
        yield (x, prevRow)
        yield (nextCol, prevRow)

        yield (prevCol, y)
        yield (nextCol, y)

        yield (prevCol, nextRow)
        yield (x, nextRow)
        yield (nextCol, nextRow)

    def __iter__(self):
        return self.cells.__iter__()

    def setdefault(self, key, value):
        self.cells.setdefault(key, value)


class Life:

    def __init__(self, xSize, ySize):
        self.xSize = xSize
        self.ySize = ySize
        self.grid = LifeGrid()
        #self.oldGrid = LifeGrid()
        self.generation = 0

    def __getitem__(self, key):
        return self.grid[key]

    def __setitem__(self, key, value):
        self.grid[key] = value

    # def previousGeneration(self, key):
    #    return self.oldGrid[key]

    def nextGeneration(self):
        self.generation += 1
        #print >> sys.stderr, "Next generation (" + str(self.generation) + ")"

        #start_time = time.clock()

        grid = self.grid
        newGrid = LifeGrid()

        for cell in grid:
            neighborCount = 0
            for neighbor in grid.neighbors(cell):
                if grid[neighbor] != 0:
                    neighborCount += 1

            # Determine new state of cell.
            if neighborCount == 3 or (grid[cell] != 0 and neighborCount == 2):
                x, y = cell
                if x >= 0 and x < self.xSize and y >= 0 and y < self.ySize:
                    newGrid[cell] = 1
                    for neighbor in grid.neighbors(cell):
                        newGrid.setdefault(neighbor, 0)

        #self.oldGrid = grid
        self.grid = newGrid

        #end_time = time.clock()
        # print str(end_time - start_time)

    def neighbors(self, cell):
        return self.grid.neighbors(cell)


if __name__ == '__main__':
    seed

    life = Life(100, 100)
    for x in range(100):
        for y in range(100):
            i = randint(0, 5)
            if i == 0:
                life[x, y] = 1

    root = tk.Tk()
    root.title('Game of Life')

    frame = tk.Frame(root)
    frame.pack()

    canvas = tk.Canvas(frame, width=400, height=400)
    canvas.create_rectangle(0, 0, 20, 20, fill='black')
    canvas.pack()

    lifeManager = LifeCanvasManager(life, canvas)
    canvas.after(100, lifeManager.setIdle)

    # while 1:
    #    life.nextGeneration()

    root.mainloop()
