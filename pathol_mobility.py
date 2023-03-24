import sys
import time

from PyQt5 import QtGui 
from PyQt5.QtCore import pyqtSignal, QRect, QVariantAnimation, QAbstractAnimation, QEasingCurve, Qt, QPropertyAnimation, pyqtProperty
from PyQt5.QtGui import QPixmap, QPainter, QColor, QFont, QCursor

from PyQt5.QtWidgets import (QApplication, QWidget, QScrollArea, QHBoxLayout, QVBoxLayout, 
                            QDesktopWidget, QPushButton, QDialog, QLabel, QGridLayout, QGroupBox,
                            QLineEdit, QMessageBox, QComboBox, QMenu, QAction, QScrollArea, QSizePolicy)

#from modules.zone_detecting.zone_choosing import ScrollOnPicture
from zone_choosing import ScrollOnPicture, Winform

class PushButton(QPushButton):
    

    def __init__(self, parent=None,font_size=None):
        super().__init__(parent)

        self._color = "#ffb4a2"
        self._color_new = "#A64A35"
        if font_size == None:
            self._font_size = 14
        else:
            self._font_size = font_size
        self.setCursor(QCursor(Qt.PointingHandCursor))
        self._update_stylesheet(QColor(self._color), QColor("#000000"))
        
        self._animation = QVariantAnimation(
            startValue=QColor(self._color_new),
            endValue=QColor(self._color),
            valueChanged=self._on_value_changed,
            duration=400,
        )

    @pyqtProperty(str)
    def color(self):
        return self._color

    @color.setter
    def color(self, value):
        self._color = value
        color_new = ""
        if value == "#f0f0f0": 
            color_new = "#B4B4B4"
        elif value == "#adff2f":
            color_new = "#91BF4A"
        elif value =="#ffb4a2":
            color_new = "#A64A35"

        elif value =="#A64A35":
            color_new = "#ffb4a2"

        elif value =="":
            color_new = ""
        elif value == "#fa8090":
            color_new = "#A32A3A"
        elif value == "#F59AB2":
            color_new = "#9F324F"

        elif value == "#FF7373":
            color_new = "#BF3030"

        elif value == "#FF4040":
            color_new = "#BF3030"

        elif value == "#BF3030":
            color_new = "#FF7373"


        self._color_new = color_new
        self._update_stylesheet(QColor(self._color),QColor("black"))
        #self.setSizePolicy(30, 60)#QSizePolicy.Fixed)

    @pyqtProperty(str)
    def color_new(self):
        return self._color_new

    @color_new.setter
    def color_new(self, color):
        if color == "#f0f0f0": 
            color_new = "#B4B4B4"
        elif color == "#adff2f":
            color_new = "#91BF4A"
        elif color =="#ffb4a2":
            color_new = "#A64A35"
        elif color =="":
            color_new = ""
        self._color_new = color_new

    def setColor (self, color):
        return color

    @pyqtProperty(int)
    def font_size(self):
        return self._font_size

    @font_size.setter
    def font_size(self, font_size):
        self._font_size = font_size

    def getColor (self):
        return self.color_main

    def _on_value_changed(self):
        foreground = (
            QColor("black")
            if self._animation.direction() == QAbstractAnimation.Forward
            else QColor("white")
        )
        background = (
            QColor(self._color)
            if self._animation.direction() == QAbstractAnimation.Forward
            else QColor(self._color_new)
            )
        self._update_stylesheet(background, foreground)


    def _update_stylesheet(self, background, foreground):

        self.setStyleSheet(
            """
        QPushButton{
            background-color: %s;
            border: none;
            color: %s;
            padding: 4px 4px 4px 4px;
            text-align: center;
            text-decoration: none;
            font-size: %spx;
            border-radius: 8px;
            margin: 4px 4px 4px 4px;
            min-height: 20 px;
            
        }
        """
            % (background.name(), foreground.name(), self._font_size)
        )

    def enterEvent(self, event):
        self._animation.setDirection(QAbstractAnimation.Backward)
        self._animation.start()
        super().enterEvent(event)

    def leaveEvent(self, event):
        self._animation.setDirection(QAbstractAnimation.Forward)
        self._animation.start()
        super().leaveEvent(event)

