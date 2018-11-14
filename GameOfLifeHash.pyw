#!/usr/bin/python

import tkinter as tk
from random import seed, randint
import time


class LifeCanvasManager:
    def __init__(self, life, canvas):
        self.life = life
        self.canvas = canvas
        self.run = False

    def update(self):
        self.life.nextGeneration()
        self.drawGrid()
        self.canvas.update()
        # canvas.update_idletasks()
        self._setIdle()

    def updateCell(self, x, y, value):
        pass

    def drawGrid(self):
        for item in self.canvas.find_all():
            self.canvas.delete(item)
        grid = self.life.grid
        for cell in grid:
            if grid[cell] == 1:
                x, y = cell
                self.canvas.create_rectangle(
                    x*4, y*4, x*4+2, y*4+2, fill='black')

    def randomize(self):
        canvas.after_idle(self.life.randomize)
        canvas.after_idle(self.drawGrid)

    def start(self):
        was_running = self.run
        self.run = True
        if not was_running:
            self._setIdle()

    def stop(self):
        self.run = False

    def _setIdle(self):
        if self.run:
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
        return [
            (prevCol, prevRow),
            (x, prevRow),
            (nextCol, prevRow),

            (prevCol, y),
            (nextCol, y),

            (prevCol, nextRow),
            (x, nextRow),
            (nextCol, nextRow),
        ]

    def __iter__(self):
        return self.cells.__iter__()

    def setdefault(self, key, value):
        self.cells.setdefault(key, value)


class Life:

    def __init__(self, xSize, ySize):
        self.xSize = xSize
        self.ySize = ySize
        self.grid = LifeGrid()
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
                life[x, y] = (i == 0)

    def nextGeneration(self):
        self.generation += 1
        # print >> sys.stderr, "Next generation (" + str(self.generation) + ")"

        # start_time = time.clock()

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

        # self.oldGrid = grid
        self.grid = newGrid

        # end_time = time.clock()
        # print str(end_time - start_time)

    def neighbors(self, cell):
        return self.grid.neighbors(cell)


class StartStopState:
    def __init__(self):
        self.started = False
        self.label = tk.StringVar()
        self._updateLabel()

    def toggle(self):
        self.started = not self.started
        self._updateLabel()

    def _updateLabel(self):
        if self.started:
            self.label.set('Stop')
        else:
            self.label.set('Start')


if __name__ == '__main__':
    seed

    life = Life(100, 100)

    root = tk.Tk()
    root.title('Game of Life')

    frame = tk.Frame(root)
    frame.pack()

    canvas = tk.Canvas(frame, width=400, height=400)
    lifeManager = LifeCanvasManager(life, canvas)
    lifeManager.randomize()

    buttonFrame = tk.Frame(frame)
    buttonFrame.pack()

    startStopState = StartStopState()

    def handleStartStop():
        global startStopState
        global lifeManager

        startStopState.toggle()

        if startStopState.started:
            lifeManager.start()
        else:
            lifeManager.stop()

    startStopButton = tk.Button(
        buttonFrame,
        textvariable=startStopState.label,
        command=handleStartStop
    )
    startStopButton.pack(side=tk.LEFT)

    randomizeButton = tk.Button(
        buttonFrame,
        text='Randomize',
        command=lifeManager.randomize,
    )
    randomizeButton.pack(side=tk.LEFT)

    canvas.create_rectangle(0, 0, 20, 20, fill='black')
    canvas.pack()
    # canvas.after(100, lifeManager.setIdle)

    # while 1:
    #    life.nextGeneration()

    root.mainloop()
