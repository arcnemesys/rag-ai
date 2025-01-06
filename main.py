# local message dir: /home/arcnemesys/.thunderbird/ufqe2ut1.default-release/Mail/pop.gmail.com 

from kivy.uix.vkeyboard import Vector
from email_utils import get_profile, get_inbox, read_inbox
from app import Lemais

class EmailSorterApp(App):
    def build(self):
        layout = BoxLayout(orientation='vertical', padding=10, spacing=10)
        
        # Email Summary View Area
        summary_container = BoxLayout(orientation='vertical', size_hint_y=0.6)
        summary_label = Label(
            text='Email Summary',
            size_hint_y=0.1,
            bold=True
        )
        self.summary_content = Label(
            text='Email content summary will appear here...',
            size_hint_y=0.9,
            text_size=(400, None),
            halign='left',
            valign='top'
        )
        summary_container.add_widget(summary_label)
        summary_container.add_widget(self.summary_content)
        
        # Reply Input Area
        reply_container = BoxLayout(orientation='vertical', size_hint_y=0.4)
        reply_label = Label(
            text='Your Reply',
            size_hint_y=0.1,
            bold=True
        )
        self.reply_input = TextInput(
            multiline=True,
            hint_text='Type your reply here...',
            size_hint_y=0.9
        )
        reply_container.add_widget(reply_label)
        reply_container.add_widget(self.reply_input)
        
        # Send Button
        send_button = Button(
            text='Send Reply',
            size_hint_y=0.1,
            on_press=self.send_reply
        )
        
        # Add all widgets to main layout
        layout.add_widget(summary_container)
        layout.add_widget(reply_container)
        layout.add_widget(send_button)
        
        return layout
    
    def send_reply(self, instance):
        reply_text = self.reply_input.text
        # Here you can add logic to send the reply
        print(f"Reply to be sent: {reply_text}")
        self.reply_input.text = ''  # Clear the reply input

def main():
    try:
        profile_folder = get_profile()
        inbox_path = get_inbox(profile_folder)
        read_inbox(inbox_path)
    except Exception as e:
        print(f"Error : {e}")
    print("Hello from rag-ai")
if __name__ == "__main__":
    # PongApp().run()
    MainApp().run()
