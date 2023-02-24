from PyQt6.QtWidgets import QProgressBar, QPushButton, QVBoxLayout, QWidget
from PyQt6.QtCore import QThread, pyqtSignal
from PyQt6.QtWidgets import QApplication
from pytube import YouTube
from requests import get
from pytube import Playlist
from dataclasses import dataclass

class DownloadThread(QThread):
    progress = pyqtSignal(int)

    def __init__(self, url: str, parent=None):
        super().__init__(parent)
        self.url = url


    def run(self):
        print("Downloading", self.url)
        yt = YouTube(self.url)
        stream = yt.streams.get_highest_resolution()
        total_size = stream.filesize
        downloaded = 0
        video = stream.url
        r = get(video, stream=True)
        with open("video.mp4", "wb") as f:
            for chunk in r.iter_content(chunk_size=1024 * 1024):
                downloaded += len(chunk)
                f.write(chunk)
                self.progress.emit(int(downloaded / total_size * 100))
        print("Downloaded", self.url)


class DownloadWidget(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.progressbar = QProgressBar()
        self.button = QPushButton("Download")
        self.button.clicked.connect(self.download)
        layout = QVBoxLayout()
        layout.addWidget(self.progressbar)
        layout.addWidget(self.button)
        self.setLayout(layout)

    def download(self):
        self.thread = DownloadThread("https://www.youtube.com/watch?v=9bZkp7q19f0")
        self.thread.progress.connect(self.progressbar.setValue)
        self.thread.start()


if __name__ == "__main__":
    import sys
    app = QApplication(sys.argv)
    widget = DownloadWidget()
    widget.show()
    sys.exit(app.exec())