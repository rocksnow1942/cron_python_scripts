from pathlib import Path
from datetime import datetime

def date(x):
    return f"{datetime.now().strftime('%Y-%m-%d %A, %H:%M:%S ')}: {x}\n"
    
def Logger(file,name='log.txt'):
    file = Path(file).parent / 'log.txt'
    fp = open(file,'a')
    def log(msg):
        print(msg)
        fp.write(date(msg))
    return log
    