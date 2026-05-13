from PySide6.QtWidgets import QWidget, QPushButton, QLineEdit, QLabel, QSlider, QVBoxLayout, QHBoxLayout, \
    QGraphicsScene, QSizePolicy
from PySide6.QtGui import QBrush, QIntValidator, QPaintEvent, QPainter, QPen, QPixmap, QColor, QResizeEvent
from PySide6.QtCore import QPoint, QSize, Qt, Slot, Signal, SignalInstance, QRect
from librosa import core as Librosa

class AudioWaveTimeline(QLabel):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.settings()
        self.painter : QPainter = QPainter()
        self.setPixmap(QPixmap(500, 100))
        self.graph_scene = None
        self.waveform_graph = None
        self.rescale_waveform_graph = None
        print(self.size().width(), self.size().height())
        self.data : dict = {}
        self.initUI()
        # self.event_handler()

    def settings(self):
        pass
        self.setMinimumSize(500,100)
        #self.setBaseSize(500,50)
        #self.setMaximumSize(500,50)

    def initUI(self):
        self.setSizePolicy(
            QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding
        )
        self.setAlignment(Qt.AlignmentFlag.AlignCenter)
        scene = self.pixmap()
        self.clear_scene(scene)
        self.setPixmap(scene)

    def event_handler(self):
        pass

    def resizeEvent(self, event: QResizeEvent):
        new_pixmap = QPixmap(self.width(), self.height())
        self.clear_scene(new_pixmap)
        if self.waveform_graph and not self.waveform_graph.isNull() and self.data != {}:
            scaled = self.waveform_graph.scaled(
                self.width(),
                self.height(),
                Qt.AspectRatioMode.IgnoreAspectRatio,
                Qt.TransformationMode.SmoothTransformation,
            )
            painter = QPainter(new_pixmap)
            x = (new_pixmap.width() - scaled.width()) // 2
            y = (new_pixmap.height() - scaled.height()) // 2
            painter.drawPixmap(x, y, scaled)
            painter.end()
        else:
            self.waveform_graph = QPixmap(500, 100)
        self.rescale_waveform_graph = new_pixmap
        self.setPixmap(new_pixmap)


    def drawWaveform(self):
        self.clear_scene(self.waveform_graph)
        self.painter.begin(self.waveform_graph)
        pen: QPen = QPen(Qt.GlobalColor.darkBlue)
        pen.setWidth(1)
        self.painter.setPen(pen)
        for pos in range(self.data["size"]):
            Xpix : int = (pos * self.waveform_graph.size().width()) / self.data["size"]
            Ypix : int = int((self.data["waveform"][pos]+1) * self.waveform_graph.size().height())//2
            self.painter.drawLine(QPoint(Xpix, Ypix), QPoint(Xpix, Ypix))
        self.painter.end()
        self.refreshGraph(self.waveform_graph)

        self.update()

    def refreshGraph(self, graph):
        scene = self.pixmap()
        self.painter.begin(scene)
        self.painter.drawPixmap(0, 0, graph)
        self.painter.end()
        self.setPixmap(scene)
        self.update()

    def updateCursor(self, time:int):
        duration : int = int(self.data["duration"]*1000)
        pix = int(time*self.rescale_waveform_graph.size().width()/duration)
        self.refreshGraph(self.rescale_waveform_graph)
        scene = self.pixmap()
        self.painter.begin(scene)
        pen: QPen = QPen(Qt.GlobalColor.red)
        self.painter.setPen(pen)
        self.painter.drawLine(QPoint(pix,0), QPoint(pix,scene.size().height()))
        self.painter.end()
        self.setPixmap(scene)

        self.update()


    def clear_scene(self, scene: QPixmap):
        scene.fill(Qt.GlobalColor.white)
        s : QSize = scene.size()
        self.painter.begin(scene)
        pen : QPen = QPen(Qt.GlobalColor.lightGray)
        self.painter.setPen(pen)
        self.painter.drawLine(QPoint(0,s.height()//2), QPoint(s.width(), s.height()//2))
        self.painter.end()
        self.update()

    def generate_waveform(self):
        pass

    def extract_waveform(self, file: str):
        file = file[1:]
        print(file)
        audio_shape, sample_rate = Librosa.load(file)
        print(len(audio_shape))
        print(sample_rate)
        self.data["waveform"] = audio_shape
        self.data["sample_rate"] = sample_rate
        self.data["size"] = len(audio_shape)
        self.data["duration"] = self.data["size"] / self.data["sample_rate"]

    
    # def paintEvent(self, event: QPaintEvent):
    #     """Override method from QWidget
    #
    #     Paint the Pixmap into the widget
    #
    #     """
    #     with QPainter(self) as painter:
    #         painter.drawPixmap(0, 0, self.graph_scene)
        
        
