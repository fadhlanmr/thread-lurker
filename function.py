import time
import json
import api_call as acall

lgb = 1675420911
lgt = 1675420911

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

while True:
    # Make request to 4chan API
    resp = req(url.default, board_code="vt", endpoint=endpoint.catalog)
    # print(resp)
    data = json.loads(resp)
    threads = []
    for item in data:
        threads.extend(item['threads'])

    json_utf8 = json.dumps(threads, ensure_ascii=False)
    print(json_utf8)

    # Wait before making next request
    time.sleep(60)

