from colorama import Fore, Style, init
init()

class Game:
    def __init__(self, length, height, win_condition):
        board = []
        for i in range(0, length):
            column = []
            for j in range(0, height):
                column.append(' ')
            board.append(column)

        self.length = length
        self.height = height
        self.board = board
        self.win_condition = win_condition

    def print_board(self):
        def print_bar():
            bar = "#"
            for i in range(0, self.length):
                bar += "---#"
            print(bar)

        print_bar()
        for i in range(0, self.height):
            line = "|"
            for j in range(0, self.length):
                sym = self.board[j][i]
                output = ""
                if (sym == 'X'):
                    output = Fore.GREEN + sym + Style.RESET_ALL
                else:
                    output = Fore.RED + sym + Style.RESET_ALL
                line += (' ' + output + ' |')
            print(line)
            print_bar()
    
    def make_move(self, player_symbol, index): # NOTE: index starts at 1
        if index < 0 or index > len(self.board)-1: # column index that is out of range
            return False
        elif self.board[index][0] != ' ': # chosen column is valid but full
            return False
        for i in range(0, self.height):
            if self.board[index][self.height - i - 1] == ' ':
                self.board[index][self.height - i - 1] = player_symbol
                return True

        print("something weird happened in make_move")
        return False

    def check_win(self, player_symbol):
        def check_line(line, player_symbol, win_condition):
            i = 0
            j = 0
            while j < len(line):
                if line[j] != player_symbol:
                    i = j + 1
                    j = i
                    continue
                elif (j - i + 1) >= win_condition:
                    return True
                else:
                    j += 1
                    continue
            return False

        vertical_batch = self.board

        horizontal_batch = []
        for i in range(0, height):
            horizontal_batch.append([self.board[j][i] for j in range(0, self.length)])

        diagonal_batch = diagonals_top_left_to_bottom_right(self.board) + diagonals_top_right_to_bottom_left(self.board)


        tocheck = vertical_batch + horizontal_batch + diagonal_batch
        for line in tocheck:
            if check_line(line, player_symbol, self.win_condition):
                return True
        return False

    def is_full(self):
        for column in self.board:
            for space in column:
                if space == ' ':
                    return False
        return True

def diagonals_top_left_to_bottom_right(grid):
    diagonals = []
    rows = len(grid)
    cols = len(grid[0])

    for col in range(cols):
        diagonal = []
        i, j = 0, col
        while i < rows and j < cols:
            diagonal.append(grid[i][j])
            i += 1
            j += 1
        diagonals.append(diagonal)

    for row in range(1, rows):
        diagonal = []
        i, j = row, 0
        while i < rows and j < cols:
            diagonal.append(grid[i][j])
            i += 1
            j += 1
        diagonals.append(diagonal)

    return diagonals

def diagonals_top_right_to_bottom_left(grid):
    diagonals = []
    rows = len(grid)
    cols = len(grid[0])

    for col in range(cols):
        diagonal = []
        i, j = 0, col
        while i < rows and j >= 0:
            diagonal.append(grid[i][j])
            i += 1
            j -= 1
        diagonals.append(diagonal)

    for row in range(1, rows):
        diagonal = []
        i, j = row, cols - 1
        while i < rows and j >= 0:
            diagonal.append(grid[i][j])
            i += 1
            j -= 1
        diagonals.append(diagonal)

    return diagonals


if __name__ == '__main__':
    player_x = input("Enter name for player 1 (X): ")
    player_o = input("Enter name for player 2 (O): ")
    length = int(input("Enter length dimesion for the board: "))
    height = int(input("Enter height dimension for the board: "))
    win_condition = int(input("Enter win condition (number): "))

    game = Game(length, height, win_condition)
    game_end = False
    turn  = 'X'

    while not game_end:
        game.print_board()
        if turn == 'X':
            print(f"Turn (X): {player_x}")
        elif turn == 'O':
            print(f"Turn (O): {player_o}")
        
        valid_move = False

        while not valid_move:
            player_input = input("Make your move on which column to place in (note that the board is 1-indexed): ")
            valid_move = game.make_move(turn, int(player_input)-1)
        
        valid_move = False

        if game.check_win(turn):
            game.print_board()
            print(f"{player_x if turn == 'X' else player_o} has won")
            break
        elif game.is_full():
            game.print_board()
            print("Tis a draw")
            break
        else:
            if turn == 'X':
                turn = 'O'
            elif turn == 'O':
                turn = 'X'