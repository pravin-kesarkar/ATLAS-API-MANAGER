''' 
ATLAS MAIL BODY TEMPLATE
'''

def mail_body(email_list,start_time,end_time,html_content):
    url ='/v1/send-email'
    headers={'x-atlas-client-id':'Atlas-Developer-Portal-Microservice',
    'x-atlas-client-secret':'C?NPwXUW=Gc5pNsC?no9xnAr*cjX}3JN7>~-dc27Bv2sV+cWD3*9DH2',
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
