from kivy.app import App
from kivy.lang import Builder
from kivy.uix.screenmanager import Screen, NoTransition
from kivy.uix.button import ButtonBehavior
from kivy.uix.image import Image
from kivy.uix.popup import Popup
import smtplib


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

class BugSending(Screen):
    pass


GUI = Builder.load_file("chiro.kv")

class MainApp(App):
    def build(self):
        return GUI
    
    def change_screen(self,screen_name):
        screen_manager = self.root.ids['screen_manager']
        screen_manager.transition = NoTransition()
        screen_manager.current = screen_name 
    
    def show_popup(self, logic_bool = True):
        if logic_bool:
            show = BugSending()
            global popupWindow
            popupWindow = Popup(title = "Bug sending", content = show, size_hint = (None,None), size = (400,400))
            popupWindow.open()
        else:
            popupWindow.dismiss()
            
    def send_message(self, text):
        try:
            server = smtplib.SMTP('smtp.gmail.com', 587)
            server.ehlo()
            server.starttls()
            server.login('jimmyouyangca@gmail.com','20000620oyjhwork')
            server.sendmail('jimmyouyangca@gmail.com','junhano@uci.edu',text)
        except:
            print('Something went wrong')
        finally:
            popupWindow.dismiss()
        

        
MainApp().run()
