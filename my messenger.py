from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.textinput import TextInput
from kivy.uix.button import Button
from kivy.uix.scrollview import ScrollView
from kivy.uix.image import Image
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.uix.gridlayout import GridLayout
from kivy.uix.popup import Popup
from kivy.uix.relativelayout import RelativeLayout
from kivy.core.window import Window
from kivy.clock import Clock
from kivy.graphics import Color, Rectangle
from kivy.uix.behaviors import ButtonBehavior
import time
from datetime import datetime

# Clickable Image for Profile Pictures
class ImageButton(ButtonBehavior, Image):
    pass

# Individual Chat Item
class ChatItem(BoxLayout):
    def __init__(self, name, last_message, time, **kwargs):
        super().__init__(**kwargs)
        self.orientation = 'horizontal'
        self.size_hint_y = None
        self.height = 70
        self.padding = [10, 5, 10, 5]
        
        # Profile picture
        self.profile_pic = Image(
            source='',  # You can add default profile pic
            size_hint=(None, None),
            size=(50, 50),
            pos_hint={'center_y': 0.5}
        )
        
        # Chat info
        info_layout = BoxLayout(orientation='vertical', size_hint_x=0.7)
        self.name_label = Label(
            text=name,
            font_size='16sp',
            bold=True,
            halign='left',
            size_hint_y=0.6
        )
        self.last_msg_label = Label(
            text=last_message,
            font_size='14sp',
            halign='left',
            size_hint_y=0.4
        )
        
        info_layout.add_widget(self.name_label)
        info_layout.add_widget(self.last_msg_label)
        
        # Time and notification
        side_layout = BoxLayout(orientation='vertical', size_hint_x=0.3)
        self.time_label = Label(
            text=time,
            font_size='12sp',
            size_hint_y=0.6
        )
        
        side_layout.add_widget(self.time_label)
        
        self.add_widget(self.profile_pic)
        self.add_widget(info_layout)
        self.add_widget(side_layout)

# Main Chats List Screen
class ChatsScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        
        # Sample chat data
        self.chats = [
            {"name": "Maths Group", "last_msg": "Amit: Assignment complete?", "time": "10:30 AM", "unread": 3},
            {"name": "Science Class", "last_msg": "Priya Ma'am: Lab tomorrow", "time": "9:15 AM", "unread": 1},
            {"name": "Amit", "last_msg": "You: Kal milte hain", "time": "Yesterday", "unread": 0},
            {"name": "Neha", "last_msg": "Notes bhej diye", "time": "Yesterday", "unread": 0},
            {"name": "Physics Doubts", "last_msg": "Rajesh Sir: Concept clear?", "time": "12/11/24", "unread": 5},
            {"name": "Coaching Friends", "last_msg": "Rahul: Party kab?", "time": "12/11/24", "unread": 0},
        ]
        
        main_layout = BoxLayout(orientation='vertical')
        
        # Header
        header = BoxLayout(
            orientation='horizontal',
            size_hint_y=0.1,
            padding=[10, 5, 10, 5]
        )
        
        header_title = Label(
            text='WhatsApp',
            font_size='20sp',
            bold=True,
            size_hint_x=0.6
        )
        
        search_btn = Button(
            text='🔍',
            size_hint_x=0.1,
            background_color=(0, 0, 0, 0)
        )
        
        menu_btn = Button(
            text='⋮',
            size_hint_x=0.1,
            background_color=(0, 0, 0, 0)
        )
        
        header.add_widget(header_title)
        header.add_widget(search_btn)
        header.add_widget(menu_btn)
        main_layout.add_widget(header)
        
        # Chats List
        self.chats_layout = GridLayout(
            cols=1,
            size_hint_y=1,
            spacing=5
        )
        self.chats_layout.bind(minimum_height=self.chats_layout.setter('height'))
        
        self.load_chats()
        
        scroll_view = ScrollView()
        scroll_view.add_widget(self.chats_layout)
        main_layout.add_widget(scroll_view)
        
        # New Chat Button
        new_chat_btn = Button(
            text='+ New Chat',
            size_hint_y=0.08,
            background_color=(0.1, 0.7, 0.3, 1)
        )
        new_chat_btn.bind(on_press=self.new_chat)
        main_layout.add_widget(new_chat_btn)
        
        self.add_widget(main_layout)
    
    def load_chats(self):
        self.chats_layout.clear_widgets()
        for chat in self.chats:
            chat_item = ChatItem(chat["name"], chat["last_msg"], chat["time"])
            chat_item.bind(on_press=lambda instance, chat_name=chat["name"]: self.open_chat(chat_name))
            self.chats_layout.add_widget(chat_item)
    
    def open_chat(self, chat_name):
        chat_screen = self.manager.get_screen('chat_window')
        chat_screen.set_chat(chat_name)
        self.manager.current = 'chat_window'
    
    def new_chat(self, instance):
        content = BoxLayout(orientation='vertical', spacing=10, padding=10)
        
        name_input = TextInput(hint_text='Contact name', size_hint_y=0.3)
        number_input = TextInput(hint_text='Phone number', size_hint_y=0.3)
        
        btn_layout = BoxLayout(orientation='horizontal', spacing=5, size_hint_y=0.3)
        cancel_btn = Button(text='Cancel')
        create_btn = Button(text='Create', background_color=(0.1, 0.7, 0.3, 1))
        
        btn_layout.add_widget(cancel_btn)
        btn_layout.add_widget(create_btn)
        
        content.add_widget(Label(text='New Chat'))
        content.add_widget(name_input)
        content.add_widget(number_input)
        content.add_widget(btn_layout)
        
        popup = Popup(title='New Chat', content=content, size_hint=(0.8, 0.5))
        
        def create_chat(btn):
            if name_input.text.strip():
                self.chats.insert(0, {
                    "name": name_input.text,
                    "last_msg": "Say hello!",
                    "time": "Now",
                    "unread": 0
                })
                self.load_chats()
                popup.dismiss()
        
        def cancel(btn):
            popup.dismiss()
        
        create_btn.bind(on_press=create_chat)
        cancel_btn.bind(on_press=cancel)
        
        popup.open()

