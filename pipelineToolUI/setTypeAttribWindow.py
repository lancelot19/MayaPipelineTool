from Qt import QtWidgets, QtCore, QtGui

import sys

class SetTypeAttribWindow(QtWidgets.QDialog):

    def __init__(self, parent = None):
        super(SetTypeAttribWindow, self).__init__(parent)

        layout = QtWidgets.QVBoxLayout()

        label = QtWidgets.QLabel('Set typeTag Attribute :')
        comboBox = QtWidgets.QComboBox()

        comboBox.addItem('characters')
        comboBox.addItem('cloth')
        comboBox.addItem('environment')
        comboBox.addItem('props')
        comboBox.addItem('propsTunnel')
        comboBox.addItem('propsArene')

        pushButton = QtWidgets.QPushButton('OK !')

        layout.addWidget(label, 0, QtCore.Qt.AlignCenter)
        layout.addWidget(comboBox, 0, QtCore.Qt.AlignCenter)
        layout.addWidget(pushButton, 0, QtCore.Qt.AlignCenter)

        self.setLayout(layout)
        self.setWindowTitle('Dialog')
        self.setMinimumSize(250, 200)

        pushButton.clicked.connect(self.hide())