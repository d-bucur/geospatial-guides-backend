import logging

from config import running_on_appengine

LOG_LEVEL = logging.DEBUG


if running_on_appengine():
    import google.cloud.logging
    client = google.cloud.logging.Client()
    client.setup_logging(log_level=LOG_LEVEL)
    logging.debug("Using stackdriver logging")
else:
    logging.basicConfig(level=LOG_LEVEL)
    logging.debug("Using std logging")
