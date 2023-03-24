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
from joints_wrist_foot import WristFootWindow

class PushButton(QPushButton):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.color_main = "white"

        self._animation = QVariantAnimation(
            startValue=QColor("#CD5C5C"),
            endValue=QColor(self.color_main),
            valueChanged=self._on_value_changed,
            duration=400,
        )
        self._update_stylesheet(QColor("white"), QColor("black"))
        self.setCursor(QCursor(Qt.PointingHandCursor))

    def setColor (self, color_new):
        self.color_main = color_new
        
        print(color_new)
        self._update_stylesheet(QColor(self.color_main),QColor("black"))

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
        if self.color_main == "white":
            self._animation.setDirection(QAbstractAnimation.Backward)
            self._animation.start()
            super().enterEvent(event)

    def leaveEvent(self, event):
        if self.color_main == "white":
            self._animation.setDirection(QAbstractAnimation.Forward)
            self._animation.start()
            super().leaveEvent(event)





class JointsWindow(QWidget):
    joints_send_info = pyqtSignal()
    def __init__(self, **kwargs):
        super().__init__( **kwargs)
        
        self.initUI()

    def initUI(self):
        self.degree_sign = u'\N{DEGREE SIGN}'
        
        self.wrist_text_right = ""
        self.wrist_text_left = ""

        self.lineEdits_right = []
        self.lineEdits_left = []
        self.lineEdits_up_center = []

        self.label_degree_up_center = []
        self.label_degree_left = []
        self.label_degree_right = []


        self.joints = ["Шейный Отдел Позвоночника", "Грудной Отдел Позвоночника", "Поясничный Отдел Позвоночника", 
                "Плечевой сустав", "Локтевой сустав", "Луче-локтевые суставы", "Лучезапястный сустав", "Кисть",
                "Тазобедренный сустав", "Коленный сустав", "Голеностопный сустав", "Стопа"]

        self.dict_joints = {
            "Шейный Отдел Позвоночника": {
                                         "flex": [40,0,40],
                                         "inclineRignt": [45,0,45],
                                         "rotRight": [70,0,70]
                                          },
            "Грудной Отдел Позвоночника": {"inclineAnt": [30,38]},
            "Поясничный Отдел Позвоночника": {"inclineAnt": [10,15]},
            "Плечевой сустав правый": {
                                "flex": [155,0,60],
                                "abdu": [155,0,25],
                                "rotExt": [45,0,90]
                                },
            "Локтевой сустав правый": {"flex": [150, 0, 0]},
            "Луче-локтевые суставы правые": {"rotSup": [90, 0, 90]},
            "Лучезапястный сустав правый": {"flex": [80, 0, 70]},
            "Кисть правая": 0,
            "Тазобедренный сустав правый": {
                                    "flex": [110,0,20],
                                    "abdu": [40,0,20],
                                    "rotExt": [40,0,30]
                                    },
            "Коленный сустав правый": {"flex": [140, 0, 0]},
            "Голеностопный сустав правый": {"flexPlant": [45,0,20]},
            "Стопа правая": 0,
            "Плечевой сустав левый": {
                                "flex": [155,0,60],
                                "abdu": [155,0,25],
                                "rotExt": [45,0,90]
                                },
            "Локтевой сустав левый": {"flex": [150, 0, 0]},
            "Луче-локтевые суставы левый": {"rotSup": [90, 0, 90]},
            "Лучезапястный сустав левый": {"flex": [80, 0, 70]},
            "Кисть левая": 0,
            "Тазобедренный сустав левый": {
                                    "flex": [110,0,20],
                                    "abdu": [40,0,20],
                                    "rotExt": [40,0,30]
                                    },
            "Коленный сустав левый": {"flex": [140, 0, 0]},
            "Голеностопный сустав левый": {"flexPlant": [45,0,20]},
            "Стопа левая": 0,
        }

        self.list_normal_move = [
            [80,90,140],
            [8],
            [5],
            [215,180,135],
            [150],
            [180],
            [150],
            [130, 60, 70],
            [140],
            [65],
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

        self.contracture_right = [
            ["","",""],
            [""],
            [""],
            [""],
            ["","",""],
            [""],
            [""],
        ]
        self.text_right = [
            ["плечевом суставе справа"],
            ["локтевом суставе справа"],
            ["луче-локтевых суставах справа"],
            ["лучезапястном суставе справа"],
            ["тазобедренном суставе справа"],
            ["коленном суставе справа"],
            ["голеностопном суставе справа"],
        ]

        self.contracture_left = [
            ["","",""],
            [""],
            [""],
            [""],
            ["","",""],
            [""],
            [""],
        ]
        self.text_left = [
            ["плечевом суставе слева"],
            ["локтевом суставе слева"],
            ["луче-локтевых суставах слева"],
            ["лучезапястном суставе слева"],
            ["тазобедренном суставе слева"],
            ["коленном суставе слева"],
            ["голеностопном суставе слева"],
        ]

        self.grid = QGridLayout(self)
       
        title = ["Справа", "Слева"]
        column = 1
        for k in title:
            label = QLabel()
            label.setStyleSheet("""
                QLabel {
                    background-color: #CD5C5C; 
                    color: white; 
                    border-style: outset;
                    border-width: 2px;
                    border-radius: 10px;
                    border-color: beige;
                    font: bold 14px;
                    padding: 2px;
                }
                """)

            label.setText(k)
            self.grid.addWidget(label,3 , column, Qt.AlignHCenter)
            column +=1

        row = 0
        for item in self.joints:
            label = QLabel()
            label.setStyleSheet('''QLabel {
                background-color: #FA8072; 
                color: black; 
                border-style: groove;
                border-width: 2px;
                border-radius: 10px;
                border-color: beige;
                font: bold 14px;
                min-width: 10em;
                padding: 2px;
                }
            ''')
            label.setText(item)
            self.grid.addWidget(label,row ,0, Qt.AlignHCenter)
            if item == "Поясничный Отдел Позвоночника":
                row += 2
            else:
                row += 1
                
        
        row_number = 0
        for key, value in self.dict_joints.items():
            if value:
                
                dict_inner = []
                movements = QWidget()
                movements.setStyleSheet('''QWidget {
                                            border: 1px solid #FA8072;
                                            border-width: 2px;
                                            border-radius: 6px;
                                            }
                                            QLabel {
                                            border-style: none;
                                            }''')

                grid_movements = QGridLayout()
                for move_dir, normal_res in value.items():
                    
                    if move_dir == "flex":
                        label_flex = QLabel("сгибание/разгибание:")
                        grid_movements.addWidget(label_flex, 0, 0, Qt.AlignRight)
                        grid, dict_flex_ext = self.flex_extention(normal = normal_res)
                        dict_inner.append(dict_flex_ext)
                        grid_movements.addLayout(grid, 0, 1, Qt.AlignRight)
                    elif move_dir == "abdu":
                        label_abdu = QLabel("отведение/приведение:")
                        grid_movements.addWidget(label_abdu, 1, 0, Qt.AlignRight)
                        grid, dict_flex_ext = self.flex_extention(normal = normal_res)
                        dict_inner.append(dict_flex_ext)
                        grid_movements.addLayout(grid, 1, 1, Qt.AlignRight)
                    elif move_dir == "rotExt":
                        label_rot = QLabel("наружная/внутренняя ротация:")
                        grid_movements.addWidget(label_rot, 2, 0, Qt.AlignRight)
                        grid, dict_flex_ext = self.flex_extention(normal = normal_res)
                        dict_inner.append(dict_flex_ext)
                        grid_movements.addLayout(grid, 2, 1, Qt.AlignRight)
                    
                    elif move_dir == "inclineRignt":
                        label_inclineRignt = QLabel("наклон головы вправо/влево:")
                        grid_movements.addWidget(label_inclineRignt, 1, 0, Qt.AlignRight)
                        grid, dict_flex_ext = self.flex_extention(normal = normal_res)
                        dict_inner.append(dict_flex_ext)
                        grid_movements.addLayout(grid, 1, 1, Qt.AlignRight)
                    elif move_dir == "rotRight":
                        label_rotRight = QLabel("поворот головы вправо/влево:")
                        grid_movements.addWidget(label_rotRight, 2, 0, Qt.AlignRight)
                        grid, dict_flex_ext = self.flex_extention(normal = normal_res)
                        dict_inner.append(dict_flex_ext)
                        grid_movements.addLayout(grid, 2, 1, Qt.AlignRight)
                    elif move_dir == "inclineAnt":
                        label_inclineAnt = QLabel("выпрямленное положении (см)/наклон вперед (см):")
                        grid_movements.addWidget(label_inclineAnt, 0, 0, Qt.AlignRight)
                        grid, dict_flex_ext = self.inclineAnt(normal = normal_res)
                        dict_inner.append(dict_flex_ext)
                        grid_movements.addLayout(grid, 0, 1, Qt.AlignRight)
                    elif move_dir == "rotSup":
                        label_rotSup = QLabel("супинация/пронация:")
                        grid_movements.addWidget(label_rotSup, 0, 0, Qt.AlignRight)
                        grid, dict_flex_ext = self.flex_extention(normal = normal_res)
                        dict_inner.append(dict_flex_ext)
                        grid_movements.addLayout(grid, 0, 1, Qt.AlignRight)
                    elif move_dir == "flexPlant":
                        label_flexPlant = QLabel("подошвенное сгибание/разгибание:")
                        grid_movements.addWidget(label_flexPlant, 0, 0, Qt.AlignRight)
                        grid, dict_flex_ext = self.flex_extention(normal = normal_res)
                        dict_inner.append(dict_flex_ext)
                        grid_movements.addLayout(grid, 0, 1, Qt.AlignRight)
                if len(dict_inner) == 1:
                    dict_inner = dict_inner[0]
                movements.setLayout(grid_movements)
                gr_common = QHBoxLayout()
                label_degree = QLabel()
                label_degree.setStyleSheet('''QLabel {
                    background-color: #C0C0C0; 
                    color: black; 
                    border-style: groove;
                    border-width: 2px;
                    border-radius: 10px;
                    border-color: beige;
                    font: bold 14px;
                    text-align: center;
                    min-width: 8em;
                    max-width: 8em;
                    }
                    ''')
                gr_common.addWidget(movements, Qt.AlignVCenter)
                gr_common.addWidget(label_degree, Qt.AlignVCenter)
                
                

                if row_number <=2:
                    self.grid.addLayout(gr_common,row_number ,1, 1, 2, Qt.AlignHCenter)
                    self.lineEdits_up_center.append(dict_inner)
                    self.label_degree_up_center.append(label_degree)
                elif row_number >2 and row_number < 12:
                    self.grid.addLayout(gr_common,row_number ,1, Qt.AlignHCenter)
                    self.lineEdits_right.append(dict_inner)
                    self.label_degree_right.append(label_degree)
                elif row_number > 11:
                    self.grid.addLayout(gr_common,row_number-9 ,2, Qt.AlignHCenter)
                    self.lineEdits_left.append(dict_inner)
                    self.label_degree_left.append(label_degree)
                if row_number == 2:
                    row_number +=2
                else:
                    row_number +=1
            else:
                row_number +=1
                print("insert detail grid")
        print(len(self.lineEdits_right))
       
        print(len(self.lineEdits_left))
        print(len(self.lineEdits_up_center))

        print(len(self.label_degree_right))
        print(len(self.label_degree_left))
        print(len(self.label_degree_up_center))


        #self.movements = QWidget()
        #self.grid_movements = QGridLayout()
        #self.grid_movements.addWidget(self.label_flex, 0, 0, Qt.AlignRight)
        #self.grid_movements.addLayout(self.flex_extention(),0, 1, Qt.AlignRight)
        #self.grid_movements.addWidget(self.label_abdu, 1, 0, Qt.AlignRight)
        #self.grid_movements.addLayout(self.abduct_adduction(), 1, 1, Qt.AlignRight)
        #self.grid_movements.addWidget(self.label_rot, 2, 0, Qt.AlignRight)
        #self.grid_movements.addLayout(self.extern_intern_rotation(), 2, 1, Qt.AlignRight)
        #self.movements.setLayout(self.grid_movements)
        #self.grid.addWidget(self.movements,5 ,1, Qt.AlignHCenter)
        #self.grid.addLayout(self.vbox_right_scroll, 0 , 1)
        #self.grid.setColumnMinimumWidth(0, self.picture.width()+40)
        #self.grid.setColumnMinimumWidth(1, (self.picture.width()+40)/3)
        #self.grid.setColumnStretch(1, 0.5)
       
        self.Ok_button = PushButton("Ok")
        self.Ok_button.clicked.connect(self.btn_to_close)
        self.label_main_text = QLabel()
        self.label_main_text.setWordWrap(True)
        self.layout_label_main_text = QHBoxLayout()
        self.layout_label_main_text.addWidget(self.label_main_text)
        self.main_text = QGroupBox("Текст")
        self.main_text.setLayout(self.layout_label_main_text)

        self.main_text.setStyleSheet('''

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
        self.dict_wrist_foot = []
        self.wrist_button_right = PushButton("Ввести объем движений и/или дефекты")
        self.dict_wrist_foot.append(self.wrist_button_right)
        self.wrist_button_right.clicked.connect(self.wrist_move)
        self.wrist_button_left = PushButton("Ввести объем движений и/или дефекты")
        self.dict_wrist_foot.append(self.wrist_button_left)
        self.wrist_button_left.clicked.connect(self.wrist_move)

        self.foot_button_right = PushButton("Ввести объем движений и/или дефекты")
        self.dict_wrist_foot.append(self.foot_button_right)
        self.foot_button_right.clicked.connect(self.foot_move)
        self.foot_button_left = PushButton("Ввести объем движений и/или дефекты")
        self.dict_wrist_foot.append(self.foot_button_left)
        self.foot_button_left.clicked.connect(self.foot_move)
        
        self.grid.addWidget(self.wrist_button_right, 8, 1)
        self.grid.addWidget(self.wrist_button_left, 8, 2)
        self.grid.addWidget(self.foot_button_right, 12, 1)
        self.grid.addWidget(self.foot_button_left, 12, 2)

        self.grid.addWidget(self.main_text , 13, 0, 1, 3)

        self.grid.addWidget(self.main_text , 13, 0, 1, 3)
        self.grid.addWidget(self.Ok_button , 14, 0, 1, 3)

        self.setLayout(self.grid)
        self.move(400, 10)
        self.setWindowTitle ("Объем движений в суставах")
        self.show()

    def flex_extention(self, normal):
        grid = QHBoxLayout()
        dict_line_edit = []
        increment = 0
        for i in range(3):
            line_edit = QLineEdit()
            line_edit.textChanged.connect(self.calculate_dif)
            #line_edit.setMaxLength(3)
            #line_edit.setValidator(QtGui.QIntValidator(0, 100))
            line_edit.setPlaceholderText(str(normal[increment]))
            line_edit.setStyleSheet('''QLineEdit {
                border-style: groove;
                border-width: 2px;
                border-radius: 8px;
                border-color: #FFA07A;
                font: bold 12px;
                padding: 2px;
                }
            ''')
            line_edit.setFixedWidth(40)
            dict_line_edit.append(line_edit)
            grid.addWidget(line_edit, Qt.AlignRight)
            label_degree_sign= QLabel(self.degree_sign)
            grid.addWidget(label_degree_sign, Qt.AlignRight)
            if i <2:
                label_slash = QLabel("/")
                grid.addWidget(label_slash, Qt.AlignRight)
            increment +=1

        return grid, dict_line_edit

    def inclineAnt(self, normal):
        grid = QHBoxLayout()
        dict_line_edit = []
        increment = 0
        for i in range(2):
            line_edit = QLineEdit()
            line_edit.textChanged.connect(self.calculate_dif)
            #line_edit.setMaxLength(3)
            #line_edit.setValidator(QtGui.QIntValidator(0, 100))
            line_edit.setPlaceholderText(str(normal[increment]))
            line_edit.setStyleSheet('''QLineEdit {
                border-style: groove;
                border-width: 2px;
                border-radius: 8px;
                border-color: #FFA07A;
                font: bold 12px;
                padding: 2px;
                }
            ''')
            line_edit.setFixedWidth(40)
            dict_line_edit.append(line_edit)
            grid.addWidget(line_edit, Qt.AlignRight)
            label_length= QLabel("см")
            grid.addWidget(label_length, Qt.AlignRight)
            if i <1:
                label_slash = QLabel("/")
                grid.addWidget(label_slash, Qt.AlignRight)
            increment +=1

        return grid, dict_line_edit


    def calculate_dif(self, text):
        print(self.sender().objectName())
        list_lineedit = [self.lineEdits_up_center, self.lineEdits_right, self.lineEdits_left]
        list_labels = [ self.label_degree_up_center, self.label_degree_right, self.label_degree_left]
        list_contracture = [self.contracture_up_center, self.contracture_right, self.contracture_left]
        list_texts = [self.text_up_center, self.text_right, self.text_left]
        print(len(self.lineEdits_left))
        print(len(self.lineEdits_up_center))
        
        column = 0
        for col in list_lineedit:
            for item in col:
                for i in item:
                    if type(i) is list:
                        for cell in i:
                            if self.sender() == cell:
                                print("found, col %s" % str(column))
                                print(col.index(item), item.index(i), i.index(self.sender()))
                                a, b, c = col.index(item), item.index(i), i.index(self.sender())
                                if list_lineedit[column][a][b][0].text() and list_lineedit[column][a][b][1].text() and list_lineedit[column][a][b][2].text():
                                    move_range = int(list_lineedit[column][a][b][0].text())-int(list_lineedit[column][a][b][1].text())+int(list_lineedit[column][a][b][2].text())
                                    if column >0:
                                        move_range_normal = self.list_normal_move[a+3][b]

                                    else:
                                        move_range_normal = self.list_normal_move[a][b]
                                    move_range_percent = (move_range_normal-move_range)/move_range_normal*100
                                    move_range_percent = round(move_range_percent, 1)
                                    list_contracture[column][a][b] = move_range_percent
                                    print(list_contracture[column][a])
                                    print(column)
                                    print(a)
                                    if  isinstance(list_contracture[column][a][0], float) and  isinstance(list_contracture[column][a][1], float) and  isinstance(list_contracture[column][a][2], float):
                                        print(list_contracture[column][a])
                                        move_range_percent_common = (list_contracture[column][a][0] + list_contracture[column][a][1] + list_contracture[column][a][2])/3
                                        move_range_percent_common = round(move_range_percent_common, 1)
                                        list_labels[column][a].setText(str(move_range_percent_common))
                                        list_labels[column][a].setStyleSheet('''QLabel {
                                                                            background-color: %s; 
                                                                            color: black; 
                                                                            border-style: groove;
                                                                            border-width: 2px;
                                                                            border-radius: 10px;
                                                                            border-color: beige;
                                                                            font: bold 14px;
                                                                            text-align: center;
                                                                            min-width: 8em;
                                                                            max-width: 8em;
                                                                            }
                                                                            '''%self.color_define(percent=move_range_percent_common))
                                        axis_a, axis_b, axis_c = list_lineedit[column][a][0], list_lineedit[column][a][1], list_lineedit[column][a][2]
                                        axises = [
                                            [axis_a[0].text(), axis_a[1].text(), axis_a[2].text()],
                                            [axis_b[0].text(), axis_b[1].text(), axis_b[2].text()], 
                                            [axis_c[0].text(), axis_c[1].text(), axis_c[2].text(),]
                                            ]
                                        
                                        self.text_formation(axises=axises, column = column, row = a, axis_number = 3)
                                break
                    elif self.sender() == i:
                        print("found-1, col %s" % str(column))
                        print(col.index(item), item.index(self.sender()))
                        a, c = col.index(item), item.index(self.sender())
                        if len(list_lineedit[column][a])>2 and list_lineedit[column][a][0].text() and list_lineedit[column][a][1].text() and list_lineedit[column][a][2].text():
                            move_range = int(list_lineedit[column][a][0].text())-int(list_lineedit[column][a][1].text())+int(list_lineedit[column][a][2].text())
                            if column >0:
                                move_range_normal = self.list_normal_move[a+3][0]
                            else:
                                move_range_normal = self.list_normal_move[a][0]
                            move_range_percent = (move_range_normal-move_range)/move_range_normal*100
                            move_range_percent = round(move_range_percent, 1)
                            list_labels[column][a].setText(str(move_range_percent))
                            list_labels[column][a].setStyleSheet('''QLabel {
                                                                            background-color: %s; 
                                                                            color: black; 
                                                                            border-style: groove;
                                                                            border-width: 2px;
                                                                            border-radius: 10px;
                                                                            border-color: beige;
                                                                            font: bold 14px;
                                                                            text-align: center;
                                                                            min-width: 8em;
                                                                            max-width: 8em;
                                                                            }
                                                                            ''' %self.color_define(percent=move_range_percent))
                            list_contracture[column][a] = str(move_range_percent)
                            axis_a, axis_b, axis_c = list_lineedit[column][a][0], list_lineedit[column][a][1], list_lineedit[column][a][2]
                            axises = [axis_a.text(), axis_b.text(), axis_c.text()]
                            
                            self.text_formation(axises=axises, column = column, row = a, axis_number = 1)
                        
                        elif len(list_lineedit[column][a])==2 and list_lineedit[column][a][0].text() and list_lineedit[column][a][1].text():
                            move_range = int(list_lineedit[column][a][1].text())-int(list_lineedit[column][a][0].text())
                            move_range_normal = self.list_normal_move[a][0]
                            move_range_percent = (move_range_normal-move_range)/move_range_normal*100
                            move_range_percent = round(move_range_percent, 1)
                            list_labels[column][a].setText(str(move_range_percent))
                            list_labels[column][a].setStyleSheet('''QLabel {
                                                                            background-color: %s; 
                                                                            color: black; 
                                                                            border-style: groove;
                                                                            border-width: 2px;
                                                                            border-radius: 10px;
                                                                            border-color: beige;
                                                                            font: bold 14px;
                                                                            text-align: center;
                                                                            min-width: 8em;
                                                                            max-width: 8em;
                                                                            }
                                                                            '''%self.color_define(percent=move_range_percent))
                            list_contracture[column][a] = str(move_range_percent)
                            axis_a, axis_b = list_lineedit[column][a][0], list_lineedit[column][a][1]
                            axises = [axis_a.text(), axis_b.text()]
                            
                            self.text_formation(axises=axises, column = column, row = a, axis_number = 0)
                        break
            column += 1
        

    def color_define(self, percent):
        color = ""
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

        return color

    def label_difference_update(self, index):
        label = self.labelDif[index]
        print(label)
        
        if self.lineEdits_right[index].text() and self.lineEdits_left[index].text():
            radius_right = int(self.lineEdits_right[index].text())
            radius_left = int(self.lineEdits_left[index].text())
            difference = radius_right - radius_left
            label.setText(str(difference))
            self.text_formation(index = index)

    def text_formation(self, axises, column, row, axis_number):
        list_texts = [self.text_up_center, self.text_right, self.text_left]
        list_lineedits = [self.lineEdits_up_center, self.lineEdits_right, self.lineEdits_left]
        
        list_labels = [ self.label_degree_up_center, self.label_degree_right, self.label_degree_left]

        column_new = 0
        row_new = 0
        text = ""
        text_main = ""
        
        for label_group in list_labels:
            for label in label_group:
                if label.text() != "" and float(label.text())>0:
                    contr = ""
                    percent = float(label.text())
                    if percent>0 and percent <5:
                        contr = "незначительная"
                    elif percent >=5 and percent < 25:
                        contr = "1 ст."
                    elif percent >= 25 and percent < 50:
                        contr = "2 ст."
                    elif percent >= 50 and percent < 75:
                        contr = "3 ст."
                    elif percent >= 75:
                        contr = "4 ст."
                    text +=  list_texts[column_new][row_new][0]
                    if (column_new==0 and row_new==0) or (column_new in (1,2) and row_new in (0,4)):
                        
                        tuple_working = []
                        for line in list_lineedits[column_new][row_new]:
                            for cell in line:
                                tuple_working.append(cell.text())
                        tuple_working.append(contr)
                        tuple_working = tuple(tuple_working)

                        if column_new == 0:
                            text += " - сгибание/разгибание %s/%s/%s гр., наклонголовы вправо %s/%s/%s гр., наклон головы влево %s/%s/%s гр., (%s); " % tuple_working

                        else:
                            text += " - сгибание/разгибание %s/%s/%s гр., отведение/приведение %s/%s/%s гр., наружная/внутренняя ротация %s/%s/%s гр., (%s); " % tuple_working


                    elif column_new ==0 and row_new in (1,2):
                        text += " - выпрямленное положение/наклон вперед %s/%s см (%s), " % (list_lineedits[column_new][row_new][0].text(),list_lineedits[column_new][row_new][1].text(), contr)
                    elif column_new in (1,2) and row_new in (1,3,5):
                        text += " - сгибание/разгибание %s/%s/%s гр. (%s), " % (list_lineedits[column_new][row_new][0].text(),list_lineedits[column_new][row_new][1].text(),list_lineedits[column_new][row_new][2].text(), contr)
                    elif column_new in (1,2) and row_new ==2:
                        text += " - супинация/пронация %s/%s/%s гр. (%s), " % (list_lineedits[column_new][row_new][0].text(),list_lineedits[column_new][row_new][1].text(),list_lineedits[column_new][row_new][2].text(), contr)
                    elif column_new in (1,2) and row_new ==6:
                        text += " - подошвенное сгибание/разгибание %s/%s/%s гр. (%s), " % (list_lineedits[column_new][row_new][0].text(),list_lineedits[column_new][row_new][1].text(),list_lineedits[column_new][row_new][2].text(), contr)

                row_new+=1
            row_new = 0
            column_new+=1

        text_main = "Ограничен объем движений в " + text[:-2] + "."
        self.label_main_text.setText(text_main)


    def btn_to_close(self):
        name = "modules/joints_text"
        text = self.label_main_text.text()
        text = text[:-1] + "."
        
        with open(name + '.pkl', 'wb') as f:
            pickle.dump(text, f, pickle.HIGHEST_PROTOCOL)
        self.joints_send_info.emit()

        self.close()
        
        return self.label_main_text.text()

    def wrist_move(self):
        index = self.dict_wrist_foot.index(self.sender())
        print(index)
        self.inner_wrist_window = WristFootWindow(text = index)
        #self.inner_joints.setStyleSheet("background-color: #fff")
        self.inner_wrist_window.text_send.connect(self.wrist_text_define)
        self.inner_wrist_window.show()
        #self.inner_joints.joints_send_info.connect(self.get_joints_info)

    def wrist_text_define(self):
        text_to_add = ""
        

        if self.inner_wrist_window.label_main_text_cont.text() != "" and self.inner_wrist_window.label_main_text.text() != "":
            text_to_add = self.inner_wrist_window.label_main_text_cont.text()[:-2] + "; " + self.inner_wrist_window.label_main_text.text().lower() + " "
        elif self.inner_wrist_window.label_main_text_cont.text() != "" and self.inner_wrist_window.label_main_text.text() == "":
            text_to_add = self.inner_wrist_window.label_main_text_cont.text() + " "
        elif self.inner_wrist_window.label_main_text_cont.text() == "" and self.inner_wrist_window.label_main_text.text() != "":
            text_to_add = self.inner_wrist_window.label_main_text.text() + " "
        if self.inner_wrist_window.text_index == 0:
            self.wrist_text_right = text_to_add
        else:
            self.wrist_text_left = text_to_add
        
        print("wrist_text_right = %s" % self.wrist_text_right)
        print("wrist_text_left = %s" % self.wrist_text_left)
        print("text_index = %s" % self.inner_wrist_window.text_index)
        
        self.dict_wrist_foot[self.inner_wrist_window.text_index].setColor("#9ACD32")

    def get_wrist_window_info(self):
        with open( "modules/joints_text.pkl", 'rb') as f:
            self.label_joints_text.setText(pickle.load(f))
            self.main_text_dict["joints"] = self.label_joints_text.text()
        print("get info")
        print(self.main_text_dict)
        self.okButton.setStyleSheet('background: rgb(250,128,114);')
        self.update()

    def foot_move(self):
        index = self.dict_wrist_foot.index(self.sender())
        print(index)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    
    form = EdemaWindow()
    form.show()
    sys.exit(app.exec_())