"""Tripad application"""
import sys

from PyQt5.QtWidgets import *
from PyQt5.QtCore import QStringListModel

from tripad.tabs.network import NetworkTab
from tripad.tabs.kasa import KasaTab
from tripad.tabs.lxi import LXITab


class MainScreenWidget(QWidget):
    def __init__(self, parent=None):
        super(MainScreenWidget, self).__init__(parent=parent)
        main_layout = QVBoxLayout()
        main_layout.setContentsMargins(5, 5, 5, 5)

        self.setWindowTitle("tripad")
        self.setGeometry(100, 100, 280, 80)
        self.move(60, 15)

        self.tabs = QTabWidget()

        self.nw_tab = NetworkTab()
        self.kasa_tab = KasaTab()
        self.lxi_tab = LXITab()

        self.tabs.addTab(self.nw_tab, "Network")
        self.tabs.addTab(self.kasa_tab, "Kasa")
        self.tabs.addTab(self.lxi_tab, "LXI")

        main_layout.addWidget(self.tabs)
        self.setLayout(main_layout)


def main():
    app = QApplication(sys.argv)

    main_window = MainScreenWidget()
    main_window.show()

    sys.exit(app.exec_())


if __name__ == "__main__":
    main()
