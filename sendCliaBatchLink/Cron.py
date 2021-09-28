import sys
sys.path.append('/home/hui/cron_python_scripts')
from cron_helper import Logger
import time
import requests

log = Logger(__file__ or '.')

log('Run script')