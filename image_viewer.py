from PySide2.QtWidgets import QMainWindow, QLabel
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
        self.imageview_wins = []
        self.add_compare()
        self.imageview_wins[0].isFocus = True

        self.ui.openimage.triggered.connect(self.on_open_img)
        self.ui.actionstats.triggered.connect(self.on_calc_stats)
        self.ui.nextphoto.triggered.connect(self.switch_next_photo)
        self.ui.prephoto.triggered.connect(self.switch_pre_photo)
        self.ui.rotateright.triggered.connect(self.rotate_photo)
        self.ui.yuvconfig.triggered.connect(self.config.show)  # 配置UI显示
        self.ui.add_compare.triggered.connect(self.add_compare)
        self.ui.delcompare.triggered.connect(self.del_compare)
        self.ui.saveimage.triggered.connect(self.on_save_photo)
        self.ui.deletephoto.triggered.connect(self.delete_photo)
        self.config.configUpdateEvent.connect(self.update_yuv_config)

    def add_compare(self):
        imgviewwin = ImageView(self.ui.horizontalLayout, self)
        imgviewwin.filenameUpdateEvent.connect(self.update_filename)
        imgviewwin.sigUpdatePointStatusEvent.connect(self.update_point_status)
        self.imageview_wins.append(imgviewwin)

    def update_filename(self):
        filenamelist = []
        for imgviewwin in self.imageview_wins:
            if imgviewwin.imageFileName != '':
                filenamelist.append('【' + imgviewwin.imageFileName + '】')
        self.ui.photo_title.setTitle('  VS  '.join(filenamelist))

    def update_yuv_config(self):
        for imgviewwin in self.imageview_wins:
            if imgviewwin.isFocus is False:
                continue
            imgviewwin.img.load_yuv_config(self.config.format)
            imgviewwin.reload_image()

    def del_compare(self):
        imgviewwin = self.imageview_wins.pop()
        imgviewwin.Exit(self.ui.horizontalLayout)

    def switch_next_photo(self):
        for imgviewwin in self.imageview_wins:
            if imgviewwin.isFocus is False:
                continue
            imgviewwin.switch_next_photo()

    def switch_pre_photo(self):
        for imgviewwin in self.imageview_wins:
            if imgviewwin.isFocus is False:
                continue
            imgviewwin.switch_pre_photo()

    def rotate_photo(self):
        for imgviewwin in self.imageview_wins:
            if imgviewwin.isFocus is False:
                continue
            imgviewwin.rotate_photo(True)

    def delete_photo(self):
        for imgviewwin in self.imageview_wins:
            if imgviewwin.isFocus is False:
                continue
            imgviewwin.delete_photo()

    def on_save_photo(self):
        for imgviewwin in self.imageview_wins:
            if imgviewwin.isFocus is False:
                continue
            imgviewwin.save_image()

    def on_open_img(self):
        for imgviewwin in self.imageview_wins:
            if imgviewwin.isFocus is False:
                continue
            imgviewwin.open_image()

    def update_point_status(self, point_status):
        self.info_bar.setText(point_status)

    def on_calc_stats(self):
        for imgviewwin in self.imageview_wins:
            imgviewwin.on_calc_stats()
