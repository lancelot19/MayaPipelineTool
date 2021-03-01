from maya			import OpenMayaUI, cmds
from shiboken2	    import wrapInstance
from PySide2        import QtWidgets, QtCore


import pipelineToolUI.pipelineUI as mUI
import pipelineToolUI.mayaAttributes as mAttrib
import pipelineToolUI.mayaExports as mExport
import pipelineToolUI.setTypeAttribWindow as sAttrib

reload(mAttrib)
reload(sAttrib)
reload(mExport)
reload(mUI)

try:
    wid.close()
except:
    pass

ptr           = OpenMayaUI.MQtUtil.mainWindow()
mainWindow    = wrapInstance(long(ptr), QtWidgets.QWidget)
wid           = mUI.PipelineUI(mainWindow)

wid.show()