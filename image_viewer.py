from PySide2.QtWidgets import QFileDialog, QMainWindow, QLabel
from ui.yuvviewer_window import Ui_YUVEditor
from image_config import YUVConfig
from components.customwidget import ImageView


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
        self.imageview_wins = []
        self.add_compare()

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
        self.ui.add_compare.triggered.connect(self.add_compare)
        self.ui.delcompare.triggered.connect(self.del_compare)

    def add_compare(self):
        imgviewwin = ImageView(self.ui.horizontalLayout, self)
        imgviewwin.sigUpdatePointStatusEvent.connect(self.update_point_status)
        self.imageview_wins.append(imgviewwin)

    def del_compare(self):
        imgviewwin = self.imageview_wins.pop()
        imgviewwin.Exit(self.ui.horizontalLayout)

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

    def update_point_status(self, point_status):
        self.info_bar.setText(point_status)

    def on_calc_stats(self):
        for imgviewwin in self.imageview_wins:
            imgviewwin.on_calc_stats()
