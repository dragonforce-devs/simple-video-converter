"""
This is a video converter
"""
import sys

from PySide2.QtWidgets import QApplication, QWidget
from PySide2 import QtGui

from Ui_test_widget import Ui_Form


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
        self.pushButton_2.setIcon(QtGui.QPixmap('./icons/file.ico'))
        self.pushButton_4.setIcon(QtGui.QPixmap('./icons/stop.ico'))

        self.setWindowTitle("Simple Video Converter")
        self.setGeometry(100, 100, 640, 480)
        
        self.pushButton_2.setFixedSize(50,30)
        self.pushButton_3.setFixedSize(50,30)
        self.pushButton_4.setFixedSize(50,30)
        self.pushButton.setFixedSize(50,30)

        self.pushButton_4.setEnabled(False)
        self.listWidget_2.setFixedWidth(200)

        

    def play(self):
        self.pushButton_4.setEnabled(True)
        self.pushButton_3.setEnabled(False)
        self.pushButton_2.setEnabled(False)
        self.item = self.listWidget_2.selectedItems()[0].text()
        print(self.item)

    def stop(self):
        self.pushButton_4.setEnabled(False)
        self.pushButton_3.setEnabled(True)
        self.pushButton_2.setEnabled(True)

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
                self.listWidget_2.addItem(item)
                

if __name__ == "__main__":
    APP = QApplication(sys.argv)
    WINDOW = VidConvertWindow()
    WINDOW.show()
    sys.exit(APP.exec_())
