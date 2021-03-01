
from Qt import QtWidgets, QtCore, QtGui

from pipelineToolUI.mayaAttributes import *
from pipelineToolUI.mayaExports import *
from pipelineToolUI.setTypeAttribWindow import *

import os

_IN_MAYA_ = False

try:
    from maya import cmds
    _IN_MAYA_ = True
except:
    pass


# Handle high resolution displays:
if hasattr(QtCore.Qt, 'AA_EnableHighDpiScaling'):
    QtWidgets.QApplication.setAttribute(QtCore.Qt.AA_EnableHighDpiScaling, True)
if hasattr(QtCore.Qt, 'AA_UseHighDpiPixmaps'):
    QtWidgets.QApplication.setAttribute(QtCore.Qt.AA_UseHighDpiPixmaps, True)

class PipelineUI(QtWidgets.QMainWindow):

    def __init__(self, parent = None, **kwargs):

        # Init this class with the parent class init.
        super(PipelineUI, self).__init__(parent = parent)

        self.attribCreateButton = QtWidgets.QPushButton('Set')
        self.comboBoxAttribTS = QtWidgets.QComboBox()
        self.attribNameLineEdit = QtWidgets.QLineEdit()
        self.attribLineEdit = QtWidgets.QLineEdit()
        

        self.attribDeleteButton = QtWidgets.QPushButton('Delete')

        self.taskPushButton = QtWidgets.QPushButton('Tasks')
        self.publishPushButton = QtWidgets.QPushButton('Publishs')

        self.initUI()

        self.localCheckBox.stateChanged.connect(lambda:self.localPathInteract())
        self.localCheckBox.stateChanged.connect(lambda:self.searchNDropInteract())
        self.pathLineEdit.returnPressed.connect(self.localPathInteract)
        self.pathLineEdit.returnPressed.connect(self.searchNDropInteract)

        self.checkBoxLock.stateChanged.connect(lambda:self.teamLockInteract())

        self.comboBoxTeam.activated[str].connect(self.searchNDropInteract)

        self.searchTreeView.doubleClicked.connect(self.openFiles)

        self.attribCreateButton.clicked.connect(self.mayaAttributeCnR)

        self.attribDeleteButton.clicked.connect(self.mayaAttributeDel)

        self.taskPushButton.clicked.connect(self.exportTasks)
        self.publishPushButton.clicked.connect(self.exportPublishs)

        
        
    def initUI(self):
        """Create the widget interface.
        """

        self.mayaAttrib = MayaAttributes()

        # Set the window title.
        self.setWindowTitle('Pipeline Tool')

        # Set the window size.
        screen = QtWidgets.QDesktopWidget().screenGeometry(-1)

        self.width = screen.width()
        self.height = screen.height()
        if(self.width > 1920):
            self.setMinimumSize(1050, 700)
            self.setMaximumSize(1500, 700)
        else:
            self.setMinimumSize(1050/1.7, 700/1.6)
            self.setMaximumSize(1050, 700)
        self.resize(self.width/4, self.height/4)

        ### Compute the different Widgets of the UI. ###
        self.layoutBase()

        self.QVLineShape()

        self.localPathWidget()

        self.teamLockWidget()

        self.searchAndDropWidget()
        
        self.attribUIWidget()

        self.exportUIWidget()

        self.attribExport()

        self.exportsInteract()

        self.exportButtons()

        ### Add widgets to child widgets. ###

        self.childLayout1.addWidget(self.teamWidget)
        self.childLayout1.addWidget(self.searchNDropWidget)

        self.childWidget1.setLayout(self.childLayout1)
        
        self.childLayout2.addWidget(self.localWidget)
        self.childLayout2.addWidget(self.attribVWidget)
        self.childLayout2.addWidget(self.exportSceneNameVWidget)
        self.childLayout2.addWidget(self.exportMainWidget)
        self.childLayout2.addWidget(self.attribExportWidget)
        self.childLayout2.addWidget(self.exportButtonWidget)

        self.childWidget2.setLayout(self.childLayout2)

        # Add child widgets to the main layout.

        self.mainLayout.addWidget(self.childWidget1)
        self.mainLayout.addWidget(self.childWidget2)

        # Set the main layout to the main widget.
        self.mainWidget.setLayout(self.mainLayout)
        self.setCentralWidget(self.mainWidget)

    def layoutBase(self):
        """Create the main and the two children base layouts.
        """

        # Create the main Widget.
        self.mainWidget = QtWidgets.QWidget()

        # Create the main Layout.
        self.mainLayout = QtWidgets.QHBoxLayout()
        self.mainLayout.setContentsMargins(0, 0, 0, 0)

        # Create the child widgets.
        self.childWidget1 = QtWidgets.QWidget()
        self.childWidget2 = QtWidgets.QWidget()

        # Create the child Layouts.
        self.childLayout1 = QtWidgets.QVBoxLayout()
        self.childLayout1.setContentsMargins(0, 0, 0, 0)
        self.childLayout2 = QtWidgets.QVBoxLayout()
        self.childLayout2.setContentsMargins(0, 0, 0, 0)

        # Set the child layouts to the child widgets.
        self.childWidget1.setLayout(self.childLayout1)
        self.childWidget2.setLayout(self.childLayout2)

    def localPathWidget(self):
        """Creating the local path Widget to have the possibility to work on a local tree structure.
        """

        self.localWidget = QtWidgets.QWidget()
        self.localLayout = QtWidgets.QHBoxLayout(self.localWidget)
        self.localLayout.setContentsMargins(0, 20, 10, 0)
        self.localLayout.setSpacing(5)

        self.pathLabel = QtWidgets.QLabel('Path :')

        # Create local CheckBox.
        self.localCheckBox = QtWidgets.QCheckBox('Local')
        self.localCheckBox.setChecked(True)

        # Create line edit for path.
        self.pathLineEdit = QtWidgets.QLineEdit("C:/")
        self.pathLineEdit.setMaximumSize(300, 32)
        self.pathLineEdit.setMaximumSize(150, 32)

        self.localPathInteract()

        # Add widgets to the layout.
        self.localLayout.addWidget(self.localCheckBox)
        self.localLayout.addWidget(self.pathLabel)
        self.localLayout.addWidget(self.pathLineEdit)

        # Set the layout.
        self.localWidget.setLayout(self.localLayout)

    def localPathInteract(self):
        """Here is the condition to set the local path if we check the checkbox 'local'.
        """

        if(self.localCheckBox.isChecked() == True):
            self.localPath = self.pathLineEdit.text()
            
        else:
            self.localPath = None
            

    def teamLockWidget(self):
        """Creating the team lock Widget. We can change the team name and lock it.
        If the team name changes, the server path is changed to point on the team tree structure.
        """

        # Create the team widget.
        self.teamWidget = QtWidgets.QWidget()

        # Create the team layout.
        self.teamLayout = QtWidgets.QHBoxLayout(self.childWidget1)
        self.teamLayout.setContentsMargins(10, 20, 0, 3)
        
        self.teamLayout.setSpacing(20)
        
        # Create and set the team QLabel.
        self.teamLabel = QtWidgets.QLabel('Team :')
        
        # Create and set the comboBox Team.
        self.comboBoxTeam = QtWidgets.QComboBox()
        self.comboBoxTeam.addItem('IA')
        self.comboBoxTeam.addItem('LDS')
        self.comboBoxTeam.addItem('OPS')
        self.comboBoxTeam.setCurrentIndex(0)

        # Create and set the checkBox Lock.
        self.checkBoxLock = QtWidgets.QCheckBox('Lock')
        self.checkBoxLock.setChecked(True)
        

        self.teamLockInteract()

        # Add the widgets to the teamLayout.
        self.teamLayout.addWidget(self.teamLabel, 0, QtCore.Qt.AlignRight)
        self.teamLayout.addWidget(self.comboBoxTeam)
        self.teamLayout.addWidget(self.checkBoxLock)
        #self.teamLayout.addWidget(self.vLine)

        # Add the layout to the widget.
        self.teamWidget.setLayout(self.teamLayout)

    def teamLockInteract(self):
        """Here is the condition to lock the possibility to change the team name.
        """

        self.comboBoxTeam.setEnabled(False)
        if(self.checkBoxLock.isChecked() == True):
            self.comboBoxTeam.setEnabled(False)
        else:
            self.comboBoxTeam.setEnabled(True)

    def searchAndDropWidget(self):
        """Creating the search and drop widget.
        We can use it to search folders and files in the path of the tree structure and drag/drop files in the software.
        """

        self.QHLineShape()
        self.hLine.setFixedWidth(474)
        self.hLine.setMinimumHeight(7)
        # Create the searchNDrop widget.
        self.searchNDropWidget = QtWidgets.QWidget()

        # Create the searchNDrop Layout.
        self.searchNDropLayout = QtWidgets.QVBoxLayout(self.childWidget1)
        self.searchNDropLayout.setContentsMargins(10, 0, 0, 0)
        # Create and set the search label.
        self.searchLabel = QtWidgets.QLabel('Search :')
        self.searchLabel.setFont(QtGui.QFont('Times', 10))
        # Create the search line editor.
        self.searchLineEdit = QtWidgets.QLineEdit()
        self.searchLineEdit.setEnabled(False)
        # Create the QtreeView searcher.
        self.searchTreeView = QtWidgets.QTreeView()

        self.searchNDropInteract()

        # Add the widgets to the searchNDropLayout.
        self.searchNDropLayout.addWidget(self.hLine)
        self.searchNDropLayout.addWidget(self.searchLabel, 0, QtCore.Qt.AlignHCenter)
        self.searchNDropLayout.addWidget(self.searchLineEdit)
        self.searchNDropLayout.addWidget(self.searchTreeView)

        self.text = self.searchLineEdit.text()

        # Add the layout to the widget.
        self.searchNDropWidget.setLayout(self.searchNDropLayout)

    def comboTeam(self):

        return self.comboBoxTeam.currentIndex()

    def searchNDropInteract(self):
        """Here is the search and drop interaction code.
        We use condition to set the path and the QTreeview point on this path.
        After we define the model of the QTreeview and we use Filters and Sort filter proxy model
        to search in the tree structure.
        """
        # Get the current index of the team.
        self.teamIdx = self.comboBoxTeam.currentIndex()

        # Condition to determine the server or local path.
        if(self.localCheckBox.isChecked() == True):
            self.path = self.localPath
        else:          
            if(self.teamIdx == 0):
                self.path = "P:\shows\IA"
            elif(self.teamIdx == 1):
                self.path = "P:\shows\LDS"
            elif(self.teamIdx == 2):
                self.path = "P:\shows\OPS"

        # Define the file system model.
        self.model = QtWidgets.QFileSystemModel(self.searchTreeView)

        # Set the root path.
        root = self.model.setRootPath(self.path)

        self.searchTreeView.setModel(self.model)

        self.searchTreeView.setRootIndex(root)
        
        self.searchTreeView.header().setSectionResizeMode(0,QtWidgets.QHeaderView.ResizeToContents)
        self.searchTreeView.header().setStretchLastSection(False)

        self.searchTreeView.setColumnHidden(1, True)
        self.searchTreeView.setColumnHidden(2, True)
        self.searchTreeView.setColumnHidden(3, True)
        self.searchTreeView.setAcceptDrops(True)
        self.searchTreeView.setDragDropOverwriteMode(True)
        self.searchTreeView.setDragDropMode(QtWidgets.QAbstractItemView.DragDrop)

    def openFiles(self):
        """This function allows to open a file by Double Clicking in the Treeview.
        """
        index = self.searchTreeView.currentIndex()

        filePath = self.model.filePath(index)

        os.startfile(filePath)

    def attribUIWidget(self):
        """Creating the attribute Widget.
        This widget can add or delete different type of attributes on transforms and shapes in maya.
        """

        self.QHLineShape()
        self.hLine.setFixedWidth(540)
        self.hLine.setMinimumHeight(10)

        # Create the attrib widget.
        self.attribWidget = QtWidgets.QWidget()
        self.attribVWidget = QtWidgets.QWidget()
        self.attribChoiceWidget = QtWidgets.QWidget()
        self.attribTypeWidget = QtWidgets.QWidget()
        # Create the attrib layout.
        self.attribTypeLayout = QtWidgets.QHBoxLayout(self.childWidget2)
        self.attribTypeLayout.setContentsMargins(50, 0, 5, 0)
        #self.attribTypeLayout.addStretch(1)

        self.attribLayout = QtWidgets.QHBoxLayout(self.childWidget2)
        self.attribLayout.setContentsMargins(0, 0, 5, 5)
        #self.attribLayout.addStretch(1)

        self.attribChoiceLayout = QtWidgets.QHBoxLayout(self.childWidget2)
        self.attribChoiceLayout.setContentsMargins(0, 0, 5, 5)
        #self.attribChoiceLayout.addStretch(2)

        self.attribVLayout = QtWidgets.QVBoxLayout(self.childWidget2)
        self.attribVLayout.setContentsMargins(0, 1, 5, 5)
        #self.attribVLayout.addStretch(1)

        # Create and set attribute labels.
        self.attribLabel = QtWidgets.QLabel('Attributes :')
        self.attribTypeLabel = QtWidgets.QLabel('Type :')
        self.attribOnLabel = QtWidgets.QLabel('On :')
        self.attribLabel.setFont(QtGui.QFont('Times', 10))
        self.attribNameLabel = QtWidgets.QLabel('Name :')
        self.setAttribLabel = QtWidgets.QLabel('Value :')
        self.setAttribLabel.setFixedWidth(50)

        #self.attribLineEdit.setFixedWidth(243)

        # Create the combo box to choose transform or shape attribute.

        self.comboBoxAttribTS.addItem('Shape')
        self.comboBoxAttribTS.addItem('Transform')

        # Create the combo box to choose the type of the attribute.
        self.comboBoxAttribType = QtWidgets.QComboBox()

        self.comboBoxAttribType.addItem('String')
        self.comboBoxAttribType.addItem('Integer')
        self.comboBoxAttribType.addItem('Float')

        # Add widgets to layout and set layout to widgets.
        
        self.attribTypeLayout.addWidget(self.attribLabel)
        self.attribTypeLayout.addWidget(self.attribTypeLabel, 0, QtCore.Qt.AlignRight)
        self.attribTypeLayout.addWidget(self.attribOnLabel, 0, QtCore.Qt.AlignHCenter)  

        self.attribTypeWidget.setLayout(self.attribTypeLayout)

        # Add the widgets to the attrib choice layout.
        self.attribChoiceLayout.addWidget(self.attribNameLabel)
        self.attribChoiceLayout.addWidget(self.attribNameLineEdit)
        self.attribChoiceLayout.addWidget(self.comboBoxAttribType)
        self.attribChoiceLayout.addWidget(self.comboBoxAttribTS)

        # Add the layout choice to the widget choice.
        self.attribChoiceWidget.setLayout(self.attribChoiceLayout)

        # Add the widgets to the attrib layout.
        self.attribLayout.addWidget(self.setAttribLabel)
        self.attribLayout.addWidget(self.attribLineEdit)
        self.attribLayout.addWidget(self.attribCreateButton)
        self.attribLayout.addWidget(self.attribDeleteButton)
        # Add the layout to the attrib widget.
        self.attribWidget.setLayout(self.attribLayout)

        self.attribVLayout.addWidget(self.hLine)
        self.attribVLayout.addWidget(self.attribTypeWidget)
        self.attribVLayout.addWidget(self.attribChoiceWidget)
        self.attribVLayout.addWidget(self.attribWidget)

        self.attribVWidget.setLayout(self.attribVLayout)
    
    def exportUIWidget(self):
        """Creating the export bases widget
        and call the other functions to complete the widget.
        """

        # Create the main export widget.
        self.exportMainWidget = QtWidgets.QWidget()

        self.exportSceneName()
        self.exportChild1()
        self.exportChild2()
        self.QVLineShape()
        self.vLine.setMinimumHeight(1)
        self.vLine.setFixedHeight(250)

        # Create the main export layout.
        self.exportMainLayout = QtWidgets.QHBoxLayout(self.exportMainWidget)
        self.exportMainLayout.setContentsMargins(0, 0, 5, 0)

        # Add child widgets to the main export layout.
        self.exportMainLayout.addWidget(self.exportChildWidget1)
        self.exportMainLayout.addWidget(self.vLine)
        self.exportMainLayout.addWidget(self.exportChildWidget2)

        # Set main layout to the main export widget.
        self.exportMainWidget.setLayout(self.exportMainLayout)

    def exportSceneName(self):     
        """ Here is the export scene name function.
        This create all the scene name part of the export widget.
        """

        self.QHLineShape()
        self.hLine.setMinimumHeight(0)
        self.hLine.setFixedWidth(540)

        # Create export scene name widget.
        self.exportSceneNameWidget = QtWidgets.QWidget()
        self.exportSceneNameVWidget = QtWidgets.QWidget()

        # Create the export scene name layout.
        self.exportSceneNameLayout = QtWidgets.QHBoxLayout(self.exportSceneNameWidget)
        self.exportSceneNameLayout.setContentsMargins(0, 0, 5, 0)
        self.exportSceneNameVLayout = QtWidgets.QVBoxLayout(self.exportSceneNameVWidget)
        self.exportSceneNameVLayout.setContentsMargins(0, 10, 5, 0)

        # Create labels.
        self.exportLabel = QtWidgets.QLabel('Exports :')
        self.exportLabel.setFont(QtGui.QFont('Times', 10))
        self.exportSceneNameLabel = QtWidgets.QLabel('Scene Name :')

        # Create line edit scene name.
        self.sceneNameLineEdit = QtWidgets.QLineEdit()
        self.sceneNameLineEdit.returnPressed.connect(self.exportsInteract)
        # Add widgets to the scene name layout.
        self.exportSceneNameLayout.addWidget(self.exportSceneNameLabel, 0, QtCore.Qt.AlignHCenter)
        self.exportSceneNameLayout.addWidget(self.sceneNameLineEdit)

        # Set the scene name layout to the scene name widget.
        self.exportSceneNameWidget.setLayout(self.exportSceneNameLayout)
 
        # Add widgets to the sceneNameVLayout.
        self.exportSceneNameVLayout.addWidget(self.hLine)
        self.exportSceneNameVLayout.addWidget(self.exportLabel, 0, QtCore.Qt.AlignHCenter)
        self.exportSceneNameVLayout.addWidget(self.exportSceneNameWidget)
        self.exportSceneNameVLayout.addStretch()

        # Set the scene name Vlayout to the scene name Vwidget.
        self.exportSceneNameVWidget.setLayout(self.exportSceneNameVLayout)


    def exportChild1(self):
        """This function creates the file type choice that we want to export
        with the export widget.
        """

        # Create the child1 exports widget.
        self.exportChildWidget1 = QtWidgets.QWidget()

        # Create the child1 export layout.
        self.exportChildLayout1 = QtWidgets.QVBoxLayout(self.exportChildWidget1)
        self.exportChildLayout1.setContentsMargins(50, 5, 0, 0)

        # Create checkBoxes.
        self.checkExportMA = QtWidgets.QCheckBox('.ma')
        self.checkExportMA.setChecked(True)
        self.checkExportOBJ = QtWidgets.QCheckBox('.obj')
        self.checkExportOBJ.setChecked(True)
        self.checkExportABC = QtWidgets.QCheckBox('.abc')
        self.checkExportABC.setChecked(True)

        # Add Widgets to the child layouts.
        self.exportChildLayout1.addWidget(self.checkExportMA, 0, QtCore.Qt.AlignHCenter)
        self.exportChildLayout1.addWidget(self.checkExportOBJ, 0, QtCore.Qt.AlignHCenter)
        self.exportChildLayout1.addWidget(self.checkExportABC, 0, QtCore.Qt.AlignHCenter)
        self.exportChildLayout1.setSpacing(30)

        # Set child layout to child widget.
        self.exportChildWidget1.setLayout(self.exportChildLayout1)

    def exportChild2(self):
        """This function creates the alembic options part of the export widget.
        """

        self.alembicOptions()

        # Create the child2 export widget.
        self.exportChildWidget2 = QtWidgets.QWidget()
        self.exportLabelHWidget1 = QtWidgets.QWidget()
        self.subSWidget = QtWidgets.QWidget()
        # Create the child exports layout.
        self.exportChildLayout2 = QtWidgets.QVBoxLayout(self.exportChildWidget2)
        self.exportChildLayout2.setContentsMargins(0, 0, 5, 0)

        self.exportLabelHLayout1 = QtWidgets.QHBoxLayout(self.exportLabelHWidget1)
        self.exportLabelHLayout1.setContentsMargins(0, 0, 0, 0)

        self.subSLayout = QtWidgets.QHBoxLayout(self.subSWidget)
        self.subSLayout.setContentsMargins(0, 0, 0, 0)
        # Add widgets to layout.
        self.exportLabelHLayout1.addWidget(self.startLabel)
        self.exportLabelHLayout1.addWidget(self.startLineEdit)
        self.exportLabelHLayout1.addWidget(self.endLabel)
        self.exportLabelHLayout1.addWidget(self.endLineEdit)

        #self.subSLayout.addWidget(self.subsampleLabel)
        self.subSLayout.addWidget(self.startSubSLineEdit)
        self.subSLayout.addWidget(self.endSubSLineEdit)

        # Add the widgets to the layout.
        self.exportChildLayout2.addWidget(self.alembicOptionsLabel, 0, QtCore.Qt.AlignHCenter)
        self.exportChildLayout2.addWidget(self.exportLabelHWidget1, 0, QtCore.Qt.AlignHCenter)
        self.exportChildLayout2.addWidget(self.subsampleLabel, 0, QtCore.Qt.AlignHCenter)
        self.exportChildLayout2.addWidget(self.subSWidget, 0, QtCore.Qt.AlignHCenter)
        self.exportChildLayout2.setSpacing(0)

        # Set child layout to child widgets.
        self.exportLabelHWidget1.setLayout(self.exportLabelHLayout1)
        self.subSWidget.setLayout(self.subSLayout)
        self.exportChildWidget2.setLayout(self.exportChildLayout2)

    def alembicOptions(self):
        """This function set the alembic options of the export widget.
        """

        # Creates the Labels.
        self.alembicOptionsLabel = QtWidgets.QLabel('Alembic Options :')
        self.alembicOptionsLabel.setFont(QtGui.QFont('Times', 8))

        self.startLabel = QtWidgets.QLabel('Start :')
        self.endLabel = QtWidgets.QLabel('End :')

        self.subsampleLabel = QtWidgets.QLabel('Subsamples :')

        # Create the line edits.
        self.startLineEdit = QtWidgets.QLineEdit()
        self.startLineEdit.setText('1')
        self.endLineEdit = QtWidgets.QLineEdit()
        self.endLineEdit.setText('1')
        self.startSubSLineEdit = QtWidgets.QLineEdit()
        self.startSubSLineEdit.setText('-0.0')
        self.endSubSLineEdit = QtWidgets.QLineEdit()
        self.endSubSLineEdit.setText('0.0')

    def attribExport(self):
        """This function creates the export attributes widget.
        With this widget we can choose what attributes we want to export in the alembic.
        """

        # Create the widget.
        self.attribExportWidget = QtWidgets.QWidget()

        # Create the layout.
        self.attribExportLayout = QtWidgets.QHBoxLayout(self.attribExportWidget)

        # Create the label.
        self.attribExportLabel = QtWidgets.QLabel('Export Attributes :')

        # Create the comboBox.
        self.attribExportLineEdit = QtWidgets.QLineEdit()
        self.attribExportLineEdit.setText('typeTag,GuerillaTags,variant,id')
        
        # Add widgets to the layout.
        self.attribExportLayout.addWidget(self.attribExportLabel)
        self.attribExportLayout.addWidget(self.attribExportLineEdit)

        # Set the layout to the widget.
        self.attribExportWidget.setLayout(self.attribExportLayout)

    def exportButtons(self):
        """This function creates the export buttons widget.
        We have two buttons, one for 'Tasks exports' and another for 'publishs exports'.
        """

        # Create the export buttons widget.
        self.exportButtonWidget = QtWidgets.QWidget()

        # Create the export buttons layout.
        self.exportButtonLayout = QtWidgets.QHBoxLayout(self.exportButtonWidget)
        self.exportButtonLayout.setSpacing(30)

        # Set the QPushButton widgets size.
        self.taskPushButton.setFixedSize(self.width/18, self.height/20)
        self.publishPushButton.setFixedSize(self.width/18, self.height/20)

        # Add the buttons to the layout.
        self.exportButtonLayout.addWidget(self.taskPushButton)
        self.exportButtonLayout.addWidget(self.publishPushButton)

        # Add the layout to the widget.
        self.exportButtonWidget.setLayout(self.exportButtonLayout)

    def QVLineShape(self):
        """This function creates a Vertical line shape that we can re use.
        """

        self.vLine = QtWidgets.QFrame()
        self.vLine.setFixedWidth(50)
        self.vLine.setMinimumHeight(40)
        self.vLine.setLineWidth(2)
        self.vLine.setFrameShape(QtWidgets.QFrame.VLine)
        self.vLine.setFrameShadow(QtWidgets.QFrame.Plain)

    def QHLineShape(self):
        """This function creates a Horizontal line shape that we can re use.
        """

        self.hLine = QtWidgets.QFrame()
        self.hLine.setFixedWidth(50)
        self.hLine.setMinimumHeight(40)
        self.hLine.setLineWidth(2)
        self.hLine.setFrameShape(QtWidgets.QFrame.HLine)
        self.hLine.setFrameShadow(QtWidgets.QFrame.Plain)        

    def mayaAttributeCnR(self):
        """This function allows to set and delete attributes parameters
        and call the attributeCreate function from the mayaAttributes.py file.
        mayaAttributeCnR is called by the Create button when he is clicked.
        """

        self.name = self.attribNameLineEdit.text()
        self.value = self.attribLineEdit.text()
        self.type = self.comboBoxAttribType.currentText()
        self.on = self.comboBoxAttribTS.currentText()

        if(self.type == 'Integer'):
            self.type   = 'long'
            self.value  = int(self.value)
        
        elif(self.type == 'String'):
            self.type   = 'string'
            self.value  = self.value
        
        else:
            self.type   = 'double'
            self.value  = float(self.value)

        # Call function from mayaAttributes.py

        self.mayaAttrib.attributeCreate(name = self.name, value = self.value, type = self.type, on = self.on)

    def mayaAttributeDel(self):
        """This function call the attributeDelete function from the mayaAttributes.py file.
        self.name and self.on are re used from the mayaAttributeCnR function just on top.
        mayaAttributeDel is called by the Delete button when he is clicked.
        """

        self.name = self.attribNameLineEdit.text()
        self.on = self.comboBoxAttribTS.currentText()

        self.mayaAttrib.attributeDelete(attrName = self.name, on = self.on)

    def exportsInteract(self):

        if(_IN_MAYA_ == True):

            querySceneName = cmds.file(query = True, sceneName = True, shortName = True)
            extensionSplit = querySceneName.split('.')
            sceneNameSplit = extensionSplit[0].split('_')
            name = '_'.join(sceneNameSplit[:3])

            self.sceneName = ''
            self.nameSplit = ''
            self.anmSplit = ''
            self.assetSplit = ''

            self.sceneNameLineEdit.setPlaceholderText("Untilted Scene !")

            if(querySceneName):
                self.sceneNameLineEdit.setText(name)
            else:
                self.sceneNameLineEdit.setPlaceholderText("Untilted Scene !")

            if(self.sceneNameLineEdit.text().startswith('sq')):
    
                self.sceneNameLineEdit.setText('anm_' + name)

            if(self.sceneNameLineEdit.text().startswith('anm')):

                self.startLineEdit.setText(str(int(cmds.playbackOptions(q=True,min=True))))
                self.endLineEdit.setText(str(int(cmds.playbackOptions(q=True,max=True))))

                self.sceneName = self.sceneNameLineEdit.text()

                self.nameSplit = name.split('_')

    def exportTasks(self):
        """This function allows to setup and call all Tasks exports part.
        """

        self.mySel = cmds.ls(sl=True)

        self.sceneName = self.sceneNameLineEdit.text()

        self.sceneNameSplit = self.sceneName.split('_')

        seq     = ''
        shot    = ''

        self.export = MayaExports()

        self.export.getExportPath(self.path)
        self.export.defineItemsTeam(self.comboBoxTeam.currentText())
        
        if(not self.sceneName.startswith('anm')):       # Anim exports.
            
            self.export.typeTagAttribCreation('assets')
            self.export.exportMA(self.checkExportMA, 'tasks', 'assets', 'modeling', None, None, '')
            
        else:                                           # Assets exports.

            self.export.typeTagAttribCreation('shots')
            if(self.comboBoxTeam.currentText() == 'IA'):
                self.export.verifyShotTreeStructure(self.sceneNameSplit[1].upper(), self.sceneNameSplit[2].upper())
                seq     = self.sceneNameSplit[1]
                shot    = self.sceneNameSplit[2]
            elif(self.comboBoxTeam.currentText() == 'LDS'):
                self.export.verifyShotTreeStructure(self.sceneNameSplit[1].upper(), self.sceneNameSplit[2][2:].upper())
                seq     = self.sceneNameSplit[1]
                shot    = self.sceneNameSplit[2][2:]

            self.export.exportMA(self.checkExportMA, 'tasks', 'shots', 'animation', seq, shot, self.sceneName + '_')

    def exportPublishs(self):
        """This function allows to setup and call all Publishs exports part.
        """

        self.mySel = cmds.ls(sl=True)

        self.sceneName = self.sceneNameLineEdit.text()

        self.sceneNameSplit = self.sceneName.split('_')

        seq     = ''
        shot    = ''

        self.export = MayaExports()
        
        self.export.getExportPath(self.path)
        self.export.defineItemsTeam(self.comboBoxTeam.currentText())

        if(not self.sceneName.startswith('anm')):       # Anim exports.
            
            self.export.typeTagAttribCreation('assets')

            self.export.exportOBJ(self.checkExportOBJ, self.checkExportABC, 'publishs', 'assets', 'modeling', None, None, '')
            self.export.exportABC(self.checkExportABC, 'publishs', 'assets', self.startLineEdit.text(),
                self.endLineEdit.text(), self.startSubSLineEdit.text(), self.endSubSLineEdit.text(),
                self.attribExportLineEdit.text().split(','), 'modeling', None, None, '')
            
        else:                                           # Asset exports.

            self.export.typeTagAttribCreation('shots')
            if(self.comboBoxTeam.currentText() == 'IA'):
                self.export.verifyShotTreeStructure(self.sceneNameSplit[1].upper(), self.sceneNameSplit[2].upper())
                seq     = self.sceneNameSplit[1]
                shot    = self.sceneNameSplit[2]
            elif(self.comboBoxTeam.currentText() == 'LDS'):
                self.export.verifyShotTreeStructure(self.sceneNameSplit[1].upper(), self.sceneNameSplit[2][2:].upper())
                seq     = self.sceneNameSplit[1]
                shot    = self.sceneNameSplit[2][2:]

            self.export.exportABC(self.checkExportABC, 'publishs', 'shots', self.startLineEdit.text(),
                self.endLineEdit.text(), self.startSubSLineEdit.text(), self.endSubSLineEdit.text(),
                self.attribExportLineEdit.text().split(','), 'animation', seq, shot, self.sceneName + '_')