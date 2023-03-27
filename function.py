import time
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
    req(url.default, board_code="vt", endpoint=endpoint.catalog)

    # Process posts as needed
    for x in req:
        # Do something with post data
        print(x['com'])

    # Wait before making next request
    time.sleep(60)

