# imports
import pprint
import copy
from chexceptions import *
from string import Template
from random import randrange
print("hello")
# Info
__version__ = "1.0"
__author__ = "Alexander Linnik"
__all__ = ["ChGame", "WHITE_START_POSITIONS", "BLACK_START_POSITIONS"]
# Constants
# MAX_CHECKERS = 12
TABLE_SIZE = 64
COLUMNS_CHARS = ('a', 'b', 'c', 'd', 'e', 'f', 'g', 'h')
LINE_CHARS = (1, 2, 3, 4, 5, 6, 7, 8)
ASCII_NUM = 96
WHITE_START_POSITIONS = (
    'a1', 'c1', 'e1', 'g1',
    'b2', 'd2', 'f2', 'h2',
    'a3', 'c3', 'e3', 'g3'
)
BLACK_START_POSITIONS = (
    'b8', 'd8', 'f8', 'h8',
    'a7', 'c7', 'e7', 'g7',
    'b6', 'd6', 'f6', 'h6'
)
TABLE_SQUARES = {'{0}{1}'.format(i, j) for i in COLUMNS_CHARS for j in LINE_CHARS if (ord(i) - ASCII_NUM + j) % 2 == 0}

# Classes and Exception Declaration
"""
Classes:
ChGame - Controls moves, make new moves, include black and white player
ChPlayer - Player, his checkers
ChChecker - checker
ChTable - table

Threads:
CheckerException
    WrongColorError
    PositionError
    WrongMoveError
    GameInternalError
"""


