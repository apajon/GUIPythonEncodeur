# Copyright (c) 2021 Adrien Pajon (adrien.pajon@gmail.com)
# 
# This software is released under the MIT License.
# https://opensource.org/licenses/MIT

from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg
from matplotlib.figure import Figure

class MplCanvas(FigureCanvasQTAgg):

    def __init__(self, parent=None, width=5, height=4, dpi=100):
        fig = Figure(figsize=(width, height), dpi=dpi)
        self.axes = fig.add_subplot(111)
        super(MplCanvas, self).__init__(fig)

    def replaceFig(self,fig=None):
        super(MplCanvas, self).__init__(fig)