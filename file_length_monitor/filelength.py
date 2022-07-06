import os


from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import Mail
from dotenv import load_dotenv
from datetime import datetime

from pathlib import Path

load_dotenv() 



def date(x):
    return f"{datetime.now().strftime('%Y-%m-%d %A, %H:%M:%S ')}: {x}\n"

def log(msg):
    print(msg)
    logfile.write(date(msg))
    

    

def checkFileLen(folder,thre=200):
    total = 0
    filec = []
    for root, dir, files in os.walk(folder):
        for name in files:
            p = os.path.join(root ,name)
            p = '/'.join(p.replace(folder,'/QMS').split('\\'))
            total+=1
            if len(p)>=thre and (p not in FileLengthLog):
                filec.append(p)
    log(f'Checked total of {total} files.')
    log(f'{len(filec)} new files length > {thre}.')
    filec.sort(key=lambda x:len(x), reverse=True)
    for i in filec:
        log(i)
    return filec
    

def composeEmail(filec):
    filetoolong = '\n'.join(
    f'<p>Length: {len(i)}, File: {i}</p>' for i in filec
    )
    html_content = f'''
    <p>Some file name length in Cloud station QMS folder is too long:</p>
    {filetoolong}
    <p>Please take a look.</p>
    '''
    return html_content

def sendEmail(html, to):
    message = Mail(
        from_email='hui.kang@aptitudemedical.com',
        to_emails=to,
        subject='Cloud Station Filename length warning',
        html_content=html
    )
    try:
        sg = SendGridAPIClient(os.environ.get('SENDGRID_KEY'))
        response = sg.send(message) 
        log(f'Send warning to {len(to)} recipients')
    except Exception as e:
        log(f"Send grid error: {e.message}")
        
        
if __name__ == '__main__':
    file = Path(__file__).parent / 'log.txt'
    try:
        with open(file,'r') as f:
            FileLengthLog = f.read()
    except:
        FileLengthLog = ''
            
    logfile =  open(file,'a')

    folder = os.environ.get("FILE_NAME_LENGTH_FOLDER")
    thre = os.environ.get("FILE_NAME_LENGTH_THRESHOLD")

    longfile = checkFileLen(folder,thre=int(thre))

    to = ['wentao.shi@aptitudemedical.com','tyler.chozinski@aptitudemedical.com','erika.wells@aptitudemedical.com']

    if longfile:
        msg = composeEmail(longfile)
        
        sendEmail(msg,to)
        
    logfile.close()
 
