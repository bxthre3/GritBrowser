from kivy.clock import Clock
from kivy.properties import NumericProperty, ObjectProperty
from kivy.uix.widget import Widget

class IntelligenceLogic(Widget):
    tenacity_rank = NumericProperty(1)
    stall_timer = NumericProperty(0)
    
    def __init__(self, engine, **kwargs):
        super(IntelligenceLogic, self).__init__(**kwargs)
        self.engine = engine
        Clock.schedule_interval(self.check_stall, 10) # Check every 10s
        
    def check_stall(self, dt):
        # Stall Detection: Trigger Socratic intervention if Delta <1% for 5 mins
        if self.engine.image_delta < 0.01:
            self.stall_timer += 10
        else:
            self.stall_timer = 0
            
        if self.stall_timer >= 300: # 5 minutes
            self.trigger_socratic_intervention()
            self.stall_timer = 0
            
    def trigger_socratic_intervention(self):
        # Fading Scaffolding: AI shifts from providing answers to asking guided questions
        if self.tenacity_rank < 5:
            message = "I noticed you've been still for a while. Need a hint on the next step?"
        else:
            message = "You've been here before. What's the one small action that breaks this loop?"
        
        print(f"SOCRATIC INTERVENTION: {message}")
        # In a real app, this would show a popup or notification

    def update_tenacity(self, xp):
        # Increase rank based on XP
        self.tenacity_rank = 1 + (xp // 1000)
