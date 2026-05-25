from PySide6.QtWidgets import QWidget, QPushButton, QComboBox, QLineEdit, QLabel, QListWidget, QListWidgetItem, QDialog, \
    QDialogButtonBox, QMessageBox, QSlider, QVBoxLayout, QHBoxLayout, QTextEdit
from PySide6.QtGui import QValidator, QIntValidator
from tagClass import Tag, GoToTag

class AboutDialog(QDialog):
    
    def __init__(self, parent=None):
        super().__init__(parent=parent)
        self.setWindowTitle("About")
        self.text = QTextEdit()
        self.text.setReadOnly(True)
        self.initUI()
        
    
    def initUI(self):
        # Basic UI elements
        QBtn = QDialogButtonBox.Ok

        self.buttonBox = QDialogButtonBox(QBtn)
        self.buttonBox.accepted.connect(self.accept)

        # Layout
        layout = QVBoxLayout()

        layout.addWidget(self.text)

        layout.addWidget(self.buttonBox)
        self.setLayout(layout)
