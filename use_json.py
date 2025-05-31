import random
x_wins = 0
o_wins = 0
xo_ties = 0
game_mode = 0
scores = {
    'X': 10,
    'O': -10,
    'tie': 0
}


# create board object
class Hashtag:
    def __init__(self, is_x_turn=None, board=None):
        """This is the docString for the class Hashtag.
        list of all funcs inside here"""
        # TODO create a docString
        # TODO make is_x_turn independent of comp and user

        # Keeps track of if a piece has been placed at a position
        self.move_list = [10] * 9
        # If is_x_turn param is not passed
        if is_x_turn is None:
            is_x_turn = True
        self.is_x_turn = is_x_turn
        if board is None:
            board = [" "] * 9
        self.board = board

    def is_valid(self, index):
        """Takes an int for the index of the value to be evaluated == 10.
        If True then returns True,
        and if not prints the index and warns user the index is not a valid input,
        and returns False.
        :param index type int
        :param index is the index of the value that is checked in move_list
        :returns bool"""

        if self.move_list[index] == 10:
            self.move_list[index] = index
            return True
        elif index in self.move_list:
            # TODO don't print when its comp turn and don't print board(make it stop)
            print(f"hey, {index + 1} is not a valid input ")
            return False

    def valid_move_list(self):
        """:param self.move_list
        :returns valid_li: list of open/valid moves"""
        valid_li = []
        # loops for then length of num list
        for i in range(len(self.move_list)):
            if self.move_list[i] == 10:
                valid_li.append(i)

        return valid_li

    def write_board(self, index):
        not_used = self.is_valid(index)
        if not_used:
            if self.is_x_turn:
                self.board[index] = "X"
            if not self.is_x_turn:
                self.board[index] = "O"
            self.take_turn()
        # FIxME

    def display_board(self):
        return print(f"""
         {self.board[6]} | {self.board[7]} | {self.board[8]} 
        -----------
         {self.board[3]} | {self.board[4]} | {self.board[5]} 
        -----------
         {self.board[0]} | {self.board[1]} | {self.board[2]} \n\n""")

    @staticmethod
    def example_board():
        """Prints a board and tells user the number layout"""
        return print(f"""
The number corresponds to the position for the move.
         {7} | {8} | {9}   
        -----------
         {4} | {5} | {6} 
        -----------
         {1} | {2} | {3}""")

    def take_turn(self):
        self.is_x_turn = not self.is_x_turn
        # fixme print(f"its is {self.is_x_turn} that it is x's turn.")
        return self.is_x_turn


