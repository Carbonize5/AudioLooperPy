import os
from PySide6.QtWidgets import QApplication, QMainWindow, QWidget, QDockWidget, QPushButton, QLabel, QListWidget, QFileDialog, QSlider, QVBoxLayout, QHBoxLayout
from PySide6.QtCore import Qt, QUrl, QTimer, QTimeLine, Slot, QStandardPaths
from PySide6.QtGui import QAction
from PySide6.QtMultimedia import QMediaPlayer, QAudioOutput

class AudioPlayer(QWidget):
    def __init__(self):
        super().__init__()
        self.settings()
        self.initUI()
        self.event_handler()
        self.wasPlaying = True
    
    def settings(self):
        pass

    def initUI(self):

        #Basic UI elements
        self.btn_pause = QPushButton("Pause")
        self.btn_resume = QPushButton("Play")
        self.btn_reset = QPushButton("Reset")

        
        self.btn_pause.setDisabled(True)
        self.btn_resume.setDisabled(True)
        self.btn_reset.setDisabled(True)

        self.media_slider = QSlider(Qt.Orientation.Horizontal)
        self.media_slider.setMinimum(0)
        self.media_slider.setMaximum(100)
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

        btn_subrow.addWidget(self.btn_pause)
        btn_subrow.addWidget(self.btn_resume)
        btn_subrow.addWidget(self.btn_reset)

        self.master_layout.addLayout(row)
        self.master_layout.addLayout(btn_subrow)
        self.setLayout(self.master_layout)

    def event_handler(self):
        self.media_player.sourceChanged.connect(self.new_audio_file)
        self.media_player.positionChanged.connect(self.updateSlider)
        self.media_slider.sliderPressed.connect(self.sliderPressed)
        self.media_slider.sliderReleased.connect(self.sliderReleased)
        self.btn_resume.clicked.connect(self.play)
        self.btn_pause.clicked.connect(self.pause)
        self.btn_reset.clicked.connect(self.reset)
    
    @Slot()
    def updateSlider(self):
        self.media_slider.setValue(int(self.media_player.position()/float(self.media_player.duration())*100))
    
    @Slot()
    def sliderPressed(self):
        self.wasPlaying = self.media_player.isPlaying()
        if self.wasPlaying:
            self.media_player.stop()

    @Slot()
    def sliderReleased(self):
        self.media_player.setPosition(int(self.media_slider.value()/100.*self.media_player.duration()))
        if self.wasPlaying:
            self.media_player.play()


    @Slot()
    def new_audio_file(self):
        self.media_slider.setEnabled(True)
        self.btn_pause.setDisabled(True)
        self.btn_resume.setEnabled(True)
        self.btn_reset.setDisabled(True)
    
    @Slot()
    def play(self):
        self.media_player.play()

        self.btn_pause.setEnabled(True)
        self.btn_resume.setDisabled(True)
        self.btn_reset.setEnabled(True)
    
    @Slot()
    def pause(self):
        self.media_player.pause()

        self.btn_pause.setDisabled(True)
        self.btn_resume.setEnabled(True)
        self.btn_reset.setEnabled(True)
    
    @Slot()
    def reset(self):
        if self.media_player.isPlaying():
            self.media_player.stop()
        
        self.media_player.setPosition(0)

        self.btn_pause.setDisabled(True)
        self.btn_resume.setEnabled(True)
        self.btn_reset.setDisabled(True)

class AudioLoopApp(QMainWindow):
    def __init__(self):
        super().__init__()
        self.settings()
        self.initUI()
        self.event_handler()
    
    def settings(self):
        self.setWindowTitle("AudLoop")
        self.mime_type_filters = ["audio/mpeg", "audio/ogg", "audio/wav"]

    
    def initUI(self):
        
        # AudioLecturer
        self.audioPlayer = AudioPlayer()

        # Tag Manager


        # App Layout

        ## Menu Bar
        self.load_action = QAction(self, text="Load File")
        self.load_action.setStatusTip("Load an audio file in the player")

        self.save_state_action = QAction(self, text="Save State")
        self.save_state_action.setStatusTip("Save your work in a separate file")

        self.load_state_action = QAction(self, text="Load State")
        self.load_state_action.setStatusTip("Load your work from a separate file")

        menu = self.menuBar()
        file_menu = menu.addMenu("File")
        file_menu.addAction(self.load_action)
        file_menu.addAction(self.save_state_action)
        file_menu.addAction(self.load_state_action)

        ## Central Widget

        ## Bottom Widget
        playerWidget = QDockWidget()
        playerWidget.setWidget(self.audioPlayer)
        playerWidget.setAllowedAreas(Qt.DockWidgetArea.BottomDockWidgetArea)
        playerWidget.setFeatures(QDockWidget.DockWidgetFeature.NoDockWidgetFeatures)
        self.addDockWidget(Qt.DockWidgetArea.BottomDockWidgetArea, playerWidget)


    def event_handler(self):
        self.load_action.triggered.connect(self.load_audio_file)
        #self.save_state_action.triggered.connect()
        #self.load_state_action.triggered.connect()
    
    @Slot()
    def load_audio_file(self):

        dialog = QFileDialog(self, "Load Audio File")
        dialog.setMimeTypeFilters(self.mime_type_filters)
        dialog.setFileMode(QFileDialog.FileMode.ExistingFile)
        dialog.setAcceptMode(QFileDialog.AcceptMode.AcceptOpen)
        dialog.setDirectory(
            QStandardPaths.writableLocation(QStandardPaths.StandardLocation.PicturesLocation)
        )

        if dialog.exec() == QFileDialog.DialogCode.Accepted:
            if dialog.selectedFiles():
                self.audioPlayer.media_player.setSource(QUrl.fromLocalFile(dialog.selectedFiles()[0]))

if __name__ in "__main__":
    os.environ['QT_MEDIA_BACKEND'] = "windows"
    app = QApplication([])
    main = AudioLoopApp()
    main.show()
    app.exec()