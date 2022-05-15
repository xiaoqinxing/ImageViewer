from PySide2.QtCore import Signal, QPointF, Qt, QSize
from PySide2.QtWidgets import QWidget, QTableWidget, QTableWidgetItem, QHeaderView, QGraphicsView, QAbstractScrollArea, QLabel, QProgressBar
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg, NavigationToolbar2QT
import matplotlib.pyplot as plt
from matplotlib.figure import Figure
from PySide2.QtWidgets import QMessageBox, QGraphicsScene
from PySide2.QtGui import QPixmap, QImage
from components.BasicImage import ImageBasic
from components.status_code_enum import ImageToolError


class MplCanvas(FigureCanvasQTAgg):
    def __init__(self, parent=None, width=5, height=4, dpi=100):
        plt.rcParams['font.family'] = ['SimHei']
        plt.rcParams['axes.unicode_minus'] = False
        fig = Figure(figsize=(width, height), dpi=dpi)
        self.axes = fig.add_subplot(111)
        # self.axes.hold(False) #每次绘图时都不保留上一次绘图的结果
        super(MplCanvas, self).__init__(fig)


class MatplotlibLayout(QWidget):
    """
    自定义的matplot窗口
    """

    def __init__(self, layout):
        self.plt = MplCanvas()
        self.layout = layout
        self.mpl_ntb = NavigationToolbar2QT(self.plt, parent=None)

    def draw(self, navigationBar=True):
        self.layout.addWidget(self.plt)
        if navigationBar == True:
            self.layout.addWidget(self.mpl_ntb)

    def clean(self, navigationBar=True):
        self.layout.removeWidget(self.plt)
        if navigationBar == True:
            self.layout.removeWidget(self.mpl_ntb)
        self.plt = MplCanvas()
        self.mpl_ntb = NavigationToolbar2QT(self.plt, parent=None)

    def input(self, x, y):
        self.plt.axes.plot(x, y)

    def input_2line(self, x, y1, y2):
        self.plt.axes.plot(x, y1, color='green')
        self.plt.axes.plot(x, y2, color='red')
        self.plt.axes.fill_between(x, y1, y2, color='blue', alpha=0.25)

    def label(self, string_x, string_y, enable_grid=True):
        self.plt.axes.set_xlabel(string_x)
        self.plt.axes.set_ylabel(string_y)
        if enable_grid == True:
            self.plt.axes.grid(True)


class MatplotlibWidget(QWidget):
    """
    自定义的matplot窗口
    """

    def __init__(self, layout):
        super().__init__()
        self.layout = layout
        self.plt = MplCanvas()
        self.first_draw = 0
        self.setMinimumSize(QSize(352, 0))
        # self.mpl_ntb = NavigationToolbar2QT(self.plt, parent=None)

    def draw(self, navigationBar=True):
        self.layout.addWidget(self.plt, 1, 1, 1, 1)
        self.first_draw = 1

    def clean(self, navigationBar=True):
        if self.first_draw == 1:
            self.layout.removeWidget(self.plt)
            self.plt = MplCanvas()

    def input(self, x, y):
        self.plt.axes.plot(x, y)

    def input_2line(self, x, y1, y2):
        self.plt.axes.plot(x, y1, color='green')
        self.plt.axes.plot(x, y2, color='red')
        self.plt.axes.fill_between(x, y1, y2, color='blue', alpha=0.25)

    def input_r_hist(self, x, y):
        self.plt.axes.plot(x, y, color='red')

    def input_g_hist(self, x, y):
        self.plt.axes.plot(x, y, color='green')

    def input_b_hist(self, x, y):
        self.plt.axes.plot(x, y, color='blue')

    def input_y_hist(self, x, y):
        self.plt.axes.plot(x, y, color='black')

    def label(self, string_x, string_y, enable_grid=True):
        self.plt.axes.set_xlabel(string_x)
        self.plt.axes.set_ylabel(string_y)
        if enable_grid == True:
            self.plt.axes.grid(True)


