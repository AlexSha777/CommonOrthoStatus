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
from ped_zone_working import PedDefects

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
        print(color_new)
        self._update_stylesheet(QColor(self.color_main),QColor("black"))
        #self.update()

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
            padding: 4px 4px;
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





class PedFootWindow(QWidget):
    ped_send = pyqtSignal(str)
    text_send = pyqtSignal()
    #text = property(__get_text, __set_text)
    def __init__(self, entered_data, button_name, text=None, **kwargs):
        super().__init__( **kwargs)
        
        print("text=%s" %text)
        print("entered_data=%s" % entered_data)
        self.text_index = text
        #self.window_kind = x
        if text == 0:
            self.filename = "Ped_d.bmp"

            self.initUI()
        elif text == 1:
            self.filename = "Ped_s.bmp"
            self.initUI()
        self.button_name = button_name[:]
        self.entered_data = entered_data[:]
        if entered_data !=[[],[]]:
            self.entered_data_processing(entered_data=entered_data)
        

    def initUI(self):
        self.degree_sign = u'\N{DEGREE SIGN}'
        

        self.artic_contacture = []
        _var = self.artic_contacture
        self.defect_kind = ""
        
        self.ampute_level_coding = {}
        self.art_contr_coding = []

        self.lineEdits_right = []
        self.lineEdits_left = []
        self.lineEdits_up_center = []

        self.label_degree_up_center = []
        self.label_degree_left = []
        self.label_degree_right = []


        self.joints_areas_2_5 = ["пястная кость","ПФС","проксимальная фаланга", "ПМФС", "средняя фаланга", "ДМФС", "дистальная фаланга"]

        self.joints_areas_1 = ["пястная кость","ПФС","проксимальная фаланга", "МФС", "дистальная фаланга"]
        
        self.joints_names = {
            "M 1": "1 плюсне-фаланговом суставе",
            "IP 1":"1 межфаланговом суставе",
            "M 2": "2 плюсне-фаланговом суставе", 
            "PI 2": "2 проксимальном межфаланговом суставе",
            "DI 2": "2 дистальном межфаланговом суставе",
            "M 3": "3 плюсне-фаланговом суставе", 
            "PI 3": "3 проксимальном межфаланговом суставе",
            "DI 3": "3 дистальном межфаланговом суставе",
            "M 4": "4 плюсне-фаланговом суставе", 
            "PI 4": "4 проксимальном межфаланговом суставе",
            "DI 4": "4 дистальном межфаланговом суставе",
            "M 5": "5 плюсне-фаланговом суставе", 
            "PI 5": "5 проксимальном межфаланговом суставе",
            "DI 5": "5 дистальном межфаланговом суставе",
            "Abd/Add": "среднего отдела",
            "Sup/Pron":"среднего отдела", 
            }



        self.dict_joints = {
            "M": [40,0,40], 
            "PI": [50,0,0],
            "DI": [45,0,20],
            "M 1": [35,0,80],
            "IP 1" :[40, 0, 20],
            "Abd/Add": [30,0,45],
            "Sup/Pron": [35,0,15],
            }

        self.artic_weight = {"DI": 0.15, "PI": 0.35, "M": 0.50, "IP 1": 0.50, "M 1": 0.50}

        self.finger_weight = {"1": 0.2, "2": 0.08, "3": 0.075, "4": 0.075, "5": 0.07}

        self.entering_artilatio = []
        self.work_window = PedDefects(self.filename)
        self.work_window.text_changed.connect(self.update_text_label)
        w_pix = self.work_window.frameGeometry().width() 
        
        print(w_pix)
        h_pix = self.work_window.geometry().height()
        
        self.scroll = QScrollArea()
        #scroll.setBackgroundRole(QPalette.Dark)
        self.scroll.setWidget(self.work_window)
        

        height = 0
        vbox = QVBoxLayout(self)
        self.hbox = QHBoxLayout()
        self.label_main_text = QLabel()
        self.label_main_text.setWordWrap(True)

        self.label_main_text_cont = QLabel()
        self.label_main_text_cont.setWordWrap(True)

        self.okButton = PushButton("OK")
        self.okButton.clicked.connect(self.text_send_method)
        
        #self.okButton.setStyleSheet('background: rgb(173,255,47);')
        #self.okButton.clicked.connect(self.sendInfo)
        

        self.cancelButton = PushButton("Cancel")
        
        #self.cancelButton.setStyleSheet('background: rgb(173,255,47);')
        self.cancelButton.clicked.connect(self.close)
        
        self.clearButton = PushButton("Clear")
        self.clearButton.setColor("#DC143C")
        self.clearButton.clicked.connect(self.clear_info)

        self.hbox.addWidget(self.okButton)
        self.hbox.addWidget(self.cancelButton)
        self.hbox.addWidget(self.clearButton)

        vbox.addWidget(self.scroll)
        
        style_box_text = QGroupBox("Текст дефекты")
        style_box_text.setStyleSheet('''
            QGroupBox {
                margin-top: 2ex;
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
        group_box_text = QVBoxLayout()
        self.combo_defect_kind = QComboBox()
        self.combo_defect_kind.addItems(["Выберите вид дефекта", "Травматический", "Врожденный"])
        self.combo_defect_kind.activated[str].connect(self.onActivated)
        group_box_text.addWidget(self.combo_defect_kind)
        group_box_text.addWidget(self.label_main_text)
        style_box_text.setLayout(group_box_text)
        
        vbox.addWidget(style_box_text)

        style_box_text_cont = QGroupBox("Текст контрактуры")
        style_box_text_cont.setStyleSheet('''
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
        group_box_text_cont = QHBoxLayout()
        group_box_text_cont.addWidget(self.label_main_text_cont)
        style_box_text_cont.setLayout(group_box_text_cont)
        
        vbox.addWidget(style_box_text_cont)
        
        vbox.addLayout(self.hbox)
        #self.setLayout(self.grid)
        #self.move(400, 10)
        self.setWindowTitle("Дефекты и объем движений СТОПА")

        screen = QDesktopWidget().screenGeometry(-1)
        
        self.resize(w_pix+40, screen.height()-150)
        self.move(screen.width()/2 - self.width()/2 , 20)
        
        self.artic_but_coord = [
        [453,35],
        [466,105],
        [478, 405], 
        [482, 545], 
        [358, 445], 
        [361, 558], 
        [362, 611], 
        [282, 434], 
        [292, 545], 
        [290, 596], 
        [173, 412], 
        [231, 517],
        [228, 567],
        [81, 364],
        [105, 457], 
        [109, 506],]

        self.artic_buttons = []
        self.artic_names = ["M", "PI", "DI", "IP"]
        for i in [2,3,4,5]:
            for art in self.artic_names:
                if art !="IP":
                    name = art + " " + str(i)
                    but = PushButton(self, font_size=10)
                    but.setText(name)
                    self.artic_buttons.append(but)
        but_1 =  PushButton(self,font_size=10)
        but_1.setText("M 1")
        but_2 =  PushButton(self,font_size=10)
        but_2.setText("IP 1")
        but_3 =  PushButton(self,font_size=10)
        but_3.setText("Abd/Add")
        but_4 =  PushButton(self,font_size=10)
        but_4.setText("Sup/Pron")
        self.artic_buttons.insert(0, but_3)
        self.artic_buttons.insert(1, but_4)
        self.artic_buttons.insert(2, but_1)
        self.artic_buttons.insert(3, but_2)
        

        increment = 0
        for button in self.artic_buttons:
            if button.text() in ["Abd/Add", "Sup/Pron"]:
                pass
            else:
                button.resize(30, 40)
            button.clicked.connect(self.movement_def)
            if self.filename == "Ped_d.bmp":
                button.move(self.artic_but_coord[increment][0], self.artic_but_coord[increment][1])
            else:
                if button.text() in ["Abd/Add", "Sup/Pron"]:
                    button.move(self.size().width() - self.artic_but_coord[increment][0] - button.width(), self.artic_but_coord[increment][1])
                else:
                    button.move(self.size().width() - self.artic_but_coord[increment][0] - 45, self.artic_but_coord[increment][1])
            increment+=1
        self.show()

    def entered_data_processing(self, entered_data):
        if entered_data[0] !={}:
            for key, value in entered_data[0].items():
                self.work_window.change_color(key, self.filename, value[1])

        if entered_data[1] !=[]:
            for i in entered_data[1]:
                self.artic_contacture.append(i[1:])
            for but in self.artic_buttons:
                for artic in self.artic_contacture:
                    if artic[0] == but.text():
                        but.setText(artic[2])
                        but.setColor(self.color_define(float(artic[2].split("\n")[-1][:-1])))

            self.text_contr_formation()
            

        print("entered_data__________:%s" %entered_data)

    def onActivated(self, text):
        if text == "Травматический":
            self.defect_kind = "травматический "
            self.update_text_label()
        elif text == "Врожденный":
            self.defect_kind = "врожденный "
            self.update_text_label()

    def update_text_label(self):
        but_name = []
        self.ampute_level = self.work_window.checked_zones[:]
        self.detail_ampute_level = self.work_window.amputation_level.copy()
        self.detail_ampute_level_point = self.work_window.amputation_level_point.copy()
        if self.ampute_level != []:
            self.label_main_text.setText("Имеется " + self.defect_kind + self.work_window.get_text())
            
            for zone in self.detail_ampute_level.keys():
                if zone[6:] == "cub":
                    but_name.append("M 5")
                    but_name.append("M 4")
                    but_name.append("PI 4")
                    but_name.append("PI 5")
                    but_name.append("DI 4")
                    but_name.append("DI 5")
                    self.ampute_level_coding[zone] = ["", self.detail_ampute_level_point[zone]]
                elif zone[6:] in ["scaph", "sphen"]:
                    for i in ["IP 1", "M 1","M 2", "M 3","PI 2","PI 3","DI 2","DI 3"]:
                        but_name.append(i)

                    self.ampute_level_coding[zone] = ["", self.detail_ampute_level_point[zone]]
                elif zone[6:] in ["tal_calc"]:
                    but_name.append("IP 1")
                    but_name.append("M 1")
                    but_name.append("M 2")
                    but_name.append("M 3")
                    but_name.append("M 4")
                    but_name.append("M 5")
                    but_name.append("PI 2")
                    but_name.append("PI 3")
                    but_name.append("PI 4")
                    but_name.append("PI 5")
                    but_name.append("DI 2")
                    but_name.append("DI 3")
                    but_name.append("DI 4")
                    but_name.append("DI 5")
                    self.ampute_level_coding[zone] = ["", self.detail_ampute_level_point[zone]]

                else:
                    if zone[6:] == "1_ray":
                        #print("self.work_window.ampute_detail : %s" %self.work_window.ampute_detail[zone[6:]])
                        for detail_zone, level in self.work_window.ampute_detail[zone[6:]].items():
                            if self.detail_ampute_level[zone] >= level[0] and self.detail_ampute_level[zone] <= level[1]:
                                self.ampute_level_coding[zone] = [detail_zone, self.detail_ampute_level_point[zone]]
                                if detail_zone in ["dp_base", "pp_caput", "pp_diaf"]:
                                    but_name.append("IP 1")
                                elif detail_zone in ["pp_base", "meta_caput", "meta_diaf", "meta_base"]:
                                    but_name.append("IP 1")
                                    but_name.append("M 1")

                    else:
                        
                        for detail_zone, level in self.work_window.ampute_detail[zone[6:]].items():
                            if self.detail_ampute_level[zone] >= level[0] and self.detail_ampute_level[zone] <= level[1]:
                                self.ampute_level_coding[zone] = [detail_zone, self.detail_ampute_level_point[zone]]
                                if detail_zone in ["mp"]:
                                    but_name.append("DI " + zone[6])
                                elif detail_zone in ["pp_caput", "pp_diaf"]: 
                                    but_name.append("DI " + zone[6])
                                    but_name.append("PI " + zone[6])
                                elif detail_zone in ["pp_base", "meta_caput", "meta_diaf", "meta_base"]:
                                    but_name.append("DI " + zone[6])
                                    but_name.append("PI " + zone[6])
                                    but_name.append("M "+ zone[6])
                   
        else:
            self.label_main_text.setText("")
            self.ampute_level_coding = {}

        for but in self.artic_buttons:
            
            if but.text().split("\n")[0] in but_name:
                but.setColor(color_new="#808080")
                print("artic_contacture: %s" %self.artic_contacture)
                for artic in self.artic_contacture:
                    if but.text().split("\n")[0] == artic[0]:
                        self.artic_contacture.remove(artic)
                        self.text_contr_formation()
                but.setText(but.text().split("\n")[0])
                #but.resize(30, 40)
            elif len(but.text().split("\n")) == 1:
                but.setColor(color_new="#ffb4a2")
        
        #print("but_name: %s" % but_name)
        #print("ampute_level: %s" %self.ampute_level)
        print("ampute_level_coding: %s" %self.ampute_level_coding)
        print("art_contr_coding: %s" %self.art_contr_coding)


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
                


                if len(button_text.split("\n")) <1:

                    if button_text in ["M 1", "IP 1", "Abd/Add", "Sup/Pron"]:
                        self.articulatio = button_text[:]
                        articulatio_editing = button_text[:]
                    else:
                        self.articulatio = button_text[:-2]
                        articulatio_editing = button_text[:]
                    
                else:
                    if button_text.split("\n")[0] in ["M 1", "IP 1", "Abd/Add", "Sup/Pron"]:
                        self.articulatio = button_text.split("\n")[0][:]
                        articulatio_editing = button_text.split("\n")[0][:]
                    else:
                        self.articulatio = button_text.split("\n")[0][:-2]
                        articulatio_editing = button_text.split("\n")[0]
                   
                
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

                box = QHBoxLayout()
                box_common = QVBoxLayout()
                label = QLabel()
                if articulatio_editing == "Abd/Add":
                    label.setText("отвед./привед.")
                elif articulatio_editing == "Sup/Pron":
                    label.setText("супин./пронац.")
                else:
                    label.setText("сгиб./разгиб.")
                
                #print(button.x(), button.y())
                #label.move(button.y(), button.x())
                
                text_edit_1 = QLineEdit()
                text_edit_1.resize(40, 30)
                text_edit_1.setPlaceholderText(str(self.dict_joints[self.articulatio][0]))
                text_edit_1.setValidator(QtGui.QIntValidator(0, self.dict_joints[self.articulatio][0]))
                label_1 = QLabel()
                label_1.setText(self.degree_sign + "/ ")
                text_edit_2 = QLineEdit()
                text_edit_2.resize(40, 30)
                text_edit_2.setPlaceholderText(str(self.dict_joints[self.articulatio][1]))
                text_edit_2.setValidator(QtGui.QIntValidator(0, 100))
                label_2 = QLabel()
                label_2.setText(self.degree_sign + "/ ")
                text_edit_3 = QLineEdit()
                text_edit_3.resize(40, 30)
                text_edit_3.setPlaceholderText(str(self.dict_joints[self.articulatio][2]))
                text_edit_3.setValidator(QtGui.QIntValidator(0, self.dict_joints[self.articulatio][2]))
                label_3 = QLabel()
                label_3.setText(self.degree_sign)
                self.button_new = PushButton("Ok")
                self.button_new_1 = PushButton("Cancel")
                self.button_new.clicked.connect(self.range_calculate)
                #button_ok.resize(40, 30)
                
                box.addWidget(label)
                box.addWidget(text_edit_1)
                box.addWidget(label_1)
                box.addWidget(text_edit_2)
                box.addWidget(label_2)
                box.addWidget(text_edit_3)
                box.addWidget(label_3)

                box_common.addLayout(box)

                box_buttons = QHBoxLayout()
                box_buttons.addWidget(self.button_new)
                box_buttons.addWidget(self.button_new_1)
                box_common.addLayout(box_buttons)

                moving.setLayout(box_common)
                moving.resize(250,80)

                if (self.filename == "Ped_d.bmp" and articulatio_editing[-1] in ["1","2", "n", "d"]) or (self.filename == "Ped_s.bmp" and articulatio_editing[-1] in ["4","5"]):
                    moving.move(button.x()-moving.width()+button.width(), button.y() + button.height())
                    
                else:
                    moving.move(button.x(), button.y() + button.height())

                self.entering_artilatio = [self.sender(),text_edit_1, text_edit_2, text_edit_3, moving]

                moving.show()
                
                self.button_new_1.clicked.connect(self.moving_close)
                self.update()
                
            else:
                msgBox = QMessageBox()
                msgBox.setWindowTitle("Warning")
                msgBox.setText("Завершите введение обема движений в текущем суставе")
                msgBox.exec_()
    
    def moving_close(self):
        self.entering_artilatio[-1].setParent(None)
        self.entering_artilatio = []


    def range_calculate(self):
        text = ""
       

        if self.entering_artilatio[1].text() and self.entering_artilatio[2].text() and self.entering_artilatio[3].text():
             
            first = int(self.entering_artilatio[1].text()) 
            second = int(self.entering_artilatio[2].text()) 
            third = int(self.entering_artilatio[3].text())
            if 0 in [first, second, third]:
                move_range = first - second + third
                if move_range<0:
                    msgBox = QMessageBox()
                    msgBox.setWindowTitle("Warning")
                    msgBox.setText("Неправильно введен объем движений")
                    msgBox.exec_()
                else:
                    normal_range = self.dict_joints[self.articulatio][0] - self.dict_joints[self.articulatio][1] + self.dict_joints[self.articulatio][2]
                    percent = ((normal_range - move_range)/normal_range)*100
                    percent = round(percent, 1)
                    #print(percent)
                    if percent <= 0:
                        if self.artic_contacture != []:
                            for artic in self.artic_contacture:
                                if artic[0] == self.entering_artilatio[0].text().split("\n")[0]:
                                    self.artic_contacture.pop(self.artic_contacture.index(artic))
                        self.entering_artilatio[0].setText(self.entering_artilatio[0].text().split("\n")[0])
                        self.color_define(percent=percent)
                        self.entering_artilatio[0].setColor(color_new=self.color_define(percent=percent))
                        #self.entering_artilatio[0].resize(40, 40)
                        self.entering_artilatio[4].setParent(None)
                        self.entering_artilatio = []
                    else:

                        text = (self.entering_artilatio[0].text().split("\n")[0] + "\n" + "m_r:\n"+self.entering_artilatio[1].text()+"/"+ 
                            self.entering_artilatio[2].text() + "/" + self.entering_artilatio[3].text() +"\n"+str(percent) + "%")
                        color = self.color_define(percent=percent)
                        self.entering_artilatio[0].setText(text)
                        self.entering_artilatio[0].setColor(color_new=color)
                        #self.entering_artilatio[0].resize(50, 60)
                        self.entering_artilatio[4].setParent(None)
                        inc = 0
                        if self.artic_contacture != []:
                            for artic in self.artic_contacture:
                                
                                print("artic:")
                                print(artic)
                                if artic[0] == self.entering_artilatio[0].text().split("\n")[0]:
                                    artic[1] = color
                                    artic[2] = text
                                    break
                                else:
                                    inc += 1
                                    if len(self.artic_contacture) == inc:
                                        self.artic_contacture.append([self.entering_artilatio[0].text().split("\n")[0], color, text])
                                        


                        else:
                            self.artic_contacture.append([self.entering_artilatio[0].text().split("\n")[0], color, text])
                        self.entering_artilatio = []
                
                self.text_contr_formation()
                
            else:
                msgBox = QMessageBox()
                msgBox.setWindowTitle("Warning")
                msgBox.setText("Неправильно введен объем движений:\nНет '0' положения среди введенных значений!!!")
                msgBox.exec_()


        else:
            msgBox = QMessageBox()
            msgBox.setWindowTitle("Warning")
            msgBox.setText("Введите объем движений")
            msgBox.exec_()

    def color_get(self, text):
        if self.artic_contacture != []:
            for artic in self.artic_contacture:
                if artic[0] == text:
                    color = artic[1]
        return color

    def color_define(self, percent):
        color = ""
        text = ""
        if percent >0 and percent <5:
            color = "#DCDCDC"
        elif percent >=5 and percent < 25:
            color = "#B0E0E6"
        elif percent >= 25 and percent < 50:
            color = "#ADFF2F"
        elif percent >= 50 and percent < 75:
            color = "#FFFF00"
        elif percent >= 75:
            color = "#FF4500"
        elif percent <= 0:
            color = "#ffb4a2"

        return color
    
    def text_contr_formation(self):
        
        self.art_contr_coding = []

        if self.filename == "Ped_d.bmp":
            side = "правой"
        elif self.filename == "Ped_s.bmp":
            side = "левой"
        print("artic_contacture=%s" %self.artic_contacture)
        text = "Ограничен объем движений в суставах " + side + " стопы: "
        common_wrist_deficit = 0
        if self.artic_contacture !=[]:
            for artic in self.artic_contacture:
                artic_to_save = artic[:]
                artic_to_save.insert(0, self.filename[:5])
                self.art_contr_coding.append(artic_to_save)
                text += self.joints_names[artic[0]]
                if artic[0] == "Abd/Add":
                    text += " отвед./привед.- "
                elif artic[0] == "Sup/Pron":
                    text += " супин./пронац.- "
                else:
                    text += " сгиб./разгиб.- "
                text += artic[2].split("\n")[2]
                text += "(огр.%s), " %artic[2].split("\n")[3]
                #if artic[0] in ["IP 1", "MCP 1"]:
                #    common_wrist_deficit += round(float(artic[2].split("\n")[3][:-1]) * self.artic_weight[artic[0]] * self.finger_weight["1"], 2)
                #else:
                #    common_wrist_deficit += round(float(artic[2].split("\n")[3][:-1]) * self.artic_weight[artic[0][:-2]] * self.finger_weight[artic[0][-1]], 2)
            #text += "(всего: %s" %common_wrist_deficit
            #text += "% от манипулятивной ф-ии кистей)."
            self.label_main_text_cont.setText(text)

            
            #print("common_wrist_deficit: %s" % common_wrist_deficit)
        else:
            self.label_main_text_cont.setText("")

        print("art_contr_coding: %s" %self.art_contr_coding)
        print("ampute_level_coding: %s" %self.ampute_level_coding)


    def text_send_method(self):
        self.ped_send.emit(self.button_name)
        self.close()

    def get_ped_contr_def_text(self):
        if self.label_main_text_cont.text()=="" and self.label_main_text.text()=="":
            text = ""
        elif self.label_main_text_cont.text()=="" and self.label_main_text.text()!="":
            text = self.label_main_text.text()
        elif self.label_main_text_cont.text()!="" and self.label_main_text.text()=="":
            text = self.label_main_text_cont.text()
        else:
            text = self.label_main_text_cont.text() + " " + self.label_main_text.text()
        
        return text

    def clear_info(self):
        print("artic_contacture=%s" %self.artic_contacture)
        if self.artic_contacture !=[]:
            for artic in self.artic_contacture:
                print("artic=%s" %artic)
                for but in self.artic_buttons:
                    if artic[0] == but.text().split("\n")[0]:
                        but.setColor(color_new="#808080")
                        but.setText(artic[0])
                        but.resize(40, 40)

        self.work_window.picture_clear()
        self.ampute_level_coding = {}
        self.art_contr_coding = []
        self.artic_contacture = []
        self.update_text_label()
        self.text_contr_formation()

    def btn_to_close(self):
        name = "modules/joints_text"
        text = self.label_main_text.text()
        text = text[:-1] + "."
        
        with open(name + '.pkl', 'wb') as f:
            pickle.dump(text, f, pickle.HIGHEST_PROTOCOL)
        self.joints_send_info.emit()

        self.close()
        
        return self.label_main_text.text()

#    def __set_text(self, text):
#        self.__text = text
#        print("Set X")

#    def __get_text(self):
#        print("Get X")
#        return self.__text

    def wrist_move(self):
        index = self.dict_wrist_foot.index(self.sender())
        print(index)

    def foot_move(self):
        index = self.dict_wrist_foot.index(self.sender())
        print(index)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    
    form = EdemaWindow()
    form.show()
    sys.exit(app.exec_())