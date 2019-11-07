"""R&D staff"""

__version__ = '0.2'

from glob import glob
from os.path import join, dirname
from kivy.app import App
from kivy.uix.image import Image
from kivy.logger import Logger
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.uix.recycleview import RecycleView
from kivy.properties import ObjectProperty
from kivy.properties import StringProperty
from kivy.config import Config


class MenuScreen(Screen):
    pass


class ListScreen(Screen):
    pass


class ListBases(RecycleView):
    def __init__(self, **kwargs):
        super(ListBases, self).__init__(**kwargs)
        self.data = [{'text': 'home1'}, {'text': 'home2'}]


class ImageScreen(Screen):
    def show_picture(self):
        image_box = self.children[0]
        print(image_box)
        image = image_box.children[1]
        print(image)
        image.clear_widgets()

        # Get any files into images directory
        curdir = dirname(__file__)
        for filename in glob(join(curdir, 'images', '*')):
            try:
                # load the image
                picture = Picture(source=filename)
                image.add_widget(picture)
            except Exception as e:
                Logger.exception('Pictures: Unable to load <%s>' % filename)
            print(filename)
            break


class Picture(Image):
    source = StringProperty(None)


class MnemoApp(App):
    def build(self):
        # Create the screen manager
        sm = ScreenManager()
        sm.add_widget(MenuScreen(name='menu'))
        sm.add_widget(ListScreen(name='list'))
        sm.add_widget(ImageScreen(name='image'))
        return sm


if __name__ == '__main__':
    # 1080x2160 pixels
    Config.set('graphics', 'width', 270)
    Config.set('graphics', 'height', 540)
    MnemoApp().run()
