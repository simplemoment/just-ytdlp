import http.client
import sys
from PyQt6.QtCore import Qt, QThread, pyqtSignal
from PyQt6.QtWidgets import QApplication, QWidget, QVBoxLayout, QPushButton, QProgressBar, QLineEdit, QLabel
from yt_dlp import YoutubeDL
from tqdm import tqdm


class DownloadThread(QThread):
    progress_signal = pyqtSignal(int)
    complete_signal = pyqtSignal(str)

    def __init__(self, url, parent=None):
        super().__init__(parent)
        self.url = url

    def run(self):
        try:
            ydl_opts = {
                'format': 'best',
                'outtmpl': 'downloads/%(title)s.%(ext)s',
            }

            with YoutubeDL(ydl_opts) as ydl:
                ydl.download([self.url])
            self.complete_signal.emit("finish")
        except Exception as e:
            self.complete_signal.emit(f"Error: {str(e)}")


class YouTubeDownloaderApp(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("YouTubeVideoDownload")
        self.setGeometry(300, 300, 400, 200)

        self.layout = QVBoxLayout()

        self.url_label = QLabel("video url, like a 'https://youtu.be/qwerty01234' or 'https://youtube.com/watch?v=abcdf01234'")
        self.layout.addWidget(self.url_label)

        self.url_input = QLineEdit(self)
        self.layout.addWidget(self.url_input)

        self.download_button = QPushButton("download", self)
        self.download_button.clicked.connect(self.start_download)
        self.layout.addWidget(self.download_button)

        self.progress_bar = QProgressBar(self)
        self.progress_bar.setRange(0, 100)
        self.layout.addWidget(self.progress_bar)

        self.status_label = QLabel("-")
        self.layout.addWidget(self.status_label)

        self.setLayout(self.layout)

    def start_download(self):
        url = self.url_input.text()
        if not url:
            self.status_label.setText("Invalid url.")
            return

        # Starting thread for stream (download)
        self.status_label.setText("loading")
        self.download_thread = DownloadThread(url)
        self.download_thread.progress_signal.connect(self.update_progress)
        self.download_thread.complete_signal.connect(self.on_complete)
        self.download_thread.start()

    def update_progress(self, progress):
        self.status_label.setValue(progress)

    def on_complete(self, message):
        self.status_label.setText(message)
        self.progress_bar.setValue(100)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = YouTubeDownloaderApp()
    window.show()
    sys.exit(app.exec())