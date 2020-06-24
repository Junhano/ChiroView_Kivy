from Helper.EvaDict import ResultsDict

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
            if (abs(self.coordinate_dict["LeftEye"][1] - self.coordinate_dict["RightEye"][1]) >= 5):
                error_list.append("Eye")
        if "LeftEar" in self.coordinate_dict and "RightEar" in self.coordinate_dict:
            if (abs(self.coordinate_dict["LeftEar"][1] - self.coordinate_dict["RightEar"][1]) >= 5):
                error_list.append("Ear")
        if "LeftShoulderTip" in self.coordinate_dict and "RightShoulderTip" in self.coordinate_dict:
            if (abs(self.coordinate_dict["LeftShoulderTip"][1] - self.coordinate_dict["RightShoulderTip"][1]) >= 5):
                error_list.append("Shoulder Tip")
        if "LeftMiddleKneeCap" in self.coordinate_dict and "RightMiddleKneeCap" in self.coordinate_dict:
            if (abs(self.coordinate_dict["LeftMiddleKneeCap"][1] - self.coordinate_dict["RightMiddleKneeCap"][1]) >= 5):
                error_list.append("Middle Knee Cap")
        if "LeftMedialAnkle" in self.coordinate_dict and "RightMedialAnkle" in self.coordinate_dict:
            if (abs(self.coordinate_dict["LeftMedialAnkle"][1] - self.coordinate_dict["RightMedialAnkle"][1]) >= 5):
                error_list.append("Medial Ankle")

        return error_list

    def sideCalculation(self):
        #Algorithm is put the 6 point or things into a line, and calculate the range
        #of the coordinates, and if it is smaller than some value, it will put them in the error_list

        error_list = list()
        result_list = list()
        for k,v in self.coordinate_dict.items():
            result_list.append((k,v[0]))
        while len(result_list) > 0 and (max(result_list, key = lambda x: x[1]) - min(result_list, key = lambda x: x[1]) >= 10):
            error_list.append(max(result_list, key = lambda x:x[1])[0])
            error_list.append(min(result_list, key = lambda x:x[1])[0])
            result_list.remove(max(result_list, key = lambda x:x[1]))
            result_list.remove(min(result_list, key = lambda x:x[1]))
        return error_list

    def displayResults(self):
        if self.view == 'FRONT':
            result = self.frontCalculation()
        else:
            result = self.sideCalculation()
        result_str = ""
        if len(result) == 0:
            result_str += ResultsDict["NoError"][self.lang]
        else:
            pass
        return result_str

'''     
class ImagePosture(Posture):
    def __init__(self):
        pass
'''