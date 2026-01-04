from kivy.uix.progressbar import ProgressBar
from kivy.uix.modalview import ModalView
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.uix.boxlayout import BoxLayout
from kivy.properties import NumericProperty, BooleanProperty, StringProperty
from kivy.animation import Animation
from kivy.clock import Clock
from kivymd.uix.button import MDRaisedButton

class GritBar(ProgressBar):
    def __init__(self, **kwargs):
        super(GritBar, self).__init__(**kwargs)
        self.height = '5dp'
        self.size_hint_y = None
        self.value = 0
        
    def pulse(self, rate):
        Animation.stop_all(self)
        anim = Animation(value=100, duration=rate/2) + Animation(value=0, duration=rate/2)
        anim.repeat = True
        anim.start(self)

class GritChallengeModal(ModalView):
    def __init__(self, on_complete, **kwargs):
        super(GritChallengeModal, self).__init__(**kwargs)
        self.size_hint = (0.8, 0.4)
        self.auto_dismiss = False
        self.on_complete = on_complete
        
        layout = BoxLayout(orientation='vertical', padding=20, spacing=10)
        layout.add_widget(Label(text="GRIT CHALLENGE: 15% PUSH", font_size='20sp', bold=True))
        layout.add_widget(Label(text="Complete this session extension for 2x XP!"))
        
        btn = MDRaisedButton(text="I HAVE THE GRIT", pos_hint={'center_x': 0.5})
        btn.bind(on_release=self.complete)
        layout.add_widget(btn)
        
        self.add_widget(layout)
        
    def complete(self, instance):
        if self.on_complete:
            self.on_complete()
        self.dismiss()

class AMCCDashboard(BoxLayout):
    xp = NumericProperty(0)
    streak = NumericProperty(0)
    
    def __init__(self, **kwargs):
        super(AMCCDashboard, self).__init__(**kwargs)
        self.orientation = 'vertical'
        self.padding = 10
        self.add_widget(Label(text="aMCC NEURO-PERFORMANCE", bold=True))
        self.xp_label = Label(text=f"XP: {self.xp}")
        self.streak_label = Label(text=f"6-Month Streak: {self.streak} days")
        self.add_widget(self.xp_label)
        self.add_widget(self.streak_label)
        
    def update_stats(self, xp_gain, streak_inc=0):
        self.xp += xp_gain
        self.streak += streak_inc
        self.xp_label.text = f"XP: {self.xp}"
        self.streak_label.text = f"6-Month Streak: {self.streak} days"

class CoolDownOverlay(BoxLayout):
    def __init__(self, **kwargs):
        super(CoolDownOverlay, self).__init__(**kwargs)
        self.orientation = 'vertical'
        # In a real app, we'd play brown noise here
        self.add_widget(Label(text="COOL DOWN ACTIVE", color=[0.2, 0.6, 1, 1], bold=True))