class ComboWidget(QLabel):
    #combo_widget_closing = pyqtProperty()
    def __init__(self, parent=None, size=None):
        super().__init__(parent)
        self.setStyleSheet(
            '''
                background-color: #FFC2C2;
                color: black;
                padding: 2px 2px 2px 2px;
                text-align: center;
                border-radius: 4px;
                margin: 2px 2px 2px 2px;
                border: 2px solid #A64A35;
            ''')


class PatholMobilWindow(QWidget):
    patholmobil_send_info = pyqtSignal()
    def __init__(self, **kwargs):
        super().__init__( **kwargs)

        self.initUI()

    def initUI(self):
        
        self.degree_sign = u'\N{DEGREE SIGN}'
        self.lineEdits_right = []
        self.labelDif = []
        self.lineEdits_left = []
        self.button_detail_right = []
        self.button_detail_left = []
        self.button_entered = []
        self.button_pressed = ""
        self.button_all = []
        self.combo_box_new = None
        self.button_axis = []
        self.button_degree = []

        areas = ["Верхняя конечность", "Плечо" , "Локтевой сустав", "Предплечье", "Лучезапястный сустав", 
                "Нижняя конечность", "Бедро","Коленный сустав", "Голень", "Голеностопный сустав"]

        self.deform_directions = ["НЕТ","вальгус","варус","антекурвация","рекурвация", "вальгус-антекурвация",
                                "варус-антекурвация","вальгус-рекурвация","варус-рекурвация"]



        self.areas_names_text = ["плеча" , "предплечья", "кисти", "ВСЕГО",
                "бедра", "голени", "стопы",
                "ВСЕГО"]
        
        self.areas_names_separate_left = ["левое плечо" , "левое предплечье", "левая кисть", "ВСЕГО",
                "левое бедро", "левая голень", "левая стопа",
                "ВСЕГО"]
        
        self.areas_names_separate_right = ["правое плечо" , "правое предплечье", "правая кисть", "ВСЕГО",
                "правое бедро", "правая голень", "правая стопа",
                "ВСЕГО"]

        self.localize = {
            "20": "верхней трети плеча",
            "21": "средней трети плеча",
            "22": "нижней трети плеча",
            "_3": "локтевого сустава",
            "40": "верхней трети предплечья",
            "41": "средней трети предплечья",
            "42": "нижней трети предплечья",
            "_5": "лучезапястного сустава",
            "70": "верхней трети бедра",
            "71": "средней трети бедра",
            "72": "нижней трети бедра",
            "_8": "коленного сустава",
            "90": "верхней трети голени",
            "91": "средней трети голени",
            "92": "нижней трети голени",
            "10": "голеностопного сустава",
        }
        self.grid = QGridLayout(self)
       
        title = ["Справа","Слева"]
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

            self.grid.addWidget(label,0 , column, 1, 2, Qt.AlignHCenter)
            column +=2

        areas_column_number = [0,2]
        for column in areas_column_number:
            row = 1
            for i in areas:
                
                if row ==1 or row ==6 :
                    label = QLabel()
                    label.setText(i)
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
                    self.grid.addWidget(label,row , column, 1, 2, Qt.AlignHCenter)
                elif row  in (2,4,7,9):
                    label = QLabel()
                    label.setText(i)
                    label.setStyleSheet('''QLabel {
                        background-color: white; 
                        color: black; 
                        border-style: groove;
                        border-width: 2px;
                        border-radius: 10px;
                        border-color: beige;
                        font: bold 14px;
                        padding: 3px;
                    }
                    ''')
                    self.grid.addWidget(label,row , column, Qt.AlignHCenter)
                elif row  in (3,5,8,10):
                    button_artic = PushButton(i)

                    if column ==0:
                        button_artic.setObjectName("but_det_right"+"_"+str(row))
                        self.button_all.append(button_artic)
                    else:
                        button_artic.setObjectName("but_det_left"+"_"+str(row))
                        self.button_all.append(button_artic)

                    button_artic.clicked.connect(self.but_detail_process)
                    self.grid.addWidget(button_artic, row, column, 1, 2)
                row += 1

        for column in (1,3):
            row = 1
            for i in range(len(areas)):
                if row in (1,3,5,6,8,10):
                    row +=1
                else:
                    inc = 0
                    lay_out = QVBoxLayout()
                    for level_name in ("верхняя треть", "средняя треть", "нижняя треть"):
                        button = PushButton(level_name)
                        self.button_all.append(button)
                        button.clicked.connect(self.but_detail_process)
                        lay_out.addWidget(button)
                        if column ==1:
                            button.setObjectName("but_det_right"+"_"+str(row)+str(inc))
                            self.button_detail_right.append(button)
                        else:
                            button.setObjectName("but_det_left"+"_"+str(row)+str(inc))
                            self.button_detail_left.append(button)
                        inc+=1
                        
                    self.grid.addLayout(lay_out,row , column, Qt.AlignHCenter)
                    row += 1

        self.Ok_button = PushButton("Ok")
        self.Ok_button.clicked.connect(self.closeEvent)
        self.cancel_button = PushButton("Cancel")
        self.cancel_button.clicked.connect(self.delete_close)
        
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
        
        self.grid.addWidget(self.scroll_text, 11, 0, 1, 4)
        self.grid.addWidget(self.Ok_button , 12, 0, 1, 3)
        self.grid.addWidget(self.cancel_button , 12, 3, 1, 1)
        self.setLayout(self.grid)
        screen = (QDesktopWidget().availableGeometry().width(), QDesktopWidget().availableGeometry().height())
        print(screen)
        print(self.height())
        
        self.setWindowTitle ("Патологическая подвижность на протяжении конечностей")
        self.show()
        self.move(300,(screen[1]-self.height())/2)

        print("lenht=%s" %len(self.button_all))
        for but in self.button_all:
            if but.objectName() == "but_det_right_3":
                self.combo_width = but.width()
        self.size_after_show = (self.width(),self.height())
        print(self.size_after_show)


    def but_detail_process(self):
        but_name = self.sender().objectName()
        x_coord = self.sender().x()
        y_coord = self.sender().y()

        print(x_coord)
        print(y_coord)
        print(but_name)

        if self.combo_box_new == None:
            
            self.deform_directions = ["фронтальная","сагитальная","горизонтальная","многоплоск-ая"]
            self.deform_directions_but = []
            self.deform_degree = ["5","10","15","20","25","30","35"]
            self.deform_degree_but = []
            combo_layout = QGridLayout()
            combo_axis_layout = QVBoxLayout()
            combo_degree_layout = QVBoxLayout()
            
            for item in self.deform_directions:
                button_combo = PushButton(item, font_size=12)
                button_combo.color = "#FF7373"
                button_combo.clicked.connect(self.combo_box_def_direction)
                self.deform_directions_but.append(button_combo)
                combo_axis_layout.addWidget(button_combo)
                combo_axis_layout.addSpacing(100)
            
            for item in self.deform_degree:
                button_combo = PushButton(item, font_size=12)
                button_combo.color = "#FF7373"
                button_combo.clicked.connect(self.combo_box_def_direction)
                self.deform_degree_but.append(button_combo)
                combo_degree_layout.addWidget(button_combo)
            label_ax = QLabel("Плоскость")
            label_ax.setAlignment(Qt.AlignHCenter)
            label_ax.setStyleSheet(
            '''
                background-color: #FF9898;
                color: black;
                padding: 2px 2px 2px 2px;
                text-align: center;
                font-size: 14px;
                border-radius: 4px;
                margin: 2px 2px 2px 2px;
            ''')
            label_degree = QLabel("Величина")
            label_degree.setAlignment(Qt.AlignHCenter)
            label_degree.setStyleSheet(
            '''
                background-color: #FF9898;
                color: black;
                padding: 2px 2px 2px 2px;
                text-align: center;
                font-size: 14px;
                border-radius: 4px;
                margin: 2px 2px 2px 2px;
            ''')
            cancel_combo = PushButton("Cancel")
            cancel_combo.color = "#BF3030"
            cancel_combo.clicked.connect(self.combo_box_def_direction)
            combo_layout.addWidget(label_ax,0, 0)
            combo_layout.addWidget(label_degree, 0, 1)
            combo_layout.addLayout(combo_axis_layout, 1, 0)
            combo_layout.addLayout(combo_degree_layout, 1, 1)
            combo_layout.addWidget(cancel_combo, 2, 0, 1, 2)
            self.combo_box_new = ComboWidget(self)
            self.combo_box_new.setLayout(combo_layout)
            self.combo_box_new.show()
            self.combo_box_new.resize(self.combo_width, self.sender().size().height()*9)
            if but_name[:12]=="but_det_left" and but_name[-2] in ("2","4","7","9"):
                print("different move")
                if but_name[-2:] in ["_8", "90", "91", "92", "10"]:
                    self.combo_box_new.move(x_coord+self.sender().width()-self.combo_box_new.width(), y_coord - self.combo_box_new.height())
                else:
                    self.combo_box_new.move(x_coord+self.sender().width()-self.combo_box_new.width(), y_coord + self.sender().height())

            else:
                if but_name[-2:] in ["_8", "90", "91", "92", "10"]:
                    self.combo_box_new.move(x_coord, y_coord - self.combo_box_new.height())
                else:
                    self.combo_box_new.move(x_coord, y_coord + self.sender().height())

            initial_rect = self.combo_box_new.geometry()
            final_rect = QRect(self.combo_box_new.x(),self.combo_box_new.y(),1,1)

            final_rect_down = QRect(self.combo_box_new.x()+self.combo_box_new.width(),self.combo_box_new.y()+self.combo_box_new.height(),1,1)
            
            print("final_rect=%s" % final_rect)

            self.combo_animation = QPropertyAnimation(self.combo_box_new, b'geometry')
            self.combo_animation.setEasingCurve(QEasingCurve.InOutSine)
            self.combo_animation.setDuration(300)
            self.combo_animation.setStartValue(initial_rect)
            self.combo_animation.setEndValue(final_rect)

            self.combo_animation_down = QPropertyAnimation(self.combo_box_new, b'geometry')
            self.combo_animation_down.setEasingCurve(QEasingCurve.InOutSine)
            self.combo_animation_down.setDuration(300)
            self.combo_animation_down.setStartValue(initial_rect)
            self.combo_animation_down.setEndValue(final_rect_down)

            if but_name[-2:] in ["_8", "90", "91", "92", "10"]:
                self.combo_animation_down.setDirection(QAbstractAnimation.Backward)
                self.combo_animation_down.start()
            else:
                self.combo_animation.setDirection(QAbstractAnimation.Backward)
                self.combo_animation.start()

            self.button_pressed = self.sender()
            self.button_pressed.color = "#A64A35"

        else:
            msg = QMessageBox()
            msg.setWindowTitle("Информация")
            msg.setText("Закончите введение вида деформации!!!")
            msg.setIcon(QMessageBox.Information)
            center = (self.geometry().center().x(), self.geometry().center().y())
            msg.show()
            msg.move(center[0]-(msg.size().width()/2), center[1]+(msg.size().height()/2))
            msg.exec_()


    def combo_box_def_direction(self, index=None):
        text = self.sender().text()
        print(text)
        print(self.button_entered)
        print("self.button_pressed=%s" %self.button_pressed)
        text_axis = ""
        text_degree = ""
        if text in ["фронтальная","сагитальная","горизонтальная","многоплоск-ая"]:
            self.button_axis = [self.sender()]
            text_axis = text
            for item in self.deform_directions_but: item.color = "#FF7373"
            self.sender().color = "#BF3030"

        elif text in ["5","10","15","20","25","30","35"]:
            self.button_degree = [self.sender()]
            text_degree = text
            for item in self.deform_degree_but: item.color = "#FF7373"
            self.sender().color = "#BF3030"


        if self.sender().text() != "Cancel":
            inc = 0
            to_add_new_but = True
            for item in self.button_entered:
                if item[0] == self.button_pressed:
                    if text_axis != "":
                        self.button_entered[inc][0] = self.button_pressed
                        self.button_entered[inc][1]["axis"] = text_axis
                    elif text_degree != "":
                        self.button_entered[inc][0] = self.button_pressed
                        self.button_entered[inc][1]["degree"] = text_degree
                    
                    to_add_new_but = False
                inc+=1
            if to_add_new_but != False:
                print (to_add_new_but)
                if text_axis != "":
                    self.button_entered.append([self.button_pressed, {"axis": text_axis, "degree": ""}])
                elif text_degree != "":
                    self.button_entered.append([self.button_pressed, {"axis": "", "degree": text_degree}])
            
        else:
            inc_1 = 0
            for item in self.button_entered:
                if item[0] == self.button_pressed:
                    print(item)
                    self.button_entered.pop(inc_1)
                    self.button_pressed.color = "#ffb4a2"
                    self.button_pressed.setText(self.button_pressed.text()[:-7])
                inc_1+=1

            self.button_pressed.color = "#ffb4a2"
            
            if self.button_pressed.objectName()[-2:] in ["_8", "90", "91", "92", "10"]:
                self.combo_animation_down.setDirection(QAbstractAnimation.Forward)
                self.combo_animation_down.start()
            else:
                self.combo_animation.setDirection(QAbstractAnimation.Forward)
                self.combo_animation.start()
            
            self.text_formation()
            self.combo_box_new = None
            self.button_axis = [] 
            self.button_degree = []
        
        print(self.button_entered)
        print("self.button_pressed=%s" %self.button_pressed)
        

        if self.button_axis != [] and self.button_degree != []:
            if self.button_pressed.text()[-1] == ".":
                self.button_pressed.setText(self.button_pressed.text()[:-7]+" "+ self.button_axis[0].text()[0] + 
                                            "/" + self.button_degree[0].text() + "..")
                self.button_pressed.color = "#fa8090"
            else:
                self.button_pressed.setText(self.button_pressed.text()+" "+ self.button_axis[0].text()[0] + 
                                            "/" + self.button_degree[0].text() + "..")
                self.button_pressed.color = "#fa8090"


            if self.button_pressed.objectName()[-2:] in ["_8", "90", "91", "92", "10"]:
                self.combo_animation_down.setDirection(QAbstractAnimation.Forward)
                self.combo_animation_down.start()
            else:
                self.combo_animation.setDirection(QAbstractAnimation.Forward)
                self.combo_animation.start()

            self.combo_box_new = None
            self.button_axis = [] 
            self.button_degree = []
            self.text_formation()


    def close_combo_box(self):
        time.sleep(0.75)
        self.widget_combo_box.setParent(None)


    def text_formation(self):

        text = ""
        right_but_hand = []
        left_but_hand = []
        right_but_leg = []
        left_but_leg = []
        for button in self.button_entered:
            if button[0].objectName()[:12]=="but_det_left":
                if button[0].objectName()[-2:] in ["20", "21","22","_3","40","41","42","_5"]:
                    left_but_hand.append(button)
                else:
                    left_but_leg.append(button)

            elif button[0].objectName()[:13]=="but_det_right":
                if button[0].objectName()[-2:] in ["20", "21","22","_3","40","41","42","_5"]:
                    right_but_hand.append(button)
                else:
                    right_but_leg.append(button)
        if right_but_hand != [] or left_but_hand != [] or right_but_leg != [] or left_but_leg != []:
            text += "Определяется патологическиая подвижность: "
            inc = 0
            for part in [right_but_hand,right_but_leg, left_but_hand, left_but_leg]:
                if part ==[]:
                    inc+=1
                    continue
                else:
                    if inc ==0:
                        text += "на протяжении правой руки -"
                    elif inc ==1:
                        text += "на протяжении правой ноги -"
                    elif inc ==2:
                        text += "на протяжении левой руки -"
                    elif inc ==3:
                        text += "на протяжении левой ноги -"
                    for but in part:
                        if but[1]["axis"] == "фронтальная":
                            text_axis = " во фронтальной плоскости"
                        elif but[1]["axis"] == "сагитальная":
                            text_axis = " в сагитальной плоскости"
                        elif but[1]["axis"] == "горизонтальная":
                            text_axis = " в горизонтальной плоскости"
                        elif but[1]["axis"] == "многоплоск-ая":
                            text_axis = " многоплоскостная"

                        text += " в проекции " + self.localize[but[0].objectName()[-2:]] + text_axis + " в пределах " + but[1]["degree"] + self.degree_sign +", "
                    text = text[:-2] + "; "
                    inc+=1
        print("print dict:")
        print(right_but_hand)
        print(left_but_hand)
        print(right_but_leg)
        print(left_but_leg)
        self.label_main_text.setText(text)
        self.update()


    def get_text(self):
        return self.label_main_text.text()

    def closeEvent(self, event):
        self.patholmobil_send_info.emit()
        self.close()
        self.setParent(None)

    def delete_close(self):
        self.label_main_text.setText("")
        self.patholmobil_send_info.emit()
        self.close()
        self.setParent(None)