import requests
import re

#USER REGISTRATION
URL = 'http://localhost:8000' 

def api_userRegistration(username, password):
    
    REGISTER_URL = URL + '/register'

    data = {
        "username": username,
        "password": password
    }

    response = requests.post(REGISTER_URL, json=data)
    if response.status_code == 201:
        return True
    else:
        return False

    # if re.match(USERNAME_PATTERN, username):
    #     if re.match(PASSWORD_PATTERN, password):
    #         pass        
    #     else: return { message: 'Incorrect password format' }
    # else:
    #     return { message: "Provide correct username format" }

def api_userLogin(username, password):

    LOGIN_URL = URL + '/login'

    data = {
        "username": username,
        "password": password
    }

    response = requests.post(LOGIN_URL, json = data)
    
    if response.status_code == 200:
        data = {
            "status": response.status_code,
            "response": response.json()['token']
        }
        return data  
    else:
        data = {
            "status": response.status_code,
            "response": response.json()["detail"]
        }

        return data
    # except:
    #     print('API call error!')


def api_getGOESYear(token):

    try:
        GET_GOES_URL = URL + '/geos_get_year'

        response = requests.get(GET_GOES_URL, headers={'Authorization': f'Bearer {token}'})
        yearList = []
        if response.status_code == 200:
            for item in response.json():
                yearList.append(item['year'])

            print(yearList)
            return yearList
        else:
            print(response.json())
            return []
    except:
        print("Issue with API call: geos_get_year")


def api_getGOESDay(token, year):
    try:
        GET_GOES_URL = URL + f'/geos_get_day/{year}'
        # print(token)
        response = requests.get(GET_GOES_URL, headers={'Authorization': f'Bearer {token}'})
        dayList = []
        if response.status_code == 200:
            for item in response.json():
                dayList.append(item['day'])

            # print(dayList)
            return dayList
        else:
            # print(response.json())
            return []
    except:
        print("Issue with API call: geos_get_day")

def api_getGOESHour(token, year, day):
    try:
        GET_GOES_URL = URL + f'/geos_get_hour/{year}/{day}'
        response = requests.get(GET_GOES_URL, headers={'Authorization': f'Bearer {token}'})
        hourList = []
        if response.status_code == 200:
            for item in response.json():
                hourList.append(item['hour'])

            # print(hourList)
            return hourList
        else:
            # print(response.json())
            return []
    except:
        print("Issue with API call: geos_get_hour")

def api_getNEXRADYear(token):

    try:
        GET_NEXRAD_URL = URL + '/nexrad_get_year'

        response = requests.get(GET_NEXRAD_URL, headers={'Authorization': f'Bearer {token}'})
        yearList = []
        if response.status_code == 200:
            for item in response.json():
                yearList.append(item['year'])

            print(yearList)
            return yearList
        else:
            print(response.json())
            return []
    except:
        print("Issue with API call: api_getNEXRADYear")

def api_getNEXRADMonth(token, year):
    try:
        GET_NEXRAD_URL = URL + f'/nexrad_get_month/{year}'
        # print(token)
        response = requests.get(GET_NEXRAD_URL, headers={'Authorization': f'Bearer {token}'})
        dayList = []
        if response.status_code == 200:
            for item in response.json():
                dayList.append(item['month'])

            # print(dayList)
            return dayList
        else:
            # print(response.json())
            return []
    except:
        print("Issue with API call: api_getNEXRADMonth")

def api_getNEXRADDay(token, year, month):
    try:
        GET_NEXRAD_URL = URL + f'/nexrad_get_day/{year}/{month}'
        response = requests.get(GET_NEXRAD_URL, headers={'Authorization': f'Bearer {token}'})
        dayList = []
        if response.status_code == 200:
            for item in response.json():
                dayList.append(item['day'])

            # print(hourList)
            return dayList
        else:
            # print(response.json())
            return []
    except:
        print("Issue with API call: api_getNEXRADDay")

def api_getNEXRADSites(token, year, month, day):
    try:
        GET_NEXRAD_URL = URL + f'/nexrad_get_sites/{year}/{month}/{day}'
        response = requests.get(GET_NEXRAD_URL, headers={'Authorization': f'Bearer {token}'})
        sitesList = []
        if response.status_code == 200:
            for item in response.json():
                sitesList.append(item['stationcode'])

            # print(hourList)
            return sitesList
        else:
            # print(response.json())
            return []
    except:
        print("Issue with API call: api_getNEXRADSites")

def api_getNEXRADSitesLoc(token):
    try:
        GET_NEXRAD_URL = URL + f'/get_nexrad_sites'
        response = requests.get(GET_NEXRAD_URL, headers={'Authorization': f'Bearer {token}'})
        sitesLocList = []
        if response.status_code == 200:
            return response.json()
        else:
            # print(response.json())
            return []
    except:
        print("Issue with API call: api_getNEXRADSitesLoc")

def api_NEXRADQueryFiles(token, year, month, day, site):
    try:
        GET_NEXRAD_URL = URL + f'/nexrad_query_files/{year}/{month}/{day}/{site}'
        response = requests.get(GET_NEXRAD_URL, headers={'Authorization': f'Bearer {token}'})
        if response.status_code == 200:
            print(response)
            print(response.json())
            return response.json()
        else:
            # print(response.json())
            return []
    except:
        print("Issue with API call: api_NEXRADQueryFiles")


def copyFileToBucket(token, product, year, day, hour, filename, source_bucket="noaa-goes18"):
    try:
        GET_GOES_URL = URL + f'/copy_file_s3/{source_bucket}/{product}/{year}/{day}/{hour}/{filename}'
        response = requests.get(GET_GOES_URL, headers={'Authorization': f'Bearer {token}'})
        
        if response.status_code == 200:
            return True
        else:
            return False
    except:
        print("Issue with API call: copyFileToBucket")

def copyNEXRADFileToBucket(token, year, month, day, site, filename, source_bucket="noaa-nexrad-level2"):
    try:
        GET_NEXRAD_URL = URL + f'/copy_nexrad_file_s3/{source_bucket}/{year}/{month}/{day}/{site}/{filename}'
        response = requests.get(GET_NEXRAD_URL, headers={'Authorization': f'Bearer {token}'})
        
        if response.status_code == 200:
            return True
        else:
            return False
    except:
        print("Issue with API call: copyFileToBucket")

def get_goes_by_filename(token, filename, source_bucket="noaa-goes18"):
    try:
        GET_GOES_URL = URL + f'/get_goes_by_filename/{source_bucket}/{filename}'
        response = requests.get(GET_GOES_URL, headers={'Authorization': f'Bearer {token}'})
        
        if response.status_code == 200:
            print(response)
            return response.json()['file_prefix']
        else:
            return False
    except:
        print("Issue with API call: get_goes_by_filename")


