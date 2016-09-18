import sys
import subprocess
import os
import time
from TesterInterface import *
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import (QMainWindow, QTextEdit, QAction, QFileDialog, QApplication)
from PyQt5.QtGui import QIcon

 
class TesterInt(QtWidgets.QMainWindow):
   
    def __init__(self, parent=None):
        QtWidgets.QWidget.__init__(self, parent)
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        self.ui.pushButton.clicked.connect(self.TestScripts)
        self.ui.toolButton.clicked.connect(self.GetDirectory)
        self.DIR = ""


    #Устанавливаем директорию в которой будем проверять скрипты
    def GetDirectory(self):        
        self.DIR = QFileDialog.getExistingDirectory(self, "Open Directory", "/home")
        self.ui.lineEdit.setText(self.DIR)
    #Проверяем все скрипты на python в выбранной директории
    def TestScripts(self):
        self.ui.textEdit.clear()
        flag = True
        
        try:
            if len(self.ui.lineEdit_2.text()) != 0:
                Timeout_time = int(float(self.ui.lineEdit_2.text()))
            else:
                Timeout_time = 0

            flag = True

        except ValueError:
            self.ui.textEdit.setText("You should not print anything but integer in Timeout box!")
            flag = False
        

        if flag:
            if self.DIR == "":
                self.ui.textEdit.setText("Choose Directory")
            else:
                files_list = os.listdir(path = self.DIR)
                scripts_list = list()
                for x in files_list:
                    if x[-3:] == ".py":
                        scripts_list.append(x) #Выбираем из директории файлы с разрешением .py

                if len(scripts_list)==0:
                    self.ui.textEdit.setText("No scripts in choosen directory")

                else:
                    sucsessful_tests = 0
                    for fnames in scripts_list:
                        DIR=self.DIR+'/'+fnames
                        self.ui.textEdit.append(DIR + ":")#Выводим название тестриуемого файла
                        try:
                            proc = subprocess.Popen(['python', DIR], stderr=subprocess.PIPE, stdin=subprocess.PIPE, universal_newlines=True)
                            outs, errs = proc.communicate(timeout=Timeout_time)#Если процесс висит больше Timeout_time секунд - принудительно убиваем его
                            if str(proc.returncode) == "0":
                                self.ui.textEdit.append("Status: OK\n")#Если в процессе исполнения не было выявленно никаких необработанных
                                sucsessful_tests += 1                  #исключений или ошибок - отмечает тест пройденным успешно
                            else:
                                self.ui.textEdit.append("Status: Failed - Return code: " + str(proc.returncode) + " - Error: " + errs + "\n")#Не уверен, что эта строчка необходима, теоретически если returncode!=0 subprocess должен инициировать исключение, обработчик которого описан ниже
                        except subprocess.TimeoutExpired:
                            proc.kill()
                            #self.ui.textEdit.append("must be terminated")
                            outs, errs = proc.communicate()
                            if len(errs)==0:
                                addition=""
                            else:
                                addition=" + "
                            self.ui.textEdit.append("Status: Failed - Return code: " + str(proc.returncode) + " - Error: Timeout Expired" + addition + errs + "\n")

                        except subprocess.SubprocessError:
                            proc.kill()
                            outs, errs = proc.communicate()
                            self.ui.textEdit.append("Status: Failed - Return code: " + str(proc.returncode) + errs + "\n")


                    #Подсчитываем количество удачно пройденных тестов
                    self.ui.textEdit.append("Scripts in folder: " + str(len(scripts_list)) + " - " + "Sucsessful tests: " + str(sucsessful_tests)+"\n")
             
            
        
         
        
    
if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    myapp = TesterInt()
    myapp.show()
    sys.exit(app.exec_())
