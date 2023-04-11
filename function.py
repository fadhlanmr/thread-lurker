import time
import json
import api_call as acall
import os
from dotenv import load_dotenv
import pymongo

class env :
    load_dotenv()
    mongoURL = os.environ.get("MONGODB")
    mongodb = os.environ.get("THREAD_LURKER_DB")
    threadCollect = os.environ.get("THREAD_COLLECT")
    boardCollect = os.environ.get("BOARD_COLLECT")

class url :
    default = "a.4cdn.org"
    media = "i.4cdn.org"
    static_content = "s.4cdn.org"

class endpoint :
    thread = "threads.json"
    board = "boards.json"
    catalog = "catalog.json"
    archive = "archive.json"

# Set up collection for thread collect
client = pymongo.MongoClient(env.mongoURL)
db = client[env.mongodb]
boardCollect = db[env.boardCollect]
threadCollect = db[env.threadCollect]

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
    an array of thread list
    """

    # Make request to 4chan API
    resp = req(url, **kwargs)
    data = json.loads(resp)
    # threads = []
    thread_list = []
    for item in data:
        # threads.extend(item['threads'])
        for listed in item['threads']:
            thread_id = listed['no']
            thread_exists = boardCollect.find_one({'no': thread_id})

            if 'sticky' not in listed:
                if 'closed' in listed:
                    # skip if sticky and closed 
                    thread_list.append({
                        'thread_id':listed['no'],
                        'thread_posted':listed['time'],
                        'thread_update':listed['last_modified'],
                        'thread_closed':listed['closed']})
                else:
                    # skip if sticky 
                    thread_list.append({
                        'thread_id':listed['no'],
                        'thread_posted':listed['time'],
                        'thread_update':listed['last_modified']})
            if thread_exists:
                # Update the reply if it has changed
                boardCollect.update_one({'no': listed['no']}, {'$set': listed})
                print(f"[{current_time}] - Updated list: {listed['no']}; on: {listed['time']}")
            else:
                # Insert the new reply
                boardCollect.insert_one(listed)
                print(f"[{current_time}] - Inserted list: {listed['no']}; on: {listed['time']}")

    # turn list -> str, use encode utf to get bytes
    # json_utf8 = json.dumps(threads, ensure_ascii=False)

    # return thread_list for updating purpose
    return thread_list

while True:
    tLocal = time.localtime()
    tCurrent = time.time()
    current_time = time.strftime("%d/%b/%Y %H:%M:%S", tLocal)
    # initiate and get thread list
    try:
        thread_loop = board_list(url.default, board_code="vt", endpoint=endpoint.catalog)
        for threads in thread_loop:
            # check if thread aren't outdated from last get
            thread_update_check = threadCollect.find_one({{"no": threads['thread_id']}},{ "_id": 0, "time": 1})
            print(thread_update_check, tCurrent)
            if thread_update_check['time'] <= tCurrent:
                print(thread_update_check, tCurrent)
                continue
            # check if thread aren't closed
            if 'thread_closed' in threads:
                continue
            
            thread_resp = req(url.default, board_code="vt", thread=threads['thread_id'])
            thread_resp_data = json.loads(thread_resp)
            # threads = []
            for post in thread_resp_data['posts']:
                if 'resto' in post:
                    if threadCollect.find_one({"no": post['no']}):
                        continue
                        # feature flag : 
                        # only run if post is sticky
                        # ===========================
                        # threadCollect.update_one({"no": post["no"]}, {"$set": post})
                        # print(f"[{current_time}] - Updated thread reply: {post['no']}; on: {post['time']}")
                    else:
                        threadCollect.insert_one(post)
                        print(f"[{current_time}] - Inserted thread reply: {post['no']}; on: {post['time']}")    
        time.sleep(2)
    except Exception as e:
        print(f"Request failed: {e}")
        
    # Wait before making next request
    time.sleep(60)