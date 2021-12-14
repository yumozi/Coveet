"""CovidData"""
import datetime
import pandas as pd


class CovidData:
    """
    Class to process covid data
    """
    ca_data = pd.DataFrame
    us_data = pd.DataFrame

    def __init__(self) -> None:
        # Load Canada covid data
        self.ca_data = pd.read_csv("data/Provincial_Daily_Totals.csv")

        # Dataframe representing daily cases for provinces in Canada
        self.ca_data = self.ca_data[['Province', 'SummaryDate', 'DailyTotals']]

        # Reformat names in the 'Province' column
        self.ca_data["Province"].replace({'ALBERTA': 'Alberta', 'NWT': 'Northwest Territories',
                                          'YUKON': 'Yukon', 'SASKATCHEWAN': 'Saskatchewan',
                                          'PEI': 'Prince Edward Island', 'ONTARIO': 'Ontario',
                                          'NEW BRUNSWICK': 'New Brunswick',
                                          'NOVA SCOTIA': 'Nova Scotia',
                                          'NL': 'Newfoundland and Labrador',
                                          'MANITOBA': 'Manitoba', 'BC': 'British Columbia',
                                          'NUNAVUT': 'Nunavut', 'QUEBEC': 'Quebec',
                                          'PRINCE EDWARD ISLAND': 'Prince Edward Island',
                                          'NEWFOUNDLAND AND LABRADOR': 'Newfoundland and Labrador',
                                          'BRITISH COLUMBIA': 'British Columbia',
                                          'NORTHWEST TERRITORIES': 'Northwest Territories'}, inplace=True)

        # Remove any rows with 'REPATRIATED' in the Province column
        indices = self.ca_data[self.ca_data['Province'] == 'REPATRIATED'].index
        self.ca_data.drop(indices, inplace=True)

        # Replace any DailyTotals that is less than 0 with 0
        indices = self.ca_data[self.ca_data['DailyTotals'] < 0].index
        self.ca_data.loc[indices, 'DailyTotals'] = 0

        # Load US covid data
        self.us_data = pd.read_csv("data/State_Daily_Totals.csv")

        # Dataframe representing daily cases for states in US
        self.us_data = self.us_data[['State Name', 'Submission Date', '7-day Avg Cases']]

        # Replace any 7-day Avg Cases that is less than 0 with 0
        indices = self.us_data[self.us_data['7-day Avg Cases'] < 0].index
        self.us_data.loc[indices, '7-day Avg Cases'] = 0

    def get_data(self, date: datetime.datetime) -> tuple[pd.DataFrame, pd.DataFrame, list[float]]:
        """
        Returns daily cases for every province in Canada, daily cases for every state in US, and
        the bin boundaries for the daily cases across Canada and US.

        Preconditions:
          - datetime.datetime(2020, 1, 22) <= date <= datetime.datetime(2021, 12, 11)
        """
        # Convert input date into "year-month-day" format
        date_str = date.strftime('%Y-%m-%d')

        # Fetch for cases in Canada on the given date
        ca_rtn = self.ca_data.loc[self.ca_data['SummaryDate'] == date_str.replace('-', '/') + ' 12:00:00+00']\
            .drop('SummaryDate', axis=1).reset_index(drop=True)

        # Fetch for cases in US on the given date
        us_rtn = self.us_data.loc[self.us_data['Submission Date'] == date_str].drop('Submission Date', axis=1)\
            .reset_index(drop=True)

        # Calculate bin boundaries for the given date
        max_cases = max(ca_rtn['DailyTotals'].max(), us_rtn['7-day Avg Cases'].max())
        step = max_cases / 9
        bins = [x * step for x in range(10)]

        return ca_rtn, us_rtn, bins


if __name__ == "__main__":
    pass
