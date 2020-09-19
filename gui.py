import time
import pygame
from generate import Puzzle
from solver_helper import solve, printPuzzle, returnEmptySquare, isGridFull, isLegalNumber
from tkinter.filedialog import askopenfilename
from tkinter import *

pygame.font.init()


class Square:
    rows = 9
    cols = 9

    def __init__(self, value, row, col, width, height):
        self.value = value
        self.preValue = 0
        self.row = row
        self.col = col
        self.width = width
        self.height = height
        self.selected = False
        self.backtracking = 0

    def draw(self, win):
        fnt = pygame.font.SysFont("Arial", 40)
        x = self.col * self.width / 9
        y = self.row * self.width / 9

        if self.preValue != 0 and self.value == 0:
            text = fnt.render(str(self.preValue), 1, (128, 128, 128))
            win.blit(text, (x+5, y+5))
        elif not(self.value == 0):
            text = fnt.render(str(self.value), 1, (0, 0, 0))
            win.blit(text, (x + (self.width / 9/2 - text.get_width()/2),
                            y + (self.width / 9/2 - text.get_height()/2)))

        if self.selected:
            pygame.draw.rect(
                win, (100, 100, 255), (x, y, self.width / 9, self.width / 9), 3)
        if self.backtracking == 1:
            pygame.draw.rect(
                win, (200, 10, 255), (x, y, self.width / 9, self.width / 9), 3)
        elif self.backtracking == 2:
            pygame.draw.rect(
                win, (255, 100, 100), (x, y, self.width / 9, self.width / 9), 3)

    def set(self, val):
        self.value = val

    def set_preValue(self, val):
        self.preValue = val


class Board:
    def __init__(self, width, height, file):
        if(file == None):
            self.myPuzzle = Puzzle(None)

        else:
            self.myPuzzle = Puzzle(file)
        grid = self.myPuzzle.puzzle
        self.board = grid
        self.width = width
        self.height = height
        self.currentBoard = None
        self.selected = None
        self.rows = 9
        self.cols = 9
        self.squares = []
        self.solved = []
        for i in range(9):
            self.boardRow = []
            for j in range(9):
                self.boardRow.append(self.board[i][j])
            self.solved.append(self.boardRow)
        solve(self.solved)
        # fill up squares on the board
        for i in range(self.rows):
            self.squareRows = []
            for j in range(self.cols):
                self.squareRows.append(
                    Square(self.board[i][j], i, j, width, height))
            self.squares.append(self.squareRows)

    def solve_grid(self):
        for row in range(9):
            for col in range(9):
                if self.squares[row][col].value == 0:
                    self.squares[row][col].set(self.solved[row][col])
                    self.squares[row][col].set_preValue(0)

    def update(self):
        self.currentBoard = []
        for i in range(self.rows):
            self.currentBoardRows = []
            for j in range(self.cols):
                self.currentBoardRows.append(
                    self.squares[i][j].value)
            self.currentBoard.append(self.currentBoardRows)

    def addValue(self, val):
        row, col = self.selected
        if self.squares[row][col].value == 0:
            self.squares[row][col].set(val)
            self.update()

            if self.checkIfEqual(self.solved, self.currentBoard):
                self.board = self.currentBoard
                return True
            else:
                self.squares[row][col].set(0)
                self.squares[row][col].set_preValue(0)
                self.update()
                return False

    def checkIfEqual(self, solved, currentBoard):
        for i in range(9):
            for j in range(9):
                if currentBoard[i][j] != solved[i][j] and currentBoard[i][j] != 0:
                    return False
        return True

    def noteValue(self, val):
        row, col = self.selected
        if(self.squares[row][col].selected == True):
            self.squares[row][col].set_preValue(val)

    def draw(self, win):
        # drawing the 9x9 lines
        for i in range(10):
            if i % 3 != 0:
                pygame.draw.line(win, (205, 205, 255), (0, i*self.width / 9),
                                 (self.width, i*self.width / 9), 1)
                pygame.draw.line(win, (205, 205, 255), (i * self.width / 9, 0),
                                 (i * self.width / 9, self.height), 1)
        for i in range(10):
            if i % 3 == 0:
                pygame.draw.line(win, (150, 150, 255), (0, i*self.width / 9),
                                 (self.width, i*self.width / 9), 4)
                pygame.draw.line(win, (150, 150, 255), (i * self.width / 9, 0),
                                 (i * self.width / 9, self.height), 4)

        # Display the numbers
        for i in range(self.rows):
            for j in range(self.cols):
                self.squares[i][j].draw(win)

    # selected a tile will highlight it, also able to deselect it by clicking on it again
    def select(self, row, col):
        if(self.squares[row][col].selected == True):
            self.squares[row][col].selected = False
        else:
            if(self.squares[row][col].value == 0):
                for i in range(self.rows):
                    for j in range(self.cols):
                        self.squares[i][j].selected = False

                self.squares[row][col].selected = True
                self.selected = (row, col)

    # set tile back to blank
    def reset(self):
        row, col = self.selected
        if self.squares[row][col].value == 0:
            self.squares[row][col].set_preValue(0)

    def click(self, pos):
        if pos[0] < self.width and pos[1] < self.height:
            gap = self.width / 9
            x = pos[0] // gap
            y = pos[1] // gap
            return (int(y), int(x))
        else:
            return None

    def isGridFull(self):
        for i in range(self.rows):
            for j in range(self.cols):
                if self.squares[i][j].value == 0:
                    return False
        return True