# ChClasses
class ChGame:
    """
    Main class of the game process
    """
    run_games = 0

    def __init__(self, num_of_game=run_games):
        type(self).run_games += 1
        self.num = num_of_game
        self.white_player = ChPlayer('white', self)
        self.black_player = ChPlayer('black', self)
        self.table_obj = ChTable(self)
        self.even_flag = 0
        self.pos_repeat = 0
        self.three_vs_one = 0
        self.logged_moves = []
        self.positions_made = {}
        self.count_queens = [0, 0]
        self.count_all = [12, 12]
        self.logged_random_moves = []
        self.new_queen_on = False

    def check_game_win(self) -> int: # -1 Black Win, 0 No Win, 1 White Win
        print('WHITE AVAIL MOVES=',self.scan_all_moves('white'))
        print('BLACK AVAIL MOVES=', self.scan_all_moves('black'))
        if not self.white_player.checkers or self.scan_all_moves('white')[0] is None:
            if not self.black_player.checkers:
                raise GameInternalError
            return -1
        if not self.black_player.checkers or self.scan_all_moves('black')[0] is None:
            if not self.white_player.checkers:
                raise GameInternalError
            return 1
        return 0
        # Check

    def check_game_draw_3_1(self):
        ch_w = self.white_player.checkers
        ch_b = self.black_player.checkers
        if self.three_vs_one != 0 and ((len(ch_b) == 1 and len(ch_w) >= 3) or (len(ch_w) == 1 and len(ch_b) >= 3)):
            self.three_vs_one += 1
            return True if self.three_vs_one == 15 else False
        if ((len(ch_b) >= 3 and len(ch_w) == 1) or (len(ch_w) >= 3 and len(ch_b) == 1)) and \
           all([ch.queen for ch in ch_b.values()]) and all([ch.queen for ch in ch_w.values()]):
            self.three_vs_one += 1
        else:
            return False
        # Checked probably

    def check_game_draw_repeat(self) -> bool:
        """
        Returns True if position has been repeated
        :return:
        """
        counter_queens = [0, 0]
        if [len(self.white_player.checkers), len(self.black_player.checkers)] != self.count_all:
            self.count_all = [len(self.white_player.checkers), len(self.black_player.checkers)]
            self.positions_made.clear()
        for num, color in enumerate((self.white_player.checkers.values(), self.black_player.checkers.values())):
            for checker in color:
                if checker.queen:
                    counter_queens[num] += 1
        if counter_queens != self.count_queens:
            self.count_queens = counter_queens
            self.positions_made.clear()
        curr_pos = (frozenset(self.white_player.checkers.keys()), frozenset(self.black_player.checkers.keys()))
        if self.positions_made.get(curr_pos):
            self.positions_made[curr_pos] += 1
            if self.positions_made[curr_pos] == 3:
                return True
        else:
            self.positions_made[curr_pos] = 1
        return False

    def make_move(self, color: str, move: tuple):
        """
        Makes move with checking its possibility
        Takes color of checker and move (from, to)
        """
        if color != 'black' and color != 'white':
            raise WrongColorError
        if move is None:
            return -1
        opposite_player = self.white_player if color == 'black' else self.black_player
        player = self.white_player if color == 'white' else self.black_player
        if len(move) == 3:
            from_pos, to_pos, eaten_pos = move
            if opposite_player.checkers.get(eaten_pos) is None:
                raise WrongMoveError(move)
            del opposite_player.checkers[eaten_pos]
        elif len(move) == 2:
            from_pos, to_pos = move
        else:
            raise WrongMoveError(move)
        # -- #
        player.make_move(from_pos, to_pos)
        self.update_table()
        if (to_pos[1] == '8' and color == 'white') or (to_pos[1] == '1' and color == 'black'):
            player.checkers[to_pos].queen = True
            self.new_queen_on = True
        return player.checkers[to_pos]

    @staticmethod
    def take_move():
        """
        Read move
        If returns -1 then the game was canceled
        """
        try:
            move = tuple(input("Make move: ").split('-'))
            for elem in move:
                if elem not in TABLE_SQUARES:
                    raise SyntaxWarning
        except CheckerException as cherr:
            print(cherr)
            return 1
        except SyntaxWarning as exc:
            print('Want exit? Y/n')
            get = input()
            if get == 'Y':
                return -1
            else:
                return 1
        else:
            return move

    def take_random_move(self, *scan_res):
        """
        Give random move from list of available moves
        """
        all_moves = [(from_pos, to_pos) for from_pos, to_pos, eaten, in scan_res[0]] if scan_res[1] else scan_res[0]
        rand_ind=randrange(len(all_moves))
        print('-'.join(all_moves[rand_ind]))
        self.logged_random_moves.append('-'.join(all_moves[rand_ind]))
        return all_moves[rand_ind]

    def write_state(self, state): # Delegate func
        print(state)

    def play(self, random_moves=False):
        """
        Main function to start the game,
        Random_moves is only for debug
        Returns -1 - Game Canceled
        Returns 0 - Game ended clearly
        """
        self.logged_random_moves.clear()
        turn = 1
        while self.check_game_win() == 0 and not self.check_game_draw_3_1() and not self.check_game_draw_repeat():
            end_move_flag = False
            self.table_obj.table_print()
            all_moves, must_eat_flag = self.scan_all_moves('white') if turn == 1 else self.scan_all_moves('black')
            while not end_move_flag:
                print(Template("Turn is $color").substitute(color='white' if turn == 1 else 'black'))
                move = self.take_move() if not random_moves else self.take_random_move(all_moves, must_eat_flag)
                if move == 1:
                    continue
                elif move == -1:
                    return -1
                if not must_eat_flag:
                    if move not in all_moves:
                        print('Illegal move, first break, make new')
                        self.write_state('N---')
                        continue
                    else:
                        try:
                            self.make_move('white' if turn == 1 else 'black', move)
                        except CheckerException as cherr:
                            print(cherr, 'Something Wrong with that', sep='\n')
                            self.write_state('N---')
                            return -1
                        else:
                            self.write_state('YN--')
                            end_move_flag = True
                else:
                    short_moves = [(from_pos, to_pos) for from_pos, to_pos, eaten, in all_moves]
                    if move not in short_moves:
                        self.write_state('N---')
                        print('Illegal move, make new')
                        continue
                    try:
                        last_checker = self.make_move('white' if turn == 1 else 'black',
                                                      all_moves[short_moves.index(move)])
                    except CheckerException as cherr:
                        self.write_state('N---')
                        print(cherr, 'Something went wrong...', sep='\n')
                        return -1
                    if self.scan_checker(last_checker, True)[0] is None:
                        self.write_state('YN' + all_moves[short_moves.index(move)][2])
                        end_move_flag = True
                    else:
                        self.write_state('YS' + all_moves[short_moves.index(move)][2])
                        all_moves, must_eat_flag = self.scan_checker(last_checker, True)
            turn = 0 if turn == 1 else 1
        else:
            self.table_obj.table_print()
            if self.three_vs_one == 15:
                # Print pipe Draw
                print('Draw!')
            elif self.check_game_win() == 1:
                # Print pipe Draw
                print('White won')
            elif self.check_game_win() == -1:
                # Print pipe Draw
                print('Black won')
            else:
                print('Draw by the repeat')
            return 0

    def update_table(self):
        for pos, checker_color in self.table_obj:
            if pos in self.white_player.checkers.keys():
                self.table_obj[pos] = 1
            elif pos in self.black_player.checkers.keys():
                self.table_obj[pos] = 2
            else:
                self.table_obj[pos] = 0

    def scan_checker(self, checker, must_eat_flag=False) -> ([(str, str)], bool):
        """
        Scans moves of 1 checker
        :returns list of moves
        ! If must_eat_flag was or become True, then i returns list of:
        [(checker.pos, next_checker_pos, eaten_checker_pos), ...], must_eat_flag
        else
        [(checker.pos, next_checker_pos)], must_eat_flag
        """
        color = 1 if checker.color == 'white' else 2
        moves = []
        if not checker.queen:
            # --- FOR SIMPLE CHECKERS --- #
            fields = self.table_obj.gen_fields(checker.position)
            for field in fields:
                if (self.table_obj[field] == color or                                        # 1)The same color is next
                   (self.table_obj[field] == 0 and not                                       # 2)The field is free
                   ((checker.color == 'white' and int(field[1]) > int(checker.position[1])) or  # but field is behind
                   (checker.color == 'black' and int(field[1]) < int(checker.position[1]))))):  # the position.
                    continue
                elif (self.table_obj[field] == 0 and                                         # 3)The field is free
                     ((checker.color == 'white' and int(field[1]) > int(checker.position[1])) or  # and the field is aft
                     (checker.color == 'black' and int(field[1]) < int(checker.position[1])))):   # the position
                    if not must_eat_flag:
                        moves.append((checker.position, field))
                else:                                                                        # 4)The enemy checker is
                    next_field = self.table_obj.next_on_dg(checker.position, field)
                    if next_field == -1 or self.table_obj[next_field] != 0:   # 4.1) If next isn't free
                        continue
                    else:
                        # CAREFUL
                        if not must_eat_flag:
                            moves.clear()
                        eaten_field = field
                        moves.append((checker.position, next_field, eaten_field))
                        must_eat_flag = True
            return (moves, must_eat_flag) if len(moves) != 0 else (None, must_eat_flag)
        else:
            # --- FOR QUEENS --- #
            dgs = self.table_obj.gen_dgs(checker.position)
            all_moves = []
            for dg in dgs:
                is_eaten_checker = False
                gonna_eaten = False
                eaten_field = ""
                moves = []
                for field in dg:
                    if self.table_obj[field] == color:  # 1)The same color is next
                        break
                    elif self.table_obj[field] == 0:
                        if not must_eat_flag:
                            if gonna_eaten:
                                all_moves.clear()
                                moves.clear()
                                moves.append((checker.position, field, eaten_field))
                                must_eat_flag = True
                                gonna_eaten = False
                                is_eaten_checker = True
                            else:
                                moves.append((checker.position, field))
                        elif gonna_eaten:
                            moves.append((checker.position, field, eaten_field))
                            gonna_eaten = False
                            is_eaten_checker = True
                        elif is_eaten_checker:
                            moves.append((checker.position, field, eaten_field))
                    else:
                        if gonna_eaten or is_eaten_checker:  # is_eaten_checker to prevent 2 depth of scan (like combo)
                            break
                        else:
                            eaten_field = field
                            gonna_eaten = True
                all_moves += moves
            if len(all_moves) != 0:
                return all_moves, must_eat_flag
            else:
                return None, must_eat_flag

    def scan_all_moves(self, color: str, must_eat_flag=False) -> (list, bool): # list of all or must moves, flag checks i
        one_time_flag = False
        if color != 'white' and color != 'black':
            raise WrongColorError
        all_moves = []
        num_color = 1 if color == 'white' else 2
        player = self.white_player if color == 'white' else self.black_player
        for checker in player.checkers.values():
            moves, must_eat_flag = self.scan_checker(checker, must_eat_flag)
            if must_eat_flag and not one_time_flag:
                all_moves.clear()
                one_time_flag = True
            if moves is not None:
                for move in moves:
                    all_moves.append(move)
        if all_moves:
            return all_moves, must_eat_flag
        else:
            return None, must_eat_flag


