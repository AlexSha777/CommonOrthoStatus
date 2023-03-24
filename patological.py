import sys
import pickle
from PyQt5.QtCore import pyqtSignal, QRect, QVariantAnimation, QAbstractAnimation
from PyQt5.QtGui import QPixmap, QPainter, QColor, QFont, QCursor, QIntValidator
from PyQt5.QtCore import Qt
import time

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





class PatologicalWindow(QWidget):
    patolog_send_info = pyqtSignal()
    def __init__(self, soft_tissue_zones, entered_info=None,  **kwargs):
        super().__init__( **kwargs)
        self.soft_tissue_checked_zones = soft_tissue_zones
        if entered_info != None and entered_info != "":
            self.entered_info_text = entered_info[:]
        else:
            self.entered_info_text = []
        self.initUI()

    def initUI(self):
        self.file_name = "front_clear.bmp"
        self.picture = Winform(self.file_name, soft_tissue_zones=self.soft_tissue_checked_zones)
        self.scroll = QScrollArea()
        self.scroll.setWidget(self.picture)
        

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

        
        self.tumors = QVBoxLayout()

        self.lab_entered_tumors = QLabel("Введенные образования")
        self.entered_tumors = QGroupBox(self.lab_entered_tumors.text())
        
        self.lab_tumors = QLabel()
        self.lab_tumors.setWordWrap(True)
        

        self.entered_info_text = self.entered_info_text[:-1]
        text_to_add = ""
        counter = 1
        for item in self.entered_info_text:
            text_to_add += str(counter) + ") " + item + ". "
            counter+=1
        self.lab_tumors.setText(text_to_add)
        self.entered_info_text = text_to_add.split(".")[:-1]
        print("self.entered_info_text=", self.entered_info_text)



        self.but_edit = QHBoxLayout()
        self.delete_tumors = PushButton("Очистить")
        self.delete_tumors.clicked.connect(lambda: self.lab_tumors.setText(""))
        
        self.tumor_edit_button = QPushButton("Редактировать")
        
        self.update_editing_menu(self.tumor_edit_button)

        
        
        self.tumor_edit_button.setStyleSheet('''
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
        self.but_edit.addWidget(self.tumor_edit_button)
        self.but_edit.addWidget(self.delete_tumors) 


        self.tumors.addWidget(self.lab_tumors)
        self.tumors.addLayout(self.but_edit)
        self.entered_tumors.setLayout(self.tumors)

        self.entered_tumors.setStyleSheet('''

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




        self.tumor_text_forming = QVBoxLayout()
        self.tumor_zone = ""
        self.lab_chosen_zones = QLabel("Текущее описание опухоли")
        self.chosen_zones = QGroupBox(self.lab_chosen_zones.text())
        self.inner_chosen_zones = QLabel()
        self.inner_chosen_zones.setWordWrap(True)
        self.tumor_text_forming.addWidget(self.inner_chosen_zones)
        self.button_new_tumor = PushButton("Ввести опухоль")
        self.button_new_tumor.clicked.connect(self.add_formed_tumor)
        self.tumor_text_forming.addWidget(self.button_new_tumor)
        self.chosen_zones.setLayout(self.tumor_text_forming)
        
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
 

        self.label_tumor_type = QLabel("Форма образования")
        self.tumor_type = QGroupBox(self.label_tumor_type.text())
        self.tumor_type.setStyleSheet('''
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
        self.tumor_type_box = QVBoxLayout()
        self.tumor_type_text = ""
        tumor_types = [ "Округлая", "Овоидная", "Вытянутая", "Без четких границ"]
        menu_type = QMenu(self)
        self.create_menu(tumor_types, menu_type)
        
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
        
        self.tumor_type_box.addWidget(self.type_menu_button)
        self.tumor_type.setLayout(self.tumor_type_box)

        self.label_tumor_size = QLabel("Размеры образования")
        self.tumor_size = QGroupBox(self.label_tumor_size.text())
        self.tumor_size.setStyleSheet('''
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
        self.tumor_size_box = QVBoxLayout()
        self.tumor_size_text = ""
        self.label_lenght = QLabel("Длина, см")
        self.tumor_size_lenght = QLineEdit(self.label_lenght)
        self.tumor_size_lenght.textChanged.connect(self.add_size)
        pIntValidator = QIntValidator(self)
        pIntValidator.setRange(1, 99)
        self.tumor_size_lenght.setValidator(pIntValidator)
        self.tumor_size_lenght.setPlaceholderText("1")
        self.tumor_size_lenght.setStyleSheet('border: 2px solid grey; border-radius: 5px;')
        self.label_width = QLabel("Ширина, см")
        self.tumor_size_width = QLineEdit(self.label_width)
        self.tumor_size_width.textChanged.connect(self.add_size)
        self.tumor_size_width.setValidator(pIntValidator)
        self.tumor_size_width.setPlaceholderText("1")
        self.tumor_size_width.setStyleSheet('border: 2px solid grey; border-radius: 5px;')
        self.label_depth = QLabel("Толщина, см")
        self.tumor_size_depth = QLineEdit(self.label_depth)
        self.tumor_size_depth.textChanged.connect(self.add_size)
        self.tumor_size_depth.setValidator(pIntValidator)
        self.tumor_size_depth.setPlaceholderText("1")
        self.tumor_size_depth.setStyleSheet('border: 2px solid grey; border-radius: 5px;')
        self.tumor_size_box.addWidget(self.label_lenght)
        self.tumor_size_box.addWidget(self.tumor_size_lenght)
        self.tumor_size_box.addWidget(self.label_width)
        self.tumor_size_box.addWidget(self.tumor_size_width)
        self.tumor_size_box.addWidget(self.label_depth)
        self.tumor_size_box.addWidget(self.tumor_size_depth)

        #self.add_tumor_size = PushButton("Добавить")
        #self.add_tumor_size.clicked.connect(self.add_size)
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
        #self.tumor_size_box.addWidget(self.add_tumor_size)

        self.tumor_size.setLayout(self.tumor_size_box)




        self.tumor_consistency = QGroupBox("Консистенция")
        self.tumor_consistency.setStyleSheet('''
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
        self.tumor_consistency_box = QVBoxLayout()
        self.tumor_consistency_text = ""
        
        d = ["Мягкоэластичная","Тугоэластичная","Твердая","Деревянистая"]
        menu_consistency = QMenu(self)
        self.create_menu(d, menu_consistency)
        self.consistency_menu_button = QPushButton()
        self.consistency_menu_button.setMenu(menu_consistency)
        menu_consistency.triggered.connect(self.consistency_action)
        self.consistency_menu_button.setStyleSheet('''
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
        menu_consistency.setStyleSheet('''
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

        self.tumor_consistency_box.addWidget(self.consistency_menu_button)
        self.tumor_consistency.setLayout(self.tumor_consistency_box)

        self.tumor_moveable = QGroupBox("Подвижность образования")
        self.tumor_moveable.setStyleSheet('''
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
        self.tumor_moveable_box = QVBoxLayout()
        self.tumor_moveable_text = ""
        menu_moveable = QMenu(self)
        
        moveableness = [
        {"Самостоятельная":["Самостоятельно неподвижная","Смещаемая при сокращении мышцы",
                        "Смещаемая при глотании", "Смещаемая при перемене положения тела"]},
        {"Спровоцированная":["Неспаянная с окужающими тканями","Спаянная с окружающими тканями"]},
        ]
        self.create_menu(moveableness, menu_moveable)
        self.moveable_menu_button = QPushButton()
        self.moveable_menu_button.setMenu(menu_moveable)
        menu_moveable.triggered.connect(self.moveable_action)

        self.moveable_menu_button.setStyleSheet('''
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
        menu_moveable.setStyleSheet('''
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

        self.tumor_moveable_box.addWidget(self.moveable_menu_button)
        self.tumor_moveable.setLayout(self.tumor_moveable_box)
        
        
        self.tumor_aching = QGroupBox("Болезненность при пальпации")
        self.tumor_aching.setStyleSheet('''
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

        menu_aching = QMenu(self)
        aching = ["Болезненное", "Безболезненное"]
        for z in aching:
            action = menu_aching.addAction(z)
            action.setIconVisibleInMenu(False)
        
        self.aching_menu_button = QPushButton()
        self.aching_menu_button.setMenu(menu_aching)
        menu_aching.triggered.connect(self.aching_action)

        self.aching_menu_button.setStyleSheet('''
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
        menu_aching.setStyleSheet('''
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
        self.tumor_aching_box = QVBoxLayout()
        self.tumor_aching_box.addWidget(self.aching_menu_button)
        self.tumor_aching_text = ""
        self.tumor_aching.setLayout(self.tumor_aching_box)

        self.right_scroll = QScrollArea()
        self.vbox_right = QVBoxLayout()
        self.vbox_right.addWidget(self.entered_tumors)
        self.vbox_right.addWidget(self.chosen_zones)
        self.vbox_right.addWidget(self.tumor_type)
        self.vbox_right.addWidget(self.tumor_size)
        self.vbox_right.addWidget(self.tumor_consistency)
        self.vbox_right.addWidget(self.tumor_moveable)
        self.vbox_right.addWidget(self.tumor_aching)

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
        self.grid.setColumnMinimumWidth(1, (self.picture.width()+40)/3+30)
        self.grid.setColumnStretch(1, 0.5)
        
        
        self.setWindowTitle ("Патологические образования")
        self.show()
     
    def entered_info_process(self):
        self.entered_info_text = self.entered_info_text[:-1]
        text_to_add = ""
        counter = 1
        for item in self.entered_info_text:
            text_to_add += str(counter) + ") " + item + ". "
            counter+=1
        self.lab_tumors.setText(text_to_add)
        self.entered_info_text = text_to_add.split(".")[:-1]

        
        print(self.entered_info)

    def update_editing_menu(self, pushbut):

        if len(self.entered_info_text) ==1:
            patol_numbers = ["Удалить образование 1)..."]
        elif self.entered_info_text == []:
            patol_numbers = []
        else: 
            patol_numbers = ["Удалить образование " + i.strip()[:2] + "..." for i in  self.entered_info_text]
        #wound_numbers = [i[:2] + "" for i in  self.entered_wounds_text]
        menu_patol_number = QMenu(self)
        self.create_menu(patol_numbers, menu_patol_number)
        
        pushbut.setMenu(menu_patol_number)
        menu_patol_number.triggered.connect(self.editing_action)
        menu_patol_number.setStyleSheet('''
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
        text_updated_list = self.lab_tumors.text().split(".")[:-1]
        text_updated_list.pop(number)
        self.soft_tissue_checked_zones["tumor"].pop(number)
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
        self.lab_tumors.setText(text_updated)
        self.entered_info_text = self.lab_tumors.text().split(".")[:-1]
        self.update_editing_menu (self.tumor_edit_button)

        self.scroll.takeWidget()
        self.picture = Winform(self.file_name, soft_tissue_zones=self.soft_tissue_checked_zones)
        self.picture.update()
        self.scroll.setWidget(self.picture)



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

    def moveable_action(self, action):
        text = action.text()
        self.moveable_menu_button.setText(text)
        text = text.lower()[:-2] +"ое, " 
        self.tumor_moveable_text = text
        self.forming_tumor_description()


    def consistency_action(self, action):
        text = action.text()
        self.consistency_menu_button.setText(text)
        text = text[:-2].lower() + "ой консистенции, "
        #text = "края %s, " %(text[:].lower())
        self.tumor_consistency_text = text
        self.forming_tumor_description()

    def type_action(self, action):
        text = action.text()
        self.type_menu_button.setText(text)
        text = text.lower()
        text = text[:-2] + "ой формы, "
        #text = "%s " %(text)
        self.tumor_type_text = text
        self.forming_tumor_description()

    def aching_action(self, action):
        text = action.text()
        self.aching_menu_button.setText(text)
        text = "%s при пальпации, " %(text.lower())
        self.tumor_aching_text = text
        self.forming_tumor_description()

    def mouseReleaseEvent(self, event):
        posMouse =  event.pos()
        
        #try:



        if self.picture and self.scroll.rect().contains(posMouse) and self.picture.get_checked_zones() != []:
            print("Under Mouse")
            

            #print(self.picture.get_checked_zones())
            #print(len(self.picture.get_checked_zones()))
            line = str(self.picture.get_checked_zones()[0])
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
            line_prepared = ""

            k=1
            for word in line_format:
                line_prepared += word
                if k <len(line_format):
                    line_prepared += " "
                k+=1


            self.tumor_zone = "Патологическое образование %s, " %(line_prepared)
            self.forming_tumor_description()
            
            if len(self.picture.get_checked_zones()) >= 1:
                
                #screen = QApplication.primaryScreen()
                #self.screenshot = screen.grabWindow(self.picture.winId())
                #self.screenshot = QPixmap(self.screenshot)
                #print(self.screenshot)
                time.sleep(0.5)
                self.waiting_label = QLabel()
                self.waiting_label.setWordWrap(True)
                

                self.waiting_label.setStyleSheet('''background: rgb(250,128,114); 
                                                font: 22pt/24pt sans-serif;
                                                text-align: center;''')

                self.text_waiting = "Зона: %s.\nВведите параметры патологического образования" %(str(self.picture.get_checked_zones()[0]))
                self.waiting_label.setText(self.text_waiting)
                print("Paint event")
                self.scroll.setWidget(self.waiting_label)
                self.scroll.setAlignment(Qt.AlignCenter)
                



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
                #msg.setText("Введите параметры патологического образования")
                #msg.setIcon(QMessageBox.Information)
                #msg.exec_()

            
            
                self.update()
        else:
            print("winform doesnot exist")
        #except RuntimeError:
        #   print(some ERROR)

    def get_text(self):
        text = self.lab_tumors.text()
        if text != "":
            text_new =""
            for item in text.split(".")[:-1]:
                text_new += item[item.find(")")+1:].strip().capitalize() + ". "
            print("text_new=", text_new)
            return text_new
        else:
            return ""


    def get_patology_zones(self):
        return self.soft_tissue_checked_zones["tumor"]


    def picture_view(self):
        if self.sender().text() == "Вид спереди":
            self.scroll.takeWidget()
            self.picture = Winform("front_clear.bmp")
            self.picture.update()
            self.scroll.setWidget(self.picture)
            #self.chosen_zones.setText("")
            #self.chosen_zones.update()
            sizeObject = QDesktopWidget().screenGeometry(-1)
            self.resize(self.picture.width(), (sizeObject.height()-90))
            self.update()
            
        else:
            self.scroll.takeWidget()
            self.picture = Winform("back_clear.bmp")
            self.picture.update()
            self.scroll.setWidget(self.picture)
            #self.chosen_zones.setText("")
            #self.chosen_zones.update()
            sizeObject = QDesktopWidget().screenGeometry(-1)
            self.resize(self.picture.width(), (sizeObject.height()-90))
            self.update()
        
    def add_formed_tumor(self):
    
        if (self.tumor_zone!="" and self.tumor_size_text!="" and self.tumor_type_text != "" and 
                self.tumor_consistency_text != "" and self.tumor_moveable_text != "" and self.tumor_aching_text != ""):
            text = self.lab_tumors.text()
            if text!="":
                text = text[0:-2] + ". "
                print("len(self.entered_info_text)=", len(self.entered_info_text))
                print("self.entered_info_text=", self.entered_info_text)
                self.lab_tumors.setText(text + str(len(self.entered_info_text) +1)+ ") " + (self.inner_chosen_zones.text()[0:-2] + ". "))
                self.entered_info_text = self.lab_tumors.text().split(".")[:-1]
                
                self.update_editing_menu (self.tumor_edit_button)


            else:
                self.lab_tumors.setText("1) " + self.inner_chosen_zones.text()[0:-2] + ". ")
                self.entered_info_text = [self.lab_tumors.text().split(".")[:-1]]
                self.update_editing_menu (self.tumor_edit_button)
                print("self.entered_info_text=", self.entered_info_text)

            self.soft_tissue_checked_zones["tumor"].append(self.picture.get_checked_zones()[:])

            
            self.tumor_size_lenght.setText("")
            self.tumor_size_width.setText("")
            self.tumor_size_depth.setText("")

            self.consistency_menu_button.setText("")
            self.moveable_menu_button.setText("")
            self.type_menu_button.setText("")
            self.aching_menu_button.setText("")
            
            
            self.inner_chosen_zones.setText("")
            self.tumor_zone = ""
            self.tumor_size_text = ""
            self.tumor_type_text = ""
            self.tumor_consistency_text = ""
            self.tumor_moveable_text = ""
            self.tumor_aching_text = ""



            self.picture = Winform(self.file_name, soft_tissue_zones=self.soft_tissue_checked_zones)
            self.picture.update()
            self.scroll.setWidget(self.picture)
            return 1



        else:
            msg = QMessageBox()
            msg.setWindowTitle("Информация")
            msg.setText("Не введены все параметры патологического образования")
            msg.setIcon(QMessageBox.Information)
            msg.exec_()
            return 0





    def add_size(self):
        if self.tumor_size_lenght.text()!="" and self.tumor_size_width.text()!=""  and self.tumor_size_depth.text()=="":
            self.tumor_size_depth.setText("неопределима")
            self.tumor_size_text = "размерами: %sх%s (в см, Д,Ш), " % (self.tumor_size_lenght.text(), 
                                                                    self.tumor_size_width.text())
            self.forming_tumor_description()

        elif self.tumor_size_lenght!="" and self.tumor_size_width!=""  and self.tumor_size_depth.text()!="":
            self.tumor_size_text = "размерами: %sх%sх%s (в см, Д,Ш,Т), " % (self.tumor_size_lenght.text(), 
                                                                    self.tumor_size_width.text(),
                                                                    self.tumor_size_depth.text())
            self.forming_tumor_description()


        

    def forming_tumor_description(self):
        self.inner_chosen_zones.setText(self.tumor_zone + self.tumor_type_text + self.tumor_size_text + 
                                        self.tumor_consistency_text + self.tumor_moveable_text + self.tumor_aching_text)


    def picture_clear(self):
        self.picture = Winform(self.file_name, soft_tissue_zones=self.soft_tissue_checked_zones)
        self.inner_chosen_zones.setText("")
        self.picture.update()
        self.scroll.setWidget(self.picture)


    def closeEvent(self, event):
        if self.inner_chosen_zones.text() != "":
            msg = QMessageBox()
            msg.setWindowTitle("Информация")
            msg.setText("Сохранить невведенное описание патологические образования")
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
                    self.patolog_send_info.emit()
                    event.accept()
                else:
                    event.ignore()
                    print("SMTH is broken")

            elif ret == 1:
                self.patolog_send_info.emit()
                event.accept()

            elif ret == 2:
                event.ignore()
            
        else:
            self.patolog_send_info.emit()
            event.accept()



    

if __name__ == "__main__":
    app = QApplication(sys.argv)
    
    form = EdemaWindow()
    form.show()
    sys.exit(app.exec_())