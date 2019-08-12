from kivy.app import App
from vdesign import *
from checkers import ChGame, BLACK_START_POSITIONS, WHITE_START_POSITIONS
from kivy.uix.button import Button
from chexceptions import *
# Config change
from kivy.config import Config

Config.set('graphics', 'resizable', '0')  # Config may be deleted in future
Config.set('graphics', 'width', 800)
Config.set('graphics', 'height', 640)


class NewGameButton(Button):
    pass


class VChecker(Widget):
    turn_all = {}
    move_flag = BooleanProperty(False)
    start_touch = ListProperty([None, None])
    delta = ListProperty([None, None])
    border = ListProperty([None, None, None, None])  # x left y top x right y bottom
    move = ListProperty([None, None])

    def __init__(self, color, border_pos_list, game, queen=False, **kwargs):
        self.turn_all[game.num] = 1
        self.border = border_pos_list
        self.num_of_game = game.num
        self.game_playing = game
        if kwargs.get("pos") is not None:
            pos = kwargs.pop('pos')
        else:
            raise PositionError()
        if kwargs.get("real_pos") is None:
            raise AttributeError
        self.real_pos = kwargs.pop('real_pos')
        print(f"real_pos={self.real_pos}, childcenter={self.center}")
        super().__init__(**kwargs)
        self.size_hint = (None, None)
        self.size = (60, 60)
        self.pos = pos[0] - self.size[0] / 2, pos[1] - self.size[1] / 2
        self.chcolor = color
        with self.canvas:
            self.ch = Ellipse(pos=self.pos, size=self.size)
            print(self.ch.pos, 'it is ELLIPSE BEGIN POS')
            self.ch.source = "data/{0}_ch{1}png".format(color, "_q." if queen else ".")
            print(self.ch.source)
            self.bind(pos=self.update_ch)
        print(self.x, self.y, self.right, self.top)

    def update_ch(self, *args):
        self.ch.pos = self.pos

    def become_queen(self):
        self.ch.source = "data/{0}_ch_q.png".format(self.chcolor)

    def on_touch_down(self, touch):
        if self.collide_point(*touch.pos):
            self.move = []
            if (self.turn_all[self.num_of_game] == 1 and self.chcolor == 'white') or \
               (self.turn_all[self.num_of_game] == 0 and self.chcolor == 'black'):
                parent = self.parent
                parent.remove_widget(self)
                parent.add_widget(self)
                self.move_flag = True
                self.move.append(self.real_pos)
                self.start_touch = touch.pos
                self.delta = self.start_touch[0] - self.center[0], self.start_touch[1] - self.center[1]

    def on_touch_move(self, touch):
        if self.move_flag and self.border[0] + self.width / 2 <= touch.x <= self.border[2] - self.width / 2 \
                and self.border[3] + self.height / 2 <= touch.y <= self.border[1] - self.height / 2:
            self.center = (touch.x - self.delta[0], touch.y - self.delta[1])
        elif self.move_flag and self.border[0] + self.width / 2 <= touch.x <= self.border[2] - self.width / 2:
            self.center = (touch.x - self.delta[0], self.center_y)
        elif self.move_flag and self.border[3] + self.height / 2 <= touch.y <= self.border[1] - self.height / 2:
            self.center = (self.center_x, touch.y - self.delta[1])

    def on_touch_up(self, touch):
        if self.move_flag:
            self.move_flag = False
            squares = []
            for child in self.parent.ids["MainTable"].children:
                if self.collide_widget(child):
                    squares.append((child.real_pos, child.center_x, child.center_y, child.col))
            squares_dist = list(
                map(lambda elem: ((elem[1] - self.center_x) ** 2 + (elem[2] - self.center_y) ** 2) ** 1 / 2,
                    squares))
            square = squares[squares_dist.index(min(squares_dist))][0]
            if squares[squares_dist.index(min(squares_dist))][3] == 'white' or square in self.parent.checkers.keys():
                for child in self.parent.ids["MainTable"].children:
                    if child.real_pos == self.real_pos:
                        Animation(pos=(child.center_x - self.width / 2, child.center_y - self.height / 2),
                                  duration=.3).start(self)
            else:
                self.move.append(square)
                print(self.move)
                answer = self.game_playing.check_move(move=tuple(self.move))
                print(answer)
                if answer[0] == 'N':
                    for child in self.parent.ids["MainTable"].children:
                        if child.real_pos == self.real_pos:
                            Animation(pos=(child.center_x - self.width / 2, child.center_y - self.height / 2),
                                      duration=.3).start(self)
                else:
                    if self.game_playing.new_queen_on:
                        self.become_queen()
                        self.game_playing.new_queen_on = False
                    pos = (squares[squares_dist.index(min(squares_dist))][1] - self.size[0] / 2,
                           squares[squares_dist.index(min(squares_dist))][2] - self.size[1] / 2)
                    Animation(pos=pos, duration=.3).start(self)
                    tmp_obj = self.parent.checkers.pop(self.real_pos)
                    self.parent.checkers[square] = tmp_obj
                    self.real_pos = square
                    if answer[1] == 'N':
                        self.turn_all[self.num_of_game] = (self.turn_all[self.num_of_game] + 1) % 2
                    if answer[2:4] != "--":
                        print(answer[2:4])
                        self.game_playing.animated_delete_checker(answer[2:4])
                    if answer[4] != 'P':
                        self.turn_all[self.num_of_game] = 2
                        StateAlert(answer[4]).open()


