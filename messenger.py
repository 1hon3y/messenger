from PyQt5 import QtWidgets
import design
import requests
import time
import datetime
import threading

class MessApp(QtWidgets.QMainWindow, design.Ui_mainWindow):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.pushButton.clicked.connect(self.send)

        threading.Thread(target=self.receive).start()

    def send(self):
        username = self.lineEdit.text()
        password = self.lineEdit_2.text()
        text = self.plainTextEdit.toPlainText()

        if not username or not password or not text:
            return

        try:
            requests.post(
                'http://127.0.0.1:5000/send',
                json={"username": username, 'password': password, "text": text}
            )
        except:
            pass

        self.plainTextEdit.setPlainText('')
        self.plainTextEdit.repaint()

    def receive(self):
        last_received = 0

        while True:
            response = requests.get(
                'http://127.0.0.1:5000/messages',
                params={'after': last_received}

            )

            if response.status_code == 200:
                messages = response.json()['messages']
                for message in messages:
                    username = message['username']
                    time_1 = datetime.datetime.fromtimestamp(message['time'])
                    time_str =time_1.strftime('%H:%M:%S %d.%m.%Y')
                    text = message['text']

                    self.textBrowser.append(f'{username} {time_str}')
                    self.textBrowser.append(text)
                    self.textBrowser.append('')
                    #self.textBrowser.repaint()

                    last_received = message['time']

            time.sleep(1)


if __name__ == '__main__':
    app = QtWidgets.QApplication([])
    window = MessApp()
    window.show()
    app.exec_()
