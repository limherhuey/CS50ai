"""
Tic Tac Toe Player
"""

import math
from copy import deepcopy

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


def player(board):
    """
    Returns player who has the next turn on a board.
    """

    Xcount, Ocount = 0, 0

    for row in board:
        Xcount += row.count(X)
        Ocount += row.count(O)

    diff = Xcount - Ocount

    if diff == 0:
        return X
    else:
        return O


def actions(board):
    """
    Returns set of all possible actions (i, j) available on the board.
    """

    possible_actions = set()

    for i in range(len(board)):
        for j in range(len(board[i])):
            if board[i][j] == EMPTY:
                possible_actions.add((i, j))

    return possible_actions


def result(board, action):
    """
    Returns the board that results from making move (i, j) on the board.
    """

    result_board = deepcopy(board)

    input = player(result_board)
    result_board[action[0]][action[1]] = input
    
    return result_board


def winner(board):
    """
    Returns the winner of the game, if there is one.
    """
    
    # check horizontal
    for row in board:
        winner = row[0]

        for cell in row:
            # if the cell is occupied by a different player, no winner, stop checking this row
            if cell != winner:
                winner = None
                break
        
        if winner:
            # return the winner if there is one
            return winner
    
    # check vertical
    for j in range(len(board)):
        winner = board[0][j]

        for i in range(len(board)):
            if board[i][j] != winner:
                winner = None
                break
        
        if winner:
            return winner
    
    # check diagonals
    winner = board[0][0]

    for i in range(len(board)):
        if board[i][i] != winner:
            winner = None
            break

    if winner:
        return winner
        
    winner = board[0][2]

    for i in range(len(board)):
        if board[i][-i - 1] != winner:
            winner = None
            break
    
    # final return, whether there is a winner or None
    return winner


def terminal(board):
    """
    Returns True if game is over, False otherwise.
    """

    if winner(board):
        return True
    
    # check if board is filled
    for row in board:
        for cell in row:
            # game not finished if there is at least one empty cell
            if cell == EMPTY:
                return False

    return True


def utility(board):
    """
    Returns 1 if X has won the game, -1 if O has won, 0 otherwise.
    """
    
    win = winner(board)

    if win == X:
        return 1

    elif win == O:
        return -1

    else:
        return 0


def minimax(board):
    """
    Returns the optimal action for the current player on the board.
    """
    
    # when game is over already
    if terminal(board):
        return None

    # get the current player
    play = player(board)

    # find the optimal action based on player goal
    if play == X:
        optimal_action = max_value(board, 1)[1]
    else:
        optimal_action = min_value(board, -1)[1]

    return optimal_action    


def max_value(board, current_min):
    """
    Returns the value and action that maximises outcome given opponent's minimising strategy
    """

    # base case
    if terminal(board):
        return utility(board), None
    
    # assume maximum utility value is the absolute minimum possible
    max = -1
    first = True

    # find the largest possible value from all minimum values
    for action in actions(board):
        # initialise the action to be returned 
        if first:
            first = False
            optimal_action = action

        min = min_value(result(board, action), max)[0]
        
        if min > max:
            max = min

            # alpha-beta pruning (or stop if reached maximum utility) to reduce time complexity
            if max > current_min or max == 1:
                return max, action
            
            optimal_action = action
    
    return max, optimal_action


def min_value(board, current_max):
    """
    Returns the value and action that minimises outcome given opponent's maximising strategy
    """

    # base case
    if terminal(board):
        return utility(board), None
    
    # assume minimum utility value is the absolute maximum possible
    min = 1
    first = True

    # find the smallest possible value from all maximum values
    for action in actions(board):
        # initialise the action to be returned 
        if first:
            first = False
            optimal_action = action
        
        max = max_value(result(board, action), min)[0]
        
        if max < min:
            min = max

            # alpha-beta pruning (or stop if reached minimum utility) to reduce time complexity
            if min < current_max or min == -1:
                return min, action

            optimal_action = action
    
    return min, optimal_action
