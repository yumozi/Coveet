import io
import sys
import pandas as pd
import folium

from PyQt5.QtCore import Qt
from PyQt5 import QtWidgets, QtWebEngineWidgets


class NAChoropleth(QtWidgets.QMainWindow):
    def __init__(self):
        super().__init__()
        self.america_covid_data = pd.read_csv("US_Unemployment_Oct2012.csv")
        self.canada_covid_data = pd.read_csv("canada_test.csv")

        # Window initialization
        self.setWindowTitle(self.tr("MAP PROJECT"))
        self.setFixedSize(1200, 1000)

        # GUI initalization
        self.view = QtWebEngineWidgets.QWebEngineView()
        self.view.setContentsMargins(25, 25, 25, 25)

        base_frame = QtWidgets.QWidget()
        self.setCentralWidget(base_frame)
        h_layout = QtWidgets.QHBoxLayout(base_frame)

        self.combo = QtWidgets.QComboBox()

        # Combobox
        self.maxes = {"Covid Cases": 10000, "Population": 100000}
        for x in self.maxes:
            self.combo.addItem(x)
        self.combo.activated[str].connect(self.combo_changed)

        # Slide value display lable
        self.slide_val = QtWidgets.QLabel('0')
        self.slide_val.setAlignment(Qt.AlignLeft | Qt.AlignVCenter)

        # Slider
        self.slider = QtWidgets.QSlider(Qt.Vertical)
        self.slider.setFocusPolicy(Qt.StrongFocus)
        self.slider.setTickInterval(10)
        self.slider.setSingleStep(1)
        self.slider.valueChanged[int].connect(self.slide_changed)
        self.slider.setMaximum(self.maxes["Covid Cases"])

        adjust_frame = QtWidgets.QWidget()
        v_layout = QtWidgets.QVBoxLayout(adjust_frame)

        v_layout.addWidget(self.combo)
        v_layout.addWidget(self.slide_val)
        v_layout.addWidget(self.slider)

        h_layout.addWidget(adjust_frame)
        h_layout.addWidget(self.view, stretch=1)

        # Map widget creation
        self.map = folium.Map(location=[40, -95], zoom_start=4, tiles="Stamen Toner")

        # Choropleth configuration
        self.america_choropleth = folium.Choropleth(
            geo_data="us-states.json",
            name="America",
            data=self.america_covid_data,
            columns=["State", "Unemployment"],
            key_on="feature.id",
            fill_color="YlGn",
            fill_opacity=0.7,
            line_opacity=.1,
            legend_name="America",
            highlight=True,
        )
        self.america_choropleth.add_to(self.map)

        self.canada_choropleth = folium.Choropleth(
            geo_data="canada_provinces.geojson",
            name="Canada",
            data=self.canada_covid_data,
            columns=["Province", "Value"],
            key_on="feature.properties.name",
            fill_color="YlGn",
            fill_opacity=0.7,
            line_opacity=.1,
            legend_name="Canada",
            highlight=True,
        )
        self.canada_choropleth.add_to(self.map)

        folium.LayerControl().add_to(self.map)  # add layer control and toggling to the map

        #folium.TileLayer('cartodbdark_matter', overlay=True, name="dark mode").add_to(self.map)
        #folium.TileLayer('cartodbpositron', overlay=True, name="light mode").add_to(self.map)

        # Connect the map and api
        data = io.BytesIO()
        self.map.save(data, close_file=False)
        self.view.setHtml(data.getvalue().decode())

    def slide_changed(self, value):
        self.slide_val.setText(str(value))

    def combo_changed(self, text):
        self.slider.setMaximum(self.maxes[text])
        print(text)
        self.canada_choropleth = folium.Choropleth(
            geo_data="canada_provinces.geojson",
            name="Canada",
            data=self.canada_covid_data,
            columns=["Province", "Value"],
            key_on="feature.properties.name",
            fill_color="OrRd",
            fill_opacity=0.2,
            line_opacity=.1,
            legend_name="Canada",
            highlight=True,
        )
        self.canada_choropleth.add_to(self.map)
        folium.LayerControl().add_to(self.map)
        data = io.BytesIO()
        self.map.save(data, close_file=False)
        self.view.setHtml(data.getvalue().decode())

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
