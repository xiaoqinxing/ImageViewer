from sys import exit
from PySide2.QtWidgets import QApplication
from PySide2.QtCore import Qt
import components.logconfig as log
from image_viewer import ImageViewer

if __name__ == "__main__":
    QApplication.setAttribute(Qt.AA_EnableHighDpiScaling)
    apps = QApplication([])
    apps.setStyle('Fusion')
    log.clean_old_log()
    log.init_log()
    appswindow = ImageViewer()
    appswindow.show()
    exit(apps.exec_())
