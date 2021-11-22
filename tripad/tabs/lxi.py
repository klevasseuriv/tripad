"""LXI Tab"""

from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import *

import vxi11


class LXITab(QWidget):
    def __init__(self, parent=None):
        super(LXITab, self).__init__(parent=parent)
        main_layout = QHBoxLayout()
        main_layout.setContentsMargins(5, 5, 5, 5)

        self.device_data = {}
        self.device_list = QListWidget()
        self.refresh_device_list()

        # TODO fucntions/init are distinct between SPD/SDG devices
        # need to have a class per device type and maybe a factory
        self.device_control = QWidget()
        device_control_layout = QVBoxLayout()
        device_control_layout.setContentsMargins(5, 5, 5, 5)

        sliders = QWidget()
        sliders_layout = QHBoxLayout()
        self.v_slider = QSlider(Qt.Vertical)
        self.v_slider.setMinimum(0)
        self.v_slider.setMaximum(20)
        self.v_slider.setFocusPolicy(Qt.StrongFocus)
        self.v_slider.setTickPosition(QSlider.TicksBothSides)
        self.v_slider.setTickInterval(1)
        self.v_slider.setSingleStep(1)
        self.v_slider.setStyle(SliderProxyStyle(self.v_slider.style()))
        self.v_slider.valueChanged.connect(self._change_voltage)

        self.c_slider = QSlider(Qt.Vertical)
        self.c_slider.setMinimum(0)
        self.c_slider.setMaximum(3)
        self.c_slider.setFocusPolicy(Qt.StrongFocus)
        self.c_slider.setTickPosition(QSlider.TicksBothSides)
        self.c_slider.setTickInterval(0.5)
        self.c_slider.setSingleStep(0.5)
        self.c_slider.setStyle(SliderProxyStyle(self.c_slider.style()))
        self.c_slider.valueChanged.connect(self._change_current)

        sliders_layout.addWidget(self.v_slider)
        sliders_layout.addWidget(self.c_slider)
        sliders.setLayout(sliders_layout)

        self.on_button = QPushButton("\n\n\nOn\n\n\n")
        self.on_button.clicked.connect(self._on_click_on)
        self.off_button = QPushButton("\n\n\nOff\n\n\n")
        self.off_button.clicked.connect(self._on_click_off)

        device_control_layout.addWidget(sliders)
        device_control_layout.addWidget(self.on_button)
        device_control_layout.addWidget(self.off_button)
        self.device_control.setLayout(device_control_layout)

        main_layout.addWidget(self.device_list, 33)
        main_layout.addWidget(self.device_control, 66)
        self.setLayout(main_layout)

    def refresh_device_list(self):
        # TODO discovery doesn't work on SPD devices
        # ideal setup would be discovery+netbox integration
        with open("lxi_devices") as devs:
            for dev in devs:
                addr = dev.split(":")[0]
                name = dev.split(":")[1]
                self.device_data[addr] = {"name": name}

                dev_item = QListWidgetItem()
                dev_item.setText(f"\n{addr} - {name}\n")
                self.device_list.insertItem(0, dev_item)

    def _on_click_on(self):
        addr = self.device_list.selectedItems()[0].text().split("-")[0].strip()
        name = self.device_list.selectedItems()[0].text().split("-")[1].strip()
        init_str = f"TCPIP::{addr}::5025::INSTR" if "power" in name.lower() else addr
        dev = vxi11.Instrument(init_str)
        try:
            if "power" in name.lower():
                dev.write("OUTPUT CH1,ON")
            elif "waveform" in name.lower():
                dev.write("C1:OUTP ON")
        except:
            pass

    def _on_click_off(self):
        addr = self.device_list.selectedItems()[0].text().split("-")[0].strip()
        name = self.device_list.selectedItems()[0].text().split("-")[1].strip()
        init_str = f"TCPIP::{addr}::5025::INSTR" if "power" in name.lower() else addr
        dev = vxi11.Instrument(init_str)
        try:
            if "power" in name.lower():
                dev.write("OUTPUT CH1,OFF")
            elif "waveform" in name.lower():
                dev.write("C1:OUTP OFF")
        except:
            pass

    def _change_voltage(self):
        addr = self.device_list.selectedItems()[0].text().split("-")[0].strip()
        name = self.device_list.selectedItems()[0].text().split("-")[1].strip()
        init_str = f"TCPIP::{addr}::5025::INSTR" if "power" in name.lower() else addr
        dev = vxi11.Instrument(init_str)
        try:
            if "power" in name.lower():
                dev.write(f"CH1:VOLTage {self.v_slider.value()}")
        except:
            pass

    def _change_current(self):
        addr = self.device_list.selectedItems()[0].text().split("-")[0].strip()
        name = self.device_list.selectedItems()[0].text().split("-")[1].strip()
        init_str = f"TCPIP::{addr}::5025::INSTR" if "power" in name.lower() else addr
        dev = vxi11.Instrument(init_str)
        try:
            if "power" in name.lower():
                dev.write(f"CH1:CURRent {self.c_slider.value()}")
        except:
            pass


class SliderProxyStyle(QProxyStyle):
    def pixelMetric(self, metric, option, widget):
        if metric == QStyle.PM_SliderThickness:
            return 80
        elif metric == QStyle.PM_SliderLength:
            return 80
        return super().pixelMetric(metric, option, widget)
