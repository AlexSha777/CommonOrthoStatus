import sys
import time

from PyQt5 import QtGui 
from PyQt5.QtCore import pyqtSignal, QRect, QVariantAnimation, QAbstractAnimation, QEasingCurve
from PyQt5.QtGui import QPixmap, QPainter, QColor, QFont, QCursor
from PyQt5.QtGui import QPalette, QBrush, QPixmap

from PyQt5.QtCore import Qt, QSize, QPropertyAnimation, pyqtProperty

from PyQt5.QtWidgets import (QApplication, QWidget, QScrollArea, QHBoxLayout, QVBoxLayout, QTabWidget,
                            QDesktopWidget, QPushButton, QDialog, QLabel, QGridLayout, QGroupBox,
                            QLineEdit, QMessageBox, QComboBox, QMenu, QAction, QScrollArea, QSizePolicy)


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
        if value == "#CCCCCC":
            color_new = "#909090"

        elif value == "#adff2f":
            color_new = "#91BF4A"
        elif value =="#ffb4a2":
            color_new = "#A64A35"

        elif value == "#d5e664":
            color_new = "#869621"


        elif value =="#58C7E6":
            color_new = "#1D7B96"
        
        elif value == "#DC5E9E":
            color_new = "#8F1F58"

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
        


        elif value == "#e77251":    #5A8CA7   #B2E877
            color_new = "#96361A"
        elif value == "#A19AB0":
            color_new = "#3B2765"
        elif value == "#a6a852":
            color_new = "#6B6D1B"


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
        #self._update_stylesheet(QColor(self.color_main),QColor("black"))
        #self.update()

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
        #if self.color_main == "#f0f0f0": 
        #    self.start_color = "#B4B4B4"
        #elif self.color_main == "#adff2f":
        #    self.start_color = "#91BF4A"
        
        self._animation.setDirection(QAbstractAnimation.Backward)
        self._animation.start()
        super().enterEvent(event)

    def leaveEvent(self, event):
        #if self.color_main == "#f0f0f0": 
        #    self.start_color = "#B4B4B4"
        #elif self.color_main == "#adff2f":
        #    self.start_color = "#91BF4A"
        
        self._animation.setDirection(QAbstractAnimation.Forward)
        self._animation.start()
        super().leaveEvent(event)

class ComboWidget(QLabel):
    #combo_widget_closing = pyqtProperty()
    def __init__(self, parent=None, size=None):
        super().__init__(parent)
        
        #if self.color_ap == "":
        #    self._update_stylesheet(QColor(self.color_main), QColor("black"))
        #else:
        #    self._update_stylesheet(QColor(self.color_ap), QColor("black"))
        self.setStyleSheet(
            '''
                background-color: #FFFFFF;
                color: black;
                padding: 2px 2px 2px 2px;
                text-align: center;
                border-radius: 4px;
                border: 2px solid #9B9B9B;
                margin: 2px 2px 2px 2px;
            ''')
        #self._color = "#ffb4a2"
        #self._color_new = "#A64A35"
        #self._font_size = 14

class Label_vertebra(QLabel):
    def __init__(self, parent=None, size=None):
        super().__init__(parent)
        self._base_color = "white"
        self._update_stylesheet()

    @pyqtProperty(str)
    def color(self):
        return self._color

    @color.setter
    def color(self, value):
        self._base_color = value
        self._update_stylesheet()

    def _update_stylesheet(self):
        self.setStyleSheet(
            '''
                background-color: %s;
                color: black;
                border: none;
                padding: 2px 2px 2px 2px;
                text-align: center;
                font-size: 14px;
                border-radius: 4px;
                margin: 2px 2px 2px 2px;
            ''' % self._base_color
            )





