from solver_helper import isLegalNumber, returnEmptySquare, isGridFull
from random import randint, shuffle


class Puzzle:
    def __init__(self, file):
        if file is None:
            self.puzzle = [
                [0, 0, 0, 0, 0, 0, 0, 0, 0],
                [0, 0, 0, 0, 0, 0, 0, 0, 0],
                [0, 0, 0, 0, 0, 0, 0, 0, 0],
                [0, 0, 0, 0, 0, 0, 0, 0, 0],
                [0, 0, 0, 0, 0, 0, 0, 0, 0],
                [0, 0, 0, 0, 0, 0, 0, 0, 0],
                [0, 0, 0, 0, 0, 0, 0, 0, 0],
                [0, 0, 0, 0, 0, 0, 0, 0, 0],
                [0, 0, 0, 0, 0, 0, 0, 0, 0]
            ]
            newPuzzle(self.puzzle)
            removeElements(self.puzzle)
        else:
            self.puzzle = file


# function for finding all possible solutions for the puzzle (check if puzzle is unique)
def findAllSolutions(puzzle, counter):
    # Find row and col position of the next empty spot
    row, col = returnEmptySquare(puzzle)

    # try out possible numbers
    for value in range(1, 10):
        if isLegalNumber(puzzle, value, row, col):
            puzzle[row][col] = value
            # if the entire puzzle is filled then we found a solution
            if isGridFull(puzzle):
                counter[0] += 1
            else:
                # backtracking
                if findAllSolutions(puzzle, counter):
                    return True
        puzzle[row][col] = 0
    return False


def removeElements(puzzle):
    runs = 2
    # remove as many elements as possible to create a unique puzzle
    while runs > 0:
        # get random number in puzzle, if its already empty keep trying to get it
        row = randint(0, 8)
        col = randint(0, 8)
        while puzzle[row][col] == 0:
            row = randint(0, 8)
            col = randint(0, 8)
        # In case getting rid of the cell gives us multiple solutions we want to store the original value so we can put it back
        original = puzzle[row][col]
        puzzle[row][col] = 0

        # Check to see if our puzzle has a unique solution
        amountOfSolutions = [0]
        findAllSolutions(puzzle, amountOfSolutions)
        # If we have more than 1 solution then we put the number back and stop
        if amountOfSolutions[0] != 1:
            puzzle[row][col] = original
            runs -= 1


def newPuzzle(puzzle):
    possibleNumbers = [1, 2, 3, 4, 5, 6, 7, 8, 9]
    # finding the next empty cell
    row, col = returnEmptySquare(puzzle)
    # randomize the numbers
    shuffle(possibleNumbers)
    # try to insert them
    for number in possibleNumbers:
        if(isLegalNumber(puzzle, number, row, col)):
            puzzle[row][col] = number
            # check if board is filled
            if isGridFull(puzzle):
                return True
            else:
                # not filled, continue making the puzzle
                if newPuzzle(puzzle):
                    return True
    # make it empty again and try next value on previously solved number
    puzzle[row][col] = 0

# check to see for multiple solutions for puzzle, does not alter puzzle
