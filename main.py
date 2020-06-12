from kivymd.app import MDApp
from kivy.lang import Builder
from kivy.uix.screenmanager import Screen, NoTransition
from kivy.uix.button import ButtonBehavior
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.image import Image
from kivy.graphics import Line, Color
from kivy.properties import ObjectProperty, NumericProperty,BooleanProperty, StringProperty
from plyer import camera, filechooser
from os.path import exists, join
from configparser import ConfigParser
from kivy.utils import platform
from kivymd.uix.button import MDFlatButton
from kivymd.uix.dialog import MDDialog
from kivymd.uix.textfield import MDTextField
from languageDict.LanguageDict import langDict
from kivy.config import ConfigParser




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

class Help(Screen):
    pass

class About(Screen):
    pass

class Contact(Screen):
    pass

class GeneralSetting(Screen):
    pass

class SecondScreenB(Screen):
    image_change_B = ObjectProperty(None)

class LineContent(BoxLayout):
    pass


class MainApp(MDApp):

    state = NumericProperty(0)
    mode = NumericProperty(0)
    dialog = None
    remove_confirm = None
    error_dialog = None
    image_source = StringProperty("icons/no-camera.png")
    default_image = BooleanProperty(True)
    def build(self):
        parser = ConfigParser()
        location = 'dev.ini'
        if platform == 'ios':
            savepath = MDApp.get_running_app().user_data_dir
            location = join(savepath, location)

        parser.read(location)
        try:
            self.state = int(parser.get('Setting', 'lang'))
            self.mode = int(parser.get('Setting', 'mode'))
        except:
            pass
        GUI = Builder.load_file("chiro.kv")
        return GUI
    
    def change_screen(self,screen_name):
        screen_manager = self.root.ids['screen_manager']
        screen_manager.transition = NoTransition()
        screen_manager.current = screen_name 
    

            
    def send_message(self, text):
        try:
            print(text)
        except:
            print('Something went wrong')
       

    def modify_image(self,vertical,horizontal,objectname):
        self.clean_image(objectname)
        global remove_list
        remove_list = []
        try:
            vertical = int(vertical)
            horizontal = int(horizontal)
            if vertical > 20:
                vertical = 20
            if horizontal > 20:
                horizontal = 20
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
        else:
            self.state = 1
        parser['Setting'] = {
            'lang': str(self.state),
            'mode': str(self.mode)
        }
        savefileName = 'dev.ini'
        if platform == 'ios':
            savepath = MDApp.get_running_app().user_data_dir
            savefileName = join(savepath, savefileName)
        with open(savefileName, 'w') as f:
            parser.write(f)

    def switchMode(self):
        parser = ConfigParser()
        if self.mode == 0:
            self.mode = 1
        else:
            self.mode = 0
        parser['Setting'] = {
            'lang': str(self.state),
            'mode': str(self.mode)
        }
        savefileName = 'dev.ini'
        if platform == 'ios':
            savepath = MDApp.get_running_app().user_data_dir
            savefileName = join(savepath, savefileName)
        with open(savefileName, 'w') as f:
            parser.write(f)

    def change_picture(self, source):

        self.image_source = source
        self.root.ids.second_screen.image_change.reload()
        self.default_image = False
        self.change_screen("second_screen")

    def capture(self):
        try:
            file_name = "test.png"
            if platform == 'ios':
                savepath = MDApp.get_running_app().user_data_dir
                savepath = savepath[:len(savepath) - 4]
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
        self.image_source = "icons/no-camera.png"
        self.default_image = True

    def AnalysisWithPoints(self):
        print('OK')

    def line_draw_setting(self):
        if not self.dialog:
            self.dialog = MDDialog(
                title= '[font=Font/NotoSansSC-Regular.otf]{}[/font]'.format(langDict["EnterNumber"][self.state]),
                type="custom",
                content_cls=LineContent(),
                buttons=[
                        MDFlatButton(
                            text=langDict["Cancel"][self.state], text_color=self.theme_cls.primary_color, on_release= self.closeDialog
                        ),
                        MDFlatButton(
                            text=langDict["Draw"][self.state],text_color=self.theme_cls.primary_color, on_release=self.grabText
                        ),
                    ],
                )
        self.dialog.set_normal_height()
        self.dialog.open()

    def confirm_remove_setting(self):
        if not self.remove_confirm:
            self.remove_confirm = MDDialog(
                text= '[font=Font/NotoSansSC-Regular.otf]{}[/font]'.format(langDict["ConfirmRemoveMessage"][self.state]),
                type="custom",
                buttons=[
                        MDFlatButton(
                            text=langDict["CANCEL"][self.state], text_color=self.theme_cls.primary_color, on_release= self.dismissRemoveConfirm
                        ),
                        MDFlatButton(
                            text=langDict["CONFIRM"][self.state],text_color=self.theme_cls.primary_color, on_release=self.action
                        ),
                    ],
                )
        self.remove_confirm.set_normal_height()
        self.remove_confirm.open()

    def errorDialog(self, keyString):
        self.error_dialog = None
        if not self.error_dialog:
            self.error_dialog = MDDialog(
                text='[font=Font/NotoSansSC-Regular.otf]{}[/font]'.format(langDict[keyString][self.state]),
                radius = [20, 7, 20, 7]
            )
        self.error_dialog.open()


    def action(self, inst):
        self.clear_all(self.root.ids.second_screen.image_change)
        self.remove_confirm.dismiss()
        self.remove_confirm = None

    def dismissRemoveConfirm(self, inst):
        self.remove_confirm.dismiss()
        self.remove_confirm = None

    def grabText(self, inst):
        lista = []
        for obj in self.dialog.content_cls.children:
            if isinstance(obj, MDTextField):
                lista.append(obj.text)
                obj.text = ""
        if not self.root.ids.second_screen.image_change.default_image:
            self.modify_image(lista[0],lista[1],self.root.ids.second_screen.image_change)
        self.dialog.dismiss()
        self.dialog = None

    def closeDialog(self, inst):
        self.dialog.dismiss()
        self.dialog = None

MainApp().run()
