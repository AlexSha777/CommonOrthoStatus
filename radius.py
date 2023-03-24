import sys
import pickle
from PyQt5 import QtGui 
from PyQt5.QtCore import pyqtSignal, QRect, QVariantAnimation, QAbstractAnimation
from PyQt5.QtGui import QPixmap, QPainter, QColor, QFont, QCursor
from PyQt5.QtCore import Qt

from PyQt5.QtWidgets import (QApplication, QWidget, QScrollArea, QHBoxLayout, QVBoxLayout, 
                            QDesktopWidget, QPushButton, QDialog, QLabel, QGridLayout, QGroupBox,
                            QLineEdit, QMessageBox, QComboBox, QMenu, QAction)

#from modules.zone_detecting.zone_choosing import ScrollOnPicture
from zone_choosing import ScrollOnPicture, Winform

class PushButton(QPushButton):
    def __init__(self, parent=None):
        super().__init__(parent)
        self._animation = QVariantAnimation(
            startValue=QColor("#CD5C5C"),
            endValue=QColor("white"),
            valueChanged=self._on_value_changed,
            duration=400,
        )
        self._update_stylesheet(QColor("white"), QColor("black"))
        self.setCursor(QCursor(Qt.PointingHandCursor))

    def _on_value_changed(self, color):
        foreground = (
            QColor("black")
            if self._animation.direction() == QAbstractAnimation.Forward
            else QColor("white")
        )
        self._update_stylesheet(color, foreground)

    def _update_stylesheet(self, background, foreground):

        self.setStyleSheet(
            """
        QPushButton{
            background-color: %s;
            border: none;
            color: %s;
            padding: 6px 12px;
            text-align: center;
            text-decoration: none;
            font-size: 12px;
            border-radius: 8px;
            margin: 4px 2px;
            border: 2px solid #CD5C5C;
        }
        """
            % (background.name(), foreground.name())
        )

    def enterEvent(self, event):
        self._animation.setDirection(QAbstractAnimation.Backward)
        self._animation.start()
        super().enterEvent(event)

    def leaveEvent(self, event):
        self._animation.setDirection(QAbstractAnimation.Forward)
        self._animation.start()
        super().leaveEvent(event)





