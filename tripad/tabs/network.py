"""Network Tab"""

from PyQt5.QtWidgets import *
import nmcli


class NetworkTab(QWidget):
    def __init__(self, parent=None):
        super(NetworkTab, self).__init__(parent=parent)
        main_layout = QHBoxLayout()
        main_layout.setContentsMargins(5, 5, 5, 5)

        self.wifi_data = {}
        self.wifi_list = QListWidget()
        self.wifi_list.itemSelectionChanged.connect(self.on_wifi_list_item_changed)
        self.refresh_wifi_list()

        self.wifi_selected = QLabel("None")

        main_layout.addWidget(self.wifi_list, 33)
        main_layout.addWidget(self.wifi_selected, 66)
        self.setLayout(main_layout)

    def refresh_wifi_list(self):
        for con in nmcli.device.wifi():
            if not con.ssid:
                continue

            self.wifi_data[con.ssid] = {
                "security": con.security,
                "channel": con.chan,
                "strength": con.signal,
            }

            con_item = QListWidgetItem()
            con_item.setText(con.ssid)
            self.wifi_list.insertItem(0, con_item)

    def on_wifi_list_item_changed(self):
        selected_item = self.wifi_list.selectedItems()[0].text()
        self.wifi_selected.setText(
            self._generate_selected_text(
                ssid=selected_item,
                channel=self.wifi_data[selected_item]["channel"],
                security=self.wifi_data[selected_item]["security"],
                strength=self.wifi_data[selected_item]["strength"],
            )
        )

    def _generate_selected_text(
        self, ssid: str, security: str, channel: str, strength: str
    ) -> str:
        return f"<h1>{ssid}</h1><br>Security: {security}<br>Channel: {channel}<br>Strength: {strength}"
