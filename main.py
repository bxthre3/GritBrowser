from kivymd.app import MDApp
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.floatlayout import FloatLayout
from kivy.core.window import Window
from kivy.clock import Clock
from kivy.properties import ObjectProperty
from kivymd.uix.textfield import MDTextField
from kivymd.uix.button import MDIconButton

from grit_engine import GritEngine
from ui_components import GritBar, AMCCDashboard, GritChallengeModal, CoolDownOverlay
from adhd_scaffolding import TaskPagingOverlay, FactCatcherSidebar
from intelligence import IntelligenceLogic
from utils import PersistenceManager

class GritBrowserApp(MDApp):
    def build(self):
        self.theme_cls.theme_style = "Dark"
        self.theme_cls.primary_palette = "BlueGray"
        self.persistence = PersistenceManager()
        self.click_count = 0
        self.last_click_time = 0
        
        # Main Layout
        root = FloatLayout()
        
        # 1. Grit Engine (Background/Webview)
        self.engine = GritEngine()
        root.add_widget(self.engine)
        
        # 2. UI Layer
        ui_layout = BoxLayout(orientation='vertical')
        
        # Top: Grit Bar
        self.grit_bar = GritBar()
        ui_layout.add_widget(self.grit_bar)
        
        # URL Bar Area
        url_bar = BoxLayout(size_hint_y=None, height='50dp', padding='5dp', spacing='5dp')
        self.url_input = MDTextField(
            text="https://www.google.com",
            hint_text="Enter URL",
            mode="fill",
            size_hint_x=0.8
        )
        self.url_input.bind(on_text_validate=self.on_url_submit)
        
        go_btn = MDIconButton(icon="arrow-right", on_release=self.on_url_submit)
        
        url_bar.add_widget(self.url_input)
        url_bar.add_widget(go_btn)
        ui_layout.add_widget(url_bar)
        
        # Main Content Area (Browser + Sidebar)
        main_content = BoxLayout(orientation='horizontal')
        
        # Placeholder for browser view (the engine renders here)
        browser_placeholder = BoxLayout()
        main_content.add_widget(browser_placeholder)
        
        # Right: Fact Catcher Sidebar
        self.sidebar = FactCatcherSidebar()
        main_content.add_widget(self.sidebar)
        
        ui_layout.add_widget(main_content)
        root.add_widget(ui_layout)
        
        # 3. ADHD Scaffolding (Overlay)
        self.task_overlay = TaskPagingOverlay()
        root.add_widget(self.task_overlay)
        
        # 4. Intelligence Logic
        self.intel = IntelligenceLogic(self.engine)
        root.add_widget(self.intel)
        
        # 5. aMCC Dashboard (Bottom Left)
        last_url, last_notes, last_xp, last_streak = self.persistence.load_session()
        self.dashboard = AMCCDashboard(size_hint=(0.2, 0.2), pos_hint={'x': 0, 'y': 0})
        self.dashboard.xp = last_xp
        self.dashboard.streak = last_streak
        root.add_widget(self.dashboard)
        
        # Cliff-Hanging: Restore session
        if last_url:
            self.url_input.text = last_url
            self.engine.navigate(last_url)
        
        # Setup Exit Override
        Window.bind(on_request_close=self.on_request_close)
        Window.bind(on_touch_down=self.on_global_touch)
        
        # Start Grit Bar Pulse
        Clock.schedule_interval(self.update_grit_pulse, 1)
        Clock.schedule_interval(self.check_rage_control, 2)
        
        return root

    def on_global_touch(self, window, touch):
        current_time = Clock.get_time()
        if current_time - self.last_click_time < 2:
            self.click_count += 1
        else:
            self.click_count = 1
        self.last_click_time = current_time
        
    def check_rage_control(self, dt):
        if self.click_count > 10:
            # Auto-trigger "Cool Down"
            overlay = CoolDownOverlay()
            self.root.add_widget(overlay)
            Clock.schedule_once(lambda dt: self.root.remove_widget(overlay), 5)
            self.click_count = 0

    def on_stop(self):
        # Save session on exit
        self.persistence.save_session(
            self.url_input.text, 
            "", # Notes would be from a notes widget
            self.dashboard.xp, 
            self.dashboard.streak
        )

    def on_url_submit(self, *args):
        url = self.url_input.text
        self.engine.navigate(url)
        self.task_overlay.update_task(f"Working on: {url}")

    def update_grit_pulse(self, dt):
        rate = self.engine.capture_interval
        self.grit_bar.pulse(rate)

    def on_request_close(self, *args):
        modal = GritChallengeModal(on_complete=self.extend_session)
        modal.open()
        return True

    def extend_session(self):
        self.dashboard.update_stats(xp_gain=200, streak_inc=1)
        print("Session Extended! 2x XP Awarded.")

if __name__ == '__main__':
    GritBrowserApp().run()
