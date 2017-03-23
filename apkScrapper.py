import requests
import re


# categories retrieved from Google Play Store
CATEGORIES = ['COMMUNICATION','ART_AND_DESIGN','AUTO_AND_VEHICLES','COMICS', 'FOOD_AND_DRINK', 'LIBRARIES_AND_DEMO', 'ENTERTAINMENT','EDUCATION'
              ,'FINANCE', 'HOUSE_AND_HOME', 'VIDEO_PLAYERS', 'LIFESTYLE', 'BOOKS_AND_REFERENCE', 'MEDICAL', 'GAME', 'FAMILY']

# look for the pattern in the html page returned and extract the package name of the app
APK_ID_PATTERN = r'<a class="title" href="/store/apps/details\?id=(\w+\.(\w+\.)*\w+)"'

# number of apps, which may vary depending on the category
# Exceding a certain threshold (130 at the time of writing) may result in an html page containing very few apps. 
START = 0
NUM = 120

def get_top_app_url(categorie)->str:
    return 'https://play.google.com/store/apps/category/'+categorie+'/collection/topselling_free'

def get_topselling_free_apps(url, start, num)->'response':
    return requests.get(url, params = {'start': start, 'num': num})


apk_id_regex = re.compile(APK_ID_PATTERN)
apk_ids = set()

for categorie in CATEGORIES:
    print("processing... "+categorie)
    response = get_topselling_free_apps(get_top_app_url(categorie), start =START, num =NUM)
    found_strings = apk_id_regex.findall(response.text)
     #eleminate duplicates
    current_apks = [ id for id, _ in found_strings if id not in apk_ids ]
    apk_ids = apk_ids | set(current_apks)

    print("number of currents apks... " + str(len(current_apks)))
    print( str(len(apk_ids)) + " apks retreived so far ...")
    #create a file and store the IDs in it
    print("writing to file")
    with open('topselling_free_'+categorie+'.txt','w') as ids_file:
        for id in current_apks:
            ids_file.write(id+"\n")
