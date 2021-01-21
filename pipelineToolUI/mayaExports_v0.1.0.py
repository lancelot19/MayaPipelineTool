
from pipelineToolUI.setTypeAttribWindow import *

import os

_IN_MAYA_ = False
try:
    from maya import cmds
    
    _IN_MAYA_ = True
except:
    print("PAS DANS MAYA")

class MayaExports():

    def getExportPath(self, rootPath):
        """This function get the root export path.
        Activated in pipelineUI in the exports functions.

        Args:
            rootPath (string): The root path got in pipelineUI 
        """

        self.exportPath = rootPath

        print('Maya export path is : ' + self.exportPath)
    
    def defineItemsTeam(self, defTeam):
        """This function get the team name.
        Activated in pipelineUI in the exports functions.

        Args:
            defTeam (string): The team name got in pipelineUI.
        """
        self.team = defTeam

    def typeTagAttribCreation(self):
        """This function allow to verify if the typeTag exists.
        If not exists, the function call the setTypeAttribWindow
        to set the attributs on each assets with personalized tags by team name.
        """

        self.setAttribDial = SetTypeAttribWindow()                                      #Instantiate the SetTypeAttribWindow class.

        self.typeTagDic = {'ch' : 'characters', 'cl' : 'cloth' ,'en' : 'environment',
                            'p' : 'props', 'pt' : 'propsTunnel', 'pa' : 'propsArene',
                            'pf': 'propsFemale', 'pm' : 'propsMale'}                    # Define a dictionnary of tags possibilities as keys and their values.

        self.mySel = cmds.ls(sl = True)                                                 # Get the current selection in a list.

        self.dicValue = ''

        if(self.team == 'IA'):                                                          # Condition to set comboBox items of the QDialog Window by team name.
            self.setAttribDial.items(team = 'IA')
        elif(self.team == 'LDS'):
            self.setAttribDial.items(team = 'LDS')

        for each in self.mySel:                                                         # For loop on the current selection.

            self.tagQuery = cmds.attributeQuery('typeTag', node = each, exists = True)  # Query if the typeTag attribute exists.

            if(not self.tagQuery):                                                      # If the attribute not exists.
                print('tag is not existing')
                self.setAttribDial.assetName(each)                                      # Get the selected asset name and return it to the QDialog Window.



                self.setAttribDial.show()                                               # Call the QDialog Window SetTypeAttribWindow.

                if(self.setAttribDial.exec_()):                                         # If the QDialog Window is executed.

                    self.getTypeTag = self.setAttribDial.comboBox.currentText()         # Get the value wanted to set from the QDialog comboBox.

                    createAttr      = cmds.addAttr(each, shortName = 'typeTag', longName = 'typeTag', dt = 'string')                        # Create attribute of type string on Transform.
                    setAttri        = cmds.setAttr(each + '.typeTag', self.getKeyDict(self.typeTagDic, self.getTypeTag), type = 'string')   # Set the attribute with the getKeyDict function.
                    
            else:                                                                       # Else, the attribute exists.

                self.tagValue = cmds.getAttr(each + '.typeTag')                         # Get the typeTag value.

                if(self.tagValue == ''):                                                # If the value is empty.
                    
                    self.setAttribDial.assetName(each)                                  # Get the selected asset name and return it to the QDialog Window.

                    self.setAttribDial.show()                                           # Call the QDialog Window SetTypeAttribWindow.

                    if(self.setAttribDial.exec_()):                                     # If the QDialog Window is executed.

                        self.getTypeTag = self.setAttribDial.comboBox.currentText()     # Get the value wanted to set from the QDialog comboBox.

                        setAttri        = cmds.setAttr(each + '.typeTag', self.getKeyDict(self.typeTagDic, self.getTypeTag), type = 'string')   # Set the attribute with the getKeyDict function.
            self.getDicValue(each)
            self.verifyAssetTreeStructure(each)

    def getDicValue(self, each):

        self.tagValue = cmds.getAttr(each + '.typeTag')                                 # Get the typeTag value.

        for(key, value) in self.typeTagDic.items():                                     # For loop on the typeTagDic to know if the value corresponds to a key.
            if(self.tagValue == key):                                                   # If the value corresponds to a key.

                self.dicValue = value

    def getKeyDict(self, dict, val):
        """This funtion allow to get a key from the value.

        Args:
            dict (dictionnary): The dictionnary in we want to verify.
            val (string): The value with we want to verify.

        Returns:
            (string): The key of the good value.
        """

        for key, value in dict.items():
            if val == value:
                return key

    def verifyAssetTreeStructure(self, each):
        """This function allows to verify if the treeStructure of the assets
        existing before exporting them.
        """

        self.assetDirs = [self.exportPath + r"/assets/" + self.dicValue + r"/" + each + r"/publishs/modeling",
        self.exportPath + r"/assets/" + self.dicValue + r"/" + each + r"/publishs/rigging",
        self.exportPath + r"/assets/" + self.dicValue + r"/" + each + r"/publishs/shading",
        self.exportPath + r"/assets/" + self.dicValue + r"/" + each + r"/publishs/texturing",
        self.exportPath + r"/assets/" + self.dicValue + r"/" + each + r"/publishs/uv",
        self.exportPath + r"/assets/" + self.dicValue + r"/" + each + r"/refs/images",
        self.exportPath + r"/assets/" + self.dicValue + r"/" + each + r"/refs/videos",
        self.exportPath + r"/assets/" + self.dicValue + r"/" + each + r"/tasks/modeling",
        self.exportPath + r"/assets/" + self.dicValue + r"/" + each + r"/tasks/rigging",
        self.exportPath + r"/assets/" + self.dicValue + r"/" + each + r"/tasks/shading",
        self.exportPath + r"/assets/" + self.dicValue + r"/" + each + r"/tasks/texturing",
        self.exportPath + r"/assets/" + self.dicValue + r"/" + each + r"/tasks/uv"]

        for dirs in self.assetDirs:
            self.verification = os.path.isdir(dirs)

            if(self.verification == False):
                os.makedirs(dirs)