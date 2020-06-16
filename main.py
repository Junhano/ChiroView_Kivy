from kivymd.app import MDApp
from kivy.lang import Builder
from kivy.uix.screenmanager import Screen, NoTransition
from kivy.uix.button import ButtonBehavior
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.image import Image
from kivy.graphics import Line, Color
from kivy.properties import ObjectProperty, NumericProperty,BooleanProperty, StringProperty
from plyer import camera, filechooser, email
from os.path import exists, join
from configparser import ConfigParser
from kivy.utils import platform
from kivymd.uix.button import MDFlatButton
from kivymd.uix.dialog import MDDialog
from kivy.uix.textinput import TextInput
from languageDict.LanguageDict import langDict
from kivymd.uix.list import OneLineAvatarIconListItem
from os import remove


class ItemConfirm(OneLineAvatarIconListItem):
    divider = None

    def set_icon(self, instance_check):
        instance_check.active = True
        check_list = instance_check.get_widgets(instance_check.group)
        for check in check_list:
            if check != instance_check:
                check.active = False



class ImageButton(ButtonBehavior,Image):
    pass

class HomeScreen(Screen):
    pass

class SecondScreen(Screen):
    image_change = ObjectProperty(None)

class ThirdScreen(Screen):
    pass

class BugSending(Screen):
    pass

class Help(Screen):
    pass

class About(Screen):
    pass

class GeneralSetting(Screen):
    pass

class LineContent(BoxLayout):
    pass

class BugSetting(BoxLayout):
    pass

class Helper(BoxLayout):
    pass

class RotationValue(BoxLayout):
    pass


