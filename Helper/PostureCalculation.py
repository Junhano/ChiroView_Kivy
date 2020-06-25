from Helper.EvaDict import ResultsDict


verticalLineSideCheckList = ['EarCanal', 'TipOfShoulder', 'Trochanter', 'lateralmalleolus']
verticalLineFrontCheckList = ['NoseTip', 'SternalNotch', 'Umbilicus']

class Posture:
    def __init__(self, dict1, view, lang):
        self.coordinate_dict = dict1
        self.view = view
        self.lang = lang

    def frontCalculation(self):
        #Algorithm is first calculate all the components that need to be at the same line,
        #Then calculate the midpoint and see if the components that need to be at the mid point is at the
        #mid point
        error_list = list()
        if "LeftEye" in self.coordinate_dict and "RightEye" in self.coordinate_dict:
            if abs(self.coordinate_dict["LeftEye"][1] - self.coordinate_dict["RightEye"][1]) >= 3:
                error_list.append("Eye")
        if "LeftEar" in self.coordinate_dict and "RightEar" in self.coordinate_dict:
            if abs(self.coordinate_dict["LeftEar"][1] - self.coordinate_dict["RightEar"][1]) >= 3:
                error_list.append("Ear")
        if "LeftShoulderTip" in self.coordinate_dict and "RightShoulderTip" in self.coordinate_dict:
            if abs(self.coordinate_dict["LeftShoulderTip"][1] - self.coordinate_dict["RightShoulderTip"][1]) >= 3:
                error_list.append("Shoulder Tip")
        if "LeftKneeCap" in self.coordinate_dict and "RightKneeCap" in self.coordinate_dict:
            if abs(self.coordinate_dict["LeftMiddleKneeCap"][1] - self.coordinate_dict["RightMiddleKneeCap"][1]) >= 3:
                error_list.append("Middle Knee Cap")
        if "LeftAnkle" in self.coordinate_dict and "RightAnkle" in self.coordinate_dict:
            if abs(self.coordinate_dict["LeftMedialAnkle"][1] - self.coordinate_dict["RightMedialAnkle"][1]) >= 3:
                error_list.append("Medial Ankle")
        if "LASIS" in self.coordinate_dict and "RASIS" in self.coordinate_dict:
            if abs(self.coordinate_dict["LASIS"][1] - self.coordinate_dict["RASIS"][1]) >= 3:
                error_list.append("ASIS")

        check_value = list()
        for i in verticalLineFrontCheckList:
            if i in self.coordinate_dict:
                check_value.append(self.coordinate_dict[i][0])
        if len(check_value) != 0:
            if max(check_value) - min(check_value) >= 5:
                error_list.append('No Stright')


        return error_list

    def sideCalculation(self):
        #Algorithm is put the 4 point or things into a line, and calculate the range
        #of the coordinates, and if it is smaller than some value, it will put them in the error_list

        error_list = list()
        check_value = list()
        for i in verticalLineSideCheckList:
            if i in self.coordinate_dict:
                check_value.append(self.coordinate_dict[i][0])
        if len(check_value) != 0:
            if max(check_value) - min(check_value) >= 5:
                error_list.append('Bad Posture')
        return error_list

    def displayResults(self):
        if self.view == 0:
            result = self.frontCalculation()
        else:
            result = self.sideCalculation()
        result_str = ""
        if len(result) == 0:
            result_str += ResultsDict["NoError"][self.lang]
        else:
            result_str += ResultsDict["ErrorBegin"][self.lang]
            result_str += '\n\n'
            if self.view == 0:
                for k,i in enumerate(result):
                    result_str += str(k) + '. '
                    if i == "No Stright":
                        result_str += ResultsDict['NoStrightFront'][self.lang]
                    else:
                        result_str += ResultsDict['LR'][self.lang]
                        result_str += ResultsDict[i][self.lang]
                        result_str += ResultsDict['NotOnSameHorizontalLine'][self.lang]
                    result_str += '\n'
            else:
                for k,i in enumerate(result):
                    if i == 'Bad Posture':
                        result_str += str(k) + '. '
                        result_str += ResultsDict['BadSidePosture'][self.lang]
                        result_str += '\n'
        return result_str

