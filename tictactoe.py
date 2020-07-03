import random
import numpy as np


def gen_grid():
    # generates a list of size 9 which can be reshaped to a 3x3 grid
    return list(range(9))


def valid_move(pos, grid):
    # returns whether a certain move is valid
    try:
        test = grid[pos] + 1
        return True
    except TypeError:
        return False


def fill_space(pos, grid, x):
    # places a x/o in a space in the grid if valid
    if not valid_move(pos, grid):
        raise Exception('Invalid Move')

    if x:
        mark = 'X'
    else:
        mark = 'O'

    grid[pos] = mark

    return grid


def get_three(grid):
    # returns all three-in-a-row combinations in a grid
    three = []
    rows = [[0, 1, 2], [3, 4, 5], [6, 7, 8]]

    #  horizontal
    for row in rows:
        vals = []
        for i in row:
            vals.append(grid[i])

        three.append(vals)

    #  vertical
    for i in range(3):
        vals = []
        for row in rows:
            vals.append(grid[row[i]])

        three.append(vals)

    # diagonals
    three.append([grid[0], grid[4], grid[8]])
    three.append([grid[2], grid[4], grid[6]])

    return three


def game_won(grid, x):
    # returns whether x/o has won the game
    if x:
        mark = 'X'
    else:
        mark = 'O'

    threes = get_three(grid)

    for three in threes:
        if len(list(set(three))) == 1 and three[0] == mark:
            return True

    return False


def game_over(grid):
    # returns whether the game is over
    if game_won(grid, True) or game_won(grid, False):
        return True

    for pos in grid:
        try:
            test = pos + 1
            return False
        except TypeError:
            continue

    return True


def who_won(grid):
    # returns 0 is x won, 1 is o won and 2 if a tie
    if game_won(grid, True):
        return 0
    elif game_won(grid, False):
        return 1
    else:
        return 2


def display_grid(grid):
    # displays grid in a 3x3 format
    print(f"\n{grid[0]} {grid[1]} {grid[2]}\n{grid[3]} {grid[4]} {grid[5]}\n{grid[6]} {grid[7]} {grid[8]}\n")


def valid_moves(grid):
    # returns all valid spaces that can be filled in a grid
    valid = []
    for pos in grid:
        try:
            test = pos + 1
            valid.append(pos)
        except TypeError:
            continue

    return valid


def heuristics(grid, x):
    # returns the heuristic score for a certain grid
    if x:
        mark = 'X'
        mark_op = 'O'
    else:
        mark = 'O'
        mark_op = 'X'

    # points to add/subtract if in a given three-in-a-row there is only 1/2/3 of x/o filled and all other spaces are blank
    points = [1, 10, 100]
    points_op = [1, 10, 100]

    threes = get_three(grid)

    score = 0
    for three in threes:
        count = three.count(mark)
        count_op = three.count(mark_op)

        if count != 0 and count_op == 0:
            score += points[count - 1]
        if count_op != 0 and count == 0:
            score -= points_op[count - 1]

    return score


def player_agent(grid, x):
    # agent where player makes moves
    if x:
        mark = 'X'
    else:
        mark = 'O'

    moves = valid_moves(grid)
    return int(input(f"Select position for {mark} from" + f" {moves}: "))


def random_agent(grid, x):
    # agent where moves are decided at random based on current valid moves
    moves = valid_moves(grid)

    return random.choice(moves)


def minimax_agent(grid, x):
    # agent where move decided on maximum minimax score

    def minimax(grid, depth, maximising, x):
        # minimax recursive algorithm
        if game_over(grid) or depth == 0:
            return heuristics(grid, x)

        if maximising:
            max_score = -np.Inf

            for move in valid_moves(grid):
                temp_grid = fill_space(move, grid[:], x)
                max_score = max([max_score, minimax(temp_grid, depth - 1, False, x)])

            return max_score

        else:
            min_score = np.Inf

            for move in valid_moves(grid):
                temp_grid = fill_space(move, grid[:], not x)
                min_score = min(min_score, minimax(temp_grid, depth - 1, True, x))

            return min_score

    scores_dict = {}
    for child in valid_moves(grid):
        child_grid = fill_space(child, grid[:], x)
        child_score = minimax(child_grid, 2, False, x)

        scores_dict[child] = child_score

    # for each child choose the move which maximises the score
    max_pos = [key for key in scores_dict.keys() if scores_dict[key] == max(scores_dict.values())]

    return random.choice(max_pos)


def agent_play(agent_x, agent_o):
    # plays one game with two chosen agents, displays grid after each move
    grid = gen_grid()
    over = False

    display_grid(grid)
    while not over:
        pos = agent_x(grid, True)
        grid = fill_space(pos, grid[:], True)
        display_grid(grid)

        if game_over(grid):
            display_grid(grid)
            break

        pos = agent_o(grid, False)
        grid = fill_space(pos, grid[:], False)
        display_grid(grid)

        if game_over(grid):
            display_grid(grid)
            break


def agent_play_sim(agent_x, agent_o, sims):
    # plays game between two agents a certain number of time and returns results
    results = []
    for i in range(sims):
        grid = gen_grid()
        over = False

        while not over:
            pos = agent_x(grid, True)
            grid = fill_space(pos, grid[:], True)

            if game_over(grid):
                results.append(who_won(grid))
                break

            pos = agent_o(grid, False)
            grid = fill_space(pos, grid[:], False)

            if game_over(grid):
                results.append(who_won(grid))
                break

    x_prop = results.count(0) / len(results)
    o_prop = results.count(1) / len(results)
    tie_prop = results.count(2) / len(results)

    print(f"X win - {int(x_prop * 100)}%\nO win - {int(o_prop * 100)}%\nTie - {int(tie_prop * 100)}%")


if __name__ == '__main__':
    """
    Example usage: agent_play_sim(minimax_agent, minimax_agent, 100)
                   agent_play(player_agent, minimax_agent)
    """
