from kivy.app import App
from kivy.lang import Builder
from kivy.uix.screenmanager import Screen, NoTransition
from kivy.uix.button import ButtonBehavior
from kivy.uix.image import Image
from kivy.graphics import Line, Color
from kivy.properties import ObjectProperty, NumericProperty
from plyer import camera, filechooser
from os.path import exists, join
from configparser import ConfigParser
from kivy.utils import platform
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






class MainApp(App):

    state = NumericProperty(0)

    def build(self):
        parser = ConfigParser()
        location = 'dev.ini'
        if platform == 'ios':
            savepath = App.get_running_app().user_data_dir
            location = join(savepath, location)

        parser.read(location)
        if len(parser.sections()) != 0:
            Lang = int(parser.get('LangSetting', 'lang'))
            self.state = Lang

        GUI = Builder.load_file("chiro.kv")
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

    def switchLanguage(self):
        parser = ConfigParser()
        if self.state == 1:
            self.state = 0
            parser['LangSetting'] = {
                'lang': '0'
            }
        else:
            self.state = 1
            parser['LangSetting'] = {
                'lang': '1'
            }
        savefileName = 'dev.ini'
        if platform == 'ios':
            savepath = App.get_running_app().user_data_dir
            savefileName = join(savepath, savefileName)
        with open(savefileName, 'w') as f:
            parser.write(f)


    def change_picture(self, source):

        self.root.ids.second_screen.image_change.source = source
        self.root.ids.second_screen.image_change.default_image = False
        self.change_screen("second_screen")

    def capture(self):
        try:
            file_name = "test.png"
            if platform == 'ios':
                savepath = App.get_running_app().user_data_dir
                file_name = join(savepath, file_name)
            camera.take_picture(filename = file_name,on_complete = self.camera_callback)

        except NotImplementedError:
            pass

    def camera_callback(self, filename):
        if (exists(filename)):
            self.change_picture(filename)

    def open_photos(self):
        try:
            filechooser.open_file(on_selection=self.handle_selection)
        except NotImplementedError:
            pass


    def handle_selection(self,selection):
        try:
            self.selection = selection
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
