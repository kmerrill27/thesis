import sys
from PyQt4 import QtGui

def get_pil_image(w, h):
    clr = chr(0)+chr(255)+chr(0)
    im = Image.fromstring("RGB", (w,h), clr*(w*h))
    return im

def pil2qpixmap(pil_image):
    w, h = pil_image.size
    data = pil_image.tostring("raw", "BGRX")
    qimage = QtGui.QImage(data, w, h, QtGui.QImage.Format_RGB32)
    qpixmap = QtGui.QPixmap(w,h)
    pix = QtGui.QPixmap.fromImage(qimage)
    return pix

class ImageLabel(QtGui.QLabel):
    def __init__(self, parent=None):
        QtGui.QLabel.__init__(self, parent)

        self.setGeometry(300, 300, 250, 150)
        self.setWindowTitle('Window')

        self.pix = pil2qpixmap(get_pil_image(50,50))
        self.setPixmap(self.pix)

app = QtGui.QApplication(sys.argv)
imageLabel = ImageLabel()
imageLabel.show()
sys.exit(app.exec_())
