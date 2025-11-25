import os
from PySide6.QtWidgets import QApplication, QMainWindow, QWidget, QDockWidget, QPushButton, QLabel, QFileDialog, QVBoxLayout, QHBoxLayout
from PySide6.QtCore import Qt, QUrl, QTimer, QTimeLine, Slot, QStandardPaths
from PySide6.QtGui import QAction
from audioPlayerClass import AudioPlayer
from tagManagerClass import TagManager

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
        self.tagManager = TagManager()

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
        self.setCentralWidget(self.tagManager)

        ## Bottom Widget
        playerWidget = QDockWidget()
        playerWidget.setWidget(self.audioPlayer)
        playerWidget.setAllowedAreas(Qt.DockWidgetArea.BottomDockWidgetArea)
        playerWidget.setFeatures(QDockWidget.DockWidgetFeature.NoDockWidgetFeatures)
        self.addDockWidget(Qt.DockWidgetArea.BottomDockWidgetArea, playerWidget)

        ## Side/Floating Widgets

        ### Sound Manager


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
            QStandardPaths.writableLocation(QStandardPaths.StandardLocation.MusicLocation)
        )

        if dialog.exec() == QFileDialog.DialogCode.Accepted:
            if dialog.selectedFiles():
                if self.audioPlayer.media_player.source() : self.audioPlayer.media_player.stop()
                self.audioPlayer.media_player.setSource(QUrl.fromLocalFile(dialog.selectedFiles()[0]))
                self.tagManager.enableTagManager()
                self.tagManager.clearAll()

if __name__ in "__main__":
    os.environ['QT_MEDIA_BACKEND'] = "windows"
    app = QApplication([])
    main = AudioLoopApp()
    main.show()
    app.exec()