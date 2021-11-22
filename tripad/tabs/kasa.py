"""Kasa Tab"""

from PyQt5.QtWidgets import *

import asyncio
from kasa import Discover
from kasa import SmartPlug


class KasaTab(QWidget):
    def __init__(self, parent=None):
        super(KasaTab, self).__init__(parent=parent)
        main_layout = QHBoxLayout()
        main_layout.setContentsMargins(5, 5, 5, 5)

        self.device_data = {}
        self.device_list = QListWidget()
        self.refresh_device_list()

        self.on_button = QPushButton("\n\n\nOn\n\n\n")
        self.on_button.clicked.connect(self._on_click_on)
        self.off_button = QPushButton("\n\n\nOff\n\n\n")
        self.off_button.clicked.connect(self._on_click_off)

        main_layout.addWidget(self.device_list, 33)
        main_layout.addWidget(self.on_button, 33)
        main_layout.addWidget(self.off_button, 33)
        self.setLayout(main_layout)

    def refresh_device_list(self):
        devices = asyncio.run(Discover.discover())
        for addr, dev in devices.items():
            asyncio.run(dev.update())
            self.device_data[addr] = {"alias": dev.alias}

            dev_item = QListWidgetItem()
            dev_item.setText(f"\n{addr} - {dev.alias}\n")
            self.device_list.insertItem(0, dev_item)

    def _on_click_on(self):
        plug = SmartPlug(
            self.device_list.selectedItems()[0].text().split("-")[0].strip()
        )
        try:
            asyncio.run(plug.turn_on())
        except:
            pass

    def _on_click_off(self):
        plug = SmartPlug(
            self.device_list.selectedItems()[0].text().split("-")[0].strip()
        )
        try:
            asyncio.run(plug.turn_off())
        except:
            pass
