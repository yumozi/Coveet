"""Coveet: Twitter COVID Sentiment Analyser

Copyright and Usage Information
===============================
This file is Copyright (c) 2021 Eric Xue and Jeremy Xie.
"""
country_provinces = {'Canada': ['alberta', 'british columbia', 'manitoba',
                                'new brunswick', 'newfoundland and labrador',
                                'northwest territories', 'nova scotia', 'nunavut',
                                'ontario', 'prince edward island', 'quebec',
                                'saskatchewan', 'yukon'],
                     'United States': ['alabama', 'alaska', 'arizona', 'arkansas', 'california',
                                       'colorado', 'connecticut', 'delaware', 'florida', 'georgia',
                                       'hawaii', 'idaho', 'illinois', 'indiana', 'iowa', 'kansas',
                                       'kentucky', 'louisiana', 'maine', 'maryland',
                                       'massachusetts', 'michigan', 'minnesota', 'mississippi',
                                       'missouri', 'montana', 'nebraska', 'nevada', 'new hampshire',
                                       'new jersey', 'new mexico', 'new york', 'north carolina',
                                       'north dakota', 'ohio', 'oklahoma', 'oregon', 'pennsylvania',
                                       'rhode island', 'south carolina', 'south dakota',
                                       'tennessee', 'texas', 'utah', 'vermont', 'virginia',
                                       'washington', 'west virginia', 'wisconsin', 'wyoming']}

all_provinces = ['Alberta', 'British Columbia', 'Manitoba', 'New Brunswick',
                 'Newfoundland and Labrador', 'Northwest Territories', 'Nova Scotia',
                 'Nunavut', 'Ontario', 'Prince Edward Island', 'Quebec', 'Saskatchewan',
                 'Yukon', 'Alabama', 'Alaska', 'Arizona', 'Arkansas', 'California',
                 'Colorado', 'Connecticut', 'Delaware', 'Florida', 'Georgia', 'Hawaii',
                 'Idaho', 'Illinois', 'Indiana', 'Iowa', 'Kansas', 'Kentucky', 'Louisiana',
                 'Maine', 'Maryland', 'Massachusetts', 'Michigan', 'Minnesota', 'Mississippi',
                 'Missouri', 'Montana', 'Nebraska', 'Nevada', 'New Hampshire', 'New Jersey',
                 'New Mexico', 'New York', 'North Carolina', 'North Dakota', 'Ohio', 'Oklahoma',
                 'Oregon', 'Pennsylvania', 'Rhode Island', 'South Carolina', 'South Dakota',
                 'Tennessee', 'Texas', 'Utah', 'Vermont', 'Virginia', 'Washington', 'West Virginia',
                 'Wisconsin', 'Wyoming']

if __name__ == '__main__':
    import python_ta.contracts

    python_ta.contracts.DEBUG_CONTRACTS = False
    python_ta.contracts.check_all_contracts()

    import doctest

    doctest.testmod(verbose=True)

    import python_ta
    python_ta.check_all(config={
        'allowed-io': ['run_example'],
        'max-line-length': 100,
        'disable': ['R1705', 'C0200', 'R0201']
    })