class ImageView(QGraphicsView):
    """
    自定义的图片显示（可以获取到鼠标位置和放大比例）
    """
    img = ImageBasic()
    sigUpdatePointStatusEvent = Signal(str)  # 注意 signal不能嵌套
    filenameUpdateEvent = Signal(str)
    sigRectDataEvent = Signal(int, int, int, int)
    rect = [0, 0, 0, 0]
    sceneMousePos = QPointF()
    startRectPos = QPointF()
    endRectPos = QPointF()
    scale_ratio = 1.0
    img_index_str = ''

    def __init__(self, parent=None):
        self.scene = QGraphicsScene()
        super().__init__(self.scene, parent)
        self.setUi()

    def setUi(self):
        self.setMouseTracking(True)
        self.setAcceptDrops(True)
        self.setDragMode(QGraphicsView.ScrollHandDrag)
        self.setToolTipDuration(-1)
        self.setVerticalScrollBarPolicy(Qt.ScrollBarAsNeeded)
        self.setHorizontalScrollBarPolicy(Qt.ScrollBarAsNeeded)
        self.setSizeAdjustPolicy(
            QAbstractScrollArea.AdjustToContents)
        self.setTransformationAnchor(
            QGraphicsView.AnchorViewCenter)
        self.setResizeAnchor(QGraphicsView.AnchorViewCenter)

    def mousePressEvent(self, event):
        self.startRectPos = self.mapToScene(event.pos())
        return super().mousePressEvent(event)

    def mouseMoveEvent(self, event):
        self.sceneMousePos = self.mapToScene(event.pos())
        self.__update_point_stats()
        return super().mouseMoveEvent(event)

    def mouseReleaseEvent(self, event):
        if self.dragMode() == QGraphicsView.RubberBandDrag:
            self.endRectPos = self.mapToScene(event.pos())
            self.sigRectDataEvent.emit(
                int(self.startRectPos.x()), int(self.startRectPos.y()), int(self.endRectPos.x()), int(self.endRectPos.y()))
        return super().mouseReleaseEvent(event)

    def wheelEvent(self, event):
        angle = event.angleD.y()
        self.sceneMousePos = self.mapToScene(event.pos())
        self.centerOn(self.sceneMousePos)
        if (angle > 0):
            self.scale(1.25, 1.25)
            self.scale_ratio *= 1.25
        else:
            self.scale(0.8, 0.8)
            self.scale_ratio *= 0.8
        self.__update_point_stats()
        return super().wheelEvent(event)

    def dragEnterEvent(self, event):
        if event.mimeData().hasUrls():
            urls = event.mimeData().urls()
            filename = urls[-1].path()[1:]
            self.init_image(filename)
        event.accept()

    def __update_point_stats(self):
        if self.img.img is not None:
            int_x = int(self.sceneMousePos.x())
            int_y = int(self.sceneMousePos.y())
            rgb = self.img.get_img_point(int_x, int_y)
            if rgb is not None:
                scale_ratio = int(self.scale_ratio * 100)
                self.sigUpdatePointStatusEvent.emit("x:{},y:{} : R:{} G:{} B:{} 缩放比例:{}%".format(
                    int_x, int_y, rgb[2], rgb[1], rgb[0], scale_ratio))

    def display(self):
        try:
            if self.img.img is not None:
                self.img.display_in_scene(self.scene)
                self.filenameUpdateEvent.emit(
                    self.img_index_str + self.img.get_basename())
                if self.dragMode() == QGraphicsView.RubberBandDrag:
                    self.sigRectDataEvent.emit(
                        int(self.startRectPos.x()), int(self.startRectPos.y()), int(self.endRectPos.x()), int(self.endRectPos.y()))
        except ImageToolError as err:
            err.show()

    def init_image(self, filename):
        try:
            # self.img.load_yuv_config(
            #     self.config.width, self.config.height, self.config.yuv_format)
            self.img.load_file(filename)
            _, index, files_nums = self.img.find_next_time_photo(0)
            self.img_index_str = "({}/{})".format(index + 1, files_nums)
            self.display()
        except ImageToolError as err:
            err.show()

    def rotate_photo(self, need_saveimg_in_rotate):
        try:
            self.img.rotate90()
            self.display()
            if need_saveimg_in_rotate is True:
                self.img.save_image(self.img.imgpath)
        except ImageToolError as err:
            err.show()

    def delete_photo(self):
        self.img.remove_image()
        next_photo, index, files_nums = self.img.find_next_time_photo(1)
        self.img_index_str = "({}/{})".format(index, files_nums - 1)
        self.init_image(next_photo)

    def switch_next_photo(self):
        next_photo, index, files_nums = self.img.find_next_time_photo(1)
        self.img_index_str = "({}/{})".format(index + 1, files_nums)
        self.init_image(next_photo)

    def switch_pre_photo(self):
        pre_photo, index, files_nums = self.img.find_next_time_photo(-1)
        self.img_index_str = "({}/{})".format(index + 1, files_nums)
        self.init_image(pre_photo)


class VideoView(QLabel):
    sigDragEvent = Signal(str)

    def __init__(self, parent=None):
        super().__init__(parent)
        self.setAcceptDrops(True)

    def dragEnterEvent(self, event):
        event.accept()

    def dragMoveEvent(self, event):
        event.accept()

    def dropEvent(self, event):
        if event.mimeData().hasUrls():
            try:
                for url in event.mimeData().urls():
                    self.sigDragEvent.emit(url.path()[1:])
            except Exception as e:
                print(e)


def critical_win(string: str, parent=None):
    if(string is not None):
        QMessageBox.critical(
            parent, '警告', string, QMessageBox.Yes, QMessageBox.Yes)
    return


def info_win(string: str, parent=None):
    if(string is not None):
        QMessageBox.information(
            parent, '提示', string, QMessageBox.Yes, QMessageBox.Yes)
    return
