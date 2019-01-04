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
        self.ffmpeg_process = ''
        self.ffprobe_process = ''
        #self.thread_thd.setWorkingDirectory('/')
        self.dat = ''
        self.signal_bar.connect(self.set_bar)
        #self.ffmpeg_process.readyReadStandardOutput.connect(self.read_output) 
        self.file_list_model = QStandardItemModel(self.listViewFiles)
        self.listViewFiles.setModel(self.file_list_model)
        self.format_list_model = QStandardItemModel(self.listViewFormat)
        self.listViewFormat.setModel(self.format_list_model)
        #self.listViewFormat.setSelectionMode(SingleSelection)
        self.selected_format = ''
        self.current_file = ''
        self.current_dir = ''
        #self.thread_conv = '' 
        self.int_index = 0
        self.arr_file_lengths = []
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
        
        
        self.int_index = 0
        for index in range(self.file_list_model.rowCount()):
    
                        
            self.ffprobe_process = QProcess()

            self.ffprobe_process.readyReadStandardOutput.connect(self.read_ffprobe)
            #Get File locations from file_list_model
            self.current_file = str(self.file_list_model.item(index).data(Qt.DisplayRole))
            str_dir_loc = self.current_file.rsplit('/',1)[0] 
            self.ffprobe_process.setWorkingDirectory(str_dir_loc)
            str_file_name = self.current_file.rsplit('/',1)[-1]
            print(self.current_file + '\n' + str_dir_loc + '\t' + str_file_name)
            self.ffprobe_process.start('ffprobe -i "' + str_file_name + '" -show_entries format=duration -v quiet -of csv="p=0"')
            self.ffprobe_process.waitForFinished()
 
        self.int_index = 0 
        print(self.arr_file_lengths) 
        
        self.toggle_buttons('set')

        self.int_stop_flag = 1
        thread_conv = threading.Thread(target = self.start_convert)
        thread_conv.setDaemon(True) 
        thread_conv.start()
        
    
    
    
    
    
    def start_convert(self):
        
        
        #Toggling Buttons and detting current video length
        print('reached start Convert')

        for index in range(self.file_list_model.rowCount()):
    
                        
            self.progbarCurrent.setMaximum(self.arr_file_lengths[self.int_index])
            self.ffmpeg_process = QProcess()
            #self.ffmpeg_process.Daemon = True
            self.ffmpeg_process.readyReadStandardError.connect(self.read_output)
            #Get File locations from file_list_model
            self.current_file = str(self.file_list_model.item(index).data(Qt.DisplayRole))

            str_dir_loc = self.current_file.rsplit('/',1)[0] 
            str_file_name = self.current_file.rsplit('/',1)[-1]
            self.ffmpeg_process.setWorkingDirectory(str_dir_loc)
            
            print(self.current_file + '\n' + str_dir_loc + '\t' + str_file_name)
            print('ffmpeg -i "' + str_file_name + '" "' + str_file_name.rsplit('.',1)[0] + '.avi"')
            self.ffmpeg_process.start('ffmpeg -i "' + str_file_name + '" "' + str_file_name.rsplit('.',1)[0] + '.avi"' )
            self.ffmpeg_process.waitForFinished()
            self.ffmpeg_process.close()
            self.int_index += 1

        self.toggle_buttons('reset')
        print('Ended') 
        
    
    
    
    def read_ffprobe(self):
        
        str_op = self.ffprobe_process.readAllStandardOutput().data().decode("utf-8")
        self.arr_file_lengths.append(float(str_op))
        self.int_index += 1

        
    
    def stop(self):

        #Not yet implemented
        print('Yet to be implemented')


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


   
    def read_output(self):
        
        #print(mode)
        #print("Reading File")
        str_op = self.ffmpeg_process.readAllStandardError().data().decode("utf-8")
        #print(str_op)
        if ('time=' in str_op): #filter by keyword 'time'
            str_progress = str_op[str_op.index('time=') + len('time='):str_op.index('time=')+16]
            print(str_progress)
            hh, mm, ss = str_progress.split(':')
            float_progress = (float(hh) * 3600 + float(mm) * 60)
            ss, sss = ss.split('.')
            float_progress = float_progress + (float(ss) + (float(sss)/100))
            self.signal_bar.emit(float_progress)
        

    
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



if __name__ == "__main__":
    APP = QApplication(sys.argv)
    WINDOW = VidConvertWindow()
    WINDOW.show()
    sys.exit(APP.exec_())
