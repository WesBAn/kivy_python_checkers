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


class MainLayout(FloatLayout):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.checkers = {}


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