class MainApp(MDApp):

    state = NumericProperty(0) #which language, 0 is English, 1 is Chinese
    rotateDegree = NumericProperty(90) #RotateDegree for rotation image
    View = NumericProperty(0) #0 is front body view while 1 is side body view
    HorizontalLine = NumericProperty(8)
    VerticalLine = NumericProperty(8)
    dialog = None  #Dialog that prompt user for how many lines to draw both vertically and horizontally
    remove_confirm = None      #Dialog that confirm user to remove the picture from the canvas
    error_dialog = None          #Dialog that give user error alert when things go wrong
    BugSetting_dialog = None    #Dialog that give user to choose what option they want to enter to either change setting, contact or get help etc
    HelperDialog = None      #Dialog that give user to choose picture when they haven't choose it yet
    PointDrawDialog = None     #Dialog that give user to choose what kind of body part they want to points
    RotationDegreeDialog = None  #Dialog that give user the ability to choose how many degree they want to rotate
    image_source = StringProperty("icons/no-camera.png")
    default_image = BooleanProperty(True)
    remove_list = list()

    coordinateDict = dict()
    coordinateKey = None
    capturePoint = False
    captureCoordinate = None

    def build(self):
        #self.theme_cls.theme_style = "Dark"
        parser = ConfigParser()
        location = 'dev.ini'
        if platform == 'ios':
            savepath = MDApp.get_running_app().user_data_dir
            location = join(savepath, location)

        parser.read(location)
        try:
            self.state = int(parser.get('Setting', 'lang'))
            self.rotateDegree = int(parser.get('Setting', 'rotationDegree'))
            self.VerticalLine = int(parser.get('Setting', 'VerticalLine'))
            self.HorizontalLine = int(parser.get('Setting', 'HorizontalLine'))
        except:
            pass
        GUI = Builder.load_file("chiro.kv")
        return GUI



    #Function here that about declear of different MD Dialog

    def line_draw_setting(self):
        #Dialog that about line draw setting, how many lines
        if not self.dialog:
            self.dialog = MDDialog(
                title= '[font=Font/NotoSansSC-Regular.otf]{}[/font]'.format(langDict["EnterNumber"][self.state]),
                type="custom",
                content_cls=LineContent(),
                buttons=[
                        MDFlatButton(
                            text=langDict["CANCEL"][self.state], text_color=self.theme_cls.primary_color, on_release= self.closeDialog
                        ),
                        MDFlatButton(
                            text=langDict["APPLY"][self.state],text_color=self.theme_cls.primary_color, on_release=self.grabText
                        ),
                    ],
                )
        self.dialog.set_normal_height()
        self.dialog.open()

    def confirm_remove_setting(self, func, keyStr):
        #Dialog that about remove picture from canvas
        if not self.remove_confirm:
            self.remove_confirm = MDDialog(
                text= '[font=Font/NotoSansSC-Regular.otf]{}[/font]'.format(langDict[keyStr][self.state]),
                type="custom",
                buttons=[
                        MDFlatButton(
                            text=langDict["CANCEL"][self.state], text_color=self.theme_cls.primary_color, on_release= self.dismissRemoveConfirm
                        ),
                        MDFlatButton(
                            text=langDict["CONFIRM"][self.state],text_color=self.theme_cls.primary_color, on_release= func
                        ),
                    ],
                )
        self.remove_confirm.set_normal_height()
        self.remove_confirm.open()

    def BugSettingDialog(self):
        #Dialog that about bug setting in home page
        if not self.BugSetting_dialog:
            self.BugSetting_dialog = MDDialog(
                type = "custom",
                size_hint = (0.5, 0.5),
                pos_hint = {'x': 0.52, 'top': 1},
                content_cls = BugSetting()
            )

        self.BugSetting_dialog.open()

    def HelperDialogWhenNoImage(self):
        #Dialog that give user choice to choose picture when they haven't choose it yet
        if not self.HelperDialog:
            self.HelperDialog = MDDialog(
                title = '[font=Font/NotoSansSC-Regular.otf]{}[/font]'.format(langDict["OptionForUserWhenNoImage"][self.state]),
                type = "custom",
                content_cls = Helper()
            )
        self.HelperDialog.set_normal_height()
        self.HelperDialog.open()


    def pointDrawDialog(self):
        #Dialog that give user to choose what point they want to identify
        FrontViewItem = {
            ItemConfirm(text = '[font=Font/NotoSansSC-Regular.otf]{}[/font]'.format(langDict['LeftEye'][self.state])),
            ItemConfirm(text = '[font=Font/NotoSansSC-Regular.otf]{}[/font]'.format(langDict['RightEye'][self.state])),
            ItemConfirm(text = '[font=Font/NotoSansSC-Regular.otf]{}[/font]'.format(langDict['LeftEar'][self.state])),
            ItemConfirm(text = '[font=Font/NotoSansSC-Regular.otf]{}[/font]'.format(langDict['RightEar'][self.state])),
            ItemConfirm(text = '[font=Font/NotoSansSC-Regular.otf]{}[/font]'.format(langDict['NoseTip'][self.state])),
            ItemConfirm(text = '[font=Font/NotoSansSC-Regular.otf]{}[/font]'.format(langDict['SternalNotch'][self.state])),
            ItemConfirm(text = '[font=Font/NotoSansSC-Regular.otf]{}[/font]'.format(langDict['LeftShoulderTip'][self.state])),
            ItemConfirm(text = '[font=Font/NotoSansSC-Regular.otf]{}[/font]'.format(langDict['RightShoulderTip'][self.state])),
            ItemConfirm(text = '[font=Font/NotoSansSC-Regular.otf]{}[/font]'.format(langDict['Umbilicus'][self.state])),
            ItemConfirm(text = '[font=Font/NotoSansSC-Regular.otf]{}[/font]'.format(langDict['ASIS'][self.state])),
            ItemConfirm(text = '[font=Font/NotoSansSC-Regular.otf]{}[/font]'.format(langDict['LeftKneeCap'][self.state])),
            ItemConfirm(text = '[font=Font/NotoSansSC-Regular.otf]{}[/font]'.format(langDict['RightKneeCap'][self.state])),
            ItemConfirm(text = '[font=Font/NotoSansSC-Regular.otf]{}[/font]'.format(langDict['LeftAnkle'][self.state])),
            ItemConfirm(text = '[font=Font/NotoSansSC-Regular.otf]{}[/font]'.format(langDict['RightAnkle'][self.state]))
        }

        SideViewItem = {
            ItemConfirm(text = '[font=Font/NotoSansSC-Regular.otf]{}[/font]'.format(langDict['EarCanal'][self.state])),
            ItemConfirm(text = '[font=Font/NotoSansSC-Regular.otf]{}[/font]'.format(langDict['CornerOfEye'][self.state])),
            ItemConfirm(text = '[font=Font/NotoSansSC-Regular.otf]{}[/font]'.format(langDict['TipOfShoulder'][self.state])),
            ItemConfirm(text = '[font=Font/NotoSansSC-Regular.otf]{}[/font]'.format(langDict['CANCEL'][self.state])),
            ItemConfirm(text = '[font=Font/NotoSansSC-Regular.otf]{}[/font]'.format(langDict['CANCEL'][self.state])),
            ItemConfirm(text = '[font=Font/NotoSansSC-Regular.otf]{}[/font]'.format(langDict['CANCEL'][self.state]))
        }

        if not self.PointDrawDialog:
            FinalView = list(SideViewItem)
            if self.View == 0:
                FinalView = list(FrontViewItem)
            self.PointDrawDialog = MDDialog(
                title = '[font=Font/NotoSansSC-Regular.otf]{}[/font]'.format(langDict['PointChoosing'][self.state]),
                type = 'confirmation',
                items = FinalView,
                buttons = [
                        MDFlatButton(
                            text=langDict["CANCEL"][self.state], text_color=self.theme_cls.primary_color, on_release= self.closePointDraw
                        ),
                        MDFlatButton(
                            text=langDict["CONFIRM"][self.state],text_color=self.theme_cls.primary_color, on_release= self.continuePointDraw
                        ),
                    ],
            )
        self.PointDrawDialog.set_normal_height()
        self.PointDrawDialog.open()

    def setDegreeDialog(self):
        #Dialog that give user ability to choose what degree they want to rotate
        if not self.RotationDegreeDialog:
            self.RotationDegreeDialog = MDDialog(
                title = '[font=Font/NotoSansSC-Regular.otf]{}[/font]'.format(langDict['SetRotationDegreeSpecific'][self.state]),
                type = 'custom',
                content_cls = RotationValue(),
                buttons=[
                    MDFlatButton(
                        text=langDict["CANCEL"][self.state], text_color=self.theme_cls.primary_color,
                        on_release=self.closeRotateDialog
                    ),
                    MDFlatButton(
                        text=langDict["CONFIRM"][self.state], text_color=self.theme_cls.primary_color,
                        on_release=self.closeRotateDialogAction
                    ),
                ],
            )
        self.RotationDegreeDialog.set_normal_height()
        self.RotationDegreeDialog.open()

    def errorDialog(self, keyString):
        #Error Dialog
        self.error_dialog = None
        if not self.error_dialog:
            self.error_dialog = MDDialog(
                text='[font=Font/NotoSansSC-Regular.otf]{}[/font]'.format(langDict[keyString][self.state]),
                radius = [20, 7, 20, 7],
            )
        self.error_dialog.open()


    #Function here that execute about all dialog button callback
    def BugSettingCallBack(self, inst):
        self.BugSetting_dialog.dismiss()
        self.BugSetting_dialog = None
        self.change_screen(inst)



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
            if isinstance(obj, TextInput):
                lista.append(obj.text)
                obj.text = ""
        self.VerticalLine = int(lista[0])
        self.HorizontalLine = int(lista[1])
        self.dialog.dismiss()
        self.dialog = None
        self.UpdateConfig()

    def closeDialog(self, inst):
        self.dialog.dismiss()
        self.dialog = None


    def closePointDraw(self, inst):
        self.PointDrawDialog.dismiss()
        self.PointDrawDialog = None

    def continuePointDraw(self, inst):
        result_text = ""
        for i in self.PointDrawDialog.items:
            if i.ids.check.active:
                result_text = i.text.split('[')[1].split(']')[1]
        if result_text in self.coordinateDict:
            self.confirm_remove_setting(self.closeReplaceDialogAction, "ReplaceConfirm")
        else:
            self.PointDrawDialog.dismiss()
            self.PointDrawDialog = None
        self.coordinateKey = result_text
        self.capturePoint = True

    def closeRotateDialog(self, inst):
        self.RotationDegreeDialog.dismiss()
        self.RotationDegreeDialog = None

    def closeRotateDialogAction(self, inst):
        self.RotationDegreeDialog.dismiss()
        self.rotateDegree = int(self.RotationDegreeDialog.content_cls.ids.ROValue.value)
        self.RotationDegreeDialog = None
        self.UpdateConfig()

    def closeReplaceDialogAction(self, inst):
        del self.coordinateDict[self.coordinateKey]
        self.remove_confirm.dismiss()
        self.remove_confirm = None
        self.PointDrawDialog.dismiss()
        self.PointDrawDialog = None

    def confirmSwitchView(self, inst):
        self.remove_confirm.dismiss()
        self.remove_confirm = None
        if self.View == 0:
            self.View = 1
        else:
            self.View = 0
        self.coordinateDict.clear()

    def storeDialogConfirm(self, inst):
        self.remove_confirm.dismiss()
        self.remove_confirm = None
        self.coordinateDict[self.coordinateKey] = self.captureCoordinate
        self.captureCoordinate = None
        self.capturePoint = False
        print(self.coordinateDict)

    #Function here about all the button callback function

    def clear_all(self,objectname):
        try:
            for i in self.remove_list:
                objectname.canvas.remove(i)
            self.remove_list.clear()
        except:
            pass
        self.image_source = "icons/no-camera.png"
        self.default_image = True


    def change_screen(self,screen_name):
        screen_manager = self.root.ids['screen_manager']
        screen_manager.transition = NoTransition()
        screen_manager.current = screen_name 
    

            
    def send_message(self, text):
        try:
            print(text)
        except:
            print('Something went wrong')
       

    def modify_image(self,objectname):
        horizontal = self.HorizontalLine
        vertical = self.VerticalLine
        if self.VerticalLine > 20:
            vertical = 20
        if self.HorizontalLine > 20:
            horizontal = 20
        with objectname.canvas:
            Color(0, 0, 0)
            for k in range(vertical):
                temp = Line(points=[objectname.x + objectname.width // (vertical + 1) * (k+1), objectname.y, objectname.x + objectname.width // (vertical + 1) * (k+1), objectname.y + objectname.height], width=1.2)
                self.remove_list.append(temp)
            for i in range(horizontal):
                temp = Line(points=[objectname.x, objectname.y + (objectname.height //(horizontal + 1) * (i + 1)), objectname.x + objectname.width, objectname.y + (objectname.height // (horizontal + 1) * (i+1))], width=1.2)
                self.remove_list.append(temp)


    def change_picture(self, source):
        self.image_source = source
        self.root.ids.second_screen.image_change.reload()
        self.default_image = False
        self.change_screen("second_screen")
        #Clock.schedule_once(partial(self.modify_image, self.VerticalLine,self.HorizontalLine,self.root.ids.second_screen.image_change), 1)
        #self.modify_image(self.VerticalLine, self.HorizontalLine, self.root.ids.second_screen.image_change)


    def switchView(self):
        self.confirm_remove_setting(self.confirmSwitchView, "SwitchViewConfirm")


    def imagePosCallBack(self, *args):
        if self.capturePoint:
            if args[0][1].is_double_tap:
                if self.captureCoordinate != None:
                    self.confirm_remove_setting(self.storeDialogConfirm, "SavingCoordinateConfirm")
            elif args[0][1].is_triple_tap:
                pass
            else:
                self.captureCoordinate = args[0][1].pos

    #Changing APP Setting Function
    def switchLanguage(self):
        if self.state == 1:
            self.state = 0
        else:
            self.state = 1
        self.UpdateConfig()

    def switchRotateDegree(self, rotationDegree):
        self.rotateDegree = rotationDegree
        self.UpdateConfig()


    def resetDefaultSetting(self, inst):
        location = 'dev.ini'
        if platform == 'ios':
            savepath = MDApp.get_running_app().user_data_dir
            location = join(savepath, location)
        if exists(location):
            remove(location)
        self.state = 0
        self.rotateDegree = 90
        self.HorizontalLine = 8
        self.VerticalLine = 8
        self.remove_confirm.dismiss()
        self.remove_confirm = None


    def UpdateConfig(self):
        parser = ConfigParser()
        parser['Setting'] = {
            'lang': str(self.state),
            'rotationDegree': str(self.rotateDegree),
            'VerticalLine': str(self.VerticalLine),
            'HorizontalLine': str(self.HorizontalLine)
        }
        savefileName = 'dev.ini'
        if platform == 'ios':
            savepath = MDApp.get_running_app().user_data_dir
            savefileName = join(savepath, savefileName)
        with open(savefileName, 'w') as f:
            parser.write(f)

    #Function that calls to camera, filechooser or their associate callback function
    def capture(self):

        try:
            file_name = "test.png"
            if platform == 'ios':
                savepath = MDApp.get_running_app().user_data_dir
                savepath = savepath[:len(savepath) - 4]
                file_name = join(savepath, file_name)
            camera.take_picture(filename = file_name,on_complete = self.camera_callback)

        except NotImplementedError:
            self.errorDialog('ErrorOpeningCamera')



    def camera_callback(self, filename):
        if (exists(filename)):
            self.change_picture(filename)

    def open_photos(self):
        try:
            filechooser.open_file(on_selection=self.handle_selection)
        except NotImplementedError:
            self.errorDialog('ErrorOpeningFileChooser')


    def handle_selection(self,selection):
        try:
            self.selection = selection
            self.change_picture(self.selection[0])
        except:
            pass

    def Contact(self):
        try:
            email.send(recipient = "Junhano@uci.edu")
        except NotImplementedError:
            self.errorDialog('ErrorOpeningMail')






MainApp().run()