class RadiusWindow(QWidget):
    radius_send_info = pyqtSignal()
    def __init__(self, **kwargs):
        super().__init__( **kwargs)
        
        self.initUI()

    def initUI(self):
        
        self.lineEdits_right = []
        self.labelDif = []
        self.lineEdits_left = []

        areas = ["Верхняя конечность", "Средняя треть плеча" , "Нижняя треть плеча", "Верхняя треть предплечья", 
                "Средняя треть предплечья", "Нижняя треть предплечья",
                "Нижняя конечность", "Вержняя треть бедра", "Средняя треть бедра", "Нижняя треть бедра",
                "Верхняя треть голени", "Средняя треть голени", "Нижняя треть голени"]

        self.areas_names_text = ["Средняя треть плеча" , "Нижняя треть плеча", "Верхняя треть предплечья", 
                "Средняя треть предплечья", "Нижняя треть предплечья", "Вержняя треть бедра", "Средняя треть бедра", 
                "Нижняя треть бедра", "Верхняя треть голени", "Средняя треть голени", "Нижняя треть голени"]

        
        self.grid = QGridLayout(self)
       
        title = ["Справа", "Окружность, см", "Разница", "Окружность, см", "Слева"]
        column = 0
        for k in title:
            label = QLabel()
            label.setStyleSheet("""
                QLabel {
                    background-color: #CD5C5C; 
                    color: white; 
                    border-style: outset;
                    border-width: 2px;
                    border-radius: 10px;
                    border-color: beige;
                    font: bold 14px;
                    
                    padding: 6px;
                }
                """)

            label.setText(k)
            if k == "Окружность, см" or k == "Разница" or k == "Окружность, см":
                #label.setFixedWidth(50)
                print("fixed")
            self.grid.addWidget(label,0 , column, Qt.AlignHCenter)
            column +=1

        areas_column_number = [0,4]
        for column in areas_column_number:
            row = 1
            for i in areas:
                label = QLabel()
                if row ==1 or row == 7:
                    label.setStyleSheet('''QLabel {
                        background-color: #FA8072; 
                        color: black; 
                        border-style: groove;
                        border-width: 2px;
                        border-radius: 10px;
                        border-color: beige;
                        font: bold 14px;
                        min-width: 10em;
                        padding: 6px;
                    }
                    ''')
                else:
                    label.setStyleSheet('''QLabel {
                        background-color: #FFA07A; 
                        color: black; 
                        border-style: groove;
                        border-width: 2px;
                        border-radius: 10px;
                        border-color: beige;
                        font: bold 14px;
                        min-width: 10em;
                        padding: 6px;
                    }
                    ''')
                label.setText(i)
                self.grid.addWidget(label,row , column, Qt.AlignHCenter)
                row += 1

        row = 1
        for i in range(len(areas)):
            if row ==1 or row == 7:
                row +=1
            else:
                line_edit = QLineEdit()
                line_edit.setMaxLength(2)
                line_edit.setStyleSheet('''QLineEdit {
                    border-style: groove;
                    border-width: 2px;
                    border-radius: 10px;
                    border-color: #FFA07A;
                    font: bold 14px;
                    
                    padding: 6px;
                }
                ''')
                line_edit.setObjectName("line_edit_right"+"_"+str(row))
                line_edit.setValidator(QtGui.QIntValidator(0, 100))
                self.lineEdits_right.append(line_edit)
                line_edit_obj = line_edit.objectName()
                line_edit.setFixedWidth(50)
                line_edit.textChanged.connect(self.calculate_dif)
                self.grid.addWidget(line_edit,row , 1, Qt.AlignHCenter)
                row += 1

        row = 1
        label_difference_list = []
        for i in range(len(areas)):
            if row ==1 or row == 7:
                row +=1
            else:
                label_difference = QLabel()
                label_difference.setObjectName("label_dif"+"_"+str(row))
                label_difference_list.append(label_difference.objectName())
                label_difference.setStyleSheet('''QLabel {
                    
                    color: #FF8C00; 
                    font: bold 16px;
                    
                    padding: 6px;
                }
                ''')
                label_difference.setFixedWidth(50)
                self.labelDif.append(label_difference)
                self.grid.addWidget(label_difference,row , 2, Qt.AlignHCenter)
                row += 1

        row = 1
        for i in range(len(areas)):
            if row ==1 or row == 7:
                row +=1
            else:
                line_edit_L = QLineEdit()
                line_edit_L.setMaxLength(2)
                line_edit_L.setStyleSheet('''QLineEdit {
                    border-style: groove;
                    border-width: 2px;
                    border-radius: 10px;
                    border-color: #FFA07A;
                    font: bold 14px;
                    
                    padding: 6px;
                }
                ''')
                line_edit_L.setObjectName("line_edit_left"+"_"+str(row))
                self.lineEdits_left.append(line_edit_L)
                line_edit_L.setFixedWidth(50)
                line_edit_L.textChanged.connect(self.calculate_dif)
                self.grid.addWidget(line_edit_L,row , 3, Qt.AlignHCenter)
                row += 1
        

        #self.grid.addLayout(self.vbox_right_scroll, 0 , 1)
        #self.grid.setColumnMinimumWidth(0, self.picture.width()+40)
        #self.grid.setColumnMinimumWidth(1, (self.picture.width()+40)/3)
        #self.grid.setColumnStretch(1, 0.5)
        print(self.lineEdits_right, len(self.lineEdits_right)) 
        print(self.labelDif, len(self.labelDif))
        print(self.lineEdits_left, len(self.lineEdits_left))
        print(label_difference_list)

        self.Ok_button = PushButton("Ok")
        self.Ok_button.clicked.connect(self.btn_to_close)
        self.label_main_text = QLabel()
        self.label_main_text.setWordWrap(True)
        self.layout_label_main_text = QHBoxLayout()
        self.layout_label_main_text.addWidget(self.label_main_text)
        self.main_text = QGroupBox("Текст")
        self.main_text.setLayout(self.layout_label_main_text)

        self.main_text.setStyleSheet('''

            QGroupBox {margin-top: 2ex;
            }
            QGroupBox:enabled {
                border: 3px solid #CD5C5C;
                border-radius: 5px;
            }
            QGroupBox::title {
                subcontrol-origin: margin;
                left: 3ex;
            }
        ''')
        
        self.grid.addWidget(self.main_text , 14, 0, 1, 5)
        self.grid.addWidget(self.Ok_button , 15, 0, 1, 5)
        self.setLayout(self.grid)
        self.setWindowTitle ("Окружность конечностей")
        self.show()

    def calculate_dif(self, text):
        print(self.sender().objectName())
        if self.sender() in self.lineEdits_right:
            index = self.lineEdits_right.index(self.sender())
        elif self.sender() in self.lineEdits_left:
            index = self.lineEdits_left.index(self.sender())
        
        print(self.sender())
        print(index)
        self.label_difference_update(index=index)
        #print(text)

    def label_difference_update(self, index):
        label = self.labelDif[index]
        print(label)
        
        if self.lineEdits_right[index].text() and self.lineEdits_left[index].text():
            radius_right = int(self.lineEdits_right[index].text())
            radius_left = int(self.lineEdits_left[index].text())
            difference = radius_right - radius_left
            label.setText(str(difference))
            self.text_formation(index = index)

    def text_formation(self, index):
        self.label_main_text.setText("Уменьшена окружность конечностей:")
        for item in self.labelDif:
            if item.text() and int(item.text())>0:
                text = " " + (self.areas_names_text[self.labelDif.index(item)]).lower() + " слева на " + item.text() + " см,"
                self.label_main_text.setText(self.label_main_text.text()+text)
            elif item.text() and int(item.text())<0:
                text = " " + (self.areas_names_text[self.labelDif.index(item)]).lower() + " справа на " + item.text()[1:] + " см,"
                self.label_main_text.setText(self.label_main_text.text()+text)
                

            #print(item.text(), index)
    
    def get_radius_text(self):
        text = self.label_main_text.text()
        if text != "":
            text = text[:-1] + "."
        return text

    def closeEvent(self, e):
        print("closeEvent")
        self.radius_send_info.emit()
        self.close()
        self.setParent(None)

    def btn_to_close(self):
       # name = "modules/radius_text"
        #text = self.label_main_text.text()
        #if text != "":
        #    text = text[:-1] + "."
        
        #with open(name + '.pkl', 'wb') as f:
        #    pickle.dump(text, f, pickle.HIGHEST_PROTOCOL)
        self.radius_send_info.emit()
        self.close()
        return self.label_main_text.text()

    def close_window(self):
        self.radius_send_info.emit()
        self.close()
        self.setParent(None)


    

if __name__ == "__main__":
    app = QApplication(sys.argv)
    
    form = EdemaWindow()
    form.show()
    sys.exit(app.exec_())