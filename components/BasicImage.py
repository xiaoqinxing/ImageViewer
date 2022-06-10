import cv2
import numpy as np
from PySide2.QtGui import QPixmap, QImage
from os import listdir, remove
from os.path import isfile, join, getmtime, dirname, basename, isdir, splitext
from natsort import natsorted
from components.status_code_enum import *

YUV_FORMAT_MAP = {
    'NV21': cv2.COLOR_YUV2BGR_NV21,
    'NV12': cv2.COLOR_YUV2BGR_NV12,
    'YCrCb': cv2.COLOR_YCrCb2BGR,
    'YUV420': cv2.COLOR_YUV2BGR_I420,
    'YUV422': cv2.COLOR_YUV2BGR_Y422,
    'UYVY': cv2.COLOR_YUV2BGR_UYVY,
    'YUYV': cv2.COLOR_YUV2BGR_YUYV,
    'YVYU': cv2.COLOR_YUV2BGR_YVYU,
}


class YuvParam:
    """YUV图像参数"""
    height = 2160
    width = 3840
    yuv_format = 'NV21'


class ImageBasic:
    """
    基础图像组件
    具有加载图片，显示，以及基本的图像旋转等操作
    """
    img = None
    imgpath = ''  # 图片路径
    height = 0
    width = 0
    depth = 0  # 通道数
    yuv_param = YuvParam()

    def __update_attr(self):
        if (self.img is not None):
            self.height = self.img.shape[0]
            self.width = self.img.shape[1]
            self.depth = self.img.shape[2]

    def get_dir(self):
        if self.imgpath == '':
            return '.'
        return dirname(self.imgpath)

    def get_basename(self):
        if self.imgpath == '':
            return ''
        return basename(self.imgpath)

    def remove_image(self):
        self.img = None
        if isfile(self.imgpath) is False:
            return
        remove(self.imgpath)

    def load_yuv_config(self, yuv_param: YuvParam):
        self.yuv_param = yuv_param

    def load_file(self, filename):
        if isfile(filename) is False:
            raise FileNotFoundErr
        if splitext(filename)[-1] in ['.jpg', '.png', '.bmp']:
            self.__load_imagefile(filename)
        elif splitext(filename)[-1] in ['.yuv']:
            self.__load_yuvfile(filename)
        else:
            raise ImageFormatNotSupportErr

    def __load_imagefile(self, filename):
        # 防止有中文，因此不使用imread
        self.img = cv2.imdecode(np.fromfile(filename, dtype=np.uint8), 1)
        if self.img is None:
            raise ImageReadErr
        self.imgpath = filename
        self.__update_attr()

    def __load_yuvfile(self, filename):
        yuv_format = YUV_FORMAT_MAP.get(self.yuv_param.yuv_format)
        if yuv_format is None:
            raise ImageFormatNotSupportErr

        yuvdata = np.fromfile(filename, dtype=np.uint8)
        if yuvdata is None:
            raise ImageNoneErr
        if self.yuv_param.yuv_format in ['NV21', 'NV12', 'YUV420']:
            if len(yuvdata) != self.yuv_param.height * self.yuv_param.width * 3 / 2:
                raise ImageFormatErr
            yuvdata = yuvdata.reshape(
                self.yuv_param.height * 3 // 2, self.yuv_param.width)
        elif self.yuv_param.yuv_format in ['YCrCb', 'YUV422', 'UYVY', 'YUYV', 'YVYU']:
            if len(yuvdata) != self.yuv_param.height * self.yuv_param.width * 2:
                raise ImageFormatErr
            yuvdata = yuvdata.reshape(
                self.yuv_param.height * 2, self.yuv_param.width)
        else:
            raise ImageFormatNotSupportErr

        try:
            self.img = cv2.cvtColor(yuvdata, yuv_format)
        except Exception:
            raise ImageFormatErr
        self.imgpath = filename
        self.__update_attr()

    # display
    def display_in_scene(self, scene):
        """
        return: true or error string
        """
        scene.clear()
        if self.img is not None:
            # numpy转qimage的标准流程
            if len(self.img.shape) == 2:
                bytes_per_line = self.img.shape[1]
                qimg = QImage(
                    self.img, self.img.shape[1], self.img.shape[0], bytes_per_line, QImage.Format_Grayscale8)
            elif self.img.shape[2] == 3:
                bytes_per_line = 3 * self.img.shape[1]
                qimg = QImage(
                    self.img, self.img.shape[1], self.img.shape[0], bytes_per_line, QImage.Format_BGR888)
            elif self.img.shape[2] == 4:
                bytes_per_line = 4 * self.img.shape[1]
                qimg = QImage(
                    self.img, self.img.shape[1], self.img.shape[0], bytes_per_line, QImage.Format_RGBA8888)
            else:
                raise ImageFormatNotSupportErr
            scene.addPixmap(QPixmap.fromImage(qimg))
            return
        raise ImageNoneErr

    # proc
    def save_image(self, filename):
        if self.img is None:
            raise ImageNoneErr
        if isdir(dirname(filename)) is False:
            raise FilePathNotValidErr
        # 解决中文路径的问题, 不使用imwrite
        cv2.imencode('.jpg', self.img)[1].tofile(filename)

    def get_img_point(self, x, y):
        """
        获取图像中一个点的RGB值，注意颜色顺序是BGR
        """
        if(x > 0 and x < self.width and y > 0 and y < self.height):
            return self.img[y, x]
        else:
            return None

    def rotate90(self):
        """
        顺时针旋转90度
        """
        if self.img is None:
            raise ImageNoneErr
        self.img = cv2.rotate(self.img, cv2.ROTATE_90_CLOCKWISE)
        self.__update_attr()

    def find_next_time_photo(self, nextIndex):
        """
        获取下一个或者上一个图片(按照时间顺序排列)
        """
        next_photo_name = ''
        index = 0
        path = dirname(self.imgpath)
        img_name = basename(self.imgpath)
        filelist = [f for f in listdir(path) if isfile(
            join(path, f)) and f.split('.')[-1] in ["jpg", "png", "bmp", "yuv"]]
        filelist = sorted(
            filelist,  key=lambda x: getmtime(join(path, x)))
        files_nums = len(filelist)
        if img_name in filelist:
            index = filelist.index(img_name) + nextIndex
            if(index > len(filelist) - 1):
                index = 0
            elif(index < 0):
                index = len(filelist) - 1
            next_photo_name = join(path, filelist[index])
        return (next_photo_name, index, files_nums)

    def find_next_nat_photo(self, nextIndex):
        """
        获取下一个或者上一个图片(按照自然顺序排列)
        """
        next_photo_name = ''
        index = 0
        path = dirname(self.imgpath)
        img_name = basename(self.imgpath)
        filelist = [f for f in listdir(path) if isfile(
            join(path, f)) and f.split('.')[-1] in ["jpg", "png", "bmp", "yuv"]]
        natsorted(filelist)
        files_nums = len(filelist)
        if img_name in filelist:
            index = filelist.index(img_name) + nextIndex
            if(index > len(filelist) - 1):
                index = 0
            elif(index < 0):
                index = len(filelist) - 1
            next_photo_name = join(path, filelist[index])
        return (next_photo_name, index, files_nums)
