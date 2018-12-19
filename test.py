"""
this approach loads the ui file directly
"""

import sys
from PySide2.QtUiTools import QUiLoader
from PySide2.QtCore import QFile
from PySide2.QtWidgets import QApplication, QMainWindow


class VidConWin(QMainWindow):
    """
    mainwindow class
    """

    def __init__(self):
        super().__init__()
        self.load_ui()

    def load_ui(self):
        """
        loads ui from file
        """
        ui_file = QFile("test_widget.ui")
        ui_file.open(QFile.ReadOnly)

        ui_loader = QUiLoader()
        ui_widget = ui_loader.load(ui_file)
        self.setCentralWidget(ui_widget)



if __name__ == "__main__":
    APP = QApplication(sys.argv)
    WINDOW = VidConWin()
    WINDOW.show()
    sys.exit(APP.exec_())
