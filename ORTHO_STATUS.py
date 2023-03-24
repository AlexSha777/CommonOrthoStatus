#!/usr/bin/python3
# -*- coding: utf-8 -*-

import sys
import os
import pickle
import logging
import time
import stat
from PyQt5.QtWidgets import (QWidget, QTextEdit, QPushButton, QScrollArea, QScrollBar, QSizePolicy,
    QHBoxLayout, QVBoxLayout, QApplication, QLabel, QRadioButton, QButtonGroup, QComboBox, QInputDialog, 
    QGridLayout, QGroupBox, QMessageBox, QDesktopWidget, QFileDialog, QTabWidget)
from PyQt5.QtCore import QVariant, QEvent, QPoint
from PyQt5.QtCore import (Qt, pyqtSignal, QRect, QVariantAnimation,QEasingCurve, QAbstractAnimation, 
                        QPropertyAnimation, pyqtProperty)
from PyQt5.QtGui import   QPainter ,QPixmap, QImage, QColor, QPen, QCursor, QTextCharFormat, QTextCursor, QIcon

from edema_new import EdemaWindow
from hyperemia import HyperemiaWindow
from wound import WoundWindow
from algia import AlgiaWindow
from abrasion import AbrasionWindow
from bruise import BruiseWindow
from pustule import PustuleWindow
from scar import ScarWindow

from radius import RadiusWindow
from lenght import LenghtWindow
from axis_deformity import AxisWindow
from pathol_mobility import PatholMobilWindow


from joints_defects_working import  BodyDefects
from patological import PatologicalWindow
from vertebra_deformity import VertebraWindow

from common_status import Common_status
from common_status_repeated import Common_repeated
from consultation import Consult



class PushButton(QPushButton):
    

    def __init__(self, parent=None,font_size=None, child_windows=None):
        super().__init__(parent)
        
        #if self.color_ap == "":
        #    self._update_stylesheet(QColor(self.color_main), QColor("black"))
        #else:
        #    self._update_stylesheet(QColor(self.color_ap), QColor("black"))
        self.parent = parent
        self._color = "#ffb4a2"
        self._color_new = "#A64A35"
        self._font_size = 14
        self._child_windows = False
        self.setCursor(QCursor(Qt.PointingHandCursor))
        
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
        
        if value == "#B4B4B4": 
            color_new = "#D2D2D2"

        elif value == "#adff2f":
            color_new = "#6AA60F"
        elif value =="#ffb4a2":
            color_new = "#A64A35"

        elif value =="#A64A35":
            color_new = "#ffb4a2"

        elif value =="":
            color_new = ""
        elif value == "#fa8090":
            color_new = "#BB7780"
        
        elif value == "#FF7373":
            color_new = "#BF3030"

        elif value == "#FF4040":
            color_new = "#BF3030"

        elif value == "#BF3030":
            color_new = "#FF7373"


        self._color_new = color_new
        self._update_stylesheet(QColor(self._color),QColor("black"))

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

    @pyqtProperty(bool)
    def childWindows(self):
        return self._child_windows

    @childWindows.setter
    def childWindows(self, value):
        self._child_windows = value

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
            padding: 4px 8px;
            text-align: center;
            text-decoration: none;
            font-size: %spx;
            border-radius: 8px;
            margin: 4px 2px;
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

    def mousePressEvent(self, event):
        
        if self._child_windows:
            msg = QMessageBox()
            msg.setWindowTitle("Информация")
            msg.setText("Закончите работу с открытым окном!!!")
            msg.setIcon(QMessageBox.Information)
            center = [QDesktopWidget().screenGeometry(-1).width()/2, QDesktopWidget().screenGeometry(-1).height()/2] 
            msg.show()
            msg.move(center[0],center[1])
            msg.exec_()
            print('!!!!!!!!!mousePressEvent!!!!!!!!!!!!!!!!!!', event.x(), event.y(),)
            return None
        
        elif self._child_windows == False:
            print('mousePressEvent', event.x(), event.y(),)
            return QPushButton.mousePressEvent(self, event)

class PushButtonCombo(PushButton):
    

    def __init__(self, parent=None,font_size=None, child_windows=None):
        super().__init__(parent)
        
        #if self.color_ap == "":
        #    self._update_stylesheet(QColor(self.color_main), QColor("black"))
        #else:
        #    self._update_stylesheet(QColor(self.color_ap), QColor("black"))


    def _update_stylesheet(self, background, foreground):

        self.setStyleSheet(
            """
        QPushButton{
            background-color: %s;
            border: none;
            color: %s;
            text-align: center;
            text-decoration: none;
            font-size: %spx;
            border-radius: 2px;
            min-height: 14 px;
            padding: 2px 2px;
        }
        """
            #margin: 0.5px 0.5px;
            % (background.name(), foreground.name(), self._font_size)
        )

