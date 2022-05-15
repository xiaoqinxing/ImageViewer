from components.customwidget import ImageView
from components.status_code_enum import ImageToolError
from components.histview import HistView


class ImageViewWin(ImageView):
    def __init__(self, layout, parent=None):
        super().__init__(parent)
        self.hist_window = None
        layout.addWidget(self)
        self.sigUpdatePointStatusEvent.connect(self.printStr)
        self.filenameUpdateEvent.connect(self.printStr)
        self.sigRectDataEvent.connect(self.printRect)

    def printStr(self, strin):
        print(strin)

    def printRect(self, start_x, start_y, end_x, end_y):
        print('x:{} y:{} endx:{} endy:{}'.format(
            start_x, start_y, end_x, end_y))

    def __display_img(self, indexstr=''):
        try:
            self.img.display_in_scene(self.scene)
            self.filenameUpdateEvent(indexstr + self.img.imgpath)
            if self.hist_window is not None and self.hist_window.enable is True:
                self.hist_window.update_rect_data(self.img.img, self.rect)
        except ImageToolError as e:
            e.show()

    def update_stats_range(self, _, fromScenePoint, toScenePoint):
        if(toScenePoint.x() == 0 and toScenePoint.y() == 0
                and self.rect[2] > self.rect[0] and self.rect[3] > self.rect[1]):
            if self.hist_window is not None:
                self.hist_window.update_rect_data(self.img.img, self.rect)
        else:
            self.rect = [int(fromScenePoint.x()), int(fromScenePoint.y()), int(
                toScenePoint.x()), int(toScenePoint.y())]
        return

    def show_point_rgb(self, point):
        """func: 鼠标移动的回调"""
        self.x = int(point.x())
        self.y = int(point.y())
        self.__show_point_stats()

    def on_calc_stats(self):
        """打开统计信息的窗口"""
        if self.img.img is not None:
            self.hist_window = HistView(self)
            self.rect = [0, 0, self.img.img.shape[1], self.img.img.shape[0]]
            self.hist_window.update_rect_data(self.img.img, self.rect)
            self.hist_window.show()
