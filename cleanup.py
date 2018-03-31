# Script to clean up the users, content and groups created for demo

from arcgis.gis import *
import argparse

try:
    #region read cmd line args
    url = ""
    user = ""
    password = ""


    # Read the log file in append mode

    print("\n")
    print("=====================================================================\n")
    print("RUNNING CLEANUP\n")

    # connect to gis
    gis = GIS(url, user, password, verify_cert=False)

    # region remove groups
    group_list = gis.groups.search("owner:" + user)
    print("Deleting groups\n")
    print("---------------\n")

    for group in group_list:
        try:
            print("\nDeleting " + group.title + "  ##  ")
            group.delete()
            print("success")
        except Exception as group_del_ex:
            print("Error deleting : " + str(group_del_ex))
    # endregion

    #region remove content for each user
    print("\n\nDeleting user content\n")
    print("---------------------\n")
    user_list = gis.users.search("")
    try:
        for user in user_list:
            print('\nUser : ' + user.username + " # ")
            if user.fullName in ['Administrator', 'Esri', 'Esri Navigation', 'anieto']:
                print('skipped')
                continue

            user_content = gis.content.search('owner:{0}'.format(user.username))
            for item in user_content:
                print('\nDeleting : '+ item.title + " # ")
                delete_status = item.delete()
                print(str(delete_status)+ " | ")
            print('empty')

    except Exception as content_del_ex:
        print(str('content_del_ex'))
    #endregion

    # region remove users
    user_list = gis.users.search()
    print("\n\nDeleting users\n")
    print("--------------\n")

    for user in user_list:
        if user.username == "admin" or user.username.startswith("esri_") or user.username.startswith("AVWORLD") or user.username == "anieto":
            continue
        else:
            print("\nDeleting " + user.username + "  ##  ")
            user.delete()
            print("success")
    # endregion



    # region reset ux
    print("\n\nResetting theme, banner, and logo\n")
    print("--------------\n") 
    gis.admin.ux.set_background(background_file=None, is_built_in=False)
    gis.admin.ux.set_background(is_built_in=True)

    gis.admin.ux.set_banner(banner_file = 'organizationSplash.jpg')
    # endregion

    gis.admin.ux.name = 'ArcGIS Enterprise'
    gis.admin.ux.description = '<br>'
    gis.admin.ux.description_visibility = False

    print("\n All clean")

except Exception as create_ex:
    print("Error... ", str(create_ex))