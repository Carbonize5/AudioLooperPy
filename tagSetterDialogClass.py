from PySide6.QtWidgets import QWidget, QPushButton, QComboBox, QLineEdit, QLabel, QListWidget, QListWidgetItem, QDialog, QDialogButtonBox, QMessageBox, QSlider, QVBoxLayout, QHBoxLayout
from PySide6.QtGui import QValidator, QIntValidator
from tagClass import Tag, GoToTag

class TagSetterDialog(QDialog):
    
    def __init__(self, validator : QValidator, tag:Tag = None):
        super().__init__()
        if tag: self.setWindowTitle("Modify Tag")
        else: self.setWindowTitle("Create Tag")
        self.validator : QIntValidator = validator
        self.tag : Tag = tag
        self.initUI()
        
    
    def initUI(self):
        # Basic UI elements
        QBtn = (
            QDialogButtonBox.Ok | QDialogButtonBox.Cancel
        )

        self.buttonBox = QDialogButtonBox(QBtn)
        self.buttonBox.accepted.connect(self.accept)
        self.buttonBox.rejected.connect(self.reject)

        self.typeLabel = QLabel("Tag type")
        self.tagTypeDropDown = QComboBox()
        self.tagTypeDropDown.addItem("Go To Tag")
        self.tagTypeDropDown.setCurrentIndex(0)

        self.positionLabel = QLabel("Tag position")
        self.editPosition = QLineEdit()
        self.editPosition.setValidator(self.validator)

        self.positionAltLabel = QLabel("Tag destination")
        self.editPositionAlt = QLineEdit()
        self.editPositionAlt.setValidator(self.validator)

        # Modify Tag
        if self.tag:
            # GoToTag case
            tag : GoToTag = self.tag
            self.editPosition.setText(tag.getPosition().__str__())
            self.editPositionAlt.setText(tag.getDestination().__str__())
        else:
            self.editPosition.setText("0")
            self.editPositionAlt.setText("0")

        # Layout
        layout = QVBoxLayout()
        
        row = QHBoxLayout()
        col1 = QVBoxLayout()
        col2 = QVBoxLayout()
        col3 = QVBoxLayout()

        row.addLayout(col1)
        row.addLayout(col2)
        row.addLayout(col3)

        col1.addWidget(self.typeLabel)
        col1.addWidget(self.tagTypeDropDown)

        col2.addWidget(self.positionLabel)
        col2.addWidget(self.editPosition)

        col3.addWidget(self.positionAltLabel)
        col3.addWidget(self.editPositionAlt)

        layout.addLayout(row)
        layout.addWidget(self.buttonBox)
        self.setLayout(layout)
    
    def accept(self):
        match self.tagTypeDropDown.currentIndex():
            case 0:
                self.tag = GoToTag(int(self.editPosition.text()), int(self.editPositionAlt.text()))
            case _:
                pass
        return super().accept()