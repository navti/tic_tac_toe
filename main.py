import pyglet
from pyglet import shapes
from settings import *
from pyglet.window import mouse
from pyglet.window import key

class Cross():
    """
    class Cross to draw crosses on board
    """
    def __init__(self, x, y, batch):
        self.lines = []
        delta = 50.0
        x1, y1 = x - delta, y + delta
        x2, y2 = x + delta, y1
        x3, y3 = x1, y - delta
        x4, y4 = x2, y3
        self.lines.append(shapes.Line(x1, y1, x4, y4, LINE_THICKNESS, color=LINE_COLOR, batch=batch))
        self.lines.append(shapes.Line(x2, y2, x3, y3, LINE_THICKNESS, color=LINE_COLOR, batch=batch))

class Nought(shapes.Arc):
    """
    class Nought to draw noughts on board, derived from pyglet Arc
    """
    def __init__(self, *args, **kwargs):
        super(Nought, self).__init__(*args, **kwargs)

class TicTacToe(pyglet.window.Window):
    """
    TicTacToe class derived from pyglet Window to create board instance
    """
    def __init__(self, *args, **kwargs):
        super(TicTacToe, self).__init__(*args, **kwargs)
        self.batch = pyglet.graphics.Batch()
        self.board_width = WIN_W
        self.board_height = WIN_H
        self.grid_lines = []
        self.crosses = {}
        self.noughts = {}
        for i in range(1,3):
            self.grid_lines.append(shapes.Line(i*self.board_width/3, 0, i*self.board_width/3, self.board_height, 3, color=GRID_COLOR, batch=self.batch))
            self.grid_lines.append(shapes.Line(0, i*self.board_height/3, self.board_width, i*self.board_height/3, 3, color=GRID_COLOR, batch=self.batch))

    def get_box_info(self, x: float, y: float) -> tuple[int,int]:
        """
        get_box_info gets the center coordinates and id of a grid box where mouse click is made
        :param x: the x coordinate of mouse click
        :param y: the y coordinate of mouse click
        :return: tuple of center coordinates and box id (cx, cy, box_id)
        """
        col_id = x//(self.board_width/3)
        row_id = y//(self.board_height/3)
        box_id = 3*row_id + col_id
        cx = self.board_width/6 + (col_id*self.board_width/3)
        cy = self.board_height/6 + (row_id*self.board_height/3)
        return cx, cy, box_id

    def on_mouse_press(self, x: int, y: int, button: int, modifiers: int) -> None:
        """
        on_mouse_press checks for mouse left click and draws a nought or a cross
        :param x: x coordinate of mouse click
        :param y: y coordinate of mouse click
        :param button: the button on mouse that was pressed
        :param modifiers: the modifier key pressed on keyboard (ctrl, shift, etc)
        :return: None
        """
        if button & mouse.LEFT:
            cx, cy, box_id = self.get_box_info(x,y)
            if box_id not in self.noughts and box_id not in self.crosses:
                if len(self.crosses) > len(self.noughts):
                    self.noughts[box_id] = Nought(cx, cy, radius=50.0, thickness=LINE_THICKNESS, color=(LINE_COLOR), batch=self.batch)
                else:
                    self.crosses[box_id] = Cross(cx, cy, self.batch)

    def on_key_press(self, symbol: int, modifiers: int) -> None:
        """
        on_key_press checks for space key press and clears the board

        :param symbol: the pressed key symbol passed to this function from the OS
        :param modifiers: modifier key pressed like ctrl or shift 
        :return: None
        """
        if symbol & key.SPACE:
            self.crosses.clear()
            self.noughts.clear()

    def on_draw(self):
        """
        on_draw call to redraw window contents, called every frame
        :return: None
        """
        self.clear()
        self.batch.draw()

if __name__ == "__main__":
    ttt = TicTacToe(*WIN_SIZE, caption="Tic Tac Toe")
    pyglet.app.run()