"""Tripad application"""
from kivy.app import App
from kivy.uix.tabbedpanel import TabbedPanel
from kivy.uix.behaviors import FocusBehavior
from kivy.uix.recycleboxlayout import RecycleBoxLayout
from kivy.uix.recycleview.layout import LayoutSelectionBehavior

# unused imports but necessary for kivy to detect these
from tripad.networkconfigitem import NetworkConfigItem
from tripad.kasacontrolitem import KasaControlItem


class MainPanel(TabbedPanel):
    pass


class SelectableRecycleBoxLayout(
    FocusBehavior, LayoutSelectionBehavior, RecycleBoxLayout
):
    """Adds selection and focus behaviour to the view."""


class TripadApp(App):
    def build(self):
        return MainPanel()


if __name__ == "__main__":
    TripadApp().run()
