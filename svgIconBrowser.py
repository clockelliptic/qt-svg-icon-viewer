import os

import numpy as np
from matplotlib import cm
from matplotlib.pyplot import colormaps as mpl_cmaps

from PyQt5.QtGui import QPalette, QColor, QFont, qRgba, QIcon, QPainter, QImage, QPixmap
from PyQt5.QtSvg import QSvgRenderer
from PyQt5.QtCore import Qt, QFile, QTextStream, QSize, QFileInfo, QByteArray, pyqtSignal
from PyQt5.QtWidgets import (QApplication, QGridLayout, QHBoxLayout, QLayout, QLineEdit,
                             QSizePolicy, QToolButton, QWidget, QLabel, QCheckBox,
                             QTableView, QTableWidget, QTableWidgetItem, QToolBar,
                             QToolBox, QWidget, QPushButton, QScrollArea, QVBoxLayout)

# stylesheet
import breeze_resources

#TODO: CustomSVGIcons
# Parse SVG icon files, set a custom fill color, and yield a button with each icon
class CustomSVGIcons():
    def __init__(self):
        root = QFileInfo(__file__).absolutePath()

        svg_files = os.listdir(root+"/icons/svg/")

        self.images = {}

        for filename in svg_files:
            f = QFile(root+'/icons/svg/'+filename)
            if f.open(QFile.ReadOnly | QFile.Text):
                textStream = QTextStream(f)
                svgData = textStream.readAll().replace('fill="#000000"', 'fill="#eeeeee"')
                svgData_hover = svgData.replace('fill="#eeeeee"', 'fill="#3daee9"')
                f.close()

            svg = QSvgRenderer(QByteArray().append(svgData))
            svg_hover = QSvgRenderer(QByteArray().append(svgData_hover))

            qim = QImage(76, 76, QImage.Format_RGBA8888)
            qim.fill(0)
            painter = QPainter()
            painter.begin(qim)
            svg.render(painter)
            painter.end()

            qim_hover = QImage(76, 76, QImage.Format_ARGB32)
            qim_hover.fill(0)
            painter = QPainter()
            painter.begin(qim_hover)
            svg_hover.render(painter)
            painter.end()

            self.images[filename.replace("appbar.","").replace(".svg","")] = (QIcon(QPixmap.fromImage( qim )),
                                                                              QIcon(QPixmap.fromImage( qim_hover )))

    def do(self):
        return self.images

#ANCHOR: BigMiniButton
class BigMiniButton(QToolButton):
    mouseHover = pyqtSignal(bool)

    def __init__(self, text, icon, hovericon, parent, onClicked):
        super(BigMiniButton, self).__init__(parent)
        self.icon = icon
        self.hovericon = hovericon

        self.clicked.connect(onClicked)
        self.setIcon(self.icon)
        self.setText(text)
        self.setFixedSize(48, 48)

        self.setStyleSheet('''
                            BigMiniButton
                            {
                                color: #eeeeee;
                                background-color: transparent;
                                border: 0ex solid #3daee9;
                                margin: 0ex;
                                padding: 0ex;
                                icon-size:48px 48px;
                            }

                            BigMiniButton:hover
                            {
                            background-color: rgba(0,0,0,0.1);
                            color: #3daee9;
                            }

                            BigMiniButton:pressed
                            {
                            background-color: rgba(0,0,0,0.2);
                            }
                            ''')
        self.setToolButtonStyle(Qt.ToolButtonTextUnderIcon)
        self.setMinimumSize(75, 75)

    def enterEvent(self, event):
        self.mouseHover.emit(True)
        self.setIcon(self.hovericon)

    def leaveEvent(self, event):
        self.mouseHover.emit(False)
        self.setIcon(self.icon)

#ANCHOR: Main app
class CalculatorApp(QWidget):
    def __init__(self, parent=None):
        super(CalculatorApp, self).__init__()

        buttonGrid = QGridLayout()
        buttonGridContainer = QWidget()
        buttonGridContainer.setSizePolicy(QSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding))
        buttonGridContainer.setLayout(buttonGrid)
        self.setStyleSheet("QScrollArea {border: none;}")

        scrollarea = QScrollArea()
        scrollarea.setWidget(buttonGridContainer)
        scrollarea.setWidgetResizable(True)

        icon_dict = CustomSVGIcons().do()

        buttons = []

        for n, i in enumerate(icon_dict.keys()):
                button = BigMiniButton(i, icon=icon_dict[i][0],
                                       hovericon=icon_dict[i][1],
                                       parent = self,
                                       onClicked = self.handleButtonClick)
                button.setToolTip(i)
                buttonGrid.addWidget(button, n//15, n%15)

        mainLayout = QVBoxLayout(self)
        mainLayout.addWidget(scrollarea)
        self.setWindowIcon(icon_dict["calculator"][0])

    def handleButtonClick(self):
        pass

if __name__ == '__main__':

    import sys

    app = QApplication(sys.argv)

    # set stylesheet
    file = QFile(":/dark.qss")
    file.open(QFile.ReadOnly | QFile.Text)
    stream = QTextStream(file)
    app.setStyleSheet(stream.readAll())

    calc = CalculatorApp()
    calc.show()
    sys.exit(app.exec_())

    del calc