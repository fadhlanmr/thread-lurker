import time
import json
import api_call as acall

class url :
    default = "a.4cdn.org"
    media = "i.4cdn.org"
    static_content = "s.4cdn.org"

class endpoint :
    thread = "threads.json"
    board = "boards.json"
    catalog = "catalog.json"
    archive = "archive.json"

def req (url, **kwargs) :
    r"""Request 4chan API.
    :param url: URL for the 4chan API.
    :param \*\*kwargs: Optional arguments that ``api_call`` takes.
    :return: :JSON type object response
    :rtype: json

    Usage::
      >>> import function
      >>> req = function.req(url.default, last_get=lgb, thread=endpoint.board)
      >>> req
      <Response JSON>
    """
    return acall.call_api(url=url, **kwargs)

def board_list(url, **kwargs) :
    r"""Board Listing purpose, uses 4chan catalog api, return should be 
    a dict of thread list
    """

    # Make request to 4chan API
    resp = req(url, **kwargs)
    data = json.loads(resp)
    threads = []
    thread_list = []
    for item in data:
        threads.extend(item['threads'])
        for listed in item['threads']:
            if 'sticky' not in listed:
                thread_list.extend({'thread_id':item['no'],'thread_posted':item['time'],'thread_update':item['last_modified']})

    # turn list -> str, use encode utf to get bytes
    json_utf8 = json.dumps(threads, ensure_ascii=False)
    #
    # threads[] json to mangodb
    #

    # return thread_list for updating purpose
    return thread_list

while True:
    # initiate and get thread list
    thread_loop = []
    thread_loop.extend(board_list(url.default, board_code="vt", endpoint=endpoint.catalog))
    
    for threads in thread_loop :
        time.sleep(2)


    # Wait before making next request
    time.sleep(60)

