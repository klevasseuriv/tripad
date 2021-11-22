"""Network Tab"""

from PyQt5.QtWidgets import *
import nmcli


class NetworkTab(QWidget):
    def __init__(self, parent=None):
        super(NetworkTab, self).__init__(parent=parent)
        main_layout = QHBoxLayout()
        main_layout.setContentsMargins(5, 5, 5, 5)

        # Wifi list - pane 1
        self.wifi_data = {}
        self.wifi_list = QListWidget()
        self.wifi_list.itemSelectionChanged.connect(self.on_wifi_list_item_changed)
        self.refresh_wifi_list()

        # Connection selection - pane 2
        connection_select = QWidget()
        connection_layout = QVBoxLayout()
        connection_layout.setContentsMargins(5, 5, 5, 5)

        self.wifi_selected = QLabel("None")
        self.connect_button = QPushButton("\n\n\nConnect\n\n\n")
        self.connect_button.clicked.connect(self._on_click_connect)

        connection_layout.addWidget(self.wifi_selected)
        connection_layout.addWidget(self.connect_button)
        connection_select.setLayout(connection_layout)

        # Add panes to main layout
        main_layout.addWidget(self.wifi_list, 33)
        main_layout.addWidget(connection_select, 66)
        self.setLayout(main_layout)

    def refresh_wifi_list(self):
        for con in nmcli.device.wifi():
            if not con.ssid:
                continue

            # assumes that wireless connections have the same name as the SSID
            # ideally we would be able to just pull the connection SSID and compare
            matched_con = None
            for saved_con in nmcli.connection():
                if saved_con.name == con.ssid:
                    matched_con = saved_con
                    break

            self.wifi_data[con.ssid] = {
                "security": con.security,
                "channel": con.chan,
                "strength": con.signal,
                "con": {
                    "name": matched_con.name if matched_con else None,
                    "interface": matched_con.device if matched_con else None,
                },
            }

            con_item = QListWidgetItem()
            con_item.setText(con.ssid)
            self.wifi_list.insertItem(0, con_item)

    def on_wifi_list_item_changed(self):

        # Update the connection details display
        selected_item = self.wifi_list.selectedItems()[0].text()
        self.wifi_selected.setText(
            self._generate_selected_text(
                ssid=selected_item,
                channel=self.wifi_data[selected_item]["channel"],
                security=self.wifi_data[selected_item]["security"],
                strength=self.wifi_data[selected_item]["strength"],
                connection_profile=True
                if self.wifi_data[selected_item]["con"]["name"]
                else False,
            )
        )

    def _on_click_connect(self):
        return

    def _generate_selected_text(
        self,
        ssid: str,
        security: str,
        channel: str,
        strength: str,
        connection_profile: bool,
    ) -> str:
        return f"<h1>{ssid}</h1><br>Security: {security}<br>Channel: {channel}<br>Strength: {strength}<br>Connection Profile: {connection_profile}"
