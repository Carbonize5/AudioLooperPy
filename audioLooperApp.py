import os
from PySide6.QtWidgets import QApplication, QMainWindow, QWidget, QDockWidget, QPushButton, QLabel, QFileDialog, QVBoxLayout, QHBoxLayout
from PySide6.QtCore import Qt, QUrl, QTimer, QTimeLine, Slot, QStandardPaths
from PySide6.QtGui import QAction
from audioPlayerClass import AudioPlayer
from tagManagerClass import TagManager
from tagClass import Tag, GoToTag
import json

class AudioLoopApp(QMainWindow):
    def __init__(self):
        super().__init__()
        self.settings()
        self.initUI()
        self.event_handler()
        self.lastTick : int = 0
    
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
        self.save_state_action.setDisabled(True)

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
        self.audioPlayer.media_player.positionChanged.connect(self.positionChecker)
        self.save_state_action.triggered.connect(self.onSave)
        self.load_state_action.triggered.connect(self.onLoad)
    
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
                self.audioPlayer.media_player.durationChanged.connect(self.setupTagManager)
    
    def setupTagManager(self):
        self.save_state_action.setEnabled(True)
        self.tagManager.enableTagManager(self.audioPlayer.onlyTicks)
        self.tagManager.clear()
        self.audioPlayer.media_player.durationChanged.disconnect(self.setupTagManager)

    def positionChecker(self):
        tick = self.audioPlayer.media_player.position()
        for tag in self.tagManager.tag_list:
            if tag[1] and self.audioPlayer.isPlaying and not self.audioPlayer.isDragging and self.lastTick <= tag[0].position <= tick:
                # print(self.lastTick, tag[0].position, tick)
                tag[0].useTag(self.audioPlayer.media_player)
                break
        self.lastTick = tick
    
    def onSave(self):
        source : QUrl = self.audioPlayer.media_player.source()
        tag_list : list[list[Tag, bool]] = self.tagManager.tag_list
        json_tag_list : list[list[dict, bool]] = []
        for tag_duo in tag_list:
            tag = tag_duo[0].toPyJSON()
            json_tag_list.append([tag, tag_duo[1]])
        pre_json_file : dict = dict()
        pre_json_file["source"] = source.toString()
        pre_json_file["tag_list"] = json_tag_list
        json_file = json.dumps(pre_json_file)

        dialog = QFileDialog(self, "Save File")
        dialog.setMimeTypeFilters(["application/json"])
        dialog.setFileMode(QFileDialog.FileMode.AnyFile)
        dialog.setAcceptMode(QFileDialog.AcceptMode.AcceptSave)
        dialog.setDefaultSuffix("json")
        dialog.setDirectory(
            QStandardPaths.writableLocation(QStandardPaths.StandardLocation.DocumentsLocation)
        )

        if dialog.exec() == QFileDialog.DialogCode.Accepted:
            if dialog.selectedFiles():
                file = open(dialog.selectedFiles()[0],'w')
                file.write(json_file)
                file.close()

    def onLoad(self):
        dialog = QFileDialog(self, "Load File")
        dialog.setMimeTypeFilters(["application/json"])
        dialog.setFileMode(QFileDialog.FileMode.ExistingFile)
        dialog.setAcceptMode(QFileDialog.AcceptMode.AcceptOpen)
        dialog.setDefaultSuffix("json")
        dialog.setDirectory(
            QStandardPaths.writableLocation(QStandardPaths.StandardLocation.DocumentsLocation)
        )

        if dialog.exec() == QFileDialog.DialogCode.Accepted:
            if dialog.selectedFiles():
                file = open(dialog.selectedFiles()[0], "r")
                json_file = file.readlines()
                json_file = "".join(json_file)
                file.close()

                self.tagManager.clear()
                setup = lambda : (self.save_state_action.setEnabled(True),
                                self.tagManager.enableTagManager(self.audioPlayer.onlyTicks),
                                self.audioPlayer.media_player.durationChanged.disconnect(setup))
                self.audioPlayer.media_player.durationChanged.connect(setup)
                pyJSON_data = json.loads(json_file)
                self.audioPlayer.media_player.setSource(QUrl(pyJSON_data["source"]))

                tag_list = []
                index = 0
                for tag_duo in pyJSON_data["tag_list"]:
                    match tag_duo[0]["Type"]:
                        case 0:
                            tag = Tag(tag_duo[0]["Args"][0])
                        case 1:
                            tag = GoToTag(tag_duo[0]["Args"][0], tag_duo[0]["Args"][1])
                        case _:
                            print("Oopsie Daisie")
                            raise ValueError
                    tag_list.append([tag, tag_duo[1]])
                    self.tagManager.tag_list_ui.addItem(tag.toUI())
                    if not tag_duo[1]:
                        self.tagManager.tag_list_ui.item(index).setBackground(Qt.GlobalColor.red)
                    index+=1

                if tag_list:
                    self.tagManager.tag_list = tag_list
                    self.tagManager.btn_clearTag.setEnabled(True)
                



if __name__ in "__main__":
    os.environ['QT_MEDIA_BACKEND'] = "windows"
    app = QApplication([])
    main = AudioLoopApp()
    main.show()
    app.exec()