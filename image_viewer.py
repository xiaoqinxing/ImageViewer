from PySide2.QtWidgets import QFileDialog, QMainWindow, QLabel
from ui.yuvviewer_window import Ui_YUVEditor
from image_config import YUVConfig
from image_view_win import ImageViewWin


class ImageViewer(QMainWindow):
    def __init__(self):
        super().__init__()
        self.ui = Ui_YUVEditor()
        self.ui.setupUi(self)
        self.config = YUVConfig()
        self.info_bar = QLabel()
        self.ui.statusBar.addPermanentWidget(self.info_bar, stretch=8)
        # self.config.configUpdateEvent.connect(
        #     lambda: self.__init_img(self.img.imgpath))  # 配置界面参数更新

        self.imageview_wins = [ImageViewWin(self.ui.horizontalLayout, self)]

        self.ui.openimage.triggered.connect(self.on_open_img)
        # self.ui.saveimage.triggered.connect(self.save_now_image)
        self.ui.actionstats.triggered.connect(self.on_calc_stats)
        self.ui.nextphoto.triggered.connect(self.switch_next_photo)
        self.ui.prephoto.triggered.connect(self.switch_pre_photo)
        # self.imageview_wins.rubberBandChanged.connect(self.update_stats_range)
        # self.ui.deletephoto.triggered.connect(self.delete_photo)
        self.ui.rotateright.triggered.connect(self.rotate_photo)
        self.ui.yuvconfig.triggered.connect(self.config.show)  # 配置UI显示
        # self.imageview_wins[0].updatePointStatusEvent.connect(
        #     self.update_point_status)

    # def delete_photo(self):
    #     self.img.remove_image()
    #     next_photo, index, files_nums = self.img.find_next_time_photo(1)
    #     self.img_index_str = "({}/{})".format(index, files_nums - 1)
    #     self.__init_img(next_photo, self.img_index_str)

    def switch_next_photo(self):
        for imgviewwin in self.imageview_wins:
            imgviewwin.switch_next_photo()

    def switch_pre_photo(self):
        for imgviewwin in self.imageview_wins:
            imgviewwin.switch_pre_photo()

    def rotate_photo(self):
        for imgviewwin in self.imageview_wins:
            imgviewwin.rotate_photo(True)

    def on_open_img(self):
        imagepath = QFileDialog.getOpenFileName(
            None, '打开图片', '.', "Images (*.jpg *.png *.bmp *.yuv)")
        for imgviewwin in self.imageview_wins:
            imgviewwin.init_image(imagepath[0])

    # def save_now_image(self):
    #     try:
    #         imagepath = QFileDialog.getSaveFileName(
    #             None, '保存图片', self.img.get_dir(), "Images (*.jpg)")
    #         if imagepath[0] != '':
    #             self.img.save_image(imagepath[0])
    #     except ImageToolError as e:
    #         e.show()
    def update_point_status(self, point_status):
        self.info_bar.setText(point_status)

    def on_calc_stats(self):
        for imgviewwin in self.imageview_wins:
            imgviewwin.on_calc_stats()
