import os
import json
from datetime import datetime
import sys
# file size function
def file_size(file_name): 
        statinfo = os.stat(file_name) 
        statinfo =statinfo.st_size/1000/1000
        return round(statinfo,3)
# file size function completed

# date
today = datetime.now().strftime('%Y_%m_%d')
# date

# File names
site_name = 'century21global'
raw_filename = site_name + '.json'
native_ascci_file = site_name + '_temp.json'
clean_data_file = site_name + '_' + today + '.json'
zipped_file_name = clean_data_file + '.zip'
meta_file = site_name + '_metadata.txt'
# file name assigning finished

# Export Data
os.system('db details use in export' %(raw_filename))
# Export complete

# Native to Aacii
os.system('native2ascii -encoding UTF-8 -reverse %s > %s ' % (raw_filename, native_ascci_file))
# Native to Aacii finished

# validate json
exce = False
f = open(native_ascci_file)
lines = f.readlines()
no_of_lines = len(lines)
for i,line in enumerate(lines):
    try:
        item = json.loads(line)
    except Exception as e:
        exce = True
        print(str(e) + 'in line %s' % str(i+1))
f.close()
if exce == True:
    print('Invalid JSON')
    sys.exit()
else:
    print ('JSON validated...!')
# Json validation finished

# remove _id 
os.system('awk \'{gsub("\\"_id[^,]*,", "");print}\' %s > %s' % (native_ascci_file, clean_data_file))
# removed _id

# zip the file
os.system('zip %s %s' % (zipped_file_name, clean_data_file))
# zipped file

# create meta file
# with open(meta_file, "a") as f:
with open("users.txt", "a") as f:
    f.write('filename : %s' % zipped_file_name +'\n')
    f.write('Dropbox path : '+'\n')
    # f.write("Total data size: %s MB" % file_size(clean_data_file) +'\n')
    f.write("Zipped data size: %s MB" % file_size(zipped_file_name) +'\n')
    f.write("Total data count: %s" % no_of_lines +'\n')
    f.write("Data format: json.zip" +'\n')
    f.write('Date transferred: %s' % today +'\n')
    f.write(''+'\n')
# created meta file

# remove unwanted files 
os.system('rm %s %s' % (raw_filename,native_ascci_file))
# removed unwanted files 
