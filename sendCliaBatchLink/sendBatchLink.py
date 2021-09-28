import sys
from dotenv import load_dotenv
load_dotenv()

sys.path.append('/home/hui/cron_python_scripts')
sys.path.append('../')
from cron_helper import Logger,dirname,sendEmail    

log = Logger(__file__ or '.')

try:
    
    from pathlib import Path
    import json
    from firebaseClient import Firebase
    from datetime import datetime, timedelta
    import os
    from croniter import croniter
    import time
except Exception as e:
    log(f'Failed to import module: {e}')

log('Starting script')




def date():
    return datetime.now().strftime('%m/%d')


def ISO_Hours_Later(hours):
    t = datetime.utcnow() + timedelta(hours=int(hours))
    return t.strftime('%Y-%m-%dT%H:%M:%S.000Z')




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
            log(f'{attempt} Error in request: grpu: {batch["group"]}: {e}')
        finally:
            time.sleep(3)
            attempt -= 1
    return None
        



def formatBatch(batch):
    return {
        'group': batch['group'],        
        'note': f'{date()} Batch Order',
        'exp': ISO_Hours_Later(batch.get('expInHours',24)),
        'forwardEmail': batch.get('forwardEmail',[]),
    }


def main(testConfig=False,mode='prod'):
    log('Starting  main function')
    firebase =  Firebase(username=os.getenv('FIREBASE_USERNAME'), password=os.getenv('FIREBASE_PASSWORD'),mode=mode)
    firebase.start()
    config = load_config()
    notice = [f"{date()} Create Batch Link"]
    for c in config:
        try:
            cron = c['cron']
            if (croniter.match(cron, datetime.now())):
                batch = formatBatch(c)
                if testConfig:
                    log(f'Send batch Link Request: {batch}')
                else:
                    url = ''
                    # url = sendBatchLink(batch,firebase)
                    notice.append(f'Created batch {batch["group"]}: {url or "!!!!create url failed!!!!"}')
                    time.sleep(1)
            else:
                log(f'Skip send link to {c["group"]}')
                notice.append(f'Skip group {c["group"]}, cron: {c["cron"]}')
                if testConfig:
                    batch = formatBatch(c)
                    log(f'Not sent batch Link Request: {batch}')
        except Exception as e:
            log(f'Failed to get batch link for {c["group"]}: {e}')    
    try:
        #sendEmail('Batch Link Url Notice', '\n'.join(notice), to=['jskanghui@gmail.com'])        
        pass
    except:
        log('Send notification email error')
    
    

"""
config format:
{
    group: name of the group,
    expInDays: how many days to expire the batch.
    email: the email of the user to receive batch url email. This email must be a valid portal user email. 
    forwardEmail: [{name,email}] // additional emails to forward the link to.
    
}

Use cron to run the script

59 12 * * 1-5 python3  /home/hui/cron_python_scripts/sendCliaBatchLink/sendBatchLink.py

"""


if __name__ == "__main__":
    log('Starting script 2')
    if len(sys.argv)>1:
        log(f'Test config file {sys.argv}', )
        main(testConfig=True,mode=sys.argv[1])
    else:
        main(mode='prod')
    
    
    
    





