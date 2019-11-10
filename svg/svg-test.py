from kivy.config import Config
Config.set('kivy', 'log_level', 'debug')

from kivy.app import App
from kivy.lang import Builder
from kivy.uix.floatlayout import FloatLayout
from kivy.graphics.svg import Svg
from kivy.uix.scatter import Scatter
from kivy.core.window import Window


kv = """
<SvgWidget>:
    do_rotation: False
<FloatLayout>:
    canvas.before:
        Color:
            rgb: (0.75, 0.75, 0.75)
        Rectangle:
            pos: self.pos
            size: self.size
"""


class SvgWidget(Scatter):
    def __init__(self, filename, **kwargs):
        super(SvgWidget, self).__init__(**kwargs)
        with self.canvas:
            svg = Svg(filename)
        self.size = svg.width, svg.height


class TestApp(App):
    def build(self):
        self.root = FloatLayout()

        filename = 'cloud.svg'
        svg = SvgWidget(filename, size_hint=(None, None))
        self.root.add_widget(svg)
        svg.scale = 2.
        svg.center = Window.center


if __name__ == '__main__':
    Builder.load_string(kv)
    TestApp().run()