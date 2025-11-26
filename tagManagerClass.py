from PySide6.QtWidgets import QWidget, QPushButton, QComboBox, QLineEdit, QLabel, QListWidget, QListWidgetItem, QDialog, QDialogButtonBox, QMessageBox, QSlider, QVBoxLayout, QHBoxLayout
from PySide6.QtCore import Qt, QUrl, Slot, QStandardPaths
from PySide6.QtGui import QValidator
from tagClass import GoToTag, Tag
from tagSetterDialogClass import TagSetterDialog

class TagManager(QWidget):
    def __init__(self):
        super().__init__()
        self.settings()
        self.initUI()
        self.event_handler()
        self.tag_list : list[list[Tag,bool]] = []
        self.validator : QValidator
    
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
        self.btn_clearTag.clicked.connect(self.clearAllBtn)
        self.btn_deleteTag.clicked.connect(self.deleteTag)
        self.btn_modifyTag.clicked.connect(self.modifyTag)
        self.tag_list_ui.itemClicked.connect(self.update_btns)
        self.tag_list_ui.itemDoubleClicked.connect(self.onOffTag)
    
    def update_btns(self):
        self.btn_deleteTag.setEnabled(True)
        self.btn_modifyTag.setEnabled(True)
    
    def addTagDialog(self):
        dial = TagSetterDialog(self.validator)
        if dial.exec():
            new_tag = dial.tag
            self.tag_list.append([new_tag, True])
            self.tag_list_ui.addItem(new_tag.toUI())

            self.btn_clearTag.setEnabled(True)
    
    def modifyTag(self):
        index = self.tag_list_ui.currentRow()
        active_tag = self.tag_list[index]
        
        # Do Dialog to change Tag information
        dial = TagSetterDialog(self.validator, active_tag[0])
        if dial.exec():
            new_tag = dial.tag
            self.tag_list[index] = [new_tag, active_tag[1]]
            self.tag_list_ui.takeItem(index)
            self.tag_list_ui.insertItem(index, new_tag.toUI())
    
    def deleteTag(self):
        index = self.tag_list_ui.currentRow()
        self.tag_list.pop(index)
        self.tag_list_ui.takeItem(index)
        self.tag_list_ui.setCurrentRow(-1)

        self.btn_deleteTag.setDisabled(True)
        self.btn_modifyTag.setDisabled(True)
        if not self.tag_list:
            self.btn_clearTag.setDisabled(True)
    
    def clear(self):
        self.tag_list.clear()
        self.tag_list_ui.clear()

        self.btn_clearTag.setDisabled(True)
        self.btn_modifyTag.setDisabled(True)
        self.btn_deleteTag.setDisabled(True)
    
    def clearAllBtn(self):
        self.clear()
        dial = QMessageBox(text="All Tags have been removed.")  # need better understanding
        dial.exec()
    
    def enableTagManager(self, v : QValidator):
        self.validator = v
        self.btn_addTag.setEnabled(True)
        self.tag_list_ui.setEnabled(True)
    
    def onOffTag(self, item : QListWidgetItem):
        index = self.tag_list_ui.indexFromItem(item).row()
        print(index)
        self.tag_list[index][1] = not self.tag_list[index][1]
        if not self.tag_list[index][1]:
            item.setBackground(Qt.GlobalColor.red)
        else:
            item.setBackground(Qt.GlobalColor.white)