class MainGame(ChGame):
    run_games = 0

    def __init__(self, mainlayout: MainLayout, num_of_game=run_games):
        super().__init__(num_of_game)
        self.ml = mainlayout
        self.turn = 1
        self.last_res = ''
        self.end_move_flag = True
        self.all_moves = []
        self.must_eat_flag = False

    def game_ended(self):
        self.turn = 2
        self.run_games -= 1

    def run(self):
        self.__init__(self.ml, self.num)
        self.create_start()

    def create_start(self):
        print("ok new game")
        self.delete_all_checkers()
        for wh_pos in WHITE_START_POSITIONS:
            self.create_checker('white', real_pos=wh_pos)
        for bl_pos in BLACK_START_POSITIONS:
            self.create_checker('black', real_pos=bl_pos)

    def create_checker(self, color, **kwargs):
        queen = kwargs['queen'] if kwargs.get('queen') is not None else False
        print("Creating")
        stat_arg = (color, [self.ml.ids['Nums'].right,
                            self.ml.ids['Nums'].top,
                            self.ml.ids['Chars'].right,
                            self.ml.ids['Chars'].top])
        if kwargs.get('real_pos'):
            for child in self.ml.ids["MainTable"].children:
                if child.real_pos == kwargs['real_pos']:
                    checker = VChecker(*stat_arg,
                                       game=self,
                                       pos=child.center,
                                       real_pos=kwargs.pop('real_pos'))
                    self.ml.add_widget(checker)
                    break
            else:
                raise PositionError
        else:
            raise AttributeError
        self.ml.checkers[checker.real_pos] = checker

    def animated_delete_checker(self, real_pos, duration=.6):
        try:
            checker = self.ml.checkers.pop(real_pos)
        except KeyError:
            raise GameInternalError
        Animation(opacity=0, duration=duration).start(checker)
        Clock.schedule_once(lambda dt: self.ml.remove_widget(checker), duration + .1)

    def delete_all_checkers(self):
        for item in self.ml.checkers.values():
            self.ml.remove_widget(item)
            del item
        self.ml.checkers.clear()

    def check_move(self, move):
        """
        Main function to start the game,
        Random_moves is only for debug
        Returns -1 - Game Canceled
        Returns 0 - Game ended clearly
        """
        print("CHECKING YOUR MOVE ACTIVATED")
        if self.end_move_flag and self.last_res != 'N---':
            self.table_obj.table_print()
            self.all_moves, self.must_eat_flag = self.scan_all_moves('white') if self.turn == 1 else self.scan_all_moves('black')
        if not self.must_eat_flag:
            print(move, self.all_moves)
            if move not in self.all_moves:
                print('Illegal move, first break, make new')
                self.last_res = 'N---P'
                return self.last_res
            else:
                try:
                    self.make_move('white' if self.turn == 1 else 'black', move)
                except CheckerException as cherr:
                    print(cherr, 'Something Wrong with that', sep='\n')
                    self.last_res = 'N---P'
                    return self.last_res
                else:
                    self.last_res = 'YN--'
                    self.end_move_flag = True
                    self.turn = (self.turn + 1) % 2
                    return 'YN--' + self.check_result()
        else:
            short_moves = [(from_pos, to_pos) for from_pos, to_pos, eaten, in self.all_moves]
            if move not in short_moves:
                self.last_res = 'N---'
                print('Illegal move, make new')
                return self.last_res + 'P'
            try:
                last_checker = self.make_move('white' if self.turn == 1 else 'black',
                                              self.all_moves[short_moves.index(move)])
            except CheckerException as cherr:
                self.last_res = 'N---'
                print("Some Internal Error")
                return self.last_res
            if self.scan_checker(last_checker, True)[0] is None:
                self.last_res = ('YN' + self.all_moves[short_moves.index(move)][2])
                self.end_move_flag = True
                self.turn = (self.turn + 1) % 2
                return 'YN' + self.all_moves[short_moves.index(move)][2] + self.check_result()
            else:
                self.last_res = 'YS' + self.all_moves[short_moves.index(move)][2] + 'P'
                self.all_moves, self.must_eat_flag = self.scan_checker(last_checker, True)
                self.end_move_flag = False
                return self.last_res

    def check_result(self):
        """
        :param self:
        :return
        'D' = Draw
        'P' = Playing still
        'B' = Black Won
        'W' = White Won:
        """
        self.table_obj.table_print()
        if self.check_game_win() == 0:
            if self.check_game_draw_3_1() or self.check_game_draw_repeat():
                return 'D'
            return 'P'
        elif self.check_game_win() == 1:
            return 'W'
        elif self.check_game_win() == -1:
            return 'B'
        else:
            raise GameInternalError

# MainApp Class
class MainApp(App):
    def changeScreenToMain(self, dt):
        self.sm.current = "main"

    def build(self):
        self.sm = ScreenManagement()
        self.game = MainGame(self.sm.get_screen("main").ml)
        Clock.schedule_once(self.changeScreenToMain, 5)
        return self.sm


# Running part
def main():
    MainApp().run()


if __name__ == "__main__":
    main()