
from PyQt4 import QtCore, QtGui

try:
    _fromUtf8 = QtCore.QString.fromUtf8
except AttributeError:
    def _fromUtf8(s):
        return s

try:
    _encoding = QtGui.QApplication.UnicodeUTF8
    def _translate(context, text, disambig):
        return QtGui.QApplication.translate(context, text, disambig, _encoding)
except AttributeError:
    def _translate(context, text, disambig):
        return QtGui.QApplication.translate(context, text, disambig)

class Ui_Widget(object):
    def setupUi(self, Widget):
        Widget.setObjectName(_fromUtf8("Widget"))
        Widget.resize(926, 506)
        self.groupBox = QtGui.QGroupBox(Widget)
        self.groupBox.setGeometry(QtCore.QRect(280, 90, 521, 141))
        self.groupBox.setObjectName(_fromUtf8("groupBox"))
        self.label = QtGui.QLabel(self.groupBox)
        self.label.setGeometry(QtCore.QRect(50, 30, 21, 41))
        font = QtGui.QFont()
        font.setPointSize(20)
        self.label.setFont(font)
        self.label.setObjectName(_fromUtf8("label"))
        self.label_2 = QtGui.QLabel(self.groupBox)
        self.label_2.setGeometry(QtCore.QRect(180, 30, 21, 41))
        font = QtGui.QFont()
        font.setPointSize(20)
        self.label_2.setFont(font)
        self.label_2.setObjectName(_fromUtf8("label_2"))
        self.label_3 = QtGui.QLabel(self.groupBox)
        self.label_3.setGeometry(QtCore.QRect(320, 30, 21, 41))
        font = QtGui.QFont()
        font.setPointSize(20)
        self.label_3.setFont(font)
        self.label_3.setObjectName(_fromUtf8("label_3"))
        self.label_4 = QtGui.QLabel(self.groupBox)
        self.label_4.setGeometry(QtCore.QRect(450, 30, 21, 41))
        font = QtGui.QFont()
        font.setPointSize(20)
        self.label_4.setFont(font)
        self.label_4.setObjectName(_fromUtf8("label_4"))
        self.textEdit = QtGui.QTextEdit(self.groupBox)
        self.textEdit.setGeometry(QtCore.QRect(10, 80, 101, 31))
        self.textEdit.setObjectName(_fromUtf8("textEdit"))
        self.textEdit_2 = QtGui.QTextEdit(self.groupBox)
        self.textEdit_2.setGeometry(QtCore.QRect(140, 80, 101, 31))
        self.textEdit_2.setObjectName(_fromUtf8("textEdit_2"))
        self.textEdit_3 = QtGui.QTextEdit(self.groupBox)
        self.textEdit_3.setGeometry(QtCore.QRect(280, 80, 101, 31))
        self.textEdit_3.setObjectName(_fromUtf8("textEdit_3"))
        self.textEdit_4 = QtGui.QTextEdit(self.groupBox)
        self.textEdit_4.setGeometry(QtCore.QRect(410, 80, 101, 31))
        self.textEdit_4.setObjectName(_fromUtf8("textEdit_4"))
        self.pushButton = QtGui.QPushButton(Widget)
        self.pushButton.setGeometry(QtCore.QRect(50, 90, 111, 51))
        self.pushButton.setObjectName(_fromUtf8("pushButton"))

        self.retranslateUi(Widget)
        QtCore.QObject.connect(self.pushButton, QtCore.SIGNAL(_fromUtf8("clicked()")), Widget.close)
        QtCore.QMetaObject.connectSlotsByName(Widget)

    def retranslateUi(self, Widget):
        Widget.setWindowTitle(_translate("Widget", "Widget", None))
        self.groupBox.setTitle(_translate("Widget", "Single Photon Counts", None))
        self.label.setText(_translate("Widget", "A", None))
        self.label_2.setText(_translate("Widget", "B", None))
        self.label_3.setText(_translate("Widget", "C", None))
        self.label_4.setText(_translate("Widget", "D", None))
        self.pushButton.setText(_translate("Widget", "STOP", None))


if __name__ == "__main__":
    import sys
    app = QtGui.QApplication(sys.argv)
    Widget = QtGui.QWidget()
    ui = Ui_Widget()
    ui.setupUi(Widget)
    Widget.show()
    sys.exit(app.exec_())

