import time
import numpy as np
import threading
from PIL import Image
from kivy.graphics import Fbo, ClearColor, ClearWindow, Rectangle, Color
from kivy.clock import Clock
from kivy.uix.widget import Widget
from kivy.uix.behaviors import FocusBehavior
from kivy.properties import NumericProperty, StringProperty, BooleanProperty

class GritEngine(Widget, FocusBehavior):
    velocity = NumericProperty(0)
    image_delta = NumericProperty(0)
    current_gear = NumericProperty(10)
    capture_interval = NumericProperty(0.2)
    url = StringProperty("https://www.google.com")
    is_processing = BooleanProperty(False)
    
    def __init__(self, **kwargs):
        super(GritEngine, self).__init__(**kwargs)
        self.fbo = None
        self.last_texture_data = None
        self.gear_map = {
            10: 0.2, 9: 0.5, 8: 1.0, 7: 2.0,
            6: 10.0, 5: 30.0, 4: 60.0,
            3: 180.0, 2: 450.0, 1: 900.0
        }
        Clock.schedule_once(self.init_fbo, 0)
        Clock.schedule_interval(self.adaptive_loop, self.capture_interval)

    def init_fbo(self, dt):
        with self.canvas:
            self.fbo = Fbo(size=self.size)
            with self.fbo:
                ClearColor(0.05, 0.05, 0.05, 1)
                ClearWindow()
                Color(1, 1, 1, 1)
                self.fbo_rect = Rectangle(size=self.size, pos=self.pos)
            
    def adaptive_loop(self, dt):
        if self.is_processing or not self.fbo:
            return
            
        # GPU-accelerated texture capture (must be on main thread)
        self.fbo.draw()
        pixels = self.fbo.pixels
        size = self.size
        
        # Offload Delta calculation to background thread for 60FPS UI
        self.is_processing = True
        threading.Thread(target=self.process_frame, args=(pixels, size)).start()

    def process_frame(self, pixels, size):
        try:
            w, h = size if size[0] > 0 else (800, 600)
            img = Image.frombytes('RGBA', (int(w), int(h)), pixels).convert('L').resize((8, 8))
            
            if self.last_texture_data is not None:
                last_img = Image.frombytes('RGBA', (int(w), int(h)), self.last_texture_data).convert('L').resize((8, 8))
                arr1 = np.array(img, dtype=np.float32)
                arr2 = np.array(last_img, dtype=np.float32)
                mse = np.mean((arr1 - arr2) ** 2)
                delta = mse / 255.0
            else:
                delta = 0
                
            self.last_texture_data = pixels
            
            # Update UI properties on main thread
            Clock.schedule_once(lambda dt: self.update_engine_state(delta))
        except Exception as e:
            print(f"Engine Error: {e}")
            Clock.schedule_once(lambda dt: setattr(self, 'is_processing', False))

    def update_engine_state(self, delta):
        self.image_delta = delta
        score = (self.velocity * 0.4) + (self.image_delta * 0.6)
        new_gear = int(max(1, min(10, score * 100)))
        self.current_gear = new_gear
        
        new_interval = self.gear_map.get(self.current_gear, 0.2)
        if abs(new_interval - self.capture_interval) > 0.01:
            self.capture_interval = new_interval
            Clock.unschedule(self.adaptive_loop)
            Clock.schedule_interval(self.adaptive_loop, self.capture_interval)
            
        self.is_processing = False

    def on_touch_down(self, touch):
        if self.collide_point(*touch.pos):
            self.update_velocity(0.2)
            return super().on_touch_down(touch)
        return False

    def update_velocity(self, v):
        self.velocity = min(1.0, self.velocity + v)
        Clock.schedule_once(lambda dt: setattr(self, 'velocity', max(0, self.velocity - 0.05)), 1.0)

    def navigate(self, url):
        self.url = url
        self.update_velocity(0.5)
