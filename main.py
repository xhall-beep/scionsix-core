import os
import threading
import subprocess
import logging
from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.textinput import TextInput
from kivy.uix.scrollview import ScrollView
from kivy.clock import mainthread

# Augmented Logging Logic
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(message)s')
logger = logging.getLogger('SovereignAgent')

class SovereignAgent(App):
    def build(self):
        self.title = "ORI SCION - Sovereign Node"
        self.root = BoxLayout(orientation='vertical', padding=10, spacing=10)

        self.scroll_view = ScrollView(size_hint=(1, 0.8))
        self.output_log = TextInput(
            text="[SYSTEM] Sovereign Node Online (Android 16)...\n",
            readonly=True,
            background_color=(0, 0, 0, 1),
            foreground_color=(0, 1, 0, 1),
            size_hint_y=None,
            font_size='14sp'
        )
        self.output_log.bind(minimum_height=self.output_log.setter('height'))
        self.scroll_view.add_widget(self.output_log)

        self.cmd_input = TextInput(
            hint_text="Enter Orchestration Command...",
            multiline=False,
            size_hint=(1, 0.1),
            background_color=(0.1, 0.1, 0.1, 1),
            foreground_color=(1, 1, 1, 1)
        )
        self.cmd_input.bind(on_text_validate=self.execute_orchestration)

        self.root.add_widget(self.scroll_view)
        self.root.add_widget(self.cmd_input)
        return self.root

    def execute_orchestration(self, instance):
        cmd = instance.text.strip()
        if not cmd: return
        self.update_log(f"\n[EXECUTE] > {cmd}")
        threading.Thread(target=self._run_task, args=(cmd,), daemon=True).start()
        instance.text = ""

    def _run_task(self, cmd):
        try:
            process = subprocess.Popen(
                cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True
            )
            stdout, stderr = process.communicate()
            if stdout: self.update_log(stdout)
            if stderr: self.update_log(f"[ERROR] {stderr}")
        except Exception as e:
            self.update_log(f"[EXCEPTION] {str(e)}")

    @mainthread
    def update_log(self, text):
        self.output_log.text += text + "\n"
        self.output_log.cursor = (0, len(self.output_log.text))

if __name__ == '__main__':
    SovereignAgent().run()
