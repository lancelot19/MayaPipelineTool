
from Qt import QtWidgets, QtCore, QtGui
from pipelineToolUI.separation_line import QVSeperationLine
_IN_MAYA_ = False

try:
    from maya import cmds
    _IN_MAYA_ = True
except:
    pass

class PipelineUI(QtWidgets.QMainWindow):

    def __init__(self, parent = None, **kwargs):
        # Init this class with the parent class init.
        super(PipelineUI, self).__init__(parent = parent)

        self.initUI()

    def initUI(self):
        """Create the widget interface.
        """
        
        # Set the window title.
        self.setWindowTitle('Pipeline Tool')
        # Set the window size.
        self.setMinimumSize(1050, 900)
        self.setMaximumSize(1050, 900)

        self.layoutBase()

        self.localPathWidget()

        # Compute the team lock layout function.
        self.teamLockWidget()

        # Compute the searchAndDropLayout function.
        self.searchAndDropWidget()

        self.attribUIWidget()

        self.exportUIWidget()

        self.attribExport()

        self.exportButtons()
        # Add widgets to child widgets

        self.childLayout1.addWidget(self.teamWidget)
        self.childLayout1.addWidget(self.searchNDropWidget)

        self.chilWidget1.setLayout(self.childLayout1)
        
        self.childLayout2.addWidget(self.localWidget)
        self.childLayout2.addWidget(self.attribVWidget)
        self.childLayout2.addWidget(self.exportSceneNameVWidget)
        self.childLayout2.addWidget(self.exportMainWidget)
        self.childLayout2.addWidget(self.attribExportWidget)
        self.childLayout2.addWidget(self.exportButtonWidget)

        self.chilWidget2.setLayout(self.childLayout2)

        # Add child widgets to the main layout.

        self.mainLayout.addWidget(self.chilWidget1)
        self.mainLayout.addWidget(self.chilWidget2)

        # Set the main layout to the main widget.
        self.mainWidget.setLayout(self.mainLayout)
        self.setCentralWidget(self.mainWidget)
    '''
    def createLocator(self):
        if(_IN_MAYA_ == True):
            nameLoc = self.line.text()
            cmds.spaceLocator(name = nameLoc)
        else:
            print("IL VEUT PAS")
    '''

    def layoutBase(self):
        # Create the main Widget.
        self.mainWidget = QtWidgets.QWidget()
        # Create the main Layout.
        self.mainLayout = QtWidgets.QHBoxLayout()
        self.mainLayout.setContentsMargins(0, 0, 0, 0)

        # Create the child widgets.
        self.chilWidget1 = QtWidgets.QWidget()
        self.chilWidget2 = QtWidgets.QWidget()
        # Create the child Layouts.
        self.childLayout1 = QtWidgets.QVBoxLayout()
        self.childLayout1.setContentsMargins(0, 0, 0, 0)
        self.childLayout2 = QtWidgets.QVBoxLayout()
        self.childLayout2.setContentsMargins(0, 0, 0, 0)

        # Set the child layouts to the child widgets.

        self.chilWidget1.setLayout(self.childLayout1)
        self.chilWidget2.setLayout(self.childLayout2)

    def localPathWidget(self):
        self.localWidget = QtWidgets.QWidget()
        self.localLayout = QtWidgets.QHBoxLayout(self.localWidget)
        self.localLayout.setContentsMargins(0, 20, 10, 0)

        self.localLayout.setSpacing(5)
        self.pathLabel = QtWidgets.QLabel('Path :')
        self.localCheckBox = QtWidgets.QCheckBox('Local')

        # Create line edit for path.
        self.pathLineEdit = QtWidgets.QLineEdit()
        self.pathLineEdit.setFixedSize(300, 32)

        self.localLayout.addWidget(self.localCheckBox, 0, QtCore.Qt.AlignRight)
        self.localLayout.addWidget(self.pathLabel, 0, QtCore.Qt.AlignRight)
        self.localLayout.addWidget(self.pathLineEdit)

        self.localWidget.setLayout(self.localLayout)

    def teamLockWidget(self):
        # Create the team widget.
        self.teamWidget = QtWidgets.QWidget()

        # Create the team layout.
        self.teamLayout = QtWidgets.QHBoxLayout(self.chilWidget1)
        self.teamLayout.setContentsMargins(10, 15, 0, 0)
        
        self.teamLayout.setSpacing(20)
        
        # Create and set the team QLabel.
        self.teamLabel = QtWidgets.QLabel('Team :')
        

        # Create and set the comboBox Team.
        self.comboBoxTeam = QtWidgets.QComboBox()
        self.comboBoxTeam.addItem('IA')
        self.comboBoxTeam.addItem('LDS')
        self.comboBoxTeam.addItem('OPS')
        
        # Create and set the checkBox Lock.
        self.checkBoxLock = QtWidgets.QCheckBox('Lock')
        


        self.QVLineShape()
        self.vLine.setFixedWidth(15)

        # Add the widgets to the teamLayout.
        self.teamLayout.addWidget(self.teamLabel, 0, QtCore.Qt.AlignRight)
        self.teamLayout.addWidget(self.comboBoxTeam)
        self.teamLayout.addWidget(self.checkBoxLock)
        self.teamLayout.addWidget(self.vLine)

        # Add the layout to the widget.
        self.teamWidget.setLayout(self.teamLayout)

    def searchAndDropWidget(self):
        # Create the searchNDrop widget.
        self.searchNDropWidget = QtWidgets.QWidget()

        # Create the searchNDrop Layout.
        self.searchNDropLayout = QtWidgets.QVBoxLayout(self.chilWidget1)
        # Create and set the search label.
        self.searchLabel = QtWidgets.QLabel('Search :')
        self.searchLabel.setFont(QtGui.QFont('Times', 10))
        # Create the search line editor.
        self.searchLineEdit = QtWidgets.QLineEdit()
        # Create the QtreeView searcher.
        self.searchTreeView = QtWidgets.QTreeView()

        self.path = "P:\shows\IA"

        self.model = QtWidgets.QFileSystemModel()
        self.model.setRootPath(self.path)

        self.searchTreeView.setModel(self.model)
        self.searchTreeView.setRootIndex(self.model.index(self.path))
        self.searchTreeView.setAcceptDrops(True)
        self.searchTreeView.setDragDropOverwriteMode(True)
        self.searchTreeView.setDragDropMode(QtWidgets.QAbstractItemView.DragDrop)

        # Add the widgets to the searchNDropLayout.
        self.searchNDropLayout.addWidget(self.searchLabel, 0, QtCore.Qt.AlignHCenter)
        self.searchNDropLayout.addWidget(self.searchLineEdit)
        self.searchNDropLayout.addWidget(self.searchTreeView)

        # Add the layout to the widget.
        self.searchNDropWidget.setLayout(self.searchNDropLayout)

    def attribUIWidget(self):

        self.QHLineShape()
        self.hLine.setFixedWidth(540)
        self.hLine.setMinimumHeight(10)

        # Create the attrib widget.
        self.attribWidget = QtWidgets.QWidget()
        self.attribVWidget = QtWidgets.QWidget()
        self.attribChoiceWidget = QtWidgets.QWidget()
        self.attribTypeWidget = QtWidgets.QWidget()
        # Create the attrib layout.
        self.attribTypeLayout = QtWidgets.QHBoxLayout(self.chilWidget2)
        self.attribTypeLayout.setContentsMargins(50, 0, 5, 0)

        self.attribLayout = QtWidgets.QHBoxLayout(self.chilWidget2)
        self.attribLayout.setContentsMargins(0, 0, 5, 5)

        self.attribChoiceLayout = QtWidgets.QHBoxLayout(self.chilWidget2)
        self.attribChoiceLayout.setContentsMargins(0, 0, 5, 5)

        self.attribVLayout = QtWidgets.QVBoxLayout(self.chilWidget2)
        self.attribVLayout.setContentsMargins(0, 12, 5, 5)

        # Create and set attribute labels.
        self.attribLabel = QtWidgets.QLabel('Attributes :')
        self.attribTypeLabel = QtWidgets.QLabel('Type :')
        self.attribOnLabel = QtWidgets.QLabel('On :')
        self.attribLabel.setFont(QtGui.QFont('Times', 10))
        self.attribNameLabel = QtWidgets.QLabel('Name :')
        self.setAttribLabel = QtWidgets.QLabel('Value :')
        # Create attrib edit line.
        self.attribLineEdit = QtWidgets.QLineEdit()
        self.attribNameLineEdit = QtWidgets.QLineEdit()
        self.attribNameLineEdit.setText('GuerillaTags')
        # Create the combo box to choose transform or shape attribute.
        self.comboBoxAttribTS = QtWidgets.QComboBox()
        self.comboBoxAttribTS.addItem('Shape')
        self.comboBoxAttribTS.addItem('Transform')

        # Create the combo box to choose the type of the attribute.
        self.comboBoxAttribType = QtWidgets.QComboBox()
        self.comboBoxAttribType.addItem('String')
        self.comboBoxAttribType.addItem('Integer')
        self.comboBoxAttribType.addItem('Float')

        # Create attrib buttons 'create' and 'replace'.
        self.attribCreateButton = QtWidgets.QPushButton('Create')
        self.attribReplaceButton = QtWidgets.QPushButton('Replace')
        self.attribDeleteButton = QtWidgets.QPushButton('Delete')

        self.attribTypeLayout.addWidget(self.attribLabel, 0, QtCore.Qt.AlignRight)
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
        self.attribLayout.addWidget(self.attribReplaceButton)
        self.attribLayout.addWidget(self.attribDeleteButton)
        # Add the layout to the attrib widget.
        self.attribWidget.setLayout(self.attribLayout)

        self.attribVLayout.addWidget(self.attribTypeWidget)
        self.attribVLayout.addWidget(self.attribChoiceWidget)
        self.attribVLayout.addWidget(self.attribWidget)
        self.attribVLayout.addWidget(self.hLine)

        self.attribVWidget.setLayout(self.attribVLayout)

        # Connect attrib type to attribName line edit.
        self.comboBoxAttribTS.activated[str].connect(self.determineAttribName)

    def determineAttribName(self):
        self.idx = self.comboBoxAttribTS.currentIndex()
        if(self.idx == 0):
            self.attribNameLineEdit.setText('GuerillaTags')
        else:
            self.attribNameLineEdit.setText('variant')

    def exportUIWidget(self):
        # Create the main export widget.
        self.exportMainWidget = QtWidgets.QWidget()

        self.exportSceneName()
        self.exportChild1()
        self.exportChild2()
        self.QVLineShape()
        self.vLine.setMinimumHeight(1)
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

        # Add widgets to the scene name layout.
        self.exportSceneNameLayout.addWidget(self.exportSceneNameLabel, 0, QtCore.Qt.AlignHCenter)
        self.exportSceneNameLayout.addWidget(self.sceneNameLineEdit)

        # Set the scene name layout to the scene name widget.
        self.exportSceneNameWidget.setLayout(self.exportSceneNameLayout)
 
        # Add widgets to the sceneNameVLayout.
        self.exportSceneNameVLayout.addWidget(self.exportLabel, 0, QtCore.Qt.AlignHCenter)
        self.exportSceneNameVLayout.addWidget(self.exportSceneNameWidget)
        self.exportSceneNameVLayout.addStretch()

        # Set the scene name Vlayout to the scene name Vwidget.
        self.exportSceneNameVWidget.setLayout(self.exportSceneNameVLayout)


    def exportChild1(self):
        # Create the child1 exports widget.
        self.exportChildWidget1 = QtWidgets.QWidget()

        # Create the child1 export layout.
        self.exportChildLayout1 = QtWidgets.QVBoxLayout(self.exportChildWidget1)
        self.exportChildLayout1.setContentsMargins(50, 0, 0, 45)

        # Create checkBoxes.
        self.checkExportOBJ = QtWidgets.QCheckBox('.Ma')
        self.checkExportMA = QtWidgets.QCheckBox('.Obj')
        self.checkExportABC = QtWidgets.QCheckBox('.Abc')

        # Add Widgets to the child layouts.
        self.exportChildLayout1.addWidget(self.checkExportOBJ, 0, QtCore.Qt.AlignHCenter)
        self.exportChildLayout1.addWidget(self.checkExportMA, 0, QtCore.Qt.AlignHCenter)
        self.exportChildLayout1.addWidget(self.checkExportABC, 0, QtCore.Qt.AlignHCenter)
        self.exportChildLayout1.setSpacing(75)

        # Set child layout to child widget.
        self.exportChildWidget1.setLayout(self.exportChildLayout1)

    def exportChild2(self):

        self.alembicOptions()

        # Create the child2 export widget.
        self.exportChildWidget2 = QtWidgets.QWidget()
        self.exportLabelHWidget1 = QtWidgets.QWidget()
        self.stepWidget = QtWidgets.QWidget()
        self.subSWidget = QtWidgets.QWidget()
        # Create the child exports layout.
        self.exportChildLayout2 = QtWidgets.QVBoxLayout(self.exportChildWidget2)
        self.exportChildLayout2.setContentsMargins(0, 0, 5, 75)

        self.exportLabelHLayout1 = QtWidgets.QHBoxLayout(self.exportLabelHWidget1)
        self.exportLabelHLayout1.setContentsMargins(0, 0, 0, 75)

        self.stepLayout = QtWidgets.QHBoxLayout(self.stepWidget)
        self.stepLayout.setContentsMargins(0, 0, 0, 50)
        self.subSLayout = QtWidgets.QHBoxLayout(self.subSWidget)
        self.subSLayout.setContentsMargins(0, 0, 0, 0)
        # Add widgets to layout.
        self.exportLabelHLayout1.addWidget(self.startLabel)
        self.exportLabelHLayout1.addWidget(self.startLineEdit)
        self.exportLabelHLayout1.addWidget(self.endLabel)
        self.exportLabelHLayout1.addWidget(self.endLineEdit)

        self.stepLayout.addWidget(self.stepLabel)
        self.stepLayout.addWidget(self.stepLineEdit)

        #self.subSLayout.addWidget(self.subsampleLabel)
        self.subSLayout.addWidget(self.startSubSLineEdit)
        self.subSLayout.addWidget(self.endSubSLineEdit)

        # Add the widgets to the layout.
        self.exportChildLayout2.addWidget(self.alembicOptionsLabel, 0, QtCore.Qt.AlignHCenter)
        self.exportChildLayout2.addWidget(self.exportLabelHWidget1, 0, QtCore.Qt.AlignHCenter)
        self.exportChildLayout2.addWidget(self.stepWidget, 0, QtCore.Qt.AlignHCenter)
        self.exportChildLayout2.addWidget(self.subsampleLabel, 0, QtCore.Qt.AlignHCenter)
        self.exportChildLayout2.addWidget(self.subSWidget, 0, QtCore.Qt.AlignHCenter)
        self.exportChildLayout2.setSpacing(20)

        # Set child layout to child widgets.
        self.exportLabelHWidget1.setLayout(self.exportLabelHLayout1)
        self.stepWidget.setLayout(self.stepLayout)
        self.subSWidget.setLayout(self.subSLayout)
        self.exportChildWidget2.setLayout(self.exportChildLayout2)

    def alembicOptions(self):

        # Creates the Labels.
        self.alembicOptionsLabel = QtWidgets.QLabel('Alembic Options :')
        self.alembicOptionsLabel.setFont(QtGui.QFont('Times', 8))

        self.startLabel = QtWidgets.QLabel('Start :')
        self.endLabel = QtWidgets.QLabel('End :')

        self.stepLabel = QtWidgets.QLabel('Step :')
        self.subsampleLabel = QtWidgets.QLabel('Subsamples :')

        # Create the line edits.
        self.startLineEdit = QtWidgets.QLineEdit()
        self.startLineEdit.setText('1')
        self.endLineEdit = QtWidgets.QLineEdit()
        self.endLineEdit.setText('1')
        self.stepLineEdit = QtWidgets.QLineEdit()
        self.stepLineEdit.setText('1.0')
        self.startSubSLineEdit = QtWidgets.QLineEdit()
        self.startSubSLineEdit.setText('-0.2')
        self.endSubSLineEdit = QtWidgets.QLineEdit()
        self.endSubSLineEdit.setText('0.2')

    def attribExport(self):
        # Create the widget.
        self.attribExportWidget = QtWidgets.QWidget()

        # Create the layout.
        self.attribExportLayout = QtWidgets.QHBoxLayout(self.attribExportWidget)

        # Create the label.
        self.attribExportLabel = QtWidgets.QLabel('Export Attributes :')

        # Create the comboBox.
        self.attribExportLineEdit = QtWidgets.QLineEdit()
        self.attribExportLineEdit.setText('GuerillaTags,variant')

        # Create the Add Button.
        self.attribExportButton = QtWidgets.QPushButton('Add')
        
        # Add widgets to the layout.
        self.attribExportLayout.addWidget(self.attribExportLabel)
        self.attribExportLayout.addWidget(self.attribExportLineEdit)
        self.attribExportLayout.addWidget(self.attribExportButton)

        # Set the layout to the widget.
        self.attribExportWidget.setLayout(self.attribExportLayout)

    def exportButtons(self):
        # Create the export buttons widget.
        self.exportButtonWidget = QtWidgets.QWidget()
        # Create the export buttons layout.
        self.exportButtonLayout = QtWidgets.QHBoxLayout(self.exportButtonWidget)
        self.exportButtonLayout.setSpacing(30)

        # Create the QPushButton widgets.
        self.taskPushButton = QtWidgets.QPushButton('Tasks')
        self.taskPushButton.setFixedSize(250, 100)
        self.publishPushButton = QtWidgets.QPushButton('Publishs')
        self.publishPushButton.setFixedSize(250, 100)

        # Add the buttons to the layout.
        self.exportButtonLayout.addWidget(self.taskPushButton)
        self.exportButtonLayout.addWidget(self.publishPushButton)

        # Add the layout to the widget.
        self.exportButtonWidget.setLayout(self.exportButtonLayout)

    def QVLineShape(self):
        self.vLine = QtWidgets.QFrame()
        self.vLine.setFixedWidth(50)
        self.vLine.setMinimumHeight(40)
        self.vLine.setLineWidth(2)
        self.vLine.setFrameShape(QtWidgets.QFrame.VLine)
        self.vLine.setFrameShadow(QtWidgets.QFrame.Plain)

    def QHLineShape(self):
        self.hLine = QtWidgets.QFrame()
        self.hLine.setFixedWidth(50)
        self.hLine.setMinimumHeight(40)
        self.hLine.setLineWidth(2)
        self.hLine.setFrameShape(QtWidgets.QFrame.HLine)
        self.hLine.setFrameShadow(QtWidgets.QFrame.Plain)
        self.hLine.setSizePolicy(QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Preferred)

    def clickMeClicked(self):

        print(self.line.text())

        if(_IN_MAYA_ == True):
            for node in cmds.ls():
                print(node)

        else:
            print("NON JE SUIS PAS DANS MAYA, CAR MAYA C'EST DU BRIN")