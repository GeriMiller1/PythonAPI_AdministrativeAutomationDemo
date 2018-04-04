from arcgis.gis import GIS
import time

print("\n")
# print(">>>>>>>>>>>>>>>>>>>>> ---------- <<<<<<<<<<<<<<<<<<<<<")
print("Starting Process...\n")
# print(">>>>>>>>>>>>>>>>>>>>> ---------- <<<<<<<<<<<<<<<<<<<<<")
# region: Authenticate
source_password = ""
source_username = ""
source_url = ""
target_password = ""
target_username = ""
target_url = ""

source_group_title = ""   # Example: "Transportation Group"

source = GIS(source_url, source_username, source_password)
target = GIS(target_url, target_username, target_password, verify_cert=False)

source_group = source.groups.search("title:{0}".format(source_group_title, outside_org = True)[0]

source_items = source_group.content()

print("\tCreating target groups...")
import tempfile
if not target.groups.search('Vector Basemaps'):
    try:
        with tempfile.TemporaryDirectory() as temp_dir:
            thumbnail_file = source_group.download_thumbnail(temp_dir)
            
            #create a group in the target portal with all the properties of the group in the source
            target_group = target.groups.create(title = source_group.title,
                                                 tags = source_group.tags,
                                                 description = source_group.description,
                                                 snippet = source_group.snippet,
                                                 access = source_group.access, 
                                                 thumbnail= thumbnail_file,
                                                 is_invitation_only = True,
                                                 sort_field = 'avgRating',
                                                 sort_order ='asc',
                                                 is_view_only=True)

            
    except Exception as e:
        # print('Group {} could not be created'.format(source_group.title))
        # print(e)
        pass
else:
    print('\tGroup {} already exists in the portal'.format(source_group.title))
    target_group = target.groups.search('Vector Basemaps')[0]

#making a list for the items to be cloned in the target portal
items_to_be_cloned = list(source_items)

print("\tScanning items in target portal...")
#checking for the presence of the item in the target portal 
for item in source_items:
    searched_items = target.content.search(query='title:'+item.title, item_type = item.type)   
    
    for s_item in searched_items:
        
        if s_item.title == item.title:
            
            #if an item is not a part of the group in the target portal then share it 
            if s_item not in target_group.content():
                s_item.share(groups= [target_group])
            
            #remove the already existing item from the list of items to be cloned
            items_to_be_cloned.remove(item)                    
                     
            break

print("\tPublishing cloned content...")
#cloning all items that were not present on the portal before
for item in items_to_be_cloned:    
    try:
        with tempfile.TemporaryDirectory() as temp_dir:
            thumbnail_file = item.download_thumbnail(temp_dir)
            metadata_file = item.download_metadata(temp_dir)
            target_item_properties = {'title': item.title,
                                      'tags': item.tags,
                                      'text':item.get_data(True),
                                      'type':item.type,
                                      'url':item.url
                                     }       
            #create an item
            target_item = target.content.add(target_item_properties, thumbnail=thumbnail_file)
            
            
            #share that item with the group on the target portal
            target_item.share(groups=[target_group])
            print("\tpublished {0}  |   added to: {1}".format(item.title, target_group))
            
            
    except Exception as e:
        # print('Item {} could not be created in the target portal'.format(item.title))
        # print(e)
        pass


# print("\tSetting featured content...")
traffic_group = target.groups.search("Transportation Analysis")[0]
target.admin.ux.featured_content = {'group':traffic_group}

for i in range(20):
  time.sleep(2)
  print("\tSupplemental cloned item {0} transferred successfully...".format(str(i)))