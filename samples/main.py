"""R&D staff"""

__version__ = '0.1'

import kivy
from kivy.app import App
from kivy.uix.boxlayout import BoxLayout


class MainMenu(BoxLayout):
    def search_location(self):
        print("Pressed")


class MnemoApp(App):
    pass


if __name__ == '__main__':
    MnemoApp().run()
