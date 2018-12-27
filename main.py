"""
This is a video converter
"""
import sys

from time import sleep

import threading
from PySide2.QtWidgets import QApplication, QWidget
from PySide2 import QtGui, QtWidgets, QtCore
#from multiprocessing import Process
from PySide2.QtCore import Signal
from PySide2.QtCore import QProcess, QIODevice, QByteArray

from Form import Ui_Form


class VidConvertWindow(QWidget, Ui_Form):
    """
    main class
    """
    signal_bar = Signal(float)
    float_timetot = 0
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        "self.listWidget_2.itemSelectionChanged.connect(self.itemActivated_event)"
        self.btnStart.clicked.connect(self.play)
        self.btnStop.clicked.connect(self.stop)
        self.btnOpen.clicked.connect(self.open)
        self.post_init()
        self.addVideoProfiles()
        self.int_stop_flag = 1
        #self.connect(self, QtCore.SIGNAL("Progressvalue"), self.increaseBar)
        self.thread_thd = QProcess() 
        self.thread_thd.setWorkingDirectory('/')
        self.dat = ''
        self.signal_bar.connect(self.setBar)
        #self.thread_thd.readyReadStandardOutput.connect(self.startConvert)



    def post_init(self):
        """
        does extra
        """
        self.btnStart.setIcon(QtGui.QPixmap('./icons/start.ico'))
        self.btnOpen.setIcon(QtGui.QPixmap('./icons/file.ico'))
        self.btnStop.setIcon(QtGui.QPixmap('./icons/stop.ico'))


        self.setWindowTitle("Simple Video Converter")
        self.setGeometry(100, 100, 640, 480)
        
        self.btnOpen.setFixedSize(50,30)
        self.btnStart.setFixedSize(50,30)
        self.btnStop.setFixedSize(50,30)
        self.pushButton.setFixedSize(50,30)

        self.btnStop.setEnabled(False)
        self.listWidget_format.setFixedWidth(200)
        self.progbarCurrent.setValue(0)
        self.progbarTotal.setValue(0)

        

    def play(self):
        
        
        #Toggling Buttons and detting current video length
        
        self.toggleButtons('set')
        self.item = self.listWidget_format.selectedItems()[0].text()
        print(self.item)
        self.thread_thd.start("sh",["-c",'ffprobe -i vid.mp4 -show_entries format=duration -v quiet -of csv="p=0"> tot.txt'])
        self.thread_thd.waitForFinished()
        self.thread_thd.close()
        
        #Read Video length
        with open('/home/avenger047/Desktop/tot.txt', 'r') as f:
            self.float_timetot = float(f.read())
            #print(self.float_timetot)

        self.progbarCurrent.setMaximum(self.float_timetot)


        self.thread_thd.start("sh", ["-c","ffmpeg -i vid.mp4 testr.avi 2> test.txt"]) #Start the conversion process
        print("starting Convert")

        #Read the log file to set progress using a new thread
        p = threading.Thread(target = self.readFile)
        p.setDaemon(True)
        p.start()

        
        
    
    def stop(self):

        self.int_stop_flag = 0
        self.btnStop.setEnabled(False)
        self.btnOpen.setEnabled(True)
        self.btnStart.setEnabled(True)


    def setBar(self, i):
        
        #Set Progress bar from the received signal
        self.progbarCurrent.setValue(i)

    def addVideoProfiles(self):
        
        """
        Here we add the format list items
        """
               
        int_k=1
        format = ['AVI', 'MP4', 'WMV']
        for i in format:
            for j in range (1,4):
                item = str(int_k)+')'+' '+i+' ' +str(j)
                int_k += 1
                self.listWidget_format.addItem(item)


    def open(self):

        """
        Select Video Files
        """
        
        list_loc, _ = QtWidgets.QFileDialog.getOpenFileNames(None,"Open File","", "Videos (*.mp4 *.avi *.wmv *.mkv *.flv *.dat);;All Files(*.*)")
        for i in list_loc:
            self.listWidget_files.addItem(i)


   
    def readFile(self):
        
        print("Reading File")
        i = 1
        while i:
            try:
                with open('/home/avenger047/Desktop/test.txt', 'r') as f:
                    lines = f.read().splitlines() #Get the end line
                    last_line = lines[-1]
                    if ('time=' in last_line): #filter by keyword 'time'
                        str_progress = last_line[last_line.index('time=') + len('time='):last_line.index('time=')+16]
                        print(str_progress)
                        hh, mm, ss = str_progress.split(':')
                        int_progress = (float(hh) * 3600 + float(mm) * 60)
                        ss, sss = ss.split('.')
                        int_progress = int_progress + (float(ss) + (float(sss)/100))
                        self.signal_bar.emit(int_progress)
                        end = int_progress/self.float_timetot
                        #print(end)
                        if (end >= 0.98):
                            self.signal_bar.emit(float_timetot)
                            i=0
                            break
                    
            except:
                pass



    
    def toggleButtons(self,i):
        print(i)
        if i == 'set':
            self.btnStop.setEnabled(True)
            self.btnOpen.setEnabled(False)
            self.btnStart.setEnabled(False)
        elif i == 'reset':
            self.btnStop.setEnabled(False)
            self.btnOpen.setEnabled(True)
            self.btnStart.setEnabled(True)
        else:
            pass



if __name__ == "__main__":
    APP = QApplication(sys.argv)
    WINDOW = VidConvertWindow()
    WINDOW.show()
    sys.exit(APP.exec_())
