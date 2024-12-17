from textual.app import App, ComposeResult
from textual.widgets import Welcome
from textual import events 

class Lemais(App):
    def compose(self) -> ComposeResult:
        yield Welcome()

    def on_button_pressed(self) -> None:
        self.exit()
