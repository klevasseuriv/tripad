"""Tripad application"""
import sys

from PyQt5.QtWidgets import QApplication
from PyQt5.QtWidgets import QLabel
from PyQt5.QtWidgets import QWidget


def main():
    app = QApplication(sys.argv)
    window = QWidget()
    window.setWindowTitle("tripad")
    window.setGeometry(100, 100, 280, 80)
    window.move(60, 15)
    helloMsg = QLabel("<h1>tripad</h1>", parent=window)
    helloMsg.move(60, 15)

    window.show()

    sys.exit(app.exec_())


if __name__ == "__main__":
    main()
