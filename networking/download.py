from PyQt6.QtWidgets import QProgressBar, QPushButton, QHBoxLayout, QWidget
from PyQt6.QtCore import QThread, pyqtSignal
from PyQt6.QtSvg import QSvgRenderer
from pytube import YouTube
from requests import get


class DownloadThread(QThread):
    progress = pyqtSignal(int)

    def __init__(
            self,
            url: str,
            parent=None,
            save_path: str = None,
            condition: str = "get_highest_resolution",
            chunk_size: int = 1024,
    ):
        super().__init__(parent)
        self.url = url
        self.save_path = save_path
        self.condition = condition
        self.chunk_size = chunk_size

    def run(self):
        yt = YouTube(self.url)

        stream = getattr(yt.streams, self.condition)()  # Call the method with the name self.condition
        total_size = stream.filesize
        downloaded = 0
        video = stream.url
        r = get(video, stream=True)
        with open(self.save_path, "wb") as f:
            for chunk in r.iter_content(chunk_size=self.chunk_size):
                downloaded += len(chunk)
                f.write(chunk)
                self.progress.emit(int(downloaded / total_size * 100))


class DownloadWidget(QWidget):
    def __init__(self, parent=None, url: str = None, save_path: str = None, condition: str = "get_highest_resolution", chunk_size: int = 1024):
        super().__init__(parent)
        self.progressbar = QProgressBar()
        self.button = QPushButton("Download")
        self.button.clicked.connect(self.download)
        self.button.setIcon(QSvgRenderer("assets/ui/download_black.svg"))
        self.url = url
        self.save_path = save_path
        self.condition = condition
        self.chunk_size = chunk_size

        layout = QHBoxLayout()
        layout.addWidget(self.progressbar)
        layout.addWidget(self.button)
        self.downloading = False
        self.setLayout(layout)

    def download(self):
        if self.downloading:
            return

        self.thread = DownloadThread(
            self.url,
            self,
            self.save_path,
            self.condition,
            self.chunk_size,
        )
        self.thread.progress.connect(self.progressbar.setValue)
        self.thread.start()
        self.downloading = True
        self.button.setText("Downloading...")
        self.button.setEnabled(False)
        self.thread.finished.connect(self.finished)

    def finished(self):
        self.downloading = False
        self.button.setText("Download")
        self.button.setEnabled(True)

