import os
import sys
import glob
import re
from kml2g1000 import export
import fas
import pandas as pd
import copy
from datetime import datetime


def local():
    searchDir = input('Show me the directory containing the track files (defaults to user Downloads folder): ')
    if searchDir == '':
        searchDir = os.path.join(os.path.expanduser('~'), 'Downloads')
    
    for kml in glob.glob('*.kml', root_dir=searchDir):
        print(f"Exporting {kml} to csv...")
        export(searchDir + "/" + kml)
        print("Done!")

    print(f"A total of {len(glob.glob('*.kml', root_dir=searchDir))} files in '{searchDir}' folder were exported to csv.")
    
def remote():
    tn = input("Enter the tail number of your aircraft : ")
    
    print(f"Finding history for aircraft: {tn}...")
    tn = tn.upper()
    pdataRAW = fas.findPlaneData(tn)
    
    pdataDisplay = copy.deepcopy(pdataRAW)
    _data = ["Date", "Time", "Departure", "Destination"]

    for flight in pdataDisplay:
        flight[0] = datetime.strptime(flight[0], "%Y%m%d").strftime("%m/%d/%Y")
        flight[1] = datetime.strptime(flight[1][:-1], "%H%M").strftime("%H:%M " + "Z")
    
    historyData = pd.DataFrame(pdataDisplay, columns=_data)
    print(f"Found {len(pdataRAW)} flights for {tn} within the last 14 days:")
    print("#"*100)
    print(historyData)
    
    flight = input("Enter the flight you would like to download: ")
    if not re.fullmatch("^([0-9]){1}$|^([1-9]){2}$", flight) or int(flight) >= len(pdataRAW):
        print("ERROR: Invalid flight number. Exiting...")
        sys.exit(1)
    
    print(f"Downloading flight {flight}...")
    trackRAW = fas.downloadKML(tn, pdataRAW, int(flight))
    with open("track.kml", "wb") as f:
        f.write(trackRAW.content)
    print("Done!")
    
    print("Exporting track to csv...")
    try:
        export("track.kml")
        print("Done!")
    except:
        print("There was an error exporting the .kml to .csv...")
    finally:
        print("Cleaning up...")
        os.remove("track.kml")
        print("Done!")
    
    print(f"Exported flight on {pdataDisplay[int(flight)][0]} from {pdataDisplay[int(flight)][2]} to {pdataDisplay[int(flight)][3]} to csv.")
        
def fURL():
    url = input("Enter the URL of the flight you would like to download (should end with '.../tracklog'): ")
    print("Downloading flight...")

    try:
        r = fas.downloadFLink(url)
    except INCORRECTURL:
        print("That is not the expected URL. Please check the docs for which url to input")

    with open ("track.kml", "wb") as f:
        f.write(r.content)
    print("Done!")
    
    print("Exporting track to csv...")
    try:
        export("track.kml")
        print("`track.csv` has been exported to the Downloads folder.")
    except:
        print("There was an error converting the track file.")
    finally:
        print("Cleaning up track.kml...")
        os.remove("track.kml")
        print("Done!")
    

if __name__ == '__main__':
    print("""##################_____################_____####################_____##################
#################/\####\##############/\####\##################/\####\#################
################/::\____\############/::\####\################/::\####\################
###############/:::/####/############\:::\####\##############/::::\####\###############
##############/:::/####/##############\:::\####\############/::::::\####\##############
#############/:::/####/################\:::\####\##########/:::/\:::\####\#############
############/:::/____/##################\:::\####\########/:::/##\:::\####\############
###########/::::\####\##################/::::\####\######/:::/####\:::\####\###########
##########/::::::\____\________########/::::::\####\####/:::/####/#\:::\####\##########
#########/:::/\:::::::::::\####\######/:::/\:::\####\##/:::/####/###\:::\#___\#########
########/:::/##|:::::::::::\____\####/:::/##\:::\____\/:::/____/##___\:::|####|########
########\::/###|::|~~~|~~~~~########/:::/####\::/####/\:::\####\#/\##/:::|____|########
#########\/____|::|###|############/:::/####/#\/____/##\:::\####/::\#\::/####/#########
###############|::|###|###########/:::/####/############\:::\###\:::\#\/____/##########
###############|::|###|##########/:::/####/##############\:::\###\:::\____\############
###############|::|###|##########\::/####/################\:::\##/:::/####/############
###############|::|###|###########\/____/##################\:::\/:::/####/#############
###############|::|###|#####################################\::::::/####/##############
###############\::|###|######################################\::::/####/###############
################\:|###|#######################################\::/____/################
#################\|___|################################################################
#######################################################################################""")
    print()
    print("Welcome to the KML to G1000 converter!")
    print("This program will convert all KML files in a folder to CSV files that can be imported into the Garmin G1000.")
    print("Please select an option:")
    print("\t\t1. Convert files in a local directory")
    print("\t\t2. Find files directly on flightaware.com")
    print("\t\t3. Input a URL")
    option = input("$: ")
    
    if option == '1':
        local()
    elif option == '2':
        remote()
    elif option == '3':
        fURL()
    else:
        print("Invalid option. Exiting...")
        sys.exit(1)