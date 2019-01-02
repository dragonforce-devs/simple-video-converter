"""
This is a video converter
"""
import sys
import os

from time import sleep

import threading
from PySide2.QtWidgets import QApplication, QWidget
from PySide2 import QtGui, QtWidgets, QtCore
from PySide2.QtGui import QStandardItemModel, QStandardItem
from PySide2.QtCore import QProcess, QIODevice, QByteArray, Qt, Signal

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
        self.btnStart.clicked.connect(self.convert_clicked)
        self.btnStop.clicked.connect(self.stop)
        self.btnOpen.clicked.connect(self.open)
        self.btnClearQueue.clicked.connect(self.clear_queue)
        
        self.listViewFormat.clicked.connect(self.get_format_item)

        self.int_stop_flag = 1
        self.thread_thd = ''
        #self.thread_thd.setWorkingDirectory('/')
        self.dat = ''
        self.signal_bar.connect(self.set_bar)
        
        self.file_list_model = QStandardItemModel(self.listViewFiles)
        self.listViewFiles.setModel(self.file_list_model)
        self.format_list_model = QStandardItemModel(self.listViewFormat)
        self.listViewFormat.setModel(self.format_list_model)
        #self.listViewFormat.setSelectionMode(SingleSelection)
        self.selected_format = ''
        self.current_file = ''
        self.current_dir = ''
        self.thread_conv = '' 
        self.thread_read = ''

        self.post_init()



    def post_init(self):
        """
        does extra
        """
        self.btnStart.setIcon(QtGui.QPixmap('./icons/start.ico'))
        self.btnOpen.setIcon(QtGui.QPixmap('./icons/file.jpg'))
        self.btnStop.setIcon(QtGui.QPixmap('./icons/stop.ico'))


        self.setWindowTitle("Simple Video Converter")
        self.setGeometry(100, 100, 640, 480)
        
        self.btnOpen.setFixedSize(50,30)
        self.btnStart.setFixedSize(50,30)
        self.btnStop.setFixedSize(50,30)
        self.btnClearQueue.setFixedSize(100,30)

        self.btnStop.setEnabled(False)
        self.listViewFormat.setFixedWidth(200)
        self.progbarCurrent.setValue(0)
        self.progbarTotal.setValue(0)
        self.add_to_listView(['avi', 'mp4', 'wmv'], self.format_list_model, False)

        

    def convert_clicked(self):
        
        self.int_stop_flag = 1
        self.thread_conv = threading.Thread(target = self.start_convert)
        self.thread_conv.setDaemon(True) 
        self.thread_conv.start()
        
    
    
    
    
    
    def start_convert(self):
        
        
        #Toggling Buttons and detting current video length
        

        for index in range(self.file_list_model.rowCount()):

            if (self.int_stop_flag == 0):
                print("Breaking from start_convert")
                break

            #Get File locations from file_list_model
            self.current_file = str(self.file_list_model.item(index).data(Qt.DisplayRole))
            self.toggle_buttons('set')

            self.thread_thd = QProcess() 

            dir_loc = self.current_file.rsplit('/',1)[0]
            self.current_dir = dir_loc
            #print('The selected format is :', self.selected_format)
            self.toggle_buttons('set')
            #print('ffprobe -i ' + file_loc + ' -show_entries format=duration -v quiet -of csv="p=0"> tot.txt')
            self.thread_thd.start("sh",["-c",'ffprobe -i ' + self.current_file + ' -show_entries format=duration -v quiet -of csv="p=0">' + self.current_dir + '/tot.dat'])
            
            #self.thread_thd.waitForFinished() [This operation is causing problem. Hence the try-except]
            #self.thread_thd.close()
        
            #Read Video length
            try:
                with open((self.current_dir + '/tot.dat'), 'r') as f:
                    self.float_timetot = float(f.read())
            except:
                sleep(0.4)
                with open((self.current_dir + '/tot.dat'), 'r') as f:
                    self.float_timetot = float(f.read())
            
            self.thread_thd.close()
            self.progbarCurrent.setMaximum(self.float_timetot)


            self.thread_thd.start("sh", ["-c","ffmpeg -i " + self.current_file + " " + self.current_dir  + "/" + (self.current_file.rsplit('/',1)[1].rsplit('.',1)[0]) + ".avi 2>" + dir_loc + "/logs.dat"]) #Start the conversion process
            print("starting Convert")

            #Read the log file to set progress using a new thread
            self.thread_read = threading.Thread(target = self.read_file)
            self.thread_read.setDaemon(True)
            self.thread_read.start()
            self.thread_thd.waitForFinished()
            self.progbarCurrent.setValue(self.float_timetot)
            self.toggle_buttons('reset')
        sys.exit()

        
        
    
    def stop(self):

        #Not yet implemented
        self.int_stop_flag = 0
        pid = (self.thread_thd.pid())
        print(pid)
        os.system("kill $(pgrep -P "+str(pid)+")")
       
        #self.thread_thd.kill()
        print("killed")
        self.toggle_buttons('reset')
        self.clear_logs(self.current_dir)


    def set_bar(self, i):
        
        #Set Progress bar from the received signal
        self.progbarCurrent.setValue(i)

    def add_to_listView(self, names, model: QStandardItemModel, checkable: bool):

        for items in names:
            list_item = QStandardItem(items)
            list_item.setCheckable(checkable)
            list_item.setEditable(False)
            model.appendRow(list_item)
        
       


    def open(self):

        """
        Select Video Files
        """
        #self.file_list_model.clear() 
        list_loc, _ = QtWidgets.QFileDialog.getOpenFileNames(None,"Open File","", "Videos (*.mp4 *.avi *.wmv *.mkv *.flv *.dat);;All Files(*.*)")
        self.add_to_listView(list_loc, self.file_list_model, False)
        self.file_list = list_loc


   
    def read_file(self):
        
        
        print("Reading File")
        i = 1
        while i==self.int_stop_flag:
            try:
                #print(self.current_file.rsplit('/',1)[0] + '/test.txt')
                with open((self.current_dir + '/logs.dat'), 'r') as f:
                    
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
                            print(">0.98:")
                            i=0
                            self.clear_logs(self.current_dir)
                            sys.exit()
                            
                        else:
                            pass
                    
                    else:
                        pass
            except:
                pass

        print("Breaking from read_file", self.int_stop_flag)
                



    
    def toggle_buttons(self,i):
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


    def get_format_item(self):
		
        #Here we get the selected format

        print('Got Item')
        index = self.listViewFormat.currentIndex()
        sel_format = index.data(Qt.DisplayRole)
        self.selected_format = sel_format
        print(self.selected_format)
    
    def clear_queue(self):
        self.file_list_model.clear()
        self.file_list_model.clear()

    def clear_logs(self, dir_loc: str):
         os.remove(dir_loc + "/logs.dat")
         os.remove(dir_loc + "/tot.dat")



if __name__ == "__main__":
    APP = QApplication(sys.argv)
    WINDOW = VidConvertWindow()
    WINDOW.show()
    sys.exit(APP.exec_())
