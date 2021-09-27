import sys
sys.path.append('/home/hui/cron_python_scripts')
from cron_helper import Logger

import requests




log = Logger(__file__ or '.')



try:
    res = requests.get('https://ucsb-641309.workflowcloud.com/forms/05598009-e8ba-40d4-ae36-eff7e8260631')
    token = ''
    for i in res.text[res.text.find('token: "')+8:]:
        if i =='"':break
        token += i
    log('Fetched token.')
except Exception as e:
    log(f'Failed to get token; {e}')
    exit(0)


url = 'https://ucsb-641309.workflowcloud.com/api/v3/form/Submit/05598009-e8ba-40d4-ae36-eff7e8260631'

headers = {
"accept": "application/json, text/plain, */*",
"accept-encoding": "gzip, deflate, br",
"accept-language": "en-US,en;q=0.9",
"authorization": f"Bearer {token}",
"cache-control": "no-cache",
"content-type": "application/json",
"origin": "https://gbo-app-znc.nintex.io",
"pragma": "no-cache",
"referer": "https://gbo-app-znc.nintex.io/",
"sec-ch-ua": '"Chromium";v="92", " Not A;Brand";v="99", "Google Chrome";v="92"',
"sec-ch-ua-mobile": '?0',
"sec-fetch-dest":'empty',
'sec-fetch-mode': 'cors',
'sec-fetch-site': 'cross-site',
'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/92.0.4515.107 Safari/537.36',
'x-ntx-correlation-id': '462e4b4e-fd48-46ea-be36-e9df858c152c',
'x-operation-id': '6e1d5eb0423749d1aa2604630845c2aa',
'x-tenancy': 'ucsb-641309.workflowcloud.com'
}



data = {'formData': {'se_text_short_1_j8d0s3p4nd': {'readOnly': False,
   'visible': True,
   'value': 'Hui',
   'type': 'string',
   'connectedVariableId': 'se_text_short_1_j8d0s3p4nd'},
  'se_text_short_2_PUOD4zWtq': {'readOnly': False,
   'visible': True,
   'value': 'Kang',
   'type': 'string',
   'connectedVariableId': 'se_text_short_2_PUOD4zWtq'},
  'se_email_1_LCtULPv1F': {'readOnly': False,
   'visible': True,
   'value': 'jskanghui@gmail.com',
   'type': 'string',
   'connectedVariableId': 'se_email_1_LCtULPv1F'},
  'se_text_short_1_NM0KBX3EVo': {'readOnly': False,
   'visible': False,
   'value': '',
   'type': 'string',
   'connectedVariableId': 'se_text_short_1_NM0KBX3EVo'},
  'se_text_short_1_lHndtk0XN': {'readOnly': False,
   'visible': False,
   'value': '',
   'type': 'string',
   'connectedVariableId': 'se_text_short_1_lHndtk0XN'},
  'se_choice_single_1_ogG6FyCMf': {'readOnly': False,
   'visible': False,
   'value': '',
   'type': 'string',
   'connectedVariableId': 'se_choice_single_1_ogG6FyCMf'},
  'se_yes_no_1_oLG67W5rs': {'readOnly': False,
   'visible': False,
   'value': False,
   'type': 'boolean',
   'connectedVariableId': 'se_yes_no_1_oLG67W5rs'},
  'se_child_1_name_copy_wGmkZba0D': {'readOnly': False,
   'visible': False,
   'value': '',
   'type': 'string',
   'connectedVariableId': 'se_child_1_name_copy_wGmkZba0D'},
  'se_text_short_1_Cj3rrMcAf': {'readOnly': False,
   'visible': False,
   'value': '',
   'type': 'string',
   'connectedVariableId': 'se_text_short_1_Cj3rrMcAf'},
  'se_child_1_classroom_copy_alEJPkMej': {'readOnly': False,
   'visible': False,
   'value': '',
   'type': 'string',
   'connectedVariableId': 'se_child_1_classroom_copy_alEJPkMej'},
  'se_are_you_bringing_another_child_today_copy_SAv4HV7yI': {'readOnly': False,
   'visible': False,
   'value': False,
   'type': 'boolean',
   'connectedVariableId': 'se_are_you_bringing_another_child_today_copy_SAv4HV7yI'},
  'se_child_2_name_copy_gafruC6VA': {'readOnly': False,
   'visible': False,
   'value': '',
   'type': 'string',
   'connectedVariableId': 'se_child_2_name_copy_gafruC6VA'},
  'se_text_short_1_NgYEV6teP': {'readOnly': False,
   'visible': False,
   'value': '',
   'type': 'string',
   'connectedVariableId': 'se_text_short_1_NgYEV6teP'},
  'se_child_1_classroom_copy_copy_XJ4HyUvKi': {'readOnly': False,
   'visible': False,
   'value': '',
   'type': 'string',
   'connectedVariableId': 'se_child_1_classroom_copy_copy_XJ4HyUvKi'},
  'se_choice_single_1_KbXGW8otj': {'readOnly': False,
   'visible': True,
   'value': 'No',
   'type': 'string',
   'connectedVariableId': 'se_choice_single_1_KbXGW8otj'},
  'se_symptoms_copy_W8gMxVifC': {'readOnly': False,
   'visible': True,
   'value': 'No',
   'type': 'string',
   'connectedVariableId': 'se_symptoms_copy_W8gMxVifC'},
  'se_diagnosed_copy_tapGurVY6': {'readOnly': False,
   'visible': True,
   'value': 'No',
   'type': 'string',
   'connectedVariableId': 'se_diagnosed_copy_tapGurVY6'},
  'se_choice_single_1_7d0sZo5YB': {'readOnly': False,
   'visible': True,
   'value': 'No',
   'type': 'string',
   'connectedVariableId': 'se_choice_single_1_7d0sZo5YB'},
  'se_choice_single_1_tL8Cv9Ef5': {'readOnly': False,
   'visible': False,
   'value': '',
   'type': 'string',
   'connectedVariableId': 'se_choice_single_1_tL8Cv9Ef5'},
  'se_choice_single_1_Io3R6bUIn': {'readOnly': False,
   'visible': False,
   'value': '',
   'type': 'string',
   'connectedVariableId': 'se_choice_single_1_Io3R6bUIn'}},
 'version': '2'}



try:
    res = requests.post(url,json=data,headers=headers,timeout=10)
    log(f'Formdata sent: {res.text}')
except Exception as e:
    log(f'Failed to send formdata; {e}')
    exit(0)
