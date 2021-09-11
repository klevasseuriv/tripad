from kivy.app import App
from kivy.uix.tabbedpanel import TabbedPanel


class MainPanel(TabbedPanel):
    pass


class TripadApp(App):
    def build(self):
        return MainPanel()


if __name__ == "__main__":
    TripadApp().run()
