from textual.app import App, ComposeResult, RenderResult
from textual.widgets import Welcome, Footer, Header, Label, ListItem, ListView
from textual.widget import Widget 
from textual import events 

class LemaisMenu(Widget):
    CSS_PATH = "app.tcss"
    def compose(self) -> ComposeResult:
        yield ListView(
            ListItem(Label("Inbox")),
            ListItem(Label("Sent"))
        )
class Lemais(App):
    CSS_PATH = "app.tcss"
    def compose(self) -> ComposeResult:
        yield Header()
        yield Footer()
        yield ListView(
            ListItem(Label("Inbox")),
            ListItem(Label("Sent"))
        )
    

    def on_button_pressed(self) -> None:
        self.exit()
