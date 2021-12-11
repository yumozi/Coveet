import io
import sys
import pandas as pd
import folium

from PyQt5.QtCore import Qt
from PyQt5 import QtWidgets, QtWebEngineWidgets


class ChoroplethMap(QtWidgets.QMainWindow):
    """A choropleth map"""
    def __init__(self, mode: str):
        super().__init__()

        # Window initialization
        self.setWindowTitle(self.tr("MAP PROJECT"))
        self.setFixedSize(1200, 1000)

        # GUI initalization
        self._view = QtWebEngineWidgets.QWebEngineView()
        self._view.setContentsMargins(25, 25, 25, 25)

        base_frame = QtWidgets.QWidget()
        self.setCentralWidget(base_frame)
        h_layout = QtWidgets.QHBoxLayout(base_frame)

        adjust_frame = QtWidgets.QWidget()
        v_layout = QtWidgets.QVBoxLayout(adjust_frame)

        h_layout.addWidget(adjust_frame)
        h_layout.addWidget(self._view, stretch=1)

        self._map = folium.Map(location=[40, -95], zoom_start=4, tiles="Stamen Terrain")

        if mode == "sentiment":
            raise NotImplementedError("Sentiment analysis is not yet implemented")
        elif mode == "covid":
            self._american_data = pd.read_csv("data/us_template.csv")
            self._canadian_data = pd.read_csv("data/canada_template.csv")

        # Choropleth configuration
        self._america_choropleth = folium.Choropleth(
            geo_data="data/us_states.json",
            name="America",
            data=self._american_data,
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
            data=self._canadian_data,
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


def display_map(mode: str) -> None:
    """Displays the interactive map"""

    app = QtWidgets.QApplication(sys.argv)

    if mode == "sentiment" or mode == "covid":
        window = ChoroplethMap(mode)
        window.show()
    else:
        window = QtWidgets.QMainWindow()
        base_frame = QtWidgets.QWidget()
        window.setCentralWidget(base_frame)
        hlay = QtWidgets.QHBoxLayout(base_frame)
        hlay.addWidget(ChoroplethMap('sentiment'))
        hlay.addWidget(ChoroplethMap('covid'))
        window.show()

    sys.exit(app.exec_())


if __name__ == "__main__":
    display_map('covid')
