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




class AbrasionWindow(QWidget):
    abrasion_send_info = pyqtSignal()
    def __init__(self, entered_abrasions, soft_tissue_zones, **kwargs):
        super().__init__( **kwargs)
        
        self.entered_abrasions_text = entered_abrasions
        self.soft_tissue_checked_zones = soft_tissue_zones
        self.initUI()

    def initUI(self):
        
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

        
        self.abrasions = QVBoxLayout()

        self.lab_entered_abrasions = QLabel("Введенные ссадины")
        self.entered_abrasions = QGroupBox(self.lab_entered_abrasions.text())
        
        self.lab_abrasions = QLabel()
        self.lab_abrasions.setWordWrap(True)
        if self.entered_abrasions_text != "":
            self.entered_abrasions_text = self.entered_abrasions_text[:-1]
            text_to_add = ""
            counter = 1
            for item in self.entered_abrasions_text:
                text_to_add += str(counter) + ") " + item + ". "
                counter+=1
            self.lab_abrasions.setText(text_to_add)
            self.entered_abrasions_text = text_to_add.split(".")[:-1]

        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        scroll.setWidget(self.lab_abrasions)

        self.abrasions.addWidget(scroll)
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

        self.abrasion_edit_button = QPushButton("Редактировать")
        
        self.update_editing_menu(self.abrasion_edit_button)

        
        
        self.abrasion_edit_button.setStyleSheet('''
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
        self.abrasions.addWidget(self.abrasion_edit_button)


        self.entered_abrasions.setLayout(self.abrasions)

        self.entered_abrasions.setStyleSheet('''

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

        self.abrasion_text_forming = QVBoxLayout()
        self.abrasion_zone = ""
        self.chosen_zones = QGroupBox("Текущее описание ссадины")
        self.inner_chosen_zones = QLabel()
        self.inner_chosen_zones.setWordWrap(True)
        self.abrasion_text_forming.addWidget(self.inner_chosen_zones)
        self.button_new_abrasion = PushButton("Ввести ссадину")
        self.button_new_abrasion.clicked.connect(self.add_formed_abrasion)
        self.abrasion_text_forming.addWidget(self.button_new_abrasion)
        self.chosen_zones.setLayout(self.abrasion_text_forming)
        
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


        self.abrasion_type = QGroupBox("Форма ссадины")
        self.abrasion_type.setStyleSheet('''
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
        self.abrasion_type_box = QVBoxLayout()
        self.abrasion_type_text = ""
        clinic_types = ["линейная", "округлая", "овальная", "неправильная овальная", "фигурная"]
        menu_type = QMenu(self)
        self.create_menu(clinic_types, menu_type)
        
        self.type_menu_button = QPushButton()
        self.type_menu_button.setMenu(menu_type)
        menu_type.triggered.connect(self.type_action)
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
        menu_type.setStyleSheet('''
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
        
        self.abrasion_type_box.addWidget(self.type_menu_button)
        self.abrasion_type.setLayout(self.abrasion_type_box)

        self.abrasion_size = QGroupBox("Размер ссадины")
        self.abrasion_size.setStyleSheet('''
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
        self.abrasion_size_box = QVBoxLayout()
        self.abrasion_size_text = ""
        self.label_lenght = QLabel("Длинна, см")
        self.abrasion_size_lenght = QLineEdit(self.label_lenght)
        self.abrasion_size_lenght.textChanged.connect(self.add_size)
        self.abrasion_size_lenght.setStyleSheet('border: 2px solid grey; border-radius: 5px;')
        self.label_width = QLabel("Ширина, см")
        self.abrasion_size_width = QLineEdit(self.label_width)
        self.abrasion_size_width.textChanged.connect(self.add_size)
        self.abrasion_size_width.setStyleSheet('border: 2px solid grey; border-radius: 5px;')
        
        self.abrasion_size_box.addWidget(self.label_lenght)
        self.abrasion_size_box.addWidget(self.abrasion_size_lenght)
        self.abrasion_size_box.addWidget(self.label_width)
        self.abrasion_size_box.addWidget(self.abrasion_size_width)
        

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

        self.abrasion_size.setLayout(self.abrasion_size_box)



        self.abrasion_direction = QGroupBox("Направление ссадины")
        self.abrasion_direction.setStyleSheet('''
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
        self.abrasion_direction_box = QVBoxLayout()
        self.abrasion_direction_text = ""
        menu_direction = QMenu(self)
        
        directions = ["вертикальное", "горизонтальное", "косое (сверху-вниз)", "косое (снизу-вверх)", "---"]
        for z in directions:
            action = menu_direction.addAction(z)
            action.setIconVisibleInMenu(False)
        
        self.direction_menu_button = QPushButton()
        self.direction_menu_button.setMenu(menu_direction)
        menu_direction.triggered.connect(self.direction_action)

        self.direction_menu_button.setStyleSheet('''
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
        menu_direction.setStyleSheet('''
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

        self.abrasion_direction_box.addWidget(self.direction_menu_button)
        self.abrasion_direction.setLayout(self.abrasion_direction_box)
        
        

        self.abrasion_bottom = QGroupBox("Дно ссадины")
        self.abrasion_bottom.setStyleSheet('''
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

        menu_bottom = QMenu(self)
        bottoms = ["влажная, западает", "под корочкой"]
        for z in bottoms:
            action = menu_bottom.addAction(z)
            action.setIconVisibleInMenu(False)
        
        self.bottom_menu_button = QPushButton()
        self.bottom_menu_button.setMenu(menu_bottom)
        menu_bottom.triggered.connect(self.bottom_action)

        self.bottom_menu_button.setStyleSheet('''
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
        menu_bottom.setStyleSheet('''
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
        self.abrasion_bottom_box = QVBoxLayout()
        self.abrasion_bottom_text = ""
        self.abrasion_bottom_box.addWidget(self.bottom_menu_button)
        self.abrasion_bottom.setLayout(self.abrasion_bottom_box)
        


        self.right_scroll = QScrollArea()
        self.right_scroll.setStyleSheet("""
            QScrollArea{
                border: none;
            }
            """)
        self.vbox_right = QVBoxLayout()
        self.vbox_right.addWidget(self.entered_abrasions)
        self.vbox_right.addWidget(self.chosen_zones)
        self.vbox_right.addWidget(self.zone_detailes)
        self.vbox_right.addWidget(self.abrasion_type)
        self.vbox_right.addWidget(self.abrasion_size)
        self.vbox_right.addWidget(self.abrasion_direction)
        self.vbox_right.addWidget(self.abrasion_bottom)
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
        
        
        self.setWindowTitle ("Ссадины")
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

        if len(self.entered_abrasions_text) ==1:
            abrasion_numbers = ["Удалить ссадину 1)..."]
        elif self.entered_abrasions_text == []:
            abrasion_numbers = []
        else: 
            abrasion_numbers = ["Удалить ссадину " + i.strip()[:2] + "..." for i in  self.entered_abrasions_text]
        #wound_numbers = [i[:2] + "" for i in  self.entered_wounds_text]
        menu_type_abrasion = QMenu(self)
        self.create_menu(abrasion_numbers, menu_type_abrasion)
        
        pushbut.setMenu(menu_type_abrasion)
        menu_type_abrasion.triggered.connect(self.editing_action)
        menu_type_abrasion.setStyleSheet('''
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
        text_updated_list = self.lab_abrasions.text().split(".")[:-1]
        text_updated_list.pop(number)
        self.soft_tissue_checked_zones["abrasion"].pop(number)
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
        self.lab_abrasions.setText(text_updated)
        self.entered_abrasions_text = self.lab_abrasions.text().split(".")[:-1]
        self.update_editing_menu (self.abrasion_edit_button)
        self.scroll.takeWidget()
        self.picture = Winform(self.file_name, soft_tissue_zones=self.soft_tissue_checked_zones)
        self.picture.update()
        self.scroll.setWidget(self.picture)

    def zone_detailes_action(self, action):
        text = action.text()
        self.zone_detailes_menu_button.setText(text)
        text = "в %sм отделе " %(text)
        self.zone_detailes_text = text
        self.forming_abrasion_description()

    def type_action(self, action):
        text = action.text()
        self.type_menu_button.setText(text)
        text = "%s ссадина " %(text)
        self.abrasion_type_text = text.capitalize()
        self.forming_abrasion_description()

    def direction_action(self, action):
        text = action.text()
        self.direction_menu_button.setText(text)
        if text != "---":
            list_text = text.split(" ")
            if len(list_text)>1:
                list_text[0]= list_text[0][:-1]+"го"
            else:
                list_text[0]= list_text[0][:-1]+"го"
            
            text_1 = ""
            for i in list_text:
                text_1 = text_1+ " " +i 
            text = "%s направления, " %(text_1.lower())
            self.abrasion_direction_text = text
            self.forming_abrasion_description()
        else:
            self.abrasion_direction_text = ""
            self.forming_abrasion_description()

    def bottom_action(self, action):
        text = action.text()
        self.bottom_menu_button.setText(text)
        text = "поверхность ссадины %s, " %(text.lower())
        self.abrasion_bottom_text = text
        self.forming_abrasion_description()



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
                    

                self.abrasion_zone = "%s, " %(line_prepared)




                
                self.forming_abrasion_description()
                
                if len(self.picture.get_checked_zones()) >= 1:
                    
                    #screen = QApplication.primaryScreen()
                    #self.screenshot = screen.grabWindow(self.picture.winId())
                    #self.screenshot = QPixmap(self.screenshot)
                    #print(self.screenshot)

                    self.waiting_label = QLabel()
                    self.waiting_label.setStyleSheet('''background: rgb(250,128,114); 
                                                    font: 22pt/24pt sans-serif;
                                                    text-align: center;''')

                    self.text_waiting = "Зона: %s.\nВведите параметры ссадины " %(str(self.picture.get_checked_zones()[0]))
                    
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
                self.abrasion_zone = ""
                self.forming_abrasion_description()
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
            
    def add_formed_abrasion(self):
        
        if (self.abrasion_size_text!="" and 
            self.type_menu_button.text()!="" and
            self.bottom_menu_button.text()!="" and
            self.direction_menu_button.text()!="" and
            self.picture.get_checked_zones()!=[]):

            text = self.lab_abrasions.text()
            
            if text:
                text = text[0:-2] + ". "
                self.lab_abrasions.setText(text + str(len(self.entered_abrasions_text) +1)+ ") " + (self.inner_chosen_zones.text()[0:-2] + ". "))
                self.entered_abrasions_text = self.lab_abrasions.text().split(".")[:-1]
                self.update_editing_menu(self.abrasion_edit_button)

            else:
                self.lab_abrasions.setText("1) " + self.inner_chosen_zones.text()[0:-2] + ". ")
                self.entered_abrasions_text = [self.lab_abrasions.text().split(".")[:-1]]
                self.update_editing_menu (self.abrasion_edit_button)
            
            #print(self.entered_wounds_text)

            self.soft_tissue_checked_zones["abrasion"].append(self.picture.get_checked_zones()[:])


            self.abrasion_zone = ""
            self.abrasion_size_text = ""
            self.abrasion_size_lenght.setText("")
            self.abrasion_size_width.setText("")
            self.zone_detailes_menu_button.setText("")
            self.zone_detailes_menu_button.color = "white"

            self.type_menu_button.setText("")
            self.bottom_menu_button.setText("")
            self.direction_menu_button.setText("")
            
            self.zone_detailes_text=""
            self.abrasion_type_text = ""
            self.abrasion_bottom_text = ""
            self.abrasion_direction_text = ""

            self.inner_chosen_zones.setText("")

            self.scroll.takeWidget()
            self.picture = Winform(self.file_name, soft_tissue_zones=self.soft_tissue_checked_zones)
            self.picture.update()
            self.scroll.setWidget(self.picture)
            print(self.soft_tissue_checked_zones)
            return 1
        else:
            msg = QMessageBox()
            msg.setWindowTitle("Информация")
            msg.setText("Не все параметры ссадины введены!!!")
            msg.setIcon(QMessageBox.Information)
            msg.exec_()
            return 0

    def add_size(self):
        l = self.abrasion_size_lenght.text()
        w = self.abrasion_size_width.text()
        l_com ="в см, Д"
        w_com = ",Ш"

        if l =="": l_com = ""
        
        if w =="": 
            w_com = ""
        else:
                w = "x"+w

        self.abrasion_size_text = "размерами: %s%s (%s%s), " % (l, w, l_com, w_com)
        self.forming_abrasion_description()


    def forming_abrasion_description(self):
        
        if len(self.picture.get_checked_zones()) >1:
            self.zone_detailes_menu_button.color = "#FF0700"
            self.zone_detailes_text = ""
            self.zone_detailes_menu_button.setText("")
        else:
            self.zone_detailes_menu_button.color = "white"

        self.inner_chosen_zones.setText(self.abrasion_type_text + self.zone_detailes_text + self.abrasion_zone +
                                        self.abrasion_size_text + self.abrasion_direction_text + self.abrasion_bottom_text)


    def picture_clear(self):
        self.scroll.takeWidget()
        self.picture = Winform(self.file_name, soft_tissue_zones=self.soft_tissue_checked_zones)
        self.inner_chosen_zones.setText("")
        self.picture.update()
        self.scroll.setWidget(self.picture)
        self.forming_abrasion_description()

    def get_abrasion_text(self):

        text = self.lab_abrasions.text()
        if text !="":
            text_new =""
            for item in text.split(".")[:-1]:
                text_new += item[item.find(")")+1:].strip().capitalize() + ". "
            print("text_new=", text_new)
            return text_new
        else:
            return ""



    def get_abrasion_zones(self):
        return self.soft_tissue_checked_zones["abrasion"]


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
                if self.add_formed_abrasion() == 1:
                    self.abrasion_send_info.emit()
                    event.accept()
                else:
                    event.ignore()
                    print("SMTH is broken")


            elif reply == QMessageBox.Cancel:
                event.ignore()

            elif reply==QMessageBox.No:

                self.abrasion_send_info.emit()
                event.accept()


        else:

            self.abrasion_send_info.emit()
            event.accept()


    

if __name__ == "__main__":
    app = QApplication(sys.argv)
    
    form = EdemaWindow()
    form.show()
    sys.exit(app.exec_())