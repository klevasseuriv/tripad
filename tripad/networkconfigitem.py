from kivy.uix.recycleview import RecycleView
from kivy.uix.recycleview.views import RecycleDataViewBehavior
from kivy.uix.label import Label

from tripad._shared import TripadItem


class SelectableSSID(RecycleDataViewBehavior, Label):
    """SSID list view item"""

    index = None
    selected = False
    selectable = True

    def refresh_view_attrs(self, rv, index, data):
        self.index = index
        return super().refresh_view_attrs(rv, index, data)

    def on_touch_down(self, touch):
        if super().on_touch_down(touch):
            return True
        if self.collide_point(*touch.pos) and self.selectable:
            return self.parent.select_with_touch(self.index, touch)
        return super().on_touch_down(touch)

    def apply_selection(self, rv, index, is_selected):
        self.selected = is_selected
        if is_selected:
            print(f"Selection changed to {rv.data[index]}")
        else:
            print(f"Selection removed {rv.data[index]}")


class ListRecycleView(RecycleView):
    """A list view that doesn't suck"""

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.data = [{"text": str(x)} for x in range(100)]


class NetworkConfigItem(TripadItem):
    """Tab item to contain network config related controls"""

    def testbutton(self):
        print("some words")
