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
        self.box_center = {}
        self.game_state = True
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
        return int(cx), int(cy), int(box_id), int(row_id), int(col_id)

    def end_game(self, win_set=None):
        """
        end_game ends the game, win or draw
        :param win_set: set containing box ids of winning combination, None if draw
        :return: None
        """
        if win_set:
            for box_id in win_set:
                *_, mark = self.box_center[box_id]
                if mark == 'x':
                    self.crosses[box_id].lines[0].color = WIN_COLOR
                    self.crosses[box_id].lines[1].color = WIN_COLOR
                else:
                    self.noughts[box_id].color = WIN_COLOR
        self.game_state = False

    def check_cross_win(self, row_id, col_id):
        """
        check_cross_win checks if the last drawn cross results in a win
        :param row_id: the row id of the box last drawn
        :param col_id: the col id of the box last drawn
        :return: a set containing winning combination of box ids
        """
        row_set = set()
        col_set = set()
        diag_set = set()
        anti_diag_set = set()

        # check the row the new element falls into
        for col in range(3):
            box_id = row_id*3 + col
            if box_id not in self.crosses:
                row_set.clear()
                break
            row_set.add(box_id)
        
        # check the col the new element falls into
        for row in range(3):
            box_id = row*3 + col_id
            if box_id not in self.crosses:
                col_set.clear()
                break
            col_set.add(box_id)

        # check the diagonals
        # anti diagonal
        if row_id == col_id:
            for i in range(3):
                box_id = i*3 + i
                if box_id not in self.crosses:
                    anti_diag_set.clear()
                    break
                anti_diag_set.add(box_id)
        # main diagonal
        if row_id == 2-col_id:
            for i in range(3):
                box_id = i*3 + 2-i
                if box_id not in self.crosses:
                    diag_set.clear()
                    break
                diag_set.add(box_id)

        return row_set | col_set | diag_set | anti_diag_set

    def check_nought_win(self, row_id, col_id):
        """
        check_nought_win checks if the last drawn nought results in a win
        :param row_id: the row id of the box last drawn
        :param col_id: the col id of the box last drawn
        :return: a set containing winning combination of box ids
        """
        row_set = set()
        col_set = set()
        diag_set = set()
        anti_diag_set = set()

        # check the row the new element falls into
        for col in range(3):
            box_id = row_id*3 + col
            if box_id not in self.noughts:
                row_set.clear()
                break
            row_set.add(box_id)
        
        # check the col the new element falls into
        for row in range(3):
            box_id = row*3 + col_id
            if box_id not in self.noughts:
                col_set.clear()
                break
            col_set.add(box_id)

        # check the diagonals
        # anti diagonal
        if row_id == col_id:
            for i in range(3):
                box_id = i*3 + i
                if box_id not in self.noughts:
                    anti_diag_set.clear()
                    break
                anti_diag_set.add(box_id)
        # main diagonal
        if row_id == 2-col_id:
            for i in range(3):
                box_id = i*3 + 2-i
                if box_id not in self.noughts:
                    diag_set.clear()
                    break
                diag_set.add(box_id)

        return row_set | col_set | diag_set | anti_diag_set

    def on_mouse_press(self, x: int, y: int, button: int, modifiers: int) -> None:
        """
        on_mouse_press checks for mouse left click and draws a nought or a cross
        :param x: x coordinate of mouse click
        :param y: y coordinate of mouse click
        :param button: the button on mouse that was pressed
        :param modifiers: the modifier key pressed on keyboard (ctrl, shift, etc)
        :return: None
        """
        if self.game_state and (button & mouse.LEFT):
            cx, cy, box_id, row_id, col_id = self.get_box_info(x,y)
            if box_id not in self.noughts and box_id not in self.crosses:
                if len(self.crosses) > len(self.noughts):
                    self.box_center[box_id] = (cx, cy, 'o')
                    self.noughts[box_id] = Nought(cx, cy, radius=50.0, thickness=LINE_THICKNESS, color=(LINE_COLOR), batch=self.batch)
                    win_set = self.check_nought_win(row_id, col_id)
                else:
                    self.box_center[box_id] = (cx, cy, 'x')
                    self.crosses[box_id] = Cross(cx, cy, self.batch)
                    win_set = self.check_cross_win(row_id, col_id)
                if len(win_set)>2:
                    self.end_game(win_set)
            else:
                self.end_game()
            
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
            self.box_center.clear()
            self.game_state = True

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