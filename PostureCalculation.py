class Posture:
    def __init__(self, dict1, view):
        self.coordinate_dict = dict1
        self.view = view
        self.horizontal_check = ['Eye', 'Ear', 'ShoulderTip', 'Knee cap', 'Middle Ankle']

    def frontCalculation(self):
        error_list = list()
        return error_list
    def sideCalculation(self):
        error_list = list()
        list1 = list()
        for k,v in self.coordinate_dict.items():
            list1.append((k, v[0]))
        return error_list
    def displayResults(self):
        if self.view == 'FRONT':
            result = self.frontCalculation()
        else:
            result = self.sideCalculation()

        for i in result:
            pass

'''     
class ImagePosture(Posture):
    def __init__(self):
        pass
'''