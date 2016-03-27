# coding=utf-8
import sys
from PyQt4 import QtGui, QtCore, uic
import cv2

class MyDialog(QtGui.QDialog):
    def __init__(self):
        super(MyDialog, self).__init__()
        uic.loadUi("test.ui", self)
        self.create_signal_slot()
 
        self.iscameraWorking = False
        self.isfileWorking = False
	self.ishasFile = False
        r = self.exec_()

    def create_signal_slot(self):
        self.connect(self.fileButton, QtCore.SIGNAL('clicked()'), self.onfileButton)
        self.connect(self.cameraButton, QtCore.SIGNAL('clicked()'), self.oncameraButton)
        self.connect(self.registerButton, QtCore.SIGNAL('clicked()'), self.onregisterButton)
        self.connect(self.startButton, QtCore.SIGNAL('clicked()'), self.onstartButton)


    def onfileButton(self):
        self.file_name = QtGui.QFileDialog.getOpenFileName(self, "选取文件夹" , "./")
	self.ishasFile = True
        print self.file_name

    def oncameraButton(self):
        if self.iscameraWorking == False:
            self.cameraButton.setText("CLOSE")
            self.cap = cv2.VideoCapture(0)
            self.iscameraWorking = True
            
            success,frame = self.cap.read()

            while success and self.iscameraWorking :
                success, frame = self.cap.read() #获取下一帧
                if success:
                    image = QtGui.QImage(frame.data, frame.shape[1], frame.shape[0], QtGui.QImage.Format_RGB888).rgbSwapped()
                    pixmap = QtGui.QPixmap.fromImage(image)
                    self.showlabel.setPixmap(pixmap)
                    k = cv2.waitKey(1000)
        else:
            self.cameraButton.setText("CAMERA")
            self.iscameraWorking = False
            self.cap.release()
            self.showlabel.clear()

    def onregisterButton(self):
        print "register"

    def onstartButton(self):

        if self.isfileWorking == False and self.ishasFile == True:
            self.ishasFile = False
            self.startButton.setText("CLOSE")

            self.cap = cv2.VideoCapture(self.file_name)

            self.isfileWorking = True
            
            success,frame = self.cap.read()

            while success and self.isfileWorking :
                success, frame = self.cap.read() #获取下一帧
                if success:
                    image = QtGui.QImage(frame.data, frame.shape[1], frame.shape[0], QtGui.QImage.Format_RGB888).rgbSwapped()
                    pixmap = QtGui.QPixmap.fromImage(image)
                    self.showlabel.setPixmap(pixmap)
                    k = cv2.waitKey(1000)
        else:
            self.ishasFile = False
            self.startButton.setText("START")
            self.isfileWorking = False
            self.cap.release()
            self.showlabel.clear()


if __name__ == '__main__':
    app = QtGui.QApplication(sys.argv)
    demo = MyDialog()
    #app.exec_()