# Individual Chat Window
class ChatWindow(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.current_chat = ""
        self.messages = []
        
        main_layout = BoxLayout(orientation='vertical')
        
        # Chat Header
        self.header = BoxLayout(
            orientation='horizontal',
            size_hint_y=0.1,
            padding=[10, 5, 10, 5]
        )
        
        back_btn = Button(
            text='←',
            size_hint_x=0.1,
            background_color=(0, 0, 0, 0)
        )
        back_btn.bind(on_press=self.go_back)
        
        self.chat_title = Label(
            text='Chat',
            font_size='18sp',
            bold=True,
            size_hint_x=0.7
        )
        
        call_btn = Button(
            text='📞',
            size_hint_x=0.1,
            background_color=(0, 0, 0, 0)
        )
        
        video_btn = Button(
            text='🎥',
            size_hint_x=0.1,
            background_color=(0, 0, 0, 0)
        )
        
        self.header.add_widget(back_btn)
        self.header.add_widget(self.chat_title)
        self.header.add_widget(call_btn)
        self.header.add_widget(video_btn)
        main_layout.add_widget(self.header)
        
        # Messages Area
        self.messages_layout = GridLayout(
            cols=1,
            size_hint_y=1,
            spacing=10,
            padding=10
        )
        self.messages_layout.bind(minimum_height=self.messages_layout.setter('height'))
        
        self.scroll_view = ScrollView()
        self.scroll_view.add_widget(self.messages_layout)
        main_layout.add_widget(self.scroll_view)
        
        # Input Area
        input_layout = BoxLayout(
            orientation='horizontal',
            size_hint_y=0.12,
            padding=[10, 5, 10, 5],
            spacing=10
        )
        
        attach_btn = Button(
            text='📎',
            size_hint_x=0.15,
            background_color=(0.7, 0.7, 0.7, 1)
        )
        
        self.message_input = TextInput(
            hint_text='Type a message',
            size_hint_x=0.65,
            multiline=False
        )
        self.message_input.bind(on_text_validate=self.send_message)
        
        send_btn = Button(
            text='➤',
            size_hint_x=0.2,
            background_color=(0.1, 0.7, 0.3, 1)
        )
        send_btn.bind(on_press=self.send_message)
        
        input_layout.add_widget(attach_btn)
        input_layout.add_widget(self.message_input)
        input_layout.add_widget(send_btn)
        
        main_layout.add_widget(input_layout)
        
        self.add_widget(main_layout)
    
    def go_back(self, instance):
        self.manager.current = 'chats'
    
    def set_chat(self, chat_name):
        self.current_chat = chat_name
        self.chat_title.text = chat_name
        self.messages = []
        self.messages_layout.clear_widgets()
        
        # Add sample messages based on chat
        sample_messages = {
            "Maths Group": [
                {"sender": "Amit", "message": "Assignment complete karo", "time": "10:25 AM"},
                {"sender": "You", "message": "Ho gaya sab", "time": "10:28 AM"},
                {"sender": "Neha", "message": "Mera bhi ho gaya", "time": "10:30 AM"}
            ],
            "Science Class": [
                {"sender": "Priya Ma'am", "message": "Kal lab hai, instruments le aana", "time": "9:10 AM"},
                {"sender": "You", "message": "Okay ma'am", "time": "9:12 AM"}
            ],
            "Amit": [
                {"sender": "Amit", "message": "Bro, kal milte hain?", "time": "Yesterday"},
                {"sender": "You", "message": "Haan, coaching ke baad", "time": "Yesterday"}
            ]
        }
        
        if chat_name in sample_messages:
            for msg in sample_messages[chat_name]:
                self.add_message(msg["sender"], msg["message"], msg["time"])
        else:
            self.add_message("System", f"Started chat with {chat_name}", "Now")
    
    def send_message(self, instance):
        message = self.message_input.text.strip()
        if message:
            current_time = datetime.now().strftime("%I:%M %p")
            self.add_message("You", message, current_time)
            self.message_input.text = ''
            
            # Auto-reply simulation
            Clock.schedule_once(lambda dt: self.auto_reply(message, current_time), 2)
    
    def auto_reply(self, user_message, original_time):
        replies = {
            "Maths Group": ["Achha hai", "Mera bhi ho gaya", "Kal discuss karenge"],
            "Science Class": ["Samjha", "Lab manual le aana", "Experiment record karna"],
            "Amit": ["Theek hai", "Milte hain", "Location bhej"],
            "default": ["Okay", "Samjha", "Achha idea hai", "Baad mein batata hun"]
        }
        
        import random
        if self.current_chat in replies:
            reply = random.choice(replies[self.current_chat])
            sender = "Amit" if self.current_chat == "Amit" else "Friend"
        else:
            reply = random.choice(replies["default"])
            sender = "Friend"
        
        current_time = datetime.now().strftime("%I:%M %p")
        self.add_message(sender, reply, current_time)
    
    def add_message(self, sender, message, msg_time):
        # Create message bubble
        msg_layout = BoxLayout(
            orientation='horizontal',
            size_hint_y=None,
            height=40,
            padding=[10, 5]
        )
        
        if sender == "You":
            # Right aligned (your message)
            msg_layout.add_widget(Label(size_hint_x=0.6))  # Spacer
            bubble = BoxLayout(
                orientation='vertical',
                size_hint_x=0.4,
                padding=[10, 5]
            )
            bubble.canvas.before.clear()
            with bubble.canvas.before:
                Color(0.1, 0.7, 0.3, 0.8)  # Green bubble
                Rectangle(pos=bubble.pos, size=bubble.size)
            
            msg_text = Label(
                text=message,
                halign='right',
                color=(1, 1, 1, 1)
            )
            time_text = Label(
                text=msg_time,
                font_size='10sp',
                halign='right',
                color=(1, 1, 1, 0.7)
            )
        else:
            # Left aligned (other's message)
            bubble = BoxLayout(
                orientation='vertical',
                size_hint_x=0.4,
                padding=[10, 5]
            )
            bubble.canvas.before.clear()
            with bubble.canvas.before:
                Color(0.9, 0.9, 0.9, 1)  # Gray bubble
                Rectangle(pos=bubble.pos, size=bubble.size)
            
            sender_label = Label(
                text=sender,
                font_size='12sp',
                bold=True,
                halign='left',
                color=(0, 0, 0, 1)
            )
            msg_text = Label(
                text=message,
                halign='left',
                color=(0, 0, 0, 1)
            )
            time_text = Label(
                text=msg_time,
                font_size='10sp',
                halign='left',
                color=(0.3, 0.3, 0.3, 1)
            )
            
            bubble.add_widget(sender_label)
            msg_layout.add_widget(bubble)
            msg_layout.add_widget(Label(size_hint_x=0.6))  # Spacer
        
        bubble.add_widget(msg_text)
        bubble.add_widget(time_text)
        
        if sender == "You":
            msg_layout.add_widget(bubble)
        
        self.messages_layout.add_widget(msg_layout)
        
        # Auto scroll to bottom
        Clock.schedule_once(self.scroll_to_bottom, 0.1)
    
    def scroll_to_bottom(self, dt):
        self.scroll_view.scroll_y = 0

# Status Screen
class StatusScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        layout = BoxLayout(orientation='vertical')
        
        # Header
        header = BoxLayout(orientation='horizontal', size_hint_y=0.1)
        header.add_widget(Label(text='Status', font_size='20sp', bold=True))
        layout.add_widget(header)
        
        # Status content
        content = Label(
            text='Status Feature Coming Soon...\n\nYou can add:\n• Image/Video Status\n• Text Status\n• Status Views',
            halign='center'
        )
        layout.add_widget(content)
        
        self.add_widget(layout)

# Calls Screen
class CallsScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        layout = BoxLayout(orientation='vertical')
        
        # Header
        header = BoxLayout(orientation='horizontal', size_hint_y=0.1)
        header.add_widget(Label(text='Calls', font_size='20sp', bold=True))
        layout.add_widget(header)
        
        # Calls content
        content = Label(
            text='Call Feature Coming Soon...\n\nYou can add:\n• Voice Calls\n• Video Calls\n• Call History',
            halign='center'
        )
        layout.add_widget(content)
        
        self.add_widget(layout)

# Main WhatsApp App
class WhatsAppApp(App):
    def build(self):
        Window.size = (400, 700)
        
        # Create screen manager
        sm = ScreenManager()
        
        # Add screens
        sm.add_widget(ChatsScreen(name='chats'))
        sm.add_widget(StatusScreen(name='status'))
        sm.add_widget(CallsScreen(name='calls'))
        sm.add_widget(ChatWindow(name='chat_window'))
        
        return sm

# Run the app
if __name__ == '__main__':
    WhatsAppApp().run()