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
    signal_bar = Signal(float, str)
    signal_buttons = Signal(str)
    signal_file_name = Signal(str)
    float_timetot = 0
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        "self.listWidget_2.itemSelectionChanged.connect(self.itemActivated_event)"
        self.btnStart.clicked.connect(self.convert_clicked)
        self.btnStop.clicked.connect(self.stop)
        self.btnOpen.clicked.connect(self.open)
        self.btnClearQueue.clicked.connect(self.clear_queue)
        
        self.crfSlider.sliderMoved.connect(self.slider_val)

        self.listViewFormat.clicked.connect(self.get_format_item)

        self.int_stop_flag = 1
        self.ffmpeg_process = None
        self.ffprobe_process = None
        #self.thread_thd.setWorkingDirectory('/')
        self.dat = ''

        self.signal_bar.connect(self.set_bar)
        self.signal_buttons.connect(self.toggle_buttons)
        self.signal_file_name.connect(self.set_label_text)
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
        self.float_total_length = 0.0
        
        self.str_preset = ['ultrafast', 'superfast', 'veryfast', 'faster', 'fast', 'medium', 'slow', 'slower', 'veryslow']
        self.str_reso = ['1080', '720', '480', '320']
        
        
        self.set_combo()
        self.post_init()
        


    def post_init(self):
        """
        does extra
        """
        self.btnStart.setIcon(QtGui.QPixmap('./icons/start.ico'))
        self.btnOpen.setIcon(QtGui.QPixmap('./icons/file.jpg'))
        self.btnStop.setIcon(QtGui.QPixmap('./icons/stop.ico'))


        self.setWindowTitle("Simple Video Converter")
        self.setGeometry(100, 100, 768, 480)
        
        self.btnOpen.setFixedSize(50,30)
        self.btnStart.setFixedSize(50,30)
        self.btnStop.setFixedSize(50,30)
        self.btnClearQueue.setFixedSize(100,30)
        self.label_3.setFixedSize(90,30)
        
        self.textDest.setFixedHeight(24)
        self.textFrameRate.setFixedSize(50,24)
        self.comboPreset.setFixedSize(150,24)
        self.comboReso.setFixedSize(150,24)
        
        self.crfSlider.setMinimum(-1)
        self.crfSlider.setMaximum(52)
        self.crfSlider.setValue(18)
        self.labelCRFVal.setText('18')

        self.btnStop.setEnabled(False)
        self.listViewFormat.setFixedWidth(200)
        self.progbarCurrent.setValue(0)
        self.progbarTotal.setValue(0)
        self.add_to_listView(['avi', 'mp4', 'wmv'], self.format_list_model, False)

        
    def set_combo(self):
        for i in self.str_preset:
            self.comboPreset.addItem(i)
        self.comboPreset.setCurrentIndex(4)

        for i in self.str_reso:
            self.comboReso.addItem(i+'p')



    def convert_clicked(self):
        
        
        self.progbarTotal.setValue(0)
        self.progbarCurrent.setValue(0)
        self.progbarTotal.setMaximum(self.float_total_length)
        self.int_stop_flag = 1
        thread_conv = threading.Thread(target = self.start_convert)
        thread_conv.setDaemon(True) 
        
        thread_conv.start()
  
    
    def post_file_load(self):
        
         
        
        print('post file load')
        self.arr_file_lengths.clear()
        self.float_total_length = 0.0
        self.ffprobe_process = None
        
        for index in range(self.file_list_model.rowCount()):
    
            
            self.ffprobe_process = QProcess()

            self.ffprobe_process.readyReadStandardOutput.connect(self.read_ffprobe)
            #Get File locations from file_list_model
            self.current_file = str(self.file_list_model.item(index).data(Qt.DisplayRole))
            str_dir_loc = self.current_file.rsplit('/',1)[0] 
            self.ffprobe_process.setWorkingDirectory(str_dir_loc)
            str_file_name = self.current_file.rsplit('/',1)[-1]
            
            self.ffprobe_process.start('ffprobe -i "' + str_file_name + '" -show_entries format=duration -v quiet -of csv="p=0"')
            self.ffprobe_process.waitForFinished()
            #self.ffprobe_process.close()
        
        print(self.arr_file_lengths)
    
    
    def start_convert(self):
        
        self.ffmpeg_process = None
        self.int_index = 0
        self.signal_buttons.emit('set')
        print(self.float_total_length)
        print('reached start Convert')
        
        

        for index in range(self.file_list_model.rowCount()):
            


            if(self.int_stop_flag == 0):
                print('Breaking')
                break


                        
            self.progbarCurrent.setMaximum(self.arr_file_lengths[self.int_index])
            
            self.ffmpeg_process = QProcess()

            
            self.ffmpeg_process.readyReadStandardOutput.connect(self.read_output_err)
            #self.ffmpeg_process.readyReadStandardOutput.connect(self.read_output)

            #Get File locations from file_list_model
            self.current_file = str(self.file_list_model.item(index).data(Qt.DisplayRole))
            

            str_dir_loc = self.current_file.rsplit('/',1)[0] 
            str_file_name = self.current_file.rsplit('/',1)[-1]
            #print(str_file_name+' '+str_dir_loc)
            self.ffmpeg_process.setWorkingDirectory(str_dir_loc)
            
            str_op = '"'+ str_file_name.rsplit('.',1)[0] + self.selected_format + '"'
            str_flag = '"' + str_file_name + '"'
            str_flag += ' -preset ' + self.comboPreset.currentText()
            str_flag += ' -crf ' + self.labelCRFVal.text()
            str_flag += ' ' + str_op
            print(str_flag)
            
            arr_flag = []
            self.str_cmd = ''
            if(os.name == 'posix'):
                str_cmd = 'sh'
                arr_flag.append('-c')
                arr_flag.append('ffmpeg -i ' + str_flag + ' 2>&1')
            else:
                self.str_cmd = 'cmd.exe'
                arr_flag.append('ffmpeg -i ' + str_flag + ' 2>&1')


            #self.ffmpeg_process.start(self.str_cmd, ['-c', 'ffmpeg -i ' + str_flag + ' 2>&1'])
            self.ffmpeg_process.start(str_cmd, arr_flag)
            self.ffmpeg_process.waitForFinished()
            #self.ffmpeg_process.close()
            self.int_index += 1

        self.signal_buttons.emit('reset')
        print('Ended') 
        
    
    
    
    def read_ffprobe(self):
        
        str_op = self.ffprobe_process.readAllStandardOutput().data().decode("utf-8")
        self.float_total_length += float(str_op)
        self.arr_file_lengths.append(float(str_op))
        self.int_index += 1

        
    
    def stop(self):

        
        self.int_stop_flag = 0
        int_pid = self.ffmpeg_process.pid()
        print(int_pid)
        self.progbarCurrent.setValue(0.1)
        self.progbarTotal.setValue(0.1)

        os.system('kill ' + str(int_pid))
        self.labelFileName.setText('Process Interrupted')    
    
    
    def set_bar(self, i: float, mode: str):
        
        #Set Progress bar from the received signal
        if(mode == 'current'):
            self.progbarCurrent.setValue(i)
        else:
            self.progbarTotal.setValue(i)

    
    
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
        self.post_file_load()


   
    def read_output_err(self):
        
        #print(mode)
        #print("Reading File")
   
        str_op = self.ffmpeg_process.readAllStandardOutput().data().decode("utf-8")
        #if(self.current_file.split('.')[-1] == 'avi'):
            #str_op = self.ffmpeg_process.readAllStandardOutput().data().decode("utf-8")
    
        print(str_op)
        if ('time=' in str_op): #filter by keyword 'time'
            str_progress = str_op[str_op.index('time=') + len('time='):str_op.index('time=')+16]
            #print(str_progress)
            hh, mm, ss = str_progress.split(':')
            float_progress = (float(hh) * 3600 + float(mm) * 60)
            ss, sss = ss.split('.')
            float_progress = float_progress + (float(ss) + (float(sss)/100))
            self.signal_bar.emit(float_progress, 'current')
            self.signal_file_name.emit(self.current_file)
            #print(float_progress)
            if(self.int_index == 0):
                self.signal_bar.emit(float_progress, 'total')
            
            else:
                self.signal_bar.emit(float(self.arr_file_lengths[self.int_index-1])+float_progress, 'total')
            

   
    def read_output(self):
        
        #print(mode)
        #print("Reading File")
   
        str_op = self.ffmpeg_process.readAllStandardOutput().data().decode("utf-8")
        print(str_op)
        if ('time=' in str_op): #filter by keyword 'time'
            str_progress = str_op[str_op.index('time=') + len('time='):str_op.index('time=')+16]
            #print(str_progress)
            hh, mm, ss = str_progress.split(':')
            float_progress = (float(hh) * 3600 + float(mm) * 60)
            ss, sss = ss.split('.')
            float_progress = float_progress + (float(ss) + (float(sss)/100))
            self.signal_bar.emit(float_progress, 'current')
            self.signal_file_name.emit(self.current_file)
            #print(float_progress)
            if(self.int_index == 0):
                self.signal_bar.emit(float_progress, 'total')
            
            else:
                self.signal_bar.emit(float(self.arr_file_lengths[self.int_index-1])+float_progress, 'total')
     


    
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
        self.selected_format = '.' + sel_format
        print(self.selected_format)
    
    def clear_queue(self):
        self.file_list_model.clear()
    

    def set_label_text(self, name: str):
        self.labelFileName.setText(name)

    def slider_val(self):
        int_val = self.crfSlider.value()
        self.labelCRFVal.setText(str(int_val))


if __name__ == "__main__":
    APP = QApplication(sys.argv)
    WINDOW = VidConvertWindow()
    WINDOW.show()
    sys.exit(APP.exec_())
