"""R&D staff"""

__version__ = '0.42'

from glob import glob, os
from os.path import join, dirname
from random import shuffle
from kivy.app import App
from kivy.clock import Clock
from kivy.uix.scatter import Scatter
from kivy.uix.recycleview.views import RecycleDataViewBehavior
from kivy.uix.button import Button
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.uix.recycleview import RecycleView
from kivy.properties import ObjectProperty
from kivy.properties import StringProperty
from kivy.config import Config


class MenuScreen(Screen):
    pass


class LessonsScreen(Screen):
    text = StringProperty(None)

    def __init__(self, **kwargs):
        super(LessonsScreen, self).__init__(**kwargs)
        self.lesson_file = ''
        self.text = ''

    def on_pre_enter(self):
        current_dir = dirname(__file__)
        file_path = join(current_dir, 'lessons', self.lesson_file)

        with open(file_path, encoding="utf8") as fobj:
            for line in fobj:
                self.text += line


class LessonsListScreen(Screen):
    pass


class LessonButton(RecycleDataViewBehavior, Button):
    def on_press(self):
        App.get_running_app().switch_to_lesson(base=self.text)


class ListLessons(RecycleView):
    def __init__(self, **kwargs):
        super(ListLessons, self).__init__(**kwargs)
        self.data = list()
        current_dir = dirname(__file__)
        for dir_name in sorted(os.listdir(join(current_dir, 'lessons'))):
            self.data.append({'text': dir_name})


class BaseImageScreen(Screen):
    """Handles screen for Base images"""
    def __init__(self, **kwargs):
        super(BaseImageScreen, self).__init__(**kwargs)
        self.filenames = None
        self.image_base = ''
        self.file_index = dict()

        image_box = self.children[0]
        self.image_parent = image_box.children[1]

        self.initial = 0

    def prepare_filenames(self):
        if not self.filenames:
            self.filenames = dict()
            current_dir = dirname(__file__)
            for dir_name in sorted(os.listdir(join(current_dir, 'infoblocks'))):
                self.filenames[dir_name] = list()
                for filename in sorted(glob(join(current_dir, 'infoblocks', dir_name, '*'))):
                    self.filenames[dir_name].append(filename)

    # def on_touch_down(self, touch):
    #     if touch.y > 100:
    #         self.initial = touch.x
    #     else:
    #         pass
    #
    # def on_touch_up(self, touch):
    #     if touch.y > 100:
    #         # Swipe right
    #         if (touch.x - self.initial) > 100:
    #             self.initial = 0
    #             self.show_next_image()
    #
    #         # Swipe left
    #         if (self.initial - touch.x) > 100:
    #             self.initial = 0
    #             self.show_previous_image()
    #     else:
    #         pass

    def clear_image(self):
        self.image_parent.clear_widgets()

    def show_previous_image(self):
        self.prepare_filenames()
        self.clear_image()

        if self.image_base not in self.file_index.keys():
            self.file_index[self.image_base] = 0

        self.file_index[self.image_base] -= 1
        if self.file_index[self.image_base] < 0:
            self.file_index[self.image_base] = len(self.filenames[self.image_base])-1

        picture = Picture(source=self.filenames[self.image_base][self.file_index[self.image_base]])
        self.image_parent.add_widget(picture)

    def show_next_image(self):
        self.prepare_filenames()
        self.clear_image()

        if self.image_base not in self.file_index.keys():
            self.file_index[self.image_base] = 0

        self.file_index[self.image_base] += 1
        if self.file_index[self.image_base] >= len(self.filenames[self.image_base]):
            self.file_index[self.image_base] = 0

        picture = Picture(source=self.filenames[self.image_base][self.file_index[self.image_base]])
        self.image_parent.add_widget(picture)


class BasesListScreen(Screen):
    pass


class BaseButton(RecycleDataViewBehavior, Button):
    def on_press(self):
        App.get_running_app().switch_to_image(base=self.text)


class ListBases(RecycleView):
    def __init__(self, **kwargs):
        super(ListBases, self).__init__(**kwargs)
        self.data = list()
        current_dir = dirname(__file__)
        for dir_name in sorted(os.listdir(join(current_dir, 'infoblocks'))):
            self.data.append({'text': dir_name})


