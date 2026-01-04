from kivymd.app import MDApp
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.floatlayout import FloatLayout
from kivy.core.window import Window
from kivy.clock import Clock
from kivy.properties import ObjectProperty, NumericProperty
from kivymd.uix.textfield import MDTextField
from kivymd.uix.button import MDIconButton, MDRaisedButton
from kivy.graphics import Color, Rectangle

from grit_engine import GritEngine
from ui_components import GritBar, AMCCDashboard, GritChallengeModal, CoolDownOverlay
from adhd_scaffolding import TaskPagingOverlay, FactCatcherSidebar, TunnelWindow
from intelligence import IntelligenceLogic
from utils import PersistenceManager
from shader_widget import GritShaderWidget

class GritBrowserApp(MDApp):
    def build(self):
        self.theme_cls.theme_style = "Dark"
        self.theme_cls.primary_palette = "BlueGray"
        self.persistence = PersistenceManager()
        self.click_count = 0
        self.last_click_time = 0
        
        # Root Container with Shader Effects
        self.root_container = GritShaderWidget()
        
        # 1. Grit Engine (Background/Webview)
        self.engine = GritEngine()
        self.root_container.add_widget(self.engine)
        
        # 2. UI Layer
        ui_layout = BoxLayout(orientation='vertical')
        
        # Top: Grit Bar
        self.grit_bar = GritBar()
        ui_layout.add_widget(self.grit_bar)
        
        # URL Bar Area (Physically Caged by TaskPagingOverlay)
        url_bar = BoxLayout(size_hint_y=None, height='50dp', padding='5dp', spacing='5dp')
        with url_bar.canvas.before:
            Color(0.1, 0.1, 0.1, 1)
            self.url_bg = Rectangle(size=url_bar.size, pos=url_bar.pos)
        
        self.url_input = MDTextField(
            text="https://www.google.com",
            hint_text="NEURO-TUNNEL URL",
            mode="fill",
            size_hint_x=0.8,
            font_size='14sp'
        )
        self.url_input.bind(on_text_validate=self.on_url_submit)
        
        go_btn = MDIconButton(icon="shield-check-outline", on_release=self.on_url_submit, theme_text_color="Custom", text_color=[0.2, 0.6, 1, 1])
        tunnel_btn = MDIconButton(icon="window-maximize", on_release=self.launch_tunnel, theme_text_color="Custom", text_color=[0, 1, 0.8, 1])
        
        url_bar.add_widget(self.url_input)
        url_bar.add_widget(go_btn)
        url_bar.add_widget(tunnel_btn)
        ui_layout.add_widget(url_bar)
        
        # Main Content Area
        main_content = BoxLayout(orientation='horizontal')
        main_content.add_widget(BoxLayout()) # Browser Placeholder
        
        self.sidebar = FactCatcherSidebar()
        main_content.add_widget(self.sidebar)
        
        ui_layout.add_widget(main_content)
        self.root_container.add_widget(ui_layout)
        
        # 3. ADHD Scaffolding (Overlay)
        self.task_overlay = TaskPagingOverlay()
        self.root_container.add_widget(self.task_overlay)
        
        # 4. Intelligence Logic
        self.intel = IntelligenceLogic(self.engine)
        self.root_container.add_widget(self.intel)
        
        # 5. aMCC Dashboard
        last_url, last_notes, last_xp, last_streak = self.persistence.load_session()
        self.dashboard = AMCCDashboard(size_hint=(0.2, 0.2), pos_hint={'x': 0, 'y': 0})
        self.dashboard.xp = last_xp
        self.dashboard.streak = last_streak
        self.root_container.add_widget(self.dashboard)
        
        # Restore Session
        if last_url:
            self.url_input.text = last_url
            self.engine.navigate(last_url)
        
        # Global Events
        Window.bind(on_request_close=self.on_request_close)
        Window.bind(on_touch_down=self.on_global_touch)
        
        # Loops
        Clock.schedule_interval(self.update_grit_pulse, 1)
        Clock.schedule_interval(self.check_rage_control, 2)
        Clock.schedule_interval(self.sync_shaders, 0.1)
        
        return self.root_container

    def sync_shaders(self, dt):
        # Sync intelligence state to shaders
        if self.intel.stall_timer > 60:
            self.root_container.grayscale_amount = min(1.0, (self.intel.stall_timer - 60) / 240)
        else:
            self.root_container.grayscale_amount = 0

    def on_global_touch(self, window, touch):
        current_time = Clock.get_time()
        if current_time - self.last_click_time < 2:
            self.click_count += 1
        else:
            self.click_count = 1
        self.last_click_time = current_time
        
    def check_rage_control(self, dt):
        if self.click_count > 10:
            self.root_container.blue_light_filter = 1.0
            overlay = CoolDownOverlay()
            self.root_container.add_widget(overlay)
            Clock.schedule_once(lambda dt: self.reset_cooldown(overlay), 5)
            self.click_count = 0

    def reset_cooldown(self, overlay):
        self.root_container.remove_widget(overlay)
        self.root_container.blue_light_filter = 0.0

    def launch_tunnel(self, *args):
        tunnel = TunnelWindow(url=self.url_input.text, size_hint=(0.6, 0.6), pos_hint={'center_x': 0.5, 'center_y': 0.5})
        self.root_container.add_widget(tunnel)

    def on_url_submit(self, *args):
        url = self.url_input.text
        self.engine.navigate(url)
        self.task_overlay.update_task(f"EXECUTING: {url}")

    def update_grit_pulse(self, dt):
        self.grit_bar.pulse(self.engine.capture_interval)

    def on_request_close(self, *args):
        modal = GritChallengeModal(on_complete=self.extend_session)
        modal.open()
        return True

    def extend_session(self):
        self.dashboard.update_stats(xp_gain=200, streak_inc=1)
        self.intel.update_tenacity(self.dashboard.xp)

    def on_stop(self):
        self.persistence.save_session(self.url_input.text, "", self.dashboard.xp, self.dashboard.streak)

if __name__ == '__main__':
    GritBrowserApp().run()
