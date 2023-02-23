import requests
import json
import datetime

lgb = 1675420911
lgt = 1675420911

class lastGet :
    boards = lgb
    threads = lgt

class url :
    default = "a.4cdn.org"
    media = "i.4cdn.org"
    static_content = "s.4cdn.org"

class endpoint :
    thread = "threads.json"
    board = "boards.json"
    catalog = "catalog.json"
    archive = "archive.json"

def unix_to_gmt (unix_num) :
    date_raw = datetime.datetime.fromtimestamp(unix_num)
    date_gmt = f'{date_raw.strftime("%a")}, {date_raw.strftime("%d")} {date_raw.strftime("%b")} {date_raw.strftime("%Y")} {date_raw.strftime("%X")} GMT'

    return date_gmt

def call_api (last_get, urls, endpoints) :
    url_board = f"http://{urls}/{endpoints}"
    headers = {"If-Modified-Since":last_get}
    try:
        response = requests.get(url_board, headers=headers)
        response.raise_for_status()
        #below refers to requests stored status codes https://github.com/psf/requests/blob/main/requests/status_codes.py
        if response.status_code == requests.codes.ok :
            api_output = response.json()
        else :
            api_output = response.status_code
        
        return api_output

    except requests.exceptions.RequestException as e:
        print(f'Request failed: {e}')

print(call_api(unix_to_gmt(lgb), url.default, endpoint.board))

def list_thread (board_2_code, thread_last_get) :
    url_thread = f'{url.default}/{board_2_code}/{endpoint.catalog}'
    headers = {"If-Modified-Since":thread_last_get}
    response = requests.get(url_thread, headers)
    # clean some column
    # response_thread store the cleaned response
    return response

def list_single_thread (board_2_code, thread_code, thread_last_get) :
    url_thread = f'{url.default}/{board_2_code}/thread/{thread_code}'
    headers = {"If-Modified-Since":thread_last_get}
    response = requests.get(url_thread, headers)
    # clean some column
    # response_cleaned store the cleaned response
    return response