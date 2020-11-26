import sys
from PyQt5 import QtGui, QtCore
from PyQt5.QtWidgets import QWidget,QApplication
from urllib.request import urlopen

class myApplication(QWidget):
    def __init__(self, parent=None):
        super(myApplication, self).__init__(parent)

        #---- Prepare a Pixmap ----

        url = ('../Ressources/auigille.png')
        url = ('https://i.stack.imgur.com/6R42h.png')
        
        self.img = QtGui.QImage()


        pixmap = QtGui.QPixmap(self.img)

        #---- Embed Pixmap in a QLabel ----

        diag = (pixmap.width()**2 + pixmap.height()**2)**0.5

        self.label = QtGui.QLabel()
        self.label.setMinimumSize(diag, diag)
        self.label.setAlignment(QtCore.Qt.AlignCenter)
        self.label.setPixmap(pixmap)

        #---- Prepare a Layout ----

        grid = QtGui.QGridLayout()

        button = QtGui.QPushButton('Rotate 15 degrees')
        button.clicked.connect(self.rotate_pixmap)

        grid.addWidget(self.label, 0, 0)
        grid.addWidget(button, 1, 0)

        self.setLayout(grid)

        self.rotation = 0

    def rotate_pixmap(self):

        #---- rotate ----

        # Rotate from initial image to avoid cumulative deformation from
        # transformation

        pixmap = QtGui.QPixmap(self.img)
        self.rotation += 15

        transform = QtGui.QTransform().rotate(self.rotation)
        pixmap = pixmap.transformed(transform, QtCore.Qt.SmoothTransformation)

        #---- update label ----

        self.label.setPixmap(pixmap)

if __name__ == '__main__':

    app = QApplication(sys.argv)

    instance = myApplication()  
    instance.show()    

    sys.exit(app.exec_())