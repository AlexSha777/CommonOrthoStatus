import sys
from PyQt5.QtWidgets import QApplication

from zone_choosing import ScrollOnPicture

if __name__ == "__main__":
    app = QApplication(sys.argv)
    file_name = "back_clear.bmp"
    form = ScrollOnPicture(file_name)
    form.show()
    sys.exit(app.exec_())