import io
import sys
import pandas as pd
import folium

from tweet import create_dataframe, Tweet
from PyQt5 import QtWidgets, QtWebEngineWidgets


class ChoroplethMap(QtWidgets.QMainWindow):
    """A choropleth map"""
    def __init__(self, mode: str, canada_data: pd.DataFrame, us_data: pd.DataFrame, bins: list):
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

        # Map initialization
        self._canada_data = canada_data
        self._us_data = us_data

        if mode == "sentiment":
            name = 'sentiment score'
        else:
            name = 'daily cases'

        # Choropleth configuration
        self._canada_choropleth = folium.Choropleth(
            geo_data="data/canada_provinces.geojson",
            name="Canada",
            data=self._canada_data,
            columns=["location", "value"],
            key_on="feature.properties.name",
            fill_color="YlGn",
            fill_opacity=0.7,
            line_opacity=.1,
            legend_name=name,
            highlight=True,
            bins=bins
        )
        self._canada_choropleth.add_to(self._map)

        self._us_choropleth = folium.Choropleth(
            geo_data="data/us_states.json",
            name="America",
            data=self._us_data,
            columns=["location", "value"],
            key_on="feature.id",
            fill_color="YlGn",
            fill_opacity=0.7,
            line_opacity=.1,
            legend_name="America",
            highlight=True,
            bins=bins
        )
        self._us_choropleth.add_to(self._map)

        # An issue under foilum's GitHub page highlighted that
        # this is the only way to display one legend with two
        # choropleth maps.
        for key in self._us_choropleth._children:
            if key.startswith('color_map'):
                del(self._us_choropleth._children[key])

        folium.LayerControl().add_to(self._map)  # add layer control and toggling to the map

        data = io.BytesIO()
        self._map.save(data, close_file=False)
        self._view.setHtml(data.getvalue().decode())


def display_map(mode: str, tweets: list[Tweet]) -> None:
    """Displays the interactive map"""

    app = QtWidgets.QApplication(sys.argv)

    if mode == "sentiment":
        canada_data, us_data = create_dataframe(tweets)
        window = ChoroplethMap(mode, canada_data, us_data, bins=[-1, -0.5, 0, 0.5, 1])
        window.show()
    elif mode == 'covid':
        window = ChoroplethMap(mode,
                               canada_data=pd.read_csv("data/canada_covid.csv"),
                               us_data=pd.read_csv("data/us_covid.csv"),
                               bins=[0, 300, 600, 900, 1200, 1500, 1800, 2100, 2400, 2700])
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
