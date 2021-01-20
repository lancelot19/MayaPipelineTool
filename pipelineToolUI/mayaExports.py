
from maya.cmds import pause
from pipelineToolUI.setTypeAttribWindow import *

import os

_IN_MAYA_ = False

try:
    from maya import cmds
    
    _IN_MAYA_ = True
except:
    print("PAS DANS MAYA")

class MayaExports():

    def mayaExportPath(self, rootPath):
        
        self.exportPath = rootPath

        print('Maya export path is : ' + self.exportPath)

    def treeVerification(self):
        self.setAttribDial = SetTypeAttribWindow()

        self.typeTagDic = {'ch' : 'characters', 'cl' : 'cloth' ,'en' : 'environment',
                            'p' : 'props', 'pt' : 'propsTunnel', 'pa' : 'propsArene',
                            'pf': 'propsFemale', 'pm' : 'propsMale'}

        mySel = cmds.ls(sl = True)

        for each in mySel:

            self.tagQuery = cmds.attributeQuery('typeTag', node = each, exists = True)

            if(not self.tagQuery):
                print('tag is not existing')
                self.setAttribDial.show()
                
            else:
                self.tagValue = cmds.getAttr(each + '.typeTag')
                for(key, value) in self.typeTagDic.items():
                    if(self.tagValue == key):
                        print(value)
                if(self.tagValue == ''):
                    print('Value Error')
                    self.setAttribDial.show()
            
            
            '''
            self.IADirs = [self.exportPath + r"/assets/characters/" + each + r"/publishs/modeling",
            self.exportPath + r"/assets/characters/" + each + r"/publishs/rigging",
            self.exportPath + r"/assets/characters/" + each + r"/publishs/shading",
            self.exportPath + r"/assets/characters/" + each + r"/publishs/texturing",
            self.exportPath + r"/assets/characters/" + each + r"/publishs/uv",
            self.exportPath + r"/assets/characters/" + each + r"/refs/images",
            self.exportPath + r"/assets/characters/" + each + r"/refs/videos",
            self.exportPath + r"/assets/characters/" + each + r"/tasks/modeling",
            self.exportPath + r"/assets/characters/" + each + r"/tasks/rigging",
            self.exportPath + r"/assets/characters/" + each + r"/tasks/shading",
            self.exportPath + r"/assets/characters/" + each + r"/tasks/texturing",
            self.exportPath + r"/assets/characters/" + each + r"/tasks/uv"]

            for dirs in self.IADirs:
                self.verification = os.path.isdir(dirs)

                if(self.verification == False):
                    os.makedirs(dirs)
            '''