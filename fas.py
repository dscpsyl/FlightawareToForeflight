import requests
from bs4 import BeautifulSoup 

URL = "https://flightaware.com/live/flight/"

def findPlaneData(tailnum):
    """Looks through global URL for history of aircraft based on the tailnumber through flightaware.com. There is a limitation of 14 days when
    using this function because of the way flightaware.com stores data.

    Args:
        tailnum (str): The six character tail number of the aircraft.

    Returns:
        dataPoints (list): A list of lists containing the data points for each flight. Each list entry contains the following data points:
            [0] = Date in YYYMMDD format
            [1] = Time in HHMMZ UTC format
            [2] = Departing airport
            [3] = Destination airport
    """
    
    page = requests.get(URL + tailnum + "/history")
    soup = BeautifulSoup(page.content, "html.parser")
    table = soup.findAll(class_="nowrap")

    if not table:
        print("No data found for this tail number. Please try downloading the files manually. Exiting...")

    dataPoints = []
    for t in table:
        rawData = t.find("a", href=True)
        dataPoint = str(rawData["href"]).split("/")
        dataPoints.append(dataPoint[-4:])

    return dataPoints
    
    
