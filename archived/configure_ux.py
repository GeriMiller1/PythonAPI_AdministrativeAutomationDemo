# Script to read list of groups from a csv and create them on the portal.
from arcgis.gis import *
import csv

try:

    # url = "https://idt.esri.com/portal"
    # user = "anieto"
    # password = "an198432"

    url = "https://ngse-dev.eastus.cloudapp.azure.com/portal"
    user = "anieto"
    password = "an198432"


    print("\n")
    print("=====================================================================\n")
    print("CONFIGURING ARCGIS ENTERPRISE UX")

    # connect to gis
    gis = GIS(url, user, password, verify_cert=False)

    # Set Portal properties
	gis.admin.ux.name = 'LA PWD GIS'
	gis.admin.ux.description = 'Spatial information portal for the Public Works Department of the city of Los Angeles'
	gis.admin.ux.description_visibility = True


except Exception as create_ex:
    print("Error... ", str(create_ex))