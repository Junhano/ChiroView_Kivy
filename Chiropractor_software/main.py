from kivy.app import App
from kivy.lang import Builder
from kivy.uix.screenmanager import Screen
from kivy.uix.button import ButtonBehavior
from kivy.uix.image import Image

class HomeScreen(Screen):
    pass

class ImageButton(ButtonBehavior,Image):
    pass

class SecondScreen(Screen):
    pass

class ThirdScreen(Screen):
    pass

class BugSetting(Screen):
    pass


GUI = Builder.load_file("chiro.kv")

class MainApp(App):
    def build(self):
        return GUI
    
    def change_screen(self,screen_name):
        screen_manager = self.root.ids['screen_manager']
        screen_manager.current = screen_name 

MainApp().run()