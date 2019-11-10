"""Chess training application"""

__version__ = '0.01'

from glob import glob, os
from os.path import join, dirname
from random import shuffle, randint
from kivy.app import App
from kivy.clock import Clock
from kivy.uix.scatter import Scatter
from kivy.uix.recycleview.views import RecycleDataViewBehavior
from kivy.uix.button import Button
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.uix.recycleview import RecycleView
from kivy.properties import ObjectProperty
from kivy.properties import StringProperty
from kivy.uix.popup import Popup
from kivy.graphics.svg import Svg
from kivy.core.window import Window
from kivy.uix.relativelayout import RelativeLayout
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.label import Label
import chess
import chess.svg


class MenuScreen(Screen):
    pass


class LessonScreen(Screen):
    def __init__(self, **kwargs):
        super(LessonScreen, self).__init__(**kwargs)

        image_box = self.children[0]
        self.image_parent = image_box.children[1]

    def clear_board(self):
        self.image_parent.clear_widgets()

    # def show_board(self):
    #     self.clear_board()
    #     board = chess.Board()
    #
    #     svg_code = chess.svg.board()
    #
    #     filename = 'tmp.svg'
    #     with open(filename, 'w') as outfile:
    #         outfile.write(svg_code)
    #
    #     svg = SvgWidget(filename)
    #
    #     print(self.image_parent)
    #     self.image_parent.add_widget(svg)
    #     svg.center = Window.center

    def show_board(self):
        self.clear_board()

        board = chess.Board()
        text_board = TextBoard()
        text_board.text = str(board)
        self.image_parent.add_widget(text_board)


class TextBoard(Label):
    pass


class SvgWidget(Scatter):
    def __init__(self, filename, **kwargs):
        super(SvgWidget, self).__init__(**kwargs)
        with self.canvas:
            svg = Svg(filename)
        self.size = svg.width, svg.height


class ChessApp(App):
    def __init__(self, **kwargs):
        super(ChessApp, self).__init__(**kwargs)
        self.sm = ScreenManager()

    def build(self):
        self.sm.add_widget(MenuScreen(name='menu'))
        self.sm.add_widget(LessonScreen(name='lesson'))

        return self.sm


if __name__ == '__main__':
    ChessApp().run()
