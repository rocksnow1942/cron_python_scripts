
import sys
sys.path.append('/home/hui/cron_python_scripts')
from cron_helper import Logger,sendEmail,dirname

log = Logger(__file__ or '.')
log('Starting script')

from dotenv import load_dotenv
load_dotenv()

from pathlib import Path
import json
from firebaseClient import Firebase
from datetime import datetime, timedelta
import os
from croniter import croniter
import time


def date():
    return datetime.now().strftime('%m/%d')



def load_config():
    config_file = dirname(__file__) / 'config.json'
    if not config_file.is_file():
        return []
    with open(config_file) as f:
        return json.load(f)


def sendBatchLink(batch,fire):
    attempt = 5
    while attempt > 0:
        try:
            res = fire.post('/scr/script/createBatchBookingUrl', json=batch)
            if res.status_code == 200:
                batch_url = res.json()['url']
                log(f'Got batch url: {batch_url}')
                return batch_url
            else:
                log(f'{attempt} Failed to get batch url for {batch["group"]}: {res.text}')
        except Exception as e:
            log(f'{attempt} Error in request: group: {batch["group"]}: {e}')
        finally:
            time.sleep(5)
            attempt -= 1
    return None


def loginFirebase(mode):
    attempt = 10
    while attempt > 0:
        try:
            fire = Firebase(username=os.getenv('FIREBASE_USERNAME'), password=os.getenv('FIREBASE_PASSWORD'),mode=mode)
            fire.start()
            log('Firebase started')
            return fire
        except Exception as e:
            time.sleep(15)
            log(f'Error in loginFirebase: {e}')
            attempt -= 1    
    return None


def main(testConfig=False,mode='prod'):

    fire = loginFirebase(mode)
    if not fire:
        log('Failed to login to firebase')
        sendEmail('[CRITICAL]Batch Link Url Creation', "<h1>!!!Can't Log in Firebase !!!</h1>", to=ADMIN_EMAIL)
        return
    
    config = load_config()
    notice = [f"{date()} Create Batch Link"]
    for batch in config:
        try:            
            if testConfig:
                log(f'Send batch Link Request: {batch}')
            else:
                url = ''
                url = sendBatchLink(batch,fire)
                notice.append(f'Created batch {batch["group"]}: {url or "!!!!create url failed!!!!"}')
                time.sleep(1)
            
        except Exception as e:
            log(f'Failed to get batch link for {batch["group"]}: {e}')    
    try:
        sendEmail('Batch Link Url Notice', '\n'.join(f"<p>{l}</p>" for l in notice), to=ADMIN_EMAIL)
        pass
    except:
        log('Send notification email error')
    


"""
config format:
{
    group: name of the group,
    expInHours: how many hours to expire the batch.
    forwardEmail: [{name,email}] // additional emails to forward the link to.
}

Use cron to run the script

59 12 * * 1-5 python3  /home/hui/cron_python_scripts/sendCliaBatchLink/sendBatchLink.py

"""
ADMIN_EMAIL = ['hui.kang@aptitudemedical.com']

if __name__ == "__main__":    
    if len(sys.argv)>1:        
        main(testConfig=True,mode=sys.argv[1])
    else:
        main(mode='prod')
    
    
    
    





