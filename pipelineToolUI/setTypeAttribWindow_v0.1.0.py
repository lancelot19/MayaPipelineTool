from Qt import QtWidgets, QtCore, QtGui

_IN_MAYA_ = False

try:
    from maya import cmds
    
    _IN_MAYA_ = True
except:
    print("PAS DANS MAYA")

class SetTypeAttribWindow(QtWidgets.QDialog):

    def __init__(self, parent = None):
        super(SetTypeAttribWindow, self).__init__(parent)

        layout = QtWidgets.QVBoxLayout()

        label = QtWidgets.QLabel('Set typeTag Attribute :')
        assetNameLabel = QtWidgets.QLabel('Asset Name :')
        self.nameAsset = QtWidgets.QLabel()
        self.nameAsset.setFont(QtGui.QFont('Times', 10))

        self.comboBox = QtWidgets.QComboBox()

        self.pushButton = QtWidgets.QPushButton('OK !')
        self.pushButton.setDefault(True)

        layout.addWidget(assetNameLabel, 0, QtCore.Qt.AlignCenter)
        layout.addWidget(self.nameAsset, 0, QtCore.Qt.AlignCenter)
        layout.addWidget(label, 0, QtCore.Qt.AlignCenter)
        layout.addWidget(self.comboBox, 0, QtCore.Qt.AlignCenter)
        layout.addWidget(self.pushButton, 0, QtCore.Qt.AlignCenter)

        self.setLayout(layout)
        self.setWindowTitle('Dialog')
        self.setMinimumSize(250, 200)

        # Re set self flags and add WindowStayOnTopHint to keep the Dialog window on top of desktop.
        self.setWindowFlags(self.windowFlags() | QtCore.Qt.WindowStaysOnTopHint) 

        self.pushButton.clicked.connect(self.clickedClose)
        #self.pushButton.clicked.connect(self.clickedClose)

    def clickedClose(self):

        self.accept()

    def clickedGetTypeTag(self):

        self.comboBox.currentText()

    def assetName(self, assetName):

        self.nameAsset.setText(assetName)

    def items(self, team):

        if(team == 'IA'):

            self.comboBox.addItem('characters')
            self.comboBox.addItem('cloth')
            self.comboBox.addItem('environment')
            self.comboBox.addItem('props')
            self.comboBox.addItem('propsTunnel')
            self.comboBox.addItem('propsArene')

        if(team == 'LDS'):

            self.comboBox.addItem('characters')
            self.comboBox.addItem('cloth')
            self.comboBox.addItem('environment')
            self.comboBox.addItem('props')
            self.comboBox.addItem('propsMale')
            self.comboBox.addItem('propsFemale')