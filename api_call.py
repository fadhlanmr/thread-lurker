import requests
import json
import datetime

def unix_to_gmt (unix_num) :
    date_raw = datetime.datetime.fromtimestamp(unix_num)
    date_gmt = f'{date_raw.strftime("%a")}, {date_raw.strftime("%d")} {date_raw.strftime("%b")} {date_raw.strftime("%Y")} {date_raw.strftime("%X")} GMT'

    return date_gmt

def call_api (url, endpoint=None, unix=None, board_code=None, thread=None) :
    if(board_code is not None):
        if(thread is not None):
            url_call = f"http://{url}/{board_code}/thread/{thread}.json"
        else:
            url_call = f"http://{url}/{board_code}/{endpoint}"
    else:
        url_call = f"http://{url}/{endpoint}"
    try:
        if(unix is not None):
            last_get = unix_to_gmt(unix)
            headers = {"If-Modified-Since":last_get}
            response = requests.get(url_call, headers=headers)
        else:
            response = requests.get(url_call)
        response.raise_for_status()
        #below refers to requests stored status codes https://github.com/psf/requests/blob/main/requests/status_codes.py
        if response.status_code == requests.codes.ok :
            api_output = response.json()
        else :
            api_output = response.status_code
        
        return api_output

    except requests.exceptions.RequestException as e:
        print(f'Request failed: {e}')

#call_api(url.default, endpoint.catalog, unix_to_gmt(lgb), board_code='vt')

def list_thread (urls, endpoints, board_2_code, thread_last_get) :
    url_thread = f'{urls}/{board_2_code}/{endpoints}'
    headers = {"If-Modified-Since":thread_last_get}
    response = requests.get(url_thread, headers)
    # clean some column
    # response_thread store the cleaned response
    return response

def list_single_thread (urls, endpoints, board_2_code, thread_code, thread_last_get) :
    url_thread = f'{urls}/{board_2_code}/thread/{thread_code}'
    headers = {"If-Modified-Since":thread_last_get}
    response = requests.get(url_thread, headers)
    # clean some column
    # response_cleaned store the cleaned response
    return response