from pathlib import Path
from datetime import datetime
import os
from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import Mail



def date(x):
    return f"{datetime.now().strftime('%Y-%m-%d %A, %H:%M:%S ')}: {x}\n"
    
def Logger(file,name='log.txt'):
    folder = dirname(file)
    error = ''
    attempt = 5
    while attempt:
        try:
            fp = open(folder/name,'a')
            fp.write(date('='*50))
            if (error):
                fp.write(date(error))                
            break
        except Exception as e:
            error = f"Error Opening File {folder/name}: {e}\n"
            name = name + '_'
            attempt -= 1
            
    def log(msg):
        print(msg)
        fp.write(date(msg))
    return log

def dirname(file):
    return Path(file).parent



def sendEmail(subject, html, to):
    message = Mail(
        from_email='hui.kang@aptitudemedical.com',
        to_emails=to,
        subject=subject,
        html_content=html
    )    
    sg = SendGridAPIClient(os.environ.get('SENDGRID_KEY'))
    return sg.send(message)         
        
    