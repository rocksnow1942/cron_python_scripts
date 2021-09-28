file = open('/home/hui/cron_python_scripts/sendCliaBatchLink/testCron.txt','a')
file.write('\n')
counter = 1
file.write(f'step {counter}\n')

import sys
sys.path.append('/home/hui/cron_python_scripts')

try:
    from cron_helper import Logger
except Exception as e:
    file.write(f'cron_helper.py not found{e}\n')
import time
import requests

file.write('later \n')
file.write(f'{__file__} \n')

log = Logger()

log('test message')

file.write('later write message \n')