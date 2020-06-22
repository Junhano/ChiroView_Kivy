from kivymd.app import MDApp
from kivy.lang import Builder
from kivy.uix.screenmanager import Screen, NoTransition
from kivy.uix.button import ButtonBehavior
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.image import Image
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
from kivy.graphics import Line, Color, Ellipse
from kivy.clock import Clock
from os import remove
import functools
from collections import defaultdict

valuetoKeyDict = dict()
for k,v in langDict.items():
    for x, y in v.items():
        valuetoKeyDict[y] = k

class ItemConfirm(OneLineAvatarIconListItem):
    divider = None

    def set_icon(self, instance_check):
        instance_check.active = True
        check_list = instance_check.get_widgets(instance_check.group)
        for check in check_list:
            if check != instance_check:
                check.active = False


ConnectBodyPart = {
    'LeftEye': ['RightEye', 'NoseTip'],
    'RightEye': ['LeftEye', 'NoseTip'],
    'LeftEar': ['RightEar'],
    'RightEar': ['LeftEar'],
    'NoseTip': ['LeftEye', 'RightEye', 'SternalNotch'],

            #...

}


def tuple_coordinate_key_generate(coordinate1, coordinate2):
    if coordinate1[0] > coordinate2[0] or (coordinate1[0] == coordinate2[0] and coordinate1[1] > coordinate2[1]):
        return coordinate2, coordinate1
    elif coordinate1[0] < coordinate1[1] or (coordinate1[0] == coordinate2[0] and coordinate1[1] < coordinate2[1]):
        return coordinate1, coordinate2


class ImageButton(ButtonBehavior,Image):
    pass

class HomeScreen(Screen):
    pass

