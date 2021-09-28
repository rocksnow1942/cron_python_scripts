file = open('/home/hui/cron_python_scripts/sendCliaBatchLink/testCron.txt','a')
file.write('=================================\n')
counter = 1
file.write(f'step {counter}\n')

import sys
sys.path.append('/home/hui/cron_python_scripts')
from cron_helper import Logger,dirname,date

import time
import requests
from pathlib import Path




file.write(date('later \n'))
file.write(date(f'{__file__} \n'))

log = Logger(__file__)

try:
    log('test message')
except Exception as e:
    file.write(date(f'later write message {e}\n'))


file.write(date('later write message \n'))

file.write(date(f'{dirname(__file__)} \n'))