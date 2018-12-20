"""
This is a video converter
"""
import sys

from PySide2.QtWidgets import QApplication, QWidget, QFileDialog
from PySide2 import QtGui, QtWidgets

from Form import Ui_Form


class VidConvertWindow(QWidget, Ui_Form):
    """
    main class
    """
    item = ''

    def __init__(self):
        super().__init__()
        self.setupUi(self)

        self.filePicker = QFileDialog(self)

        self.btnStop.clicked.connect(self.stop_convertion)
        self.btnAdd.clicked.connect(self.add_files)
        self.btnConvert.clicked.connect(self.start_convertion)
        self.post_init()
        self.addVideoProfiles()

    """
    def itemActivated_event(self):
        self.item = self.listWidget_2.selectedItems()[0].text()
    """

    def post_init(self):
        """
        does extra
        """
        self.btnConvert.setIcon(QtGui.QPixmap('./icons/start.ico'))
        self.btnAdd.setIcon(QtGui.QPixmap('./icons/file.ico'))
        self.btnStop.setIcon(QtGui.QPixmap('./icons/stop.ico'))

        self.setWindowTitle("Simple Video Converter")
        self.setGeometry(100, 100, 640, 480)

        # self.btnAdd.setFixedSize(50,30)
        # self.btnConvert.setFixedSize(50,30)
        # self.btnStop.setFixedSize(50,30)

    def add_files(self):
        self.filePicker.setFileMode(QFileDialog.ExistingFiles)
        self.filePicker.setNameFilter("Videos (*.mp4 *.mkv *.mov)")
        self.filePicker.setViewMode(QFileDialog.Detail)
        if self.filePicker.exec_():
            files_selected = self.filePicker.selectedFiles()
            for f in files_selected:
                print(f)
        pass

    def start_convertion(self):
        pass

    def stop_convertion(self):
        pass

    def play(self):
        self.pushButton_4.setEnabled(True)
        self.pushButton_3.setEnabled(False)
        self.pushButton_open.setEnabled(False)
        self.item = self.listWidget_format.selectedItems()[0].text()
        print(self.item)

    def stop(self):
        self.pushButton_4.setEnabled(False)
        self.pushButton_3.setEnabled(True)
        self.pushButton_open.setEnabled(True)

    def addVideoProfiles(self):
        pass

    #     """
    #     Here we add the format list items
    #     """

    #     k=1
    #     format = ['AVI', 'MP4', 'WMV']
    #     for i in format:
    #         for j in range (1,4):
    #             item = str(k)+')'+' '+i+' ' +str(j)
    #             k = k+1
    #             self.listWidget_format.addItem(item)

    # def open(self):

    #     """
    #     Select Video Files
    #     """
    #     options = QtWidgets.QFileDialog.Options()
    #     loc, _ = QtWidgets.QFileDialog.getOpenFileNames(None,"Open File","", "Videos (*.mp4 *.avi *.wmv *.mkv *.flv *.dat);;All Files(*.*)")
    #     for i in loc:
    #         self.listWidget_files.addItem(i)


if __name__ == "__main__":
    APP = QApplication(sys.argv)
    WINDOW = VidConvertWindow()
    WINDOW.show()
    sys.exit(APP.exec_())
