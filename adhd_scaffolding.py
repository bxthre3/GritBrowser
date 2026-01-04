from kivy.uix.floatlayout import FloatLayout
from kivy.uix.label import Label
from kivy.uix.boxlayout import BoxLayout
from kivy.graphics import Color, Rectangle
from kivy.properties import StringProperty, ListProperty

class TaskPagingOverlay(FloatLayout):
    current_task = StringProperty("Focus on the current objective")
    
    def __init__(self, **kwargs):
        super(TaskPagingOverlay, self).__init__(**kwargs)
        # Semi-transparent cage for URL bar area
        with self.canvas.before:
            Color(0, 0, 0, 0.7)
            self.rect = Rectangle(size=(800, 60), pos=(0, 540)) # Simulated URL bar position
            
        self.task_label = Label(
            text=self.current_task,
            pos_hint={'center_x': 0.5, 'top': 0.98},
            size_hint=(1, 0.05),
            color=[1, 1, 0, 1], # High visibility yellow
            bold=True
        )
        self.add_widget(self.task_label)
        self.bind(size=self._update_rect, pos=self._update_rect)

    def _update_rect(self, *args):
        self.rect.pos = (self.x, self.top - 60)
        self.rect.size = (self.width, 60)

    def update_task(self, task_text):
        self.current_task = task_text
        self.task_label.text = task_text

class FactCatcherSidebar(BoxLayout):
    facts = ListProperty([])
    
    def __init__(self, **kwargs):
        super(FactCatcherSidebar, self).__init__(**kwargs)
        self.orientation = 'vertical'
        self.size_hint_x = 0.25
        self.padding = 10
        with self.canvas.before:
            Color(0.1, 0.1, 0.1, 1)
            self.rect = Rectangle(size=self.size, pos=self.pos)
        
        self.add_widget(Label(text="FACT CATCHER", bold=True, size_hint_y=None, height=40))
        self.facts_container = BoxLayout(orientation='vertical', spacing=5)
        self.add_widget(self.facts_container)
        self.bind(size=self._update_rect, pos=self._update_rect)

    def _update_rect(self, *args):
        self.rect.pos = self.pos
        self.rect.size = self.size
        
    def add_fact(self, fact_text):
        self.facts.append(fact_text)
        new_fact = Label(text=f"• {fact_text}", text_size=(self.width-20, None), halign='left')
        self.facts_container.add_widget(new_fact)

class TunnelWindow(BoxLayout):
    # Simulated PWA "Caging"
    def __init__(self, url, **kwargs):
        super(TunnelWindow, self).__init__(**kwargs)
        self.orientation = 'vertical'
        self.add_widget(Label(text=f"TUNNEL: {url}", bold=True))
        # In a real app, this would be a chromeless window
