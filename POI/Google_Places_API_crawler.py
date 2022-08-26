import requests
import pandas as pd
import json
import time

def Google_Places_API_crawler():

    radius = 500

    df = pd.read_csv('csv_files/station_info.csv')
    print(df)

    my_API_key = 'API_key'

    for s in range(len(df)):

        total_results = []
        print('station_name:', df.iloc[s, 2])
        print('lat, lng: {}'.format(str(df.iloc[s, 3]) + ', ' + str(df.iloc[s, 4])))
        print('{} / {}'.format(s + 1, len(df)))

        url = 'https://maps.googleapis.com/maps/api/place/nearbysearch/json?location=' + str(df.iloc[s, 3]) + ',' + str(df.iloc[s, 4]) + '&radius=' + str(radius) + '&rankBy=google.maps.places.RankBy.DISTANCE&key=my_API_key&language=zh-TW'
        print(url)

        payload = {}
        headers = {}

        response = requests.request('GET', url, headers = headers, data = payload).json()

        if response and response.get('status') == 'REQUEST_DENIED':
            print(response)
            continue
        elif response and response.get('status') != 'ZERO_RESULTS':

            total_results += response['results']

            while(True):

                if 'next_page_token' in response:
                    print('It has next_page_token!')
                    next_token = response['next_page_token']    
                    url = 'https://maps.googleapis.com/maps/api/place/nearbysearch/json?location=' + str(df.iloc[s, 3]) + ',' + str(df.iloc[s, 4]) + '&pagetoken=' + next_token + '&key=my_API_key'
                    time.sleep(5)
                    response = requests.request('GET', url, headers = headers, data = payload).json()
                    if response and response.get('status') == 'REQUEST_DENIED':
                        print(response)
                        sys.exit(1)
                    elif response and response.get('status') != 'ZERO_RESULTS':
                        total_results += response['results']
                else:
                    break

            # print('total_results:')
            # print(total_results)
            print('len(total_results):')
            print(len(total_results))
            response['results'] = total_results

            output_filename = 'json_files/s_' + str(s + 1) + '.json'
            with open(output_filename, 'w', encoding = 'UTF-8') as f:
                json.dump(response, f, indent = 2)
