#! /usr/bin/python3

import argparse
import tkinter as tk
from random import seed


class Application(tk.Frame):
    def __init__(self, gameOfLife, master=None):
        super().__init__(master)

        self.gameOfLife = gameOfLife

        self.pack()
        self.create_widgets()

    def create_widgets(self):
        frame = tk.Frame(root)
        frame.pack()

        canvas = tk.Canvas(frame, width=400, height=400)
        lifeManager = LifeCanvasManager(self.gameOfLife, canvas)
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
    def __init__(self, gameOfLife, canvas):
        self.gameOfLife = gameOfLife
        self.canvas = canvas
        self.run = False

    def update(self):
        self.gameOfLife.nextGeneration()
        self.drawGrid()
        self.canvas.update()
        # canvas.update_idletasks()
        self._setIdle()

    def updateCell(self, x, y, value):
        pass

    def drawGrid(self):
        for item in self.canvas.find_all():
            self.canvas.delete(item)
        grid = self.gameOfLife.grid
        for cell in grid:
            if grid[cell] == 1:
                x, y = cell
                self.canvas.create_rectangle(
                    x * 4, y * 4, x * 4 + 2, y * 4 + 2, fill="black"
                )

    def randomize(self):
        self.canvas.after_idle(self.gameOfLife.randomize)
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


def parseArgs():
    parser = argparse.ArgumentParser(
        description="Game of Life App",
        formatter_class=argparse.ArgumentDefaultsHelpFormatter,
    )
    parser.add_argument(
        "-a",
        "--algorithm",
        choices=("dict", "list"),
        default="dict",
        help="Use the given algorithm",
    )
    return parser.parse_args()


if __name__ == "__main__":
    args = parseArgs()

    seed()

    root = tk.Tk()
    root.title("Game of Life")

    match args.algorithm:
        case "dict":
            from game_of_life_dict import GameOfLifeDict as GameOfLife
        case "list":
            from game_of_life_list import GameOfLifeList as GameOfLife
        case _:
            raise Exception(f"Unknown algorithm '{args.algorithm}'")

    life = GameOfLife(100, 100)

    app = Application(life, root)
    app.mainloop()
