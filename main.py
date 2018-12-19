"""
This is a video converter
"""
import sys

from PySide2.QtWidgets import QApplication, QWidget
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
        "self.listWidget_2.itemSelectionChanged.connect(self.itemActivated_event)"
        self.pushButton_3.clicked.connect(self.play)
        self.pushButton_4.clicked.connect(self.stop)
        self.pushButton_open.clicked.connect(self.open)
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
        self.pushButton_3.setIcon(QtGui.QPixmap('./icons/start.ico'))
        self.pushButton_open.setIcon(QtGui.QPixmap('./icons/file.ico'))
        self.pushButton_4.setIcon(QtGui.QPixmap('./icons/stop.ico'))

        self.pushButton_3.setText('')
        self.pushButton_4.setText('')

        self.setWindowTitle("Simple Video Converter")
        self.setGeometry(100, 100, 640, 480)
        
        self.pushButton_open.setFixedSize(50,30)
        self.pushButton_3.setFixedSize(50,30)
        self.pushButton_4.setFixedSize(50,30)
        self.pushButton.setFixedSize(50,30)

        self.pushButton_4.setEnabled(False)
        self.listWidget_format.setFixedWidth(200)

        

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
        
        """
        Here we add the format list items
        """
               
        k=1
        format = ['AVI', 'MP4', 'WMV']
        for i in format:
            for j in range (1,4):
                item = str(k)+')'+' '+i+' ' +str(j)
                k = k+1
                self.listWidget_format.addItem(item)


    def open(self):

        """
        Select Video Files
        """
        options = QtWidgets.QFileDialog.Options()
        loc, _ = QtWidgets.QFileDialog.getOpenFileNames(None,"Open File","", "Videos (*.mp4 *.avi *.wmv *.mkv *.flv *.dat);;All Files(*.*)")
        for i in loc:
            self.listWidget_files.addItem(i)
                

if __name__ == "__main__":
    APP = QApplication(sys.argv)
    WINDOW = VidConvertWindow()
    WINDOW.show()
    sys.exit(APP.exec_())
