import os
import glob
import re
from kml2g1000 import export
import fas


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
    tn = tn.upper()
    if re.fullmatch("^([A-Z]|[0-9]){6}$", tn):
        pdata = fas.findPlaneData(tn)
    else:
        print("ERROR: Invalid tail number. Exiting...")
    
    
    

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
    print("\t\t2. Find files direectly on flightaware.com")
    option = input("$: ")
    
    if option == '1':
        local()
    elif option == '2':
        remote()
    else:
        print("Invalid option. ")