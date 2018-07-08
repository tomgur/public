import csv
import json

import requests

#############################################################################################
##########    This script will search the NASA image repository for SEARCH_TERM    ##########
##########    Create a CSV file called CSV_FILE_NAME                               ##########
##########    And add to that file, only images from the search result             ##########
##########    that are larger than IMAGE_SIZE_THREASHOLD                           ##########
#############################################################################################


SEARCH_TERM = "ilan ramon"
NASA_IMG_API = "https://images-api.nasa.gov/search?q=%s"
CSV_FILE_NAME = 'images.csv'
IMAGE_SIZE_THREASHOLD = 1024

image_search_result = requests.get(NASA_IMG_API % SEARCH_TERM)
image_json_result = json.loads(image_search_result.text)

images = image_json_result["collection"]["items"]
image_result_csv = open(CSV_FILE_NAME, 'w')
results_list = [['Nasa_id', 'kb']]
non_complient_results = [['Nasa_id', 'kb']]

counter = 0


def print_result_info(result):
    print('')
    print('-------------------------------------------------------')
    print('Search term [' + SEARCH_TERM + '] retrieved [' + str(len(images)) + '] images')
    print('[' + str(counter) + '] Images processed')
    print('[' + str(len(result)-1) + '] Images matching the size criterion')
    print('[' + str(len(non_complient_results)-1) + '] Images did NOT match the size criterion')
    print('Compliant results saved as CSV in file: ' + CSV_FILE_NAME)
    print('-------------------------------------------------------')


def getSize(image):
    # Get the image metadata
    metadata_url = image['href'].replace('collection', 'metadata')
    # Make metadata JSON
    metadata = json.loads(requests.get(metadata_url).text)
    # Read file size
    file_size = metadata['File:FileSize']
    # Read NASA_ID of image
    nasa_id = image['data'][0]['nasa_id']
    # If the file size attribute contains the string 'MB' - convert to kb
    fixed = [int(s) for s in file_size.split() if s.isdigit()]
    if file_size.upper().count('MB') > 0:
        fixed = file_size.split(' MB')
        results_list.append([nasa_id, int(float(fixed[0])*1024)])
        print('Added [' + nasa_id + '] - Size: [' + str(float(fixed[0])*1024) + ' kb]', flush=True)
    # Filesize is not in MB
    else:
        # Assuming the number is in KB, compare to 1024 (if larger, add to result, if not...)
        if fixed[0] >= IMAGE_SIZE_THREASHOLD:
            results_list.append([nasa_id, fixed[0]])
            print('Added [' + nasa_id + '] - Size: [' + str(fixed[0]) + ' kb]', flush=True)
        else:
            print('Skipped [' + nasa_id + '] - reason [' + str(fixed[0]) + ' <= ' + str(IMAGE_SIZE_THREASHOLD) + '] ')
            non_complient_results.append([nasa_id, str(fixed[0])])


for image in images:
    getSize(image)
    counter += 1

with image_result_csv:
    csvwriter = csv.writer(image_result_csv)
    csvwriter.writerows(results_list)

print_result_info(results_list)
