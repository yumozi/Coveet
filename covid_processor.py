import datetime
import pandas

import country_provinces
import pandas as pd


class CovidProcessor():
    """
    A class used to handle manipulating American and Canadian COVID records and deriving covid_data
    """

    def __init__(self):
        self.ca_data = pd.read_csv("covid_data/Provincial_Daily_Totals.csv")

        # Cleaning up and removing unnecessary info:
        self.ca_data["Province"].replace({'ALBERTA': 'Alberta', 'NWT': 'Northwest Territories', 'YUKON': 'Yukon',
                                          'SASKATCHEWAN': 'Saskatchewan', 'PEI': 'Prince Edward Island',
                                          'ONTARIO': 'Ontario', 'NEW BRUNSWICK': 'New Brunswick',
                                          'NOVA SCOTIA': 'Nova Scotia', 'NL': 'Newfoundland and Labrador',
                                          'MANITOBA': 'Manitoba', 'BC': 'British Columbia',
                                          'NUNAVUT': 'Nunavut', 'QUEBEC': 'Quebec'}, inplace=True)

        self.ca_data["Province"].replace({'PRINCE EDWARD ISLAND': 'Prince Edward Island',
                                          'NEWFOUNDLAND AND LABRADOR': 'Newfoundland and Labrador',
                                          'BRITISH COLUMBIA': 'British Columbia',
                                          'NORTHWEST TERRITORIES': 'Northwest Territories'}, inplace=True)

        # Remove canada total and repatriated canada (not provinces)
        for x in ['CANADA', 'REPATRIATED']:
            indexes = self.ca_data[self.ca_data['Province'] == x].index
            self.ca_data.drop(indexes, inplace=True)

        # Negative covid_data is inadmissable for our uses
        num = self.ca_data._get_numeric_data()
        num[num < 0] = 0

        # Continuing on to US covid_data
        self.us_data = pd.read_csv("covid_data/State_Daily_Totals.csv")

        # Negative covid_data is inadmissable for our uses
        num = self.us_data._get_numeric_data()
        num[num < 0] = 0

        # Restrictive ranges
        self.ca_range = [datetime.datetime(2020, 1, 25), datetime.datetime(2021, 12, 11)]
        self.us_range = [datetime.datetime(2020, 1, 22), datetime.datetime(2021, 12, 10)]

        # Relevant columns for us to use
        self.ca_cases = self.ca_data[['Province', 'SummaryDate', 'DailyTotals']]
        self.us_cases = self.us_data[['State Name', 'Submission Date', '7-day Avg Cases']]

    def get_data(self, date: datetime.datetime) -> tuple[pd.DataFrame, pd.DataFrame, list[float], list[str]]:
        """
        Returns the dataset's daily cases for every region and the maximum for all the regions, given a date
        The resulting tuple holds the american covid_data at index 0 and the canadian covid_data at index 1.

        Preconditions:
          - self.ca_range[0] <= date <= self.ca_range[1]
          - self.us_range[0] <= date <= self.us_range[1]
        """
        date_str = date.strftime('%Y-%m-%d')  # Convert our datetime into (year month day) format

        # Dataframe representing daily cases for provinces in Canada, during the date
        ca_rtn = self.ca_cases.loc[self.ca_cases['SummaryDate'] == date_str.replace('-', '/') + ' 12:00:00+00']\
            .drop('SummaryDate', axis=1).reset_index(drop=True)

        # Dataframe representing daily cases for provinces in America, during the date
        us_rtn = self.us_cases.loc[self.us_cases['Submission Date'] == date_str].drop('Submission Date', axis=1)\
            .reset_index(drop=True)

        # Maximum of all daily cases
        max_count = max(ca_rtn['DailyTotals'].max(), us_rtn['7-day Avg Cases'].max())
        step = max_count / 9
        bins_rtn = [x * step for x in range(10)]

        region_rtn = ca_rtn['Province'].tolist() + us_rtn['State Name'].tolist()

        return (ca_rtn, us_rtn, bins_rtn, region_rtn)


if __name__ == "__main__":
    a = CovidProcessor()
    data = a.get_data(datetime.datetime(2020, 12, 4))
    print(data[0].shape, data[1].shape, data[2], data[3])
    #print(covid_data[1])
