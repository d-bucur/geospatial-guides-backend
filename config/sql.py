import logging

from config import running_on_appengine

# configs removed
USERNAME = 'USERNAME'
PASSWORD = 'PASSWORD'
HOST = 'HOST'
DB_NAME = 'DB_NAME'
CLOUD_SQL_INSTANCE = 'CLOUD_SQL_INSTANCE'

# Change code and use direct connection if having trouble with cloudsql proxy (when running locally)
# DIRECT_CONNECTION = 'postgresql://%s:%s@%s/%s' % (USERNAME, PASSWORD, HOST, DB_NAME)

# Use cloudsql proxy by default
if running_on_appengine():
    SQL_PROXY_CONNECTION = 'postgresql+pg8000://%s:%s@/%s?unix_sock=/cloudsql/%s/.s.PGSQL.5432' % (
        USERNAME, PASSWORD, DB_NAME, CLOUD_SQL_INSTANCE)
    logging.debug('Using socket connection through Cloud SQL Proxy')
else:
    SQL_PROXY_CONNECTION = 'postgresql+pg8000://%s:%s@/%s' % (
        USERNAME, PASSWORD, DB_NAME)
    logging.debug('Using TCP connection through Cloud SQL Proxy')
    #SQL_PROXY_SOCKET = expanduser("~") + '/cloudsql'

URI = SQL_PROXY_CONNECTION
