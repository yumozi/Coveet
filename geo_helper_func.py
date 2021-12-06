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


def load_lookup_from_file(file_name: str) -> dict[str, City]:
    """
    Reads a file from a name and returns a dictionary mapping
    city to population and location (lattitude, longitude)
    """
    dict_so_far = {}
    with open(file_name, encoding="utf-8") as file:
        raw = file.read() # Read the file as a string
        raw = raw.split("\n")[1:]  # Split lines by newlines, take only the first item
        for row in raw:
            if row != "": # Avoid processing ending row from original newline split
                parsed = row.split(sep=";")  # Split table entries apart
                #print("{}, {}, {}, {}".format(parsed[1], parsed[7], parsed[10], parsed[16]))
                #print(len(parsed))
                city = process_row(parsed)
                dict_so_far[city.name] = city
    return dict_so_far

def process_row(row: list):
    """Takes in a parsed list and returns a City class"""
    temp = row[19].split(",")
    coords = (float(temp[0]), float(temp[1]))
    return City(name=row[1], country=row[7], population=int(row[13]), coordinates=coords)

if __name__ == "__main__":
    # Test code
    csv_file = "geonames-all-cities-with-a-population-1000.csv"
    a = load_lookup_from_file(csv_file)
    pprint(a)
