import sys
import pickle
from PyQt5 import QtGui 
from PyQt5.QtCore import Qt, pyqtSignal, QRect, QVariantAnimation, QAbstractAnimation
from PyQt5.QtGui import QPixmap, QPainter, QColor, QFont, QCursor


from PyQt5.QtWidgets import (QApplication, QWidget, QScrollArea, QHBoxLayout, QVBoxLayout, 
                            QDesktopWidget, QPushButton, QDialog, QLabel, QGridLayout, QGroupBox,
                            QLineEdit, QMessageBox, QComboBox, QMenu, QAction)

#from modules.zone_detecting.zone_choosing import ScrollOnPicture
from joints_defects_working import ScrollOnPicture, WristDefects

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


class WristFootWindow(QWidget):
    wrist_send = pyqtSignal(str)
    def __init__(self, text=None, **kwargs):
        super(WristFootWindow,self).__init__(parent)
        
        print("text=%s" %text)

        
        self.text_index = text
        #self.window_kind = x
        if text == 0:
            self.filename = "wrists_r.bmp"

            self.initUI()
        elif text == 1:
            self.filename = "wrists_l.bmp"
            self.initUI()


    def initUI(self):
        self.degree_sign = u'\N{DEGREE SIGN}'

        self.artic_contacture = []
        _var = self.artic_contacture
        self.defect_kind = ""
        
        self.lineEdits_right = []
        self.lineEdits_left = []
        self.lineEdits_up_center = []

        self.label_degree_up_center = []
        self.label_degree_left = []
        self.label_degree_right = []


        self.joints_areas_2_5 = ["пястная кость","ПФС","проксимальная фаланга", "ПМФС", "средняя фаланга", "ДМФС", "дистальная фаланга"]

        self.joints_areas_1 = ["пястная кость","ПФС","проксимальная фаланга", "МФС", "дистальная фаланга"]
        
        self.joints_names = {
            "MCP 1": "1 пястно-фаланговом суставе",
            "IP 1":"1 межфаланговом суставе",
            "MCP 2": "2 пястно-фаланговом суставе", 
            "PIP 2": "2 проксимальном межфаланговом суставе",
            "DIP 2": "2 дистальном межфаланговом суставе",
            "MCP 3": "3 пястно-фаланговом суставе", 
            "PIP 3": "3 проксимальном межфаланговом суставе",
            "DIP 3": "3 дистальном межфаланговом суставе",
            "MCP 4": "4 пястно-фаланговом суставе", 
            "PIP 4": "4 проксимальном межфаланговом суставе",
            "DIP 4": "4 дистальном межфаланговом суставе",
            "MCP 5": "5 пястно-фаланговом суставе", 
            "PIP 5": "5 проксимальном межфаланговом суставе",
            "DIP 5": "5 дистальном межфаланговом суставе",
            }



        self.dict_joints = {
            "MCP": [90,0,20], 
            "PIP": [100,0,0],
            "DIP": [80,0,0],
            "MCP 1": [70,0,0],
            "IP 1" :[90, 0, 20],
            }

        self.artic_weight = {"DIP": 0.15, "PIP": 0.35, "MCP": 0.50, "IP 1": 0.50, "MCP 1": 0.50}

        self.finger_weight = {"1": 0.2, "2": 0.08, "3": 0.075, "4": 0.075, "5": 0.07}


        self.list_normal_move = [
            [110],
            [100],
            [80],
            [70],
            [110],
            ]
        
        self.contracture_up_center = [
            ["","",""],
            [""],
            [""]
        ]
        self.text_up_center = [
            ["шейном отделе позвоночника"],
            ["грудном отделе позвоночника"],
            ["поясничном отделе позвоночника"]
        ]
        self.entering_artilatio = []
        self.work_window = WristDefects(self.filename)
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
        
        self.hbox.addWidget(self.okButton)
        self.hbox.addWidget(self.cancelButton)

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
        self.setWindowTitle("Дефекты и объем движений КИСТЬ")

        screen = QDesktopWidget().screenGeometry(-1)
        
        self.resize(w_pix+40, screen.height()-150)
        self.move(screen.width()/2 - self.width()/2 , 20)
        print (self.size().height())
        print (self.size().width())
        
        self.artic_but_coord = [
        [94, 153], 
        [189, 70], 
        [170, 513], 
        [194, 435], 
        [225, 290], 
        [293, 587], 
        [309, 487], 
        [337, 403], 
        [500, 563], 
        [510, 474],
        [514, 383],
        [635, 474],
        [616, 407], 
        [603, 315],]

        self.artic_buttons = []
        self.artic_names = ["DIP", "PIP", "MCP", "IP"]
        for i in [2,3,4,5]:
            for art in self.artic_names:
                if art !="IP":
                    name = art + " " + str(i)
                    print(name)
                    but = PushButton(self, font_size=10)
                    but.setText(name)
                    self.artic_buttons.append(but)
        but_1 =  PushButton(self,font_size=10)
        but_1.setText("IP 1")
        but_2 =  PushButton(self,font_size=10)
        but_2.setText("MCP 1")
        self.artic_buttons.insert(0, but_1)
        self.artic_buttons.insert(1, but_2)
        

        increment = 0
        for button in self.artic_buttons:
            button.resize(40, 40)
            button.clicked.connect(self.movement_def)
            if self.filename == "wrists_r.bmp":
                button.move(self.artic_but_coord[increment][0], self.artic_but_coord[increment][1])
            else:
                button.move(self.size().width() - self.artic_but_coord[increment][0] - 50, self.artic_but_coord[increment][1])
            increment+=1
        self.show()

    def text_send_method(self):
        text = self.label_main_text_cont + " " + self.label_main_text
        self.wrist_send.emit(text)
        self.close()

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
        if self.work_window.get_text() != "":
            self.label_main_text.setText("Имеется " + self.defect_kind + self.work_window.get_text())
            
            for zone in self.ampute_level:
                if zone == "pp_1":
                    but_name.append("IP 1")

                elif zone == "metacarp_1":
                    but_name.append("IP 1")
                    but_name.append("MCP 1")

                else:
                    if zone[:-2] == "mp":
                        but_name.append("DIP " + zone[-1])
                    elif zone[:-2] == "pp":
                        but_name.append("DIP " + zone[-1])
                        but_name.append("PIP " + zone[-1])
                    elif zone[:-2] == "metacarp":
                        but_name.append("DIP " + zone[-1])
                        but_name.append("PIP " + zone[-1])
                        but_name.append("MCP " + zone[-1])
        else:
            self.label_main_text.setText("")

        for but in self.artic_buttons:
            
            if but.text().split("\n")[0] in but_name:
                but.setColor(color_new="#808080")
                print("artic_contacture: %s" %self.artic_contacture)
                for artic in self.artic_contacture:
                    if but.text().split("\n")[0] == artic[0]:
                        self.artic_contacture.remove(artic)
                        self.text_contr_formation()
                but.setText(but.text().split("\n")[0])
                but.resize(40, 40)
            elif len(but.text().split("\n")) == 1:
                but.setColor(color_new="#ffb4a2")
        
        print("but_name: %s" % but_name)
        print("ampute_level: %s" %self.ampute_level)


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
                


                if len(button_text) <=5:

                    if button_text in ["MCP 1", "IP 1"]:
                        self.articulatio = button_text[:]
                        articulatio_editing = button_text[:]
                    else:
                        self.articulatio = button_text[:-2]
                        articulatio_editing = button_text[:]
                    
                else:
                    if button_text[:5] =="MCP 1":
                        self.articulatio = "MCP 1"
                        articulatio_editing = "MCP 1"
                    elif button_text[:5] == "IP 1\n":
                        self.articulatio = "IP 1"
                        articulatio_editing = "IP 1"
                    else:
                        self.articulatio = button_text[:3]
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
                label.setText("сгиб./разгиб.")
                
                #print(button.x(), button.y())
                #label.move(button.y(), button.x())
                
                text_edit_1 = QLineEdit()
                text_edit_1.resize(40, 30)
                text_edit_1.setPlaceholderText(str(self.dict_joints[self.articulatio][0]))
                text_edit_1.setValidator(QtGui.QIntValidator(0, 100))
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
                text_edit_3.setValidator(QtGui.QIntValidator(0, 100))
                label_3 = QLabel()
                label_3.setText(self.degree_sign)
                self.button_new = PushButton("Ok")
                #button_ok.resize(40, 30)
                self.button_new.clicked.connect(self.range_calculate)
                
                box.addWidget(label)
                box.addWidget(text_edit_1)
                box.addWidget(label_1)
                box.addWidget(text_edit_2)
                box.addWidget(label_2)
                box.addWidget(text_edit_3)
                box.addWidget(label_3)

                box_common.addLayout(box)
                box_common.addWidget(self.button_new)

                moving.setLayout(box_common)
                moving.resize(250,80)

                if (self.filename == "wrists_r.bmp" and articulatio_editing[-1] in ["4","5"]) or (self.filename == "wrists_l.bmp" and articulatio_editing[-1] in ["1","2"]):
                    moving.move(button.x()-moving.width()+40, button.y() + button.height())
                    
                else:
                    moving.move(button.x(), button.y() + button.height())

                self.entering_artilatio = [self.sender(),text_edit_1, text_edit_2, text_edit_3, moving]

                moving.show()
                self.update()
                
            else:
                msgBox = QMessageBox()
                msgBox.setWindowTitle("Warning")
                msgBox.setText("Завершите введение обема движений в текущем суставе")
                msgBox.exec_()
        
    def range_calculate(self):
        text = ""
        if self.entering_artilatio[1].text() and self.entering_artilatio[2].text() and self.entering_artilatio[3].text():
            first = int(self.entering_artilatio[1].text()) 
            second = int(self.entering_artilatio[2].text()) 
            third = int(self.entering_artilatio[3].text())
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
                print(percent)
                if percent <= 0:
                    if self.artic_contacture != []:
                        for artic in self.artic_contacture:
                            if artic[0] == self.entering_artilatio[0].text().split("\n")[0]:
                                self.artic_contacture.pop(self.artic_contacture.index(artic))
                    self.entering_artilatio[0].setText(self.entering_artilatio[0].text().split("\n")[0])
                    self.color_define(percent=percent)
                    self.entering_artilatio[0].setColor(color_new=self.color_define(percent=percent))
                    self.entering_artilatio[0].resize(40, 40)
                    self.entering_artilatio[4].setParent(None)
                    self.entering_artilatio = []
                else:

                    text = (self.entering_artilatio[0].text().split("\n")[0] + "\n" + "с/р:\n"+self.entering_artilatio[1].text()+"/"+ 
                        self.entering_artilatio[2].text() + "/" + self.entering_artilatio[3].text() +"\n"+str(percent) + "%")
                    color = self.color_define(percent=percent)
                    self.entering_artilatio[0].setText(text)
                    self.entering_artilatio[0].setColor(color_new=color)
                    self.entering_artilatio[0].resize(50, 60)
                    self.entering_artilatio[4].setParent(None)
                    inc = 0
                    if self.artic_contacture != []:
                        for artic in self.artic_contacture:
                            print(self.entering_artilatio)
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
            print(self.artic_contacture)
            if self.artic_contacture !=[]:
                self.text_contr_formation()
            elif self.artic_contacture ==[]:
                self.label_main_text_cont.setText("")


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
            color = "#C0C0C0"
        elif percent >=5 and percent < 25:
            color = "#FFDAB9"
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
        if self.filename == "wrists_r.bmp":
            side = "правой"
        elif self.filename == "wrists_l.bmp":
            side = "левой"
        
        text = "Ограничен объем движений в суставах " + side + " кисти: "
        common_wrist_deficit = 0
        if self.artic_contacture !=[]:
            for artic in self.artic_contacture:
                text += self.joints_names[artic[0]]
                text += " сгиб./разгиб.- "
                text += artic[2].split("\n")[2]
                text += "(огр.%s), " %artic[2].split("\n")[3]
                if artic[0] in ["IP 1", "MCP 1"]:
                    common_wrist_deficit += round(float(artic[2].split("\n")[3][:-1]) * self.artic_weight[artic[0]] * self.finger_weight["1"], 2)
                else:
                    common_wrist_deficit += round(float(artic[2].split("\n")[3][:-1]) * self.artic_weight[artic[0][:-2]] * self.finger_weight[artic[0][-1]], 2)
            text += "(всего: %s" %common_wrist_deficit
            text += "% от манипулятивной ф-ии кистей)."
            self.label_main_text_cont.setText(text)
            
            print("common_wrist_deficit: %s" % common_wrist_deficit)
        else:
            self.label_main_text_cont.setText("")



    def get_wrist_contr_def_text (self):
        text = self.label_main_text_cont + " " + self.label_main_text
        return text



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