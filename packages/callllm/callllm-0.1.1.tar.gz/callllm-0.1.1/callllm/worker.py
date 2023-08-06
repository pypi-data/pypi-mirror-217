
import sys
import json
import time
import requests
import gevent
from gevent import Greenlet

from .tasks import add_task, get_task, empty


class Worker(Greenlet):

    def __init__(self, api_key=None, api_hoster=None, max_retries=5, rate_limit=None):
        Greenlet.__init__(self)
        self.api_key = api_key
        if api_hoster == 'huggingface':
            self.auth = dict(headers={"Authorization": f"Bearer {api_key}"})
            self.auth.update({'headers': {'Content-Type': 'application/json'}})
        else:
            raise NotImplementedError(f'api_hoster {api_hoster} not implemented')
        self.max_retries = max_retries
        self.rate_limit = rate_limit
        self.counter = 0
        self.counter_start_time = time.time()

    def _run(self):
        while not empty():
            url, kwargs, callback, retries = get_task()
            
            kwargs.update(self.auth)
            kwargs['data'] = json.dumps(kwargs['data'])

            try:
                response = requests.request("POST", url, **kwargs)
            except requests.RequestException as e:
                sys.stderr.write("Error requesting %s: %s, " % (response.full_url, e.message))

                if retries < self.max_retries:
                    # Retry...
                    sys.stderr.write("retrying...\n")
                    add_task(url, kwargs, callback, retries + 1)
                else:
                    # Give up
                    sys.stderr.write("giving up...\n")

            else:
                # Invoke callback
                if callable(callback):
                    callback(response, self)
                
                # Stay within rate limits
                if self.rate_limit is not None:
                    self.throttle()
                   
        sys.stderr.write("%s exiting...\n" % str(self))

    def __str__(self):
        return f'Worker({self.api_key})'
    
    def throttle(self):
        if self.counter >= self.rate_limit and time.time() - self.counter_start_time < 60:
            time_to_sleep = 60 - (time.time() - self.counter_start_time)
            gevent.sleep(time_to_sleep)
            self.counter = 0
            self.counter_start_time = time.time()
        elif self.counter >= self.rate_limit and time.time() - self.counter_start_time >= 60:
            self.counter = 0
            self.counter_start_time = time.time()
        else:
            self.counter += 1