# Start game
def start(player_1=0, player_2=1, other=False):
    global x_wins
    global o_wins
    global xo_ties

    def has_won(list_grid, move_list=None):
        """Checks if Cols, Rows or Diagonal is occupied by either a X or an O
        :param list_grid type list
        :returns if there is a win and who won :return bool"""
        x_o = ["X", "O"]
        for i in x_o:
            # Check Cols
            if list_grid[0] == i and list_grid[1] == i and list_grid[2] == i:
                return True, i
            elif list_grid[3] == i and list_grid[4] == i and list_grid[5] == i:
                return True, i
            elif list_grid[6] == i and list_grid[7] == i and list_grid[8] == i:
                return True, i
            # Check Rows
            elif list_grid[6] == i and list_grid[3] == i and list_grid[0] == i:
                return True, i
            elif list_grid[7] == i and list_grid[4] == i and list_grid[1] == i:
                return True, i
            elif list_grid[8] == i and list_grid[5] == i and list_grid[2] == i:
                return True, i
            # Check Diagonals
            elif list_grid[0] == i and list_grid[4] == i and list_grid[8] == i:
                return True, i
            elif list_grid[2] == i and list_grid[4] == i and list_grid[6] == i:
                return True, i
        else:
            if '10' not in move_list:
                return False

    # Setup
    b1 = Hashtag(is_x_turn=True)

    if not other:
        b1.example_board()

    def best_move(avail, board_li, who):
        """If there are two pieces in a row it returns the winning move,
        else returns -1
        :param board_li: list
        :param avail: all the available positions to play
        :param who: str either X or O
        """

        for i in avail:
            new_board = board_li[:]
            new_board[i] = who
            # if the move won when passed in the func, it returned True
            good = has_won(new_board, b1.move_list)
            if good:
                # it returns the move
                return str(i + 1)
        else:
            # The stop move func
            if who == 'X':
                who = 'O'
            elif who == 'O':
                who = 'X'
                # Ip all avail moves and if any produces a win for the other player
                # return move
            for i in avail:
                new_board = board_li[:]
                new_board[i] = who
                baby = has_won(new_board, b1.move_list)
                if baby:
                    return str(i + 1)
            else:
                return -1

    # ----------- Main loop -------------------------
    while not has_won(b1.board, b1.move_list) and 10 in b1.move_list:
        whose_turn = ''
        if b1.is_x_turn:
            whose_turn = 'X'
        elif not b1.is_x_turn:
            whose_turn = 'O'

        # Player 1
        if b1.is_x_turn:
            hi2 = b1.valid_move_list()
            if player_1 == 0:
                var1 = input(f"It's {whose_turn}'s turn. \nEnter your move here: ")
            elif player_1 == 1:
                var1 = random.randint(0, 9)
                var1 = str(var1)
            elif player_1 == 3:
                gold = best_move(hi2, b1.board, 'X')
                if gold != -1:
                    var1 = str(gold)
                else:
                    var1 = str(random.randint(0, 9))
            else:
                var1 = '0'
            if var1 == 'quit':
                quit()
            # checks if the move if valid and if not loop input until valid
            while not var1.isdecimal():
                if player_1 == 0:
                    var1 = input("Enter your move here: ")
                elif player_1 == 1:
                    var1 = random.randint(0, 9)
                    var1 = str(var1)

            var1 = int(var1)
            if 1 <= var1 <= 9:
                var1 -= 1
                b1.write_board(var1)
                b1.display_board()
        # Player 2
        elif not b1.is_x_turn:
            hi = b1.valid_move_list()
            if player_2 == 0:
                var2 = input(f"It's {whose_turn}'s turn. \nEnter your move here: ")
                if var2 == 'quit':
                    quit()
            elif player_2 == 1:
                # Computer plays random move
                var2 = str(random.randint(0, 9))
            elif player_2 == 3:

                gold = best_move(hi, b1.board, 'O')
                if gold != -1:
                    var2 = gold
                else:
                    var2 = str(random.randint(0, 9))
            # elif player_2 == 4:
            #     optimal_move(b1.board)
            else:
                var2 = '0'

            # check if the move if valid and if not loop input until valid
            while not var2.isdecimal():
                if player_2 == 0:
                    var2 = input("Enter your move here: ")
                elif player_2 == 1:
                    var2 = str(random.randint(0, 9))
            var2 = int(var2)
            if 1 <= var2 <= 9:
                var2 -= 1
                b1.write_board(var2)
                # Prints board to console
                b1.display_board()

    # Checks what type the end game was and then prints it
    if 10 not in b1.move_list:
        xo_ties += 1
        print("it's a tie")
        print(f"\tX Wins: {x_wins}\n\tO Wins: {o_wins}\n\tTies: {xo_ties}")
    elif b1.is_x_turn:
        o_wins += 1
        print("Yay O won!")
        print(f"\tX Wins: {x_wins}\n\tO Wins: {o_wins}\n\tTies: {xo_ties}")

    elif not b1.is_x_turn:
        x_wins += 1
        print("Yay X won!")
        print(f"\tX Wins: {x_wins}\n\tO Wins: {o_wins}\n\tTies: {xo_ties}")

    init_func_game(True)


# TODO choose which player goes first and what piece they are
def init_func_game(other=False):
    global game_mode
    global x_wins
    global o_wins
    global xo_ties

    def ip_func(ip_str):
        if ip_str == '':
            pass
        elif ip_str == 'n' or ip_str == 'no' or ip_str == 'quit' \
                or ip_str == 'nope' or ip_str[0] == 'n':
            quit()
        mode = input("Enter Option Number 1-9:\n"
                     "\t1:Human vs Computer AI\n"
                     "\t2:Human vs Computer Random.\n"
                     "\t3:Human vs Human\n"
                     "\t4:Computer AI vs Human\n"
                     "\t5:Computer Random vs Human\n"
                     "\t6:Computer Random vs Computer AI\n"
                     "\t7:Computer AI vs Computer Random\n"
                     "\t8:Computer AI vs Computer AI\n"
                     "\t9:Computer Random vs Computer Random\n\n>")
        return mode

    def start_mode(mode):
        # 0:Human 1:Comp Rand 3:Comp AI
        mode_li = [(1, 4), (0, 3), (0, 1), (0, 0), (3, 0), (1, 0), (1, 3), (3, 1), (3, 3), (1, 1)]
        for num, i in enumerate(mode_li):
            if mode == str(num):
                start(i[0], i[1], other)

    if not other:
        init_game = input('Do you want to play a game?\n> ')
        init_game = init_game.lower()
        game_mode = ip_func(init_game)
        start_mode(game_mode)
    if other:
        restart = input('Do you want to play again?\n>')
        if restart.startswith('n'):
            quit()
        print("New Game")
        start_mode(game_mode)


if __name__ == "__main__":
    while True:
        try:
            init_func_game()
        except RecursionError:
            print('Error:\n\tRestarting')
            x_wins = 0
            o_wins = 0
            xo_ties = 0
