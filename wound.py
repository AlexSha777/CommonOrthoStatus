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


class WoundWindow(QWidget):
    wound_send_info = pyqtSignal()
    def __init__(self, entered_wounds, soft_tissue_zones, **kwargs):
        super().__init__( **kwargs)
        
        self.entered_wounds_text = entered_wounds
        self.soft_tissue_checked_zones = soft_tissue_zones
        self.initUI()

    def initUI(self):
        self.file_name = "front_clear.bmp"
        print(self.entered_wounds_text)
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

        
        self.wounds = QVBoxLayout()

        self.lab_entered_wounds = QLabel("Введенные раны")
        self.entered_wounds = QGroupBox(self.lab_entered_wounds.text())
        
        self.lab_wounds = QLabel()
        self.lab_wounds.setWordWrap(True)
        if self.entered_wounds_text != "":
            self.entered_wounds_text = self.entered_wounds_text[:-1]
            text_to_add = ""
            counter = 1
            for item in self.entered_wounds_text:
                text_to_add += str(counter) + ") " + item + ". "
                counter+=1
            self.lab_wounds.setText(text_to_add)
            self.entered_wounds_text = text_to_add.split(".")[:-1]

        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        scroll.setWidget(self.lab_wounds)

        self.wounds.addWidget(scroll)
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

        self.wound_edit_button = QPushButton("Редактировать")
        
        self.update_editing_menu(self.wound_edit_button)

        
        
        self.wound_edit_button.setStyleSheet('''
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
        self.wounds.addWidget(self.wound_edit_button)


        self.entered_wounds.setLayout(self.wounds)

        self.entered_wounds.setStyleSheet('''

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

        self.wound_text_forming = QVBoxLayout()
        self.wound_zone = ""
        self.zone_detailed_text = ""
        self.chosen_zones = QGroupBox("Текущее описание раны")
        self.inner_chosen_zones = QLabel()
        self.inner_chosen_zones.setWordWrap(True)
        self.wound_text_forming.addWidget(self.inner_chosen_zones)
        self.button_new_wound = PushButton("Ввести рану")
        self.button_new_wound.clicked.connect(self.add_formed_wound)
        self.wound_text_forming.addWidget(self.button_new_wound)
        self.chosen_zones.setLayout(self.wound_text_forming)
        
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
        menu_zone_detailes.setObjectName("zone_detailes")
        self.create_menu(zone_detailes, menu_zone_detailes)
        
        self.zone_detailes_menu_button = PushButton_zone()   # check_zone_number  zone_number
        self.zone_detailes_menu_button.zones_checked_determine.connect(self.check_zone_number)
        self.zone_detailes_menu_button.setObjectName("zone_detailes")
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





        self.label_wound_type = QLabel("Клинический тип раны")
        self.wound_type = QGroupBox(self.label_wound_type.text())
        self.wound_type.setStyleSheet('''
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
        self.wound_type_box = QVBoxLayout()
        self.wound_type_text = ""
        clinic_types = [ "Резаная", "Колотая", "Рубленая", "Рваная", "Колото-резаная", "Ушибленная", 
                        "Скальпированная", "Размозженная", "Операционная", "Укушенная", "Огнестрельная", "Язва"]
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
        
        self.wound_type_box.addWidget(self.type_menu_button)
        self.wound_type.setLayout(self.wound_type_box)

        self.label_wound_size = QLabel("Размер раны")
        self.wound_size = QGroupBox(self.label_wound_size.text())
        self.wound_size.setStyleSheet('''
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
        self.wound_size_box = QVBoxLayout()
        self.wound_size_text = ""
        self.label_lenght = QLabel("Длинна, см")
        self.wound_size_lenght = QLineEdit(self.label_lenght)
        self.wound_size_lenght.setMinimumHeight(20)
        self.wound_size_lenght.textChanged.connect(self.add_size)
        self.wound_size_lenght.setStyleSheet('border: 2px solid grey; border-radius: 5px;')
        self.label_width = QLabel("Ширина, см")
        self.wound_size_width = QLineEdit(self.label_width)
        self.wound_size_width.setMinimumHeight(20)
        self.wound_size_width.textChanged.connect(self.add_size)
        self.wound_size_width.setStyleSheet('border: 2px solid grey; border-radius: 5px;')
        self.label_depth = QLabel("Глубина, см")
        self.wound_size_depth = QLineEdit(self.label_depth)
        self.wound_size_depth.setMinimumHeight(20)
        self.wound_size_depth.textChanged.connect(self.add_size)
        self.wound_size_depth.setStyleSheet('border: 2px solid grey; border-radius: 5px;')
        self.wound_size_box.addWidget(self.label_lenght)
        self.wound_size_box.addWidget(self.wound_size_lenght)
        self.wound_size_box.addWidget(self.label_width)
        self.wound_size_box.addWidget(self.wound_size_width)
        self.wound_size_box.addWidget(self.label_depth)
        self.wound_size_box.addWidget(self.wound_size_depth)

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

        self.wound_size.setLayout(self.wound_size_box)



        self.label_wound_form = QLabel("Форма раны")
        self.wound_form = QGroupBox(self.label_wound_form.text())
        self.wound_form.setStyleSheet('''
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
        self.wound_form_box = QVBoxLayout()
        self.wound_form_text = ""
        self.lab_wound_form_box = QLabel("По А.И. Муханову")
        
        d = [
            {"Линейная": ["прямолинейная", "Линейная дуговидная", "линейно-ломанная"]},
            {"Лучистая": ["Г-образная", "Т-образная", "У-образная", "X-образная", "Н-образная"]},
            "Округлая",
            "Щелевидная",
            "Веретенообразная",
            "Серповидная",
            "Зигзагообразная",
            "Древовидная",
            "Прямоугольная",
            "Треугольная",
            "Трапециевидная",
            "Лоскутная",
            "Неправильной формы" ]
        menu_form = QMenu(self)
        self.create_menu(d, menu_form)
        self.form_menu_button = QPushButton()
        self.form_menu_button.setMenu(menu_form)
        menu_form.triggered.connect(self.form_action)
        self.form_menu_button.setStyleSheet('''
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
        menu_form.setStyleSheet('''
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
        
        self.wound_form_box.addWidget(self.lab_wound_form_box)

        self.wound_form_box.addWidget(self.form_menu_button)

        self.wound_form.setLayout(self.wound_form_box)
    


        self.label_wound_margin = QLabel("Края раны")
        self.wound_margin = QGroupBox(self.label_wound_margin.text())
        self.wound_margin.setStyleSheet('''
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
        self.wound_margin_box = QVBoxLayout()
        self.wound_margin_text = ""
        menu_margin = QMenu(self)
        
        margins = ["Ровные", "Неровные не оссадненные", "Неровные оссадненные"]
        for z in margins:
            action = menu_margin.addAction(z)
            action.setIconVisibleInMenu(False)
        
        self.margin_menu_button = QPushButton()
        self.margin_menu_button.setMenu(menu_margin)
        menu_margin.triggered.connect(self.margin_action)

        self.margin_menu_button.setStyleSheet('''
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
        menu_margin.setStyleSheet('''
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

        self.wound_margin_box.addWidget(self.margin_menu_button)
        self.wound_margin.setLayout(self.wound_margin_box)
        
        self.label_wound_bottom = QLabel("Дно раны")
        self.wound_bottom = QGroupBox(self.label_wound_bottom.text())
        self.wound_bottom.setStyleSheet('''
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
        bottoms = ["Грануляции", "Налет фибрина", "Грануляции и налет фибрина", "Плотный струп", "Рыхлый струп", 
                    "Металлоконструкция", "Кость", "Сухожилие"]
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
        self.wound_bottom_box = QVBoxLayout()
        self.wound_bottom_text = ""
        self.wound_bottom_box.addWidget(self.bottom_menu_button)
        self.wound_bottom.setLayout(self.wound_bottom_box)
        
        self.label_wound_excretion = QLabel("Отделяемое из раны")
        self.wound_excretion = QGroupBox(self.label_wound_excretion.text())
        self.wound_excretion.setStyleSheet('''
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
        menu_excretion = QMenu(self)
        excretions = ["Нет", 
                    {"Скудное": ["Скудное серозное", "Скудное гнойное"]},
                    {"Умеренное": ["Умеренное серозное", "Умеренное гнойное", "Умеренное серозно-гнойное"]},
                    {"Обильное": ["Обильное серозное", "Обильное гнойное", "Обильное серозно-гнойное"]}
                    ]
        self.create_menu(excretions, menu_excretion)
        
        self.excretion_menu_button = QPushButton()
        self.excretion_menu_button.setMenu(menu_excretion)
        menu_excretion.triggered.connect(self.excretion_action)

        self.excretion_menu_button.setStyleSheet('''
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
        menu_excretion.setStyleSheet('''
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
        self.wound_excretion_box = QVBoxLayout()
        self.wound_excretion_text = ""
        self.wound_excretion.setLayout(self.wound_excretion_box)
        self.wound_excretion_box.addWidget(self.excretion_menu_button)
        


        self.label_wound_channel = QLabel("Раневой канал")
        self.wound_channel = QGroupBox(self.label_wound_channel.text())
        self.wound_channel.setStyleSheet('''
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
        menu_channel = QMenu(self)
        channels = [
                    "Нет",
                    "Слепой",
                    {"Проникающий": ["Проникающий в брюшную полость", "Проникающий в грудную полость", "Проникающий в полость черепа"]},
                    ]
        self.create_menu(channels, menu_channel)
        
        self.channel_menu_button = QPushButton()
        self.channel_menu_button.setMenu(menu_channel)
        menu_channel.triggered.connect(self.channel_action)

        self.channel_menu_button.setStyleSheet('''
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
        menu_channel.setStyleSheet('''
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

        self.wound_channel_box = QVBoxLayout()
        self.wound_channel_text = ""
        self.wound_channel_box.addWidget(self.channel_menu_button)
        self.wound_channel.setLayout(self.wound_channel_box)
        



        self.right_scroll = QScrollArea()
        self.right_scroll.setStyleSheet("""
            QScrollArea{
                border: none;
            }
            """)
        self.vbox_right = QVBoxLayout()
        self.vbox_right.addWidget(self.entered_wounds)
        self.vbox_right.addWidget(self.chosen_zones)
        self.vbox_right.addWidget(self.zone_detailes)
        self.vbox_right.addWidget(self.wound_type)
        self.vbox_right.addWidget(self.wound_size)
        self.vbox_right.addWidget(self.wound_form)
        self.vbox_right.addWidget(self.wound_margin)
        self.vbox_right.addWidget(self.wound_bottom)
        self.vbox_right.addWidget(self.wound_excretion)
        self.vbox_right.addWidget(self.wound_channel)
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
        
        
        self.setWindowTitle ("Раны")
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

        if len(self.entered_wounds_text) ==1:
            wound_numbers = ["Удалить рану 1)..."]
        elif self.entered_wounds_text == []:
            wound_numbers = []
        else: 
            wound_numbers = ["Удалить рану " + i.strip()[:2] + "..." for i in  self.entered_wounds_text]
        #wound_numbers = [i[:2] + "" for i in  self.entered_wounds_text]
        menu_type_wound = QMenu(self)
        self.create_menu(wound_numbers, menu_type_wound)
        
        pushbut.setMenu(menu_type_wound)
        menu_type_wound.triggered.connect(self.editing_action)
        menu_type_wound.setStyleSheet('''
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
        text_updated_list = self.lab_wounds.text().split(".")[:-1]
        text_updated_list.pop(number)
        self.soft_tissue_checked_zones["wound"].pop(number)
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
        self.lab_wounds.setText(text_updated)
        self.entered_wounds_text = self.lab_wounds.text().split(".")[:-1]
        self.update_editing_menu (self.wound_edit_button)

        self.scroll.takeWidget()
        self.picture = Winform(self.file_name, soft_tissue_zones=self.soft_tissue_checked_zones)
        self.picture.update()
        self.scroll.setWidget(self.picture)


    def form_action(self, action):
        text = action.text()
        self.form_menu_button.setText(text)
        text = "форма %s, " %(text.lower())
        self.wound_form_text = text
        self.forming_wound_description()

    def zone_detailes_action(self, action):
        text = action.text()
        self.zone_detailes_menu_button.setText(text)
        text = "в %sм отделе " %(text)
        self.zone_detailes_text = text
        self.forming_wound_description()

    def margin_action(self, action):
        text = action.text()
        self.margin_menu_button.setText(text)
        text = "края %s, " %(text.lower())
        self.wound_margin_text = text
        self.forming_wound_description()

    def type_action(self, action):
        text = action.text()
        self.type_menu_button.setText(text)
        if text != "Язва":
            text = "%s рана " %(text)
        else:
            text = "Язва "
        self.wound_type_text = text
        self.forming_wound_description()

    def bottom_action(self, action):
        text = action.text()
        self.bottom_menu_button.setText(text)
        text = "дно раны - %s, " %(text.lower())
        self.wound_bottom_text = text
        self.forming_wound_description()

    def excretion_action(self, action):
        text = action.text()
        self.excretion_menu_button.setText(text)
        if text == "Нет":
            text = "отделяемого нет, "
        else:
            text = "отделяемое %s, " %(text.lower())
        self.wound_excretion_text = text
        self.forming_wound_description()

    def channel_action(self, action):
        text = action.text()
        self.channel_menu_button.setText(text)
        if text == "Нет":
            text = ""
        else:
            text = "раневой канал %s. " %(text.lower())

        self.wound_channel_text = text
        self.forming_wound_description()



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
                    

                self.wound_zone = "%s, " %(line_prepared)
                

                # adding every checked zone to existing number
                print(self.picture.get_checked_zones())
                #if len(self.picture.get_checked_zones())>1:
                #    self.soft_tissue_checked_zones["wound"][-1] = self.picture.get_checked_zones()[:]
                #    self.zone_detailes_text = ""
                #    self.zone_detailes_menu_button.setText("")
                #else:
                #    self.soft_tissue_checked_zones["wound"].append(self.picture.get_checked_zones()[0])
                
                #print(self.soft_tissue_checked_zones)
                
                self.forming_wound_description()

                if len(self.picture.get_checked_zones()) >= 1:
                    
                    #screen = QApplication.primaryScreen()
                    #self.screenshot = screen.grabWindow(self.picture.winId())
                    #self.screenshot = QPixmap(self.screenshot)
                    #print(self.screenshot)

                    self.waiting_label = QLabel()
                    self.waiting_label.setStyleSheet('''background: rgb(250,128,114); 
                                                    font: 22pt/24pt sans-serif;
                                                    text-align: center;''')

                    self.text_waiting = "Зона: %s.\nВведите параметры раны " %(str(self.picture.get_checked_zones()[0]))
                    
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
                #self.soft_tissue_checked_zones["wound"] = self.soft_tissue_checked_zones["wound"][:-1]
                self.wound_zone = ""
                self.forming_wound_description()
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
            
    def add_formed_wound(self, event=0):
        if (self.wound_size_text!="" and self.form_menu_button.text() !="" and
                self.margin_menu_button.text()!="" and
                self.type_menu_button.text()!="" and
                self.bottom_menu_button.text()!="" and
                self.excretion_menu_button.text()!="" and
                self.channel_menu_button.text()!="" and self.picture.get_checked_zones()!=[]):

            text = self.lab_wounds.text()
            
            if text:
                text = text[0:-2] + ". "

                self.lab_wounds.setText(text + str(len(self.entered_wounds_text) +1)+ ") " + (self.inner_chosen_zones.text()[0:-2] + ". "))
                self.entered_wounds_text = self.lab_wounds.text().split(".")[:-1]
                
                self.update_editing_menu (self.wound_edit_button)


            else:
                self.lab_wounds.setText("1) " + self.inner_chosen_zones.text()[0:-2] + ". ")
                self.entered_wounds_text = [self.lab_wounds.text().split(".")[:-1]]
                self.update_editing_menu (self.wound_edit_button)


            self.soft_tissue_checked_zones["wound"].append(self.picture.get_checked_zones()[:])

            #print(self.entered_wounds_text)
            self.wound_zone = ""
            self.wound_size_text = ""
            self.wound_size_lenght.setText("")
            self.wound_size_width.setText("")
            self.wound_size_depth.setText("")

            self.zone_detailes_menu_button.setText("")
            self.zone_detailes_menu_button.color = "white"
            self.form_menu_button.setText("")
            self.margin_menu_button.setText("")
            self.type_menu_button.setText("")
            self.bottom_menu_button.setText("")
            self.excretion_menu_button.setText("")
            self.channel_menu_button.setText("")
            self.zone_detailes_text = ""
            self.wound_type_text = ""
            self.wound_channel_text = ""
            self.wound_form_text = ""
            self.wound_margin_text = ""
            self.wound_bottom_text = ""
            self.wound_excretion_text = ""

            self.inner_chosen_zones.setText("")

            self.scroll.takeWidget()
            self.picture = Winform(self.file_name, soft_tissue_zones=self.soft_tissue_checked_zones)
            self.picture.update()
            self.scroll.setWidget(self.picture)
            return 1
        
        else:
            print(event)
            msg = QMessageBox()
            msg.setWindowTitle("Информация")
            msg.setText("Не все параметры раны введены!!!")
            msg.setIcon(QMessageBox.Information)
            msg.exec_()
            return 0



    def add_size(self):
        l = self.wound_size_lenght.text()
        w = self.wound_size_width.text()
        d = self.wound_size_depth.text()
        l_com ="в см, Д"
        w_com = ",Ш"
        d_com = ",Г"
        if l =="": l_com = ""
        if w =="": 
            w_com = ""
        else:
                w = "x"+w
        if d =="":
            d_com = ""
        else:
            d= "x"+d

        self.wound_size_text = "размерами: %s%s%s (%s%s%s), " % (l, w,d, l_com, w_com,d_com)
        self.forming_wound_description()


        

    def forming_wound_description(self):
        if len(self.picture.get_checked_zones()) >1:
            self.zone_detailes_menu_button.color = "#FF0700"
            self.zone_detailes_text = ""
            self.zone_detailes_menu_button.setText("")
        else:
            self.zone_detailes_menu_button.color = "white"
            
        self.inner_chosen_zones.setText(self.wound_type_text + self.zone_detailes_text + self.wound_zone + self.wound_size_text + self.wound_form_text + 
                                        self.wound_margin_text + self.wound_bottom_text + self.wound_excretion_text + 
                                        self.wound_channel_text)


    def picture_clear(self):
        #self.zone_detailes_menu_button.color = "white"
        self.scroll.takeWidget()
        self.picture = Winform(self.file_name, soft_tissue_zones=self.soft_tissue_checked_zones)
        self.picture.update()
        self.scroll.setWidget(self.picture)
        self.forming_wound_description()

    def get_wound_text(self):

        text = self.lab_wounds.text()
        if text != "":
            text_new =""
            for item in text.split(".")[:-1]:
                text_new += item[item.find(")")+1:].strip().capitalize() + ". "
            print("text_new=", text_new)
            return text_new
        else:
            return ""

    def get_wound_zones(self):
        return self.soft_tissue_checked_zones["wound"]


    def closeEvent(self, event):
        if self.inner_chosen_zones.text() != "":
            msg = QMessageBox()
            msg.setWindowTitle("Информация")
            msg.setText("Сохранить невведенное описание раны")
            msg.setIcon(QMessageBox.Information)
            yes =  PushButton("Yes")
            no=  PushButton("No")
            cancel=  PushButton("Cancel")
            msg.addButton(yes, QMessageBox.AcceptRole)
            msg.addButton(no, QMessageBox.RejectRole)
            msg.addButton(cancel, QMessageBox.DestructiveRole)
            ret = msg.exec_()
            
            if ret == 0:
                if self.add_formed_wound() == 1:
                    self.wound_send_info.emit()
                    event.accept()
                else:
                    event.ignore()
                    print("SMTH is broken")

            elif ret == 1:
                self.wound_send_info.emit()
                event.accept()

            elif ret == 2:
                event.ignore()
            
        else:
            self.wound_send_info.emit()
            event.accept()



if __name__ == "__main__":
    app = QApplication(sys.argv)
    
    form = EdemaWindow()
    form.show()
    sys.exit(app.exec_())