class ChChecker:
    def __init__(self, color: str, position: str, ch_game: ChGame, queen=False):
        if ch_game is None:
            raise TypeError('ch_game is None')
        if color != 'black' and color != 'white':
            raise WrongColorError(color)
        if position[0] not in COLUMNS_CHARS or int(position[1]) not in LINE_CHARS:
            raise PositionError(position)
        self.color = color
        self.position = position
        self.num_of_game = ch_game.num
        self.queen = queen


class ChPlayer:
    def __init__(self, color: str, ch_game: ChGame):
        """
        Create new player
        """
        if ch_game is None:
            raise TypeError('ch_game is None')
        if color != 'black' and color != 'white':
            raise WrongColorError(color)
        self.color = color
        self.num_of_game = ch_game.num
        if color == 'white':
            self.checkers = {pos: ChChecker('white', pos, ch_game) for pos in WHITE_START_POSITIONS}
        else:
            self.checkers = {pos: ChChecker('black', pos, ch_game) for pos in BLACK_START_POSITIONS}

    def make_move(self, from_pos: str, to_pos: str):
        """
        Makes move without any checking (manual use only for testing!)
        """
        if self.checkers.get(from_pos) is None:
            raise WrongMoveError('from')
        if to_pos not in TABLE_SQUARES:
            raise WrongMoveError('to')
        tmp_checker = self.checkers[from_pos]
        del self.checkers[from_pos]
        self.checkers[to_pos] = tmp_checker
        self.checkers[to_pos].position = to_pos


