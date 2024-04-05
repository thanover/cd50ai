"""
Tic Tac Toe Player
"""

import math
import copy

X = "X"
O = "O"
EMPTY = None


def initial_state():
    """
    Returns starting state of the board.
    """
    return [[EMPTY, EMPTY, EMPTY],
            [EMPTY, EMPTY, EMPTY],
            [EMPTY, EMPTY, EMPTY]]


# The player function should take a board state as input, and return which player’s turn it is (either X or O).
# In the initial game state, X gets the first move. Subsequently, the player alternates with each additional move.
# Any return value is acceptable if a terminal board is provided as input (i.e., the game is already over).
def player(board):
    """
    Returns player who has the next turn on a board.
    """
    X_count = 0
    O_count = 0
    for row in board:
        for cell in row:
            if cell == X:
                X_count += 1
            elif cell == O:
                O_count += 1
    if O_count < X_count:
        return O
    
    return X

# The actions function should return a set of all of the possible actions that can be taken on a given board.
# Each action should be represented as a tuple (i, j) where i corresponds to the row of the move (0, 1, or 2) and j corresponds to which cell in the row corresponds to the move (also 0, 1, or 2).
# Possible moves are any cells on the board that do not already have an X or an O in them.
# Any return value is acceptable if a terminal board is provided as input.
def actions(board):
    """
    Returns set of all possible actions (i, j) available on the board.
    """
    actions = set()

    for i in range(3):
        for j in range(3):
            if board[i][j] == EMPTY:
                actions.add((i, j))

    return actions

# The result function takes a board and an action as input, and should return a new board state, without modifying the original board.
# If action is not a valid action for the board, your program should raise an exception.
# The returned board state should be the board that would result from taking the original input board, and letting the player whose turn it is make their move at the cell indicated by the input action.
# Importantly, the original board should be left unmodified: since Minimax will ultimately require considering many different board states during its computation. This means that simply updating a cell in board itself is not a correct implementation of the result function. You’ll likely want to make a deep copy of the board first before making any changes.
def result(board, action):
    """
    Returns the board that results from making move (i, j) on the board.
    """
    for _action in [action[0], action[1]]:
        if _action > 2 or _action < 0:
            raise ValueError(f"{action} is not a valid for a 3 x 3 board")

    if board[action[0]][action[1]] != EMPTY:
        raise ValueError(f"{action} is not a valid move for {board}")
    
    new_board = copy.deepcopy(board)
    new_board[action[0]][action[1]] = player(board)
    return new_board

# The winner function should accept a board as input, and return the winner of the board if there is one.
# If the X player has won the game, your function should return X. If the O player has won the game, your function should return O.
# One can win the game with three of their moves in a row horizontally, vertically, or diagonally.
# You may assume that there will be at most one winner (that is, no board will ever have both players with three-in-a-row, since that would be an invalid board state).
# If there is no winner of the game (either because the game is in progress, or because it ended in a tie), the function should return None.
def winner(board):
    # check for any winner horizontally
    for i in range(3):
        if board[i][0] == EMPTY:
            continue
        for j in range(3):
            if board[i][j] != board[i][0]:
                break
            if j == 2:
                return board[i][0]
    
    for j in range(3):
        if board[0][j] == EMPTY:
            continue
        for i in range(3):
            if board[i][j] != board[0][j]:
                break
            if i == 2:
                return board[0][j]
    
    if board[0][0] == board[1][1] == board[2][2]:
        return board[0][0]
    
    if board[0][2] == board[1][1] == board[2][0]:
        return board[0][2]

    return None 
        
# The terminal function should accept a board as input, and return a boolean value indicating whether the game is over.
# If the game is over, either because someone has won the game or because all cells have been filled without anyone winning, the function should return True.
# Otherwise, the function should return False if the game is still in progress.
def terminal(board):
    """
    Returns True if game is over, False otherwise.
    """
    if winner(board) != None:
        return True
    
    for i in range(3):
        for j in range(3):
            if board[i][j] == EMPTY:
                return False
    
    return True


# The utility function should accept a terminal board as input and output the utility of the board.
# If X has won the game, the utility is 1. If O has won the game, the utility is -1. If the game has ended in a tie, the utility is 0.
# You may assume utility will only be called on a board if terminal(board) is True.
def utility(board):
    """
    Returns 1 if X has won the game, -1 if O has won, 0 otherwise.
    """
    if winner(board) == X:
        return 1
    elif winner(board) == O:
        return -1
    else:
        return 0

# The minimax function should take a board as input, and return the optimal move for the player to move on that board.
# The move returned should be the optimal action (i, j) that is one of the allowable actions on the board. If multiple moves are equally optimal, any of those moves is acceptable.
# If the board is a terminal board, the minimax function should return None.
def minimax(board):
    """
    Returns the optimal action for the current player on the board.
    """
    if terminal(board):
        return None
    current_player = player(board)
    if current_player == X:
        best_result = -10
    else:
        best_result = 10
    for action in actions(board):
        new_board = result(board, action)
        util = complete_board(new_board)
        if current_player == X:
            if util > best_result:
                best_result = util
                best_action = action
        else:
            if util < best_result:
                best_action = action
                best_result = util
    return best_action

def complete_board(board):
    if terminal(board):
        return utility(board)
    
    return complete_board(result(board, minimax(board)))
