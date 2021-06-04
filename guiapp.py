from kivy.app import App
from kivy.uix.widget import Widget

class AircraftList(Widget):
    pass

class AircraftVisualizer(App):
    def build(self):
        return AircraftList()