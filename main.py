from kivymd.app import MDApp
from kivymd.uix.screen import MDScreen
from kivymd.lang import Builder
import subprocess
import os

KV = '''
MDScreen:
    MDBoxLayout:
        orientation: 'vertical'
        padding: "20dp"
        spacing: "15dp"
        MDLabel:
            text: "SCIONSIX SOVEREIGN CORE"
            halign: "center"
            font_style: "H4"
            theme_text_color: "Custom"
            text_color: 0, 0.8, 0, 1
        MDRaisedButton:
            text: "TRIGGER CAMERA"
            pos_hint: {"center_x": .5}
            on_release: app.execute_cmd("camera")
        MDRaisedButton:
            text: "SYSTEM VIBRATE"
            pos_hint: {"center_x": .5}
            on_release: app.execute_cmd("vibrate")
'''

class ScionSixApp(MDApp):
    def build(self):
        self.theme_cls.theme_style = "Dark"
        self.theme_cls.primary_palette = "Green"
        return Builder.load_string(KV)

    def execute_cmd(self, action):
        if action == "camera":
            subprocess.run(["termux-camera-photo", f"{os.getenv('HOME')}/DCIM/scion_shot.jpg"])
        elif action == "vibrate":
            subprocess.run(["termux-vibrate", "-d", "500"])

if __name__ == "__main__":
    ScionSixApp().run()
