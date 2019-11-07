"""R&D staff"""

__version__ = '0.21'

from glob import glob
from os.path import join, dirname
from kivy.app import App
from kivy.uix.scatter import Scatter
from kivy.logger import Logger
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
    def __init__(self, **kwargs):
        super(ImageScreen, self).__init__(**kwargs)
        self.image_base = 'home1'
        self.filenames = list()
        self.file_index = 0

        # Get any files into images directory
        curdir = dirname(__file__)
        for filename in glob(join(curdir, 'infoblocks', self.image_base, '*')):
            self.filenames.append(filename)

    def show_picture(self):
        # Find image parent
        image_box = self.children[0]
        image = image_box.children[1]
        image.clear_widgets()

        # load the image
        picture = Picture(source=self.filenames[self.file_index])
        image.add_widget(picture)
        self.file_index += 1
        if self.file_index >= len(self.filenames):
            self.file_index = 0


class Picture(Scatter):
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