class SecondScreen(Screen):
    image_change = ObjectProperty(None)


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
    default_image = BooleanProperty(True)

    NumberLineChoosedialog = None  #Dialog that prompt user for how many lines to draw both vertically and horizontally
    cancelconfirm = None      #Dialog that confirm user to remove the picture from the canvas
    error_dialog = None          #Dialog that give user error alert when things go wrong
    BugSetting_dialog = None    #Dialog that give user to choose what option they want to enter to either change setting, contact or get help etc
    StartExamDialog = None      #Dialog that give user to choose picture when they haven't choose it yet
    ChooseBodyPartDialog = None     #Dialog that give user to choose what kind of body part they want to points
    RotationDegreeDialog = None  #Dialog that give user the ability to choose how many degree they want to rotate
    DeleteBodyPartDialog = None

    image_source = StringProperty("icons/no-camera.png")

    coordinateDict = dict()
    coordinateKey = None #Key from the bodypart list
    userChooseCord = False   #Did system chose the point or not, if no user cannot double tap to save image
    captureCoordinate = None     #What's the point that user captured

    CanvasDrawingCoordinate = dict()  #Dictionary that store each point coordinate, for future deletion reference
    CanvasConnectionInfo = defaultdict(list)  #Dictionary that store the line content, for bodypart connection line check
    CanvasLineDrawingContent = dict() #Dictionary that store the lines and for future deletion reference

    @staticmethod
    def compareFuncAlreadyChose(Item1, Item2):
        if Item1.text.split('[')[1].split(']')[1] > Item2.text.split('[')[1].split(']')[1]:
            return 1
        else:
            return -1





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

    def delete_Body_Part_Dialog(self):
        if not self.DeleteBodyPartDialog:
            BodyList = []
            for k in self.coordinateDict.keys():
                BodyList.append(ItemConfirm(text = '[font=Font/NotoSansSC-Regular.otf]{}[/font]'.format(langDict[k][self.state])))
            cmp = functools.cmp_to_key(MainApp.compareFuncAlreadyChose)
            FinalView = sorted(BodyList, key = cmp)
            FinalView.append(ItemConfirm(text = '[font=Font/NotoSansSC-Regular.otf]{}[/font]'.format(langDict['DeleteAll'][self.state])))
            self.DeleteBodyPartDialog = MDDialog(
                title = '[font=Font/NotoSansSC-Regular.otf]{}[/font]'.format(langDict["DeleteCord"][self.state]),
                type = "confirmation",
                items = FinalView,
                buttons=[
                    MDFlatButton(
                        text=langDict["CANCEL"][self.state], text_color=self.theme_cls.primary_color,
                        on_release=self.closeDeleteCoordinateDialog
                    ),
                    MDFlatButton(
                        text=langDict["CONFIRM"][self.state], text_color=self.theme_cls.primary_color,
                        on_release=self.continueDeleteCoordinateDialog
                    ),
                ],
            )
        self.DeleteBodyPartDialog.set_normal_height()
        self.DeleteBodyPartDialog.open()

    def grid_image_create_setting(self):
        #Dialog that about line draw setting, how many lines
        if not self.NumberLineChoosedialog:
            self.NumberLineChoosedialog = MDDialog(
                title= '[font=Font/NotoSansSC-Regular.otf]{}[/font]'.format(langDict["EnterNumber"][self.state]),
                type="custom",
                content_cls=LineContent(),
                buttons=[
                        MDFlatButton(
                            text=langDict["CANCEL"][self.state], text_color=self.theme_cls.primary_color, on_release= self.closeDialog
                        ),
                        MDFlatButton(
                            text=langDict["APPLY"][self.state],text_color=self.theme_cls.primary_color, on_release=self.setLineAmount
                        ),
                    ],
                )
        self.NumberLineChoosedialog.set_normal_height()
        self.NumberLineChoosedialog.open()

    def confirm_setting(self, func, keyStr, cancelFunc = None, left_button = None, right_button = None):
        if cancelFunc is None:
            cancelFunc = self.dismissRemoveConfirm
        if left_button is None:
            left_button = "CANCEL"
        if right_button is None:
            right_button = "CONFIRM"
        #Dialog that about remove picture from canvas
        if not self.cancelconfirm:
            self.cancelconfirm = MDDialog(
                text= '[font=Font/NotoSansSC-Regular.otf]{}[/font]'.format(langDict[keyStr][self.state]),
                type="custom",
                buttons=[
                        MDFlatButton(
                            text=langDict[left_button][self.state], text_color=self.theme_cls.primary_color, on_release= cancelFunc
                        ),
                        MDFlatButton(
                            text=langDict[right_button][self.state],text_color=self.theme_cls.primary_color, on_release= func
                        ),
                    ],
                )
        self.cancelconfirm.set_normal_height()
        self.cancelconfirm.open()

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

    def BeginDialog(self):
        #Dialog that give user choice to choose picture when they haven't choose it yet
        if not self.StartExamDialog:
            self.StartExamDialog = MDDialog(
                title = '[font=Font/NotoSansSC-Regular.otf]{}[/font]'.format(langDict["OptionForUserWhenNoImage"][self.state]),
                type = "custom",
                content_cls = Helper()
            )
        self.StartExamDialog.set_normal_height()
        self.StartExamDialog.open()

    def IdentifyBodyPartDialog(self):
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

        if not self.ChooseBodyPartDialog:
            FinalView = list(FrontViewItem)
            if self.View == 1:
                FinalView = list(SideViewItem)
            cmp = functools.cmp_to_key(MainApp.compareFuncAlreadyChose)
            FinalView = sorted(FinalView, key = cmp)
            self.ChooseBodyPartDialog = MDDialog(
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
        self.ChooseBodyPartDialog.set_normal_height()
        self.ChooseBodyPartDialog.open()

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

    def continueDeleteCoordinateDialog(self, inst):
        for i in self.DeleteBodyPartDialog.items:
            if i.ids.check.active:
                result_text = i.text.split('[')[1].split(']')[1]
                if valuetoKeyDict[result_text] != 'DeleteAll':
                    self.deletePoint(self.root.ids.second_screen.image_change, self.coordinateDict[valuetoKeyDict[result_text]])
                    self.deleteConnectedLine(self.root.ids.second_screen.image_change, valuetoKeyDict[result_text])
                    del self.coordinateDict[valuetoKeyDict[result_text]]
                else:
                    for v in self.CanvasDrawingCoordinate.values():
                        self.root.ids.second_screen.image_change.canvas.remove(v)
                    for z in self.CanvasLineDrawingContent.values():
                        self.root.ids.second_screen.image_change.canvas.remove(z)
                    self.CanvasConnectionInfo.clear()
                    self.CanvasLineDrawingContent.clear()
                    self.coordinateDict.clear()
                    self.CanvasDrawingCoordinate.clear()
        self.DeleteBodyPartDialog.dismiss()
        self.DeleteBodyPartDialog = None
        print(self.coordinateDict)

    def closeDeleteCoordinateDialog(self, inst):
        self.DeleteBodyPartDialog.dismiss()
        self.DeleteBodyPartDialog = None

    def changeBackScreenWithOutSave(self, inst):
        self.image_source = "icons/no-camera.png"
        self.default_image = True
        self.cancelconfirm.dismiss()
        self.cancelconfirm = None
        for v in self.CanvasDrawingCoordinate.values():
            self.root.ids.second_screen.image_change.canvas.remove(v)
        for z in self.CanvasLineDrawingContent.values():
            self.root.ids.second_screen.image_change.canvas.remove(z)
        self.CanvasConnectionInfo.clear()
        self.CanvasLineDrawingContent.clear()
        self.CanvasDrawingCoordinate.clear()
        self.coordinateDict.clear()
        self.change_screen('home_screen')

    def changeBackScreenWithSave(self, inst):
        self.cancelconfirm.dismiss()
        self.cancelconfirm = None
        self.change_screen('home_screen')


    def BugSettingCallBack(self, inst):
        self.BugSetting_dialog.dismiss()
        self.BugSetting_dialog = None
        self.change_screen(inst)


    def dismissRemoveConfirm(self, inst):
        self.cancelconfirm.dismiss()
        self.cancelconfirm = None

    def setLineAmount(self, inst):
        lista = []
        for obj in self.NumberLineChoosedialog.content_cls.children:
            if isinstance(obj, TextInput):
                lista.append(obj.text)
                obj.text = ""
        self.VerticalLine = int(lista[0])
        self.HorizontalLine = int(lista[1])
        self.NumberLineChoosedialog.dismiss()
        self.NumberLineChoosedialog = None
        self.UpdateConfig()

    def closeDialog(self, inst):
        self.NumberLineChoosedialog.dismiss()
        self.NumberLineChoosedialog = None


    def closePointDraw(self, inst):
        self.ChooseBodyPartDialog.dismiss()
        self.ChooseBodyPartDialog = None

    def continuePointDraw(self, inst):
        result_text = ""
        for i in self.ChooseBodyPartDialog.items:
            if i.ids.check.active:
                result_text = i.text.split('[')[1].split(']')[1]
        if valuetoKeyDict[result_text] in self.coordinateDict:
            self.confirm_setting(self.closeReplaceDialogAction, "ReplaceConfirm")
        else:
            self.ChooseBodyPartDialog.dismiss()
            self.ChooseBodyPartDialog = None
        self.coordinateKey = valuetoKeyDict[result_text]
        #self.capturePoint = True

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
        self.cancelconfirm.dismiss()
        self.cancelconfirm = None
        self.PointDrawDialog.dismiss()
        self.PointDrawDialog = None

    def confirmSwitchView(self, inst):
        self.cancelconfirm.dismiss()
        self.cancelconfirm = None
        if self.View == 0:
            self.View = 1
        else:
            self.View = 0
        self.coordinateDict.clear()

    def storeDialogConfirm(self, inst):
        self.cancelconfirm.dismiss()
        self.cancelconfirm = None
        self.coordinateDict[self.coordinateKey] = self.captureCoordinate
        self.drawPoints(self.root.ids.second_screen.image_change, self.captureCoordinate[0], self.captureCoordinate[1])
        self.captureCoordinate = None
        self.coordinateKey = None
        self.drawConnectedLine(self.root.ids.second_screen.image_change)

    #Function here about all the button callback function

    def change_screen(self,screen_name):
        screen_manager = self.root.ids['screen_manager']
        screen_manager.transition = NoTransition()
        screen_manager.current = screen_name 
    

            
    def send_message(self, text):
        try:
            print(text)
        except:
            print('Something went wrong')


    def change_picture(self, source):
        self.image_source = source
        self.root.ids.second_screen.image_change.reload()
        self.change_screen("second_screen")


    def switchView(self):
        self.confirm_setting(self.confirmSwitchView, "SwitchViewConfirm")

    def imagePosCallBack(self, *args):
        if self.root.ids.second_screen.image_change.collide_point(*args[0][1].pos):
            if self.coordinateKey is not None:
                if args[0][1].is_double_tap:
                    self.confirm_setting(self.storeDialogConfirm, "SavingCoordinateConfirm")
                else:
                    self.captureCoordinate = args[0][1].pos
            else:
                self.IdentifyBodyPartDialog()


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
        self.cancelconfirm.dismiss()
        self.cancelconfirm = None


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


    #Canvas update drawing function
    def drawPoints(self, objectname, pos_x, pos_y):
        pos1 = pos_x, pos_y
        with objectname.canvas:
            Color(0,0,0)
            temp = Ellipse(pos = pos1, size = (5,5))
            self.CanvasDrawingCoordinate[pos1] = temp

    def deletePoint(self, objectname, pos):
        objectname.canvas.remove(self.CanvasDrawingCoordinate[pos])
        del self.CanvasDrawingCoordinate[pos]

    def drawConnectedLine(self, objectname):

        for k,v in ConnectBodyPart.items():
            #loop through the connect body part dictionary where those body part if chose by user, system will
            #automatically drew a line
            for i in v:
                if k in self.coordinateDict and i in self.coordinateDict:
                    #if they both get chose
                    if k not in self.CanvasConnectionInfo or i not in self.CanvasConnectionInfo[k]:#
                        with objectname.canvas:
                            temp = Line(points=[self.coordinateDict[k], self.coordinateDict[i]], width=1.2)
                            self.CanvasConnectionInfo[k].append(i)
                            self.CanvasConnectionInfo[i].append(k)
                            tupleKey = tuple_coordinate_key_generate(self.coordinateDict[k], self.coordinateDict[i])
                            self.CanvasLineDrawingContent[tupleKey] = temp

    def deleteConnectedLine(self, objectname, deletepoint):
        for c in self.CanvasConnectionInfo[deletepoint]:
            self.CanvasConnectionInfo[c].remove(deletepoint)
            tuplekey = tuple_coordinate_key_generate(self.coordinateDict[deletepoint], self.coordinateDict[c])
            objectname.canvas.remove(self.CanvasLineDrawingContent[tuplekey])
            del self.CanvasLineDrawingContent[tuplekey]

        del self.CanvasConnectionInfo[deletepoint]




MainApp().run()
