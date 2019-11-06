"""R&D staff"""

__version__ = '0.1'

from glob import glob
from os.path import join, dirname
from kivy.app import App
from kivy.uix.scatter import Scatter
from kivy.logger import Logger
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.properties import ObjectProperty
from kivy.properties import StringProperty


class MenuScreen(Screen):
    pass


class ImageScreen(Screen):
    def show_picture(self):
        current = self.children[1]

        # Get any files into images directory
        curdir = dirname(__file__)
        for filename in glob(join(curdir, 'images', '*')):
            try:
                # load the image
                picture = Picture(source=filename, rotation=-90)
                print(picture.user_image.image_ratio)
                current.add_widget(picture)
            except Exception as e:
                Logger.exception('Pictures: Unable to load <%s>' % filename)
            print(filename)
            break


class Picture(Scatter):
    user_image = ObjectProperty()
    source = StringProperty(None)


class MnemoApp(App):
    def build(self):
        # Create the screen manager
        sm = ScreenManager()
        sm.add_widget(MenuScreen(name='menu'))
        sm.add_widget(ImageScreen(name='image'))
        return sm


if __name__ == '__main__':
    MnemoApp().run()
