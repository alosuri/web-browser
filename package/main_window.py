from PySide6.QtWidgets import QApplication, QPushButton, QMainWindow, QVBoxLayout, QHBoxLayout, QWidget, QLineEdit, QLabel, QTextEdit
from PySide6.QtCore import Qt, QSize
from PySide6.QtGui import QPalette, QColor
from url import URL, load

import sys

class MainWindow(QMainWindow):
    def __init__(self) -> None:
        super().__init__()

        self.setWindowTitle("Web Browser")
        self.result = QTextEdit("Seach something or idk")
        self.result.setReadOnly(True)
        

        layout = QVBoxLayout()
        layout.addWidget(NavigationBar(self))
        layout.addWidget(self.result)

        layout.setStretch(0,0)
        layout.setStretch(1,1)

        widget = QWidget()
        widget.setLayout(layout)
        self.setFixedSize(QSize(1280, 720))
        self.setCentralWidget(widget)

    def updateWebsite(self, text: str) -> None:
        self.result.setText(f"URL: {text}")


class NavigationBar(QWidget):
    def __init__(self, main_window: MainWindow) -> None:
        super().__init__()

        self.main_window = main_window

        self.search_bar = QLineEdit(placeholderText="Type here...")
        self.search_button = QPushButton("Search")
        self.search_button.clicked.connect(lambda: self.searchValue())

        self.hbox = QHBoxLayout()
        self.hbox.addWidget(self.search_bar)
        self.hbox.addWidget(self.search_button)
        self.setLayout(self.hbox)

    def searchValue(self) -> str:
        url = self.search_bar.text()
        try:
            result = load(URL(url))
        except:
            print("Something went wrong")

        self.main_window.updateWebsite(result)



app = QApplication(sys.argv)

window = MainWindow()
window.show()

app.exec()