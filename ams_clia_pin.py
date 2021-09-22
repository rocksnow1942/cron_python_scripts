import sys
sys.path.append('/home/hui/cron_python_tasks')
from cron_helper import Logger
import time
import requests

log = Logger(__file__ or '.')


url = "https://us-central1-ams-clia.cloudfunctions.net/api/webhook/webhooktest"

try:
    t = time.monotonic()
    res = requests.post(url, json={'hello':'OK'})
    log(f'Pin Success. Response time: {time.monotonic() - t}')
except Exception as e:
    log(f'Ping error: {e}')
    

