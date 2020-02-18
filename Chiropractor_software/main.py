from kivy.app import App
from kivy.lang import Builder
from kivy.uix.screenmanager import Screen, NoTransition
from kivy.uix.button import ButtonBehavior
from kivy.uix.image import Image
from kivy.uix.popup import Popup
from kivy.graphics import Line, Color
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
            server.login('jimmybugreport@gmail.com','20000620oyjhwork')
            server.sendmail('jimmybugreport@gmail.com','junhano@uci.edu',text)
        except:
            print('Something went wrong')
        finally:
            popupWindow.dismiss()
        

    def modify_image(self,vertical,horizontal,objectname):
        global remove_list
        remove_list = []
        try:
            vertical = int(vertical)
            horizontal = int(horizontal)
            with objectname.canvas:
                Color(0, 0, 0)
                for k in range(vertical):
                    temp = Line(points=[objectname.x + objectname.width // (vertical + 1) * (k+1), objectname.y, objectname.x + objectname.width // (vertical + 1) * (k+1), objectname.y + objectname.height], width=1.2)
                    remove_list.append(temp)
                for i in range(horizontal):
                    temp = Line(points=[objectname.x, objectname.y + (objectname.height //(horizontal + 1) * (i + 1)), objectname.x + objectname.width, objectname.y + (objectname.height // (horizontal + 1) * (i+1))], width=1.2)
                    remove_list.append(temp)
        except:
            print("Error in getting num lines")
    
    def clean_image(self,objectname):
        for i in remove_list:
            objectname.canvas.remove(i)
        remove_list.clear()

        
MainApp().run()