class VertebraWindow(QWidget):
    vertebra_send_info = pyqtSignal()
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
        self.button_entered_sagit = []
        self.button_pressed = ""
        self.button_all = []
        self.button_axis = []
        self.button_degree = []
        self.label_to_change = []
        self.label_to_change_sagit = []

        self.text_front = ""
        self.text_sagit = ""

        self.combo_box_new = None

        self.areas = ["Шейный отдел", "Шейно-гудной отдел" , "Верхнегрудной отдел", "Среднегрудной отдел","Нижнегрудной отдел", 
                "Грудо-поясничный отдел", "Верхнепоясничный отдел", "Нижнепоясничный отдел"]

        self.areas_names_text = ["шейном отделе", "шейно-гудном отделе" , "верхнегрудном отделе", "среднегрудном отделе","нижнегрудном отделе", 
                "грудо-поясничном отделе", "верхнепоясничном отделе", "нижнепоясничном отделе"]

        self.areas_names_sagit = ["шейный лордоз", "грудной кифоз", "поясничный лордоз"]

        self.deform_directions = ["НЕТ","влево","вправо"]


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
        
        label_sample = QLabel("выпрямлен")
        label_sample.setStyleSheet(
            '''
                background-color: #E5E5E5;
                color: black;
                border: none;
                padding: 2px 2px 2px 2px;
                text-align: center;
                font-size: 14px;
                border-radius: 4px;
                margin: 2px 2px 2px 2px;
            ''')
        self.label_sample_width = label_sample.width()


        self.grid = QGridLayout(self)
        label_area = Label_vertebra("Отдел")
        label_left = Label_vertebra("Влево")
        label_axis = Label_vertebra("Позвоночник")
        label_right = Label_vertebra("Вправо")
        col = 0
        for i in [label_area, label_left, label_axis, label_right]:
            self.grid.addWidget(i,0, col,  Qt.AlignHCenter)
            col+=1

        self.file_name = "vertebra.bmp"
        self.pix = QPixmap(self.file_name)
        #self.pix_main = QPixmap(self.file_name).toImage()
        self.vert_image = QLabel("Image")
        self.vert_image.setPixmap(self.pix)

        self.grid.addWidget(self.vert_image,1, 2, 8, 1, Qt.AlignHCenter)

        #palette = QPalette()
        #palette.setBrush(QPalette.Background, QBrush(self.pix))
        #self.vert_image.setPalette(palette)
        #print("self.vert_image.rect()=%s" %self.vert_image.rect())
        #self.vert_image.show()

        row_number = 1
        for i in self.areas:
            button_zone = PushButton(i)
            
            if row_number in (1,2):
                button_zone.color = "#d5e664"
            elif row_number in (3,4,5):
                button_zone.color ="#58C7E6"
            elif row_number in (6,7,8):
                button_zone.color = "#DC5E9E"
            button_zone.clicked.connect(self.button_process)
            button_zone.setObjectName("but_0_"+str(row_number))
            label_left = Label_vertebra("-")
            
            label_left.setMinimumWidth(90)
            #label_left.setMinimumWidth(self.label_sample_width)
            
            label_left.setObjectName("lab_left_"+str(row_number))
            label_right = Label_vertebra("-")
            label_right.setMinimumWidth(90)
            #label_right.setMinimumWidth(self.label_sample_width)
            
            label_right.setObjectName("lab_right_"+str(row_number))
            self.label_to_change.append(label_right)
            self.label_to_change.append(label_left)
            self.grid.addWidget(button_zone,row_number, 0,  Qt.AlignHCenter)
            self.grid.addWidget(label_left,row_number, 1,  Qt.AlignHCenter)
            self.grid.addWidget(label_right,row_number, 3,  Qt.AlignHCenter)
            row_number += 1
        

        self.Ok_button = PushButton("Ok")
        self.Ok_button.clicked.connect(self.send_info)
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
        #self.setLayout(self.grid)
        screen = (QDesktopWidget().availableGeometry().width(), QDesktopWidget().availableGeometry().height())
        print(screen)
        print(self.height())
        

        self.tabWidget = QTabWidget(self)

        self.front = QWidget()
        self.front.setLayout(self.grid)
        self.front.adjustSize()


        self.grid_sagit = QGridLayout(self)
        label_area_sagit = Label_vertebra("Отдел")
        label_plane = Label_vertebra("Выпрямлен")
        label_axis_sagit = Label_vertebra("Позвоночник")
        label_increase = Label_vertebra("Усилен")
        for label_item in (label_plane,label_area_sagit, label_axis_sagit, label_increase): label_item.setMaximumHeight(30)
        col = 0
        for i in [label_area_sagit, label_plane, label_axis_sagit, label_increase]:
            self.grid_sagit.addWidget(i,0, col,  Qt.AlignHCenter)
            col+=1

        self.pix_sagit = QPixmap("sagit_vertebra_fit.bmp")
        self.vert_sagit_image = QLabel("Image")
        self.vert_sagit_image.setPixmap(self.pix_sagit)
        
        self.grid_sagit.addWidget(self.vert_sagit_image,1, 2, 3, 1, Qt.AlignHCenter)

        row_number = 1
        self.sagit_areas = ["Шейный лордоз", "Грудной кифоз", "Поясничный лордоз"]
        height_label_max = self.vert_sagit_image.height()/3
        for i in self.sagit_areas:
            button_zone = PushButton(i)
            if row_number ==1:
                button_zone.color = "#e77251"   #96361A
            elif row_number ==2:
                button_zone.color ="#A19AB0"     #3B2765
            elif row_number ==3:
                button_zone.color = "#a6a852"   #6B6D1B
            
            button_zone.clicked.connect(self.button_process)
            button_zone.setObjectName("but_1_"+str(row_number))
            label_plane = Label_vertebra("-")
            label_plane.setMinimumWidth(90)
            label_plane.setMaximumHeight(height_label_max)
            
            label_plane.setObjectName("lab_plan_"+str(row_number))
            label_increase = Label_vertebra("-")
            label_increase.setMinimumWidth(90)
            label_increase.setMaximumHeight(height_label_max)
           
            label_increase.setObjectName("lab_increa_"+str(row_number))
            self.label_to_change_sagit.append(label_increase)
            self.label_to_change_sagit.append(label_plane)
            self.grid_sagit.addWidget(button_zone,row_number, 0,  Qt.AlignHCenter)
            self.grid_sagit.addWidget(label_plane,row_number, 1,  Qt.AlignHCenter)
            self.grid_sagit.addWidget(label_increase,row_number, 3,  Qt.AlignHCenter)
            row_number += 1
        

        self.Ok_button_sagit = PushButton("Ok")
        self.Ok_button_sagit.clicked.connect(self.send_info)
        self.cancel_button_sagit = PushButton("Cancel")
        self.cancel_button_sagit.clicked.connect(self.delete_close)
        
        self.label_main_text_sagit = QLabel()
        self.label_main_text_sagit.setWordWrap(True)
        self.layout_label_main_text_sagit = QHBoxLayout()
        self.layout_label_main_text_sagit.addWidget(self.label_main_text_sagit)
        self.main_text_sagit = QWidget()
        self.scroll_text_sagit = QScrollArea()
        self.scroll_text_sagit.setWidgetResizable(True)
        self.group_box_sagit = QGroupBox("Текст")
        self.group_box_sagit.setLayout(self.layout_label_main_text_sagit)
        self.scroll_text_sagit.setWidget(self.group_box_sagit)

        self.group_box_sagit.setStyleSheet('''

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
        
        self.grid_sagit.addWidget(self.scroll_text_sagit, 4, 0, 1, 4)
        self.grid_sagit.addWidget(self.Ok_button_sagit , 5, 0, 1, 3)
        self.grid_sagit.addWidget(self.cancel_button_sagit , 5, 3, 1, 1)

        self.sagit = QWidget()
        self.sagit.setLayout(self.grid_sagit)
        self.sagit.adjustSize()
        #self.setLayout(self.grid)
        screen = (QDesktopWidget().availableGeometry().width(), QDesktopWidget().availableGeometry().height())
        print(screen)
        print(self.height())



        self.scroll = QScrollArea()
        self.scroll.setWidget(self.front)

        self.scroll_sagit = QScrollArea()
        self.scroll_sagit.setWidget(self.sagit)

        self.tabWidget.addTab(self.scroll,"Фронтальная плоскость")
        self.tabWidget.addTab(self.scroll_sagit,"Сагитальная плоскость")


        self.setWindowTitle ("Описание осей конечностей")
        
        self.size_front = QSize(self.front.width()+25, self.front.height()+30)
        
        self.tabWidget.resize(self.size_front)
        self.resize(self.size_front)
        #self.scroll.setMinimumSize(self.width(), self.height())
        self.show()
        self.move(300,(screen[1]-self.height())/2)
        print(self.size())
        print(self.scroll.size())

        
    #def paintEvent(self, e):
    #    painter = QPainter(self.vert_image.pixmap())

    #    print("drawing")
    #    print(self.vert_image.rect())
    #    painter.drawPixmap(0,0, self.pix)


    def button_process(self):
        but_name = self.sender().objectName()
        x_coord = self.sender().x()
        y_coord = self.sender().y()

        print(x_coord)
        print(y_coord)
        print(but_name)

        if self.combo_box_new == None:
            if but_name[4]=="0":
                self.deform_directions = ["НЕТ","влево","вправо"]
            else:
                self.deform_directions = ["НЕТ","выпрямлен","усилен"]

            self.deform_directions_but = []

            combo_layout = QGridLayout()
            combo_axis_layout = QVBoxLayout()
            
            for item in self.deform_directions:
                button_combo = PushButton(item, font_size=12)
                button_combo.color = "#CCCCCC"
                button_combo.clicked.connect(lambda: self.combo_box_def_direction(button_sender=but_name))
                self.deform_directions_but.append(button_combo)
                combo_axis_layout.addWidget(button_combo)
                combo_axis_layout.addSpacing(100)
            
            
            label_ax = QLabel("Направление деформации")
            label_ax.setAlignment(Qt.AlignHCenter)
            label_ax.setStyleSheet(
            '''
                background-color: #E5E5E5;
                color: black;
                border: none;
                padding: 2px 2px 2px 2px;
                text-align: center;
                font-size: 14px;
                border-radius: 4px;
                margin: 2px 2px 2px 2px;
            ''')
            label_ax_width = label_ax.width()
            combo_layout.addWidget(label_ax,0, 0)
            combo_layout.addLayout(combo_axis_layout, 1, 0)

            self.combo_box_new = ComboWidget(self)
            self.combo_box_new.setLayout(combo_layout)
            self.combo_box_new.show()
            
            
            #self.combo_box_new.resize(self.sender().size().width()*1.2, self.sender().size().height()*4)
            self.combo_box_new.resize(self.size_front.width()/3, self.sender().size().height()*4.5)

            self.combo_box_new.move(x_coord, y_coord + self.sender().height()+20)

            initial_rect = self.combo_box_new.geometry()
            final_rect = QRect(self.combo_box_new.x(),self.combo_box_new.y(),1,1)

            final_rect_down = QRect(self.combo_box_new.x()+self.combo_box_new.width(),self.combo_box_new.y()+self.combo_box_new.height(),1,1)
            
            print("final_rect=%s" % final_rect)

            self.combo_animation = QPropertyAnimation(self.combo_box_new, b'geometry')
            self.combo_animation.setEasingCurve(QEasingCurve.InOutSine)
            self.combo_animation.setDuration(300)
            self.combo_animation.setStartValue(initial_rect)
            self.combo_animation.setEndValue(final_rect)

            #self.combo_animation_down = QPropertyAnimation(self.combo_box_new, b'geometry')
            #self.combo_animation_down.setEasingCurve(QEasingCurve.InOutSine)
            #self.combo_animation_down.setDuration(300)
            #self.combo_animation_down.setStartValue(initial_rect)
            #self.combo_animation_down.setEndValue(final_rect_down)

            self.combo_animation.setDirection(QAbstractAnimation.Backward)
            self.combo_animation.start()

            self.button_pressed = self.sender()


        else:
            msg = QMessageBox()
            msg.setWindowTitle("Информация")
            msg.setText("Закончите введение вида деформации!!!")
            msg.setIcon(QMessageBox.Information)
            center = (self.geometry().center().x(), self.geometry().center().y())
            msg.show()
            msg.move(center[0]-(msg.size().width()/2), center[1]+(msg.size().height()/2))
            msg.exec_()


    def combo_box_def_direction(self, button_sender, index=None):
        
        text = self.sender().text()
        print(text)
        print(self.button_entered)
        print("self.button_pressed=%s" %self.button_pressed)
        if button_sender[4] == "0":
            if self.sender().text() != "НЕТ":
                inc = 0
                to_add_new_but = True
                for item in self.button_entered:
                    if item[0] == self.button_pressed:
                        self.button_entered[inc][0] = self.button_pressed
                        self.button_entered[inc][1] = text
                        to_add_new_but = False
                    inc+=1
                if to_add_new_but != False:
                    print (to_add_new_but)
                    self.button_entered.append([self.button_pressed, text])
                
                #self.button_pressed.color = "#fa8090"
                self.combo_animation.setDirection(QAbstractAnimation.Forward)
                self.combo_animation.start()
                label_name_l = "lab_left_" + self.button_pressed.objectName()[6:]
                label_name_r = "lab_right_" + self.button_pressed.objectName()[6:]
                label_row = {"l":"", "r": ""}

                for item in self.label_to_change:
                    if item.objectName() == label_name_r:
                        label_row["r"] = item
                    elif item.objectName() == label_name_l:
                        label_row["l"] = item
                
                if text == "влево":
                    label_row["l"].setText(text)
                    label_row["l"].color = "#FF8079"
                    label_row["r"].setText("-")
                    label_row["r"].color = "white"
                elif text == "вправо":
                    label_row["r"].setText(text)
                    label_row["r"].color = "#FF8079"
                    label_row["l"].setText("-")
                    label_row["l"].color = "white"
                self.text_formation()
                self.combo_box_new = None


            else:
                inc_1 = 0
                for item in self.button_entered:
                    if item[0] == self.button_pressed:
                        print(item)
                        self.button_entered.pop(inc_1)
                    inc_1+=1
                #print("name=%s" %button_sender[6:])
                #if button_sender[6:] in ("1","2"):
                #    self.button_pressed.color = "#d5e664"
                #elif button_sender[6:] in ("3","4","5"):
                #    self.button_pressed.color = "#58C7E6"
                #elif button_sender[6:] in ("6","7","8"):
                #    self.button_pressed.color = "#DC5E9E"

                self.combo_animation.setDirection(QAbstractAnimation.Forward)
                self.combo_animation.start()
                label_name_r = "lab_right_" + self.button_pressed.objectName()[6:]
                label_name_l = "lab_left_" + self.button_pressed.objectName()[6:]

                for item in self.label_to_change:
                    if item.objectName() in (label_name_l, label_name_r):
                        item.setText("-")
                        item.color = "white"

                self.text_formation()
                self.combo_box_new = None

        elif button_sender[4] =="1":
            if self.sender().text() != "НЕТ":
                inc = 0
                to_add_new_but = True
                for item in self.button_entered_sagit:
                    if item[0] == self.button_pressed:
                        self.button_entered_sagit[inc][0] = self.button_pressed
                        self.button_entered_sagit[inc][1] = text
                        to_add_new_but = False
                    inc+=1
                if to_add_new_but != False:
                    print (to_add_new_but)
                    self.button_entered_sagit.append([self.button_pressed, text])
                
                self.combo_animation.setDirection(QAbstractAnimation.Forward)
                self.combo_animation.start()
                label_name_l = "lab_plan_" + self.button_pressed.objectName()[6:]
                label_name_r = "lab_increa_" + self.button_pressed.objectName()[6:]
                label_row = {"l":"", "r": ""}
                
                for item in self.label_to_change_sagit:
                    if item.objectName() == label_name_r:
                        label_row["r"] = item
                    elif item.objectName() == label_name_l:
                        label_row["l"] = item
                
                if text == "выпрямлен":
                    label_row["l"].setText(text)
                    label_row["l"].color = "#FF8079"
                    label_row["r"].setText("-")
                    label_row["r"].color = "white"
                    
                elif text == "усилен":
                    label_row["r"].setText(text)
                    label_row["r"].color = "#FF8079"
                    label_row["l"].setText("-")
                    label_row["l"].color = "white"
                self.text_formation()
                self.combo_box_new = None


            else:
                inc_1 = 0
                for item in self.button_entered_sagit:
                    if item[0] == self.button_pressed:
                        print(item)
                        self.button_entered_sagit.pop(inc_1)
                    inc_1+=1
                #print("name=%s" %button_sender[6:])
                #if button_sender[6:] in ("1","2"):
                #    self.button_pressed.color = "#d5e664"
                #elif button_sender[6:] in ("3","4","5"):
                #    self.button_pressed.color = "#58C7E6"
                #elif button_sender[6:] in ("6","7","8"):
                #    self.button_pressed.color = "#DC5E9E"

                self.combo_animation.setDirection(QAbstractAnimation.Forward)
                self.combo_animation.start()
                label_name_l = "lab_plan_" + self.button_pressed.objectName()[6:]
                label_name_r = "lab_increa_" + self.button_pressed.objectName()[6:]

                for item in self.label_to_change_sagit:
                    if item.objectName() in (label_name_l, label_name_r):
                        item.setText("-")
                        item.color = "white"

                self.text_formation()
                self.combo_box_new = None



        print(self.button_entered)
        print("self.button_pressed=%s" %self.button_pressed)
        

        


    def close_combo_box(self):
        time.sleep(0.75)
        self.widget_combo_box.setParent(None)


    def text_formation(self):
        #self.button_entered[] = [self.button_pressed, text]
        text = ""
        inc = 0
        names_cort = (self.areas_names_text, self.areas_names_sagit)
        areas_cort = (self.areas, self.sagit_areas)
        for items in (self.button_entered, self.button_entered_sagit):
            if inc ==0:
                if items != []:
                    text = "Определяется деформация оси позвоночника во фронтальной плоскости: "
                    for button in items:
                        print(names_cort[inc][areas_cort[inc].index(button[0].text())])
                        text += "в "+names_cort[inc][areas_cort[inc].index(button[0].text())]+" "+button[1]+", "
                    text = text[:-2] + ". "
                else:
                    text = ""
                self.text_front = text
            elif inc ==1:
                if items != []:
                    text = "Определяется деформация оси позвоночника в сагитальной плоскости: "
                    for button in items:
                        print(names_cort[inc][areas_cort[inc].index(button[0].text())])
                        text += names_cort[inc][areas_cort[inc].index(button[0].text())]+" "+button[1]+", "
                    text = text[:-2] + ". "
                else:
                    text = ""
                self.text_sagit = text
            text = ""
            inc+=1
        text_to_add = self.text_front+self.text_sagit
        self.label_main_text.setText(text_to_add)
        self.label_main_text_sagit.setText(text_to_add)
        self.update()


    def get_text(self):
        return self.label_main_text.text()
    
    def closeEvent(self, event):
        self.vertebra_send_info.emit()
        print("vertebra closing")
        self.close()
        self.setParent(None)

    def send_info(self):
        self.vertebra_send_info.emit()
        self.close()
        self.setParent(None)

    def delete_close(self):
        self.label_main_text.setText("")
        self.vertebra_send_info.emit()
        self.close()
        self.setParent(None)