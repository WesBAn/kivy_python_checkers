# Main app import
from kivy import require as kivy_require
kivy_require("1.11.0")

# UIX imports
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.gridlayout import GridLayout
from kivy.uix.label import Label
from kivy.uix.widget import Widget
from kivy.uix.button import Button
from kivy.uix.image import Image
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.popup import Popup
# other imports
from kivy.clock import Clock
from kivy.graphics import Color, Ellipse
from kivy.properties import BooleanProperty, ListProperty, StringProperty
from kivy.animation import Animation


# ScreenManagement
class WelcomeScreen(Screen):
    pass


class MainScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.ml = MainLayout()
        self.add_widget(self.ml)


class SettingsScreen(Screen):
    pass


class ScreenManagement(ScreenManager):
    pass


# ////////////////////////////
# Visual Checkers
# Protocol !!!!
# class VChecker(Widget):
#     move_flag = BooleanProperty(False)
#     start_touch = ListProperty([None, None])
#     delta = ListProperty([None, None])
#     border = ListProperty([None, None, None, None])  # x left y top x right y bottom
#     move = ListProperty([None, None])
#
#     def __init__(self, color, border_pos_list, queen=False, **kwargs):
#         # type(Widget).__init__(**kwargs) - for multiply
#         self.border = border_pos_list
#         if kwargs.get("pos") is not None:
#             pos = kwargs.pop('pos')
#         else:
#             raise PositionError()
#         if kwargs.get("real_pos") is None:
#             raise AttributeError
#         self.real_pos = kwargs.pop('real_pos')
#         print(f"real_pos={self.real_pos}, childcenter={self.center}")
#         super().__init__(**kwargs)
#         self.size_hint = (None, None)
#         self.size = (60, 60)
#         self.pos = pos[0] - self.size[0] / 2, pos[1] - self.size[1] / 2
#         with self.canvas:
#             self.ch = Ellipse(pos=self.pos, size=self.size)
#             print(self.ch.pos, 'it is ELLIPSE BEGIN POS')
#             self.ch.source = "data/{0}_ch{1}png".format(color, "_q." if queen else ".")
#             print(self.ch.source)
#             self.bind(pos=self.update_ch)
#         print(self.x, self.y, self.right, self.top)
#
#     def update_ch(self, *args):
#         self.ch.pos = self.pos
#         print(self.ch.pos, 'it is ELLIPSE NOW POS')
#
#     def on_touch_down(self, touch):
#         if self.collide_point(*touch.pos):
#             self.move = []
#             parent = self.parent
#             parent.remove_widget(self)
#             parent.add_widget(self)
#             self.move_flag = True
#             self.move.append(self.real_pos)
#             self.start_touch = touch.pos
#             self.delta = self.start_touch[0] - self.center[0], self.start_touch[1] - self.center[1]
#
#     def on_touch_move(self, touch):
#         if self.move_flag and self.border[0] + self.width / 2 <= touch.x <= self.border[2] - self.width / 2 \
#                 and self.border[3] + self.height / 2 <= touch.y <= self.border[1] - self.height / 2:
#             print(touch.x, touch.y)
#             self.center = (touch.x - self.delta[0], touch.y - self.delta[1])
#         elif self.move_flag and self.border[0] + self.width / 2 <= touch.x <= self.border[2] - self.width / 2:
#             self.center = (touch.x - self.delta[0], self.center_y)
#         elif self.move_flag and self.border[3] + self.height / 2 <= touch.y <= self.border[1] - self.height / 2:
#             self.center = (self.center_x, touch.y - self.delta[1])
#
#     def on_touch_up(self, touch):
#         if self.move_flag:
#             self.move_flag = False
#             squares = []
#             for child in self.parent.ids["MainTable"].children:
#                 if self.collide_widget(child):
#                     squares.append((child.real_pos, child.center_x, child.center_y, child.col))
#             squares_dist = list(
#                 map(lambda elem: ((elem[1] - self.center_x) ** 2 + (elem[2] - self.center_y) ** 2) ** 1 / 2,
#                     squares))
#             square = squares[squares_dist.index(min(squares_dist))][0]
#             if squares[squares_dist.index(min(squares_dist))][3] == 'white' or square in self.parent.checkers.keys():
#                 for child in self.parent.ids["MainTable"].children:
#                     if child.real_pos == self.real_pos:
#                         Animation(pos=(child.center_x - self.width / 2, child.center_y - self.height / 2),
#                                   duration=.3).start(self)
#             else:
#                 self.move.append(square)
#                 pos = (squares[squares_dist.index(min(squares_dist))][1] - self.size[0] / 2,
#                        squares[squares_dist.index(min(squares_dist))][2] - self.size[1] / 2)
#                 Animation(pos=pos, duration=.3).start(self)
#                 tmp_obj = self.parent.checkers.pop(self.real_pos)
#                 self.parent.checkers[square] = tmp_obj
#                 self.real_pos = square

