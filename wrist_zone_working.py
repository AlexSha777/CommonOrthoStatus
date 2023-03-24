import sys
from PyQt5 import QtGui 
from PyQt5.QtWidgets import QLabel, QApplication, QWidget, QScrollArea, QHBoxLayout, QVBoxLayout, QDesktopWidget, QPushButton

from PyQt5.QtGui import   QPainter ,QPixmap, QImage, QColor, QPen
from PyQt5.QtCore import pyqtSignal, Qt , QPoint



from wrist_L_detect import wrist_L_detect
from wrist_L_name import wrist_L_name
from wrist_L_axis import wrist_L_axis
from wrist_L_to_draw import wrist_L_to_draw

from wrist_R_detect import wrist_R_detect
from wrist_R_name import wrist_R_name
from wrist_R_axis import wrist_R_axis
from wrist_R_to_draw import wrist_R_to_draw




class WristDefects (QWidget):
    text_changed = pyqtSignal()
    def __init__(self, file_name, parent=None):
        super(WristDefects,self).__init__(parent)
        self.file_name = file_name
        self.setWindowTitle ("Пример рисования")
        #self.pix = QPixmap() # создать экземпляр объекта QPixmap
        #self.lastPoint = QPoint () # начальная точка
        #self.endPoint = QPoint () # конечная точка
        self.initUi()
		
    def initUi(self):
        
        self.pix = QPixmap(self.file_name)
        self.pix_main = QPixmap(self.file_name).toImage()


        self.resize(self.pix.width(), self.pix.height())
        self.setMouseTracking(True)

        self.wrist_R_name = wrist_R_name.copy()
        self.wrist_R_detect = wrist_R_detect.copy()
        self.wrist_R_axis = wrist_R_axis.copy()
        self.wrist_R_to_draw = wrist_R_to_draw.copy()


        self.wrist_L_name = wrist_L_name.copy()
        self.wrist_L_detect = wrist_L_detect.copy()
        self.wrist_L_axis = wrist_L_axis.copy()
        self.wrist_L_to_draw = wrist_L_to_draw.copy()

        self.checked_zones = []

        self.amputation_level = {}
        self.amputation_level_point = {}
        self.amputation_level_text = ""
        
        self.defect_percent = 0
        self.wrist_defect_detailed = {}


        
        
        self.ampute_detail = {
        
        "metacarp_1": {
                "base": [0.88, 1],
                "diaf": [0.68, 0.87],
                "caput": [0.55, 0.67]
                },
        
        "pp_1": {
                "base": [0.49, 0.54],
                "diaf": [0.35, 0.48],
                "caput": [0.25, 0.34]
                },

        "dp_1": {
                "base": [0.18, 0.24],
                "diaf": [0.13, 0.17],
                "tuber": [0, 0.12]
                },

        "metacarp_2": {
                "base": [0.79, 1],
                "diaf": [0.25, 0.78],
                "caput": [0, 0.24]
                }, 

        "pp_2": {
                "base": [0.9, 1],
                "diaf": [0.63, 0.89],
                "caput": [0.5, 0.62]
                },

        "mp_2": {
                "base": [0.45, 0.49],
                "diaf": [0.31, 0.44],
                "caput": [0.25, 0.3]
                },

        "dp_2": {
                "base": [0.19, 0.24],
                "diaf": [0.12, 0.18],
                "tuber": [0, 0.11]
                },

        "metacarp_3": {
                "base": [0.79, 1],
                "diaf": [0.29, 0.78],
                "caput": [0, 0.28]
                },

        "pp_3": {
                "base": [0.9, 1],
                "diaf": [0.63, 0.89],
                "caput": [0.5, 0.62]
                },

        "mp_3": {
                "base": [0.45, 0.49],
                "diaf": [0.31, 0.44],
                "caput": [0.23, 0.3]
                },

        "dp_3": {
                "base": [0.17, 0.22],
                "diaf": [0.11, 0.16],
                "tuber": [0, 0.1]
                },

        "metacarp_4": {
                "base": [0.8, 1],
                "diaf": [0.3, 0.79],
                "caput": [0, 0.29]
                }, 

        "pp_4": {
                "base": [0.95, 1],
                "diaf": [0.67, 0.94],
                "caput": [0.56, 0.66]
                },

        "mp_4": {
                "base": [0.5, 0.55],
                "diaf": [0.35, 0.49],
                "caput": [0.26, 0.34]
                },

        "dp_4": {
                "base": [0.2, 0.25],
                "diaf": [0.13, 0.19],
                "tuber": [0, 0.12]
                },

        "metacarp_5": {
                "base": [0.79, 1],
                "diaf": [0.27, 0.78],
                "caput": [0, 0.26]
                },

        "pp_5": {
                "base": [0.93, 1],
                "diaf": [0.68, 0.92],
                "caput": [0.55, 0.67]
                },

        "mp_5": {
                "base": [0.47, 0.54],
                "diaf": [0.38, 0.46],
                "caput": [0.28, 0.37]
                },

        "dp_5": {
                "base": [0.22, 0.27],
                "diaf": [0.13, 0.21],
                "tuber": [0, 0.12]
                },
        }
        
        self.os_level_name = {
        
        "base": "основания",
        "diaf": "диафиза",
        "caput": "головки",
        "tuber": "бугристости",
        }

        # 1 base pp_1 0.49 - 0.54 
        # 1 diaf pp_1 0.35 - 0.48 
        # 1 caput pp_1  0.25 - 0.34 

        # 1 base dp_1 0.18 - 0.24 
        # 1 diaf dp_1 0.13 - 0.17 
        # 1 tuber dp_1  0 - 0.12


        # 2-5 base mc_2 0.79 - 1.0 mc_3 0.79. - 1.0    mc_4 0.8  - 1     mc_5 0.79 - 1
        # 2-5 diaf mc_2 0.25 - 0.78  mc_3 0.29 - 0.78  mc_4 0.3 - 0.79   mc_5 0.27 - 0.78
        # 2-5 caput mc_2 0 - 0.24  mc_3 0 - 0.28       mc_4 0 - 0.29     mc_5 0 - 0.26


        # 2-5 base pp_2 pp_3 0.9 - 1       pp_4 0.95  - 1      pp_5 0.93 - 1
        # 2-5 diaf pp_2 pp_3 0.63 - 0.89       pp_4 0.67 - 0.94       pp_5 0.68 - 0.92
        # 2-5 caput pp_2 pp_3 0.5 - 0.64       pp_4 0.56 - 0.68       pp_5 0.55 - 0.69

        # 2-5 base mp_2 mp_3 0.45 - 0.49       mp_4  0.5 - 0.55       mp_5 0.47 - 0.54
        # 2-5 diaf mp_2 mp_3 0.44 - 0.31       mp_4  0.49 - 0.35       mp_5 0.46 - 0.38
        # 2-5 caput mp_2  0.30 - 0.25  mp_3 0.30 - 0.23       mp_4  0.34 - 0.26       mp_5 0.37 - 0.28

        # 2-5 base dp_2  0.24 - 0.19  dp_3 0.22 - 0.17       dp_4  0.25 - 0.2       dp_5 0.27 - 0.22
        # 2-5 diaf dp_2  0.18 - 0.12  dp_3 0.16 - 0.11       dp_4  0.19 - 0.13       dp_5 0.21 - 0.13
        # 2-5 tuber dp_2  0.11 - 0  dp_3 0.1 - 0       dp_4  0.12 - 0       dp_5 0.12 - 0

        #self.bone_zones_R = load_wrist_R_bone()
        #self.bone_R_coord = []
        
        #for k, v in self.bone_zones_R.items():
        #   print(k)
        #    for i in v:
        #        self.bone_R_coord.append(i)

        #self.bone_zones_L = load_wrist_L_bone()
        #self.bone_L_coord = []
        
        #for k, v in self.bone_zones_L.items():
        #    print(k)
        #    for i in v:
        #        self.bone_L_coord.append(i)

    def get_checked_zones(self):

        return self.checked_zones
        
    def get_text(self):
        string = ""
        if self.defect_percent !=0:
            string = self.amputation_level_text[:-2] + " (всего: " + str(self.defect_percent) + "% от ф-ии хвата и удержания предметов кистями)" + "."
        return string


    
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
            if self.file_name == "wrists_l.bmp":
                for k, v in self.wrist_L_detect.items():
                    for i in v:
                        if position == i:
                            print(k)
                            self.change_color(k, self.file_name, position)
                            #print(front_zones_names_dict[k])
            else:
                for k, v in self.wrist_R_detect.items():
                    for i in v:
                        if position == i:
                            print(k)
                            self.change_color(k, self.file_name, position)
                            #print(back_zones_names_dict[k])
    
    def change_color(self, k, file_name, position):
    
        zone_name = k
        updated_image = self.pix.toImage()
        source_dict = 0
        if file_name == "wrists_l.bmp":
            source_dict = self.wrist_L_detect
            source_dict_todraw = self.wrist_L_to_draw
        else:
            source_dict = self.wrist_R_detect
            source_dict_todraw = self.wrist_R_to_draw
        finger_number = [x[-1] for x in self.checked_zones]
        print("finger_number")
        print(finger_number)

        if k in self.checked_zones or k[-1] in finger_number:
            if k in ["dp_1","metacarp_1","pp_1",]:
                zone_to_update = source_dict_todraw["finger_1_metacarp"][:]
                for b in ["dp_1","metacarp_1","pp_1",]:
                    if b in self.checked_zones:
                        self.checked_zones.remove(b)
                        del self.amputation_level[b]
                        del self.amputation_level_point[b]
            else:
                
                for z in ["dp_","mp_","metacarp_","pp_",]:
                    print(z + k[-1])
                    if (z + k[-1]) in self.checked_zones:
                        self.checked_zones.remove(z + k[-1])
                        del self.amputation_level[z + k[-1]]
                        del self.amputation_level_point[z + k[-1]]
                        zone_to_update = source_dict_todraw["finger_"+ k[-1]][:]
                        zone_to_update.extend(source_dict_todraw["metacarp_" + k[-1]][:])
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
        print("amputation_level_point=%s" %self.amputation_level_point)
        print(self.amputation_level_text)
        print("percent: %s" % self.defect_percent)
        print(self.wrist_defect_detailed)
        
    def picture_clear(self):
        
        updated_image = self.pix.toImage()
        self.pix = QPixmap.fromImage(self.pix_main)
        self.checked_zones = []
        self.amputation_level = {}
        self.amputation_level_point = {}
        self.amputation_level_text = ""
        self.defect_percent = 0
        self.update()


    def text_formation(self):
        wrist = ""
        ampute = ""
        diaf_level = 0
        diaf_level_text = ""
        self.wrist_defect_detailed = {}

        percent = 0
        phalanx_weight = {"dp_2": 0.15, "dp_3": 0.15, "dp_4": 0.15, "dp_5": 0.15,
                        "mp_2": 0.35, "mp_3": 0.35, "mp_4": 0.35, "mp_5": 0.35,
                        "pp_2": 0.50, "pp_3": 0.50, "pp_4": 0.50, "pp_5": 0.50,
                        "dp_1": 0.50, "pp_1": 0.50}

        finger_weight = {"1": 0.2, "2": 0.08, "3": 0.075, "4": 0.075, "5": 0.07}

        if self.file_name == "wrists_l.bmp":
            wrist = "левой кисти: "
        else:
            wrist = "правой кисти: "

        if self.checked_zones != []:
            ampute = "дефект " + wrist

            for key, value in self.amputation_level.items():
                print(key)
                for detail_key, detail_value in self.ampute_detail[key].items():
                    if value >= detail_value[0] and value <= detail_value[1]:
                        print(detail_key)
                        if key[:-1] != "metacarp_": 
                            phalanx_index = 1 - round((value - detail_value[0])/(list(self.ampute_detail[key].values())[0][1]-list(self.ampute_detail[key].values())[2][0]),4)
                            
                            self.wrist_defect_detailed[key] = phalanx_index

                            percent += (round((value - detail_value[0])/(detail_value[1] - detail_value[0]),4)) * phalanx_weight[key] * finger_weight[key[-1]]
                            
                            if key[:-1] == "pp_" and key != "pp_1":
                                percent+= phalanx_weight["dp_"+key[-1]] * finger_weight[key[-1]]
                                percent+= phalanx_weight["mp_"+key[-1]] * finger_weight[key[-1]]
                            elif key[:-1] == "mp_":
                                percent+= phalanx_weight["dp_"+key[-1]] * finger_weight[key[-1]]
                            elif key== "pp_1":
                                percent+= phalanx_weight["dp_1"] * finger_weight["1"]
                        elif key[:-1] == "metacarp_":
                            percent += 1 * finger_weight[key[-1]]
                            phalanx_index = 1 - round((value - detail_value[0])/(list(self.ampute_detail[key].values())[0][1]-list(self.ampute_detail[key].values())[2][0]),4)
                            self.wrist_defect_detailed[key] = phalanx_index

                        diaf_level_text = self.diaf_level(detail_key = detail_key, key = key, value = value, detail_value = detail_value)
                        print("diaf_level_text")
                        print(diaf_level_text)
 
                        ampute += key[-1] + " луча на уровне " + diaf_level_text + self.os_level_name[detail_key] + " " + self.wrist_R_name[key][:-6] + ", "
                        print("ampute")
                        print(ampute)
                        diaf_level = 0
                        diaf_level_text = ""
        
        self.amputation_level_text = ampute
        self.defect_percent = round(percent*100, 2)

    def diaf_level(self, detail_key, key, value, detail_value):
        diaf_level_text_new = ""
        if detail_key == "diaf" and key[:-1] in ["metacarp_", "pp_"]:
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
        

        zone_detail = ""

        if zone[:2] == "me" and zone[-1] != "1":
            axis_zone = "metacarp_" + zone[-1] + "_axis"
        elif zone[:2] == "me" and zone[-1] == "1":
            axis_zone = "finger_1_metacarp_axis"
        elif zone[:2] != "me" and zone[-1] != "1":
            axis_zone = "finger_" + zone[-1] + "_axis"
        elif zone[:2] != "me" and zone[-1] == "1":
            axis_zone = "finger_1_metacarp_axis"
        side = ""
        if self.file_name == "wrists_l.bmp":
            axis = self.wrist_L_axis[axis_zone]
            side = "l"

        else:
            axis = self.wrist_R_axis[axis_zone]
            side = "r"
        
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


        for key, value in self.ampute_detail[zone].items():
            
            if level >= value[0] and level <= value[1]:
                zone_detail = key[:]
                print("key=%s" %key)

        self.amputation_level_point[zone] = [zone_detail, point]


        if side == "r":
            to_draw = self.wrist_R_to_draw
            wrist_to_draw = to_draw.copy()
        elif side == "l":
            to_draw = self.wrist_L_to_draw
            wrist_to_draw = to_draw.copy()

        to_color_zone = []
        
        if zone[:3] == "met" and zone[-1] != "1":
            print(zone)
            name = "finger_" + zone[-1]
            print("name: %s" %name)
            to_color_zone = wrist_to_draw[name][:]
            print("finger zone length: %s" % len(wrist_to_draw[name]))
            print("matacarp zone length: %s" % len(wrist_to_draw[zone]))
            print(len(to_color_zone))
            print("***********")
            for point_to_draw in wrist_to_draw[zone]:
                if point_to_draw[1]>= round(k_perpend*(point_to_draw[0]-point[0]) + point[1]):
                    to_color_zone.append(point_to_draw)
            print(len(to_color_zone))
        elif zone[-1] == "1":
            for point_to_draw in wrist_to_draw["finger_1_metacarp"]:
                if point_to_draw[1]>= round(k_perpend*(point_to_draw[0]-point[0]) + point[1]):
                    to_color_zone.append(point_to_draw)
        else:
            print(zone)
            for point_to_draw in wrist_to_draw["finger_" + zone[-1]]:
                if point_to_draw[1]>= round(k_perpend*(point_to_draw[0]-point[0]) + point[1]):
                    to_color_zone.append(point_to_draw)

        return to_color_zone

        '''
        if zone[:2] == "me" and zone[-1:] != 1:
            if side == "r":
                to_color_zone = self.wrist_R_to_draw["finger_"+zone[-1:]]
            else:
                to_color_zone = self.wrist_L_to_draw["finger_"+zone[-1:]]
        else:
            to_color_zone = self.wrist_R_to_draw["finger_"+zone[-1:]]


        line = []
        start_point = point[0]-50
        for i in range(100):
            line_point = [start_point+i, ]
            line_point.append(round(k_perpend*((start_point+i)-point[0]) + point[1], 2))
            line.append(line_point)
        print(line)


        #y-point[1] = k_perpend(x-point[0])

        painter = QPainter(pixmap)
        painter.begin(self)
        painter.setPen(QPen(Qt.red, 3))
        for point_line in line:
            painter.drawPoint(point_line[0], point_line[1])
        #painter.drawLine(point[0], point[1], 30, 30)
        painter.setPen(QPen(Qt.black, 5))
        painter.drawPoint(x_cross, y_cross)
        painter.end()
        return pixmap
        #self.update()
        '''




    """
    def mouseMoveEvent(self, event):	
		 # Перемещайте мышь, удерживая нажатой левую кнопку мыши
        position = [event.x(), event.y()]

        print(position)

        if self.file_name == "front_clear.bmp":
            for k, v in self.front_zones_dict.items():
                for i in v:
                    if position == i:
                        print(k)
                        #print(front_zones_names_dict[k])
        else:
            for k, v in self.back_zones_dict.items():
                for i in v:
                    if position == i:
                        print(k)
                        #print(back_zones_names_dict[k])

    """        

        #if position in self.body_coord:
        #   print ('Ok')

            

            

         # Событие отпускания мыши
    

