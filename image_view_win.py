from components.customwidget import ImageView
from components.status_code_enum import ImageToolError
from components.histview import HistView


class ImageViewWin(ImageView):
    def __init__(self, layout, parent=None):
        super().__init__(layout, parent)
        self.hist_window = None
        self.sigUpdatePointStatusEvent.connect(self.printStr)
        self.filenameUpdateEvent.connect(self.printStr)
        self.sigRectDataEvent.connect(self.printStr)

    def printStr(self, strin):
        print(strin)
