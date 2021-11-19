from threading import Thread
import requests
import time
from getpass import getpass
from datetime import datetime, timedelta

prodURL = 'https://us-central1-ams-clia.cloudfunctions.net'
devURL = 'http://localhost:5000/ams-clia/us-central1'


class Firebase:
    nonDefaultFunctions = ['scr', ]

    def __init__(self, username='user@ams.com', password='', mode='prod',):
        self.username = username
        self._url = devURL if mode == 'dev' else prodURL
        self.expire = 0
        self.token = ""
        self.stopRefresh = False
        self.refreshThread = None
        if password:
            self.pwd = password
        else:
            self.pwd = getpass(f'Enter password for {username}')
        self.fetchToken()
        if not self.token:
            raise RuntimeError('Firebase is not logged in.')

    @property
    def headers(self):
        return {'Authorization': f'Bearer {self.token}'}

    def url(self, sub: str):
        """
        if sub domain starts with any know non api sub domain,
        use it directly, 
        otherwise, use api sub domain by append api to sub.         
        """
        if not sub.startswith('/'):
            raise RuntimeError('sub domain must start with /')
        if sub.split('/')[1] in self.nonDefaultFunctions:
            return self._url + sub
        return f"{self._url}/api{sub}"

    def fetchToken(self):
        res = requests.post(self.url('/user/login'),
                            json={'email': self.username, 'password': self.pwd})
        if res.status_code == 200:
            self.token = res.json()['token']
            # each token is valid for 55 minutes.
            self.expire = time.time() + 60 * 50
        else:
            self.token = ""

    def refreshToken(self):
        "refreshtoken every 1hour"
        while True:
            if self.stopRefresh:
                break
            if self.expire < time.time():
                self.fetchToken()
            time.sleep(0.5)

    def start(self):
        if self.refreshThread and self.refreshThread.is_alive():
            self.refreshThread.join()
        self.stopRefresh = False
        self.refreshThread = Thread(target=self.refreshToken, daemon=True)
        self.refreshThread.start()
        while not self.token:
            time.sleep(0.1)

    def stop(self):
        self.stopRefresh = True
        # if self.refreshThread:
        #     self.refreshThread.join()

    def post(self, url, *args, **kwargs):
        return requests.post(self.url(url), *args, **kwargs, headers=self.headers)

    def get(self, url, *args, **kwargs):
        return requests.get(self.url(url), *args, **kwargs, headers=self.headers)

    def delete(self, url, *args, **kwargs):
        return requests.delete(self.url(url), *args, **kwargs, headers=self.headers)

    def put(self, url, *args, **kwargs):
        return requests.put(url, *args, **kwargs, headers=self.headers)


def date():
    return datetime.now().strftime('%m/%d')


def ISO_Hours_Later(hours):
    t = datetime.utcnow() + timedelta(hours=int(hours))
    return t.strftime('%Y-%m-%dT%H:%M:%S.000Z')


def formatBatch(batch):
    return {
        'group': batch['group'],
        'note': f'{date()} Batch Order',
        'exp': ISO_Hours_Later(batch.get('expInHours', 24)),
        'forwardEmail': batch.get('forwardEmail', []),
    }


if __name__ == "__main__":
    username = input('Enter user name:\n')
    fire = Firebase(username=username, mode='dev')


# format the order information here
# the group account point person will also receive the email,
# regardless of the forwardEmail settings here.
batchOrder = {
    "group": 'GS-DEMO',  # name of the group
    "expInHours": 24,  # expiration in hours
    "forwardEmail": [ # email addresses to forward to
        {
            "email": "jskanghui@gmail.com", 
            "name": "User"
        },
        {
            "email": "kanghui06@gmail.com", 
            "name": "Hui Kang"
        },
        {
            "email": "hui.kang@aptitudemedical.com", 
            "name": "Hui Kang"
        }
    ]
}

res = fire.post('/scr/script/createBatchBookingUrl',
                json=formatBatch(batchOrder))


if res.status_code == 200:
    print(res.json())
else:
    print(res.json())
