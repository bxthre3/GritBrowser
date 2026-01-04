from kivy.clock import Clock
from kivy.properties import NumericProperty, ObjectProperty, StringProperty
from kivy.uix.widget import Widget

class IntelligenceLogic(Widget):
    tenacity_rank = NumericProperty(1)
    stall_timer = NumericProperty(0)
    current_intervention = StringProperty("")
    
    def __init__(self, engine, **kwargs):
        super(IntelligenceLogic, self).__init__(**kwargs)
        self.engine = engine
        Clock.schedule_interval(self.check_stall, 10)
        
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
        interventions = {
            1: "What is the very next physical action required?",
            2: "Is this task serving the long-term project goal?",
            3: "What would happen if you ignored this distraction for 10 minutes?",
            4: "You've mastered this pattern. What's the 'Grit' move here?",
            5: "The aMCC is strongest when it chooses the harder path. Which path is that?"
        }
        
        rank = min(5, self.tenacity_rank)
        self.current_intervention = interventions.get(rank, interventions[1])
        print(f"SOCRATIC INTERVENTION [Rank {rank}]: {self.current_intervention}")
        
        # Trigger Zen Mode if stalling persists at high rank
        if rank >= 4:
            self.trigger_zen_mode()

    def trigger_zen_mode(self):
        print("STALL DETECTED AT HIGH TENACITY: TRIGGERING ZEN MODE BLACKOUT")
        # This would communicate with the ShaderWidget to set zen_mode = 1.0

    def update_tenacity(self, xp):
        # Tenacity Rank increases every 1000 XP
        self.tenacity_rank = 1 + (xp // 1000)
