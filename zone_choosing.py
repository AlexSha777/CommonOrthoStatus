import sys
from PyQt5.QtWidgets import QApplication, QWidget, QScrollArea, QHBoxLayout, QVBoxLayout, QDesktopWidget, QPushButton

from PyQt5.QtGui import   QPainter ,QPixmap, QImage, QColor
from PyQt5.QtCore import Qt , QPoint

from front_zones import front_zones
from back_zones import back_zones
from back_zones_detect import back_zones_detect
from front_zones_detect import front_zones_detect


front_zones_dict = front_zones_detect.copy()

#front_zones_names_dict = load_obj_zone_names()

back_zones_dict = back_zones_detect.copy()
#back_zones_names_dict = load_obj_backzone_names()

#file_name = "front_clear.bmp"




class Winform(QWidget):
    def __init__(self, file_name, soft_tissue_zones={}, parent=None):
        super(Winform,self).__init__(parent)
        self.file_name = file_name
        self.setWindowTitle ("Пример рисования")
        self.pix = QPixmap() # создать экземпляр объекта QPixmap
        #self.lastPoint = QPoint () # начальная точка
        #self.endPoint = QPoint () # конечная точка
        self.soft_tissue_zones = soft_tissue_zones
        self.initUi()

    def initUi(self):
        
        self.soft_tissue_colors = {
        "algia": "#B5B5B5",
        "edema": "#FFC7AC",
        "hyperemia": "#FF9999",
        "wound": "#FF0700",
        "abrasion": "#B63D3D", # DE5353
        "bruise":"#B75EAF",
        "pustule": "#FFB140",
        "scar": "#FFD37A",
        "tumor": "#93BF85"
        }




        self.pix = QPixmap(self.file_name)

        
        self.resize(self.pix.width(), self.pix.height())
        self.setMouseTracking(True)
        
        self.front_zones_dict = front_zones_dict
        self.body_coord = []
        
        for k, v in self.front_zones_dict.items():
            #print(k)
            for i in v:
                self.body_coord.append(i)
        

        self.back_zones_dict = back_zones_dict
        self.back_body_coord = []
        
        for k, v in self.back_zones_dict.items():
            #print(k)
            for i in v:
                self.back_body_coord.append(i)
        

        self.checked_zones = []
        self.picture_proccessing(self.file_name)


    def picture_proccessing(self, file_name):
        updated_image = self.pix.toImage()
        source_dict = 0
        if self.soft_tissue_zones != {
                            "edema": [],
                            "algia": [],
                            "hyperemia": [],
                            "wound": [],
                            "abrasion": [],
                            "bruise": [],
                            "pustule": [],
                            "scar": [],
                            "tumor": [],
                            }:
            dict_soft_tissue = {}
            for key,values in self.soft_tissue_zones.items():
                for val in values:
                    if isinstance(val, list):
                        for val_item in val:
                            if val_item not in dict_soft_tissue.keys():
                                dict_soft_tissue[val_item] = [key]
                            else:
                                dict_soft_tissue[val_item].append(key)
                    else:
                        if val not in dict_soft_tissue.keys():
                                dict_soft_tissue[val] = [key]
                        else:
                            dict_soft_tissue[val].append(key)

            print(dict_soft_tissue)
            if file_name == "front_clear.bmp":
                zones_names = front_zones
                source_dict = self.front_zones_dict
            else:
                zones_names = back_zones
                source_dict = self.back_zones_dict
            
            for key, values in dict_soft_tissue.items():
                
                color_values = []
                for val in values:
                    color_values.append(self.soft_tissue_colors[val])

                if key in zones_names:
                    if len(values)>1:
                        min_iter = 0
                        max_iter = 0
                        increm = 0
                        for x in source_dict[key]:
                            if increm ==0:
                                min_iter = x[0]
                                max_iter =  x[0]
                            else:
                                if x[0]<min_iter:
                                    min_iter = x[0]
                                elif x[0]>max_iter:
                                    max_iter =  x[0]
                            increm +=1
                        print(min_iter)
                        print(max_iter)
                        zone_width = max_iter-min_iter
                        diap_width = int(zone_width/len(values))
                        diap_1 = [min_iter, min_iter+diap_width]
                        diapazones = []
                        diapazones.append(diap_1)

                        increm = 2
                        for i in range(len(values)-1):
                            if increm != len(values):
                                diap_edit = diapazones[-1][:]
                                diap_edit[0] = diap_edit[1]+1
                                diap_edit[1] = diap_edit[1]+diap_width
                                diapazones.append(diap_edit)
                            else:
                                diap_edit = diapazones[-1][:]
                                diap_edit[0] = diap_edit[1]+1
                                diap_edit[1] = max_iter
                                diapazones.append(diap_edit)
                            increm+=1

                        print(diapazones)
                        for x in source_dict[key]:
                            index = 0
                            for diap in diapazones:
                                if x[0] >= diap[0] and x[0]<=diap[1]:
                                    color = QColor(color_values[index])
                                    QImage.setPixelColor(updated_image, x[0], x[1], color)
                                else:
                                    index+=1




                    elif len(values)==1:
                        color = QColor(color_values[0])
                        for x in source_dict[key]:
                            QImage.setPixelColor(updated_image, x[0], x[1], color)

            self.pix = QPixmap.fromImage(updated_image)
            
            self.update()



    def get_checked_zones(self):
        print(self.checked_zones)
        return self.checked_zones
        

    
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
            if self.file_name == "front_clear.bmp":
                for k, v in self.front_zones_dict.items():
                    for i in v:
                        if position == i:
                            print(k)
                            print(self.file_name)
                            self.change_color(k, self.file_name)
                            #print(front_zones_names_dict[k])
            else:
                for k, v in self.back_zones_dict.items():
                    for i in v:
                        if position == i:
                            print(k)
                            print(self.file_name)
                            self.change_color(k, self.file_name)
                            #print(back_zones_names_dict[k])
    
    def change_color(self, k, file_name):

        zone_name = k
        updated_image = self.pix.toImage()
        source_dict = 0
        if file_name == "front_clear.bmp":
            source_dict = self.front_zones_dict
        else:
            source_dict = self.back_zones_dict

        if k in self.checked_zones:
            color = QColor(255, 255, 255)
            self.checked_zones.remove(k)
        else:
            color = QColor("#68DADA")
            #color = QColor(255, 99, 71)
            self.checked_zones.append(k)

        for x in source_dict[zone_name]:
            QImage.setPixelColor(updated_image, x[0], x[1], color)

        self.pix = QPixmap.fromImage(updated_image)
        
        self.update()
        print(self.checked_zones)
        
    def picture_clear(self):
        source_dict = 0
        updated_image = self.pix.toImage()
        if self.file_name == "front_clear.bmp":
            source_dict = self.front_zones_dict
        else:
            source_dict = self.back_zones_dict
        color = QColor(255, 255, 255)
        for i in self.checked_zones:
            for x in source_dict[i]:
                QImage.setPixelColor(updated_image, x[0], x[1], color)
            self.pix = QPixmap.fromImage(updated_image)
            self.update()
        self.checked_zones = []
        self.update()

        



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
        self.widget = Winform(self.file_name)
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
        

        footer.addWidget(self.okButton)
        footer.addWidget(self.cancelButton)
        main = QVBoxLayout(self)
        main.addLayout(hbox)
        main.addLayout(footer)

        sizeObject = QDesktopWidget().screenGeometry(-1)
        self.resize((self.widget.width()+40), (sizeObject.height()-90))
        
    def sendInfo(self):
        print (self.widget.get_checked_zones())
        #return
			
if __name__ == "__main__":
    app = QApplication(sys.argv)
    file_name = "front_clear.bmp"
    form = ScrollOnPicture(file_name)
    form.show()
    sys.exit(app.exec_())