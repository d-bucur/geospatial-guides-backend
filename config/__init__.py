import os


def running_on_appengine():
    return os.getenv('GAE_ENV', '').startswith('standard')


import config.logs
