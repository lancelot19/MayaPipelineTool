from maya			import OpenMayaUI
from shiboken2	    import wrapInstance
from PySide2        import QtWidgets, QtCore

import pipelineToolUI.pipelineUI as mUI

reload(mUI)

ptr           = OpenMayaUI.MQtUtil.mainWindow()
mainWindow    = wrapInstance(long(ptr), QtWidgets.QWidget)
wid           = mUI.PipelineUI(mainWindow)
wid.show()