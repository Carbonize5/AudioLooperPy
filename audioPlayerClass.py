from PySide6.QtWidgets import QWidget, QPushButton, QLabel, QSlider, QVBoxLayout, QHBoxLayout
from PySide6.QtCore import Qt, Slot
from PySide6.QtMultimedia import QMediaPlayer, QAudioOutput

class ClickableSlider(QSlider): # https://github.com/BBC-Esq/Pyside6_PyQt6_video_audio_player
    def mousePressEvent(self, event):
        if event.button() == Qt.MouseButton.LeftButton:
            value = QSlider.minimum(self) + ((QSlider.maximum(self) - QSlider.minimum(self)) * event.position().x()) / self.width()
            self.setValue(int(value))
            self.sliderPressed.emit()
            self.sliderMoved.emit(int(value))
            self.sliderReleased.emit()
        super().mousePressEvent(event)


class AudioPlayer(QWidget):
    def __init__(self):
        super().__init__()
        self.settings()
        self.initUI()
        self.event_handler()
        self.isPlaying = False
        self.isDragging = False
    
    def settings(self):
        pass

    def initUI(self):

        #Basic UI elements
        self.btn_play_n_pause = QPushButton("Play")
        self.btn_stop = QPushButton("Stop")

        self.btn_play_n_pause.setDisabled(True)
        self.btn_stop.setDisabled(True)

        self.media_slider = ClickableSlider(Qt.Orientation.Horizontal)
        self.media_slider.setMinimum(0)
        self.media_slider.setMaximum(100)
        self.media_slider.setValue(0)
        self.media_slider.setTickPosition(QSlider.TickPosition.TicksBelow)
        self.media_slider.setTickInterval(10)
        self.media_slider.setDisabled(True)

        # Specific Audio elements
        self.audio_output = QAudioOutput()
        self.media_player = QMediaPlayer()
        self.media_player.setAudioOutput(self.audio_output)

        # Layout
        self.master_layout = QVBoxLayout()
        row = QHBoxLayout()
        btn_subrow = QHBoxLayout()

        row.addWidget(self.media_slider)

        btn_subrow.addWidget(self.btn_play_n_pause)
        btn_subrow.addWidget(self.btn_stop)

        self.master_layout.addLayout(row)
        self.master_layout.addLayout(btn_subrow)
        self.setLayout(self.master_layout)

    def event_handler(self):
        self.media_player.sourceChanged.connect(self.new_audio_file)
        self.media_player.positionChanged.connect(self.updateSlider)
        self.media_player.playbackStateChanged.connect(self.isMediaEnded)
        self.media_slider.sliderPressed.connect(self.sliderPressed)
        self.media_slider.sliderReleased.connect(self.sliderReleased)
        self.btn_play_n_pause.clicked.connect(self.play_n_pause)
        self.btn_stop.clicked.connect(self.stop)
    
    @Slot()
    def updateSlider(self):
        if not self.isDragging: 
            self.media_slider.setValue(int(self.media_player.position()/float(self.media_player.duration())*100))
    
    @Slot()
    def isMediaEnded(self):
        if self.media_player.playbackState() == QMediaPlayer.PlaybackState.StoppedState:
            self.btn_stop.setDisabled(True)
            self.media_slider.setValue(0)
            self.isPlaying = False
            self.btn_play_n_pause.setText("Play")
        else:
            self.btn_stop.setEnabled(True)
        
    
    @Slot()
    def sliderPressed(self):
        #print("press the slider")
        self.isDragging = True
        if self.isPlaying:
            self.media_player.stop()

    @Slot()
    def sliderReleased(self):
        #print("release the slider")
        self.isDragging = False
        self.media_player.setPosition(int(self.media_slider.value()/100.*self.media_player.duration()))
        if self.isPlaying:
            self.media_player.play()


    @Slot()
    def new_audio_file(self):
        self.media_slider.setEnabled(True)
        self.btn_play_n_pause.setEnabled(True)
        self.btn_stop.setDisabled(True)
    
    @Slot()
    def play_n_pause(self):
        if not self.isPlaying:
            self.media_player.play()
            self.btn_play_n_pause.setText("Pause")
        else:
            self.media_player.pause()
            self.btn_play_n_pause.setText("Play")
        self.isPlaying = not self.isPlaying
        self.btn_stop.setEnabled(True)
        
    
    @Slot()
    def stop(self):
        if self.media_player.isPlaying():
            self.media_player.stop()
        
        self.media_player.setPosition(0)

        self.btn_stop.setDisabled(True)