class ChTable:
    """
    Create New Table
    Must be ChGame obj for that thing!
    """
    def __init__(self, ch_game: ChGame):
        if ch_game is None:
            raise TypeError('ch_game is None')
        self.num_of_game = ch_game.num
        self.table = [[0] * 8 for i in range(8)]
        for posit in ch_game.white_player.checkers:
            i, j = self.inv_tab_access(posit)
            self.table[i][j] = 1
        for posit in ch_game.black_player.checkers:
            i, j = self.inv_tab_access(posit)
            self.table[i][j] = 2

    def __getitem__(self, item: str):
        if ('a' <= item[0] <= 'h') and ('1' <= item[1] <= '8'):
            i, j = self.inv_tab_access(item)
            return self.table[i][j]
        else:
            raise PositionError(item)

    def __setitem__(self, key, value):
        if ('a' <= key[0] <= 'h') and ('1' <= key[1] <= '8'):
            i, j = self.inv_tab_access(key)
            self.table[i][j] = value
        else:
            raise PositionError(key)

    def __iter__(self):
        for ch in COLUMNS_CHARS:
            for num in LINE_CHARS:
                yield (ch+str(num), self[ch+str(num)])

    def table_print(self):
        """
        Print all Table with lines and columns
        """
        lined_table = copy.deepcopy(self.table)
        for i in range(8):
            lined_table[7-i].insert(0, str(i + 1)+'|')
        lined_table.append([(', '.join(COLUMNS_CHARS)).rjust(27)])
        pprint.pprint(lined_table)

    @staticmethod
    def inv_tab_access(pos: str):
        """
        Returns the tuple (i, j) to access the needed square in list table
        """
        if ('a' <= pos[0] <= 'h') and ('1' <= pos[1] <= '8'):
            return 8 - int(pos[1]), ord(pos[0]) - ASCII_NUM - 1
        else:
            raise CheckerException('something wrong with inv method')

    @staticmethod
    def gen_fields(pos: str) -> str:
        """
        :param pos - position (str,str), ex. 'a1', 'h2':
        :return - 'a1', 'c1', 'a3, 'c3':
        """
        fields = [
            '{0}{1}'.format(chr(ord(pos[0]) + fst), chr(ord(pos[1]) + snd))
            for fst in range(-1, 2, 2) for snd in range(-1,2,2)
            if (ord('a') <= ord(pos[0]) + fst <= ord('h')) and (ord('1') <= ord(pos[1]) + snd <= ord('8'))
        ]
        yield from fields

    @staticmethod
    def gen_dgs(pos: str) -> str:
        """
        :param pos - position (str,str), ex. 'a1', 'h2':
        :return ['a1', 'b2', 'c3' ...]:
        """
        for sign in (1, -1):
            for t in (-1, 1):
                dg = []
                for i in range(t, 8 * t, t):
                    if (ord('a') <= ord(pos[0]) + i * sign <= ord('h')) and (ord('1') <= ord(pos[1]) + i <= ord('8')):
                        dg.append('{0}{1}'.format(chr(ord(pos[0]) + i * sign), chr(ord(pos[1]) + i)))
                    else:
                        break
                yield dg

    @staticmethod
    def next_on_dg(from_pos: str, to_pos: str, is_queen=False) -> [(str, str)]:
        delta = ord(to_pos[0]) - ord(from_pos[0]), ord(to_pos[1]) - ord(from_pos[1])
        new_pos = chr(ord(to_pos[0]) + delta[0]) + chr(ord(to_pos[1]) + delta[1])
        if not is_queen:
            return new_pos if 'a' <= new_pos[0] <= 'h' and '1' <= new_pos[1] <= '8' else -1
        else:
            fields = []
            while 'a' <= new_pos[0] <= 'h' and '1' <= new_pos[1] <= '8':
                fields.append(new_pos)
                new_pos = chr(ord(new_pos[0]) + delta[0]) + chr(ord(new_pos[1]) + delta[1])
            return fields if fields else -1


def main():
    i = input('Wanna play? Y/n')
    if i == 'Y':
        ChGame().play()


if __name__ == "__main__":
    main()