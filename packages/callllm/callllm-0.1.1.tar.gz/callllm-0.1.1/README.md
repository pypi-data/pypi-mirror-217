# CallLLM

Asynchronous, concurrent requests to the LLM REST API, that respect its's rate limits, using [gevent](http://www.gevent.org/) and [requests](http://docs.python-requests.org/).

This library is for conducting experiments using LLM APIs.

Currently, it only supports the HuggingFace API. I plan to add OpenAI support when I actually need it.

See 'example.py' for a working example.

## Installation
Simply:
    $ pip install callllm 

