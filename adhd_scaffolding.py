from kivy.uix.floatlayout import FloatLayout
from kivy.uix.label import Label
from kivy.uix.boxlayout import BoxLayout
from kivy.graphics import Color, Rectangle, Line
from kivy.properties import StringProperty, ListProperty, NumericProperty
from kivy.animation import Animation

class TaskPagingOverlay(FloatLayout):
    current_task = StringProperty("INITIALIZING NEURO-SCAFFOLD...")
    cage_opacity = NumericProperty(0.7)
    
    def __init__(self, **kwargs):
        super(TaskPagingOverlay, self).__init__(**kwargs)
        with self.canvas.before:
            self.cage_color = Color(0, 0, 0, self.cage_opacity)
            self.rect = Rectangle(size=(800, 60), pos=(0, 540))
            Color(0.2, 0.6, 1, 0.5) # Blue glow for the cage edge
            self.border = Line(rectangle=(0, 540, 800, 60), width=1.5)
            
        self.task_label = Label(
            text=self.current_task,
            pos_hint={'center_x': 0.5, 'top': 0.98},
            size_hint=(1, 0.05),
            color=[0, 1, 0.8, 1], # Cyan for engineering feel
            font_name='Roboto',
            bold=True,
            font_size='14sp'
        )
        self.add_widget(self.task_label)
        self.bind(size=self._update_rect, pos=self._update_rect)

    def _update_rect(self, *args):
        # Physically cage the top 60dp (URL bar area)
        self.rect.pos = (self.x, self.top - 60)
        self.rect.size = (self.width, 60)
        self.border.rectangle = (self.x, self.top - 60, self.width, 60)

    def update_task(self, task_text):
        self.current_task = task_text.upper()
        self.task_label.text = self.current_task
        # Pulse animation on task change
        anim = Animation(cage_opacity=0.9, duration=0.2) + Animation(cage_opacity=0.7, duration=0.5)
        anim.start(self)

class TunnelWindow(BoxLayout):
    # One-click PWA "Caging" to launch URLs as chrome-less standalone windows
    def __init__(self, url, **kwargs):
        super(TunnelWindow, self).__init__(**kwargs)
        self.orientation = 'vertical'
        self.padding = 2
        with self.canvas.before:
            Color(0.05, 0.05, 0.05, 1)
            self.bg = Rectangle(size=self.size, pos=self.pos)
            Color(0.2, 0.6, 1, 1)
            self.border = Line(rectangle=(self.x, self.y, self.width, self.height), width=2)
            
        header = BoxLayout(size_hint_y=None, height='30dp', padding='5dp')
        header.add_widget(Label(text=f"TUNNEL: {url}", font_size='12sp', bold=True, halign='left'))
        self.add_widget(header)
        
        # Simulated Web Content Area
        self.add_widget(Label(text="[SECURE TUNNEL ACTIVE]", color=[0.5, 0.5, 0.5, 1]))
        
        self.bind(size=self._update_rect, pos=self._update_rect)

    def _update_rect(self, *args):
        self.bg.pos = self.pos
        self.bg.size = self.size
        self.border.rectangle = (self.x, self.y, self.width, self.height)

class FactCatcherSidebar(BoxLayout):
    facts = ListProperty([])
    
    def __init__(self, **kwargs):
        super(FactCatcherSidebar, self).__init__(**kwargs)
        self.orientation = 'vertical'
        self.size_hint_x = 0.25
        self.padding = 10
        self.spacing = 10
        with self.canvas.before:
            Color(0.08, 0.08, 0.08, 1)
            self.rect = Rectangle(size=self.size, pos=self.pos)
            Color(0.2, 0.2, 0.2, 1)
            self.line = Line(points=[self.x, self.y, self.x, self.top], width=1)
        
        self.add_widget(Label(text="FACT CATCHER", bold=True, size_hint_y=None, height=40, color=[0.2, 0.6, 1, 1]))
        self.facts_container = BoxLayout(orientation='vertical', spacing=5)
        self.add_widget(self.facts_container)
        self.bind(size=self._update_rect, pos=self._update_rect)

    def _update_rect(self, *args):
        self.rect.pos = self.pos
        self.rect.size = self.size
        self.line.points = [self.x, self.y, self.x, self.top]
        
    def add_fact(self, fact_text):
        self.facts.append(fact_text)
        new_fact = Label(
            text=f"• {fact_text}", 
            text_size=(self.width-20, None), 
            halign='left',
            font_size='12sp',
            color=[0.8, 0.8, 0.8, 1]
        )
        self.facts_container.add_widget(new_fact)
