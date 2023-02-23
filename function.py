import requests
import json
import datetime

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
    date_gmt = f'{date_raw.strftime("%a")}, {date_raw.strftime("%d")} {date_raw.strftime("%b")} {date_raw.strftime("%Y")} {date_raw.strftime("%X")} + GMT'

    return date_gmt

def list_board (board_last_get) :
    url_board = url.default + endpoint.board
    headers = {"If-Modified-Since":board_last_get}
    response = requests.get(url_board, headers=headers)
    # check if mongodb entry have update
    # append / insert new entry to mongodb board
    # response_board store the return code
    return response

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