class button():
    def __init__(self, color, x, y, width, height, text=''):
        self.color = color
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.text = text

    def draw(self, win, outline=None):
        if outline:
            pygame.draw.rect(win, outline, (self.x-2, self.y -
                                            2, self.width+4, self.height+4), 0)

        pygame.draw.rect(win, self.color, (self.x, self.y,
                                           self.width, self.height), 0)

        if self.text != '':
            font = pygame.font.SysFont('Courier New', 28)
            text = font.render(self.text, 1, (0, 0, 0))
            win.blit(text, (self.x + (self.width/2 - text.get_width()/2),
                            self.y + (self.height/2 - text.get_height()/2)))

    def clicked(self, pos):
        # Pos is the mouse position or a tuple of (x,y) coordinates
        if pos[0] > self.x and pos[0] < self.x + self.width:
            if pos[1] > self.y and pos[1] < self.y + self.height:
                return True

        return False


def uploadPuzzle():
    root = Tk()
    root.withdraw()
    filename = askopenfilename(parent=root, title="Select file",
                               filetypes=(('text files', 'txt'),))
    if filename != '':
        with open(filename) as f:
            lines = [line.rstrip() for line in f]
        f.close()
        root.destroy()
        numbers = "0123456789"
        myBoard = []
        for line in lines:
            myRow = []
            for character in line:
                if character in numbers:
                    myRow.append(int(character))
            myBoard.append(myRow)
        # printPuzzle(myBoard)
        return Board(540, 540, myBoard)


def visualBackTrace(puzzle, win, board, time, error):
    # check to see if there are empty squares
    empty = returnEmptySquare(puzzle)
    # if everything is filled then it is solved or else we make note where the empty square is
    if isGridFull(puzzle):  # base case
        return True
    else:
        row = empty[0]
        col = empty[1]

    # test each value and check if its legal
    for values in range(1, 10):
        if isLegalNumber(puzzle, values, row, col):
            puzzle[row][col] = values
            board.squares[row][col].backtracking = 1
            board.squares[row][col].set(values)
            redraw_window(win, board, time, error)
            pygame.time.delay(150)
            pygame.display.update()
            # backtracking by calling solve on our new puzzle
            if visualBackTrace(puzzle, win, board, time, error):
                return True
    # not correct? make it empty again and try next value on previously solved number
    puzzle[row][col] = 0
    board.squares[row][col].set(0)
    board.squares[row][col].backtracking = 2
    pygame.display.update()
    return False


grayButton = button((200, 200, 200), 416, 655, 120, 40, "Upload")
redButton = button((255, 20, 20), 0, 0, 540, 540, "GAME OVER")


def redraw_window(win, board, time, error):
    # background color
    win.fill((252, 252, 255))
    # Time spent on puzzle
    fnt = pygame.font.SysFont("Arial", 30)
    seconds = time % 60
    minutes = time//60
    text = fnt.render(" " + str(minutes) + ":" +
                      str("%02d" % seconds), 1, (0, 0, 0))
    win.blit(text, (540 - 75, 560))
    instr = fnt.render(
        "I for instant solve (Space to see backtracking)", 1, (0, 205, 250))
    win.blit(instr, (20, 600))
    instr = fnt.render(
        "N for new puzzle", 1, (95, 200, 90))
    win.blit(instr, (20, 640))
    grayButton.draw(win, (0, 0, 0))
    # Draw grid and board
    board.draw(win)
    # Draw Count Error
    errorColor = 100 * error
    if errorColor > 255:
        errorColor = 255
    text = fnt.render("Errors: {}".format(error), 1, (errorColor, 0, 0))
    win.blit(text, (20, 560))
    if(error > 2):
        redButton.draw(win, (0, 0, 0))


def main():
    win = pygame.display.set_mode((542, 700))
    pygame.display.set_caption("Sudoku Backtracking Visualization")
    puzzle = Board(540, 540, None)
    key = None
    start = time.time()
    error = 0
    while True:

        play_time = round(time.time() - start)

        for event in pygame.event.get():
            if event.type == pygame.MOUSEBUTTONDOWN:
                pos = pygame.mouse.get_pos()
                if grayButton.clicked(pos):
                    puzzle = uploadPuzzle()
                    start = time.time()
                    error = 0
                clicked = puzzle.click(pos)
                if clicked:
                    puzzle.select(clicked[0], clicked[1])
                    key = None
            if event.type == pygame.QUIT:
                return False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_1:
                    key = 1
                if event.key == pygame.K_2:
                    key = 2
                if event.key == pygame.K_3:
                    key = 3
                if event.key == pygame.K_4:
                    key = 4
                if event.key == pygame.K_5:
                    key = 5
                if event.key == pygame.K_6:
                    key = 6
                if event.key == pygame.K_7:
                    key = 7
                if event.key == pygame.K_8:
                    key = 8
                if event.key == pygame.K_9:
                    key = 9
                if event.key == pygame.K_i:
                    puzzle.solve_grid()
                if event.key == pygame.K_n:
                    puzzle = Board(540, 540, None)
                    start = time.time()
                    error = 0
                if event.key == pygame.K_BACKSPACE:
                    puzzle.reset()
                    key = None
                if event.key == pygame.K_SPACE:
                    visualBackTrace(puzzle.board, win,
                                    puzzle, play_time, error)
                    key = None
                if event.key == pygame.K_RETURN:
                    i, j = puzzle.selected
                    if puzzle.squares[i][j].preValue != 0:
                        if puzzle.addValue(puzzle.squares[i][j].preValue):
                            print("added")
                        else:
                            if(error < 3):
                                error += 1
                        key = None

                        if puzzle.isGridFull():
                            print("Game over")
                            return False

        if puzzle.selected and key != None:
            puzzle.noteValue(key)

        redraw_window(win, puzzle, play_time, error)
        pygame.display.update()


main()
pygame.quit()
