import os
from sys import platform
import pprint
from PySide6.QtWidgets import QApplication
from audioLooperApp import AudioLoopApp

if __name__ in "__main__":
    #pprint.pprint(dict(os.environ), width=1)
    if platform=="linux":
        os.environ['QT_MEDIA_BACKEND'] = "ffmpeg"
    elif platform == "darwin":
        os.environ['QT_MEDIA_BACKEND'] = "darwin"
    elif platform == "win32":
        os.environ['QT_MEDIA_BACKEND'] = "windows"
    app = QApplication([])
    main = AudioLoopApp()
    main.show()
    app.exec()