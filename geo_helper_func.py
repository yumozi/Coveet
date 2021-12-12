"""

"""
import csv
from pprint import pprint
from dataclasses import dataclass


@dataclass
class City:
    name: str
    country: str
    population: int
    coordinates: tuple[float, float]


def load_location_csv(file_name: str) -> dict[str, City]:
    """
    Reads a csv file and returns a dictionary mapping
    city to population and location (latitude, longitude)
    """
    dict_so_far = {}
    with open(file_name, encoding="utf-8") as file:
        raw = file.read()
        raw = raw.split("\n")[1:]  # Split lines by newlines, take only the first item
        for row in raw:
            if row != "": # Avoid processing ending row from original newline split
                parsed = row.split(sep=";")  # Split table entries apart
                # print("{}, {}, {}, {}".format(parsed[1], parsed[7], parsed[10], parsed[16]))
                # print(len(parsed))
                temp = row[19].split(",")
                dict_so_far[row[1]] = City(name=row[1],
                                           country=row[7],
                                           population=int(row[13]),
                                           coordinates=(float(temp[0]), float(temp[1])))
    return dict_so_far


if __name__ == "__main__":
    # Test code
    csv_file = "geonames-all-cities-with-a-population-1000.csv"
    a = load_location_csv(csv_file)
    pprint(a)
