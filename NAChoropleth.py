import io
import sys
import pandas as pd
import folium

from PyQt5.QtCore import Qt
from PyQt5 import QtWidgets, QtWebEngineWidgets


class NAChoropleth(QtWidgets.QMainWindow):
    """A class meant to aid in the creation and management of an interactive map, with additional
    choropleth functionality and ability to visualize filtered data.

    TODO: specify instance attributes?
    """
    def __init__(self):
        super().__init__()
        # Load data from files
        self._american_covid_data = pd.read_csv("data/US_Unemployment_Oct2012.csv")
        self._canadian_covid_data = pd.read_csv("data/canada_test.csv")

        # Window initialization
        self.setWindowTitle(self.tr("MAP PROJECT"))
        self.setFixedSize(1200, 1000)

        # GUI initalization
        self._view = QtWebEngineWidgets.QWebEngineView()
        self._view.setContentsMargins(25, 25, 25, 25)

        base_frame = QtWidgets.QWidget()
        self.setCentralWidget(base_frame)
        h_layout = QtWidgets.QHBoxLayout(base_frame)

        self._combo = QtWidgets.QComboBox()

        # Add arbitrary maximums for property sliders
        self._maxes = {"Covid Cases": 10000, "Population": 100000}

        # Combobox
        for x in self._maxes:
            self._combo.addItem(x)
        self._combo.activated[str].connect(self.combo_changed)

        # Slide value display lable
        self._slide_val = QtWidgets.QLabel('0')
        self._slide_val.setAlignment(Qt.AlignLeft | Qt.AlignVCenter)

        # Slider
        self._slider = QtWidgets.QSlider(Qt.Vertical)
        self._slider.setFocusPolicy(Qt.StrongFocus)
        self._slider.setTickInterval(10)
        self._slider.setSingleStep(1)
        self._slider.valueChanged[int].connect(self.slide_changed)
        self._slider.setMaximum(self._maxes["Covid Cases"])

        adjust_frame = QtWidgets.QWidget()
        v_layout = QtWidgets.QVBoxLayout(adjust_frame)

        v_layout.addWidget(self._combo)
        v_layout.addWidget(self._slide_val)
        v_layout.addWidget(self._slider)

        h_layout.addWidget(adjust_frame)
        h_layout.addWidget(self._view, stretch=1)

        # Map widget creation
        self._map = folium.Map(location=[40, -95], zoom_start=4, tiles="Stamen Terrain")

        # Choropleth configuration
        self._america_choropleth = folium.Choropleth(
            geo_data="data/us-states.json",
            name="America",
            data=self._american_covid_data,
            columns=["State", "Unemployment"],
            key_on="feature.id",
            fill_color="YlGn",
            fill_opacity=0.7,
            line_opacity=.1,
            legend_name="America",
            highlight=True,
        )
        self._america_choropleth.add_to(self._map)

        self._canada_choropleth = folium.Choropleth(
            geo_data="data/canada_provinces.geojson",
            name="Canada",
            data=self._canadian_covid_data,
            columns=["Province", "Value"],
            key_on="feature.properties.name",
            fill_color="YlGn",
            fill_opacity=0.7,
            line_opacity=.1,
            legend_name="Canada",
            highlight=True,
        )
        self._canada_choropleth.add_to(self._map)

        folium.LayerControl().add_to(self._map)  # add layer control and toggling to the map

        # Connect the map and api
        data = io.BytesIO()
        self._map.save(data, close_file=False)
        self._view.setHtml(data.getvalue().decode())

    def slide_changed(self, value: int) -> None:
        """Callback to update a label to show the slider's current value"""
        self._slide_val.setText(str(value))

    def combo_changed(self, text: str) -> None:
        """Callback that updates the map when a new selection is made to the combo box"""
        # TODO: Find a way to update the map dynamically
        self._slider.setMaximum(self._maxes[text])
        print(text)
        self._canada_choropleth = folium.Choropleth(
            geo_data="data/canada_provinces.geojson",
            name="Canada",
            data=self._canadian_covid_data,
            columns=["Province", "Value"],
            key_on="feature.properties.name",
            fill_color="OrRd",
            fill_opacity=0.2,
            line_opacity=.1,
            legend_name="Canada",
            highlight=True,
        )
        self._canada_choropleth.add_to(self._map)
        folium.LayerControl().add_to(self._map)
        data = io.BytesIO()
        self._map.save(data, close_file=False)
        self._view.setHtml(data.getvalue().decode())


if __name__ == "__main__":
    App = QtWidgets.QApplication(sys.argv)
    window = NAChoropleth()
    window.show()

    # App = QtWidgets.QApplication(sys.argv)
    # window = QtWidgets.QMainWindow()
    # base_frame = QtWidgets.QWidget()
    # window.setCentralWidget(base_frame)
    # hlay = QtWidgets.QHBoxLayout(base_frame)
    # hlay.addWidget(NAChoropleth())
    # hlay.addWidget(NAChoropleth())
    # window.show()

    sys.exit(App.exec())
