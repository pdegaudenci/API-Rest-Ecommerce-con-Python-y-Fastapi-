import logging
import logging.handlers
import sys

LOGGER_NAME= 'logger'
LOG_FOLDER = './utils'
LOG_FILE = 'API.log'
LOG = LOG_FOLDER + LOG_FILE
ROTATE_TIME = 'midnight'
LOG_LEVEL = logging.DEBUG
LOG_COUNT = 5
LOG_FORMAT = '%(asctime)s %(levelname)s %(message)s'

try:
    logger = logging.getLogger(LOGGER_NAME)
    loggerHandler = logging.handlers.TimedRotatingFileHandler(filename=LOG , when=ROTATE_TIME, interval=1, backupCount=LOG_COUNT)
    formatter = logging.Formatter(LOG_FORMAT)
    loggerHandler.setFormatter(formatter)
    logger.addHandler(loggerHandler)
    logger.setLevel(LOG_LEVEL)
except Exception as error:
    print("Error with logs: %s" % (str(error)))
    sys.exit()


logging.basicConfig(format='%(asctime)s --> %(levelname)s:%(message)s',filename='utils/logapi.log', encoding='utf-8', level=logging.DEBUG,filemode='a')


logger = logging.getLogger(__name__)
logger.setLevel("INFO")

