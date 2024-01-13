from opensearchpy import OpenSearch
from datetime import datetime, timedelta,date
from config import *
from notification import *
from template import *
import pymysql
import requests
import json
import pandas as pd
date=date.today()

current_datetime = datetime.now()

# Subtract 10 minutes
new_datetime = current_datetime - timedelta(minutes=500)

start_time=current_datetime.strftime("%Y-%m-%d %H:%M:%S")
end_time=new_datetime.strftime("%Y-%m-%d %H:%M:%S")

print(f'start_date= {start_time}  end time:- {end_time}')


open_search_query={
    "query":{
        "bool":{
            "filter":[
                {
                    "range": {
                        "status_code": {
                        "gte": 400,
                        "lte": 500
                            }
                        }
                },
                {
                    "range": {
                    "createdAt": {
                    "gte": end_time,
                    "lte": start_time
                    }
                }

                }

            ]
        }
    },
    "aggs":{
        "api_id_agg": {
        "terms": {
        "field": "api_id",
        "size": 200
      }
    }

    }
}

def atlas_db_con():
    #atlas db connection
    try:
        conn = pymysql.connect(host=atlas_db_cread['host'],user=atlas_db_cread['user'], password =atlas_db_cread['password'], db='atlas_db')
        curs = conn.cursor()
    except Exception as e:
        print(f'Unable to connect Atlas DB :- {e}')
    return curs,conn

def open_search_con():
    #open search connection
    try:
        open_search_endpoint = open_search_cread['opensearch_endpoint']
        opensearch_user = open_search_cread['opensearch_user']
        opensearch_password = open_search_cread['opensearch_password']
        auth = (opensearch_user, opensearch_password)
        client = OpenSearch(hosts=open_search_endpoint,http_compress=True,http_auth=auth,use_ssl=True,verify_certs=True)
    except Exception as e:
        print(f'Failed to connect opensearch due to  :- {e} ')
    return client

def getEmailList():
    #get email cc list from db
    try:
        curs,conn=atlas_db_con()
        query = "select email from atlas_db.user where status='ACTIVE' and user_type='ADMIN'"
        curs.execute(query)
        rows = curs.fetchall()
        email_list=[]
        for row in rows:
            email_list.append(list(row)[0])
        conn.close()
    except Exception as e:
        print('Error in getEmailList() FAILED TO GET EMIAL_LIST FROM DB DUE TO ',e)
    return email_list

def report_gen():
    atlas_failed_name=[]
    atlas_failed_count=[]
    df=None
    df_column=['API NAME','API FAILED COUNT']
    # main fucnction
    try:
        opensearch_client=open_search_con()
        cur,conn=atlas_db_con()
        try:
            response = opensearch_client.search(body=open_search_query,index="apiinsights")
            api_id_count = response['aggregations']['api_id_agg']['buckets']
        except Exception as e:
            print('Failed to get data from open search {e}')
        for api_data in api_id_count:
            api_id=api_data['key']
            #get api name from atlas db
            cur.execute(f"select name from apis where id='{api_id}' ")
            api_name=cur.fetchall()
            if api_name:
                api_failed_count=api_data['doc_count']
                atlas_failed_name.append(api_name[0][0])
                atlas_failed_count.append(str(api_data['doc_count']) + ' Times Failed in last 15 MIN.')

        if atlas_failed_name:
            # Creating a DataFrame
            data = {'API NAME': atlas_failed_name, 'API FAILED COUNT': atlas_failed_count}
            df = pd.DataFrame(data)
            print(df)
            api_name=api_name[0][0]
            failed_count=api_data['doc_count']
        conn.close()

    except Exception as e:
        print(f'Failed to generate report due to {e}')
    return df,atlas_failed_name

def Failed_Notification():

    #EMAIL ATLAS TEMPLATE
    df,atlas_failed_name=report_gen()
    email_list=getEmailList()
    try:
        subject='ATLAS API FAILED NOTIFICATION'
        if atlas_failed_name:
            html_content = df.to_html(index=False)
            payload,url,headers=mail_body(email_list,start_time,end_time,df)
            print(payload)

            # payload=json.dumps(payload)

            x = requests.post(url,headers=headers, data = payload,timeout=30)
            response=x.json()
            print('response',response)
            send_mail(subject,html_content)
        else:
            print('NO DATA FOUND ...')
    except Exception as e:
        print('Failed to sent notification',e)

Failed_Notification()
