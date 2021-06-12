#!/usr/bin/python3

#===============================================================================
#  Name        : vol_gui.py
#  Author      : Hamza
#  Version     : v1.0
#  Copyright   : Your copyright notice
#  Description : Gui for volatility forensics tool
#===============================================================================

import sys
import os
from PyQt5 import QtCore, QtGui, QtWidgets, uic
from PyQt5.QtWidgets import (QFileDialog) #import QFileDialog to  open files and save files
from PyQt5.QtCore import QProcess #import Qprocess
import config as cfg



form_path = os.path.join(os.path.dirname(__file__), "gui.ui")

#import configuration from config.py
profile_file = cfg.profile_file 

Ui_MainWindow, QtBaseClass = uic.loadUiType(form_path)

class MyWindow(QtWidgets.QMainWindow, Ui_MainWindow):
    def __init__(self):
        QtWidgets.QMainWindow.__init__(self)
        Ui_MainWindow.__init__(self)
        self.setupUi(self)
        self.pushButton.clicked.connect(self.load_img)
        self.pushButton_2.clicked.connect(self.execute)
        self.pushButton_3.clicked.connect(self.kill)
        self.pushButton_4.clicked.connect(self.save)
        self.pushButton_5.clicked.connect(self.dump_dir)
        self.onlyInt = QtGui.QIntValidator() # import validator
        self.lineEdit_4.setValidator(self.onlyInt) # allow numbers only
        #Set None to all varialbles 
        self.item = None
        self.pid = None
        self.dump_dir = None
        self.img_file = None
        self.pid = self.lineEdit_4.text()
        
        
    def build_profiles(self): #building profiles from .conf/profiles 
        try:
            with open(profile_file) as f:
                for profiles in f:
                    self.listWidget.addItem(profiles.strip())
        except:
            pass 
        
    
    def kill(self): #kill Qprocess
        self.p = QProcess()
        self.p.kill()

    def load_img(self): #Load memory image
        self.img_file = QFileDialog.getOpenFileName(self, 'Open Image File', r"<Default dir>", "")[0]  
        self.lineEdit.setText(self.img_file)

    
    def execute(self):
        
        try:
            self.item = self.listWidget.currentItem().text()
        except:
            pass    
        try:
            self.function = self.comboBox.currentText()
        except:
            pass
        try:
            self.pid = self.lineEdit_4.text()
        except:
            pass
            
        self.p = QProcess()
        self.p.readyReadStandardOutput.connect(self.handle_stdout)
        self.p.readyReadStandardError.connect(self.handle_stderr)
        self.p.stateChanged.connect(self.handle_state)
        
        if self.function == "imageinfo" and self.img_file != None:
            try:
                self.plainTextEdit.clear()
                self.p.start(cfg.config["python_bin"],[cfg.config["volatility_bin_loc"], "-f", self.img_file, self.function])
            except:
                self.label.setText("No memory image")
                
                
                
        elif self.function != "imageinfo" and self.img_file != None :
            if self.function == "procdump":
                if self.pid != None and self.dump_dir != None:
                    self.plainTextEdit.clear()
                    self.pid = self.lineEdit_4.text()
                    self.p.start(cfg.config["python_bin"], [cfg.config["volatility_bin_loc"], "-f", self.img_file, self.function, "--profile="+self.item, "-D", self.dump_dir, "-p", self.pid])
                else:
                    self.label.setText("Check PID or Dump Dir")
                    
                    
                    
            elif self.function == "dlllist" or self.function == "handles":
                if self.pid != None:
                    try:
                        self.plainTextEdit.clear()
                        self.pid = self.lineEdit_4.text()
                        self.p.start(cfg.config["python_bin"], [cfg.config["volatility_bin_loc"], "-f", self.img_file, self.function, "--profile="+self.item, "-p", self.pid])
                    except:
                        self.label.setText("Check PID or Profile")  
            elif self.function == "dumpregistry" or self.function == "dlldump":
                try:
                    self.plainTextEdit.clear()
                    self.pid = self.lineEdit_4.text()
                    self.p.start(cfg.config["python_bin"], [cfg.config["volatility_bin_loc"], "-f", self.img_file, self.function, "--profile="+self.item, "-D", self.dump_dir])
                except:
                    self.label.setText("Check Dump Dir or Profile")                
            
            
            else:
                try:
                    self.plainTextEdit.clear()
                    self.p.start(cfg.config["python_bin"], [cfg.config["volatility_bin_loc"], "-f", self.img_file, self.function, "--profile="+self.item])
                except:
                    self.label.setText("No Profile")
        else:
            self.label.setText("No Profile")
   
    
    def save(self): #save functionality
        try:
            name = QFileDialog.getSaveFileName(self, "Save File", r"", "")[0]
            save = self.plainTextEdit.toPlainText()
            with open(name, 'w') as f:
                f.write(save)
        except:
            pass
        
    def dump_dir(self): #Dump directory
        try:
            self.dump_dir = QFileDialog.getExistingDirectory(self)
            self.lineEdit_3.setText(self.dump_dir)
        except:
            pass
###########################################################################################     
# This section for setting stdout and stderr and state for Qprocess 
   
    def handle_stdout(self):
        data = self.p.readAllStandardOutput()
        self.stdout = bytes(data).decode("utf8")
        self.plainTextEdit.appendPlainText(self.stdout)
    
    
    def handle_stderr(self):
        data = self.p.readAllStandardError()
        stderr = bytes(data).decode("utf8")
        self.plainTextEdit.appendPlainText(stderr)
    
    def handle_state(self, state):
        states = {
            QProcess.NotRunning: 'Standby',
            QProcess.Starting: 'Starting',
            QProcess.Running: 'Running',
        }
        state_name = states[state]
        self.label.setText(state_name)
###########################################################################################  
   
if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    window = MyWindow()
    window.show()
    window.build_profiles()
    sys.exit(app.exec_())