class ScrollOnPicture(QWidget):

    def __init__(self, file_name):
        super().__init__()
        self.file_name = file_name
        self.initUI()
        

    def initUI(self):
        self.widget = WristDefects(self.file_name)
        scroll = QScrollArea()
        #scroll.setBackgroundRole(QPalette.Dark)
        scroll.setWidget(self.widget)
        hbox = QHBoxLayout()
        hbox.addWidget(scroll)
        
        footer = QHBoxLayout()

        self.okButton = QPushButton("OK")
        self.okButton.setStyleSheet('background: rgb(173,255,47);')
        self.okButton.clicked.connect(self.sendInfo)

        self.cancelButton = QPushButton("Cancel")
        self.cancelButton.setStyleSheet('background: rgb(173,255,47);')
        self.cancelButton.clicked.connect(self.close)
        #self.cancelButton.clicked.connect()
        
        self.label_main = QLabel()

        footer.addWidget(self.okButton)
        footer.addWidget(self.cancelButton)
        main = QVBoxLayout(self)
        main.addLayout(hbox)
        main.addWidget(self.label_main)
        main.addLayout(footer)

        #sizeObject = QDesktopWidget().screenGeometry(-1)
        sizeObject = QDesktopWidget().screenGeometry(-1)
        self.resize((self.widget.width()+40), (self.widget.height() +40))
        
    def sendInfo(self):
        print (self.widget.get_checked_zones())
        #return
			
if __name__ == "__main__":
    app = QApplication(sys.argv)
    file_name = "front_clear.bmp"
    form = ScrollOnPicture(file_name)
    form.show()
    sys.exit(app.exec_())