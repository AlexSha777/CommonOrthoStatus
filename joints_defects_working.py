# -*- coding: utf-8 -*-
import sys
import copy
from PyQt5 import QtGui 
from PyQt5.QtWidgets import (QWidget, QLabel, QApplication, QWidget, QScrollArea, QHBoxLayout, 
                            QVBoxLayout, QDesktopWidget, QPushButton, QLineEdit, QMessageBox, QGroupBox)

from PyQt5.QtCore import pyqtSignal, QRect, QVariantAnimation, QAbstractAnimation, Qt , QPoint, QEvent

from PyQt5.QtGui import   QPainter ,QPixmap, QImage, QColor, QPen, QCursor


from zone_axis import zone_axis
from zone_detect import zone_detect

from joints_wrist_foot import WristFootWindow
from ped_def_cont import PedFootWindow

class PushButton(QPushButton):
    def __init__(self, parent=None,font_size=None, color=None):
        super().__init__(parent)
        
        self.color_main ="#ffb4a2"

        self.color_ap = ""

        self._animation = QVariantAnimation(
            startValue=QColor("#A64A35"),
            endValue=QColor(self.color_main),
            valueChanged=self._on_value_changed,
            duration=400,
        )
        if font_size:
            self.font_size = font_size
        else:
            self.font_size = 14
        if self.color_ap == "":
            self._update_stylesheet(QColor(self.color_main), QColor("black"))
        else:
            self._update_stylesheet(QColor(self.color_ap), QColor("black"))
        self.setCursor(QCursor(Qt.PointingHandCursor))
  
    def setColor (self, color_new):
        self.color_main = color_new
        self.color_ap = color_new
        
        self._update_stylesheet(QColor(self.color_main),QColor("black"))
        #self.update()

    def setFont (self, font_size):
        self.font_size = font_size
        self.update()

    def getColor (self):
        return self.color_main

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
            padding: 4px 8px;
            text-align: center;
            text-decoration: none;
            font-size: %spx;
            border-radius: 8px;
            margin: 4px 2px;
            
        }
        """
            % (background.name(), foreground.name(), self.font_size)
        )

    def enterEvent(self, event):
        if self.color_main == "#ffb4a2":
            self._animation.setDirection(QAbstractAnimation.Backward)
            self._animation.start()
            super().enterEvent(event)

    def leaveEvent(self, event):
        if self.color_main == "#ffb4a2":
            self._animation.setDirection(QAbstractAnimation.Forward)
            self._animation.start()
            super().leaveEvent(event)




class BodyDefects (QWidget):
    text_changed = pyqtSignal()
    label_text_update = pyqtSignal()
    joints_send_info = pyqtSignal()

    def __init__(self, wrist_ped, joint_defects, label_text, wrist_ped_text, **kwargs):
        #super(BodyDefects,self).__init__(parent)
        super().__init__(**kwargs)
        self.file_name = "body.bmp"
        #self.pix = QPixmap() # создать экземпляр объекта QPixmap
        #self.lastPoint = QPoint () # начальная точка
        #self.endPoint = QPoint () # конечная точка
        self.initUi()
        self.wrist_ped = wrist_ped.copy()
        self.joint_defects = joint_defects.copy()
        self.label_saved_from_parent = label_text
        self.wrist_left_text, self.wrist_right_text,self.ped_left_text, self.ped_right_text = wrist_ped_text[0],wrist_ped_text[1],wrist_ped_text[2],wrist_ped_text[3]
        if wrist_ped !=0: self.wrist_ped_data_processing(wrist_ped=wrist_ped, label_text = label_text)
        if joint_defects !=0: self.joint_defects_data_processing(joint_defects=joint_defects, label_text = label_text)
    
    def initUi(self):
        self.degree_sign = u'\N{DEGREE SIGN}'
        #self.sum_sign = u'\N{GREEK CAPITAL LETTER SIGMA}'.decode("utf-8")
        self.sum_sign = "сумма"

        self.pix = QPixmap(self.file_name)
        self.pix_main = QPixmap(self.file_name).toImage()


        self.resize(self.pix.width(), self.pix.height())
        self.setMouseTracking(True)

        self.extremity_detect = zone_detect.copy()
        self.extremity_axis = zone_axis.copy()

        self.for_child_info_coding = {
                                    "Wrist L":[{},[]],
                                    "Wrist R":[{},[]],
                                    "Ped L":[{},[]],
                                    "Ped R":[{},[]],
                                    } 
        self.wrist_text = ""
        self.ped_text = ""

        self.ped_left_text = ""
        self.ped_right_text = ""
        self.wrist_left_text = ""
        self.wrist_right_text = ""

        self.artic_contacture = []
        self.checked_zones = []

        self.amputation_level = {}
        self.amputation_level_text = ""
        self.ampute_level_coding = {}
        
        self.defect_percent = 0
        self.wrist_defect_detailed = {}

        self.entering_artilatio = []

        self.inner_wrist_window = []
        self.inner_ped_window = []
        
        self.artic_to_exclude = []
        
        self.ampute_detail = {
            "hand_left": {
                    "wrist": [0, 0.10],
                    "carpus": [0.11, 0.14],
                    "rad_carp_artic": [0.15, 0.18],
                    "bracchium": [0.19, 0.50],
                    "cubitus": [0.51, 0.56],
                    "humero": [0.57, 0.85],
                    "humeri_atric": [0.86, 1.0],
            },

            "hand_right": {
                    "wrist": [0, 0.10],
                    "carpus": [0.11, 0.16],
                    "rad_carp_artic": [0.17, 0.19],
                    "bracchium": [0.20, 0.53],
                    "cubitus": [0.54, 0.57],
                    "humero": [0.58, 0.87],
                    "humeri_atric": [0.88, 1.0],
            },
             
            "leg_right": {
                    "ped": [0, 0.09],
                    "talocruralis_atric": [0.10, 0.11],
                    "crus": [0.12, 0.43],
                    "genu": [0.44, 0.51],
                    "femur": [0.52, 0.85],
                    "coxae": [0.86, 1.0],
            },

            "leg_left": {
                    "ped": [0, 0.09],
                    "talocruralis_atric": [0.10, 0.12],
                    "crus": [0.13, 0.43],
                    "genu": [0.44, 0.52],
                    "femur": [0.53, 0.86],
                    "coxae": [0.87, 1.0],
            },
        }

        self.ampute_detail_name = {
            "hand_left": "левой руки",
            "hand_right": "правой руки", 
            "leg_right": "правой ноги",
            "leg_left": "левой ноги",
            "wrist": "кисти",
            "carpus": "запястья",
            "rad_carp_artic": "лучезапястного сустава",
            "cubitus": "локтевого сустава",
            "humeri_atric": "плечевого сустава",
            "ped": "стопы",
            "talocruralis_atric": "голеностопного сустава",
            "genu": "коленного сустава",
            "coxae": "тазобедренного сустава",
            "bracchium":"предплечья", 
            "humero":"плеча", 
            "crus": "голени", 
            "femur": "бедра"
        }

        self.os_level_name = {
        
        "base": "основания",
        "diaf": "диафиза",
        "caput": "головки",
        "tuber": "бугристости",
        }
        
        self.artic_buttons = []
        self.artic_names = ["Carporadialis", "Cubitus", "Humeri", "Talocruralis", "Genus", "Coxae", "Cervicalis", "Thoracalis", "Lumbalis", "Wrist", "Ped", "Radioulnaris"]



        self.artic_names_trans = {
            "Carporadialis": "лучезапястном суставе",
            "Cubitus": "локтевом суставе",
            "Humeri": "плечевом суставе", 
            "Talocruralis": "голеностопном суставе", 
            "Genus": "коленном суставе", 
            "Coxae": "тазобедренном суставе",
            "Cervicalis": "шейном отделе позвоночника", 
            "Thoracalis": "грудном отделе позвоночника", 
            "Lumbalis": "поясничном отделе позвоночника", 
            "Wrist": "кисти", 
            "Ped": "стопы", 
            "Radioulnaris": "луче-локтевых суставах",
        }

        self.level_artic_relation = {
            "wrist": ["Wrist"],
            "carpus": ["Wrist"],
            "rad_carp_artic": ["Carporadialis", "Wrist"],
            "bracchium": ["Carporadialis", "Wrist"],
            "cubitus": ["Carporadialis", "Wrist","Radioulnaris","Cubitus"],
            "humero": ["Carporadialis", "Wrist","Radioulnaris","Cubitus"],
            "humeri_atric": ["Carporadialis", "Wrist","Radioulnaris","Cubitus","Humeri"],
            "ped": ["Ped"],
            "talocruralis_atric": ["Talocruralis", "Ped"],
            "crus": ["Talocruralis", "Ped"],
            "genu": ["Talocruralis", "Ped","Genus"],
            "femur": ["Talocruralis", "Ped","Genus"],
            "coxae": ["Talocruralis", "Ped","Genus","Coxae"],
        }

        self.artic_but_coord = [
        [60, 470],
        [443, 470],
        [75, 332],
        [455, 332],
        [95, 196], 
        [425, 196],
        [142, 853],
        [360, 853],
        [155, 664],
        [373, 664],
        [211, 389],
        [311, 389],
        [338, 112],
        [264, 211],
        [264, 332],
        [110, 537],
        [429, 537],
        [150, 907],
        [374, 907],
        [50, 401],
        [456, 401]
        ]


        for art in self.artic_names:
            if art not in ["Cervicalis", "Thoracalis", "Lumbalis"]:
                name_R = art + " R"
                name_L = art + " L"
                but_1 = PushButton(self, font_size=12)
                but_1.setText(name_R)
                but_2 = PushButton(self, font_size=12)
                but_2.setText(name_L)
                self.artic_buttons.append(but_1)
                self.artic_buttons.append(but_2)
            else:
                name = art
                but = PushButton(self, font_size=12)
                but.setText(name)
                self.artic_buttons.append(but)

        increment = 0
        for button in self.artic_buttons:
            #button.resize(button.size().width(), 40)
            if button.text() in ["Wrist L", "Ped L", "Wrist R", "Ped R"]:
                button.clicked.connect(self.movement_wrist_ped)
            else:
                button.clicked.connect(self.movement_def)
            button.move(self.artic_but_coord[increment][0], self.artic_but_coord[increment][1])
            increment+=1

        self.dict_joints = {
            "Cervicalis": {
                "flex": [40,0,40],
                "inclineRignt": [45,0,45],
                "rotRight": [70,0,70]
                    },
            "Thoracalis": {"inclineAnt": [30,38]},
            "Lumbalis": {"inclineAnt": [10,15]},
            "Humeri": {
                "flex": [180,0,40],
                "abdu": [180,0,20],
                "rotExt": [60,0,90]
                },
            "Cubitus": {"flex": [140, 0, 0]},
            "Radioulnaris": {"rotSup": [90, 0, 90]},
            "Carporadialis": {
                "flex": [80,0,70],
                "abdu": [20,0,40]
                },
            "Wrist": 0,
            "Coxae": {
                "flex": [130,0,10],
                "abdu": [50,0,40],
                "rotExt": [50,0,50]
                },
            "Genus": {"flex": [140, 0, 0]},
            "Talocruralis": {"flexPlant": [45,0,20]},
            "Ped": 0,

        }

        

        

        self.scroll = QScrollArea()
        #scroll.setBackgroundRole(QPalette.Dark)
        self.scroll.setAlignment(Qt.AlignLeft)
        self.scroll.setWidget(self)
        #self.scroll.show()
        self.main_box = QHBoxLayout()
        self.main_box.setAlignment(Qt.AlignLeft)
        self.main_box.addWidget(self.scroll)
        
        self.label_main_text_cont = QLabel()

        self.style_box_text_cont = QGroupBox("Текст")
        self.style_box_text_cont.setStyleSheet('''
            QGroupBox {
                margin-top: 2ex;
            }
            QGroupBox:enabled {
                border: 3px solid #851E1E;
                border-radius: 5px;
            }
            QGroupBox::title {
                subcontrol-origin: margin;
                left: 3ex;
            }
        ''')
        self.group_box_text_cont = QHBoxLayout()
        self.group_box_text_cont.addWidget(self.label_main_text_cont)
        #self.group_box_text_cont.addStretch()
        self.style_box_text_cont.setLayout(self.group_box_text_cont)
        self.main_box.addWidget(self.style_box_text_cont)
        
        
        
        self.footer = QHBoxLayout()
        self.okButton = PushButton("OK")
        
        self.okButton.clicked.connect(self.close)
        self.cancelButton = PushButton("Cancel")
        self.clearButton = PushButton("Clear")
        self.clearButton.setColor("#DC143C")
        self.clearButton.clicked.connect(self.clear_info)
        
        self.cancelButton.clicked.connect(self.close)
        self.footer.addWidget(self.okButton)
        self.footer.addWidget(self.cancelButton)
        self.footer.addWidget(self.clearButton)


        self.label_text_update.connect(self.label_update)


        self.main = QVBoxLayout()
        self.main.addLayout(self.main_box)
        #main.addWidget(self.label_main)
        self.main.addLayout(self.footer)

        #width_text_label = int(self.widget.size().width()) / 2
        #print(width_text_label)
        #self.label_main_text_cont.resize(width_text_label, 100)
        #self.style_box_text_cont.resize(width_text_label, 100)
        #width_main = self.widget.size().width() + width_text_label
        #sizeObject = QDesktopWidget().screenGeometry(-1)
        sizeObject = QDesktopWidget().screenGeometry(-1)
        #self.label_main_text_cont.resize(100, 100)
        self.label_main_text_cont.setWordWrap(True)
        height_label = copy.deepcopy(self.height())
        print(height_label)
        self.label_main_text_cont.setMaximumSize(200, height_label-25)
        self.label_main_text_cont.setMinimumSize(200, height_label-25)
        self.scroll.setMinimumSize(self.width(), self.height())
        #self.resize(width_main, (self.height()))
        
        #self.setWindowTitle ("Контрактуры суставов и дефекты конечностей")
        #self.setGeometry(200, 50, self.size().width()+275, self.size().height()+20)
        self.widget_main = QWidget()
        #self.widget_main.setGeometry(200, 50, self.size().width()+275, self.size().height()+20)
        self.widget_main.setLayout(self.main)
        print(self.size())
        #width = int(self.width())+275
        #height = int(self.height())+20
        self.move(0,0)
        print(self.size())
        self.widget_main.resize(600, 943)
        self.widget_main.setWindowTitle ("Контрактуры суставов и дефекты конечностей")
        self.widget_main.setWindowFlags( Qt.Window | Qt.WindowTitleHint | Qt.CustomizeWindowHint )
        
        self.widget_main.show()



    def cancel_info(self):
        #self.joints_send_info.emit()
        #self.widget_main.close()
        self.close()




    def close_window_send_info(self):
        
        #self.joints_send_info.emit()
        #self.widget_main.close()
        self.close()


    def sendInfo(self):
        text = self.label_main_text_cont.text()
        dict_wrist_ped = self.for_child_info_coding.copy()
        
        #self.joint_defects_info_coding = {
        #                            "ampute":[],
        #                            "contracture":[],
        #                            }
        dict_joint_defects = {}
        dict_joint_defects["ampute"] = self.ampute_level_coding.copy()
        dict_joint_defects["contracture"] = self.artic_contacture[:]
        
        wrist_ped_text = [self.wrist_left_text[:], self.wrist_right_text[:],self.ped_left_text[:], self.ped_right_text[:]] 

        return text, dict_joint_defects, dict_wrist_ped , wrist_ped_text


    def get_checked_zones(self):
        return self.checked_zones


    def get_text(self):
        string = ""
        if self.defect_percent !=0:
            string = self.amputation_level_text[:-2] + " (всего: " + str(self.defect_percent) + "% от ф-ии хвата и удержания предметов кистями)" + "."
        return string

    def closeEvent(self, event):
        print("closeEvent!!!")
        self.joints_send_info.emit()
        self.widget_main.close()
        #self.close()
        event.accept()

    def event(self, e):
        
        if e.type() == QEvent.KeyPress:
            print("Нажата клавиша на клавиатуре")
            print("Код:", e.key(), ", текст:", e.text())
        elif e.type() == QEvent.Close:
            print("Окно закрыто")
        elif e.type() == QEvent.MouseButtonPress:
            print ("Щелчок мышью. Координаты:", e.x(), e.y())
        return QWidget.event(self, e) # Отправляем дальше


    def paintEvent(self,event):
        pp = QPainter( self.pix)
		 # Нарисуйте прямую линию в соответствии с двумя положениями до и после указателя мыши
        #pp.drawLine( self.lastPoint, self.endPoint)
		 # Сделать предыдущее значение координаты равным следующему значению координаты,
		 # Таким образом можно нарисовать непрерывную линию
        #self.lastPoint = self.endPoint
        painter = QPainter(self)
        painter.drawPixmap (0, 0, self.pix) # Рисуем на холсте

        

       # Мышь пресс-мероприятие
    
    def mousePressEvent(self, event):
        # Нажмите левую кнопку мыши
        if event.button() == Qt.LeftButton :
            position = [event.x(), event.y()]
            print(position)

            for k, v in self.extremity_detect.items():
                for i in v:
                    if position == i:
                        print(k)
                        self.change_color(k, self.file_name, position)
                        #print(front_zones_names_dict[k])
          
    
    def change_color(self, k, file_name, position):
    
        zone_name = k
        updated_image = self.pix.toImage()
        

        if k in self.checked_zones:
            
            self.checked_zones.remove(k)
            self.amputation_level.pop(k)
            self.ampute_level_coding.pop(k)
            zone_to_update = self.extremity_detect[k][:]


            for x in zone_to_update:
                color = QColor(self.pix_main.pixel(x[0],x[1]))
                QImage.setPixelColor(updated_image, x[0], x[1], color)
        else:
            #color = QColor(255, 99, 71)
            color = (40, 10, 10)

            self.checked_zones.append(k)

            list_to_draw = self.perpendicular(zone=zone_name, point=position)
            #for x in source_dict[zone_name]:
            for x in list_to_draw:
                color_main = QColor(self.pix_main.pixel(x[0],x[1])).getRgb()[:-1]
                color_1 = [255, ]
                if (color_main[1]+color[1]) >= 255:
                    color_1.append(255)
                else:
                    color_1.append(color_main[1]+color[1])
                
                if (color_main[2]+color[2]) >= 255:
                    color_1.append(255)
                else:
                    color_1.append(color_main[2]+color[2])

                #print(color_main)
                #print(color_1)

                color_to_paste = QColor(color_1[0], color_1[1], color_1[2])
                QImage.setPixelColor(updated_image, x[0], x[1], color_to_paste)
                #c = updated_image.pixel(x[0],x[1])
                #print("color = ", QColor(c).getRgb()) 
                #print(x)

            #updated_image = self.perpendicular(zone=zone_name, point=position, pixmap=updated_image)



        self.pix = QPixmap.fromImage(updated_image)
        self.text_formation()
        self.update()
        self.text_changed.emit()
        print(self.checked_zones)
        print(self.amputation_level)
        print(self.amputation_level_text)
        print("percent: %s" % self.defect_percent)
        print(self.wrist_defect_detailed)
        
    def picture_clear(self):
        source_dict = 0
        updated_image = self.pix.toImage()
        if self.file_name == "wrists_l.bmp":
            source_dict = self.wrist_L_detect
        else:
            source_dict = self.wrist_R_detect
        color = QColor(255, 255, 255)
        for i in self.checked_zones:
            for x in source_dict[i]:
                c = updated_image.pixel(x[0],x[1])
                
                QImage.setPixelColor(updated_image, x[0], x[1], color)
            self.pix = QPixmap.fromImage(updated_image)
            self.update()
        self.checked_zones = []
        self.update()

    def text_formation(self):
        
        ampute = "Имеется дефект: "
        diaf_level = 0
        diaf_level_text = ""
        self.wrist_defect_detailed = {}
        button_to_change = []
        percent = 0
        
        if self.checked_zones != []:
            #ampute = "дефект " + wrist
            print("amputation_level=%s" %self.amputation_level)
            for key, value in self.amputation_level.items():
                
                for detail_key, detail_value in self.ampute_detail[key].items():
                    if value >= detail_value[0] and value <= detail_value[1]:
                        diaf_level_text = self.diaf_level(detail_key = detail_key, key = key, value = value, detail_value = detail_value)
                        ampute += self.ampute_detail_name[key] + " на уровне " + diaf_level_text + self.ampute_detail_name[detail_key] + ", "
                        diaf_level = 0
                        diaf_level_text = ""
                        print("detail_key=%s" %detail_key)
                        for artic in self.level_artic_relation[detail_key]:
                            
                            if key.split("_")[1] == "right":
                                side = " R"
                            else:
                                side = " L"
                            for but in self.artic_buttons:
                                if but.text().split("\n")[0] == (artic+side):
                                    print(artic+side)
                                    button_to_change.append(but)
            for but in self.artic_buttons:
                if but in button_to_change:
                    if but.text().split("\n")[0] in ["Wrist L","Wrist R", "Ped L", "Ped D"] and but.getColor()=="#B0E0E6":
                        ####
                        if but.text().split("\n")[0] =="Wrist L":
                            msgBox = QMessageBox()
                            msgBox.setWindowTitle("Warning")
                            msgBox.setStandardButtons(QMessageBox.Yes|QMessageBox.No)
                            msgBox.setText("Удалить введенные значения в поле 'Wrist L'?")
                            result =msgBox.exec_()
                            if QMessageBox.Yes == result:
                                self.for_child_info_coding["Wrist L"]=[{},[]]
                                but.setColor(color_new="#808080")
                                self.wrist_left_text = ""
                                self.label_update()
                            elif QMessageBox.No == result:
                                continue

                        elif but.text().split("\n")[0] =="Wrist R":
                            msgBox = QMessageBox()
                            msgBox.setWindowTitle("Warning")
                            msgBox.setStandardButtons(QMessageBox.Yes|QMessageBox.No)
                            msgBox.setText("Удалить введенные значения в поле 'Wrist R'?")
                            result =msgBox.exec_()
                            if QMessageBox.Yes == result:
                                self.for_child_info_coding["Wrist R"]=[{},[]]
                                but.setColor(color_new="#808080")
                                self.wrist_right_text = ""
                                self.label_update()
                            elif QMessageBox.No == result:
                                continue

                        elif but.text().split("\n")[0] =="Ped L":
                            msgBox = QMessageBox()
                            msgBox.setWindowTitle("Warning")
                            msgBox.setStandardButtons(QMessageBox.Yes|QMessageBox.No)
                            msgBox.setText("Удалить введенные значения в поле 'Ped L'?")
                            result =msgBox.exec_()
                            if QMessageBox.Yes == result:
                                self.for_child_info_coding["Ped L"]=[{},[]]
                                but.setColor(color_new="#808080")
                                self.ped_left_text = ""
                                self.label_update()
                            elif QMessageBox.No == result:
                                continue

                        elif but.text().split("\n")[0] =="Ped R":
                            msgBox = QMessageBox()
                            msgBox.setWindowTitle("Warning")
                            msgBox.setStandardButtons(QMessageBox.Yes|QMessageBox.No)
                            msgBox.setText("Удалить введенные значения в поле 'Ped R'?")
                            result = msgBox.exec_()
                            if QMessageBox.Yes == result:
                                self.for_child_info_coding["Ped R"]=[{},[]]
                                but.setColor(color_new="#808080")
                                self.ped_right_text = ""
                                self.label_update()
                            elif QMessageBox.No == result:
                                continue

                    else:
                        but.setColor(color_new="#808080")
                        print("artic_contacture: %s" %self.artic_contacture)
                        if self.artic_contacture != []:
                            for art_cont in self.artic_contacture:
                                if art_cont[0] == but.text().split("\n")[0]:
                                    self.artic_contacture.remove(art_cont)
                        #self.text_contr_formation()
                        but.setText(but.text().split("\n")[0])
                        but.adjustSize()
                elif but.getColor()=="#808080":
                    but.setColor(color_new="#ffb4a2")
        else:
            for but in self.artic_buttons:
                if but.getColor()=="#808080":
                    but.setColor(color_new="#ffb4a2")




        if ampute == "Имеется дефект: ":
            ampute = ""
        self.amputation_level_text = ampute
        self.label_text_update.emit()
        print("self.for_child_info_coding=%s" %self.for_child_info_coding)
        self.defect_percent = round(percent*100, 2)

    def diaf_level(self, detail_key, key, value, detail_value):
        diaf_level_text_new = ""
        if detail_key in ("bracchium", "humero", "crus", "femur" ):
            diaf_level = (value - detail_value[0])/(detail_value[1] - detail_value[0])
            if diaf_level <= 0.33:
                diaf_level_text_new = "дистальной трети "
            elif diaf_level > 0.33 and diaf_level <= 0.66:
                diaf_level_text_new = "средней трети "
            elif diaf_level > 0.66:
                diaf_level_text_new = "проксимальной трети "
        return diaf_level_text_new

    def get_wrist_defect_detailed(self):
        return self.wrist_defect_detailed


    def perpendicular (self, zone, point):
        
        axis_zone = "axis_" + zone
        print(axis_zone)
        print (self.extremity_axis[axis_zone])
        axis = self.extremity_axis[axis_zone][:]

        
        
        #print(axis_zone)
        #print(axis)
        
        x1 = axis[0][0]
        y1 = axis[0][1]
        x2 = axis[1][0]
        y2 = axis[1][1]
        #y = kx + b
        k = (y1-y2)/(x1-x2)
        b = y2-k*x2
        k_perpend = -(1/k)
        
        #y-point[1] = k_perpend(x-point[0])
        #y= k_perpend(x-point[0]) + point[1]
        #y= k_perpend(((y-b)/k)-point[0]) + point[1]
        c = -k_perpend*point[0] + point[1]
        #y= k_perpend*x + c
        k_index = k_perpend/k
        #y= k_index*(y-b) + c
        #y= k_index*y-k_index*b + c
        #y-k_index*y= -k_index*b + c
        #y*(1-k_index) = -k_index*b + c
        #y = (-k_index*b + c)/(1-k_index)
        y_cross = (-k_index*b + c)/(1-k_index)
        x_cross = (y_cross-b)/k
        
        print(x_cross)
        print(y_cross)
        if y2>y1:
            length = ((x2-x1)**2 + (y2 -y1)**2)**0.5
            level = round((((x2-x_cross)**2 + (y2-y_cross)**2)**0.5)/length, 2)
        else:
            length = ((x1-x2)**2 + (y1 -y2)**2)**0.5
            level = round((((x1-x_cross)**2 + (y1-y_cross)**2)**0.5)/length, 2)
        print("level: %s" %level)
        
        self.amputation_level[zone] = level
        self.ampute_level_coding[zone] = point


        to_draw = self.extremity_detect
        zone_to_draw = to_draw.copy()
        

        to_color_zone = []
        
    
        for point_to_draw in zone_to_draw[zone]:
            if point_to_draw[1]>= round(k_perpend*(point_to_draw[0]-point[0]) + point[1]):
                to_color_zone.append(point_to_draw)
        
        print(len(to_color_zone))

        return to_color_zone
    
    def movement_def(self):
        if self.sender().getColor() == "#808080":
            msgBox_error = QMessageBox()
            msgBox_error.setWindowTitle("Warning")
            msgBox_error.setText("Сустав не может быть описан - указан, как ампутированный")
            msgBox_error.exec_()

        else:
            if self.entering_artilatio ==[]:

                button_text = self.sender().text()
                button = self.sender()
                articulatio_editing = ""
                
                if len(button_text.split("\n"))>1:
                    articulatio_editing = button_text.split("\n")[0]
                    
                else:
                    articulatio_editing = button_text[:]
                length_artric = len(articulatio_editing.split(" "))
                if length_artric>1:
                    self.articulatio = articulatio_editing.split(" ")[0]
                else:
                    self.articulatio = articulatio_editing[:]

                
                moving = QWidget(self)
                
                moving.setStyleSheet('''
                    QWidget {
                        background: #ffcdb2;
                        border-radius: 6px;
                        }
                    QLineEdit {
                        background-color: white;
                        border-style: groove;
                        border-width: 2px;
                        border-radius: 6px;
                        border-color: #FFA07A;
                        font: bold 12px;
                        padding: 1px;
                        }
                            ''')
                #self.dict_joints
                
                self.entering_artilatio = [self.sender()]


                box_common = QVBoxLayout()
                
                for direction in list(self.dict_joints[self.articulatio].keys()):

                    box = QHBoxLayout()
                    label = QLabel()
                    if direction == "flex":
                        label.setText("сгиб./разгиб.")
                    elif direction == "inclineRignt":
                        label.setText("накл.вправо/влево")
                    elif direction =="rotRight":
                        label.setText("пов.вправо/влево")
                    elif direction =="inclineAnt":
                        label.setText("выпрямл.пол./накл.вперед")

                    elif direction =="abdu":
                        label.setText("отвед./привед.")

                    elif direction =="rotExt":
                        label.setText("рот.нар./внутр.")

                    elif direction =="rotSup":
                        label.setText("супин./прон.")

                    elif direction =="flexPlant":
                        label.setText("под.сгиб./разгиб.")
                    
                    #print(button.x(), button.y())
                    #label.move(button.y(), button.x())
                    direction_range_list = []
                    text_edit_1 = QLineEdit()
                    text_edit_1.resize(40, 30)
                    text_edit_1.setPlaceholderText(str(self.dict_joints[self.articulatio][direction][0]))
                    text_edit_1.setFocus(True)
                    if direction =="inclineAnt":
                        text_edit_1.setValidator(QtGui.QIntValidator(0, 50))

                    else:
                        text_edit_1.setValidator(QtGui.QIntValidator(0, int(self.dict_joints[self.articulatio][direction][0])))
                        
                    label_1 = QLabel()
                    if direction =="inclineAnt":
                        label_1.setText("см/ ")
                    else:
                        label_1.setText(self.degree_sign + "/")

                    text_edit_2 = QLineEdit()
                    text_edit_2.resize(40, 30)
                    text_edit_2.setPlaceholderText(str(self.dict_joints[self.articulatio][direction][1]))
                    if direction =="inclineAnt":
                        text_edit_2.setValidator(QtGui.QIntValidator(0, 80))
                    else:
                        text_edit_2.setValidator(QtGui.QIntValidator(0, int(self.dict_joints[self.articulatio][direction][0])))
                    label_2 = QLabel()
                    if direction =="inclineAnt":
                        label_2.setText("см")
                    else:
                        label_2.setText(self.degree_sign )
                    label.resize(10, 30)
                    box.addWidget(label)
                    box.addWidget(text_edit_1)
                    label_1.resize(10, 30)
                    box.addWidget(label_1)
                    box.addWidget(text_edit_2)
                    label_2.resize(10, 30)
                    box.addWidget(label_2)
                    direction_range_list.append(text_edit_1)
                    direction_range_list.append(text_edit_2)

                    if len(self.dict_joints[self.articulatio][direction]) >2:
                        label_2.setText(label_2.text() + "/ ")
                        label_2.resize(10, 30)
                        text_edit_3 = QLineEdit()
                        text_edit_3.resize(40, 30)
                        text_edit_3.setPlaceholderText(str(self.dict_joints[self.articulatio][direction][2]))
                        if int(self.dict_joints[self.articulatio][direction][2])>int(self.dict_joints[self.articulatio][direction][0]):
                            text_edit_2.setValidator(QtGui.QIntValidator(0, int(self.dict_joints[self.articulatio][direction][2])))
                        text_edit_3.setValidator(QtGui.QIntValidator(0, int(self.dict_joints[self.articulatio][direction][2])))
                        label_3 = QLabel()
                        label_3.setText(self.degree_sign)
                    
                        box.addWidget(text_edit_3)
                        label_3.resize(10, 30)
                        box.addWidget(label_3)
                        direction_range_list.append(text_edit_3)
                   
                    self.entering_artilatio.append(direction_range_list)
                    
                    box_common.addLayout(box)
                
                self.button_new = PushButton("Ok")
                self.button_new_cancel = PushButton("Cancel")
                self.button_new_cancel.clicked.connect(self.moving_close)
                #button_ok.resize(40, 30)
                self.button_new.clicked.connect(self.range_calculate)
                button_box = QHBoxLayout()
                button_box.addWidget(self.button_new)
                button_box.addWidget(self.button_new_cancel)
                box_common.addLayout(button_box)

                moving.setLayout(box_common)
                
                #print(moving.width(), moving.height())
                if len(self.dict_joints[self.articulatio].keys())==1:
                    height = 80
                elif len(self.dict_joints[self.articulatio].keys())==2:
                    height = 110
                elif len(self.dict_joints[self.articulatio].keys())==3:
                    height = 140

                size = [self.size().width(), self.size().height()]
                #print(size)
                #print(articulatio_editing)
                #print((size[1] - button.y())/size[1])

                if articulatio_editing[-1] != "L" and ((size[1] - button.y())/size[1])<0.25 and articulatio_editing!="Cervicalis": 
                    moving.resize(size[0]-button.x()-20,height)
                    moving.move(button.x(), button.y() - moving.height())

                elif articulatio_editing[-1] != "L" and ((size[1] - button.y())/size[1])>=0.25 and articulatio_editing!="Cervicalis":
                    moving.resize(size[0]-button.x()-20,height)
                    moving.move(button.x(), button.y() + button.height())

                elif articulatio_editing[-1] == "L" and ((size[1] - button.y())/size[1])<0.25:
                    moving.resize(button.x() + button.width()-20, height)
                    moving.move(button.x()+button.width()-moving.width(), button.y() - moving.height())

                elif articulatio_editing[-1] == "L" and ((size[1] - button.y())/size[1])>=0.25:
                    moving.resize(button.x() + button.width()-20, height)
                    moving.move(button.x()+button.width()-moving.width(), button.y() + button.height())

                elif articulatio_editing=="Cervicalis":
                    moving.resize(button.x() + button.width()-20, height)
                    moving.move(button.x()+button.width()-moving.width(), button.y() + button.height())
                






                #if len(self.dict_joints[self.articulatio].keys())==1:
                #moving.resize(250,160)


                self.entering_artilatio.append(moving)

                moving.show()
                
                self.update()
                
            else:
                msgBox = QMessageBox()
                msgBox.setWindowTitle("Warning")
                msgBox.setText("Завершите введение обема движений в текущем суставе")
                msgBox.exec_()
    
    def wrist_ped_data_processing(self, wrist_ped, label_text):
        
        #self.wrist_ped_info_coding = {
        #                            "Wrist L":[{},[]],
        #                            "Wrist R":[{},[]],
        #                            "Ped L":[{},[]],
        #                            "Ped R":[{},[]],
        #                            } 
        

        self.for_child_info_coding = wrist_ped.copy()
        for but_name, wrist_ped_dict in self.for_child_info_coding.items():
            if wrist_ped_dict != [{},[]]:
                for button in self.artic_buttons:
                    if button.text() == but_name:
                        button.setColor(color_new="#B0E0E6")
        
        if label_text !="":
            self.label_main_text_cont.setText(label_text)
        
        print(wrist_ped)
        

    def joint_defects_data_processing(self, joint_defects, label_text):

        #self.joint_defects_info_coding = {
        #                            "ampute":{},
        #                            "contracture":[],
        #                            }

        if joint_defects["ampute"] != {}:
            for key, value in joint_defects["ampute"].items():
                self.change_color(key, self.file_name, value)
        self.update()
        

        if joint_defects["contracture"] != []:
            self.artic_contacture = joint_defects["contracture"][:]
            for i in joint_defects["contracture"]:
                for button in self.artic_buttons:
                    if i[0] == button.text():
                        text = i[3].split("\n")[:]
                        if i[2] !=0:
                            button.setText(text[0] + "\n" + text[-1].split("(")[0] + i[2])
                        else:
                            button.setText(text[0] + "\n" + text[-1].split("(")[0])
                        button.adjustSize()
                        button.setColor(color_new=i[1])
        #self.get_text_common()
        if label_text !="":
            self.label_main_text_cont.setText(label_text)
        print(joint_defects)



    def moving_close(self, moving):
        self.entering_artilatio[-1].setParent(None)
        self.entering_artilatio = []


    def range_calculate(self):
        text = ""
        key_signal = 0
        normal_range_common = 0
        move_range_common = 0
        wrong_meanings = []
        direction_range = self.entering_artilatio[1:-1] 
        #print(direction_range)
        for direction in direction_range:
            for degree in direction:
                if degree.text() == "":
                    key_signal = 1
        #print(key_signal)
        if key_signal == 0:
            if True:
                percent =[]
                increment=0
                for direction in direction_range:
                    axis_dir = list(self.dict_joints[self.articulatio].keys())[increment]
                    if len(direction)>2:
                        move_range = int(direction[0].text()) - int(direction[1].text()) + int(direction[2].text())
                        normal_range = (self.dict_joints[self.articulatio][axis_dir][0] - 
                            self.dict_joints[self.articulatio][axis_dir][1] + 
                            self.dict_joints[self.articulatio][axis_dir][2])
                    else:
                        move_range = int(direction[1].text()) - int(direction[0].text())
                        normal_range = (self.dict_joints[self.articulatio][axis_dir][1] - 
                            self.dict_joints[self.articulatio][axis_dir][0])
                    increment+=1
                    text += self.text_label_formation(direction= direction, axis_dir=axis_dir) 
                    percent_1 = round(((normal_range - move_range)/normal_range)*100, 2)
                    #print("percent_1:%s" % percent_1)
                    if len(direction) == 3:
                        if move_range <0 or percent_1<0 or ("0" not in [direction[0].text(), direction[1].text(), direction[2].text()]):
                            #print("move_range: %s" %move_range)
                            #print("percent_1: %s" %percent_1)
                            #print("direction: %s" %[direction[0].text(), direction[1].text(), direction[2].text()])
                            wrong_meanings.append(axis_dir[:])
                    else:
                        if move_range <0 or percent_1<0:
                            #print("move_range: %s" %move_range)
                            #print("percent_1: %s" %percent_1)
                            wrong_meanings.append(axis_dir[:])

                    normal_range_common += normal_range
                    move_range_common += move_range
                    percent_1 = round(percent_1, 1)
                #print("wrong_meanings: %s" %wrong_meanings)

                if wrong_meanings == []:
                    percent_average = round(((normal_range_common-move_range_common)/normal_range_common)*100 ,1)

                    print(percent_average)
                    print(text)
                    if percent_average <= 0:
                        if self.artic_contacture != []:
                                for artic in self.artic_contacture:
                                    if artic[0] == self.entering_artilatio[0].text().split("\n")[0]:
                                        self.artic_contacture.pop(self.artic_contacture.index(artic))
                        self.entering_artilatio[0].setText(self.entering_artilatio[0].text().split("\n")[0])
                        #self.color_define(percent=percent_average)
                        self.entering_artilatio[0].setColor(color_new=self.color_define(percent=percent_average))
                        #self.entering_artilatio[0].resize(40, 40)
                        self.entering_artilatio[-1].setParent(None)
                        self.entering_artilatio = []

                    else:
                        
                        if self.entering_artilatio[0].text().split("\n")[0] not in ["Cervicalis","Thoracalis", "Lumbalis"]:
                            text = (self.entering_artilatio[0].text().split("\n")[0] + "\n" + 
                                text + "(" + str(percent_average) +"%, " + self.sum_sign+ " "+
                                str(move_range_common) +self.degree_sign+")")
                            fns = self.fns_calculation(artic= self.entering_artilatio[0].text().split("\n")[0], text=text, percent=percent_average)
                            self.entering_artilatio[0].setText(self.entering_artilatio[0].text().split("\n")[0]+"\n"+str(percent_average) + "%("+ fns +")")
                        else:
                            if self.entering_artilatio[0].text().split("\n")[0] != "Cervicalis":
                                text = (self.entering_artilatio[0].text().split("\n")[0] + "\n" + 
                                    text + "("+ str(percent_average)+"%, всего " +str(move_range_common) +"см)")
                            else:
                                text = (self.entering_artilatio[0].text().split("\n")[0] + "\n" + 
                                    text + "(" + str(percent_average) + "%, " +self.sum_sign+ " "+
                                    str(move_range_common) +self.degree_sign+")")
                            fns=0
                            self.entering_artilatio[0].setText(self.entering_artilatio[0].text().split("\n")[0]+"\n"+str(percent_average) + "%")
                        color = self.color_define(percent=percent_average)
                        
                        self.color_define(percent=percent_average)
                        self.entering_artilatio[0].setColor(color_new=self.color_define(percent=percent_average))
                        self.entering_artilatio[0].adjustSize()
                        #if len(direction_range) == 1:
                        #    self.entering_artilatio[0].resize(self.entering_artilatio[0].size().width(), 60)
                        #elif len(direction_range) == 2:
                        #    self.entering_artilatio[0].resize(self.entering_artilatio[0].size().width(), 60)
                        #elif len(direction_range) == 3:
                        #    self.entering_artilatio[0].resize(self.entering_artilatio[0].size().width(), 60)
                        #    self.entering_artilatio[0].setFont(font_size=10)
                        self.entering_artilatio[-1].setParent(None)
                        
                        inc = 0
                        if self.artic_contacture != []:
                            for artic in self.artic_contacture:
                                #print(self.entering_artilatio)
                                #print("artic:")
                                #print(artic)
                                if artic[0] == self.entering_artilatio[0].text().split("\n")[0]:
                                    artic[1] = color
                                    artic[2] = fns
                                    artic[3] = text
                                    break
                                else:
                                    inc += 1
                                    if len(self.artic_contacture) == inc:
                                        self.artic_contacture.append([self.entering_artilatio[0].text().split("\n")[0], color, fns, text])
                        else:
                            self.artic_contacture.append([self.entering_artilatio[0].text().split("\n")[0], color, fns, text])

                        self.entering_artilatio = []
                        self.label_text_update.emit()
                else:
                    msgBox = QMessageBox()
                    msgBox.setWindowTitle("Warning")
                    msgBox.setText("Некорректно введены значения в полях:\n%s" %self.axis_define(axis=wrong_meanings))
                    msgBox.exec_()

        

        elif key_signal==1:
            msgBox = QMessageBox()
            msgBox.setWindowTitle("Warning")
            msgBox.setText("Некоторые значения не введены")
            msgBox.exec_()
            
            
    def fns_calculation(self, artic, text, percent):
        
       
        functional_positions = {
            "Cervical":{
                "flex": [10,0,10],
                "inclineRignt": [5,0,5],
                "rotRight": [10,0,10]
                },
            "Humeri": {
                "flex": [30,0,0],
                "abdu": [60,0,0],
                "rotExt": [0,0,45]
                },
            "Cubitus": {"flex": [100, 0, 0]},
            "Radioulnaris": {"rotSup": [45, 0, 0]},
            "Carporadialis": {
                #"flex": [>0 and <40,0,0],
                "abdu": [0,0,10]
                },
            "Coxae": {
                "flex": [25,0,0],
                "abdu": [10,0,0],
                "rotExt": [0,0,0]
                },
            "Genus": {"flex": [10, 0, 0]},
            "Talocruralis": {"flexPlant": [10,0,0]},
        }

        bad_position = {
            "Humeri": {
                #"flex": [30,0,0],
                #"abdu": [<40,0,<=0],
                #"rotExt": [0,0,45]
                },
            #"Cubitus": {"flex": [<40, 0, <=0]},
            #"Radioulnaris": {"rotSup": [45, 0, 0]},
            "Carporadialis": {
                #"flex": [>40,0,>40],
                #"abdu": [0,0,10]
                },
            "Coxae": {
                #"flex": [>40,>40,0],
                #"abdu": [10,0,0],
                #"rotExt": [0,0,0]
                },
            #"Genus": {"flex": [>40, >40, 0]},
            #"Talocruralis": {"flexPlant": [>40,>40,0], [0,>10,>10]},
        }
        
        func_pos_axis = {}
        
        


        fns = ""
        position = ""
        artic = artic[:-2]
        print(artic)
        #percent = 
        #print(text)
        text = text.split("\n")[1:-1]
        #print(text)
        move_range = {}
        for axis in text:
            key = axis.split(":")[0]
            value = axis.split(":")[1]
            value_to_add = []
            for val in value.split("/"):
                val_1 = "".join(c for c in val if c.isalnum())
                #val.replace(','," ")
                val_1 = int(val_1)
                value_to_add.append(val_1)
            move_range[key] = value_to_add 

        print("move_range=%s" %move_range)
        flex_contr_percent = 0
        neutral_transition = True
        for key, value in move_range.items():
            if value[1] !=0:
                neutral_transition = False
        
        for key, value in move_range.items():
            print(key, value)
            if key in ["flex","flexPlant", "rotSup"]:
                normal_flex_range = self.dict_joints[artic][key][0] + self.dict_joints[artic][key][2]
                flex_range = value[0]-value[1]+value[2]
                flex_contr_percent = round(((normal_flex_range - flex_range) / normal_flex_range)*100, 2)

        for key, value in move_range.items():
            if artic == "Humeri":
                if key == "flex":
                    if (value[0]>=30 and value[1]<=30):
                        func_pos_axis[key] = 1
                    else:
                        func_pos_axis[key] = 0
                elif key == "abdu":
                    if (value[0]>=60 and value[1]<=60):
                        func_pos_axis[key] = 1
                    elif value[0]<40 or (value[0]==0 and value[1]==0 and value[2]>=0):
                        func_pos_axis[key] = -1
                    else:
                        func_pos_axis[key] = 0
                elif key == "rotExt":
                    if (value[2]>=45 and value[1]<=45):
                        func_pos_axis[key] = 1
                    else:
                        func_pos_axis[key] = 0

            elif artic == "Cubitus":
                if (value[0]>=100 and value[1]<=100):
                    func_pos_axis[key] = 1
                elif value[0]<40 or (value[0]==0 and value[1]==0 and value[2]>=0):
                    func_pos_axis[key] = -1
                else:
                    func_pos_axis[key] = 0
            
            elif artic == "Radioulnaris":
                if (value[0]>=45 and value[1]<=45):
                    func_pos_axis[key] = 1
                else:
                    func_pos_axis[key] = 0

            elif artic=="Carporadialis":
                if key == "flex":
                    if (value[0]>=0 and value[0]<=40):
                        func_pos_axis[key] = 1
                    elif (value[0]>40 and value[1]>40)  or (value[0]==0 and value[1]>40):
                        func_pos_axis[key] = -1
                    else:
                        func_pos_axis[key] = 0
                elif key == "abdu":
                    if value[1]<=10 and value[2]>=10:
                        func_pos_axis[key] = 1
                    else:
                        func_pos_axis[key] = 0
            
            elif artic == "Coxae":
                if key == "flex":
                    if (value[0]>=25 and value[1]<=25):
                        func_pos_axis[key] = 1
                    elif value[0]>40 or (value[0]==0 and value[1]==0 and value[2]>=0):
                        func_pos_axis[key] = -1
                    else:
                        func_pos_axis[key] = 0
                elif key == "abdu":
                    if (value[0]>=10 and value[1]<=10):
                        func_pos_axis[key] = 1
                    elif (value[0]>=25 and value[1]>=25) or (value[0]==0 and value[1]==0 and value[2]>=0):
                        func_pos_axis[key] = -1
                    else:
                        func_pos_axis[key] = 0
                elif key == "rotExt":
                    if value[1]==0:
                        func_pos_axis[key] = 1
                    else:
                        func_pos_axis[key] = 0

            elif artic == "Genus":
                if (value[0]>=10 and value[1]<=10):
                    func_pos_axis[key] = 1
                elif (value[0]>40 and value[1]>40) or (value[0]==0 and value[1]==0 and value[2]>=0):
                    func_pos_axis[key] = -1
                else:
                    func_pos_axis[key] = 0

            elif artic == "Talocruralis":
                if (value[0]>=10 and value[1]<=10):
                    func_pos_axis[key] = 1
                elif (value[0]>40 and value[1]>40) or (value[0]==0 and value[1]>10 and value[2]>10):
                    func_pos_axis[key] = -1
                else:
                    func_pos_axis[key] = 0

        if len(func_pos_axis.keys()) ==3:
            pos_axis = [c for c in func_pos_axis.values()]
            
            if pos_axis[0]==-1 or (pos_axis[1] ==-1 and pos_axis[2] ==-1):
                position = -1
            elif pos_axis[0] ==0 or (pos_axis[1] ==0 and pos_axis[2] ==0):
                position = 0
            elif pos_axis[0] ==1 and ((pos_axis[1] ==-1 and pos_axis[2] ==1) or (pos_axis[1] ==1 and pos_axis[2] ==-1)):
                position = 0
            else:
                position = 1
        else:
            pos_axis = [c for c in func_pos_axis.values()]
            print("pos_axis=%s" %pos_axis)
            position = pos_axis[0]


        print("func_pos_axis=%s" %func_pos_axis)
        print("position=%s" %position)
        print("flex_contr_percent=%s" %flex_contr_percent)
        print("text=%s" %text)
        print("artic=%s" %artic)
        print("percent=%s" %percent)


        if position ==1:
            if percent <=5:
                fns = "НФС0"
            elif (percent>5 and percent<=25) and neutral_transition:
                fns = "НФС0"
            elif (percent>5 and percent<=25) and neutral_transition==False:
                fns = "НФС1"
            elif (percent>25 and percent<=50) and neutral_transition:
                fns = "НФС1"
            elif (percent>25 and percent<=50) and neutral_transition==False:
                fns = "НФС2"
            elif (percent>50 and percent<=75) and flex_contr_percent<=50:
                fns = "НФС2"
            elif (percent>50 and percent<=75) and (flex_contr_percent>50 and flex_contr_percent<=75):
                fns = "НФС3"
            elif (percent>75 and percent<100) and (flex_contr_percent>50 and flex_contr_percent<=75):
                fns = "НФС3"
            elif (percent>75 and percent<100) and (flex_contr_percent>75 and flex_contr_percent<100):
                fns = "НФС4"
            elif percent==100:
                fns = "НФС3"
        elif position ==0:
            if percent<=25:
                fns = "НФС1"
            elif (percent>25 and percent<=50):
                fns = "НФС2"
            elif percent>50 and percent<=75:
                fns = "НФС3"
            elif percent>75 and percent<=100:
                fns = "НФС4"

        elif position ==-1:
            if percent>25 and percent<=50:
                fns = "НФС3"
            elif (percent>50 and percent<=75) and (flex_contr_percent>25 and flex_contr_percent<=50):
                fns = "НФС3"
            elif (percent>50 and percent<=75) and (flex_contr_percent>50 and flex_contr_percent<=75):
                fns = "НФС4"
            elif (percent>75 and percent<100) and (flex_contr_percent>50 and flex_contr_percent<=75):
                fns = "НФС4"
            elif (percent>75 and percent<=100) and (flex_contr_percent>75 and flex_contr_percent<=100):
                fns = "полная утрата функции"

        print("fns=%s" %fns)
      
        return fns

    def color_define(self, percent):
        color = ""
        if percent >=0 and percent <5:
            color = "#DCDCDC"
        elif percent >=5 and percent < 25:
            color = "#B0E0E6"
        elif percent >= 25 and percent < 50:
            color = "#ADFF2F"
        elif percent >= 50 and percent < 75:
            color = "#FFFF00"
        elif percent >= 75:
            color = "#FF4500"

        return color
    

    def axis_define(self, axis):
        text = ""
        for i in axis:
            if i == "flex":
                text+="сг./раз.\n"

            elif i == "inclineRignt":
                 text+="накл.впр./вл.\n"

            elif i =="rotRight":
                 text+="пов.впр./вл.\n"

            elif i =="inclineAnt":
                 text+="выпр./накл.впер.\n"

            elif i =="abdu":
                 text+="отв./прив.\n"

            elif i =="rotExt":
                 text+="рот.нар./вн.\n"

            elif i =="rotSup":
                 text+="суп./прон.\n"

            elif i =="flexPlant":
                 text+="под.сг./раз.\n"
        print(text)
        return text



    def text_label_formation(self, direction, axis_dir):
        
        if direction == "flex":
            axis_dir="сг./раз."

        elif direction == "inclineRignt":
             axis_dir="накл.впр./вл."

        elif direction =="rotRight":
             axis_dir="пов.впр./вл."

        elif direction =="inclineAnt":
             axis_dir="выпр./накл.впер."

        elif direction =="abdu":
             axis_dir="отв./прив."

        elif direction =="rotExt":
             axis_dir="рот.нар./вн."

        elif direction =="rotSup":
             axis_dir="суп./прон."

        elif direction =="flexPlant":
             axis_dir="под.сг./раз."

        text = axis_dir +":"
        for i in direction:
            if axis_dir!="inclineAnt":
                text += i.text() +self.degree_sign + "/"
            else:
                text += i.text() + "см/"
        return text[:-1] + ",\n"

    def movement_wrist_ped(self):
        if self.sender().getColor() == "#808080":
            msgBox_error = QMessageBox()
            msgBox_error.setWindowTitle("Warning")
            msgBox_error.setText("Часть тела не может быть описана - указана, как ампутированная")
            msgBox_error.exec_()
        else:
            button_name = self.sender().text()
            entered_data = self.for_child_info_coding[button_name][:]
            if button_name[-1] == "R":
                side = 0
            else:
                side = 1

            if button_name in ["Wrist R","Wrist L"]:
                self.inner_wrist_window = WristFootWindow(text=side,entered_data=entered_data, button_name=button_name)
                self.inner_wrist_window.move(30,30)
                self.inner_wrist_window.show()
                self.inner_wrist_window.wrist_send.connect(lambda: self.get_text(button_name=button_name))
                
            else:
                self.inner_ped_window = PedFootWindow(text=side, entered_data=entered_data, button_name=button_name)
                self.inner_ped_window.move(30,30)
                self.inner_ped_window.show()

                self.inner_ped_window.ped_send.connect(lambda: self.get_text(button_name=button_name))


            #"Ped L", "Ped R"
            #Ped WINDOW   
        #   pass
    

    def get_text(self, button_name):
        if self.inner_wrist_window != []:
            if button_name[-1] == "L":
                self.wrist_left_text = self.inner_wrist_window.get_wrist_contr_def_text()
            elif button_name[-1] == "R":
                self.wrist_right_text = self.inner_wrist_window.get_wrist_contr_def_text()
            self.for_child_info_coding[button_name][0] = self.inner_wrist_window.ampute_level_coding
            self.for_child_info_coding[button_name][1] = self.inner_wrist_window.art_contr_coding

            if self.inner_wrist_window.ampute_level_coding !={} or self.inner_wrist_window.art_contr_coding !=[]:
                for button in self.artic_buttons:
                #button.resize(button.size().width(), 40)
                    if button.text() == button_name:
                        button.setColor("#B0E0E6")
            else:
                for button in self.artic_buttons:
                #button.resize(button.size().width(), 40)
                    if button.text() == button_name:
                        button.setColor("#ffb4a2")
            self.inner_wrist_window = []

        elif self.inner_ped_window != []:
            if button_name[-1] == "L":
                self.ped_left_text = self.inner_ped_window.get_ped_contr_def_text()
            elif button_name[-1] == "R":
                self.ped_right_text = self.inner_ped_window.get_ped_contr_def_text()

            self.for_child_info_coding[button_name][0] = self.inner_ped_window.ampute_level_coding
            self.for_child_info_coding[button_name][1] = self.inner_ped_window.art_contr_coding
            
            if self.inner_ped_window.ampute_level_coding !={} or self.inner_ped_window.art_contr_coding !=[]:
                for button in self.artic_buttons:
                #button.resize(button.size().width(), 40)
                    if button.text() == button_name:
                        button.setColor("#B0E0E6")
            else:
                for button in self.artic_buttons:
                #button.resize(button.size().width(), 40)
                    if button.text() == button_name:
                        button.setColor("#ffb4a2")
            self.inner_ped_window = []


        self.label_update()
        print(self.for_child_info_coding)

#*******************************TO DO************************************
#self.for_child_info_coding = {
#                                    "Wrist L":[[],[]],
#                                    "Wrist R":[[],[]],
#                                    "Ped L":[[],[]],
#                                    "Ped R":[[],[]],
#                                    } 






    def get_text_common(self):
        text = ""
        for i in [self.ped_left_text, self.ped_right_text, self.wrist_left_text, self.wrist_right_text]:
            if i != "":
                text += i
                text += " "

        print("self.artic_contacture=%s" %self.artic_contacture)
        #print(self.artic_contacture)
        
        if self.artic_contacture !=[]:
            text+="Ограничен объем движений: "

            for artic in self.artic_contacture:
                artic_cont_text = artic[3].split("\n")[:]
                if artic_cont_text[0][-1] =="R":
                    side = "правом"
                    artic_name = self.artic_names_trans[artic_cont_text[0][:-2]]
                elif artic_cont_text[0][-1] =="L":
                    side = "левом"
                    artic_name = self.artic_names_trans[artic_cont_text[0][:-2]]
                else:
                    side = ""
                    artic_name = self.artic_names_trans[artic_cont_text[0]]
                text+="в " + side + " " + artic_name + " - "
                moving_text = artic_cont_text[1:-1]
                for axis_move in moving_text:
                    line = axis_move[:-1].split(":")[:]
                    text+= str(self.axis_define(axis=[line[0]])[:-1]) + " " + line[1] + ", "
                if artic[2]!=0:
                    text=text[:-2] + " " + artic[2] + " " + artic_cont_text[-1] + "; "
                else:
                    text=text[:-2] + " " + artic_cont_text[-1] + "; "

        if self.amputation_level_text !="" and self.artic_contacture !=[]:
            text= text[:-2] + "." + "\n"+ self.amputation_level_text[:-2] + "."
        elif self.amputation_level_text !="" and self.artic_contacture ==[]:
            text+= self.amputation_level_text[:-2] + "."

        

        #print(text)
        return text

    def label_update(self):
        text = self.get_text_common()
        self.label_main_text_cont.setText(text)
        #self.joints_send_info.emit()

    def clear_info(self):
        self.artic_contacture = []
        self.amputation_level_text = ""
        self.amputation_level = {}
        self.ampute_level_coding = {}
        self.checked_zones = []
        self.artic_to_exclude = []


        self.pix = QPixmap.fromImage(self.pix_main)
        self.update()

        self.label_text_update.emit()

        for button in self.artic_buttons:
            if button.getColor() not in ["#ffb4a2","#B0E0E6"]:
                button.setColor("#ffb4a2")
                if len(button.text().split("\n"))>1:
                    button.setText(button.text().split("\n")[0])
                    button.adjustSize()

            elif button.getColor() =="#B0E0E6" and button.text().split("\n")[0] =="Wrist L":
                msgBox = QMessageBox()
                msgBox.setWindowTitle("Warning")
                msgBox.setStandardButtons(QMessageBox.Yes|QMessageBox.No)
                msgBox.setText("Удалить введенные значения в поле 'Wrist L'?")
                result = msgBox.exec_()
                if QMessageBox.Yes == result:
                    self.for_child_info_coding["Wrist L"]=[{},[]]
                    button.setColor("#ffb4a2")
                    self.wrist_left_text = ""

                elif QMessageBox.No == result:
                    continue

            elif button.getColor() =="#B0E0E6" and button.text().split("\n")[0] =="Wrist R":
                msgBox = QMessageBox()
                msgBox.setWindowTitle("Warning")
                msgBox.setStandardButtons(QMessageBox.Yes|QMessageBox.No)
                msgBox.setText("Удалить введенные значения в поле 'Wrist R'?")
                result = msgBox.exec_()
                if QMessageBox.Yes == result:
                    self.for_child_info_coding["Wrist R"]=[{},[]]
                    self.wrist_right_text = ""
                    button.setColor("#ffb4a2")
                    
                elif QMessageBox.No == result:
                    continue

            elif button.getColor() =="#B0E0E6" and button.text().split("\n")[0] =="Ped L":
                msgBox = QMessageBox()
                msgBox.setWindowTitle("Warning")
                msgBox.setStandardButtons(QMessageBox.Yes|QMessageBox.No)
                msgBox.setText("Удалить введенные значения в поле 'Ped L'?")
                result = msgBox.exec_()
                if QMessageBox.Yes == result:
                    self.for_child_info_coding["Ped L"]=[{},[]]
                    self.ped_left_text = ""
                    button.setColor("#ffb4a2")
                    
                elif QMessageBox.No == result:
                    continue

            elif button.getColor() =="#B0E0E6" and button.text().split("\n")[0] =="Ped R":
                msgBox = QMessageBox()
                msgBox.setWindowTitle("Warning")
                msgBox.setStandardButtons(QMessageBox.Yes|QMessageBox.No)
                msgBox.setText("Удалить введенные значения в поле 'Ped R'?")
                result = msgBox.exec_()
                if QMessageBox.Yes == result:
                    self.for_child_info_coding["Ped R"]=[{},[]]
                    self.ped_right_text = ""
                    button.setColor("#ffb4a2")
                elif QMessageBox.No == result:
                    continue
        self.label_update()
    


            

         # Событие отпускания мыши
class CommonBodyDefects(BodyDefects):

    def __init__(self, wrist_ped, joint_defects, label_text, wrist_ped_text, parent=None):
        super(CommonBodyDefects, self).__init__(wrist_ped, joint_defects, label_text, wrist_ped_text, parent=None)
        #self.setupUi(self)



class JointsDefects(QWidget):
    joints_send_info = pyqtSignal()
    def __init__(self):
        super().__init__()
        self.file_name = "body.bmp"
        self.initUI()
        

    def initUI(self):
        self.setWindowTitle ("Контрактуры суставов и дефекты конечностей")
        self.widget = BodyDefects(self.file_name)
        self.widget.label_text_update.connect(self.label_update)
        

        
        scroll = QScrollArea()
        #scroll.setBackgroundRole(QPalette.Dark)
        scroll.setWidget(self.widget)
        
        self.main_box = QHBoxLayout()
        self.main_box.addWidget(scroll)
        
        self.label_main_text_cont = QLabel("Текст")

        self.style_box_text_cont = QGroupBox("Текст")
        self.style_box_text_cont.setStyleSheet('''
            QGroupBox {
                margin-top: 2ex;
            }
            QGroupBox:enabled {
                border: 3px solid #851E1E;
                border-radius: 5px;
            }
            QGroupBox::title {
                subcontrol-origin: margin;
                left: 3ex;
            }
        ''')
        self.group_box_text_cont = QHBoxLayout()
        self.group_box_text_cont.addWidget(self.label_main_text_cont)
        #self.group_box_text_cont.addStretch()
        self.style_box_text_cont.setLayout(self.group_box_text_cont)
        self.main_box.addWidget(self.style_box_text_cont)
        
        
        
        footer = QHBoxLayout()
        self.okButton = PushButton("OK")
        #self.okButton.setStyleSheet('background: rgb(173,255,47);')
        self.okButton.clicked.connect(self.close)
        self.cancelButton = PushButton("Cancel")
        #self.cancelButton.setStyleSheet('background: rgb(173,255,47);')
        self.cancelButton.clicked.connect(self.cancel_info)
        footer.addWidget(self.okButton)
        footer.addWidget(self.cancelButton)

        main = QVBoxLayout(self)
        main.addLayout(self.main_box)
        #main.addWidget(self.label_main)
        main.addLayout(footer)

        #width_text_label = int(self.widget.size().width()) / 2
        #print(width_text_label)
        #self.label_main_text_cont.resize(width_text_label, 100)
        #self.style_box_text_cont.resize(width_text_label, 100)
        #width_main = self.widget.size().width() + width_text_label
        #sizeObject = QDesktopWidget().screenGeometry(-1)
        sizeObject = QDesktopWidget().screenGeometry(-1)
        #self.label_main_text_cont.resize(100, 100)
        self.label_main_text_cont.setWordWrap(True)
        self.label_main_text_cont.setMaximumSize(200, 200)
        self.label_main_text_cont.setMinimumSize(200, 200)
        self.setGeometry(200, 50, self.widget.size().width()+275, self.widget.size().height()+20)
        #self.resize(width_main, (self.height()))
        self.show()
        print(self.label_main_text_cont.size().width())
        
    def sendInfo(self):
        text = self.label_main_text_cont.text()
        return text

    def cancel_info(self):
        self.label_main_text_cont.setText("")
        self.joints_send_info.emit()
        self.close()

    def label_update(self):
        text = self.widget.get_text_common()
        self.label_main_text_cont.setText(text)
        #self.joints_send_info.emit()

