from kivy.uix.floatlayout import FloatLayout
from kivy.graphics import RenderContext, Color, Rectangle, BindTexture
from kivy.properties import NumericProperty, StringProperty
from kivy.clock import Clock

class GritShaderWidget(FloatLayout):
    grayscale_amount = NumericProperty(0.0)
    blue_light_filter = NumericProperty(0.0)
    zen_mode = NumericProperty(0.0)
    
    def __init__(self, **kwargs):
        self.canvas = RenderContext(use_parent_projection=True)
        # Load the shader
        with open('shaders/grit_effects.glsl', 'r') as f:
            self.canvas.shader.source = f.read()
        super(GritShaderWidget, self).__init__(**kwargs)
        
        with self.canvas:
            Color(1, 1, 1, 1)
            self.rect = Rectangle(size=self.size, pos=self.pos)
            
        self.bind(size=self._update_rect, pos=self._update_rect)
        Clock.schedule_interval(self.update_glsl, 1 / 60.)

    def _update_rect(self, *args):
        self.rect.size = self.size
        self.rect.pos = self.pos

    def update_glsl(self, dt):
        self.canvas['grayscale_amount'] = float(self.grayscale_amount)
        self.canvas['blue_light_filter'] = float(self.blue_light_filter)
        self.canvas['zen_mode'] = float(self.zen_mode)
        self.canvas['projection_mat'] = self.canvas.projection_mat