class PushButton_MainCombo(PushButton):
    

    def __init__(self, parent=None,font_size=None, child_windows=None):
        super().__init__(parent)
        
        #if self.color_ap == "":
        #    self._update_stylesheet(QColor(self.color_main), QColor("black"))
        #else:
        #    self._update_stylesheet(QColor(self.color_ap), QColor("black"))


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
            min-height: 20 px;
            border: 2px solid #B4B4B4;
        }
        """
            #margin: 0.5px 0.5px;
            % (background.name(), foreground.name(), self._font_size)
        )



class ComboBox(QComboBox):
    def __init__(self, parent=None,font_size=None, child_windows=None):
        super().__init__(parent)
        self.setStyleSheet("""
            QComboBox {
                border: 1px solid gray;
                border-radius: 3px;
                padding: 1px 18px 1px 3px;
                min-width: 6em;
            }


            QComboBox:drop-down {
                subcontrol-origin: padding;
                subcontrol-position: top right;
                width: 15px;

                border-left-width: 1px;
                border-left-color: darkgray;
                border-left-style: solid; /* just a single line */
                border-top-right-radius: 3px; /* same radius as the QComboBox */
                border-bottom-right-radius: 3px;
            }

            QComboBox:down-arrow:on { /* shift the arrow when popup is open */
                top: 1px;
                left: 1px;
            }
            """)


class RadioButton(QRadioButton):

    def __init__(self, parent=None,font_size=None):
        super().__init__(parent)
        self._color = "#FFFFFF"
        self._color_new = "#B4B4B4"
        self._font_size = 14
        self._child_windows = False
        self._update_stylesheet(QColor(self._color),QColor("black"))
        self.setCursor(QCursor(Qt.PointingHandCursor))
        
        self._animation = QVariantAnimation(
            startValue=QColor(self._color_new),
            endValue=QColor(self._color),
            valueChanged=self._on_value_changed,
            duration=400,
        )

    
        
    def _update_stylesheet(self, background, foreground):
        self.setStyleSheet( """
            QRadioButton{
                background-color: %s;
                border: none;
                color: %s;
                padding: 4px 8px;
                text-align: center;
                text-decoration: none;
                font-size: %spx;
                border-radius: 8px;
                margin: 4px 2px;
                min-height: 20 px;
                }"""
                 % (background.name(), foreground.name(), self._font_size))
    
    @pyqtProperty(bool)
    def childWindows(self):
        return self._child_windows

    @childWindows.setter
    def childWindows(self, value):
        self._child_windows = value

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

    def mousePressEvent(self, event):
        """
        if self._child_windows:
            msg = QMessageBox()
            msg.setWindowTitle("Информация")
            msg.setText("Закончите работу с открытым окном!!!")
            msg.setIcon(QMessageBox.Information)
            center = QPoint(self.geometry().center().x(), self.geometry().center().y())
            msg.show()
            msg.move(center)
            msg.exec_()
            print('!!!!!!!!!mousePressEvent!!!!!!!!!!!!!!!!!!', event.x(), event.y(),)
            return None
        elif self._child_windows == False:
            print('mousePressEvent', event.x(), event.y(),)
            return QRadioButton.mousePressEvent(self, event)
        """
        print('mousePressEvent', event.x(), event.y(),)
        return QRadioButton.mousePressEvent(self, event)

class TabWidget(QTabWidget):

    def __init__(self, parent=None, child_windows=None):
        super().__init__(parent)
        self._child_windows=False

    @pyqtProperty(bool)
    def childWindows(self):
        return self._child_windows

    @childWindows.setter
    def childWindows(self, value):
        self._child_windows = value
    
    


class Example(QWidget):

    def __init__(self):
        super().__init__()
        self.logger = logging.getLogger("MAIN_APP.MAIN_class")
        self.initUI()


    def initUI(self):
        
        self.main_text_dict = {
                            "position": "активное",
                            "mobility": ["самостоятельное", "", "", "", "" ],
                            "edema": "",
                            "algia": "",
                            "hyperemia": "",
                            "wound": "",
                            "abrasion": "",
                            "bruise": "",
                            "pustule": "",
                            "scar": "",
                            "radius": "",
                            "joints": "",
                            "joints_defects": "",
                            "lenght_extr": "Одинаковая",
                            "axis_extr": "Нормальная",
                            "patol_mob": "Нет",
                            "vert_deform": "",
                            "patology": "",
                            }
        
        self.soft_tissue_zones ={
                            "edema": [],
                            "algia": [],
                            "hyperemia": [],
                            "wound": [],
                            "abrasion": [],
                            "bruise": [],
                            "pustule": [],
                            "scar": [],
                            "tumor": [],
                            }



        self.wrist_ped_info_coding = {
                                    "Wrist L":[{},[]],
                                    "Wrist R":[{},[]],
                                    "Ped L":[{},[]],
                                    "Ped R":[{},[]],
                                    } 
        
        self.joint_defects_info_coding = {
                                    "ampute":{},
                                    "contracture":[],
                                    }
        self.wrist_ped_text = ["","","",""]
        



        self.chapters_colors = {
            "position":"#f0f0f0",
            "mobility": "#FF9999",
            "radius": "#FF99FF",
            "algia": "#B5B5B5",
            "edema": "#FFC7AC",
            "hyperemia": "#FF9999",
            "wound": "#FF3F3F",
            "abrasion": "#B63D3D",
            "bruise":"#B75EAF",
            "pustule": "#FFB140",
            "scar": "#FFD37A",
            "wrist_ped_joints_defects": "#99CCFF",
            "lenght_extremities": "#FFF800",
            "axis_extremities": "#E567B1",
            "vert_deform":"#FF9340",
            "pathol_mobil": "#FFE591",
            "pathology_formations": "#A6A0FF",
            }


        self.patology_info_coding = []

        self.smth_changed = False
        
        self.all_buttons = []
        
        self.combo_box_new = None
        self.button_pressed = ""

        self.inner_axis = ""
        self.inner_vertebra = ""
        self.inner_lenght = ""
        self.inner_patolog = ""
        self.inner_joints = ""
        self.inner_radius = ""
        self.inner_wound = ""
        self.inner = ""
        self.inner_algia =""
        self.inner_hyperemia = ""
        self.inner_bruise = ""
        self.inner_abrasion = ""
        self.inner_pustule = ""
        self.inner_scar = ""
        

        
        print(self.main_text_dict.items())

        self.okButton = PushButton("Текс для вставки")
        self.all_buttons.append(self.okButton)
        self.okButton.color = "#adff2f"
        self.okButton.clicked.connect(self.status_build)
        self.text_area = QTextEdit()
        self.text_area.setStyleSheet('''font-size: 12px;''')
        self.copy_button = PushButton(self.text_area)
        self.copy_button.setText("Копировать текст")
        self.copy_button.clicked.connect(self.text_coping)
        self.copy_button.color = "#f0f0f0"

        self.save_button = PushButton(self.text_area)
        self.save_button.setText("Сохранить текст в файл")
        self.save_button.clicked.connect(self.text_saving)
        self.save_button.color = "#f0f0f0"

        self.position = QVBoxLayout()
        name_pos_label = QLabel("Положение пациента")
        name_pos_label.setStyleSheet("font-size: 14px;")
        self.position.addWidget(name_pos_label, alignment=Qt.AlignHCenter)
        
        position_variant = QHBoxLayout()
        
        
        group = QButtonGroup()

        
        RB_po_1 = RadioButton("активное", font_size=10)
        self.all_buttons.append(RB_po_1)
        RB_po_1.setChecked(True)
        RB_po_2 = RadioButton("пассивное", font_size=10)
        self.all_buttons.append(RB_po_2)
        RB_po_3 = RadioButton("вынужденное", font_size=10)
        self.all_buttons.append(RB_po_3)
        RB_po_1.toggled.connect(self.check_patient_position)
        RB_po_2.toggled.connect(self.check_patient_position)
        RB_po_3.toggled.connect(self.check_patient_position)
        position_variant.addWidget(RB_po_1)
        position_variant.addStretch()
        position_variant.addWidget(RB_po_2)
        position_variant.addStretch()
        position_variant.addWidget(RB_po_3)
        self.position.addLayout(position_variant)

        self.mobility_layout = QVBoxLayout()
        name_mob_label = QLabel("Способность передвигаться")
        name_mob_label.setStyleSheet("font-size: 14px;")
        self.mobility_layout.addWidget(name_mob_label, alignment=Qt.AlignHCenter)
        mobility_hor = QHBoxLayout()
        mobility_hor_1_level = QVBoxLayout()
        mobility_hor_2_level = QVBoxLayout()
        mobility_hor_3_level = QVBoxLayout()

        self.Mob_var_Button_1 = PushButton("самостоятельное")
        self.all_buttons.append(self.Mob_var_Button_1)
        self.Mob_var_Button_1.color ="#f0f0f0"
        self.Mob_var_Button_1.clicked.connect(self.mobility)
        self.Mob_var_Button_1_1 = PushButton("с дополнительной опорой")
        self.all_buttons.append(self.Mob_var_Button_1_1)
        self.Mob_var_Button_1_1.color ="#f0f0f0"
        self.Mob_var_Button_1_1.clicked.connect(self.mobility_level_2)
        self.Mob_var_Button_1_2 = PushButton("без дополнительной опоры")
        self.all_buttons.append(self.Mob_var_Button_1_2)
        self.Mob_var_Button_1_2.color ="#f0f0f0"
        self.Mob_var_Button_1_2.clicked.connect(self.mobility_level_2)
        self.Mob_var_Button_1_1.hide()
        self.Mob_var_Button_1_2.hide()
        self.combobox_mobility_helpers = PushButton_MainCombo("-------")
        self.all_buttons.append(self.combobox_mobility_helpers)
        self.combobox_mobility_helpers.color = "#B4B4B4"
        self.combobox_mobility_helpers.setObjectName("helpers")
        helpers = (
            "-------",
            "трость",
            "костыли локтевые",
            "костыли подмышечные",
            "ходунки",
            )
        self.combobox_mobility_helpers.clicked.connect(lambda: self.combobox_formation(items=helpers))
        self.combobox_mobility_helpers.hide()

        self.label_combobox_mobility_helpers = QLabel("Средства опоры:", parent = self.combobox_mobility_helpers)
        self.label_combobox_mobility_helpers.hide()

        self.combobox_gait = PushButton_MainCombo("-------")
        self.all_buttons.append(self.combobox_gait)
        self.combobox_gait.color = "#B4B4B4"
        self.combobox_gait.setObjectName("gait")
        gait_type = (
            "-------",
            "хромающая на левую ногу",
            "хромающая на правую ногу",
            "с переразгибанием в коленном суставе",
            "«утиная»",
            "с выраженным лордозом в поясничной области",
            "«перонеальная» походка - односторонний степаж",
            "«перонеальная» походка - двусторонний степаж",
            "«гемипаретическая»",
            "атактическая мозжечковая",
            "атактическая штампующая («табетическая»)",
            "атактическая при вестибулярном симптомокомплексе",
            "параспастическая",
            "спастико-атактическая",
            "гипокинетическая (шаркающая)",
            "апраксическая",
            "гиперкинетическая походка",
            "дисбазическая при умственной отсталости",
            "дисбазическая смешанного происхождения",
            "дисбазическая ятрогенная",
            "дисбазическая, вызванная болью",
            "идиопатическая сенильная дисбазия",
            "идиопатическая прогрессирующая «фризинг-дисбазия»"
            )
        #self.combobox_gait.addItems(gait_type)
        #self.combobox_gait.setMaxVisibleItems(7)
        #self.combobox_gait.setFixedWidth(200)
        self.combobox_gait.clicked.connect(lambda: self.combobox_formation(items=gait_type))
        self.combobox_gait.hide()

        self.label_combobox_gait = QLabel("Походка:", parent = self.combobox_gait)
        self.label_combobox_gait.hide()

        self.combobox_gait_speed = PushButton_MainCombo("-------")
        self.all_buttons.append(self.combobox_gait_speed)
        self.combobox_gait_speed.color = "#B4B4B4"
        self.combobox_gait_speed.setObjectName("gait_speed")
        gait_speed = (
            "-------",
            "не изменен",
            "легко снижен",
            "умеренно снижен",
            "выраженно снижен"
            )
        self.combobox_gait_speed.clicked.connect(lambda: self.combobox_formation(items=gait_speed))
        self.combobox_gait_speed.hide()

        self.label_combobox_gait_speed = QLabel("Темп ходьбы:", parent = self.combobox_gait_speed)
        self.label_combobox_gait_speed.hide()

        #self.Mob_var_Button_1.clicked.connect(self.)


        self.Mob_var_Button_2 = PushButton("не передвигается")
        self.all_buttons.append(self.Mob_var_Button_2)
        self.Mob_var_Button_2.color = "#f0f0f0"
        self.Mob_var_Button_2.clicked.connect(self.mobility)
        self.Mob_var_Button_2_1 = PushButton("лежит в постеле не встает")
        self.all_buttons.append(self.Mob_var_Button_2_1)
        self.Mob_var_Button_2_1.color ="#f0f0f0"
        self.Mob_var_Button_2_1.clicked.connect(self.mobility_level_2_2)
        self.Mob_var_Button_2_2 = PushButton("присаживается в постеле")
        self.all_buttons.append(self.Mob_var_Button_2_2)
        self.Mob_var_Button_2_2.color ="#f0f0f0"
        self.Mob_var_Button_2_2.clicked.connect(self.mobility_level_2_2)
        self.Mob_var_Button_2_3 = PushButton("передвигается в инвалидном кресле-каталке")
        self.all_buttons.append(self.Mob_var_Button_2_3)
        self.Mob_var_Button_2_3.color ="#f0f0f0"
        self.Mob_var_Button_2_3.clicked.connect(self.mobility_level_2_2)
        self.Mob_var_Button_2_4 = PushButton("присаживается в постеле и стоит у кровати")
        self.all_buttons.append(self.Mob_var_Button_2_4)
        self.Mob_var_Button_2_4.color ="#f0f0f0"
        self.Mob_var_Button_2_4.clicked.connect(self.mobility_level_2_2)
        self.Mob_var_Button_2_1.hide()
        self.Mob_var_Button_2_2.hide()
        self.Mob_var_Button_2_3.hide()
        self.Mob_var_Button_2_4.hide()

        mobility_hor_1_level.addWidget(self.Mob_var_Button_1)
        mobility_hor_1_level.addWidget(self.Mob_var_Button_2)
        mobility_hor_2_level.addWidget(self.Mob_var_Button_1_1)
        mobility_hor_2_level.addWidget(self.Mob_var_Button_1_2)
        mobility_hor_2_level.addWidget(self.Mob_var_Button_2_1)
        mobility_hor_2_level.addWidget(self.Mob_var_Button_2_2)
        mobility_hor_2_level.addWidget(self.Mob_var_Button_2_3)
        mobility_hor_2_level.addWidget(self.Mob_var_Button_2_4)
        mobility_hor_3_level.addWidget(self.label_combobox_mobility_helpers)
        mobility_hor_3_level.addWidget(self.combobox_mobility_helpers)
        mobility_hor_3_level.addWidget(self.label_combobox_gait)
        mobility_hor_3_level.addWidget(self.combobox_gait)
        mobility_hor_3_level.addWidget(self.label_combobox_gait_speed)
        mobility_hor_3_level.addWidget(self.combobox_gait_speed)
        mobility_hor.addLayout(mobility_hor_1_level)
        mobility_hor.addLayout(mobility_hor_2_level)
        mobility_hor.addLayout(mobility_hor_3_level)
        self.mobility_layout.addLayout(mobility_hor)
        
        
        
        soft_tissue = QGridLayout()
        self.soft_tissue_layout = QVBoxLayout()
        
        self.algia = QVBoxLayout()
        self.label_algia = QLabel("Боль")
        
        self.label_algia.setStyleSheet('''
            font-weight: bold;
            font-size: 12px;
            ''')
        
        self.plus_button_algia = PushButton("Добавить")
        self.all_buttons.append(self.plus_button_algia)
        self.plus_button_algia.clicked.connect(self.algia_window)
        self.plus_button_algia.color = "#ffb4a2"
        self.clear_button_algia = PushButton("Очистить")
        self.clear_button_algia.setObjectName("clear_button_algia")
        self.all_buttons.append(self.clear_button_algia)
        self.clear_button_algia.color = '#fa8090'
        self.clear_button_algia.clicked.connect(self.clear_chapter)
        self.label_algia_info = QLabel()
        self.label_algia_info.setWordWrap(True)
        self.algia.addWidget(self.label_algia)
        self.algia.addWidget(self.label_algia_info)
        self.algia.addWidget(self.plus_button_algia)
        self.algia.addWidget(self.clear_button_algia)

        self.edema = QVBoxLayout()
        self.label_edema = QLabel("Отёк")
        self.label_edema.setStyleSheet('''
            font-weight: bold;
            font-size: 12px;
            ''')
        self.plus_button = PushButton("Добавить")
        self.all_buttons.append(self.plus_button)
        self.plus_button.color = "#ffb4a2"
        self.plus_button.clicked.connect(self.edema_window)
        
        self.clear_button_edema = PushButton("Очистить")
        self.clear_button_edema.setObjectName("clear_button_edema")
        self.all_buttons.append(self.clear_button_edema)
        self.clear_button_edema.color = '#fa8090'
        self.clear_button_edema.clicked.connect(self.clear_chapter)

        self.label_edema_info = QLabel()
        self.label_edema_info.setWordWrap(True)
        self.edema.addWidget(self.label_edema)
        self.edema.addWidget(self.label_edema_info)
        self.edema.addWidget(self.plus_button)
        self.edema.addWidget(self.clear_button_edema)
        
        self.hyperemia = QVBoxLayout()
        self.label_hyperemia = QLabel("Гиперемия")
        self.label_hyperemia.setStyleSheet('''
            font-weight: bold;
            font-size: 12px;
            ''')
        
        self.hyperemia.addWidget(self.label_hyperemia)
        self.plus_button_hyperemia = PushButton("Добавить")
        self.all_buttons.append(self.plus_button_hyperemia)
        self.plus_button_hyperemia.color = "#ffb4a2"
        self.plus_button_hyperemia.clicked.connect(self.hyperemia_window)
        
        self.clear_button_hyperemia = PushButton("Очистить")
        self.clear_button_hyperemia.setObjectName("clear_button_hyperemia")
        self.all_buttons.append(self.clear_button_hyperemia)
        self.clear_button_hyperemia.color = '#fa8090'
        self.clear_button_hyperemia.clicked.connect(self.clear_chapter)

        self.label_hyperemia_info = QLabel()
        self.label_hyperemia_info.setWordWrap(True)
        self.hyperemia.addWidget(self.label_hyperemia)
        self.hyperemia.addWidget(self.label_hyperemia_info)
        self.hyperemia.addWidget(self.plus_button_hyperemia)
        self.hyperemia.addWidget(self.clear_button_hyperemia)

        self.wound = QVBoxLayout()
        self.label_wound = QLabel("Рана")
        self.label_wound.setStyleSheet('''
            font-weight: bold;
            font-size: 12px;
            ''')
        
        self.plus_button_wound = PushButton("Добавить")
        self.all_buttons.append(self.plus_button_wound)
        self.plus_button_wound.color = "#ffb4a2"
        self.plus_button_wound.clicked.connect(self.wound_window)
        
        self.clear_button_wound = PushButton("Очистить")
        self.clear_button_wound.setObjectName("clear_button_wound")
        self.all_buttons.append(self.clear_button_wound)
        self.clear_button_wound.color = '#fa8090'
        self.clear_button_wound.clicked.connect(self.clear_chapter)

        self.label_wound_info = QLabel()
        self.label_wound_info.setWordWrap(True)
        self.wound.addWidget(self.label_wound)
        self.wound.addWidget(self.label_wound_info)
        self.wound.addWidget(self.plus_button_wound)
        self.wound.addWidget(self.clear_button_wound)

        self.abrasion = QVBoxLayout()
        self.label_abrasion = QLabel("Ссадина")
        self.label_abrasion.setStyleSheet('''
            font-weight: bold;
            font-size: 12px;
            ''')
        self.plus_button_abrasion = PushButton("Добавить")
        self.all_buttons.append(self.plus_button_abrasion)
        self.plus_button_abrasion.color = "#ffb4a2"
        self.plus_button_abrasion.clicked.connect(self.abrasion_window)
        
        self.clear_button_abrasion = PushButton("Очистить")
        self.clear_button_abrasion.setObjectName("clear_button_abrasion")
        self.all_buttons.append(self.clear_button_abrasion)
        self.clear_button_abrasion.color = '#fa8090'
        self.clear_button_abrasion.clicked.connect(self.clear_chapter)

        self.label_abrasion_info = QLabel()
        self.label_abrasion_info.setWordWrap(True)
        self.abrasion.addWidget(self.label_abrasion)
        self.abrasion.addWidget(self.label_abrasion_info)
        self.abrasion.addWidget(self.plus_button_abrasion)
        self.abrasion.addWidget(self.clear_button_abrasion)


        self.bruise = QVBoxLayout()
        self.label_bruise = QLabel("Кровоподтек")
        self.label_bruise.setStyleSheet('''
            font-weight: bold;
            font-size: 12px;
            ''')
        
        
        self.plus_button_bruise = PushButton("Добавить")
        self.all_buttons.append(self.plus_button_bruise)
        self.plus_button_bruise.color = "#ffb4a2"
        self.plus_button_bruise.clicked.connect(self.bruise_window)
        
        self.clear_button_bruise = PushButton("Очистить")
        self.clear_button_bruise.setObjectName("clear_button_bruise")
        self.all_buttons.append(self.clear_button_bruise)
        self.clear_button_bruise.color = '#fa8090'
        self.clear_button_bruise.clicked.connect(self.clear_chapter)

        self.label_bruise_info = QLabel()
        self.label_bruise_info.setWordWrap(True)
        
        self.bruise.addWidget(self.label_bruise)
        self.bruise.addWidget(self.label_bruise_info)
        self.bruise.addWidget(self.plus_button_bruise)
        self.bruise.addWidget(self.clear_button_bruise)


        self.pustule = QVBoxLayout()
        self.label_pustule = QLabel("Пустула")
        self.label_pustule.setStyleSheet('''
            font-weight: bold;
            font-size: 12px;
            ''')
        
        self.plus_button_pustule = PushButton("Добавить")
        self.all_buttons.append(self.plus_button_pustule)
        self.plus_button_pustule.color = "#ffb4a2"
        self.plus_button_pustule.clicked.connect(self.pustule_window)
        
        self.clear_button_pustule = PushButton("Очистить")
        self.clear_button_pustule.setObjectName("clear_button_pustule")
        self.all_buttons.append(self.clear_button_pustule)
        self.clear_button_pustule.color = '#fa8090'
        self.clear_button_pustule.clicked.connect(self.clear_chapter)

        self.label_pustule_info = QLabel()
        self.label_pustule_info.setWordWrap(True)
        
        self.pustule.addWidget(self.label_pustule)
        self.pustule.addWidget(self.label_pustule_info)
        self.pustule.addWidget(self.plus_button_pustule)
        self.pustule.addWidget(self.clear_button_pustule)

        self.scar = QVBoxLayout()
        self.label_scar = QLabel("Рубец")
        self.label_scar.setStyleSheet('''
            font-weight: bold;
            font-size: 12px;
            ''')
        
        self.plus_button_scar = PushButton("Добавить")
        self.all_buttons.append(self.plus_button_scar)
        self.plus_button_scar.color = "#ffb4a2"
        self.plus_button_scar.clicked.connect(self.scar_window)
        
        self.clear_button_scar = PushButton("Очистить")
        self.clear_button_scar.setObjectName("clear_button_scar")
        self.all_buttons.append(self.clear_button_scar)
        self.clear_button_scar.color = '#fa8090'
        self.clear_button_scar.clicked.connect(self.clear_chapter)

        self.label_scar_info = QLabel()
        self.label_scar_info.setWordWrap(True)
        
        self.scar.addWidget(self.label_scar)
        self.scar.addWidget(self.label_scar_info)
        self.scar.addWidget(self.plus_button_scar)
        self.scar.addWidget(self.clear_button_scar)



        soft_tissue.addLayout(self.algia, 0, 0, alignment = Qt.AlignLeft)
        soft_tissue.addLayout(self.edema, 0, 1, alignment = Qt.AlignLeft)
        soft_tissue.addLayout(self.hyperemia, 0, 2, alignment = Qt.AlignLeft)
        soft_tissue.addLayout(self.wound,0, 3, alignment = Qt.AlignLeft)
        soft_tissue.addLayout(self.abrasion,0, 4, alignment = Qt.AlignLeft)
        soft_tissue.addLayout(self.bruise,0, 5, alignment = Qt.AlignLeft)
        soft_tissue.addLayout(self.pustule,0, 6, alignment = Qt.AlignLeft)
        soft_tissue.addLayout(self.scar,0, 7, alignment = Qt.AlignLeft)
        self.style_box_soft_tissue = QGroupBox("Изменения мягких тканей")
        self.style_box_soft_tissue.setStyleSheet('''
            QGroupBox {
                margin-top: 2ex;
                font-size: 14px;
                
            }
            QGroupBox:enabled {
                border: 3px solid #A64A35;
                border-radius: 5px;
            }
            QGroupBox::title {
                subcontrol-origin: margin;
                left: 3ex;
            }
        ''')
        self.soft_tissue_layout.addLayout(soft_tissue)
        self.style_box_soft_tissue.setLayout(self.soft_tissue_layout)
        
        self.style_box_rad_extremities = QGroupBox("Окружность конечностей")
        self.style_box_rad_extremities.setStyleSheet('''
            QGroupBox {
                margin-top: 2ex;
                font-size: 14px;
                
            }
            QGroupBox:enabled {
                border: 3px solid #A64A35;
                border-radius: 5px;
            }
            QGroupBox::title {
                subcontrol-origin: margin;
                left: 3ex;
            }
        ''')
        self.radius = QVBoxLayout()
        self.label_rad_text = QLabel()
        self.label_rad_text.setWordWrap(True)
        self.radius.addWidget(self.label_rad_text)
        
        self.buttons_radius = QHBoxLayout()
        self.plus_button_radius = PushButton("Ввести окружности")
        self.all_buttons.append(self.plus_button_radius)
        self.plus_button_radius.color = "#ffb4a2"
        self.plus_button_radius.clicked.connect(self.radius_window)
        
        self.clear_button_radius = PushButton("Очистить раздел")
        self.clear_button_radius.setObjectName("clear_button_radius")
        self.all_buttons.append(self.clear_button_radius)
        self.clear_button_radius.color = '#fa8090'
        self.clear_button_radius.clicked.connect(self.clear_chapter)
        self.buttons_radius.addWidget(self.plus_button_radius)
        self.buttons_radius.addWidget(self.clear_button_radius)
        self.radius.addLayout(self.buttons_radius)
        self.style_box_rad_extremities.setLayout(self.radius)
        
        self.style_box_joint_mob = QGroupBox("Объем движений и дефекты конечностей")
        self.style_box_joint_mob.setStyleSheet('''
            QGroupBox {
                margin-top: 2ex;
                font-size: 14px;
                
            }
            QGroupBox:enabled {
                border: 3px solid #A64A35;
                border-radius: 5px;
            }
            QGroupBox::title {
                subcontrol-origin: margin;
                left: 3ex;
            }
        ''')
        self.joint = QVBoxLayout()
        self.label_joints_text = QLabel()
        self.label_joints_text.setWordWrap(True)
        self.joint.addWidget(self.label_joints_text)
        
        self.plus_button_joint = PushButton("Ввести объем движений (дефект)")
        self.all_buttons.append(self.plus_button_joint)
        self.plus_button_joint.color ="#ffb4a2"
        self.plus_button_joint.clicked.connect(self.joints_window)
        self.plus_button_joint.adjustSize()
        
        self.buttons_joint = QHBoxLayout()
        self.clear_button_joint = PushButton("Очистить раздел")
        self.clear_button_joint.setObjectName("clear_button_joint")
        self.all_buttons.append(self.clear_button_joint)
        self.clear_button_joint.color = '#fa8090'
        self.clear_button_joint.clicked.connect(self.clear_chapter)
        self.buttons_joint.addWidget(self.plus_button_joint)
        self.buttons_joint.addWidget(self.clear_button_joint)
        self.joint.addLayout(self.buttons_joint)

        self.style_box_joint_mob.setLayout(self.joint)
        #self.style_box_joint_mob.adjustSize()

        self.lenght_extremities = QVBoxLayout()
        self.style_box_lenght_extremities = QGroupBox("Длина конечностей")
        self.style_box_lenght_extremities.setStyleSheet('''
            QGroupBox {
                margin-top: 2ex;
                font-size: 14px;
                
            }
            QGroupBox:enabled {
                border: 3px solid #A64A35;
                border-radius: 5px;
            }
            QGroupBox::title {
                subcontrol-origin: margin;
                left: 3ex;
            }
        ''')
        self.label_lenght_extr = QLabel("Одинаковая")
        self.label_lenght_extr.setWordWrap(True)
        self.lenght_extremities.addWidget(self.label_lenght_extr)
        
        self.RB_lenght_1 = PushButton("Установить длину")
        self.all_buttons.append(self.RB_lenght_1)
        self.RB_lenght_1.color ="#ffb4a2"
        self.RB_lenght_1.clicked.connect(self.check_lenght)
        
        self.buttons_lenght = QHBoxLayout()
        self.clear_button_lenght = PushButton("Очистить раздел")
        self.all_buttons.append(self.clear_button_lenght)
        self.clear_button_lenght.setObjectName("clear_button_lenght")
        self.clear_button_lenght.color = '#fa8090'
        self.clear_button_lenght.clicked.connect(self.clear_chapter)
        self.buttons_lenght.addWidget(self.RB_lenght_1)
        self.buttons_lenght.addWidget(self.clear_button_lenght)
        self.lenght_extremities.addLayout(self.buttons_lenght)

        

        self.style_box_lenght_extremities.setLayout(self.lenght_extremities)

        self.axis_extremities = QVBoxLayout()
        self.style_box_axis_extremities = QGroupBox("Ось конечностей")
        self.style_box_axis_extremities.setStyleSheet('''
            QGroupBox {
                margin-top: 2ex;
                font-size: 14px;
                
            }
            QGroupBox:enabled {
                border: 3px solid #A64A35;
                border-radius: 5px;
            }
            QGroupBox::title {
                subcontrol-origin: margin;
                left: 3ex;
            }
        ''')
        self.label_axis_extr = QLabel("Нормальная")
        self.label_axis_extr.setWordWrap(True)
        self.axis_extremities.addWidget(self.label_axis_extr)
        
        self.button_axis = PushButton("Описать оси конечностей")
        self.all_buttons.append(self.button_axis)
        self.button_axis.color ="#ffb4a2"
        self.button_axis.clicked.connect(self.check_axis)
        

        self.buttons_axis_layout = QHBoxLayout()
        self.clear_button_axis = PushButton("Очистить раздел")
        self.all_buttons.append(self.clear_button_axis)
        self.clear_button_axis.color = '#fa8090'
        self.clear_button_axis.setObjectName("clear_button_axis")
        self.clear_button_axis.clicked.connect(self.clear_chapter)
        self.buttons_axis_layout.addWidget(self.button_axis)
        self.buttons_axis_layout.addWidget(self.clear_button_axis)
        self.axis_extremities.addLayout(self.buttons_axis_layout)

        self.style_box_axis_extremities.setLayout(self.axis_extremities)





        self.vert_extremities = QVBoxLayout()
        self.style_box_vert_extremities = QGroupBox("Деформация позвоночника")
        self.style_box_vert_extremities.setStyleSheet('''
            QGroupBox {
                margin-top: 2ex;
                font-size: 14px;
                
            }
            QGroupBox:enabled {
                border: 3px solid #A64A35;
                border-radius: 5px;
            }
            QGroupBox::title {
                subcontrol-origin: margin;
                left: 3ex;
            }
        ''')
        self.label_vert_extr = QLabel("")
        self.label_vert_extr.setWordWrap(True)
        self.vert_extremities.addWidget(self.label_vert_extr)
        
        self.button_vert = PushButton("Описать деформацию")
        self.all_buttons.append(self.button_vert)
        self.button_vert.color ="#ffb4a2"
        self.button_vert.clicked.connect(self.check_vert)
        
        self.buttons_vert_layout = QHBoxLayout()
        self.clear_button_vert = PushButton("Очистить раздел")
        self.all_buttons.append(self.clear_button_vert)
        self.clear_button_vert.color = '#fa8090'
        self.clear_button_vert.setObjectName("clear_button_vert")
        self.clear_button_vert.clicked.connect(self.clear_chapter)
        self.buttons_vert_layout.addWidget(self.button_vert)
        self.buttons_vert_layout.addWidget(self.clear_button_vert)
        self.vert_extremities.addLayout(self.buttons_vert_layout)
        self.style_box_vert_extremities.setLayout(self.vert_extremities)


        self.pathol_mobil = QVBoxLayout()
        self.style_box_pathol_mobil = QGroupBox("Патологическая подвижность")
        self.style_box_pathol_mobil.setStyleSheet('''
            QGroupBox {
                margin-top: 2ex;
                font-size: 14px;
                
            }
            QGroupBox:enabled {
                border: 3px solid #A64A35;
                border-radius: 5px;
            }
            QGroupBox::title {
                subcontrol-origin: margin;
                left: 3ex;
            }
        ''')
        self.label_pathol_mobil = QLabel("Нет")
        self.label_pathol_mobil.setWordWrap(True)
        self.pathol_mobil.addWidget(self.label_pathol_mobil)
        
        self.button_pathol_mobil = PushButton("Описать патологическую подвижность")
        self.all_buttons.append(self.button_pathol_mobil)
        self.button_pathol_mobil.color ="#ffb4a2"
        self.button_pathol_mobil.clicked.connect(self.check_pathol_mobil)
        

        self.buttons_pathol_mobil_layout = QHBoxLayout()
        self.clear_button_pathol_mobil = PushButton("Очистить раздел")
        self.all_buttons.append(self.clear_button_pathol_mobil)
        self.clear_button_pathol_mobil.color = '#fa8090'
        self.clear_button_pathol_mobil.setObjectName("clear_button_pathol_mobil")
        self.clear_button_pathol_mobil.clicked.connect(self.clear_chapter)
        self.buttons_pathol_mobil_layout.addWidget(self.button_pathol_mobil)
        self.buttons_pathol_mobil_layout.addWidget(self.clear_button_pathol_mobil)
        self.pathol_mobil.addLayout(self.buttons_pathol_mobil_layout)

        self.style_box_pathol_mobil.setLayout(self.pathol_mobil)


        self.style_box_patolog = QGroupBox("Патологические образования")
        self.style_box_patolog.setStyleSheet('''
            QGroupBox {
                margin-top: 2ex;
                font-size: 14px;
            }
            QGroupBox:enabled {
                border: 3px solid #A64A35;
                border-radius: 5px;
            }
            QGroupBox::title {
                subcontrol-origin: margin;
                left: 3ex;
            }
        ''')
        self.patolog = QVBoxLayout()
        self.label_patolog_text = QLabel()
        self.label_patolog_text.setWordWrap(True)
        self.patolog.addWidget(self.label_patolog_text)
        self.plus_button_patolog = PushButton("Описать патологические образования")
        self.all_buttons.append(self.plus_button_patolog)
        self.plus_button_patolog.color = "#ffb4a2"
        self.plus_button_patolog.clicked.connect(self.patology_window)
        
        self.buttons_patholog = QHBoxLayout()
        self.clear_button_patholog = PushButton("Очистить раздел")
        self.all_buttons.append(self.clear_button_patholog)
        self.clear_button_patholog.color = '#fa8090'
        self.clear_button_patholog.setObjectName("clear_button_patholog")
        self.clear_button_patholog.clicked.connect(self.clear_chapter)
        self.buttons_patholog.addWidget(self.plus_button_patolog)
        self.buttons_patholog.addWidget(self.clear_button_patholog)
        self.patolog.addLayout(self.buttons_patholog)

        self.style_box_patolog.setLayout(self.patolog)

        
        vbox_inner = QVBoxLayout()
        vbox_inner.addLayout(self.position)
        #vbox_inner.addStretch(1)
        vbox_inner.addLayout(self.mobility_layout)
        #vbox_inner.addStretch(1)
        vbox_inner.addWidget(self.style_box_soft_tissue)
        vbox_inner.addWidget(self.style_box_rad_extremities)
        vbox_inner.addWidget(self.style_box_joint_mob)
        vbox_inner.addWidget(self.style_box_lenght_extremities)
        vbox_inner.addWidget(self.style_box_axis_extremities)
        vbox_inner.addWidget(self.style_box_pathol_mobil)
        vbox_inner.addWidget(self.style_box_vert_extremities)
        vbox_inner.addWidget(self.style_box_patolog)
        
        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        self.widget = QWidget()
        self.widget.setLayout(vbox_inner)
        scroll.setWidget(self.widget)
        #scroll.adjustSize()
        #vbox_inner.addWidget(self.okButton)
        #scroll.resize(1000,700)

        vbox_main = QVBoxLayout()
        #vbox_main.addStretch(1)
        vbox_main.addWidget(scroll)


        vbox_main.addWidget(self.okButton)
        
        scroll_text = QScrollArea()
        scroll_text.setWidgetResizable(True)
        scroll_text.setWidget(self.text_area)
        vbox_main.addWidget(scroll_text)
        
        self.tabWidget = TabWidget()
        self.ortho_tab = QWidget()
        self.ortho_tab.setLayout(vbox_main)
        self.tabWidget.addTab(self.ortho_tab, "Локальный ортопедический статус")
        

        self.common_status = Common_status(width=self.widget.width())
        self.common_status.clear_form_signal.connect(self.clear_tab_forms)
        scroll_common = QScrollArea()
        scroll_common.setWidgetResizable(True)
        scroll_common.setWidget(self.common_status)
        self.tabWidget.addTab(scroll_common, "Общий статус первичный")
        print("common_status size", self.common_status.size())
        print("scroll_common size", scroll_common.size())

        self.common_repeated = Common_repeated(width=self.widget.width())
        self.common_repeated.clear_form_signal.connect(self.clear_tab_forms)
        scroll_repeated = QScrollArea()
        scroll_repeated.setWidgetResizable(True)
        scroll_repeated.setWidget(self.common_repeated)
        self.tabWidget.addTab(scroll_repeated, "Повторный осмотр")
        print("common_status size", self.common_repeated.size())
        print("scroll_common size", scroll_repeated.size())



        self.consultation = Consult(width=self.widget.width())
        self.consultation.clear_form_signal.connect(self.clear_tab_forms)
        scroll_consult = QScrollArea()
        scroll_consult.setWidgetResizable(True)
        scroll_consult.setWidget(self.consultation)

        self.tabWidget.addTab(scroll_consult, "Консультативное заключение")
        print("common_status size", self.common_status.size())
        print("scroll_common size", scroll_common.size())

        self.tabWidget.tabBarClicked.connect(self.common_status_check)
        #self.tabWidget.tabBarClicked.connect(self.consult_check)

        ortho_main_layout = QVBoxLayout()
        ortho_main_layout.addWidget(self.tabWidget)
        self.setLayout(ortho_main_layout)
        screen = (QDesktopWidget().availableGeometry().width(), QDesktopWidget().availableGeometry().height())

        #self.setGeometry(screen[0]/2-300, 50, 800, screen[1]*0.8)
        self.setGeometry(int(screen[0]/2-300), 50, self.widget.width()+100, int(screen[1]*0.8))

        self.setWindowTitle('Status Orthopedic Localis')

        self.text_area.setMaximumHeight(int(self.height()/4))
        scroll_text.setMaximumHeight(int(self.height()/4))

        print("size scroll =%s" %scroll_text.size())
        print("size text_area =%s" %self.text_area.size())
        scroll_size = scroll_text.size()
        
        self.show()
        print("size text_area =%s" %self.text_area.size())
        print("size copy_button =%s" %self.copy_button.size())
        self.copy_button.move(self.widget.width()-self.copy_button.width()+17, self.text_area.height()-self.copy_button.height())
        
        self.copy_button.show()

        self.save_button.move(0, self.text_area.height()-self.save_button.height())
        self.save_button.show()
        
        self.status_build()

        print(len(self.all_buttons))
        print(self.size())
        print(scroll_common.size())
        print(self.ortho_tab.size())
    
    def clear_tab_forms(self):
        self.sender()
        if self.sender() != self.common_status: self.common_status.clear_form()

        if self.sender() != self.common_repeated: self.common_repeated.clear_form()

        if self.sender() != self.consultation: self.consultation.clear_form()

    def text_coping(self):
        if self.text_area != "":
            self.text_area.selectAll()
            self.text_area.copy()
            text = QApplication.clipboard().text()
            line_lenght = 80
            inc = 1
            new_text = ""
            for i in text:
                new_text+=i
                inc +=1
                if inc >= line_lenght and i ==" ":
                    new_text+="\n"
                    inc =1
            QApplication.clipboard().setText(new_text)
            #print(text)
            #print(new_text)

    def text_saving(self):
        {
                            "position": "активное",
                            "mobility": ["самостоятельное", "", "", "", "" ],
                            "edema": "",
                            "algia": "",
                            "hyperemia": "",
                            "wound": "",
                            "abrasion": "",
                            "bruise": "",
                            "pustule": "",
                            "scar": "",
                            "radius": "",
                            "joints": "",
                            "joints_defects": "",
                            "lenght_extr": "Одинаковая",
                            "axis_extr": "Нормальная",
                            "patol_mob": "Нет",
                            "vert_deform": "",
                            "patology": "",
                            }
        
        #self.wrist_ped_info_coding = 
        {
                                    "Wrist L":[{},[]],
                                    "Wrist R":[{},[]],
                                    "Ped L":[{},[]],
                                    "Ped R":[{},[]],
                                    } 
        
        #self.joint_defects_info_coding = 
        {
                                    "ampute":{},
                                    "contracture":[],
                                    }

        pass

    
    def status_build (self):
        
        #self.main_text_dict = {
        #                    "position": "активное",
        #                    "mobility": ["самостоятельное", "", "", "", "" ],
        #                    "soft_tissue": [],
        #                    "radius": "",
        #                    "joints": "",
        #                    "joints_defects": "",
        #                    "lenght_extr": "Одинаковая",
        #                    "axis_extr": "Нормальная",
        #                    "patology": "",
        #                    }
        for i in [1,2,3]:
            self.tabWidget.setTabEnabled(i, True)


        self.okButton.color ='#adff2f'
        #for i in [self.plus_button_radius  self.plus_button_joint]:
        #    i.color ="#ffb4a2"
        position = "Положение пациента %s. " %(self.main_text_dict["position"])
        if self.main_text_dict["mobility"] and self.main_text_dict["mobility"][0] == "самостоятельное":
            mobility = "Передвигается самостоятельно."
            mobility += "Темп ходьбы %s." %(self.main_text_dict["mobility"][4])
            if self.main_text_dict["mobility"][1]:
                mobility += " "
                if self.main_text_dict["mobility"][1] == "без дополнительной опоры":
                    mobility += str(self.main_text_dict["mobility"][1]).capitalize() + ". "
                    if self.main_text_dict["mobility"][2]:
                        mobility += "Походка %s." %(self.main_text_dict["mobility"][2])
                    else:
                        mobility += " Пациент не хромает."

                
                elif self.main_text_dict["mobility"][1] == "с дополнительной опорой":
                    if self.main_text_dict["mobility"][2] and self.main_text_dict["mobility"][3]:
                        mobility += "Походка %s, с дополнительной опорой на %s. " %(self.main_text_dict["mobility"][2], self.main_text_dict["mobility"][3])

                    elif self.main_text_dict["mobility"][2]:
                        mobility += "Походка %s." %(self.main_text_dict["mobility"][2])
  
                    elif self.main_text_dict["mobility"][3]:
                        mobility += "Походка с дополнительной опорой на %s." %(self.main_text_dict["mobility"][3])
                        mobility += " Пациент не хромает."
            


        elif self.main_text_dict["mobility"]:
            mobility = "Самостоятельно не передвигается." 
            if self.main_text_dict["mobility"][1]:
                mobility += " "
                mobility += str(self.main_text_dict["mobility"][1]).capitalize() + ". "
        
        elif not self.main_text_dict["mobility"]:
            mobility = "Передвигается ?"

        radius = self.main_text_dict["radius"]
        algia = self.main_text_dict["algia"]
        edema = self.main_text_dict["edema"]
        hyperemia = self.main_text_dict["hyperemia"]
        wound = self.main_text_dict["wound"]
        abrasion = self.main_text_dict["abrasion"]
        bruise = self.main_text_dict["bruise"]
        pustule = self.main_text_dict["pustule"]
        scar = self.main_text_dict["scar"]
        wrist_ped_joints_defects = self.main_text_dict["joints_defects"]
        lenght_extremities = self.main_text_dict["lenght_extr"]
        axis_extremities = self.main_text_dict["axis_extr"]
        vert_deformity = self.main_text_dict["vert_deform"]
        pathol_mobil = self.main_text_dict["patol_mob"]
        pathology_formations = self.main_text_dict["patology"]
        
        if lenght_extremities == "Одинаковая": lenght_extremities = "Длина конечностей одинаковая. "
        if axis_extremities == "Нормальная": axis_extremities = "Оси конечностей нормальные. "
        if pathol_mobil == "Нет": pathol_mobil = "Патологической подвижности на протяжении конечностей нет. "

        
        chapters_colors = {
            "position":"#f0f0f0",
            "mobility": "#FF9999",
            "radius": "#FF99FF",
            "algia": "#B5B5B5",
            "edema": "#FFC7AC",
            "hyperemia": "#FF9999",
            "wound": "#FF3F3F",
            "abrasion": "#B63D3D",
            "bruise":"#B75EAF",
            "pustule": "#FFB140",
            "scar": "#FFD37A",
            "wrist_ped_joints_defects": "#99CCFF",
            "lenght_extremities": "#FFF800",
            "axis_extremities": "#E567B1",
            "vert_deform":"#FF9340",
            "pathol_mobil": "#FFE591",
            "pathology_formations": "#A6A0FF",
            }

        chapters_names = {
            "position":position,
            "mobility": mobility,
            "radius": radius,
            "algia": algia,
            "edema": edema,
            "hyperemia": hyperemia,
            "wound": wound,
            "abrasion": abrasion,
            "bruise": bruise,
            "pustule": pustule,
            "scar": scar,
            "wrist_ped_joints_defects": wrist_ped_joints_defects,
            "lenght_extremities": lenght_extremities,
            "axis_extremities": axis_extremities,
            "vert_deform": vert_deformity,
            "pathol_mobil": pathol_mobil,
            "pathology_formations": pathology_formations,
            }

        self.text_area.setText("")
        cursor = self.text_area.textCursor()
        frmt = QTextCharFormat()
        self.text_area.moveCursor(1)




        for key, value in chapters_names.items():
            if value !="":
                #self.text_area.moveCursor(0)
                #document = self.text_area.document()
                #cursor = self.text_area.textCursor()
                
                #frmt.setBackground(QColor(chapters_colors[key]))
                #frmt.setTextColor(QColor("black"))
                #print(QColor(chapters_colors[key]).name())
                frmt.setBackground(QColor(self.chapters_colors[key]))
                cursor.setCharFormat(frmt)
                #self.text_area.setTextBackgroundColor(QColor(chapters_colors[key]))
                
                self.text_area.setTextColor(QColor("black"))
                
                cursor.insertText(value)
                #self.text_area.moveCursor(3)
                
                #print(value)
                #print(cursor.position())
                #print(self.text_area.textBackgroundColor().name())
            #print(self.text_area.backgroundColor().name())
            #self.text_area.insertText(value)
            

        
        #self.text_area.append(position + mobility + radius + edema + wound + 
        #                        wrist_ped_joints_defects + lenght_extremities+ 
        #                        axis_extremities+pathol_mobil+pathology_formations)
        self.consultation.localis.setText(self.text_area.toPlainText())
        self.common_status.localis_textedit.setText(self.text_area.toPlainText())
        self.common_repeated.localis_textedit.setText(self.text_area.toPlainText())


    
    def common_status_check(self,index):
        
        #self.sender().setTabEnabled(index, True)

        label = False
        for but in self.all_buttons:
            if but.childWindows == True:
                label = True
                self.sender().childWindows = True
                break
        
        if label==False:
            if index == 1:
                print(index)
                #self.common_status.textedit_res_alternative()
                if self.consultation.localis.toPlainText() !="" and self.consultation.localis.toPlainText() != self.text_area.toPlainText():
                    self.common_status.setLocalis(text=self.consultation.localis.toPlainText())
                    
                    print("consultation is primary")
                    print(self.consultation.localis.toPlainText())
                else:
                    self.common_status.setLocalis(text=self.text_area.toPlainText())
                    print("localis is primary")
                if self.consultation.manipulation.toPlainText() != "": self.common_status.manipulation_textedit.setText(self.consultation.manipulation.toPlainText())
                if self.consultation.diagnosis.toPlainText() != "": self.common_status.diagnosis_textedit.setText(self.consultation.diagnosis.toPlainText())
                if self.consultation.appointment.toPlainText() != "": self.common_status.appointment_textedit.setText(self.consultation.appointment.toPlainText())
                if self.consultation.recomendation.toPlainText() != "": self.common_status.recomendation_textedit.setText(self.consultation.recomendation.toPlainText())
            elif index == 2:
                print(index)
                #self.common_status.textedit_res_alternative()
                if self.consultation.localis.toPlainText() !="" and self.consultation.localis.toPlainText() != self.text_area.toPlainText():
                    self.common_repeated.setLocalis(text=self.consultation.localis.toPlainText())
                    
                    print("consultation is primary")
                    print(self.consultation.localis.toPlainText())
                else:
                    self.common_repeated.setLocalis(text=self.text_area.toPlainText())
                    print("localis is primary")
                
                if self.common_status.manipulation !="": self.common_repeated.manipulation_textedit.setText(self.common_status.manipulation)
                if self.common_status.diagnosis !="": self.common_repeated.diagnosis_textedit.setText(self.common_status.diagnosis)
                if self.common_status.appointment !="": self.common_repeated.appointment_textedit.setText(self.common_status.appointment)
                if self.common_status.recomendation !="": self.common_repeated.recomendation_textedit.setText(self.common_status.recomendation)

                if self.consultation.manipulation.toPlainText() != "": self.common_repeated.manipulation_textedit.setText(self.consultation.manipulation.toPlainText())
                if self.consultation.diagnosis.toPlainText() != "": self.common_repeated.diagnosis_textedit.setText(self.consultation.diagnosis.toPlainText())
                if self.consultation.appointment.toPlainText() != "": self.common_repeated.appointment_textedit.setText(self.consultation.appointment.toPlainText())
                if self.consultation.recomendation.toPlainText() != "": self.common_repeated.recomendation_textedit.setText(self.consultation.recomendation.toPlainText())

            elif index ==3:
                if self.common_status.localis !="": 
                    self.consultation.setLocalis(localis=self.common_status.localis_textedit.toPlainText())
                else:
                    self.consultation.setLocalis(localis=self.text_area.toPlainText())
                
                if self.common_status.manipulation !="" and self.common_status.manipulation !="нет": 
                    self.consultation.setLocalis(manipulation=self.common_status.manipulation)
                else:
                    self.consultation.setLocalis(manipulation=self.common_repeated.manipulation_textedit.toPlainText())

                if self.common_status.diagnosis !="": 
                    self.consultation.setLocalis(diagnosis=self.common_status.diagnosis)
                else:
                    self.consultation.setLocalis(diagnosis=self.common_repeated.diagnosis_textedit.toPlainText())


                if self.common_status.appointment !="": 
                    self.consultation.setLocalis(appointment=self.common_status.appointment)
                else:
                    self.consultation.setLocalis(appointment=self.common_repeated.appointment_textedit.toPlainText())


                if self.common_status.recomendation !="": 
                    self.consultation.setLocalis(recomendation=self.common_status.recomendation)
                else:
                    self.consultation.setLocalis(recomendation=self.common_repeated.recomendation_textedit.toPlainText())

        else:
            msg = QMessageBox()
            msg.setWindowTitle("Информация")
            msg.setText("Закончите работу с открытым элементом!!!")
            msg.setIcon(QMessageBox.Information)
            center = QPoint(self.geometry().center().x(), self.geometry().center().y())
            msg.show()
            msg.move(center)
            msg.exec_()
            self.tabWidget.setTabEnabled(index, False)

    def check_patient_position (self):
        radioButton = self.sender()
        if radioButton.isChecked():
            self.okButton.color ='#fa8090'

            print(radioButton.text())
            a = radioButton.text()
            self.main_text_dict["position"] = a
            print (self.main_text_dict.items())
        self.status_build()



    def mobility(self,e):
        self.okButton.color ='#fa8090'
        
        if self.sender().color in ["#adff2f"]:
            self.main_text_dict["mobility"] = ["самостоятельное", "", "", "", "" ]
            self.sender().color ="#f0f0f0"
            self.Mob_var_Button_1.show()
            self.Mob_var_Button_2.show()
            self.Mob_var_Button_1_1.hide()
            self.Mob_var_Button_1_1.color ="#f0f0f0"
            self.Mob_var_Button_1_2.hide()
            self.Mob_var_Button_1_2.color ="#f0f0f0"
            self.label_combobox_gait.hide()
            self.label_combobox_mobility_helpers.hide()
            self.label_combobox_gait_speed.hide()
            self.combobox_gait.hide()
            self.combobox_mobility_helpers.hide()
            self.combobox_gait_speed.hide()
            self.Mob_var_Button_2_1.hide()
            self.Mob_var_Button_2_1.color ="#f0f0f0"
            self.Mob_var_Button_2_2.hide()
            self.Mob_var_Button_2_2.color ="#f0f0f0"
            self.Mob_var_Button_2_3.hide()
            self.Mob_var_Button_2_3.color ="#f0f0f0"
            self.Mob_var_Button_2_4.hide()
            self.Mob_var_Button_2_4.color ="#f0f0f0"
        
        else:

            if self.sender().text() == "самостоятельное":
                self.sender().color ="#adff2f"
                self.Mob_var_Button_2.hide()
                self.Mob_var_Button_1_1.show()
                self.Mob_var_Button_1_2.show()
                self.main_text_dict["mobility"][0] = self.sender().text()
                print(self.sender().text())

            elif self.sender().text() == "не передвигается":
                self.sender().color ="#adff2f"
                self.Mob_var_Button_1.hide()
                self.Mob_var_Button_1_1.hide()
                self.Mob_var_Button_1_2.hide()
                self.combobox_gait.hide()
                self.combobox_mobility_helpers.hide()
                self.combobox_gait_speed.hide()
                self.label_combobox_gait.hide()
                self.label_combobox_mobility_helpers.hide()
                self.label_combobox_gait_speed.hide()
                self.Mob_var_Button_2_1.show()
                self.Mob_var_Button_2_2.show()
                self.Mob_var_Button_2_3.show()
                self.Mob_var_Button_2_4.show()
                self.main_text_dict["mobility"][0] = self.sender().text()

        self.status_build()


    def mobility_level_2(self):
        
        self.combobox_mobility_helpers.hide()
        self.combobox_gait.hide()
        self.label_combobox_mobility_helpers.hide()
        self.label_combobox_gait.hide()
        sender_color = self.sender().palette().button().color().name()
        print(sender_color)
        self.Mob_var_Button_1_1.color ="#f0f0f0"
        self.Mob_var_Button_1_2.color ="#f0f0f0"
        
        self.okButton.color ='#fa8090'
        self.sender().color ="#adff2f"
        self.main_text_dict["mobility"][1] = self.sender().text() 
        if self.sender().text() == "с дополнительной опорой":
            self.combobox_mobility_helpers.show()
            self.combobox_gait.show()
            self.combobox_gait_speed.show()
            self.label_combobox_gait.show()
            self.label_combobox_mobility_helpers.show()
            self.label_combobox_gait_speed.show()
        else:
            self.combobox_gait.show()
            self.combobox_gait_speed.show()
            self.label_combobox_gait.show()
            self.label_combobox_gait_speed.show()
        self.status_build()
    
    def mobility_level_2_2(self):
        sender_color = self.sender().palette().button().color().name()
        print(sender_color)
        self.Mob_var_Button_2_1.color ="#f0f0f0"
        self.Mob_var_Button_2_2.color ="#f0f0f0"
        self.Mob_var_Button_2_3.color ="#f0f0f0"
        self.Mob_var_Button_2_4.color ="#f0f0f0"
        self.okButton.color ='#fa8090'
        self.sender().color ="#adff2f"
        self.main_text_dict["mobility"][1] = self.sender().text()
        self.status_build()

    def combobox_formation(self, items):
        sender_name = self.sender().objectName()
        if sender_name == "gait":
            index = 2
        elif sender_name == "helpers":
            index = 3
        elif sender_name == "gait_speed":
            index = 4
        

        for but in self.all_buttons:
            but.childWindows = True

        x_coord = self.sender().x()
        y_coord = self.sender().y()


        if self.combo_box_new == None:
            
            combo_layout = QGridLayout()
            combo_axis_layout = QVBoxLayout()
            combo_degree_layout = QVBoxLayout()
            combo_but = []
            
            for item in items:
                button_combo = PushButtonCombo(item)
                button_combo.font_size = 14
                button_combo.color = "#f0f0f0"
                button_combo.clicked.connect(lambda: self.handle_combobox(index=index))
                combo_axis_layout.addWidget(button_combo)
                combo_but.append(button_combo)
                #combo_axis_layout.addSpacing(100)

            #self.combo_box_new = QLabel(self)
            #self.combo_box_new.setStyleSheet(
            '''
                background-color: #FFC2C2;
                color: black;
                padding: 2px 2px 2px 2px;
                text-align: center;
                border-radius: 4px;
                border: 2px solid #A64A35;
                margin: 2px 2px 2px 2px;
            '''
            #)
            
            
            self.combo_box_new = QScrollArea(self)
            self.widget_combo = QWidget()
            self.widget_combo.setLayout(combo_axis_layout)
            self.combo_box_new.setWidget(self.widget_combo)

            #scroll.setWidgetResizable(True)

            #self.combo_box_new.setLayout(combo_box_scroll)
            self.combo_box_new.show()
            
            if sender_name == "gait":
                self.combo_box_new.resize(self.sender().width()*2.25, self.height()-y_coord-self.sender().height()-15)
            elif sender_name == "helpers":
                self.combo_box_new.resize(self.sender().width()+15, self.widget_combo.height()+10)
            elif sender_name == "gait_speed":
                self.combo_box_new.resize(self.sender().width()-5, self.widget_combo.height()+5)

            self.combo_box_new.move(x_coord+self.sender().width()-self.combo_box_new.width()+15, y_coord + self.sender().height()+10)
            
            initial_rect = self.combo_box_new.geometry()
            final_rect = QRect(self.combo_box_new.x(),self.combo_box_new.y(),1,1)
            
            print("final_rect=%s" % final_rect)

            self.combo_animation = QPropertyAnimation(self.combo_box_new, b'geometry')
            self.combo_animation.setEasingCurve(QEasingCurve.InOutSine)
            self.combo_animation.setDuration(300)
            self.combo_animation.setStartValue(initial_rect)
            self.combo_animation.setEndValue(final_rect)

        
            self.combo_animation.setDirection(QAbstractAnimation.Backward)
            self.combo_animation.start()

            self.button_pressed = self.sender()
            #self.button_pressed.color = "#A64A35"

        else:
            msg = QMessageBox()
            msg.setWindowTitle("Информация")
            msg.setText("Закончите введение вида деформации!!!")
            msg.setIcon(QMessageBox.Information)
            center = (self.geometry().center().x(), self.geometry().center().y())
            msg.show()
            msg.move(center[0]-(msg.size().width()/2), center[1]+(msg.size().height()/2))
            msg.exec_()


    def handle_combobox(self, index):
        for but in self.all_buttons:
            but.childWindows = False

        text = self.sender().text()
        if text == "-------":
            self.button_pressed.setText(text)
            #self.button_pressed.color = "#B4B4B4"
            text = ""

        self.okButton.color ='#fa8090'
        self.main_text_dict["mobility"][index] = text
        
        if text != "" and len(text)>10:
            self.button_pressed.setText(text[:10] + "...")
        elif text != "" and len(text) <=10:
            self.button_pressed.setText(text)

        self.combo_animation.setDirection(QAbstractAnimation.Forward)
        self.combo_animation.start()

        self.combo_box_new = None
        self.status_build()
        print(self.main_text_dict)


    def algia_window(self):
        for but in self.all_buttons:
            but.childWindows = True
        
        if self.main_text_dict["algia"] != "":
            entered_algias = self.main_text_dict["algia"].split(",")
        else:
            entered_algias = ""
        self.inner_algia = AlgiaWindow(entered_algias_text=entered_algias, soft_tissue_zones=self.soft_tissue_zones)
        self.inner_algia.show()
        self.inner_algia.algia_send_info.connect(self.get_algia_info)

    def get_algia_info(self):
        for but in self.all_buttons:
            but.childWindows = False
        
        if self.inner_algia != "":
            text = self.inner_algia.get_algia_text()
            
            self.main_text_dict["algia"] = text.capitalize()
            
            self.label_algia_info.setText(self.main_text_dict["algia"])
            if text != "":
                self.label_algia_info.setStyleSheet('''background-color: %s''' %self.chapters_colors["algia"])
            self.soft_tissue_zones["algia"] = self.inner_algia.get_algia_zones()
            print(self.main_text_dict)
        
        self.status_build()
        self.okButton.color ='#fa8090'
        self.inner_algia = ""
        print(self.soft_tissue_zones)


    def edema_window(self):
        #self.hide()
        for but in self.all_buttons:
            but.childWindows = True
        
        if self.main_text_dict["edema"] != "":
            entered_edemas = self.main_text_dict["edema"].split(",")
        else:
            entered_edemas = ""

        self.inner = EdemaWindow(entered_edemas_text=entered_edemas, soft_tissue_zones=self.soft_tissue_zones)

        self.inner.show()
        self.inner.edema_send_info.connect(self.get_edema_info)

    def get_edema_info(self):
        for but in self.all_buttons:
            but.childWindows = False
        if self.inner != "":
            text = self.inner.get_edema_text()
            self.main_text_dict["edema"] = text.capitalize()
            self.label_edema_info.setText(self.main_text_dict["edema"])
            if text != "":
                self.label_edema_info.setStyleSheet('''background-color: %s''' %self.chapters_colors["edema"])
            self.soft_tissue_zones["edema"] = self.inner.get_edema_zones()
            print(self.main_text_dict)
        
        self.status_build()
        self.okButton.color ='#fa8090'
        self.inner = ""
        #self.update()

    def hyperemia_window(self):
        for but in self.all_buttons:
            but.childWindows = True
        if self.main_text_dict["hyperemia"] != "":
            entered_hyperemias = self.main_text_dict["hyperemia"].split(",")
        else:
            entered_hyperemias = ""
        self.inner_hyperemia = HyperemiaWindow(entered_hyperemias=entered_hyperemias, soft_tissue_zones=self.soft_tissue_zones)
        self.inner_hyperemia.setStyleSheet("background-color: #fff")
        self.inner_hyperemia.show()
        self.inner_hyperemia.hyperemia_send_info.connect(self.get_hyperemia_info)

    def get_hyperemia_info(self):
        for but in self.all_buttons:
            but.childWindows = False

        if self.inner_hyperemia != "":
            text = self.inner_hyperemia.get_hyperemia_text().capitalize()
            self.main_text_dict["hyperemia"] = text
            #with open( "modules/soft_tissue/wound_text.pkl", 'rb') as f:
            #    self.label_wound_info.setText(pickle.load(f))
            print("get info")
            self.label_hyperemia_info.setText(text)
            if text != "":
                self.label_hyperemia_info.setStyleSheet('''background-color: %s''' %self.chapters_colors["hyperemia"])
            self.soft_tissue_zones["hyperemia"] = self.inner_hyperemia.get_hyperemia_zones()
            print(self.main_text_dict)
        
        self.status_build()
        self.okButton.color ='#fa8090'
        self.inner_hyperemia = ""
        self.update()


    def wound_window(self):
        for but in self.all_buttons:
            but.childWindows = True
        if self.main_text_dict["wound"] != "":
            entered_wounds = self.main_text_dict["wound"].split(".")
        else:
            entered_wounds = ""
        self.inner_wound = WoundWindow(entered_wounds=entered_wounds, soft_tissue_zones=self.soft_tissue_zones)
        print(self.soft_tissue_zones)
        self.inner_wound.setStyleSheet("background-color: #fff")
        self.inner_wound.show()
        self.inner_wound.wound_send_info.connect(self.get_wound_info)

    def get_wound_info(self):
        for but in self.all_buttons:
            but.childWindows = False

        if self.inner_wound != "":
            text = self.inner_wound.get_wound_text()
            #with open( "modules/soft_tissue/wound_text.pkl", 'rb') as f:
            #    self.label_wound_info.setText(pickle.load(f))
            print("get info")
            self.label_wound_info.setText(text)
            if text != "":
                self.label_wound_info.setStyleSheet('''background-color: %s''' %self.chapters_colors["wound"])
            self.soft_tissue_zones["wound"] = self.inner_wound.get_wound_zones()
            self.main_text_dict["wound"] = text
            print(self.main_text_dict)
            print(self.soft_tissue_zones)
        
        self.status_build()
        self.okButton.color ='#fa8090'
        self.inner_wound = ""
        self.update()
    
    def abrasion_window(self):
        for but in self.all_buttons:
            but.childWindows = True
        if self.main_text_dict["abrasion"] != "":
            entered_abrasions = self.main_text_dict["abrasion"].split(".")
        else:
            entered_abrasions = ""
        self.inner_abrasion = AbrasionWindow(entered_abrasions=entered_abrasions, soft_tissue_zones=self.soft_tissue_zones)
        self.inner_abrasion.setStyleSheet("background-color: #fff")
        self.inner_abrasion.show()
        self.inner_abrasion.abrasion_send_info.connect(self.get_abrasion_info)

    def get_abrasion_info(self):
        for but in self.all_buttons:
            but.childWindows = False

        if self.inner_abrasion != "":
            text = self.inner_abrasion.get_abrasion_text()
            #with open( "modules/soft_tissue/wound_text.pkl", 'rb') as f:
            #    self.label_wound_info.setText(pickle.load(f))
            print("get info")
            self.label_abrasion_info.setText(text)
            if text != "":
                self.label_abrasion_info.setStyleSheet('''background-color: %s''' %self.chapters_colors["abrasion"])
            self.soft_tissue_zones["abrasion"] = self.inner_abrasion.get_abrasion_zones()
            self.main_text_dict["abrasion"] = text
            print(self.main_text_dict)
            print(self.soft_tissue_zones)
        
        self.status_build()
        self.okButton.color ='#fa8090'
        self.inner_abrasion = ""
        self.update()

    def bruise_window(self):
        for but in self.all_buttons:
            but.childWindows = True
        if self.main_text_dict["bruise"] != "":
            entered_bruises = self.main_text_dict["bruise"].split(".")
        else:
            entered_bruises = ""
        self.inner_bruise = BruiseWindow(entered_bruises=entered_bruises, soft_tissue_zones=self.soft_tissue_zones)
        self.inner_bruise.setStyleSheet("background-color: #fff")
        self.inner_bruise.show()
        self.inner_bruise.bruise_send_info.connect(self.get_bruise_info)

    def get_bruise_info(self):
        for but in self.all_buttons:
            but.childWindows = False

        if self.inner_bruise != "":
            text = self.inner_bruise.get_bruise_text()
            #with open( "modules/soft_tissue/wound_text.pkl", 'rb') as f:
            #    self.label_wound_info.setText(pickle.load(f))
            print("get info")
            self.label_bruise_info.setText(text)
            if text != "":
                self.label_bruise_info.setStyleSheet('''background-color: %s''' %self.chapters_colors["bruise"])
            self.soft_tissue_zones["bruise"] = self.inner_bruise.get_bruise_zones()
            self.main_text_dict["bruise"] = text
            print(self.main_text_dict)
        
        self.status_build()
        self.okButton.color ='#fa8090'
        self.inner_bruise = ""
        self.update()

    def pustule_window(self):
        for but in self.all_buttons:
            but.childWindows = True
        if self.main_text_dict["pustule"] != "":
            entered_pustules = self.main_text_dict["pustule"].split(".")
        else:
            entered_pustules = ""
        self.inner_pustule = PustuleWindow(entered_pustules=entered_pustules, soft_tissue_zones=self.soft_tissue_zones)
        self.inner_pustule.setStyleSheet("background-color: #fff")
        self.inner_pustule.show()
        self.inner_pustule.pustule_send_info.connect(self.get_pustule_info)

    def get_pustule_info(self):
        for but in self.all_buttons:
            but.childWindows = False

        if self.inner_pustule != "":
            text = self.inner_pustule.get_pustule_text()
            #with open( "modules/soft_tissue/wound_text.pkl", 'rb') as f:
            #    self.label_wound_info.setText(pickle.load(f))
            print("get info")
            self.label_pustule_info.setText(text)
            if text != "":
                self.label_pustule_info.setStyleSheet('''background-color: %s''' %self.chapters_colors["pustule"])
            self.soft_tissue_zones["pustule"] = self.inner_pustule.get_pustule_zones()
            self.main_text_dict["pustule"] = text
            print(self.main_text_dict)
        
        self.status_build()
        self.okButton.color ='#fa8090'
        self.inner_pustule = ""
        self.update()

    def scar_window(self):
        for but in self.all_buttons:
            but.childWindows = True
        if self.main_text_dict["scar"] != "":
            entered_scars = self.main_text_dict["scar"].split(".")
        else:
            entered_scars = ""
        self.inner_scar = ScarWindow(entered_scars=entered_scars, soft_tissue_zones=self.soft_tissue_zones)
        self.inner_scar.setStyleSheet("background-color: #fff")
        self.inner_scar.show()
        self.inner_scar.scar_send_info.connect(self.get_scar_info)


    def get_scar_info(self):
        for but in self.all_buttons:
            but.childWindows = False

        if self.inner_scar != "":
            text = self.inner_scar.get_scar_text()
            #with open( "modules/soft_tissue/wound_text.pkl", 'rb') as f:
            #    self.label_wound_info.setText(pickle.load(f))
            print("get info")
            self.label_scar_info.setText(text)
            if text != "":
                self.label_scar_info.setStyleSheet('''background-color: %s''' %self.chapters_colors["scar"])
            self.soft_tissue_zones["scar"] = self.inner_scar.get_scar_zones()
            self.main_text_dict["scar"] = text
            print(self.main_text_dict)
        
        self.status_build()
        self.okButton.color ='#fa8090'
        self.inner_scar = ""
        self.update()

    def patology_window(self):

        if self.main_text_dict["patology"] != "":
            entered_patologies = self.main_text_dict["patology"].split(".")
        else:
            entered_patologies = ""
        self.inner_patolog = PatologicalWindow(entered_info=entered_patologies, soft_tissue_zones=self.soft_tissue_zones)
        
        for but in self.all_buttons:
            but.childWindows = True

        self.inner_patolog.setStyleSheet("background-color: #fff")
        self.inner_patolog.show()
        self.inner_patolog.patolog_send_info.connect(self.get_patology_info)

    def get_patology_info(self):

        for but in self.all_buttons:
            but.childWindows = False
        if self.inner_patolog != "":

            text = self.inner_patolog.get_text()
            self.main_text_dict["patology"] = text
            self.soft_tissue_zones["tumor"] = self.inner_patolog.get_patology_zones()
            if text != "":
                self.plus_button_patolog.color ='#fa8090'

            else:
                self.plus_button_patolog.color = "#ffb4a2"
            self.label_patolog_text.setText(text)
        
        self.status_build()
        self.okButton.color ='#fa8090'
        self.inner_patolog = ""



    def radius_window(self):
        for but in self.all_buttons:
            but.childWindows = True
        self.inner_radius = RadiusWindow()
        self.inner_radius.setStyleSheet("background-color: #fff")
        self.inner_radius.show()
        self.inner_radius.radius_send_info.connect(self.get_radius_info)

    def get_radius_info(self):
        for but in self.all_buttons:
            but.childWindows = False
        if self.inner_radius != "":
            text = self.inner_radius.get_radius_text()
            #with open( "modules/radius_text.pkl", 'rb') as f:
            #    self.label_rad_text.setText(pickle.load(f))
            #    text = self.label_rad_text.text()
            self.main_text_dict["radius"] = text
            print("get info")
            print(self.main_text_dict)
            
            if text != "":
                self.plus_button_radius.color = '#fa8090'
            else:
                self.plus_button_radius.color = "#ffb4a2"
            
            self.label_rad_text.setText(text)
        
        self.status_build()
        self.okButton.color ='#fa8090'
        self.inner_radius = ""
        self.update()


    def joints_window(self):
        
        if (self.wrist_ped_info_coding["Wrist L"] == [{},[]] and self.wrist_ped_info_coding["Wrist R"] == [{},[]] 
            and self.wrist_ped_info_coding["Ped L"] == [{},[]] and self.wrist_ped_info_coding["Ped R"] == [{},[]]):
            joint_defects=0
        #self.wrist_ped_info_coding = {
        #                            "Wrist L":[[],[]],
        #                            "Wrist R":[[],[]],
        #                            "Ped L":[[],[]],
        #                            "Ped R":[[],[]],
        #                            } 
        if self.joint_defects_info_coding["ampute"] == {} and self.joint_defects_info_coding["contracture"] == []:
            joint_defects=0
        
        self.inner_joints = BodyDefects(wrist_ped=self.wrist_ped_info_coding, joint_defects=self.joint_defects_info_coding, 
                                        label_text=self.main_text_dict["joints_defects"],wrist_ped_text=self.wrist_ped_text)
        for but in self.all_buttons:
            but.childWindows = True
        
        self.inner_joints.setStyleSheet("background-color: #fff")
        self.inner_joints.show()
        self.inner_joints.joints_send_info.connect(self.get_joints_info)
        


    def get_joints_info(self):
        print("in ________get_joints_info________")
        for but in self.all_buttons:
            but.childWindows = False
        
        if self.inner_joints != "":
            text, joint_defects_info_coding, wrist_ped_info_coding, wrist_ped_text = self.inner_joints.sendInfo()
            self.main_text_dict["joints_defects"] = text
            self.joint_defects_info_coding = joint_defects_info_coding
            self.wrist_ped_info_coding = wrist_ped_info_coding
            self.wrist_ped_text = wrist_ped_text

            print("get info")
            print(self.main_text_dict)
            if text != "":
                self.plus_button_joint.color ='#fa8090'
            else:
                self.plus_button_joint.color = "#ffb4a2"
            self.label_joints_text.setText(text)
        
        self.status_build()
        self.okButton.color ='#fa8090'
        self.inner_joints = ""
        self.update()






    def check_lenght (self):

        Button = self.sender()
        self.okButton.color ='#fa8090'
        self.inner_lenght = LenghtWindow()

        for but in self.all_buttons:
            but.childWindows = True

        self.inner_lenght.lenght_send_info.connect(self.get_lenght_info)
        print (self.main_text_dict.items())

    def get_lenght_info(self):

        for but in self.all_buttons:
            but.childWindows = False

        text = self.inner_lenght.get_text()
        if text !="":
            self.RB_lenght_1.color = '#fa8090'
            self.main_text_dict["lenght_extr"] = text
            self.label_lenght_extr.setText(text)
        else:
            self.RB_lenght_1.color = "#ffb4a2"
            self.main_text_dict["lenght_extr"] = "Одинаковая"
            self.label_lenght_extr.setText("Одинаковая")
        
        self.status_build()
        self.inner_lenght = ""
        print(self.main_text_dict)


    def check_vert (self):

        Button = self.sender()
        self.okButton.color ='#fa8090'
        self.inner_vertebra = VertebraWindow()

        for but in self.all_buttons:
            but.childWindows = True

        self.inner_vertebra.vertebra_send_info.connect(self.get_vert_info)
        print (self.main_text_dict.items())

    def get_vert_info(self):

        for but in self.all_buttons:
            but.childWindows = False
        
        if self.inner_vertebra !="":
            text = self.inner_vertebra.get_text()
            if text !="":
                self.button_vert.color = '#fa8090'
                self.main_text_dict["vert_deform"] = text
                self.label_vert_extr.setText(text)
            else:
                self.button_vert.color = "#ffb4a2"
                self.main_text_dict["vert_deform"] = ""
                self.label_vert_extr.setText("")
        
        self.status_build()
        self.inner_vertebra = ""
        print(self.main_text_dict)



    def check_axis(self):
        #self.window_child_check(sender= self.sender())
        self.inner_axis = AxisWindow()

        for but in self.all_buttons:
            but.childWindows = True

        self.inner_axis.axis_send_info.connect(self.get_axis_info)

    def get_axis_info(self):
        
        for but in self.all_buttons:
            but.childWindows = False
        if self.inner_axis != "":
            text = self.inner_axis.get_text()
            if text !="":
                self.button_axis.color = '#fa8090'
                self.main_text_dict["axis_extr"] = text
                self.label_axis_extr.setText(text)
            else:
                self.button_axis.color = "#ffb4a2"
                self.main_text_dict["axis_extr"] = "Нормальная"
                self.label_axis_extr.setText("Нормальная")
        
        self.okButton.color ='#fa8090'
        self.status_build()
        print(self.main_text_dict)
        self.inner_axis = ""
        

    def check_pathol_mobil(self):
        #self.window_child_check(sender= self.sender())
        self.inner_pathol_mobil = PatholMobilWindow()

        for but in self.all_buttons:
            but.childWindows = True

        self.inner_pathol_mobil.patholmobil_send_info.connect(self.get_pathol_mobil_info)

    def get_pathol_mobil_info(self):
        
        for but in self.all_buttons:
            but.childWindows = False
        
        if self.inner_pathol_mobil != "":
            text = self.inner_pathol_mobil.get_text()
            if text !="":
                text = text[:-2]+". "
                self.button_pathol_mobil.color = '#fa8090'
                self.main_text_dict["patol_mob"] = text
                self.label_pathol_mobil.setText(text)
            else:
                self.button_pathol_mobil.color = "#ffb4a2"
                self.main_text_dict["patol_mob"] = "Нет"
                self.label_pathol_mobil.setText("Нет")
        
        self.okButton.color ='#fa8090'
        self.status_build()
        print(self.main_text_dict)
        self.inner_pathol_mobil = ""


    def window_child_check(self, sender):
    
        for window in [self.inner_axis, self.inner_lenght, self.inner_patolog, self.inner_joints,
                        self.inner_radius, self.inner_wound, self.inner, self.inner_algia, self.inner_bruise,
                        self.inner_hyperemia, self.inner_abrasion, self.inner_pustule, self.inner_scar]:
            if window != "":
                sender.childWindows = True
                msg = QMessageBox()
                msg.setWindowTitle("Информация")
                msg.setText("Закончите работу с %s!!!" % window.windowTitle())
                msg.setIcon(QMessageBox.Information)
                center = (self.geometry().center().x(), self.geometry().center().y())
                msg.show()
                msg.move(center[0]-(msg.size().width()/2), center[1]+(msg.size().height()/2))
                msg.exec_()

    def clear_chapter(self):
        
        print(self.sender().objectName())
        but = self.sender().objectName()
        label_to_clear = [self.label_algia_info, self.label_edema_info, self.label_hyperemia_info,
                        self.label_wound_info, self.label_abrasion_info, self.label_bruise_info,
                        self.label_pustule_info, self.label_scar_info,
                        self.label_rad_text, self.label_joints_text, self.label_lenght_extr, 
                        self.label_axis_extr, self.label_vert_extr, self.label_pathol_mobil, 
                        self.label_patolog_text]

        clear_but_all = ["clear_button_algia", "clear_button_edema", "clear_button_hyperemia",
                        "clear_button_wound","clear_button_abrasion","clear_button_bruise", 
                        "clear_button_pustule", "clear_button_scar",
                        "clear_button_radius", "clear_button_joint","clear_button_lenght", 
                        "clear_button_axis", "clear_button_vert", "clear_button_pathol_mobil",
                        "clear_button_patholog",]

        for but_in_dict in clear_but_all:
            if but_in_dict == but:

                label_to_clear[clear_but_all.index(but_in_dict)].setText("")
                label_to_clear[clear_but_all.index(but_in_dict)].setStyleSheet("background-color: None")
                if but_in_dict == "clear_button_algia":
                    self.main_text_dict["algia"] = ""
                    self.soft_tissue_zones["algia"] = []
                    self.plus_button_algia.color ="#ffb4a2"
                elif but_in_dict == "clear_button_edema":
                    self.main_text_dict["edema"] = ""
                    self.soft_tissue_zones["edema"] = []
                    self.plus_button.color ="#ffb4a2"
                elif but_in_dict == "clear_button_hyperemia":
                    self.main_text_dict["hyperemia"] = ""
                    self.soft_tissue_zones["hyperemia"] = []
                    self.plus_button_hyperemia.color ="#ffb4a2"
                elif but_in_dict == "clear_button_wound":
                    self.main_text_dict["wound"] = ""
                    self.soft_tissue_zones["wound"] = []
                    self.plus_button_wound.color ="#ffb4a2"
                elif but_in_dict == "clear_button_abrasion":
                    self.main_text_dict["abrasion"] = ""
                    self.soft_tissue_zones["abrasion"] = []
                    self.plus_button_abrasion.color ="#ffb4a2"
                elif but_in_dict == "clear_button_bruise":
                    self.main_text_dict["bruise"] = ""
                    self.soft_tissue_zones["bruise"] = []
                    self.plus_button_bruise.color ="#ffb4a2"
                elif but_in_dict == "clear_button_pustule":
                    self.main_text_dict["pustule"] = ""
                    self.soft_tissue_zones["pustule"] = []
                    self.plus_button_pustule.color ="#ffb4a2"
                elif but_in_dict == "clear_button_scar":
                    self.main_text_dict["scar"] = ""
                    self.soft_tissue_zones["scar"] = []
                    self.plus_button_scar.color ="#ffb4a2"
                elif but_in_dict == "clear_button_radius":
                    self.main_text_dict["radius"] = ""
                    self.plus_button_radius.color ="#ffb4a2"
                elif but_in_dict == "clear_button_joint":
                    self.main_text_dict["joints_defects"] = ""
                    self.plus_button_joint.color ="#ffb4a2"
                    self.joint_defects_info_coding = {"ampute":{},"contracture":[]}
                    self.wrist_ped_info_coding = {"Wrist L":[{},[]],"Wrist R":[{},[]],"Ped L":[{},[]],"Ped R":[{},[]]} 
                    self.wrist_ped_text = ["","","",""]
                elif but_in_dict == "clear_button_lenght":
                    self.main_text_dict["lenght_extr"] = "Одинаковая"
                    self.RB_lenght_1.color ="#ffb4a2"
                    label_to_clear[clear_but_all.index(but_in_dict)].setText("Одинаковая")
                elif but_in_dict == "clear_button_axis":
                    self.main_text_dict["axis_extr"] = "Нормальная"
                    self.button_axis.color ="#ffb4a2"
                    label_to_clear[clear_but_all.index(but_in_dict)].setText("Нормальная")
                elif but_in_dict =="clear_button_vert":
                    self.main_text_dict["vert_deform"] = ""
                    self.button_vert.color = "#ffb4a2"

                elif but_in_dict == "clear_button_pathol_mobil":
                    self.main_text_dict["patol_mob"] = "Нет"
                    self.button_pathol_mobil.color ="#ffb4a2"
                    label_to_clear[clear_but_all.index(but_in_dict)].setText("Нет")
                elif but_in_dict == "clear_button_patholog":
                    self.main_text_dict["patology"] = ""
                    self.soft_tissue_zones["tumor"] = []
                    self.plus_button_patolog.color ="#ffb4a2"

        self.status_build()

    def text_saving(self):
        desktop_destination = os.path.join(os.environ['USERPROFILE'], "Desktop\\ORTHO_STATUS\\")
        print(desktop_destination)
        try:
            os.mkdir(desktop_destination, mode=stat.S_ISUID)
        except OSError as error:
            print(error)   
        
        options = QFileDialog.Options()
        options |= QFileDialog.DontUseNativeDialog
        fileName, _ = QFileDialog.getSaveFileName(self,"Сохранение файла .txt",directory=desktop_destination, 
                                                    filter="All Files (*);;Text Files (*.txt)", options=options)
        if fileName:
            print(fileName)
        if fileName[-4:] !=".txt":
            full_way = fileName +".txt"
        else:
            full_way = fileName
        print(full_way)

        text = self.text_area.toPlainText()
        text_new = ""
        line_lenght = 60
        inc = 1
        if len(text) >60:
            for i in text:
                if inc >= line_lenght and i ==" ":
                    text_new += i +"\n"
                    inc = 1
                else:
                    text_new+=i
                    inc+=1

        else:
            text_new = text

        with open(full_way, "x") as f:
            f.write("Дата %s, время: %s.\n\n" %(time.strftime("%d.%m.%Y"), time.strftime("%H:%M")))
            for line in text_new:
                f.write(line)
            f.close()

    def mousePressEvent(self, event):
        print('mousePressEvent', event.x(), event.y(),)

    def closeEvent(self, event):
        print("X is clicked")
        #try:
        print([self.inner_axis, self.inner_lenght, self.inner_patolog, self.inner_joints,
            self.inner_radius, self.inner_wound, self.inner, self.inner_algia])
        for window in [self.inner_axis, self.inner_hyperemia, self.inner_lenght, self.inner_patolog, self.inner_joints,
                        self.inner_radius, self.inner_wound, self.inner_abrasion, self.inner_bruise, self.inner_pustule, 
                        self.inner_scar, self.inner, self.inner_algia, self.inner_scar]:
            if window != "":
                window.close()
        text = self.text_area.toPlainText()
        text_new = ""
        line_lenght = 60
        inc = 1
        if len(text) >60:
            for i in text:
                if inc >= line_lenght and i ==" ":
                    text_new += i +"\n"
                    inc = 1
                else:
                    text_new+=i
                    inc+=1

        else:
            text_new = text
        if text =="":
            logging.info("APP WAS CLOSED with no text in text_zone.\n")
        else:
            logging.info("APP WAS CLOSED with text in text_zone:\n%s\n" %text_new[:7] + "..." + text_new[-7:])

        sys.exit(1)

    '''
    def event(self, e):
        
        if e.type() == QEvent.KeyPress:
            print("Нажата клавиша на клавиатуре")
            print("Код:", e.key(), ", текст:", e.text())
        elif e.type() == QEvent.Close:
            print("Окно закрыто")
        elif e.type() == QEvent.MouseButtonPress:
            if self.inner_axis:
                msg = QMessageBox()
                msg.setWindowTitle("Информация")
                msg.setText("Закончите введение вида деформации!!!")
                msg.setIcon(QMessageBox.Information)
                msg.show()
                msg.exec_()
                print ("Щелчок мышью. Координаты:", e.x(), e.y())
                

        return QWidget.event(self, e) # Отправляем дальше
    '''

if __name__ == '__main__':

    logging.basicConfig(filename="app_LOG.log",level=logging.DEBUG, format='%(asctime)s - %(name)s - %(levelname)s \n- %(message)s')
    
    console = logging.StreamHandler()
    console.setLevel(logging.DEBUG)
    # установить формат, который проще для использования консоли
    formatter = logging.Formatter('%(name)s: %(levelname)s %(message)s')
    # сказать обработчику использовать этот формат
    console.setFormatter(formatter)
    # добавить обработчик в корневой логгер
    logging.getLogger('').addHandler(console)

    def exception_hook(exc_type, exc_value, exc_traceback):
        logging.error(
            "Uncaught exception",
            exc_info=(exc_type, exc_value, exc_traceback)
        )

    




    #logger = logging.getLogger('MAIN_APP')
    #logger.setLevel(logging.DEBUG)
    
    # создать обработчик файлов, который журналирует даже отладочные сообщения
    #fh = logging.FileHandler('temp/app_LOG.log')
    #fh.setLevel(logging.DEBUG)
    
    # создать обработчик консоли с более высоким уровнем журналирования
    #ch = logging.StreamHandler()
    #ch.setLevel(logging.NOTSET)
    
    # создать форматтер и добавить его в обработчики
    #formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s \n- %(message)s')
    #fh.setFormatter(formatter)
    #ch.setFormatter(formatter)

    # добавить обработчики в логгер
    #logger.addHandler(fh)
    #logger.addHandler(ch)

    try:
        app = QApplication(sys.argv)
        app.setWindowIcon(QIcon('icon.ico')) 
        ex = Example()
        sys.excepthook = exception_hook#(sys.exc_info())
        logging.info("APP RUN")
        sys.exit(app.exec_())
    except Exception as ex:
        #logger.error("SMTH wrong:%s" %ex.args)
        logging.exception(ex, exc_info=True)
        print(ex)
        sys.exit(1)

