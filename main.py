from kivymd.app import MDApp
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.floatlayout import FloatLayout
from kivy.core.window import Window
from kivy.clock import Clock
from kivy.properties import ObjectProperty
from kivymd.uix.textfield import MDTextField
from kivymd.uix.button import MDIconButton

from grit_engine import GritEngine
from ui_components import GritBar, AMCCDashboard, GritChallengeModal
from adhd_scaffolding import TaskPagingOverlay, FactCatcherSidebar
from intelligence import IntelligenceLogic

class GritBrowserApp(MDApp):
    def build(self):
        self.theme_cls.theme_style = "Dark"
        self.theme_cls.primary_palette = "BlueGray"
        
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
        self.dashboard = AMCCDashboard(size_hint=(0.2, 0.2), pos_hint={'x': 0, 'y': 0})
        root.add_widget(self.dashboard)
        
        # Setup Exit Override
        Window.bind(on_request_close=self.on_request_close)
        
        # Start Grit Bar Pulse
        Clock.schedule_interval(self.update_grit_pulse, 1)
        
        return root

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