# ///////////////////////////
# All elements in MainScreen

class MainLayout(FloatLayout):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.checkers = {}

    # def create_start(self):
    #     print("ok new game")
    #     self.delete_all_checkers()
    #     for wh_pos in WHITE_START_POSITIONS:
    #         self.create_checker('white', real_pos=wh_pos)
    #     for bl_pos in BLACK_START_POSITIONS:
    #         self.create_checker('black', real_pos=bl_pos)
    #
    # def create_checker(self, color, **kwargs):
    #     checker = ""
    #     queen = kwargs['queen'] if kwargs.get('queen') is not None else False
    #     stat_arg = (color, [self.ids['Nums'].right,
    #                         self.ids['Nums'].top,
    #                         self.ids['Chars'].right,
    #                         self.ids['Chars'].top])
    #     if kwargs.get('real_pos'):
    #         for child in self.ids["MainTable"].children:
    #             if child.real_pos == kwargs['real_pos']:
    #                 checker = VChecker(*stat_arg, pos=child.center, real_pos=kwargs.pop('real_pos'))
    #                 self.add_widget(checker)
    #                 break
    #         else:
    #             raise PositionError
    #     else:
    #         raise AttributeError
    #     self.checkers[checker.real_pos] = checker
    #
    # def animated_delete_checker(self, real_pos, duration=1.5):
    #     for child in self.ids["MainTable"].children:
    #         if child.real_pos == real_pos:
    #             checker = self.checkers.pop(child.real_pos)
    #             Animation(opacity=0, duration=duration).start(checker)
    #             Clock.schedule_once(lambda dt: self.remove_widget(checker), duration + .1)
    #             break
    #     else:
    #         raise PositionError
    #
    # def delete_all_checkers(self):
    #     for item in self.checkers.values():
    #         self.remove_widget(item)
    #         del item
    #     self.checkers.clear()


# ///////////////////////////

# Nums and Chars rows
class NumsRow(BoxLayout):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        for i in range(8):
            self.add_widget(Label(text="{0}".format(8 - i),
                                  text_size=self.size,
                                  halign='center',
                                  valign='center',
                                  font_name='data/font/helvetica.ttf',
                                  font_size=20,
                                  color=[0, 0, 0, 1]))


class CharsRow(BoxLayout):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        for st in "abcdefgh":
            self.add_widget(Label(text=st,
                                  text_size=self.size,
                                  halign='center',
                                  valign='center',
                                  font_name='data/font/helvetica.ttf',
                                  font_size=20,
                                  color=[0, 0, 0, 1]))


# ///////////////////////////
# Table Configuration
class SquareImage(Image):
    def __init__(self, color: str, real_pos, **kwargs):
        super().__init__(**kwargs)
        self.col = color
        self.source = "data/white.png" if color == 'white' else "data/black.png"
        self.real_pos = real_pos
        print(self.real_pos)


class Table(GridLayout):
    cols = "abcdefgh"
    lines = "12345678"

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        color = ("white", "black")
        for j in range(8):
            st_color_ind = j % 2
            for i in range(8):
                self.add_widget(SquareImage(color[st_color_ind] if i % 2 == 0 else color[(st_color_ind + 1) % 2],
                                            self.cols[i] + self.lines[7 - j]))


class StateAlert(Popup):

    def __init__(self, choice):
        super().__init__()
        self.states = {'D': 'Draw', 'W': 'White Won', 'B': 'Black Won'}
        self.bl = BoxLayout(orientation='vertical')
        lbl = Label(text_size=self.size,
                    halign='center',
                    valign='middle',
                    font_name='data/font/helvetica.ttf',
                    font_size=50,
                    color=[1, 1, 1, 1],
                    text=self.states[choice],
                    size_hint=(1, .8))
        button = Button(background_color=(1, 1, 1, 1),
                        background_normal="",
                        text="Принять",
                        color=(0, 0, 0, 1),
                        size_hint=(1, .2),
                        on_release=self.dismiss)
        self.bl.add_widget(lbl)
        self.bl.add_widget(button)
        self.content = self.bl

