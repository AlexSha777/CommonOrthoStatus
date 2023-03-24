import sys
from PyQt5 import QtGui 
from PyQt5.QtCore import pyqtSignal, QRect, QVariantAnimation, QAbstractAnimation
from PyQt5.QtGui import QPixmap, QPainter, QColor, QFont, QCursor
from PyQt5.QtCore import Qt

from PyQt5.QtWidgets import (QApplication, QWidget, QScrollArea, QHBoxLayout, QVBoxLayout, 
                            QDesktopWidget, QPushButton, QDialog, QLabel, QGridLayout, QGroupBox,
                            QLineEdit, QMessageBox, QComboBox, QMenu, QAction, QScrollArea)

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





class LenghtWindow(QWidget):
    lenght_send_info = pyqtSignal()
    def __init__(self, **kwargs):
        super().__init__( **kwargs)
        
        self.initUI()

    def initUI(self):
        
        self.lineEdits_right = []
        self.labelDif = []
        self.lineEdits_left = []

        areas = ["Верхняя конечность", "Плечо" , "Предплечье", "Кисть", "ВСЕГО",
                "Нижняя конечность", "Бедро", "Голень", "Стопа",
                "ВСЕГО"]

        self.areas_names_text = ["плеча" , "предплечья", "кисти", "ВСЕГО",
                "бедра", "голени", "стопы",
                "ВСЕГО"]
        
        self.areas_names_separate_left = ["левое плечо" , "левое предплечье", "левая кисть", "ВСЕГО",
                "левое бедро", "левая голень", "левая стопа",
                "ВСЕГО"]
        
        self.areas_names_separate_right = ["правое плечо" , "правое предплечье", "правая кисть", "ВСЕГО",
                "правое бедро", "правая голень", "правая стопа",
                "ВСЕГО"]

        
        self.grid = QGridLayout(self)
       
        title = ["Справа", "Длина, см", "Разница", "Длина, см", "Слева"]
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
            if k == "Длина, см" or k == "Разница" or k == "Длина, см":
                #label.setFixedWidth(50)
                print("fixed")
            self.grid.addWidget(label,0 , column, Qt.AlignHCenter)
            column +=1

        areas_column_number = [0,4]
        for column in areas_column_number:
            row = 1
            for i in areas:
                label = QLabel()
                if row ==1 or row == 6:
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
            if row ==1 or row == 6:
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
            if row ==1 or row == 6:
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
            if row ==1 or row == 6:
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
        
        #print(self.lineEdits_right, len(self.lineEdits_right)) 
        #print(self.labelDif, len(self.labelDif))
        #print(self.lineEdits_left, len(self.lineEdits_left))
        #print(label_difference_list)

        self.Ok_button = PushButton("Ok")
        self.Ok_button.clicked.connect(self.close)
        self.cancel_button = PushButton("Cancel")
        self.cancel_button.clicked.connect(self.close)
        
        self.label_main_text = QLabel()
        self.label_main_text.setWordWrap(True)
        self.layout_label_main_text = QHBoxLayout()
        self.layout_label_main_text.addWidget(self.label_main_text)
        self.main_text = QWidget()
        self.scroll_text = QScrollArea()
        self.scroll_text.setWidgetResizable(True)
        self.group_box = QGroupBox("Текст")
        self.group_box.setLayout(self.layout_label_main_text)
        self.scroll_text.setWidget(self.group_box)

        self.group_box.setStyleSheet('''

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
        
        self.grid.addWidget(self.scroll_text, 11, 0, 1, 5)
        self.grid.addWidget(self.Ok_button , 12, 0, 1, 4)
        self.grid.addWidget(self.cancel_button , 12, 4, 1, 1)
        self.setLayout(self.grid)
        self.setWindowTitle ("Длина конечностей")
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
        
        if self.lineEdits_right[index].text() != "" and self.lineEdits_left[index].text() != "":
            radius_right = int(self.lineEdits_right[index].text())
            radius_left = int(self.lineEdits_left[index].text())
            difference = radius_right - radius_left
            label.setText(str(difference))
            self.text_formation(index = index)
        else:
            label.setText("")
            self.text_formation(index = index)

    def text_formation(self, index):
        text = ""
        row = 0
        label_dif_determined = 0
        for item in self.labelDif:
            if item.text() != "":
                label_dif_determined = 1
        
        if label_dif_determined == 1:

            if self.labelDif[7].text() !='' or self.labelDif[3].text() !='':
                if self.labelDif[3].text() !='':

                    if int(self.labelDif[3].text())>0:
                        text += "левая рука на " + self.labelDif[3].text() + " см "
                        
                        if self.labelDif[0].text()!="" and self.labelDif[1].text()!="" and self.labelDif[2].text()!="":
                            summ_hand_left = int(self.lineEdits_left[0].text()) + int(self.lineEdits_left[1].text()) + int(self.lineEdits_left[2].text())
                            summ_hand_right = int(self.lineEdits_right[0].text()) + int(self.lineEdits_right[1].text()) + int(self.lineEdits_right[2].text())
                            if summ_hand_left ==  int(self.lineEdits_left[3].text()) and summ_hand_right ==  int(self.lineEdits_right[3].text()):
                                text_details = "("
                                for item in self.labelDif[:3]:
                                    
                                    if item.text() == "0":
                                        continue
                                    else:
                                        text_details = text_details + "за счет элемента " + self.areas_names_text[self.labelDif.index(item)] + " на " + item.text() + " см, "
                                if text_details != "(":
                                    text_details = text_details[:-2] + ") "
                                    text+=text_details
                                    text_details = ""

                    elif int(self.labelDif[3].text())<0:
                        text += "правая рука на " + self.labelDif[3].text()[1:] + " см "
                        
                        if self.labelDif[0].text()!="" and self.labelDif[1].text()!="" and self.labelDif[2].text()!="":
                            summ_hand_left = int(self.lineEdits_left[0].text()) + int(self.lineEdits_left[1].text()) + int(self.lineEdits_left[2].text())
                            summ_hand_right = int(self.lineEdits_right[0].text()) + int(self.lineEdits_right[1].text()) + int(self.lineEdits_right[2].text())
                            if summ_hand_left ==  int(self.lineEdits_left[3].text()) and summ_hand_right ==  int(self.lineEdits_right[3].text()):
                                text_details = "("
                                for item in self.labelDif[:3]:
                                    if item.text() == "0":
                                        continue
                                    else:
                                        text_details = text_details +"за счет элемента " + self.areas_names_text[self.labelDif.index(item)] + " на " + item.text()[1:] + " см, "
                                if text_details != "(":
                                    text_details = text_details[:-2] + ") "
                                    text+=text_details
                                    text_details = ""

                    elif int(self.labelDif[3].text()) == 0:
                        pass
                    
                    if text[-2] ==",":
                        text = text[:-2] + "; "
                    elif text[-2] ==")":
                        text = text[:-1] + ";"
                        

                if self.labelDif[7].text() !='':
                    
                    if int(self.labelDif[7].text())>0:
                        text += "левая нога на " + self.labelDif[7].text() + " см "
                        
                        if self.labelDif[4].text()!="" and self.labelDif[5].text()!="" and self.labelDif[6].text()!="":
                            summ_hand_left = int(self.lineEdits_left[4].text()) + int(self.lineEdits_left[5].text()) + int(self.lineEdits_left[6].text())
                            summ_hand_right = int(self.lineEdits_right[4].text()) + int(self.lineEdits_right[5].text()) + int(self.lineEdits_right[6].text())
                            if summ_hand_left ==  int(self.lineEdits_left[7].text()) and summ_hand_right ==  int(self.lineEdits_right[7].text()):
                                text_details = "("
                                for item in self.labelDif[4:7]:
                                    if item.text() == "0":
                                        continue
                                    else:
                                        text_details = text_details + "за счет элемента " + self.areas_names_text[self.labelDif.index(item)] + " на " + item.text() + " см, "
                                if text_details != "(":
                                    text_details = text_details[:-2] + ") "
                                    text+=text_details
                                    text_details = ""

                    elif int(self.labelDif[7].text())<0:
                        text += "правая нога на " + self.labelDif[7].text()[1:] + " см "
                        
                        if self.labelDif[4].text()!="" and self.labelDif[5].text()!="" and self.labelDif[6].text()!="":
                            summ_hand_left = int(self.lineEdits_left[4].text()) + int(self.lineEdits_left[5].text()) + int(self.lineEdits_left[6].text())
                            summ_hand_right = int(self.lineEdits_right[4].text()) + int(self.lineEdits_right[5].text()) + int(self.lineEdits_right[6].text())
                            if summ_hand_left ==  int(self.lineEdits_left[7].text()) and summ_hand_right ==  int(self.lineEdits_right[7].text()):
                                text_details = "("
                                for item in self.labelDif[4:7]:
                                    if item.text() == "0":
                                        continue
                                    else:
                                        text_details = text_details + "за счет элемента " + self.areas_names_text[self.labelDif.index(item)] + " на " + item.text()[1:] + " см, "
                                if text_details != "(":
                                    text_details = text_details[:-2] + ") "
                                    text+=text_details
                                    text_details = ""

                    elif int(self.labelDif[7].text()) == 0:
                        pass
                
            
            index = 0
            for diff in self.labelDif:
                if diff.text() !='' and ((index in (0,1,2) and self.labelDif[3].text() =='') or
                                        (index in (4,5,6) and self.labelDif[7].text() =='')):
                    if int(diff.text())>0:
                        #self.areas_names_text = ["плеча" , "предплечья", "кисти",
                        text += self.areas_names_separate_left[index] + " на " + diff.text() + " см, "
                    elif int(diff.text())<0:
                        #self.areas_names_text = ["плеча" , "предплечья", "кисти",
                        text += self.areas_names_separate_right[index] + " на " + diff.text()[1:] + " см, "

                
                index += 1

        elif label_dif_determined == 0:
            self.label_main_text.setText("")

        if text !="":
            if text[-2] in (";", ","):
                text = text[:-2] + "."
            elif text[-2] ==")":
                text = text[:-1] + "."
        
        print(text)
        self.label_main_text.setText("Укорочены конечности: " + text)
        
        
        self.update()

            #print(item.text(), index)
    
    def get_text(self):
        return self.label_main_text.text()

    def btn_to_close(self):
        self.lenght_send_info.emit()
        self.close()

    def closeEvent(self, event):
        self.lenght_send_info.emit()
        event.accept()
        


    def close_window(self):
        self.close()