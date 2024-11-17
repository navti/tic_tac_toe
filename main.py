import pyglet
from pyglet import shapes
from settings import *
from pyglet.window import mouse
from pyglet.window import key

class Cross():
    def __init__(self, x, y, batch):
        self.lines = []
        delta = 50.0
        x1, y1 = x - delta, y + delta
        x2, y2 = x + delta, y1
        x3, y3 = x1, y - delta
        x4, y4 = x2, y3
        line_width = 5.0
        self.lines.append(shapes.Line(x1,y1,x4,y4,line_width,color=LINE_COLOR,batch=batch))
        self.lines.append(shapes.Line(x2,y2,x3,y3,line_width,color=LINE_COLOR,batch=batch))

class Nought(shapes.Arc):
    def __init__(self, *args, **kwargs):
        super(Nought, self).__init__(*args, **kwargs)
        self.thickness = 5.0

class TicTacToe(pyglet.window.Window):
    def __init__(self, *args, **kwargs):
        super(TicTacToe, self).__init__(*args, **kwargs)
        self.batch = pyglet.graphics.Batch()
        self.board_width = WIN_W
        self.board_height = WIN_H
        self.grid_lines = []
        self.crosses = []
        self.noughts = []
        for i in range(1,3):
            self.grid_lines.append(shapes.Line(i*self.board_width/3, 0, i*self.board_width/3, self.board_height, 3, color=GRID_COLOR, batch=self.batch))
            self.grid_lines.append(shapes.Line(0, i*self.board_height/3, self.board_width, i*self.board_height/3, 3, color=GRID_COLOR, batch=self.batch))

    def get_grid_center(self, x: float, y: float) -> tuple[int,int]:
        col_id = x//(self.board_width/3)
        row_id = y//(self.board_height/3)
        cx = self.board_width/6 + (col_id*self.board_width/3)
        cy = self.board_height/6 + (row_id*self.board_height/3)
        return cx, cy

    def on_mouse_press(self, x: int, y: int, button: int, modifiers: int) -> None:
        if button & mouse.LEFT:
            cx, cy = self.get_grid_center(x,y)
            if len(self.crosses) > len(self.noughts):
                self.noughts.append(Nought(cx, cy, radius=50.0, color=(LINE_COLOR), batch=self.batch))
            else:
                self.crosses.append(Cross(cx, cy, self.batch))

    def on_key_press(self, symbol: int, modifiers: int) -> None:
        if symbol & key.SPACE:
            self.crosses.clear()
            self.noughts.clear()

    def on_draw(self):
        self.clear()
        self.batch.draw()

if __name__ == "__main__":
    ttt = TicTacToe(*WIN_SIZE, caption="Tic Tac Toe")
    pyglet.app.run()