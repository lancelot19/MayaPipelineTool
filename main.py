import sys

from Qt import QtWidgets
from toolUI.mainUI import MainUI

def __main__():

    # Create the Qt application.
    app = QtWidgets.QApplication(sys.argv)
    # Create the main widget.
    wid = MainUI()
    # Show the main widget.
    wid.show()
    # Launch the application and wait the close event.
    sys.exit(app.exec_())


__main__()