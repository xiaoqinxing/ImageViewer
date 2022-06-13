from PySide2.QtCore import Signal, QPointF, Qt
from PySide2.QtWidgets import QGraphicsView, QAbstractScrollArea, QLabel, QFileDialog
from PySide2.QtWidgets import QMessageBox, QGraphicsScene
from components.BasicImage import ImageBasic
from components.status_code_enum import ImageToolError
from components.histview import HistView


class ImageView(QGraphicsView):
    """
    自定义的图片显示（可以获取到鼠标位置和放大比例）
    """
    img = ImageBasic()
    sigUpdatePointStatusEvent = Signal(str)  # 注意 signal不能嵌套
    filenameUpdateEvent = Signal()
    sigRectDataEvent = Signal(list)
    rect = [0, 0, 0, 0]
    sceneMousePos = QPointF()
    startRectPos = QPointF()
    endRectPos = QPointF()
    scale_ratio = 1.0
    img_index_str = ''
    hist_window = None
    imageFileName = ''
    isFocus = False

    def __init__(self, layout, parent=None):
        self.scene = QGraphicsScene()
        super().__init__(self.scene, parent)
        self.setUi()
        layout.addWidget(self)

    def Exit(self, layout):
        layout.removeWidget(self)
        self.setParent(None)

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
        self.setFocusPolicy(Qt.ClickFocus)

    def focusInEvent(self, QFocusEvent):
        self.isFocus = True
        return super().focusInEvent(QFocusEvent)

    def focusOutEvent(self, QFocusEvent):
        self.isFocus = False
        return super().focusOutEvent(QFocusEvent)

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
            self.rect = [int(self.startRectPos.x()), int(self.startRectPos.y()), int(
                self.endRectPos.x()), int(self.endRectPos.y())]
            self.sigRectDataEvent.emit(self.rect)
            if self.img.img is not None and self.hist_window is not None and self.hist_window.enable is True:
                self.hist_window.update_rect_data(self.img.img, self.rect)
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
        event.accept()

    def dragMoveEvent(self, event):
        event.accept()

    def dropEvent(self, event):
        if event.mimeData().hasUrls():
            urls = event.mimeData().urls()
            filename = urls[-1].path()[1:]
            self.init_image(filename)
        return super().dropEvent(event)

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
                self.imageFileName = self.img_index_str + self.img.get_basename()
                self.filenameUpdateEvent.emit()
                if self.dragMode() == QGraphicsView.RubberBandDrag:
                    self.sigRectDataEvent.emit(self.rect)
                if self.hist_window is not None and self.hist_window.enable is True:
                    self.hist_window.update_rect_data(self.img.img, self.rect)
        except ImageToolError as err:
            err.show()

    def init_image(self, filename):
        try:
            self.img.load_file(filename)
            _, index, files_nums = self.img.find_next_time_photo(0)
            self.img_index_str = "({}/{})".format(index + 1, files_nums)
            self.display()
        except ImageToolError as err:
            err.show()

    def open_image(self):
        try:
            imagepath = QFileDialog.getOpenFileName(
                None, '打开图片', self.img.get_dir(), "Images (*.jpg *.png *.bmp *.yuv)")
            if imagepath[0] != '':
                self.init_image(imagepath[0])
        except ImageToolError as err:
            err.show()

    def save_image(self):
        try:
            imagepath = QFileDialog.getSaveFileName(
                None, '保存图片', self.img.get_dir(), "JPEG Images (*.jpg);;PNG Images (*.png)")
            if imagepath[0] != '':
                self.img.save_image(imagepath[0])
        except ImageToolError as err:
            err.show()

    def reload_image(self):
        if self.img.img is not None:
            self.init_image(self.img.imgpath)

    def rotate_photo(self, need_saveimg_in_rotate):
        try:
            self.img.rotate90()
            self.display()
            if need_saveimg_in_rotate is True:
                self.img.save_image(self.img.imgpath)
        except ImageToolError as err:
            err.show()

    def delete_photo(self):
        next_photo, index, files_nums = self.img.find_next_time_photo(1)
        self.img_index_str = "({}/{})".format(index, files_nums - 1)
        self.img.remove_image()
        self.init_image(next_photo)

    def switch_next_photo(self):
        next_photo, index, files_nums = self.img.find_next_time_photo(1)
        self.img_index_str = "({}/{})".format(index + 1, files_nums)
        self.init_image(next_photo)

    def switch_pre_photo(self):
        pre_photo, index, files_nums = self.img.find_next_time_photo(-1)
        self.img_index_str = "({}/{})".format(index + 1, files_nums)
        self.init_image(pre_photo)

    def on_calc_stats(self):
        """打开统计信息的窗口"""
        if self.img.img is not None:
            self.hist_window = HistView(self)
            self.rect = [0, 0, self.img.width, self.img.height]
            self.hist_window.update_rect_data(self.img.img, self.rect)
            self.hist_window.show()


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
