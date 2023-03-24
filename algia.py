import sys
import pickle
import time
from PyQt5.QtCore import pyqtSignal, QRect, QVariantAnimation, QAbstractAnimation
from PyQt5.QtGui import QPixmap, QPainter, QColor, QFont, QCursor
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import (QApplication, QWidget, QScrollArea, QHBoxLayout, QVBoxLayout, QMenu, 
                            QAction, QDesktopWidget, QPushButton, QDialog, QLabel, QGridLayout, 
                            QGroupBox, QMessageBox)

#from modules.zone_detecting.zone_choosing import ScrollOnPicture
from zone_choosing import ScrollOnPicture, Winform

class PushButton(QPushButton):
    def __init__(self, parent=None):
        super().__init__(parent)
        self._animation = QVariantAnimation(
            startValue=QColor("#CD5C5C"),
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
            border: 2px solid #CD5C5C;
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




class AlgiaWindow(QWidget):
    algia_send_info = pyqtSignal()
    def __init__(self, entered_algias_text, soft_tissue_zones, **kwargs):
        super().__init__( **kwargs)
        
        self.entered_algias_text = entered_algias_text
        self.algia_checked_zones = soft_tissue_zones

        self.initUI()

    def initUI(self):
        
        self.file_name = "front_clear.bmp"
        self.picture = Winform(self.file_name, soft_tissue_zones=self.algia_checked_zones)
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

        self.zone_detailes_text = ""
        self.algia_type_text = ""
        self.algia_zone = ""
        

        
        

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
        self.close_btn = PushButton("Закончить описание")
        self.close_btn.clicked.connect(self.close)
        self.vbox.addWidget(self.close_btn)

        self.button_clear = PushButton("Очистить")
        self.button_clear.clicked.connect(self.picture_clear)
        self.vbox.addWidget(self.button_clear)
        


        self.algia = QVBoxLayout()

        self.entered_algias = QGroupBox("Введенные зоны боли")
        
        self.lab_algias = QLabel()
        self.lab_algias.setWordWrap(True)
        
        if self.entered_algias_text != "":
            #self.entered_algias_text = self.entered_algias_text[:-1]

            text_to_add = ""
            counter = 1
            for item in self.entered_algias_text:
                if item[-1]==".":
                    item = item[:-1]
                text_to_add += str(counter) + ") " + item.lower() + ", "
                counter+=1
            self.entered_algias_text = text_to_add.split(",")[:-1]
            self.lab_algias.setText(text_to_add)

        self.algia.addWidget(self.lab_algias)
        self.algias_edit_button = QPushButton("Редактировать")
        
        self.update_editing_menu(self.algias_edit_button)

        
        
        self.algias_edit_button.setStyleSheet('''
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
        self.algia.addWidget(self.algias_edit_button)





        self.entered_algias.setLayout(self.algia)

        self.entered_algias.setStyleSheet('''

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

        self.algia_text_forming = QVBoxLayout()
        #self.wound_zone = ""
        
        self.chosen_zones = QGroupBox("Текущее описание зоны боли")
        self.inner_chosen_zones = QLabel()
        self.inner_chosen_zones.setWordWrap(True)
        self.algia_text_forming.addWidget(self.inner_chosen_zones)
        self.button_new_algia = PushButton("Добавить описание зоны боли")
        self.button_new_algia.clicked.connect(self.add_formed_algia)
        self.algia_text_forming.addWidget(self.button_new_algia)
        self.chosen_zones.setLayout(self.algia_text_forming)
        
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
        self.create_menu(zone_detailes, menu_zone_detailes)
        
        self.zone_detailes_menu_button = QPushButton()
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



        self.algia_type = QGroupBox("Выраженность боли")
        self.algia_type.setStyleSheet('''
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
        self.algia_type_box = QVBoxLayout()
        self.algia_type_text = ""
        algia_types = [ "Легкая", "Умеренная", "Выраженная", "Резко выраженная"]
        menu_type = QMenu(self)
        self.create_menu(algia_types, menu_type)
        
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
        
        self.algia_type_box.addWidget(self.type_menu_button)
        self.algia_type.setLayout(self.algia_type_box)

        self.vbox_right = QVBoxLayout()
        self.vbox_right.addWidget(self.entered_algias)
        self.vbox_right.addWidget(self.chosen_zones)
        self.vbox_right.addWidget(self.zone_detailes)
        self.vbox_right.addWidget(self.algia_type)
        
        self.grid = QGridLayout(self)
        self.grid.addLayout(self.vbox,0 , 0)
        self.grid.addLayout(self.vbox_right, 0 , 1)
        self.grid.setColumnMinimumWidth(0, self.picture.width()+40)
        self.grid.setColumnStretch(1, 0.5)
        
        self.setWindowTitle ("Болезненность")
        self.show()

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

    def type_action(self, action):
        text = action.text()
        self.type_menu_button.setText(text)
        text = "%s болезненность " %(text)
        self.algia_type_text = text
        self.forming_algia_description()

    
    def zone_detailes_action(self, action):
        text = action.text()
        self.zone_detailes_menu_button.setText(text)
        text = "в %sм отделе " %(text)
        self.zone_detailes_text = text
        self.forming_algia_description()



    
    def update_editing_menu(self, pushbut):

        if len(self.entered_algias_text) ==1:
            algia_numbers = ["Удалить зону 1)..."]
        elif self.entered_algias_text == []:
            algia_numbers = []
        else: 
            algia_numbers = ["Удалить зону " + i.strip()[:2] + "..." for i in  self.entered_algias_text]
        #wound_numbers = [i[:2] + "" for i in  self.entered_wounds_text]
        menu_type_algias = QMenu(self)
        self.create_menu(algia_numbers, menu_type_algias)
        
        pushbut.setMenu(menu_type_algias)
        menu_type_algias.triggered.connect(self.editing_action)
        menu_type_algias.setStyleSheet('''
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
        text_updated_list = self.lab_algias.text().split(",")[:-1]
        text_updated_list.pop(number)
        self.algia_checked_zones["algia"].pop(number)
        text_new =""
        print(len(text_updated_list), text_updated_list)
        if len(text_updated_list)>1:
            for item in text_updated_list:
                text_new += item[item.find(")")+1:].strip() + ", "
            text_updated = ""
            number = 1
            for item_up in text_new.split(",")[:-1]:
                text_updated += str(number) + ") " + item_up.strip() + ", "
                number+=1
        
        elif len(text_updated_list)==1:
            text_updated = "1) " + text_updated_list[0][text_updated_list[0].find(")")+1:].strip() + ", "

        else:
            text_updated = ""
        self.lab_algias.setText(text_updated)
        self.entered_algias_text = self.lab_algias.text().split(",")[:-1]
        self.update_editing_menu (self.algias_edit_button)
        print("self.algia_checked_zones=",self.algia_checked_zones)
        print("self.file_name=",self.file_name)
        self.scroll.takeWidget()
        self.picture = Winform(self.file_name, soft_tissue_zones=self.algia_checked_zones)
        self.picture.update()
        self.scroll.setWidget(self.picture)
        

    def mouseReleaseEvent(self, event):
        posMouse =  event.pos()
        
        #try:



        if self.picture and self.scroll.rect().contains(posMouse) and self.picture.get_checked_zones():
            #self.picture.get_checked_zones() !=[]
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


            self.algia_zone = "%s, " %(line_prepared)
            
            self.algia_checked_zones["algia"].append(self.picture.get_checked_zones()[0])  # adding every checked zone to existing number

            self.forming_algia_description()
            
            if len(self.picture.get_checked_zones()) >= 1:
                
                #screen = QApplication.primaryScreen()
                #self.screenshot = screen.grabWindow(self.picture.winId())
                #self.screenshot = QPixmap(self.screenshot)
                #print(self.screenshot)
                time.sleep(0.33)

                self.waiting_label = QLabel()
                

                self.waiting_label.setStyleSheet('''background: rgb(250,128,114); 
                                                font: 22pt/24pt sans-serif;
                                                text-align: center;''')

                self.text_waiting = "Зона: %s.\nВведите характер боли" %(str(self.picture.get_checked_zones()[0]))
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
                #msg.setText("Введите характер боли")
                #msg.setIcon(QMessageBox.Information)
                #msg.exec_()

            
            
                self.update()
        else:
            print("winform doesnot exist")
            print(self.picture) 
            print(self.scroll.rect().contains(posMouse)) 
            print(self.picture.get_checked_zones()) 
        #except RuntimeError:
        #   print(some ERROR)

              
    def picture_view(self):
        if self.sender().text() == "Вид спереди":
            self.scroll.takeWidget()
            self.file_name = "front_clear.bmp"
            self.picture = Winform(self.file_name, soft_tissue_zones=self.algia_checked_zones)
            self.picture.update()
            self.scroll.setWidget(self.picture)
            self.algia_zones = ""
            self.algia_type_text = ""
            self.inner_chosen_zones.setText("")
            self.type_menu_button.setText("")
            sizeObject = QDesktopWidget().screenGeometry(-1)
            self.resize(self.picture.width(), (sizeObject.height()-90))
            self.update()
            
        else:
            self.scroll.takeWidget()
            self.file_name = "back_clear.bmp"
            self.picture = Winform(self.file_name, soft_tissue_zones=self.algia_checked_zones)
            self.picture.update()
            self.scroll.setWidget(self.picture)
            self.algia_zones = ""
            self.algia_type_text = ""
            self.inner_chosen_zones.setText("")
            self.type_menu_button.setText("")
            sizeObject = QDesktopWidget().screenGeometry(-1)
            self.resize(self.picture.width(), (sizeObject.height()-90))
            self.update()
            

    def add_formed_algia(self):
        if self.inner_chosen_zones.text() != "" and self.type_menu_button!="":

            text = self.lab_algias.text()
            if text:
                text = text[0:-2] + ", "

                self.lab_algias.setText(text + str(len(self.entered_algias_text) +1)+ ") " + (self.inner_chosen_zones.text()[0:-2].lower() + ", "))
                self.entered_algias_text = self.lab_algias.text().split(",")[:-1]
                
                self.update_editing_menu (self.algias_edit_button)

            else:
                self.lab_algias.setText("1) " + self.inner_chosen_zones.text()[0:-2].lower() + ", ")
                self.entered_algias_text = [self.lab_algias.text().split(",")[:-1]]
                self.update_editing_menu (self.algias_edit_button)


            self.inner_chosen_zones.setText("")
            self.algia_zone = ""

            self.zone_detailes_menu_button.setText("")
            self.zone_detailes_text=""

            self.type_menu_button.setText("")

            self.algia_type_text = ""
            self.scroll.takeWidget()
            self.picture = Winform(self.file_name, soft_tissue_zones=self.algia_checked_zones)

            self.picture.update()
            self.scroll.setWidget(self.picture)


    def forming_algia_description(self):
        self.inner_chosen_zones.setText(self.algia_type_text.lower() + self.zone_detailes_text + self.algia_zone)


    def picture_clear(self):

        if self.picture.get_checked_zones()[0] !=[]:
            self.algia_checked_zones["algia"].pop(-1)

        self.scroll.takeWidget()
        self.picture = Winform(self.file_name, soft_tissue_zones=self.algia_checked_zones)
        self.picture.update()
        self.scroll.setWidget(self.picture)
        
        sizeObject = QDesktopWidget().screenGeometry(-1)
        self.resize(self.picture.width(), (sizeObject.height()-90))
        self.algia_type_text = ""
        self.algia_zone = ""
        self.zone_detailes_text = ""
        self.zone_detailes_menu_button.setText("")

        self.inner_chosen_zones.setText("")
        self.type_menu_button.setText("")
        self.update()
        
    def get_algia_text(self):
        
        text = self.lab_algias.text()
        if text != "":
            text_new =""
            for item in text.split(",")[:-1]:
                text_new += item[item.find(")")+1:].strip() + ", "
            print("text_new=", text_new)
            return text_new[:-2]+"."
        else:
            return ""

    def get_algia_zones(self):
        return self.algia_checked_zones["algia"]


    def closeEvent(self, event):
        if self.inner_chosen_zones.text() != "":
            reply = QMessageBox.question(self, "Внимание!",
                                        "Имеются не добавленные зоны болезненности,\nдобавить их в общее описание?",
                                        QMessageBox.Yes|QMessageBox.No|QMessageBox.Cancel, QMessageBox.Cancel)
            if reply == QMessageBox.Yes:
                self.add_formed_algia()
                self.algia_send_info.emit()
                event.accept()


            elif reply == QMessageBox.Cancel:
                event.ignore()

            elif reply==QMessageBox.No:
                if self.picture.get_checked_zones() !=[] and self.algia_checked_zones["algia"] !=[]:
                    self.algia_checked_zones["algia"] = self.algia_checked_zones["algia"][:-1]

                self.algia_send_info.emit()
                event.accept()


        else:

            self.algia_send_info.emit()
            event.accept()


        #self.algia_send_info.emit()
        #event.accept()
        #self.close()
        #self.setParent(None)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    
    form = EdemaWindow()
    form.show()
    sys.exit(app.exec_())