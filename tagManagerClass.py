from PySide6.QtWidgets import QWidget, QPushButton, QLabel, QListWidget, QListWidgetItem, QDialog, QMessageBox, QSlider, QVBoxLayout, QHBoxLayout
from PySide6.QtCore import Qt, QUrl, Slot, QStandardPaths
from tagClass import GoToTag, Tag

class TagManager(QWidget):
    def __init__(self):
        super().__init__()
        self.settings()
        self.initUI()
        self.event_handler()
        self.tag_list : list[Tag] = []
    
    def settings(self):
        pass
    
    def initUI(self):

        # Basic UI Element
        self.title = QLabel("Tag List")
        self.tag_list_ui = QListWidget()
        self.btn_addTag = QPushButton("Add Tag")
        self.btn_modifyTag = QPushButton("Modify Tag")
        self.btn_deleteTag = QPushButton("Delete Tag")
        self.btn_clearTag = QPushButton("Clear Tag List")

        self.tag_list_ui.setDisabled(True)
        self.btn_addTag.setDisabled(True)
        self.btn_clearTag.setDisabled(True)
        self.btn_deleteTag.setDisabled(True)
        self.btn_modifyTag.setDisabled(True)


        # Layout
        self.master_layout = QVBoxLayout()
        row = QHBoxLayout()
        col1 = QVBoxLayout()
        col2 = QVBoxLayout()

        row.addLayout(col1)
        row.addLayout(col2)

        col1.addWidget(self.title)
        col1.addWidget(self.tag_list_ui)

        col2.addWidget(self.btn_addTag)
        col2.addWidget(self.btn_modifyTag)
        col2.addWidget(self.btn_deleteTag)
        col2.addWidget(self.btn_clearTag)

        self.master_layout.addLayout(row)
        self.setLayout(self.master_layout)


    def event_handler(self):
        self.btn_addTag.clicked.connect(self.addTagDialog)
        self.btn_clearTag.clicked.connect(self.clearAll)
        self.btn_deleteTag.clicked.connect(self.deleteTag)
        self.tag_list_ui.itemClicked.connect(self.update_btns)
    
    def update_btns(self):
        self.btn_deleteTag.setEnabled(True)
        self.btn_modifyTag.setEnabled(True)
    
    def addTagDialog(self):
        # dial = QDialog() later maybe
        new_tag = GoToTag(0, 30)
        self.tag_list.append(new_tag)
        self.tag_list_ui.addItem(new_tag.__str__())

        self.btn_clearTag.setEnabled(True)
    
    def modifyTag(self):
        index = self.tag_list_ui.currentRow()
        active_tag = self.tag_list[index]
        
        # Do Dialog to change Tag information
    
    def deleteTag(self):
        index = self.tag_list_ui.currentRow()
        self.tag_list.pop(index)
        self.tag_list_ui.takeItem(index)
        self.tag_list_ui.setCurrentRow(-1)

        self.btn_deleteTag.setDisabled(True)
        self.btn_modifyTag.setDisabled(True)
        if not self.tag_list:
            self.btn_clearTag.setDisabled(True)
    
    def clearAll(self):
        self.tag_list.clear()
        self.tag_list_ui.clear()
        # dial = QMessageBox(text="All Tags have been removed.")  # need better understanding
        # dial.show()

        self.btn_clearTag.setDisabled(True)
        self.btn_modifyTag.setDisabled(True)
        self.btn_deleteTag.setDisabled(True)
    
    def enableTagManager(self):
        self.btn_addTag.setEnabled(True)
        self.tag_list_ui.setEnabled(True)