import subprocess
from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.textinput import TextInput
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.clock import mainthread

class SovereignAgent(App):
    def build(self):
        self.layout = BoxLayout(orientation='vertical', padding=10, spacing=10)
        
        # Terminal Display
        self.output_log = TextInput(readonly=True, multiline=True, background_color=(0,0,0,1), foreground_color=(0,1,0,1))
        self.layout.add_widget(self.output_log)
        
        # Command Input
        self.cmd_input = TextInput(hint_text="Enter Terminal Command...", size_hint_y=None, height=100, multiline=False)
        self.cmd_input.bind(on_text_validate=self.run_command)
        self.layout.add_widget(self.cmd_input)
        
        # Execute Button
        self.btn = Button(text="COMMENCE EXECUTION", size_hint_y=None, height=100, background_color=(0, 0.7, 0, 1))
        self.btn.bind(on_release=self.run_command)
        self.layout.add_widget(self.btn)
        
        return self.layout

    def run_command(self, instance):
        cmd = self.cmd_input.text
        if not cmd: return
        self.update_log(f"\n> Executing: {cmd}")
        
        try:
            # The Bridge: Executing physical terminal commands from the AI Agent
            result = subprocess.check_output(cmd, shell=True, stderr=subprocess.STDOUT)
            self.update_log(result.decode('utf-8'))
        except Exception as e:
            self.update_log(f"ERROR: {str(e)}")
        
        self.cmd_input.text = ""

    @mainthread
    def update_log(self, text):
        self.output_log.text += text + "\n"
        self.output_log.cursor = (0, len(self.output_log.text))

if __name__ == '__main__':
    SovereignAgent().run()
