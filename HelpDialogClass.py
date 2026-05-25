from PySide6.QtWidgets import QWidget, QPushButton, QComboBox, QLineEdit, QLabel, QListWidget, QListWidgetItem, QDialog, \
    QDialogButtonBox, QMessageBox, QSlider, QVBoxLayout, QHBoxLayout, QTextEdit
import json
import os
import sys

class HelpDialog(QDialog):
    
    def __init__(self,parent=None):
        super().__init__(parent=parent)
        self.setWindowTitle("? Help")
        self.helpList = QListWidget()
        self.textList = []
        self.text = QTextEdit()
        self.text.setReadOnly(True)
        self.helpTitle = QLabel()
        self.initUI()
        self.event_handler()
        
    
    def initUI(self):
        # Basic UI elements
        QBtn = QDialogButtonBox.Ok

        self.buttonBox = QDialogButtonBox(QBtn)
        self.buttonBox.accepted.connect(self.accept)

        # Layout
        layout = QVBoxLayout()
        
        row = QHBoxLayout()
        col1 = QVBoxLayout()
        col2 = QVBoxLayout()

        col1.addWidget(QLabel("Help"))
        col1.addWidget(self.helpList)

        col2.addWidget(self.helpTitle)
        col2.addWidget(self.text)

        row.addLayout(col1)
        row.addLayout(col2)

        layout.addLayout(row)
        layout.addWidget(self.buttonBox)
        self.setLayout(layout)

        self.load_help_list()

    def load_help_list(self):
        if getattr(sys, 'frozen', False):
            file = open(file=os.path.join(sys._MEIPASS, 'data/help_dialog_subject.json'), mode='r')
        else:
            file = open('data/help_dialog_subject.json', "r")
        json_file = file.readlines()
        json_file = "".join(json_file)
        file.close()
        pyJSON_data = json.loads(json_file)
        for index in range(len(pyJSON_data["Subjects"])):
            self.helpList.addItem(pyJSON_data["Subjects"][index])
        self.textList = pyJSON_data["Explanations"]

    def event_handler(self):
        self.helpList.itemClicked.connect(self.on_subject_selected)

    def on_subject_selected(self, item : QListWidgetItem):
        index = self.helpList.indexFromItem(item).row()
        self.helpTitle.setText(self.helpList.item(index).text())
        self.text.setText(self.textList[index])