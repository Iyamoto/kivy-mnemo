"""R&D staff"""

__version__ = '0.22'

from glob import glob, os
from os.path import join, dirname
from kivy.app import App
from kivy.uix.scatter import Scatter
from kivy.uix.recycleview.views import RecycleDataViewBehavior
from kivy.uix.button import Button
from kivy.uix.recycleboxlayout import RecycleBoxLayout
from kivy.uix.behaviors import FocusBehavior
from kivy.uix.recycleview.layout import LayoutSelectionBehavior
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.uix.recycleview import RecycleView
from kivy.properties import ObjectProperty
from kivy.properties import StringProperty
from kivy.config import Config


class MenuScreen(Screen):
    pass


class ListScreen(Screen):
    pass


class SelectableRecycleBoxLayout(FocusBehavior, LayoutSelectionBehavior, RecycleBoxLayout):
    """ Adds selection and focus behaviour to the view. """
    pass


class SelectableButton(RecycleDataViewBehavior, Button):
    """ Add selection support to the Button"""
    index = None

    def refresh_view_attrs(self, rv, index, data):
        """ Catch and handle the view changes """
        self.index = index
        return super(SelectableButton, self).refresh_view_attrs(rv, index, data)

    def on_release(self):
        App.get_running_app().switch_to_image(base=self.text)


class ListBases(RecycleView):
    rv_layout = ObjectProperty(None)

    def __init__(self, **kwargs):
        super(ListBases, self).__init__(**kwargs)
        self.data = list()
        current_dir = dirname(__file__)
        for filename in os.listdir(join(current_dir, 'infoblocks')):
            self.data.append({'text': filename})


class ImageScreen(Screen):
    def __init__(self, **kwargs):
        super(ImageScreen, self).__init__(**kwargs)
        self.image_base = ''
        self.file_index = dict()
        self.filenames = dict()

    def clear_image(self):
        # Find image parent
        image_box = self.children[0]
        image = image_box.children[1]
        image.clear_widgets()

    def show_image(self):

        if self.image_base:

            # Get any files into images directory
            if self.image_base not in self.filenames.keys():
                self.filenames[self.image_base] = list()
                current_dir = dirname(__file__)
                for filename in glob(join(current_dir, 'infoblocks', self.image_base, '*')):
                    self.filenames[self.image_base].append(filename)

            # Find image parent
            image_box = self.children[0]
            image = image_box.children[1]
            image.clear_widgets()

            # Load the image
            if self.image_base not in self.file_index.keys():
                self.file_index[self.image_base] = 0

            picture = Picture(source=self.filenames[self.image_base][self.file_index[self.image_base]])
            image.add_widget(picture)

            self.file_index[self.image_base] += 1
            if self.file_index[self.image_base] >= len(self.filenames[self.image_base]):
                self.file_index[self.image_base] = 0


class Picture(Scatter):
    source = StringProperty(None)


class MnemoApp(App):
    def __init__(self, **kwargs):
        super(MnemoApp, self).__init__(**kwargs)
        self.sm = ScreenManager()

    def build(self):
        # Create the screen manager
        self.sm.add_widget(MenuScreen(name='menu'))
        self.sm.add_widget(ListScreen(name='list'))
        self.sm.add_widget(ImageScreen(name='image'))
        return self.sm

    def switch_to_image(self, base=''):
        self.sm.screens[2].clear_image()
        self.sm.screens[2].image_base = base
        self.sm.screens[2].file_index[base] = 0
        self.sm.screens[2].show_image()
        self.sm.current = 'image'


if __name__ == '__main__':
    # 1080x2160 pixels
    Config.set('graphics', 'width', 270)
    Config.set('graphics', 'height', 540)
    MnemoApp().run()
