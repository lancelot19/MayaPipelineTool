
from Qt import QtWidgets

_IN_MAYA_ = False

try:
    from maya import cmds
    _IN_MAYA_ = True
except:
    pass

class MainUI(QtWidgets.QMainWindow):

    def __init__(self, parent = None, **kwargs):
        # Init this class with the parent class init.
        super(MainUI, self).__init__(parent = parent)

        self.initUI()

    def initUI(self):
        """Create the widget interface.
        """
        

        # Set the window title.
        self.setWindowTitle('My Tool')
        # Set the window size.
        self.setMinimumSize(300, 200)

        self.mainWidget = QtWidgets.QWidget()
        
        # Define the main layout.
        self.layout     = QtWidgets.QVBoxLayout()

        # Add a label widget.
        self.label      = QtWidgets.QLabel('Hello World !')

        # Add the label widget to the main layout.
        self.layout.addWidget(self.label)

        # Add a line edit.
        self.line       = QtWidgets.QLineEdit()

        # Add the line edit to the main layout.
        self.layout.addWidget(self.line)

        # Add a push button.
        self.button     = QtWidgets.QPushButton('Click ME !')

        # Connect the button to the function clickMeClicked.
        self.button.clicked.connect(self.clickMeClicked)

        self.addLocatorBtn  = QtWidgets.QPushButton('Add Locator')

        self.layout.addWidget(self.addLocatorBtn)

        # Add the push button to the main layout.

        self.layout.addWidget(self.button)

        # Add the main layout to the current widget.
        self.mainWidget.setLayout(self.layout)

        self.setCentralWidget(self.mainWidget)

    def createLocator(self):
        if(_IN_MAYA_ == True):
            nameLoc = self.line.text()
            cmds.spaceLocator(name = nameLoc)
        else:
            print("IL VEUT PAS")


    def clickMeClicked(self):

        print(self.line.text())

        if(_IN_MAYA_ == True):
            for node in cmds.ls():
                print(node)

        else:
            print("NON JE SUIS PAS DANS MAYA, CAR MAYA C'EST DU BRIN")