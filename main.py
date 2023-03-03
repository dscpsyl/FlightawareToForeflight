import os
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
    tn = input("Enter the 6 character tail number of your aircraft : ")
    print(f"Finding history for aircraft: {tn}...")
    tn = tn.upper()
    if re.fullmatch("^([A-Z]|[0-9]){6}$", tn):
        pdataRAW = fas.findPlaneData(tn)
    else:
        print("ERROR: Invalid tail number. Exiting...")
    
    pdataDisplay = copy.deepcopy(pdataRAW)
    _data = ["Date", "Time", "Departure", "Destination"]

    for flight in pdataDisplay:
        flight[0] = datetime.strptime(flight[0], "%Y%m%d").strftime("%m/%d/%Y")
        flight[1] = datetime.strptime(flight[1][:-1], "%H%M").strftime("%H:%M " + "Z")
    
    historyData = pd.DataFrame(pdataDisplay, columns=_data)
    print(f"Found {len(pdataRAW)} flights for {tn} within the last 14 days:")
    print("#"*100)
    print(historyData)
    
    
    

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
    option = input("$: ")
    
    if option == '1':
        local()
    elif option == '2':
        remote()
    else:
        print("Invalid option. ")