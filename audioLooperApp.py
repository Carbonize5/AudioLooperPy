import os
from PySide6.QtWidgets import QApplication, QMainWindow, QWidget, QDockWidget, QPushButton, QLabel, QListWidget, QFileDialog, QSlider, QVBoxLayout, QHBoxLayout
from PySide6.QtCore import Qt, QUrl, QTimer, QTimeLine
from PySide6.QtMultimedia import QMediaPlayer, QAudioOutput

class AudioLecturer(QWidget):
    def __init__(self):
        super().__init__()
        self.settings()
        self.initUI()
        self.event_handler()
    
    def settings(self):
        pass

    def initUI(self):

        #Basic UI elements
        self.btn_play = QPushButton("Play")
        self.btn_pause = QPushButton("Pause")
        self.btn_resume = QPushButton("Resume")
        self.btn_reset = QPushButton("Reset")

        
        self.btn_pause.setDisabled(True)
        self.btn_resume.setDisabled(True)
        self.btn_play.setDisabled(True)
        self.btn_reset.setDisabled(True)

        self.media_slider = QSlider(Qt.Orientation.Horizontal)
        self.media_slider.setMinimum(0)
        self.media_slider.setValue(0)
        self.media_slider.setTickPosition(QSlider.TickPosition.TicksBelow)
        self.media_slider.setTickInterval(10)
        self.media_slider.setDisabled(True)

        # Specific Audio UI elements
        self.audio_output = QAudioOutput()
        self.media_player = QMediaPlayer()
        self.media_player.setAudioOutput(self.audio_output)

        # Layout
        self.master_layout = QVBoxLayout()
        row = QHBoxLayout()
        btn_subrow = QHBoxLayout()

        row.addWidget(self.media_slider)

        btn_subrow.addWidget(self.btn_play)
        btn_subrow.addWidget(self.btn_pause)
        btn_subrow.addWidget(self.btn_resume)
        btn_subrow.addWidget(self.btn_reset)

        self.master_layout.addLayout(row)
        self.master_layout.addLayout(btn_subrow)
        self.setLayout(self.master_layout)

    def event_handler(self):
        pass

class AudioLoopApp(QMainWindow):
    def __init__(self):
        super().__init__()
        self.settings()
        self.initUI()
        self.event_handler()
    
    def settings(self):
        self.setWindowTitle("AudLoop")
        pass

    
    def initUI(self):
        
        # AudioLecturer
        self.audioLecturer = AudioLecturer()

        # Layout
        lecturerWidget = QDockWidget()
        lecturerWidget.setWidget(self.audioLecturer)
        lecturerWidget.setAllowedAreas(Qt.DockWidgetArea.BottomDockWidgetArea)
        lecturerWidget.setFeatures(QDockWidget.DockWidgetFeature.NoDockWidgetFeatures)
        self.addDockWidget(Qt.DockWidgetArea.BottomDockWidgetArea, lecturerWidget)


    def event_handler(self):
        pass

if __name__ in "__main__":
    app = QApplication([])
    main = AudioLoopApp()
    main.show()
    app.exec()