class NumberScreen(Screen):
    """Handles screen for Number codes"""
    user_input = ObjectProperty()

    def __init__(self, **kwargs):
        super(NumberScreen, self).__init__(**kwargs)
        self.filenames = None
        self.index = 0
        self.event = None
        self.timeout = 5
        image_box = self.children[0]
        self.image_parent = image_box.children[1]

    def clear_image(self):
        self.image_parent.clear_widgets()

    def show_image(self, dt=None):
        self.clear_image()

        # Load the image
        picture = Picture(source=self.filenames[self.index])
        self.index += 1
        if self.index >= len(self.filenames):
            self.index = 0
            shuffle(self.filenames)

        self.image_parent.add_widget(picture)

    def on_leave(self):
        if self.event:
            self.event.cancel()

    def update_timeout(self):
        self.timeout = int(self.user_input.text)
        if self.event:
            self.event.cancel()
            self.event = Clock.schedule_interval(self.show_image, self.timeout)

    def pause(self):
        if self.event:
            self.event.cancel()
            self.event = None
        else:
            self.event = Clock.schedule_interval(self.show_image, self.timeout)

    def on_pre_enter(self):
        if not self.filenames:
            self.filenames = list()
            current_dir = dirname(__file__)
            for filename in sorted(glob(join(current_dir, 'numbers', '*'))):
                self.filenames.append(filename)
        self.clear_image()
        self.show_image()

    def on_enter(self):
        shuffle(self.filenames)
        self.event = Clock.schedule_interval(self.show_image, self.timeout)


class Picture(Scatter):
    source = StringProperty(None)


class NumberTrainingScreen(Screen):
    output = ObjectProperty()
    user_input_timeout = ObjectProperty()
    user_input_limit = ObjectProperty()

    def __init__(self, **kwargs):
        super(NumberTrainingScreen, self).__init__(**kwargs)
        self.codes = list()
        for i in range(100):
            if i < 10:
                code = '0' + str(i)
            else:
                code = str(i)
            self.codes.append(code)
        self.index = 0
        self.event = None
        self.timeout = 7
        self.limit = 10

    def start(self):
        self.output.text = '..'
        shuffle(self.codes)
        self.event = Clock.schedule_interval(self.show_code, self.timeout)

    def show_code(self, dt=None):
        self.output.text = self.codes[self.index]
        self.index += 1
        if self.index >= self.limit:
            self.event.cancel()
            self.event = Clock.schedule_once(self.check_codes, self.timeout)

    def check_codes(self, dt=None):
        self.index = 0
        self.output.text = ''

    def update_timeout(self):
        self.timeout = int(self.user_input_timeout.text)
        self.limit = int(self.user_input_limit.text)

    def on_pre_enter(self):
        self.output.text = ''
        self.user_input_timeout.text = str(self.timeout)
        self.user_input_limit.text = str(self.limit)


class MnemoApp(App):
    def __init__(self, **kwargs):
        super(MnemoApp, self).__init__(**kwargs)
        self.sm = ScreenManager()

    def build(self):
        # Create the screen manager
        self.sm.add_widget(MenuScreen(name='menu'))
        self.sm.add_widget(BasesListScreen(name='bases_list'))
        self.sm.add_widget(BaseImageScreen(name='image'))
        self.sm.add_widget(NumberScreen(name='number'))
        self.sm.add_widget(LessonsListScreen(name='lessons_list'))
        self.sm.add_widget(LessonsScreen(name='lessons'))
        self.sm.add_widget(NumberTrainingScreen(name='number_training'))
        return self.sm

    def switch_to_image(self, base=''):
        self.sm.screens[2].clear_image()
        self.sm.screens[2].image_base = base
        self.sm.screens[2].file_index[base] = -1
        self.sm.screens[2].show_next_image()
        self.sm.current = 'image'

    def switch_to_lesson(self, base=''):
        self.sm.screens[5].lesson_file = base
        self.sm.current = 'lessons'


if __name__ == '__main__':
    # 1080x2160 pixels
    # Config.set('graphics', 'width', 500)
    # Config.set('graphics', 'height', 1000)
    MnemoApp().run()
