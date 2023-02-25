from .download import DownloadWidget
from PyQt6.QtWidgets import QApplication
from qt_material import apply_stylesheet

import sys
app = QApplication(sys.argv)
widget = DownloadWidget(
    url="https://www.youtube.com/watch?v=dQw4w9WgXcQ",
    save_path="Rick Astley - Never Gonna Give You Up (Video).mp4",
    condition="get_highest_resolution",
    chunk_size=1024 * 2,
)
apply_stylesheet(widget, theme='dark_blue.xml')
widget.show()
sys.exit(app.exec())