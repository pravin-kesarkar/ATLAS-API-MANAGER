''' 
ATLAS MAIL BODY TEMPLATE
'''
import os
ATLAS_NOTIFICATION_SERVICE_ENDPOINT=os.environ.get("ATLAS_NOTIFICATION_SERVICE_ENDPOINT")
ATLAS_CLIENT_ID=os.environ.get("ATLAS_CLIENT_ID")
ATLAS_CLIENT_SECRET=os.environ.get("ATLAS_CLIENT_SECRET")

def mail_body(email_list,start_time,end_time,html_content):
    url =f'{ATLAS_NOTIFICATION_SERVICE_ENDPOINT}/v1/send-email'
    headers={'x-atlas-client-id':ATLAS_CLIENT_ID,
    'x-atlas-client-secret':ATLAS_CLIENT_SECRET,
    'Content-Type':'application/json'}
    email_list=[]
    email_list.append('pravin.kesarkar@acc.ltd')
    print(email_list)

    payload={   
    'to': ['atlas.support@acc.ltd'],
    'cc':[] ,
    'subject': 'API Faliure Notification',
    'template': 'apialerts',
    'payload': {
        "timestamp":str(start_time) + (end_time),
        "alerts":html_content
    },
    'priority': 'high',
    'attachments': []
    }
    # print('Payload Body ',payload)
    
    return payload,url,headers
