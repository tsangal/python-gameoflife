#! /usr/bin/python3

import tkinter as tk
from random import seed

from game_of_life_hash import Life


class Application(tk.Frame):
    def __init__(self, master=None):
        super().__init__(master)
        self.pack()
        self.create_widgets()

    def create_widgets(self):
        seed
        life = Life(100, 100)

        frame = tk.Frame(root)
        frame.pack()

        canvas = tk.Canvas(frame, width=400, height=400)
        lifeManager = LifeCanvasManager(life, canvas)
        lifeManager.randomize()

        buttonFrame = tk.Frame(frame)
        buttonFrame.pack()

        startStopState = StartStopState()

        def handleStartStop():
            startStopState.toggle()

            if startStopState.started:
                lifeManager.start()
            else:
                lifeManager.stop()

        startStopButton = tk.Button(
            buttonFrame, textvariable=startStopState.label, command=handleStartStop
        )
        startStopButton.pack(side=tk.LEFT)

        randomizeButton = tk.Button(
            buttonFrame,
            text="Randomize",
            command=lifeManager.randomize,
        )
        randomizeButton.pack(side=tk.LEFT)

        canvas.create_rectangle(0, 0, 20, 20, fill="black")
        canvas.pack()


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
                    x * 4, y * 4, x * 4 + 2, y * 4 + 2, fill="black"
                )

    def randomize(self):
        self.canvas.after_idle(self.life.randomize)
        self.canvas.after_idle(self.drawGrid)

    def start(self):
        was_running = self.run
        self.run = True
        if not was_running:
            self._setIdle()

    def stop(self):
        self.run = False

    def _setIdle(self):
        if self.run:
            self.canvas.after_idle(self.update)


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
            self.label.set("Stop")
        else:
            self.label.set("Start")


if __name__ == "__main__":
    root = tk.Tk()
    root.title("Game of Life")

    app = Application(root)
    app.mainloop()
