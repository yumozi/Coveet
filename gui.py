import datetime
import io
import sys
import folium

from PyQt5.QtCore import *
from PyQt5 import QtWidgets, QtWebEngineWidgets

from covid_processor import CovidData
from tweet import get_tweets

from country_provinces import all_provinces


class ChoroplethMap(QtWidgets.QMainWindow):
    """A choropleth map

    Representation Invariants:
      - mode in {'covid','sentiment'}
    """

    def __init__(self, mode: str):
        super().__init__()
        self.mode = mode

        # Window initialization
        self.setWindowTitle(self.tr("COVEET TRACKER"))
        self.setFixedSize(900, 900)

        # GUI initalization
        self._view = QtWebEngineWidgets.QWebEngineView()
        self._view.setContentsMargins(25, 25, 25, 25)
        base_frame = QtWidgets.QWidget()
        self.setCentralWidget(base_frame)
        h_layout = QtWidgets.QHBoxLayout(base_frame)

        # Initialize selectable regions and dates
        self._selectable_dates = ['2020-08-01', '2020-10-01', '2020-12-01',
                                  '2021-02-01', '2021-04-01', '2021-06-01',
                                  '2021-08-01', '2021-10-01', '2021-12-01']
        self._selectable_regions = all_provinces

        # Initialize covid/sentiment data
        if self.mode == "covid":
            self._covid_data = CovidData()
            self._ca_data, self._us_data, self._bins = \
                self._covid_data.get_data(self.deparse_date(self._selectable_dates[0]))
            self._legend_name = 'daily cases'
        else:
            # mode == 'sentiment'
            self._ca_data, self._us_data = get_tweets(self.deparse_date(self._selectable_dates[0]))
            self._bins = [-1, -0.75, -0.5, -0.25, 0, 0.25, 0.5, 0.75, 1]
            self._legend_name = 'sentiment score'

        # Define date selector and region selector
        self._date_selector = QtWidgets.QComboBox()
        self._date_selector.addItems(self._selectable_dates)
        self._date_selector.activated[str].connect(self.update_date)

        self._region_selector = QtWidgets.QComboBox()
        self._region_selector.addItems(self._selectable_regions)
        self._region_selector.activated[str].connect(self.update_region)

        # Define value display, with default values pre-calculated using default date and region
        self._value_display = QtWidgets.QLabel()
        if mode == 'covid':
            self._value_display.setText('New COVID Cases: 0')
        else:
            self._value_display.setText('Avg. TWITTER Sentiment: -0.01649')

        adjust_frame = QtWidgets.QWidget()
        v_layout = QtWidgets.QVBoxLayout(adjust_frame)

        v_layout.addWidget(self._date_selector)
        v_layout.addWidget(self._region_selector)
        v_layout.addWidget(self._value_display)
        v_layout.setAlignment(Qt.AlignTop)
        h_layout.addWidget(adjust_frame)
        h_layout.addWidget(self._view, stretch=1)

        # Done to avoid "initialized outside of init"
        self._map = None
        self._america_choropleth = None
        self._canada_choropleth = None

        # Draw the map in the window
        self.render_map()

    def update_date(self, text: str) -> None:
        """Callback that updates the loaded data when a new date is selected
        """
        if self.mode == 'covid':
            self._ca_data, self._us_data, self._bins = \
                self._covid_data.get_data(self.deparse_date(text))
        else:
            self._ca_data, self._us_data = get_tweets(
                self.deparse_date(text))

        # Update list of available regions to choose from
        self._region_selector.clear()
        self._region_selector.addItems(self._selectable_regions)

        self.render_map()

    def update_region(self, text: str) -> None:
        """Callback that updates the value display when a new region is selected
        """
        if self.mode == 'covid':
            cases = 'NAN'
            if text in self._ca_data['Province'].values:
                cases = self._ca_data.loc[self._ca_data['Province'] == text].values[0][1]
            elif text in self._us_data['State Name'].values:
                cases = self._us_data.loc[self._us_data['State Name'] == text].values[0][1]
            self._value_display.setText("New COVID Cases: " + str(cases))

        elif self.mode == 'sentiment':
            sentiment = 'NAN'
            if text in self._ca_data['location'].values:
                sentiment = self._ca_data.loc[self._ca_data['location'] == text].values[0][1]
            elif text in self._us_data['location'].values:
                sentiment = self._us_data.loc[self._us_data['location'] == text].values[0][1]

            if sentiment == 'NAN':
                self._value_display.setText("Avg. TWITTER Sentiment: NAN")
            else:
                self._value_display.setText(" Avg. TWITTER Sentiment: " + str(round(sentiment, 5)))

    def render_map(self) -> None:
        """Renders a map with current data"""
        self._map = folium.Map(location=[40, -95], zoom_start=4, tiles="Stamen Terrain")

        # Choropleth configuration
        if self.mode == 'covid':
            c1 = ["Province", "DailyTotals"]
            c2 = ["State Name", "7-day Avg Cases"]
        else:
            c1 = ["location", "value"]
            c2 = ["location", "value"]

        self._canada_choropleth = folium.Choropleth(
            geo_data="data/canada_provinces.geojson",
            name="Canada",
            data=self._ca_data,
            columns=c1,
            key_on="feature.properties.name",
            fill_color="YlOrRd",
            fill_opacity=0.7,
            line_opacity=.1,
            _legend_name=self._legend_name,
            highlight=True,
            bins=self._bins
        )
        self._canada_choropleth.add_to(self._map)

        self._america_choropleth = folium.Choropleth(
            geo_data="data/us_states.json",
            name="America",
            data=self._us_data,
            columns=c2,
            key_on="feature.id",
            fill_color="YlOrRd",
            fill_opacity=0.7,
            line_opacity=.1,
            _legend_name="America",
            highlight=True,
            bins=self._bins
        )
        self._america_choropleth.add_to(self._map)

        # An issue under foilum's GitHub page highlighted that
        # this is the only way to hide a legend for now
        for key in self._america_choropleth._children:
            if key.startswith('color_map'):
                del (self._america_choropleth._children[key])

        self._canada_choropleth.geojson.add_child(
            folium.features.GeoJsonTooltip(['name'], labels=False)
        )

        self._america_choropleth.geojson.add_child(
            folium.features.GeoJsonTooltip(['name'], labels=False)
        )

        folium.LayerControl().add_to(self._map)  # add layer control and toggling to the map

        data = io.BytesIO()
        self._map.save(data, close_file=False)
        self._view.setHtml(data.getvalue().decode())

    def deparse_date(self, date_str: str) -> datetime.datetime:
        """Returns a datetime.datetime object from a string in (Year-Month-Date) format"""
        year, month, day = date_str.split("-")
        return datetime.datetime(int(year), int(month), int(day))


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
    # display_map('covid')
    # display_map('sentiment')
    display_map('')

    # import python_ta
    # import python_ta.contracts
    # python_ta.contracts.DEBUG_CONTRACTS = True
    # python_ta.contracts.check_all_contracts()
    # import doctest
    # doctest.testmod(verbose=True)
    # python_ta.check_all(config={
    #     # the names (strs) of imported modules
    #     'extra-imports': ['python_ta.contracts', 'datetime', 'io', 'sys', 'folium', 'covid_processor'],
    #     'allowed-io': [],  # the names (strs) of functions that call print/open/input
    #     'max-line-length': 100,
    #     'disable': ['R1705', 'C0200']
    # })
