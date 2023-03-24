import sys
from PyQt5 import QtGui 
from PyQt5.QtWidgets import QLabel, QApplication, QWidget, QScrollArea, QHBoxLayout, QVBoxLayout, QDesktopWidget, QPushButton

from PyQt5.QtGui import   QPainter ,QPixmap, QImage, QColor, QPen
from PyQt5.QtCore import pyqtSignal, Qt , QPoint

from ped_axis import ped_axis

from ped_zone_detect import ped_zone_detect


class PedDefects (QWidget):
    text_changed = pyqtSignal()
    def __init__(self, file_name, parent=None):
        super(PedDefects,self).__init__(parent)
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

        self.ped_zone_detect = ped_zone_detect.copy()
        self.ped_axis = ped_axis.copy()

        #print("zones %s" %self.ped_zone_detect.keys())
        #print("values %s" %self.ped_zone_detect["Ped_d_1_ray"])
        #print("axis %s" %self.ped_axis.keys())

        self.zone_names = {
            'Ped_d': "правая стопа", 
            'Ped_d_1_ray': "1 луча", 
            'Ped_d_2_ray':"2 луча", 
            'Ped_d_3_ray':"3 луча", 
            'Ped_d_4_ray':"4 луча", 
            'Ped_d_5_ray':"5 луча", 
            'Ped_d_cub':"кубовидной кости", 
            'Ped_d_scaph':"ладьевидной кости", 
            'Ped_d_sphen':"клиновидных костей", 
            'Ped_d_tal_calc':"таранной и пяточной костей", 
            'Ped_s': "левая стопа", 
            'Ped_s_1_ray':"1 луча", 
            'Ped_s_2_ray':"2 луча", 
            'Ped_s_3_ray':"3 луча", 
            'Ped_s_4_ray':"4 луча", 
            'Ped_s_5_ray':"5 луча", 
            'Ped_s_cub':"кубовидной кости", 
            'Ped_s_scaph':"ладьевидной кости", 
            'Ped_s_sphen':"клиновидных костей", 
            'Ped_s_tal_calc':"таранной и пяточной костей",
            }

        self.axis = [
            'Ped_d_1_ray_axis', 
            'Ped_d_2_ray_axis', 
            'Ped_d_3_ray_axis', 
            'Ped_d_4_ray_axis', 
            'Ped_d_5_ray_axis', 
            'Ped_d_cub_axis', 
            'Ped_d_scaph_axis', 
            'Ped_d_sphen_axis', 
            'Ped_d_tal_calc_axis', 
            'Ped_s_1_ray_axis', 
            'Ped_s_2_ray_axis', 
            'Ped_s_3_ray_axis', 
            'Ped_s_4_ray_axis', 
            'Ped_s_5_ray_axis', 
            'Ped_s_cub_axis', 
            'Ped_s_scaph_axis', 
            'Ped_s_sphen_axis', 
            'Ped_s_tal_calc_axis'
            ]

        self.checked_zones = []

        self.amputation_level = {}
        self.amputation_level_point = {}
        self.amputation_level_text = ""
        
        self.defect_percent = 0
        self.wrist_defect_detailed = {}

        self.ampute_detail = {
        



            '1_ray': {
                "dp_tub": [0, 0.12],
                "dp_diaf": [0.13, 0.18],
                "dp_base": [0.19, 0.24],
                "pp_caput": [0.25, 0.32],
                "pp_diaf": [0.33, 0.43],
                "pp_base": [0.44, 0.49],
                "meta_caput": [0.5, 0.66],
                "meta_diaf": [0.67, 0.88],
                "meta_base": [0.89, 1.0],
            }, 

            '2_ray':{
                "dp": [0, 0.11],
                "mp": [0.12, 0.23],
                "pp_caput": [0.24, 0.3],
                "pp_diaf": [0.31, 0.42],
                "pp_base": [0.43, 0.47],
                "meta_caput": [0.48, 0.59],
                "meta_diaf": [0.6, 0.93],
                "meta_base": [0.94, 1.0],
            }, 

            '3_ray':{
                "dp": [0, 0.13],
                "mp": [0.14, 0.23],
                "pp_caput": [0.24, 0.29],
                "pp_diaf": [0.3, 0.4],
                "pp_base": [0.41, 0.45],
                "meta_caput": [0.46, 0.57],
                "meta_diaf": [0.58, 0.88],
                "meta_base": [0.89, 1.0],
            }, 

            '4_ray':{
                "dp": [0, 0.12],
                "mp": [0.13, 0.23],
                "pp_caput": [0.24, 0.3],
                "pp_diaf": [0.31, 0.39],
                "pp_base": [0.4, 0.44],
                "meta_caput": [0.45, 0.55],
                "meta_diaf": [0.56, 0.9],
                "meta_base": [0.91, 1.0],
            }, 

            '5_ray':{
                "dp": [0, 0.07],
                "mp": [0.08, 0.14],
                "pp_caput": [0.15, 0.2],
                "pp_diaf": [0.21, 0.29],
                "pp_base": [0.3, 0.34],
                "meta_caput": [0.35, 0.45],
                "meta_diaf": [0.46, 0.78],
                "meta_base": [0.79, 1.0],
            },
            }
         
        
        self.os_level_name = {
            "dp_tub": "бугристости дистальной фаланги",
            "dp_diaf": "диафиза дистальной фаланги",
            "dp_base": "основания дистальной фаланги",

            "dp": "дистальной фаланги",
            "mp": "средней фаланги",
            "pp_caput": "головки проксимальной фаланги",
            "pp_diaf": "диафиза проксимальной фаланги",
            "pp_base": "основания проксимальной фаланги",
            "meta_caput": "головки плюсневой кости",
            "meta_diaf": "диафиза плюсневой кости",
            "meta_base": "основания плюсневой кости",
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
        string = self.amputation_level_text[:-2] + "."
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
            if self.file_name == "Ped_d.bmp":
                zones_to_detect = [
                'Ped_d_1_ray',
                'Ped_d_2_ray',
                'Ped_d_3_ray', 
                'Ped_d_4_ray',
                'Ped_d_5_ray',
                'Ped_d_cub', 
                'Ped_d_scaph', 
                'Ped_d_sphen', 
                'Ped_d_tal_calc',
                ]
            elif self.file_name == "Ped_s.bmp":
                zones_to_detect = [
                'Ped_s_1_ray',
                'Ped_s_2_ray',
                'Ped_s_3_ray', 
                'Ped_s_4_ray',
                'Ped_s_5_ray',
                'Ped_s_cub', 
                'Ped_s_scaph', 
                'Ped_s_sphen', 
                'Ped_s_tal_calc',
                ]

            position = [event.x(), event.y()]
            print(position)
            for zone in zones_to_detect:
                for v in self.ped_zone_detect[zone]:
                    if position == v:
                        print("zone_press_event:%s" %zone)
                        self.change_color(zone, self.file_name, position)
                        #print(front_zones_names_dict[k])
            
    
    def change_color(self, k, file_name, position):
    
        zone_name = k
        updated_image = self.pix.toImage()
        source_dict = 0
        zone_to_draw = []
        keys_to_delete = []
        zone_to_add_back = []
        

        if k in self.checked_zones:
            
            self.checked_zones.remove(k)
            if k in self.amputation_level.keys():
                self.amputation_level.pop(k)
                self.amputation_level_point.pop(k)
            if zone_name[6:] == "cub":
                for z in ["cub", "4_ray", "5_ray"]:
                    zone_to_add_back.append(z)
            elif zone_name[6:] == "scaph":
                for z in ["scaph","1_ray", "2_ray", "3_ray", "sphen"]:
                    zone_to_add_back.append(z)
            elif zone_name[6:] == "sphen":
                for z in ["1_ray", "2_ray", "3_ray","sphen"]:
                    zone_to_add_back.append(z)
            elif zone_name[6:] == "tal_calc":
                for z in ["1_ray", "2_ray", "3_ray", "4_ray", "5_ray", "sphen", "scaph", "cub", "tal_calc"]:
                    zone_to_add_back.append(z)
            elif zone_name[6:] in ["1_ray", "2_ray", "3_ray", "4_ray", "5_ray"]:
                zone_to_add_back.append(zone_name[6:])
            #del self.amputation_level[b]
            for zone_back in zone_to_add_back:
                for x in self.ped_zone_detect[file_name[:5] + "_" + zone_back]:
                    color = QColor(self.pix_main.pixel(x[0],x[1]))
                    QImage.setPixelColor(updated_image, x[0], x[1], color)
        else:
            #color = QColor(255, 99, 71)
            color = (40, 10, 10)

            self.checked_zones.append(k)
            list_to_draw = self.perpendicular(zone=zone_name, point=position)
            zone_to_draw.extend(list_to_draw)
            
            if zone_name[6:] in ["1_ray", "2_ray", "3_ray", "4_ray", "5_ray"]:
                pass
            elif zone_name[6:] == "cub":
                keys_to_delete = [zone_name[:6]+"4_ray", zone_name[:6]+"5_ray"]
                for i in keys_to_delete:                    
                    zone_to_draw.extend(self.ped_zone_detect[i])
                    if i not in self.checked_zones: self.checked_zones.append(i)
                

            elif zone_name[6:] == "scaph":
                keys_to_delete = [zone_name[:6]+"1_ray", zone_name[:6]+"2_ray", zone_name[:6]+"3_ray", zone_name[:6]+"sphen"]
                for i in keys_to_delete:                    
                    zone_to_draw.extend(self.ped_zone_detect[i])
                    if i not in self.checked_zones: self.checked_zones.append(i)
                

            elif zone_name[6:] == "sphen":
                keys_to_delete =[zone_name[:6]+"1_ray", zone_name[:6]+"2_ray", zone_name[:6]+"3_ray"]
                for i in keys_to_delete:                    
                    zone_to_draw.extend(self.ped_zone_detect[i])
                    if i not in self.checked_zones: self.checked_zones.append(i)
                

            elif zone_name[6:] == "tal_calc":
                keys_to_delete =  [ zone_name[:6]+"1_ray", 
                                    zone_name[:6]+"2_ray", 
                                    zone_name[:6]+"3_ray", 
                                    zone_name[:6]+"sphen", 
                                    zone_name[:6]+"scaph",
                                    zone_name[:6]+"cub",
                                    zone_name[:6]+"4_ray", 
                                    zone_name[:6]+"5_ray"]
                for i in keys_to_delete:                    
                    zone_to_draw.extend(self.ped_zone_detect[i])
                    if i not in self.checked_zones: self.checked_zones.append(i)
                
            if keys_to_delete != []:
                for x in keys_to_delete: 
                    if x in self.amputation_level.keys():
                        self.amputation_level.pop(x)
                        self.amputation_level_point.pop(x) 


            #for x in source_dict[zone_name]:
            for x in zone_to_draw:
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
        print("self.amputation_level_point=%s" %self.amputation_level_point)
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
        ped = ""
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

        if self.file_name == "Ped_s.bmp":
            ped = "левой стопы: "
        else:
            ped = "правой стопы: "

        if self.checked_zones != []:
            ampute = "дефект " + ped

            for key, value in self.amputation_level.items():
                print(key)
                if key[-3:] == "ray":
                    for detail_key, detail_value in self.ampute_detail[key[-5:]].items():
                        if value >= detail_value[0] and value <= detail_value[1]:
                            print(detail_key)
                            #if key[:-1] != "metacarp_": 
                            #    phalanx_index = 1 - round((value - detail_value[0])/(list(self.ampute_detail[key].values())[0][1]-list(self.ampute_detail[key].values())[2][0]),4)
                            #    
                            #    self.wrist_defect_detailed[key] = phalanx_index

                            #    percent += (round((value - detail_value[0])/(detail_value[1] - detail_value[0]),4)) * phalanx_weight[key] * finger_weight[key[-1]]
                            #    
                            #    if key[:-1] == "pp_" and key != "pp_1":
                            #        percent+= phalanx_weight["dp_"+key[-1]] * finger_weight[key[-1]]
                            #        percent+= phalanx_weight["mp_"+key[-1]] * finger_weight[key[-1]]
                            #    elif key[:-1] == "mp_":
                            #        percent+= phalanx_weight["dp_"+key[-1]] * finger_weight[key[-1]]
                            #    elif key== "pp_1":
                            #        percent+= phalanx_weight["dp_1"] * finger_weight["1"]
                            #elif key[:-1] == "metacarp_":
                            #    percent += 1 * finger_weight[key[-1]]
                            #    phalanx_index = 1 - round((value - detail_value[0])/(list(self.ampute_detail[key].values())[0][1]-list(self.ampute_detail[key].values())[2][0]),4)
                            #    self.wrist_defect_detailed[key] = phalanx_index
                            if detail_key == "meta_diaf" or (key[-5:] == "1_ray" and detail_key == "pp_diaf"):
                                diaf_level_text = self.diaf_level(detail_key = detail_key, key = key[-5:], value = value, detail_value = detail_value)
                                print("diaf_level_text")
                                print(diaf_level_text)
     
                            ampute += self.zone_names[key] + " на уровне " + diaf_level_text + self.os_level_name[detail_key] + ", "
                            print("ampute")
                            print(ampute)
                            diaf_level = 0
                            diaf_level_text = ""
                else:
                    ampute += "на уровне " + self.zone_names[key] + ", "

        
        self.amputation_level_text = ampute
        self.defect_percent = round(percent*100, 2)
        self.text_changed.emit()

    def diaf_level(self, detail_key, key, value, detail_value):
        diaf_level_text_new = ""

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
        
        side = ""
        axis_zone = zone + "_axis"

        axis = self.ped_axis[axis_zone]
        print(axis_zone)
        print(axis)
        
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
        self.amputation_level_point[zone] = point


        
        to_draw = self.ped_zone_detect
        ped_to_draw = to_draw.copy()
        

        to_color_zone = []
        
        
        print(zone)
        
        for point_to_draw in ped_to_draw[zone]:
            if point_to_draw[1]>= round(k_perpend*(point_to_draw[0]-point[0]) + point[1]):
                to_color_zone.append(point_to_draw)
        print(len(to_color_zone))

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