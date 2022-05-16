from PySide2.QtCore import QSize
from PySide2.QtWidgets import QWidget
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg, NavigationToolbar2QT
import matplotlib.pyplot as plt
from matplotlib.figure import Figure


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
