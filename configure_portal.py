# Script to read list of groups from a csv and create them on the portal.
from arcgis.gis import *
import csv
import pandas as pd
import time

try:

    url = ""
    user = ""
    password = ""

    print("\n")
    # print(">>>>>>>>>>>>>>>>>>>>> ---------- <<<<<<<<<<<<<<<<<<<<<")
    print("STARTING AUTOMATED CONFIGURATION OF ARCGIS ENTERPRISE")
    # print(">>>>>>>>>>>>>>>>>>>>> ---------- <<<<<<<<<<<<<<<<<<<<<")


    print("\n\n\n")
    print(">>>>>> ---- <<<<<<")    
    print("CREATING GROUPS...")
    print(">>>>>> ---- <<<<<<") 


    print("=====================================================================\n")

    # connect to gis
    gis = GIS(url, user, password, verify_cert=False)

    df = pd.read_csv("groups_normal.csv")
    df1 = df[['title','access', 'sortField']]
    df1 = df1.rename(columns = {
    'title':'TITLE',
    'access':'ACCESS',
    'sortField':'SORTFIELD'})    
    print(df1)
    print("=====================================================================\n")    

    time.sleep(1)

    with open("groups_normal.csv", 'r') as groups_csv:
        groups = csv.DictReader(groups_csv)
        for group in groups:
            try:
                print("\nCreating group: "+ group['title'] + "  ##  success")
                result = gis.groups.create_from_dict(group)

            except Exception as create_ex:
                print("Error... ", str(create_ex))

except Exception as create_ex:
    print("Error... ", str(create_ex))



try:
    user_count = 20

    print("\n\n\n")
    print(">>>>>>>>> ----- <<<<<<<<<")
    print("CREATING USER ACCOUNTS...")
    print(">>>>>>>>> ----- <<<<<<<<<") 

    print("=====================================================================\n")
    # Connect to the GIS
    gis = GIS(url, user, password, verify_cert=False)

    df = pd.read_csv("users_large.csv")
    df1 = df[['Firstname','email', 'role']]

    df1 = df1.rename(columns = {
    'Firstname':'First Name',
    'email':'E-mail',
    'role':'Role'})
    print(df1.head(user_count))    
    print("=====================================================================\n")
    # time.sleep(0.5)

    # loop through and create users
    with open("users_large.csv", 'r') as users_csv:
        users = csv.DictReader(users_csv)
        iterations = user_count
        count = 0
        for user in users:
            count+=1
            if count == iterations:
                break
            try:
                print("\nCreating user: " + user['username'] + " ## success")
                result = gis.users.create(username=user['username'],
                                          password=user['password'],
                                          firstname=user['Firstname'],
                                          lastname=user['Lastname'],
                                          email=user['email'],
                                          role =user['role'])
                if result:
                    groups = user['groups']
                    group_list = groups.split(",")

                    print("\t Adding to groups:  # {0}".format(group_list))

                    # Search for the group
                    for g in group_list:
                        group_search = gis.groups.search(g)
                        if len(group_search) > 0:
                            try:
                                group = group_search[0]
                                groups_result = group.add_users([user['username']])
                                if len(groups_result['notAdded']) == 0:
                                    # print(g + " # ")
                                    pass

                            except Exception as groups_ex:
                                print("\n \t Cannot add user to group ", g, str(groups_ex))
            except Exception as add_ex:
                print("\nCannot create user: " + user['username'])
                print("\n")
                print(str(add_ex))

except Exception as create_ex:
    print("Error... ", str(create_ex))


try:

    print("\n")
    print("=====================================================================\n")
    print("SETTING LOGO, BANNER, AND BACKGROUND...")


    print("\t Setting background...")
    gis.admin.ux.set_background(background_file='dc_background.jpg')

    print("\t Setting banner...")
    gis.admin.ux.set_banner(banner_file = 'dc_banner5.jpg')

    print("\t Setting logo...")
    gis.admin.ux.set_logo(logo_file='dc_logo.jpg')

    print("\t Setting description...")
    gis.admin.ux.name = 'Federal GIS'
    gis.admin.ux.description = 'Spatial information portal for the Federal Community'
    gis.admin.ux.description_visibility = True


except Exception as create_ex:
    print("Error... ", str(create_ex))