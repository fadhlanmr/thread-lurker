import datetime
import time
from pytz import timezone
import json
import api_call as acall
import os
from dotenv import load_dotenv
import pymongo

class env:
    load_dotenv()
    mongoURL = os.environ.get("MONGODB")
    mongodb = os.environ.get("THREAD_LURKER_DB")
    threadCollect = os.environ.get("THREAD_COLLECT")
    threadLastGet = os.environ.get("THREAD_LAST_GET")
    boardCollect = os.environ.get("BOARD_COLLECT")

class url:
    default = "a.4cdn.org"
    media = "i.4cdn.org"
    static_content = "s.4cdn.org"

class endpoint:
    thread = "threads.json"
    board = "boards.json"
    catalog = "catalog.json"
    archive = "archive.json"

# Set up collection for thread collect
client = pymongo.MongoClient(env.mongoURL)
db = client[env.mongodb]
board_collect = db[env.boardCollect]
thread_collect = db[env.threadCollect]
thread_last_get = db[env.threadLastGet]
est = timezone('EST')

def req (url, **kwargs):
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

class collector:
    def __init__(self, url, board_code, endpoint, current_time, sticky):
        self.url = url
        self.board_code = board_code
        self.endpoint = endpoint
        self.current_time = current_time
        self.sticky = sticky

    def time_get(self):
        time_local = datetime.datetime.now()
        format_time = time_local.strftime("%d/%b/%Y %H:%M:%S")

        return format_time

    def board_list(self):
        r"""Board Listing purpose, uses 4chan catalog api, return should be 
        an array of thread list
        """

        # Make request to 4chan API
        resp = req(self.url, board_code=self.board_code, endpoint=self.endpoint)
        data = json.loads(resp)
        # threads = []
        thread_list = []
        for item in data:
            # threads.extend(item['threads'])
            for listed in item['threads']:
                thread_id = listed['no']
                if 'sticky' in listed:
                    if self.sticky is False:
                        continue
                if 'closed' in listed:
                    thread_list.append({
                        'thread_id':listed['no'],
                        'thread_posted':listed['time'],
                        'thread_update':listed['last_modified'],
                        'thread_closed':listed['closed']})
                else:
                    thread_list.append({
                        'thread_id':listed['no'],
                        'thread_posted':listed['time'],
                        'thread_update':listed['last_modified']})
                    
                thread_exists = board_collect.find_one({'no': thread_id})
                if thread_exists:
                    # Update the reply if it has changed
                    board_collect.update_one({'no': listed['no']}, {'$set': listed})
                    print(f"[{self.current_time}] - Updated list: {listed['no']}; on: {listed['time']}")
                else:
                    # Insert the new reply
                    board_collect.insert_one(listed)
                    print(f"[{self.current_time}] - Inserted list: {listed['no']}; on: {listed['time']}")

        # turn list -> str, use encode utf to get bytes
        # json_utf8 = json.dumps(threads, ensure_ascii=False)

        # return thread_list for updating purpose
        return thread_list
    
    def thread_list(self):
        # initiate and get thread list
        try:
            thread_loop = self.board_list()
            for threads in thread_loop:
                time.sleep(0.05)
                self.current_time = self.time_get()
                time_est = int(time.mktime(datetime.datetime.now(est).timetuple()))
                thread_update_check = thread_last_get.find_one({"no": threads['thread_id']},{ "_id": 0, "thread_last_update": 1})
                if thread_update_check:
                    if thread_update_check['thread_last_update'] >= threads['thread_update']:
                        # skip if thread are up to date from last get
                        continue
                if 'thread_closed' in threads:
                    # skip if thread are closed
                    continue
                
                # insert the last get/update time instead
                thread_last_get_data = {
                    "thread_id": threads['thread_id'],
                    "thread_last_update": threads['thread_update'],
                    "thread_last_get": time_est
                }
                thread_resp = req(self.url, board_code=self.board_code, thread=threads['thread_id'])
                thread_resp_data = json.loads(thread_resp)
                # threads = []
                for post in thread_resp_data['posts']:
                    time.sleep(0.07)
                    self.current_time = self.time_get()
                    if 'resto' not in post:
                        raise ValueError(f"not a comment / reply to the thread, skipped id: {post['no']}")
                    if thread_collect.find_one({"no": post['no']}) :
                        # feature flag : 
                        # only run if post is sticky
                        # ===========================
                        if self.sticky is True:
                            thread_collect.update_one({"no": post["no"]}, {"$set": post})
                            print(f"[{self.current_time}] - Updated thread reply: {post['no']}; on: {post['time']}")
                        else:
                            continue
                    else:
                        thread_collect.insert_one(post)
                        print(f"[{self.current_time}] - Inserted thread reply: {post['no']}; on: {post['time']}")    
                
                # this last bit only insert thread that succesfully updated, else dont insert
                thread_last_get.insert_one(thread_last_get_data)
            time.sleep(2)
        except Exception as error:
            print(f"Request failed: {error}")
            
        # Wait before making next request
        time.sleep(60)

time_local = datetime.datetime.now()
time_now = time_local.strftime("%d/%b/%Y %H:%M:%S")

vt_thread_collect = collector(url.default, 'vt', endpoint.catalog, time_now, False)
vt_thread_collect.thread_list()