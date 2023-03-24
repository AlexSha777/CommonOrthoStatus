import sys
import pickle
import time
from PyQt5.QtCore import pyqtSignal, QRect, QVariantAnimation, QAbstractAnimation
from PyQt5.QtGui import QPixmap, QPainter, QColor, QFont, QCursor
from PyQt5.QtCore import Qt, pyqtProperty

from PyQt5.QtWidgets import (QApplication, QWidget, QScrollArea, QHBoxLayout, QVBoxLayout, 
                            QDesktopWidget, QPushButton, QDialog, QLabel, QGridLayout, QGroupBox,
                            QLineEdit, QMessageBox, QComboBox, QMenu, QAction)

#from modules.zone_detecting.zone_choosing import ScrollOnPicture
from zone_choosing import ScrollOnPicture, Winform

class PushButton(QPushButton):
    def __init__(self, parent=None):
        super().__init__(parent)
        self._animation = QVariantAnimation(
            startValue=QColor("#4CAF50"),
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
            border: 2px solid #4CAF50;
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

class PushButton_zone (QPushButton):
    zones_checked_determine = pyqtSignal()

    def __init__(self, parent=None):
        super().__init__(parent)
        self._color = "white"
        self.styling()
        self.setCursor(QCursor(Qt.PointingHandCursor))
        self._zone_number = 0
    
    @pyqtProperty(int)
    def zone_number(self):
        return self._zone_number

    @zone_number.setter
    def zone_number(self, zone_number):
        self._zone_number = zone_number

    def styling(self):

        self.setStyleSheet('''
                QPushButton{
                    background-color: %s;
                    border: none;
                    color: black;
                    padding: 6px 12px;
                    text-align: center;
                    text-decoration: none;
                    font-size: 12px;
                    border-radius: 8px;
                    margin: 4px 2px;
                    border: 2px solid #4CAF50;
                }
                ''' %self._color)

    @pyqtProperty(int)
    def color(self):
        return self._color

    @color.setter
    def color(self, color):
        self._color = color
        self.styling()


    def mousePressEvent(self, event):
        self.zones_checked_determine.emit()
        if self._zone_number >1:
            event.ignore()
            self._color = "#FF0700"
            self.styling()
            msg = QMessageBox()
            msg.setWindowTitle("Информация")
            msg.setText("Введено более одной зоны - нельзя ввести детализацию локализации!!!")
            msg.setIcon(QMessageBox.Information)
            msg.exec_()
        else:
            self._color = "white"
            self.styling()
            super().mousePressEvent(event)



class PustuleWindow(QWidget):
    pustule_send_info = pyqtSignal()

    def __init__(self, entered_pustules, soft_tissue_zones, **kwargs):
        super().__init__( **kwargs)
        
        self.entered_pustules_text = entered_pustules
        self.soft_tissue_checked_zones = soft_tissue_zones
        self.initUI()

    def initUI(self):
        
        print(self.entered_pustules_text)
        self.file_name = "front_clear.bmp"
        self.picture = Winform(self.file_name, soft_tissue_zones=self.soft_tissue_checked_zones)
        self.scroll = QScrollArea()

        self.scroll.setWidget(self.picture)
        self.scroll.setStyleSheet("""
            QScrollArea {
                border:none;
            }
            QScrollBar {
                border-radius: 2px;
            }
            QScrollBar:vertical {
                width: 10px;
            }
            QScrollBar::handle:vertical {
                background-color: grey;
                min-height: 5px;
                border-radius: 4px;
            }
            """)

        self.zones_dict = []

        
        

        sizeObject = QDesktopWidget().screenGeometry(-1)
        self.resize((self.picture.width()), (sizeObject.height()-90))

        self.button_front = PushButton("Вид спереди")
        self.button_back = PushButton("Вид сзади")
        self.vertical_buttons = QHBoxLayout()
        self.vertical_buttons.addWidget(self.button_front)
        self.vertical_buttons.addWidget(self.button_back)
        self.button_front.clicked.connect(self.picture_view)
        self.button_back.clicked.connect(self.picture_view)


        self.vbox = QVBoxLayout()
        self.vbox.addWidget(self.scroll)
        self.vbox.addLayout(self.vertical_buttons)
        self.close_btn = PushButton("Закончить введение")
        self.close_btn.clicked.connect(self.close)
        self.vbox.addWidget(self.close_btn) 

        self.button_clear = PushButton("Очистить")
        self.button_clear.clicked.connect(self.picture_clear)
        self.vbox.addWidget(self.button_clear)

        
        self.pustules = QVBoxLayout()

        self.lab_entered_pustules = QLabel("Введенные пустулы")
        self.entered_pustules = QGroupBox(self.lab_entered_pustules.text())
        
        self.lab_pustules = QLabel()
        self.lab_pustules.setWordWrap(True)
        if self.entered_pustules_text != "":
            self.entered_pustules_text = self.entered_pustules_text[:-1]
            text_to_add = ""
            counter = 1
            for item in self.entered_pustules_text:
                text_to_add += str(counter) + ") " + item + ". "
                counter+=1
            self.lab_pustules.setText(text_to_add)
            self.entered_pustules_text = text_to_add.split(".")[:-1]

        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        scroll.setWidget(self.lab_pustules)

        self.pustules.addWidget(scroll)
        scroll.setStyleSheet("""
            QScrollArea {
                border: none;
            }
            QScrollBar {
                border-radius: 5px;
            }
            QScrollBar:vertical {
                width: 10px;
            }
            QScrollBar::handle:vertical {
                background-color: gold;
                min-height: 5px;
                border-radius: 4px;
            }
            """)

        self.pustule_edit_button = QPushButton("Редактировать")
        
        self.update_editing_menu(self.pustule_edit_button)

        
        
        self.pustule_edit_button.setStyleSheet('''
            QPushButton{
                background-color: white;
                border: none;
                color: black;
                padding: 6px 12px;
                text-align: center;
                text-decoration: none;
                font-size: 12px;
                border-radius: 8px;
                margin: 4px 2px;
                border: 2px solid #4CAF50;
            }
            ''')
        self.pustules.addWidget(self.pustule_edit_button)


        self.entered_pustules.setLayout(self.pustules)

        self.entered_pustules.setStyleSheet('''

            QGroupBox {margin-top: 2ex;
            }
            QGroupBox:enabled {
                border: 3px solid gold;
                border-radius: 5px;
            }
            QGroupBox::title {
                subcontrol-origin: margin;
                left: 3ex;
            }
        ''')

        self.pustule_text_forming = QVBoxLayout()
        self.pustule_zone = ""
        self.chosen_zones = QGroupBox("Текущее описание пустулы")
        self.inner_chosen_zones = QLabel()
        self.inner_chosen_zones.setWordWrap(True)
        self.pustule_text_forming.addWidget(self.inner_chosen_zones)
        self.button_new_pustule = PushButton("Ввести пустулу")
        self.button_new_pustule.clicked.connect(self.add_formed_pustule)
        self.pustule_text_forming.addWidget(self.button_new_pustule)
        self.chosen_zones.setLayout(self.pustule_text_forming)
        
        self.chosen_zones.setStyleSheet('''
            QGroupBox {margin-top: 2ex;
            }
            QGroupBox:enabled {
                border: 3px solid lightcoral;
                border-radius: 5px;
            }
            QGroupBox:title {
                subcontrol-origin: margin;
                left: 3ex;
            }
        ''')
        
        self.zone_detailes = QGroupBox("Детализация расположения")
        self.zone_detailes_text = ""
        self.zone_detailes.setStyleSheet('''
            QGroupBox {
                margin-top: 2ex;
            }
            QGroupBox:enabled {
                border: 3px solid green;
                border-radius: 5px;
            }
            QGroupBox::title {
                subcontrol-origin: margin;
                left: 3ex;
            }
        ''')
        self.zone_detailes_box = QVBoxLayout()
        self.zone_detailes_text = ""
        zone_detailes = [ "медиально", "латерально", "проксимально", "дистально", "каудально", "краниально"]
        menu_zone_detailes = QMenu(self)
        self.create_menu(zone_detailes, menu_zone_detailes)
        
        self.zone_detailes_menu_button = PushButton_zone()
        self.zone_detailes_menu_button.zones_checked_determine.connect(self.check_zone_number)
        self.zone_detailes_menu_button.setMenu(menu_zone_detailes)
        menu_zone_detailes.triggered.connect(self.zone_detailes_action)
        self.zone_detailes_menu_button.setStyleSheet('''
            QPushButton{
                background-color: white;
                border: none;
                color: black;
                padding: 6px 12px;
                text-align: center;
                text-decoration: none;
                font-size: 12px;
                border-radius: 8px;
                margin: 4px 2px;
                border: 2px solid #4CAF50;
            }
            ''')
        menu_zone_detailes.setStyleSheet('''
            QMenu{
                background-color: white;
                margin: 2px;
                color: black;
            }
            QMenu::item {
                padding: 2px 25px 2px 20px;
                border: 1px solid transparent;
            }
            QMenu::item:selected{
                background-color: #4CAF50;
                color: black;
            } 
            ''')

        #self.button.setToolTip('<img src="icon.svg">')
        
        self.zone_detailes_box.addWidget(self.zone_detailes_menu_button)
        self.zone_detailes.setLayout(self.zone_detailes_box)





        self.pustule_type = QGroupBox("Форма пустулы")
        self.pustule_type.setStyleSheet('''
            QGroupBox {
                margin-top: 2ex;
            }
            QGroupBox:enabled {
                border: 3px solid green;
                border-radius: 5px;
            }
            QGroupBox::title {
                subcontrol-origin: margin;
                left: 3ex;
            }
        ''')
        self.pustule_type_box = QVBoxLayout()
        self.pustule_type_text = ""
        clinic_types = ["округлая", "овальная", "конусообразная", "плоская"]
        self.menu_type = QMenu(self)
        self.create_menu(clinic_types, self.menu_type)
        
        self.type_menu_button = QPushButton()
        self.type_menu_button.setMenu(self.menu_type)
        self.menu_type.triggered.connect(self.type_action)
        self.type_menu_button.setStyleSheet('''
            QPushButton{
                background-color: white;
                border: none;
                color: black;
                padding: 6px 12px;
                text-align: center;
                text-decoration: none;
                font-size: 12px;
                border-radius: 8px;
                margin: 4px 2px;
                border: 2px solid #4CAF50;
            }
            ''')
        self.menu_type.setStyleSheet('''
            QMenu{
                background-color: white;
                margin: 2px;
                color: black;
            }
            QMenu::item {
                padding: 2px 25px 2px 20px;
                border: 1px solid transparent;
            }
            QMenu::item:selected{
                background-color: #4CAF50;
                color: black;
            } 
            ''')

        #self.button.setToolTip('<img src="icon.svg">')
        
        self.pustule_type_box.addWidget(self.type_menu_button)
        self.pustule_type.setLayout(self.pustule_type_box)


        self.pustule_quantity = QGroupBox("Количество пустул")
        self.pustule_quantity.setStyleSheet('''
            QGroupBox {
                margin-top: 2ex;
            }
            QGroupBox:enabled {
                border: 3px solid green;
                border-radius: 5px;
            }
            QGroupBox::title {
                subcontrol-origin: margin;
                left: 3ex;
            }
        ''')
        self.pustule_quantity_box = QVBoxLayout()
        self.pustule_quantity_text = ""
        clinic_quantities = ["единичная", "множественные"]
        self.menu_quantity = QMenu(self)
        self.create_menu(clinic_quantities, self.menu_quantity)
        
        self.quantity_menu_button = QPushButton()
        self.quantity_menu_button.setMenu(self.menu_quantity)
        self.menu_quantity.triggered.connect(self.quantity_action)
        self.quantity_menu_button.setStyleSheet('''
            QPushButton{
                background-color: white;
                border: none;
                color: black;
                padding: 6px 12px;
                text-align: center;
                text-decoration: none;
                font-size: 12px;
                border-radius: 8px;
                margin: 4px 2px;
                border: 2px solid #4CAF50;
            }
            ''')
        self.menu_quantity.setStyleSheet('''
            QMenu{
                background-color: white;
                margin: 2px;
                color: black;
            }
            QMenu::item {
                padding: 2px 25px 2px 20px;
                border: 1px solid transparent;
            }
            QMenu::item:selected{
                background-color: #4CAF50;
                color: black;
            } 
            ''')

        #self.button.setToolTip('<img src="icon.svg">')
        
        self.pustule_quantity_box.addWidget(self.quantity_menu_button)
        self.pustule_quantity.setLayout(self.pustule_quantity_box)


        self.pustule_size = QGroupBox("Размер пустулы")
        self.pustule_size.setStyleSheet('''
            QGroupBox {
                margin-top: 2ex;
            }
            QGroupBox:enabled {
                border: 3px solid green;
                border-radius: 5px;
            }
            QGroupBox::title {
                subcontrol-origin: margin;
                left: 3ex;
            }
        ''')
        self.pustule_size_box = QVBoxLayout()
        self.pustule_size_text = ""
        self.label_lenght = QLabel("Длинна, см")
        self.pustule_size_lenght = QLineEdit(self.label_lenght)
        self.pustule_size_lenght.textChanged.connect(self.add_size)
        self.pustule_size_lenght.setStyleSheet('border: 2px solid grey; border-radius: 5px;')
        self.label_width = QLabel("Ширина, см")
        self.pustule_size_width = QLineEdit(self.label_width)
        self.pustule_size_width.textChanged.connect(self.add_size)
        self.pustule_size_width.setStyleSheet('border: 2px solid grey; border-radius: 5px;')
        
        self.pustule_size_box.addWidget(self.label_lenght)
        self.pustule_size_box.addWidget(self.pustule_size_lenght)
        self.pustule_size_box.addWidget(self.label_width)
        self.pustule_size_box.addWidget(self.pustule_size_width)
        

        #self.add_wound_size = PushButton("Добавить")
        #self.add_wound_size.clicked.connect(self.add_size)
#        self.add_wound_size.setStyleSheet('''
#        QPushButton {
#            background-color: #4CAF50; /* Green */
#            border: none;
#            color: white;
#            border-radius: 8px;
#            padding: 15px 32px;
#            text-align: center;
#            text-decoration: none;
#            display: inline-block;
#            font-size: 16px;
#            "transition-duration: 0.4s;"
#            "cursor: pointer;"
#        }
#        QPushButton:hover {
#            background-color: #4CAF50;
#            color: white;
#        }
#        ''')
        #self.wound_size_box.addWidget(self.add_wound_size)

        self.pustule_size.setLayout(self.pustule_size_box)



        self.pustule_kind = QGroupBox("Разновидность")
        self.pustule_kind.setStyleSheet('''
            QGroupBox {
                margin-top: 2ex;
            }
            QGroupBox:enabled {
                border: 3px solid green;
                border-radius: 5px;
            }
            QGroupBox::title {
                subcontrol-origin: margin;
                left: 3ex;
            }
        ''')

        self.menu_kind = QMenu(self)
        kinds = ["вокруг волосяного фолликула", "поверхностная", "глубокая"]
        for z in kinds:
            action = self.menu_kind.addAction(z)
            action.setIconVisibleInMenu(False)
        
        self.kind_menu_button = QPushButton()
        self.kind_menu_button.setMenu(self.menu_kind)
        self.menu_kind.triggered.connect(self.kind_action)

        self.kind_menu_button.setStyleSheet('''
            QPushButton{
                background-color: white;
                border: none;
                color: black;
                padding: 6px 12px;
                text-align: center;
                text-decoration: none;
                font-size: 12px;
                border-radius: 8px;
                margin: 4px 2px;
                border: 2px solid #4CAF50;
            }
            ''')
        self.menu_kind.setStyleSheet('''
            QMenu{
                background-color: white;
                margin: 2px;
                color: black;
            }
            QMenu::item {
                padding: 2px 25px 2px 20px;
                border: 1px solid transparent;
            }
            QMenu::item:selected{
                background-color: #4CAF50;
                color: black;
            } 
            ''')
        self.pustule_kind_box = QVBoxLayout()
        self.pustule_kind_text = ""
        self.pustule_kind_box.addWidget(self.kind_menu_button)
        self.pustule_kind.setLayout(self.pustule_kind_box)


        self.pustule_content = QGroupBox("Содержимое")
        self.pustule_content.setStyleSheet('''
            QGroupBox {
                margin-top: 2ex;
            }
            QGroupBox:enabled {
                border: 3px solid green;
                border-radius: 5px;
            }
            QGroupBox::title {
                subcontrol-origin: margin;
                left: 3ex;
            }
        ''')

        self.menu_content = QMenu(self)
        contents = ["прозрачное, светлое", "мутное, светлое", "прозрачное, бурое", "мутное, бурое"]
        for z in contents:
            action = self.menu_content.addAction(z)
            action.setIconVisibleInMenu(False)
        
        self.content_menu_button = QPushButton()
        self.content_menu_button.setMenu(self.menu_content)
        self.menu_content.triggered.connect(self.content_action)

        self.content_menu_button.setStyleSheet('''
            QPushButton{
                background-color: white;
                border: none;
                color: black;
                padding: 6px 12px;
                text-align: center;
                text-decoration: none;
                font-size: 12px;
                border-radius: 8px;
                margin: 4px 2px;
                border: 2px solid #4CAF50;
            }
            ''')
        self.menu_content.setStyleSheet('''
            QMenu{
                background-color: white;
                margin: 2px;
                color: black;
            }
            QMenu::item {
                padding: 2px 25px 2px 20px;
                border: 1px solid transparent;
            }
            QMenu::item:selected{
                background-color: #4CAF50;
                color: black;
            } 
            ''')
        self.pustule_content_box = QVBoxLayout()
        self.pustule_content_text = ""
        self.pustule_content_box.addWidget(self.content_menu_button)
        self.pustule_content.setLayout(self.pustule_content_box)

        self.pustule_excav = QGroupBox("Нарушение целостности")
        self.pustule_excav.setStyleSheet('''
            QGroupBox {
                margin-top: 2ex;
            }
            QGroupBox:enabled {
                border: 3px solid green;
                border-radius: 5px;
            }
            QGroupBox::title {
                subcontrol-origin: margin;
                left: 3ex;
            }
        ''')

        self.menu_excav = QMenu(self)
        excavs = ["вскрыта", "не вскрыта", "частично вскрыты"]
        for z in excavs:
            action = self.menu_excav.addAction(z)
            action.setIconVisibleInMenu(False)
        
        self.excav_menu_button = QPushButton()
        self.excav_menu_button.setMenu(self.menu_excav)
        self.menu_excav.triggered.connect(self.excav_action)

        self.excav_menu_button.setStyleSheet('''
            QPushButton{
                background-color: white;
                border: none;
                color: black;
                padding: 6px 12px;
                text-align: center;
                text-decoration: none;
                font-size: 12px;
                border-radius: 8px;
                margin: 4px 2px;
                border: 2px solid #4CAF50;
            }
            ''')
        self.menu_excav.setStyleSheet('''
            QMenu{
                background-color: white;
                margin: 2px;
                color: black;
            }
            QMenu::item {
                padding: 2px 25px 2px 20px;
                border: 1px solid transparent;
            }
            QMenu::item:selected{
                background-color: #4CAF50;
                color: black;
            } 
            ''')
        self.pustule_excav_box = QVBoxLayout()
        self.pustule_excav_text = ""
        self.pustule_excav_box.addWidget(self.excav_menu_button)
        self.pustule_excav.setLayout(self.pustule_excav_box)

        self.right_scroll = QScrollArea()
        self.right_scroll.setStyleSheet("""
            QScrollArea{
                border: none;
            }
            """)
        self.vbox_right = QVBoxLayout()
        self.vbox_right.addWidget(self.entered_pustules)
        self.vbox_right.addWidget(self.chosen_zones)
        self.vbox_right.addWidget(self.zone_detailes)
        self.vbox_right.addWidget(self.pustule_type)
        self.vbox_right.addWidget(self.pustule_quantity)
        self.vbox_right.addWidget(self.pustule_size)
        self.vbox_right.addWidget(self.pustule_excav)
        self.vbox_right.addWidget(self.pustule_kind)
        self.vbox_right.addWidget(self.pustule_content)
        self.right_scroll.setLayout(self.vbox_right)
        self.vbox_right_scroll = QVBoxLayout()
        self.vbox_right_scroll.addWidget(self.right_scroll)


        #self.box_button = QHBoxLayout()
        #self.button_light = QPushButton("Легкий")
        #self.button_light.clicked.connect(self.edema_degree)
        #self.button_medium = QPushButton("Умеренный")
        #self.button_medium.clicked.connect(self.edema_degree)
        #self.button_hard = QPushButton("Выраженный")
        #self.button_hard.clicked.connect(self.edema_degree)
        #self.box_button.addWidget(self.button_light)
        #self.box_button.addWidget(self.button_medium)
        #self.box_button.addWidget(self.button_hard)

        #self.vbox_right.addLayout(self.box_button)


        
        self.grid = QGridLayout(self)
        self.grid.addLayout(self.vbox,0 , 0)
        self.grid.addLayout(self.vbox_right_scroll, 0 , 1)
        self.grid.setColumnMinimumWidth(0, self.picture.width()+40)
        self.grid.setColumnMinimumWidth(1, (self.picture.width()+40)/3)
        self.grid.setColumnStretch(1, 0.5)
        
        
        self.setWindowTitle ("Кровоподтеки")
        self.show()
    

    def check_zone_number(self):
        self.zone_detailes_menu_button.zone_number = len(self.picture.get_checked_zones())
        print(len(self.picture.get_checked_zones()))


    def create_menu(self, d, menu):
        if isinstance(d, list):
            for e in d:
                self.create_menu(e, menu)
        elif isinstance(d, dict):
            for k, v in d.items():
                sub_menu = QMenu(k, menu)
                menu.addMenu(sub_menu)
                self.create_menu(v, sub_menu)
        else:
            action = menu.addAction(d)
            action.setIconVisibleInMenu(False)

    def update_editing_menu(self, pushbut):

        if len(self.entered_pustules_text) ==1:
            pustule_numbers = ["Удалить пустулу 1)..."]
        elif self.entered_pustules_text == []:
            pustule_numbers = []
        else: 
            pustule_numbers = ["Удалить пустулу " + i.strip()[:2] + "..." for i in  self.entered_pustules_text]
        #wound_numbers = [i[:2] + "" for i in  self.entered_wounds_text]
        menu_type_pustule = QMenu(self)
        self.create_menu(pustule_numbers, menu_type_pustule)
        
        pushbut.setMenu(menu_type_pustule)
        menu_type_pustule.triggered.connect(self.editing_action)
        menu_type_pustule.setStyleSheet('''
            QMenu{
                background-color: white;
                margin: 2px;
                color: black;
            }
            QMenu::item {
                padding: 2px 25px 2px 20px;
                border: 1px solid transparent;
            }
            QMenu::item:selected{
                background-color: #4CAF50;
                color: black;
            } 
            ''')


    def editing_action(self, action):
        number = int(action.text()[-5])-1
        text_updated_list = self.lab_pustules.text().split(".")[:-1]
        text_updated_list.pop(number)
        self.soft_tissue_checked_zones["pustule"].pop(number)
        text_new =""
        print(len(text_updated_list), text_updated_list)
        if len(text_updated_list)>1:
            for item in text_updated_list:
                text_new += item[item.find(")")+1:].strip() + ". "
            text_updated = ""
            number = 1
            for item_up in text_new.split(".")[:-1]:
                text_updated += str(number) + ") " + item_up.strip() + ". "
                number+=1
        
        elif len(text_updated_list)==1:
            text_updated = "1) " + text_updated_list[0][text_updated_list[0].find(")")+1:].strip() + ". "

        else:
            text_updated = ""
        self.lab_pustules.setText(text_updated)
        self.entered_pustules_text = self.lab_pustules.text().split(".")[:-1]
        self.update_editing_menu (self.pustule_edit_button)
        self.scroll.takeWidget()
        self.picture = Winform(self.file_name, soft_tissue_zones=self.soft_tissue_checked_zones)
        self.picture.update()
        self.scroll.setWidget(self.picture)

    def zone_detailes_action(self, action):
        text = action.text()
        self.zone_detailes_menu_button.setText(text)
        text = "в %sм отделе " %(text)
        self.zone_detailes_text = text
        self.forming_pustule_description()

    def type_action(self, action):
        # ["округлая", "овальная", "конусообразная", "плоская"]
        text = action.text()
        self.type_menu_button.setText(text)
        if self.quantity_menu_button.text() == "множественные":
            text = text[:-2] + "ые"
        text = "%s, " %(text)
        self.pustule_type_text = text
        self.forming_pustule_description()

    def quantity_action(self, action):
        text = action.text()
        self.quantity_menu_button.setText(text)
        if text == "множественные":
            text = "множественные пустулы"
        elif text == "единичная":
            text = "пустула"
        text = "%s " %(text)

        self.pustule_quantity_text = text.capitalize()


        if self.kind_menu_button.text() != "":
            print(self.kind_menu_button.text())
            for action in self.menu_kind.actions():
                if action.text() == self.kind_menu_button.text():
                    self.kind_action(action)
            
        if self.type_menu_button.text() != "":
            print(self.type_menu_button.text())
            for action in self.menu_type.actions():
                if action.text() == self.type_menu_button.text():
                    self.type_action(action)

        if self.excav_menu_button.text() != "":
            print(self.excav_menu_button.text())
            for action in self.menu_excav.actions():
                if action.text() == self.excav_menu_button.text():
                    self.excav_action(action)

        self.forming_pustule_description()


    

    def kind_action(self, action):
        # ["вокруг волосяного фолликула", "поверхностная", "глубокая"]
        text = action.text()
        self.kind_menu_button.setText(text)
        if self.quantity_menu_button.text() == "множественные":
            if text == "поверхностная":
                text = text[:-2] + "ые"
            elif text == "глубокая":
                text = text[:-2] + "ие"
            else:
                text = "вокруг волосяных фолликулов"
        text = "%s, " %(text.lower())
        self.pustule_kind_text = text
        self.forming_pustule_description()
        
    def excav_action(self, action):
        # ["вскрыта", "не вскрыта", "частично вскрыты"]
        text = action.text()
        self.excav_menu_button.setText(text)
        if self.quantity_menu_button.text() == "множественные" and text !="частично вскрыты":
            text = text[:-1] + "ые"
            text = "%s, " %(text.lower())
        else:
            text = "%s, " %(text.lower())
        self.pustule_excav_text = text
        self.forming_pustule_description()
        
    def content_action(self, action):
        # ["светлое, прозрачное", "светлое, мутное", "бурое, прозрачное", "бурое, мутное"]
        text = action.text()
        self.content_menu_button.setText(text)
        text = text.replace("ое","ым")
        text = "с %s содержимым, " %(text.lower())
        self.pustule_content_text = text
        self.forming_pustule_description()

    def add_size(self):
        l = self.pustule_size_lenght.text()
        w = self.pustule_size_width.text()
        l_com ="в см, Д"
        w_com = ",Ш"

        if l =="": l_com = ""
        
        if w =="": 
            w_com = ""
        else:
                w = "x"+w

        self.pustule_size_text = "размерами: %s%s (%s%s), " % (l, w, l_com, w_com)
        self.forming_pustule_description()


    def mouseReleaseEvent(self, event):
        posMouse =  event.pos()
        
        #try:



        if self.picture and self.scroll.rect().contains(posMouse):
            print("Under Mouse")
            

            #print(self.picture.get_checked_zones())
            #print(len(self.picture.get_checked_zones()))
            if self.picture.get_checked_zones() != []:
                line_prepared = ""
                for item in self.picture.get_checked_zones():
                    line = str(item)
                    line_format = []

                    splited_str = []
                    item = ""
                    print(line)
                    line_len = len(line)
                    i = 1
                    for ch in line:
                        print(ch)
                        if ch == " ":
                            splited_str.append(item)
                            item = ""
                            i+=1
                            continue
                        item += ch
                        if i == line_len:
                            splited_str.append(item)
                        i+=1

                    print(splited_str)

                    for word in splited_str:
                        print(word)
                        if word[-2:] == "ая":
                            word = word[:-2] +"ой"
                            line_format.append(word)

                        elif word[-2:] == "ые":
                            word = word[:-2] +"ых"
                            line_format.append(word)
                    

                        elif word[-2:] == "яя":
                            word = word[:-2] +"ей"
                            line_format.append(word)
                    

                        elif word[-2:] == "ть":
                            word = word[:-2] +"ти"
                            line_format.append(word)
                    

                        elif word[-2:] == "ка":
                            word = word[:-2] +"ки"
                            line_format.append(word)

                        else:
                            line_format.append(word)
                    print(line_format)
                    
                    if line_prepared !="":
                        line_prepared+= " и "

                    k=1
                    for word in line_format:
                        line_prepared += word
                        if k <len(line_format):
                            line_prepared += " "
                        k+=1
                    

                self.pustule_zone = "%s, " %(line_prepared)
                


                self.forming_pustule_description()
                
                if len(self.picture.get_checked_zones()) >= 1:
                    
                    #screen = QApplication.primaryScreen()
                    #self.screenshot = screen.grabWindow(self.picture.winId())
                    #self.screenshot = QPixmap(self.screenshot)
                    #print(self.screenshot)

                    self.waiting_label = QLabel()
                    self.waiting_label.setStyleSheet('''background: rgb(250,128,114); 
                                                    font: 22pt/24pt sans-serif;
                                                    text-align: center;''')

                    self.text_waiting = "Зона: %s.\nВведите параметры кровоподтека " %(str(self.picture.get_checked_zones()[0]))
                    
                    #time.sleep(0.3)
                    
                    self.waiting_label.setText(self.text_waiting)
                    print("Paint event")
                    #self.scroll.setWidget(self.waiting_label)
                    #self.scroll.setAlignment(Qt.AlignCenter)

                #to_draw = QRect(0, 0, self.width() - 1, self.height() - 1)
                #self.qp = QPainter(self)
                #self.qp.begin(self)
                #self.qp.setPen(QColor(168, 34, 3))
                #self.qp.setFont(QFont('Decorative', 10))
                #self.qp.drawPixmap(to_draw, self.screenshot)
                #self.qp.drawText(to_draw, Qt.AlignCenter, self.text_waiting)
                #self.waiting_label.setPixmap(self.qp)
                #self.qp.end()
                #self.scroll.setWidget(self.waiting_label)
                #screenshot.save('shot.jpg', 'jpg')
                #self.scroll.blockSignals(True)

                
                
                #self.waiting_label.setPixmap(self.screenshot)
                #self.scroll.setWidget(self.waiting_label)
                #screenshot.save('shot.jpg', 'jpg')

                #self.scroll.blockSignals(True)
                
                    #msg = QMessageBox()
                    #msg.setWindowTitle("Информация")
                    #msg.setText("Введите параметры раны (справа)")
                    #msg.setIcon(QMessageBox.Information)
                    #msg.exec_()
            else:
                self.pustule_zone = ""
                self.forming_pustule_description()
                print("MousePres out off detected zones!")

            
            
                self.update()
        else:
            print("winform doesnot exist")
        #except RuntimeError:
        #   print(some ERROR)

    def picture_view(self):
        if self.sender().text() == "Вид спереди":
            self.scroll.takeWidget()
            self.file_name = "front_clear.bmp"
            self.picture = Winform(self.file_name, soft_tissue_zones=self.soft_tissue_checked_zones)
            self.picture.update()
            self.scroll.setWidget(self.picture)
            #self.chosen_zones.setText("")
            #self.chosen_zones.update()
            sizeObject = QDesktopWidget().screenGeometry(-1)
            self.resize(self.picture.width(), (sizeObject.height()-90))
            self.update()
            
        else:
            self.scroll.takeWidget()
            self.file_name = "back_clear.bmp"
            self.picture = Winform(self.file_name, soft_tissue_zones=self.soft_tissue_checked_zones)
            self.picture.update()
            self.scroll.setWidget(self.picture)
            #self.chosen_zones.setText("")
            #self.chosen_zones.update()
            sizeObject = QDesktopWidget().screenGeometry(-1)
            self.resize(self.picture.width(), (sizeObject.height()-90))
            self.update()
            
    def add_formed_pustule(self):
        
        if (self.pustule_size_text!="" and 
            self.type_menu_button.text()!="" and
            self.quantity_menu_button.text()!="" and
            self.kind_menu_button.text()!="" and
            self.content_menu_button.text()!="" and
            self.excav_menu_button.text()!="" and
            self.picture.get_checked_zones()!=[]):

            text = self.lab_pustules.text()
            
            if text:
                text = text[0:-2] + ". "
                self.lab_pustules.setText(text + str(len(self.entered_pustules_text) +1)+ ") " + (self.inner_chosen_zones.text()[0:-2] + ". "))
                self.entered_pustules_text = self.lab_pustules.text().split(".")[:-1]
                self.update_editing_menu(self.pustule_edit_button)

            else:
                self.lab_pustules.setText("1) " + self.inner_chosen_zones.text()[0:-2] + ". ")
                self.entered_pustules_text = [self.lab_pustules.text().split(".")[:-1]]
                self.update_editing_menu (self.pustule_edit_button)
            

            self.soft_tissue_checked_zones["pustule"].append(self.picture.get_checked_zones()[:])



            #print(self.entered_wounds_text)
            self.pustule_zone = ""
            self.pustule_size_text = ""
            self.pustule_size_lenght.setText("")
            self.pustule_size_width.setText("")
            self.zone_detailes_menu_button.setText("")
            self.zone_detailes_menu_button.color = "white"
            self.zone_detailes_text=""



            self.type_menu_button.setText("")
            self.quantity_menu_button.setText("")
            self.kind_menu_button.setText("")
            self.content_menu_button.setText("")
            self.excav_menu_button.setText("")

            self.pustule_type_text = ""
            self.pustule_quantity_text = ""
            self.pustule_kind_text = ""
            self.pustule_content_text = ""
            self.pustule_excav_text = ""

            self.inner_chosen_zones.setText("")

            self.scroll.takeWidget()
            self.picture = Winform(self.file_name, soft_tissue_zones=self.soft_tissue_checked_zones)
            self.picture.update()
            self.scroll.setWidget(self.picture)
            return 1
        
        else:
            msg = QMessageBox()
            msg.setWindowTitle("Информация")
            msg.setText("Не все параметры кровоподтека введены!!!")
            msg.setIcon(QMessageBox.Information)
            msg.exec_()
            return 0


    def forming_pustule_description(self):
        if len(self.picture.get_checked_zones()) >1:
            self.zone_detailes_menu_button.color = "#FF0700"
            self.zone_detailes_text = ""
            self.zone_detailes_menu_button.setText("")
        else:
            self.zone_detailes_menu_button.color = "white"

        self.inner_chosen_zones.setText(self.pustule_quantity_text + self.pustule_excav_text + self.zone_detailes_text + 
                                        self.pustule_zone + self.pustule_content_text + self.pustule_type_text + 
                                        self.pustule_size_text + self.pustule_kind_text)


    def picture_clear(self):
        self.scroll.takeWidget()
        self.picture = Winform(self.file_name, soft_tissue_zones=self.soft_tissue_checked_zones)
        self.inner_chosen_zones.setText("")
        self.picture.update()
        self.scroll.setWidget(self.picture)
        self.forming_pustule_description()

    def get_pustule_text(self):

        text = self.lab_pustules.text()
        if text !="":
            text_new =""
            for item in text.split(".")[:-1]:
                text_new += item[item.find(")")+1:].strip() + ". "
            print("text_new=", text_new)
            return text_new
        else:
            return ""

    def get_pustule_zones(self):
        return self.soft_tissue_checked_zones["pustule"]


    def btn_to_close(self):
        if self.inner_chosen_zones.text() != "":
            msg = QMessageBox()
            msg.setWindowTitle("Информация")
            msg.setText("Сохранить невведенное описание кровоподтека")
            msg.setIcon(QMessageBox.Information)
            yes =  PushButton("Yes")
            no=  PushButton("No")
            cancel=  PushButton("Cancel")
            msg.addButton(yes, QMessageBox.AcceptRole)
            msg.addButton(no, QMessageBox.RejectRole)
            msg.addButton(cancel, QMessageBox.DestructiveRole)
            ret = msg.exec_()
            
            
            
            if ret == 0:
                text = self.lab_pustules.text()
                text = text[0:-2] + ". "
                self.lab_pustules.setText(text + (self.inner_chosen_zones.text()[0:-2] + ". "))
                self.inner_chosen_zones.setText("")
                self.pustule_send_info.emit()
                self.close()
                self.setParent(None)
            elif ret == 1:
                self.pustule_send_info.emit()
                self.close()
                self.setParent(None)
            
        else:
            self.pustule_send_info.emit()
            self.close()
            self.setParent(None)
        
        return self.lab_pustules.text()


    def closeEvent(self, event):
        if self.inner_chosen_zones.text() != "":
            print(self.inner_chosen_zones.text())
            
            msgbox = QMessageBox(QMessageBox.Question, "Внимание!", "Имеются не добавленные зоны отечности,\nдобавить их в общее описание?")
            msgbox.addButton(QMessageBox.Yes)
            msgbox.addButton(QMessageBox.No)
            msgbox.addButton(QMessageBox.Cancel)
            msgbox.setDefaultButton(QMessageBox.Cancel)
            reply = msgbox.exec()



            #reply = QMessageBox.question(self, "Внимание!",
            #                            "Имеются не добавленные зоны отечности,\nдобавить их в общее описание?",
            #                            QMessageBox.Yes|QMessageBox.No|QMessageBox.Cancel)
            if reply == QMessageBox.Yes:
                if self.add_formed_pustule() == 1:
                    self.pustule_send_info.emit()
                    event.accept()
                else:
                    event.ignore()
                    print("SMTH is broken")

            elif reply == QMessageBox.Cancel:
                event.ignore()

            elif reply==QMessageBox.No:
                if self.picture.get_checked_zones() !=[] and self.soft_tissue_checked_zones["pustule"] !=[]:
                    self.soft_tissue_checked_zones["pustule"] = self.soft_tissue_checked_zones["pustule"][:-1]

                self.pustule_send_info.emit()
                event.accept()


        else:

            self.pustule_send_info.emit()
            event.accept()


    

if __name__ == "__main__":
    app = QApplication(sys.argv)
    
    form = EdemaWindow()
    form.show()
    sys.exit(app.exec_())