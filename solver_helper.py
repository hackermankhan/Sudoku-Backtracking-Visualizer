def solve(puzzle):
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
            # backtracking by calling solve on our new puzzle
            if solve(puzzle):
                return True
    # not correct? make it empty again and try next value on previously solved number
    puzzle[row][col] = 0
    return False

# parameters:
#           puzzle: the current puzzle (2d list)
#           value: the current number we are trying to plug in
#           row and col: the position on the puzzle
# returns true if the number is allowed


def isLegalNumber(puzzle, value, row, col):
    # sudoku containers are broken up to 3 by 3
    #   0  1  2
    # 0 ☐ ☐ ☐
    # 1 ☐ ☐ ☐
    # 2 ☐ ☐ ☐
    # floor division and then multiply by 3 to know our starting index (only 0, 3, 6 is possible)
    # depending on column position of our number, from left to right we can be in box x axis 0, 1 or 2.
    xContainer = col // 3 * 3
    # depending on row position, from top to bottom we can be in box y axis 0, 1, or 2
    yContainer = row // 3 * 3

    # Check container
    for i in range(3):
        for j in range(3):
            if puzzle[yContainer + i][xContainer + j] == value and (i, j) != (row, col):
                return False

    # checking every row
    for i in range(len(puzzle[0])):
        # if the number already exists in the row it's false
        if puzzle[row][i] == value and col != i:
            return False

    for i in range(len(puzzle)):
        # if the number already exists in the column its true
        if puzzle[i][col] == value and row != i:
            return False

    return True


# printing puzzle on console for testing (before GUI)
def printPuzzle(puzzle):
    for row in range(len(puzzle)):
        if row % 3 == 0 and row != 0:
            print(" ")

        for col in range(len(puzzle[0])):
            if col % 3 == 0 and col != 0:
                print("  ", end="")

            if col < 8:
                print(str(puzzle[row][col]) + " ", end="")
            else:
                print(puzzle[row][col])


# return first instance of an empty square
def returnEmptySquare(puzzle):
    for row in range(len(puzzle)):
        for col in range(len(puzzle[0])):
            if puzzle[row][col] == 0:
                return (row, col)  # return tuple
    return None

# A function to check if the grid is full


def isGridFull(puzzle):
    for row in range(len(puzzle)):
        for col in range(len(puzzle[0])):
            # if 0 then it's empty
            if puzzle[row][col] == 0:
                return False

    return True
