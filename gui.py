import io
import sys
import pandas as pd
import folium

from PyQt5.QtCore import Qt
from PyQt5 import QtWidgets, QtWebEngineWidgets


class InteractiveMap(QtWidgets.QMainWindow):
    """An interactive choropleth map
    """
    def __init__(self):
        super().__init__()
        # Load data from files
        self._american_covid_data = pd.read_csv("data/us_template.csv")
        self._canadian_covid_data = pd.read_csv("data/canada_template.csv")

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

        # Slide value display label
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
            geo_data="data/us_states.json",
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

        data = io.BytesIO()
        self._map.save(data, close_file=False)
        self._view.setHtml(data.getvalue().decode())

    def slide_changed(self, value: int) -> None:
        """Callback to update a label to show the slider's current value"""
        self._slide_val.setText(str(value))

    def combo_changed(self, text: str) -> None:
        """Callback that updates the map when a new selection is made to the combo box"""
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

    def update_map(self) -> None:
        """Updates the map with the current data"""
        data = io.BytesIO()
        self._map.save(data, close_file=False)
        self._view.setHtml(data.getvalue().decode())


def display_map() -> None:
    """Displays the interactive map"""
    print("Displaying map")
    App = QtWidgets.QApplication(sys.argv)
    window = InteractiveMap()
    window.show()
    sys.exit(App.exec_())


if __name__ == "__main__":
    display_map()

    # App = QtWidgets.QApplication(sys.argv)
    # window = QtWidgets.QMainWindow()
    # base_frame = QtWidgets.QWidget()
    # window.setCentralWidget(base_frame)
    # hlay = QtWidgets.QHBoxLayout(base_frame)
    # hlay.addWidget(NAChoropleth())
    # hlay.addWidget(NAChoropleth())
    # window.show()

