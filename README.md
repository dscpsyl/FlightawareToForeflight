# kml2g1000
A CLI app to Ccnvert FlightAware KML tracklogs to G1000 CSV for importing to ForeFlight for those who do not have ADSB.

# Dependencies
* Python 3.10
* lxml
* glob
* requests

## Usage
1. Download KML tracklogs from flightaware.com
2. Run `kml2g1000.py` and input the director where the files are located. Or you can search for your flight on flightaware right in the app.
3. Upload resulting csv files to where you can easily access them on your iPad (e.g. Google Drive)
4. Import into ForeFight from More > Track Logs ([link](https://www.foreflight.com/support/support-center/category/about-foreflight-mobile/360042091114))
