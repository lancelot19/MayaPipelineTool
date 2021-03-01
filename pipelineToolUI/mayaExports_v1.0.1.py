
from pipelineToolUI.setTypeAttribWindow import *

import os, shutil

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
    
    def defineItemsTeam(self, defTeam):
        """This function get the team name.
        Activated in pipelineUI in the exports functions.

        Args:
            defTeam (string): The team name got in pipelineUI.
        """
        self.team = defTeam

    def currentSel(self):

        self.mySel = cmds.ls(sl = True)

    def typeTagAttribCreation(self, aOrS):
        """This function allow to verify if the typeTag exists.
        If not exists, the function call the setTypeAttribWindow
        to set the attributs on each assets with personalized tags by team name.
        """
        if(aOrS == 'assets'):
            self.setAttribDial = SetTypeAttribWindow()                                      #Instantiate the SetTypeAttribWindow class.

            self.typeTagDic = {'ch' : 'characters', 'cl' : 'Cloth' ,'en' : 'environment',
                                'p' : 'props', 'pt' : 'propsTunnel', 'pa' : 'propsArene',
                                'pf': 'propsFemale', 'pm' : 'propsMale'}                    # Define a dictionnary of tags possibilities as keys and their values.

            self.currentSel()                                                               # Get the current selection in a list.

            self.dicValue = ''

            if(self.team == 'IA'):                                                          # Condition to set comboBox items of the QDialog Window by team name.
                self.setAttribDial.items(team = 'IA')
            elif(self.team == 'LDS'):
                self.setAttribDial.items(team = 'LDS')

            for each in self.mySel:                                                         # For loop on the current selection.

                self.tagQuery = cmds.attributeQuery('typeTag', node = each, exists = True)  # Query if the typeTag attribute exists.

                if(not self.tagQuery):                                                      # If the attribute not exists.

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

                if('_' in each):
                    eachSplit = each.split('_')
                    
                    if(any(map(str.isdigit,str(eachSplit[-1])))):

                        each = ''.join(eachSplit[:-1])

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

        for key, value in dict.items():                                                 # For loop over the dictionnary.
            if val == value:                                                            # If the given val is equal to a value of the dictionnary.
                return key                                                              # the function return the key.

    def verifyAssetTreeStructure(self, each):
        """This function allows to verify if the treeStructure of the assets
        existing before exporting them.

        Args:
            each (string): Correponding to each in the current selection.
        """
        
        self.assetDirs =   [self.exportPath + r"/assets/" + self.dicValue + r"/" + each + r"/publishs/modeling",
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
                            self.exportPath + r"/assets/" + self.dicValue + r"/" + each + r"/tasks/uv"
                            ]                                                           # List of the assets directories.

        for dirs in self.assetDirs:                                                     # For loop over the list assetDirs.
            self.verification = os.path.isdir(dirs)                                     # Verification if each dirs in the list exists.

            if(self.verification == False):                                             # If a dir not existing.
                os.makedirs(dirs)                                                       # Create the dir.

    def verifyShotTreeStructure(self, seqNumb, shotNumb):
        """This function allows to verify if the treeStructure of the shots
        existing before exporting animation.

        Args:
            each (string): Correponding to each in the current selection.
        """
        if(self.team == 'IA'):

            self.shotDirs =   [self.exportPath + r"/shots/" + seqNumb + r"/" + shotNumb + r"/publishs/animation",
                                self.exportPath + r"/shots/" + seqNumb + r"/" + shotNumb + r"/publishs/animatic2D",
                                self.exportPath + r"/shots/" + seqNumb + r"/" + shotNumb + r"/publishs/characterFx",
                                self.exportPath + r"/shots/" + seqNumb + r"/" + shotNumb + r"/publishs/compositing",
                                self.exportPath + r"/shots/" + seqNumb + r"/" + shotNumb + r"/publishs/fx",
                                self.exportPath + r"/shots/" + seqNumb + r"/" + shotNumb + r"/publishs/layout3D",
                                self.exportPath + r"/shots/" + seqNumb + r"/" + shotNumb + r"/publishs/lighting",
                                self.exportPath + r"/shots/" + seqNumb + r"/" + shotNumb + r"/publishs/rendering",
                                self.exportPath + r"/shots/" + seqNumb + r"/" + shotNumb + r"/publishs/simulation",
                                self.exportPath + r"/shots/" + seqNumb + r"/" + shotNumb + r"/publishs/shotFinaling",
                                self.exportPath + r"/shots/" + seqNumb + r"/" + shotNumb + r"/refs/images",
                                self.exportPath + r"/shots/" + seqNumb + r"/" + shotNumb + r"/refs/videos",
                                self.exportPath + r"/shots/" + seqNumb + r"/" + shotNumb + r"/tasks/animation",
                                self.exportPath + r"/shots/" + seqNumb + r"/" + shotNumb + r"/tasks/animatic2D",
                                self.exportPath + r"/shots/" + seqNumb + r"/" + shotNumb + r"/tasks/characterFx",
                                self.exportPath + r"/shots/" + seqNumb + r"/" + shotNumb + r"/tasks/compositing",
                                self.exportPath + r"/shots/" + seqNumb + r"/" + shotNumb + r"/tasks/fx",
                                self.exportPath + r"/shots/" + seqNumb + r"/" + shotNumb + r"/tasks/layout3D",
                                self.exportPath + r"/shots/" + seqNumb + r"/" + shotNumb + r"/tasks/lighting",
                                self.exportPath + r"/shots/" + seqNumb + r"/" + shotNumb + r"/tasks/rendering",
                                self.exportPath + r"/shots/" + seqNumb + r"/" + shotNumb + r"/tasks/simulation",
                                self.exportPath + r"/shots/" + seqNumb + r"/" + shotNumb + r"/tasks/shotFinaling"
                                ]                                                       # List of the shots directories for IA.
        elif(self.team == 'LDS'):

            self.shotDirs =   [self.exportPath + r"/shots/" + seqNumb + r"/" + shotNumb + r"/publishs/animation",
                                self.exportPath + r"/shots/" + seqNumb + r"/" + shotNumb + r"/publishs/compositing",
                                self.exportPath + r"/shots/" + seqNumb + r"/" + shotNumb + r"/publishs/crowd",
                                self.exportPath + r"/shots/" + seqNumb + r"/" + shotNumb + r"/publishs/editing",
                                self.exportPath + r"/shots/" + seqNumb + r"/" + shotNumb + r"/publishs/fx",
                                self.exportPath + r"/shots/" + seqNumb + r"/" + shotNumb + r"/publishs/layout",
                                self.exportPath + r"/shots/" + seqNumb + r"/" + shotNumb + r"/publishs/lighting",
                                self.exportPath + r"/shots/" + seqNumb + r"/" + shotNumb + r"/publishs/render",
                                self.exportPath + r"/shots/" + seqNumb + r"/" + shotNumb + r"/publishs/techanim",
                                self.exportPath + r"/shots/" + seqNumb + r"/" + shotNumb + r"/refs/images",
                                self.exportPath + r"/shots/" + seqNumb + r"/" + shotNumb + r"/refs/videos",
                                self.exportPath + r"/shots/" + seqNumb + r"/" + shotNumb + r"/tasks/animation",
                                self.exportPath + r"/shots/" + seqNumb + r"/" + shotNumb + r"/tasks/compositing",
                                self.exportPath + r"/shots/" + seqNumb + r"/" + shotNumb + r"/tasks/crowd",
                                self.exportPath + r"/shots/" + seqNumb + r"/" + shotNumb + r"/tasks/editing",
                                self.exportPath + r"/shots/" + seqNumb + r"/" + shotNumb + r"/tasks/fx",
                                self.exportPath + r"/shots/" + seqNumb + r"/" + shotNumb + r"/tasks/layout",
                                self.exportPath + r"/shots/" + seqNumb + r"/" + shotNumb + r"/tasks/lighting",
                                self.exportPath + r"/shots/" + seqNumb + r"/" + shotNumb + r"/tasks/render",
                                self.exportPath + r"/shots/" + seqNumb + r"/" + shotNumb + r"/tasks/techanim"
                                ]                                                       # List of the shots directories for LDS.

        for dirs in self.shotDirs:                                                      # For loop over the list shotDirs.
            self.verification = os.path.isdir(dirs)                                     # Verification if each dirs in the list exists.

            if(self.verification == False):                                             # If a dir not existing.
                os.makedirs(dirs)                                                       # Create the dir.

    def pathExports(self, tOrP, aOrS, each, endPath, seq, shot):

        if(aOrS == 'assets'):
            dic = r"/" + self.dicValue + r"/"
            self.pathExport = self.exportPath + r"/" + aOrS + dic + each + r"/" + tOrP + r"/" + endPath + "/"                  # The relative path to export assets.
        else:
            self.pathExport = self.exportPath + r"/" + aOrS + r"/" + seq + r"/" + shot + r"/" + tOrP + r"/" + endPath + "/"   # The relative path to export assets.

    def pathExportsPublish(self, tOrP, aOrS, each, endPath, seq, shot):

        self.pathExports(tOrP, aOrS, each, endPath, seq, shot)

        folderList = os.listdir(self.pathExport)
        folderVersion = ''

        if(folderList):

            folderVersion = 'v' + str(int(folderList[-1][1:]) + 1).zfill(3)

        else:
            folderVersion = 'v' + str(1).zfill(3)

        if(aOrS == 'assets'):
            dic = r"/" + self.dicValue + r"/" 
            self.pathExport = self.exportPath + r"/" + aOrS + dic + each + r"/" + tOrP + r"/" + endPath + "/" + folderVersion + "/"                 # The relative path to export assets.
        else:
            self.pathExport = self.exportPath + r"/" + aOrS + r"/" + seq + r"/" + shot + r"/" + tOrP + r"/" + endPath + "/" + folderVersion + "/"   # The relative path to export assets.

    def publishFolder(self):

        self.verification = os.path.isdir(self.pathExport)                          # Verification if each dirs in the list exists.

        if(self.verification == False):                                             # If a dir not existing.
            os.makedirs(self.pathExport)

    def contains_word(self, s, w):

        return (' ' + w + ' ') in (' ' + s + ' ')

    def exportMA(self, checkBox, tOrP, aOrS, endPath, seq, shot, sceneName):
        """This function allows to export .ma files by current selection.

        Args:
            checkBox (bool): The checkBox who is checked.
            tOrP (string): Define if it's a tasks or a publishs export.
            aOrS (string): Define if it's a assets or shots export.
        """

        self.currentSel()                                                               # Get the current selection list.
        
        if(checkBox.isChecked() == True):                                               # If one checkbox is checked.
            
            for each in self.mySel:                                                     # Loop over the selection.
                if(aOrS == 'assets'):
                    self.getDicValue(each)                                              # Get a value from the dictionnary by key.

                cmds.select(each, r = True)                                             # Select each asset in the current sel one by one.

                includeExt = ['.ma']                                                    # The extension I want to include in the search (first parameter of my listdir filter).

                if('_' in each):
                    eachSplit = each.split('_')
                    
                    if(any(map(str.isdigit,str(eachSplit[-1])))):

                        each = ''.join(eachSplit[:-1])

                self.pathExports(tOrP, aOrS, each, endPath, seq, shot)

                sel = [each]                                                            # The name of the asset I want to include in the search (second argument of my listdir filter).
                
                files = []
                folder = os.listdir(self.pathExport)
                if(tOrP == 'tasks'):
                    if(aOrS == 'shots'):
                        files = [f for f in os.listdir(self.pathExport) if any(f.endswith(ext) for ext in includeExt) and any(self.contains_word(s, f.split('_')[3]) for s in sel)] # Comprehensive list to filter files in the dir pathExport by extension and outliner names.
                    else:
                        files = [f for f in os.listdir(self.pathExport) if any(f.endswith(ext) for ext in includeExt) and any(self.contains_word(s, each) for s in sel)] # Comprehensive list to filter files in the dir pathExport by extension and outliner names.
                else:
                    
                    if(folder):
                        
                        if(aOrS == 'shots'):
                            files = [f for f in os.listdir(self.pathExport + folder[-1]) if any(f.endswith(ext) for ext in includeExt) and any(self.contains_word(s, f.split('_')[3]) for s in sel)] # Comprehensive list to filter files in the dir pathExport by extension and outliner names.
                        else:
                            files = [f for f in os.listdir(self.pathExport + folder[-1]) if any(f.endswith(ext) for ext in includeExt) and any(self.contains_word(s, each) for s in sel)] # Comprehensive list to filter files in the dir pathExport by extension and outliner names.
                            
                    else:
                        os.makedirs(self.pathExport + 'v001')
                        if(aOrS == 'shots'):
                            files = [f for f in os.listdir(self.pathExport + 'v001') if any(f.endswith(ext) for ext in includeExt) and any(self.contains_word(s, f.split('_')[3]) for s in sel)] # Comprehensive list to filter files in the dir pathExport by extension and outliner names.
                        else:
                            files = [f for f in os.listdir(self.pathExport + 'v001') if any(f.endswith(ext) for ext in includeExt) and any(self.contains_word(s, each) for s in sel)] # Comprehensive list to filter files in the dir pathExport by extension and outliner names.
                    
                self.fileName = ''

                if(files):                                                              # If the search found one or many files.
                    lastFile = files[-1]                                                # keep the last file version.

                    delExt = lastFile.split('.')                                        # split the extension.

                    keepVersion = delExt[0].split('_v')                                 # Get the first result of the split and split again to keep the version of the file.

                    newVersion = int(keepVersion[1]) + 1                                # Create a new version using the last version number and add it 1.

                    self.fileName = sceneName + each + "_v" + str(newVersion).zfill(3)              # Define the file name with the name of the asset and the version.

                    cmds.file(self.pathExport + self.fileName, type = 'mayaAscii', pr = True, es = True, f = True)   # Exports the file.

                else:                                                                   # If the search not found one or many files.
                    newVersion = str(1).zfill(3)                                        # Creates a new version equal to '0000'.

                    self.fileName = sceneName + each + "_v" + newVersion                            # Define the filename with the name of the asset and the version.

                    cmds.file(self.pathExport + self.fileName, type = 'mayaAscii', pr = True, es = True, f = True)   # Exports the file.
                
                if(tOrP == 'publishs'):
                    if(os.path.isdir(self.pathExport + "v" + str(newVersion).zfill(3)) == False):
                        newPath = self.pathExport + 'v' + str(newVersion).zfill(3)
                        os.makedirs(newPath)
                        shutil.move(self.pathExport + self.fileName + '.ma', newPath + '/' + self.fileName + '.ma')
                        
                    else:
                        shutil.move(self.pathExport + self.fileName + '.ma', self.pathExport + 'v' + str(newVersion).zfill(3) + '/' + self.fileName + '.ma')

        cmds.select(self.mySel)

    def exportOBJ(self, checkBox, checkBoxAbc, tOrP, aOrS, endPath, seq, shot, sceneName):
        """This function allows to export .obj files by current selection.

        Args:
            checkBox (bool): The checkBow who is checked.
            tOrP (string): Define if it's a tasks or a publishs export.
            aOrS (string): Define if it's a assets or shots export.
        """

        self.currentSel()                                                               # Get the current selection list.
        
        if(checkBox.isChecked() == True):                                               # If one checkbox is checked.
            
            for each in self.mySel:                                                     # Loop over the selection.
                if(aOrS == 'assets'):
                    self.getDicValue(each)                                                  # Get a value from the dictionnary by key.

                cmds.select(each, r = True)                                             # Select each asset in the current sel one by one.

                includeExt = ['.obj']                                                    # The extension I want to include in the search (first parameter of my listdir filter).

                if('_' in each):
                    eachSplit = each.split('_')
                    
                    if(any(map(str.isdigit,str(eachSplit[-1])))):

                        each = ''.join(eachSplit[:-1])

                self.pathExports(tOrP, aOrS, each, endPath, seq, shot)

                sel = [each]                                                            # The name of the asset I want to include in the search (second argument of my listdir filter).
                
                files = []

                if(tOrP == 'tasks'):
                    files = [f for f in os.listdir(self.pathExport) if any(f.endswith(ext) for ext in includeExt) and any(self.contains_word(s, each) for s in sel)] # Comprehensive list to filter files in the dir pathExport by extension and outliner names.
                
                    self.fileName = ''

                    if(files):                                                              # If the search found one or many files.
                        lastFile = files[-1]                                                # keep the last file version.

                        delExt = lastFile.split('.')                                        # split the extension.

                        keepVersion = delExt[0].split('_v')                                 # Get the first result of the split and split again to keep the version of the file.

                        newVersion = int(keepVersion[1]) + 1                                # Create a new version using the last version number and add it 1.
                        
                        self.fileName = sceneName + each + "_v" + str(newVersion).zfill(3)              # Define the file name with the name of the asset and the version.

                        cmds.file(self.pathExport + self.fileName, options = "groups=1;ptgroups=0;materials=0;smoothing=1;normals=1", type = 'OBJexport', pr = True, es = True, f = True)   # Exports the file.

                    else:                                                                   # If the search not found one or many files.
                        newVersion = str(1).zfill(3)                                        # Creates a new version equal to '0000'.

                        self.fileName = sceneName + each + "_v" + newVersion                            # Define the filename with the name of the asset and the version.

                        cmds.file(self.pathExport + self.fileName, options = "groups=1;ptgroups=0;materials=0;smoothing=1;normals=1", type = 'OBJexport', pr = True, es = True, f = True)   # Exports the file.

                else:
                    folder = os.listdir(self.pathExport)
                    files = []
                    if(folder):                                                              # If the search found one or many files.
                        lastFile = folder[-1]                                                # keep the last file version.

                        delExt = lastFile.split('v')                                        # split the extension.
                        includeExt = ['.obj']
                        includeExtAbc = ['.abc']
                        files = [f for f in os.listdir(self.pathExport + lastFile) if any(f.endswith(ext) for ext in includeExt)] # Comprehensive list to filter files in the dir pathExport by extension and outliner names.
                        filesAbc = [f for f in os.listdir(self.pathExport + lastFile) if any(f.endswith(ext) for ext in includeExtAbc)] # Comprehensive list to filter files in the dir pathExport by extension and outliner names.
                        if(files):
                            newVersion = int(delExt[1]) + 1                                # Create a new version using the last version number and add it 1.
                        
                        elif(filesAbc and checkBoxAbc.isChecked() == True):
                            
                            newVersion = str(int(delExt[1]) + 1)                                # Create a new version using the last version number and add it 1.
                        
                        else:
                            newVersion = int(delExt[1])                                    # Create a new version using the last version number and add it 1.

                        self.fileName = sceneName + each + "_v" + str(newVersion).zfill(3)              # Define the file name with the name of the asset and the version.
                        cmds.file(self.pathExport + self.fileName, options = "groups=1;ptgroups=0;materials=0;smoothing=1;normals=1", type = 'OBJexport', pr = True, es = True, f = True)   # Exports the file.
                    else:                                                                   # If the search not found one or many files.
                        newVersion = str(1).zfill(3)                                        # Creates a new version equal to '0000'.

                        self.fileName = sceneName + each + "_v" + newVersion
                        cmds.file(self.pathExport + self.fileName, options = "groups=1;ptgroups=0;materials=0;smoothing=1;normals=1", type = 'OBJexport', pr = True, es = True, f = True)   # Exports the file.
                    newPath = ''
                    if(os.path.isdir(self.pathExport + "v" + str(newVersion).zfill(3)) == False):
                        newPath = self.pathExport + 'v' + str(newVersion).zfill(3)
                        os.makedirs(newPath)
                        shutil.move(self.pathExport + self.fileName + '.obj', newPath + '/' + self.fileName + '.obj')

                    else:
                        shutil.move(self.pathExport + self.fileName + '.obj', self.pathExport + 'v' + str(newVersion).zfill(3) + '/' + self.fileName + '.obj')


        cmds.select(self.mySel)

    def exportABC(self, checkBox, tOrP, aOrS, startFrame, endFrame, subA, subB, attrExport, endPath, seq, shot, sceneName):
        """This function allows to export .abc files by current selection.

        Args:
            checkBox (bool): The checkBow who is checked.
            tOrP (string): Define if it's a tasks or a publishs export.
            aOrS (string): Define if it's a assets or shots export.
        """

        self.currentSel()                                                               # Get the current selection list.
        
        if(checkBox.isChecked() == True):                                               # If one checkbox is checked.
            
            for each in self.mySel:                                                     # Loop over the selection.
                if(aOrS == 'assets'):
                    self.getDicValue(each)                                                  # Get a value from the dictionnary by key.

                cmds.select(each, r = True)                                             # Select each asset in the current sel one by one.

                includeExt = ['.abc']                                                   # The extension I want to include in the search (first parameter of my listdir filter).

                root = each

                if('_' in each):
                    eachSplit = each.split('_')
                    
                    if(any(map(str.isdigit,str(eachSplit[-1])))):

                        each = ''.join(eachSplit[:-1])


                self.pathExports(tOrP, aOrS, each, endPath, seq, shot)


                sel = [each]                                                            # The name of the asset I want to include in the search (second argument of my listdir filter).
                
                files = []
                if(tOrP == 'tasks'):
                    if(aOrS == 'shots'):
                        files = [f for f in os.listdir(self.pathExport) if any(f.endswith(ext) for ext in includeExt) and any(self.contains_word(s, f.split('_')[3]) for s in sel)] # Comprehensive list to filter files in the dir pathExport by extension and outliner names.
                    else:
                        files = [f for f in os.listdir(self.pathExport) if any(f.endswith(ext) for ext in includeExt) and any(self.contains_word(s, each) for s in sel)] # Comprehensive list to filter files in the dir pathExport by extension and outliner names.
                
                    self.fileName = ''

                    if(files):                                                              # If the search found one or many files.
                        lastFile = files[-1]                                                # keep the last file version.

                        delExt = lastFile.split('.')                                        # split the extension.

                        keepVersion = delExt[0].split('_v')                                 # Get the first result of the split and split again to keep the version of the file.

                        newVersion = int(keepVersion[1]) + 1                                # Create a new version using the last version number and add it 1.

                        self.fileName = sceneName + each + "_v" + str(newVersion).zfill(3)              # Define the file name with the name of the asset and the version.

                    else:                                                                   # If the search not found one or many files.
                        newVersion = str(1).zfill(3)                                        # Creates a new version equal to '0000'.

                        self.fileName = sceneName + each + "_v" + newVersion
                    self.abcCommandBuilder(root, startFrame, endFrame, subA, subB, attrExport)
                else:
                    folder = os.listdir(self.pathExport)

                    files = []

                    newVersion = ''
                    if(folder):                                                              # If the search found one or many files.
                        lastFile = folder[-1]                                                # keep the last file version.

                        delExt = lastFile.split('v')                                        # split the extension.
                        includeExt = ['.abc']

                        sel = [each]
                        if(aOrS == 'shots'):
                            files = [f for f in os.listdir(self.pathExport + lastFile) if any(f.endswith(ext) for ext in includeExt) and any(self.contains_word(s, f.split('_')[3]) for s in sel)] # Comprehensive list to filter files in the dir pathExport by extension and outliner names.
                        else:
                            files = [f for f in os.listdir(self.pathExport + lastFile) if any(f.endswith(ext) for ext in includeExt) and any(self.contains_word(s, each) for s in sel)] # Comprehensive list to filter files in the dir pathExport by extension and outliner names.

                        if(files):

                            newVersion = str(int(delExt[1]) + 1)                                # Create a new version using the last version number and add it 1.

                        else:
                            newVersion = str(int(delExt[1]))                                    # Create a new version using the last version number and add it 1.
                        self.fileName = sceneName + each + "_v" + newVersion.zfill(3)              # Define the file name with the name of the asset and the version.

                    else:                                                                   # If the search not found one or many files.
                        newVersion = str(1).zfill(3)                                        # Creates a new version equal to '0000'.

                        self.fileName = sceneName + each + "_v" + newVersion

                    self.abcCommandBuilder(root, startFrame, endFrame, subA, subB, attrExport)
                    newPath = ''
                    if(os.path.isdir(self.pathExport + "v" + newVersion.zfill(3)) == False):
                        newPath = self.pathExport + 'v' + newVersion.zfill(3)

                        os.makedirs(newPath)
                        shutil.move(self.pathExport + self.fileName + '.abc', newPath + '/' + self.fileName + '.abc')

                    else:
                        newPath = self.pathExport + 'v' + newVersion.zfill(3)
                        shutil.move(self.pathExport + self.fileName + '.abc', newPath + '/' + self.fileName + '.abc')

        cmds.select(self.mySel)

    def abcCommandBuilder(self, each, startFrame, endFrame, subA, subB, attrExport):

        frameRange = "-frameRange " + str(startFrame) + " " + str(endFrame)

        frameRSample = " -frameRelativeSample " + subA + " -frameRelativeSample 0 -frameRelativeSample " + subB
        
        attrList = []
        for attr in attrExport:

            attributes = " -attr " + attr
            attrList.append(attributes)
        
        attrJoin = ''.join(attrList)

        checkedParam = " -stripNamespaces -uvWrite -worldSpace -writeUVSets -dataFormat ogawa "

        root = "-root " + each

        file = " -file " + self.pathExport + self.fileName + ".abc"

        abcCommand = frameRange + frameRSample + attrJoin + checkedParam + root + file

        cmds.AbcExport( j = abcCommand)   # Exports the file.