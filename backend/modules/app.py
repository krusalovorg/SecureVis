import json
import sys
import asyncio
from PyQt5.QtWidgets import QApplication, QWidget, QLabel, QVBoxLayout, QLineEdit, QPushButton
from PyQt5.QtCore import QThread, pyqtSignal

from backend.modules.video_client import video_sender


class Worker(QThread):
    finished = pyqtSignal()

    def __init__(self, apiId: str, wsUrl: str):
        super().__init__()
        self.apiId = apiId
        self.wsUrl = wsUrl

    def run(self):
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        loop.run_until_complete(video_sender(self.apiId, self.wsUrl))
        loop.close()
        self.finished.emit()

    def stop(self):
        self.is_running = False

class MyApp(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        self.label = QLabel('API ID:', self)
        self.line_edit = QLineEdit(self)

        self.label_ws = QLabel('WS Url:', self)
        self.line_edit_ws = QLineEdit(self)

        self.button = QPushButton('Подключиться к серверу', self)
        self.button.clicked.connect(self.submit)

        layout = QVBoxLayout()
        layout.addWidget(self.label)
        layout.addWidget(self.line_edit)

        layout.addWidget(self.label_ws)
        layout.addWidget(self.line_edit_ws)

        layout.addWidget(self.button)

        self.setLayout(layout)

        self.setWindowTitle('API ID Input')
        self.setGeometry(300, 300, 300, 200)
        self.show()

        self.load_data()

    def submit(self):
        apiId = self.line_edit.text()
        wsUrl = self.line_edit_ws.text()
        self.worker = Worker(apiId, wsUrl)
        self.worker.finished.connect(self.on_finished)
        self.worker.start()

        self.save_data()

    def on_finished(self):
        print('Finished')

    def save_data(self):
        data = {
            'apiId': self.line_edit.text(),
            'wsUrl': self.line_edit_ws.text()
        }
        with open('data.json', 'w') as f:
            json.dump(data, f)

    def load_data(self):
        try:
            with open('data.json', 'r') as f:
                data = json.load(f)
                self.line_edit.setText(data['apiId'])
                self.line_edit_ws.setText(data['wsUrl'])
        except FileNotFoundError:
            pass

if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = MyApp()
    sys.exit(app.exec_())
