from kivy.app import App
from kivy.lang import Builder
from kivy.uix.screenmanager import Screen, NoTransition
from kivy.uix.button import ButtonBehavior
from kivy.uix.image import Image
from kivy.graphics import Line, Color
from kivy.properties import ObjectProperty
from plyer import camera
from plyer import filechooser
from os.path import exists


import smtplib


class ImageButton(ButtonBehavior,Image):
    pass

class HomeScreen(Screen):
    pass

class SecondScreen(Screen):
    image_change = ObjectProperty(None)

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
    

            
    def send_message(self, text):
        try:
            server = smtplib.SMTP('smtp.gmail.com', 587)
            server.ehlo()
            server.starttls()
            server.login('jimmybugreport@gmail.com','20000620oyjhwork')
            server.sendmail('jimmybugreport@gmail.com','junhano@uci.edu',text)
        except:
            print('Something went wrong')
       

    def modify_image(self,vertical,horizontal,objectname):
        self.clean_image(objectname)
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
        try:
            for i in remove_list:
                objectname.canvas.remove(i)
            remove_list.clear()
        except:
            pass
        
    def change_picture(self, source):

        self.root.ids.second_screen.image_change.source = source
        self.root.ids.second_screen.image_change.default_image = False
        self.change_screen("second_screen")

    def capture(self):
        try:
            file_name = "test.png"
            camera.take_picture(filename = file_name,on_complete = self.camera_callback)

        except NotImplementedError:
            pass

    def camera_callback(self, filename):
        if (exists(filename)):
            print('Hello')
        else:
            pass

    def open_photos(self):
        filechooser.open_file(on_selection=self.handle_selection)

    def handle_selection(self,selection):
        try:
            self.selection = selection
            print(self.selection[0])
            self.change_picture(self.selection[0])
        except NotImplementedError:
            pass

    

    def clear_all(self,objectname):
        try:
            for i in remove_list:
                objectname.canvas.remove(i)
            remove_list.clear()
        except:
            pass
        objectname.source = "icons/no-camera.png"
        objectname.default_image = True
        
MainApp().run()
