import pandas as pd
import cx_Oracle

import requests
from requests.exceptions import HTTPError
from urllib3.exceptions import InsecureRequestWarning
requests.packages.urllib3.disable_warnings(category = InsecureRequestWarning)

from datetime import datetime,date,timedelta
from time import time,ctime,sleep
import calendar

import re

from simple_salesforce import Salesforce
from simple_salesforce.exceptions import SalesforceMalformedRequest

from funcy import chunks
import aiohttp,asyncio 

from numpy import select,where,nan

from os.path import abspath, join, exists, dirname,isdir,basename
from os import mkdir

import logging
import logging.config

from shareplum import Site, Office365
from shareplum.site import Version
from pandas import ExcelWriter

from bs4 import BeautifulSoup as bs
import xmltodict as xd

from google.cloud import secretmanager

curr_dir = dirname(__file__)
rootFolder=abspath(join(curr_dir,'..'))
codeFolder = abspath(curr_dir)
# codeFolder = rootFolder
logFolder = abspath(join(codeFolder,'logs'))
inputFolder = abspath(join(codeFolder,'input files'))
outputFolder = abspath(join(codeFolder,'result files'))
plumeFolder = abspath(join(codeFolder, 'plume files'))

#improv API creds
improv_header = {
    "Authorization": "Basic aW1wcm92YXA6SlRBeGJZR3FjWkFUMnJ2"
}
improv_url = 'https://api.corp.intranet/Application/v1/Improv/'
improv_api_list = {
    'findUser': 'get',
    'getUserInfoByWtn': 'get',
    'getWtnByUsername':'get',
    'createAccount':'post',
    'updateUserAccount':'put'
}

lars_url = 'https://api.corp.intranet/Application/v1/LARS/subscriberManagement/'
lars_method = 'get'
lars_headers= { # prod
    'X-Application-Key': 'H8AM5JUQGaxNEmOZJQbxsMIDJfzoAxbp',    
}

lars_data = {
    'action' : 'ByWTN',
    'stat':'1',
    'applid': 'QFQUICKFIX_P'
}

# secret_file_path = abspath(join(dirname(''),'qf-secret-manager.json'))
# os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = secret_file_path

#db creds

def get_latest_secret(project_id, secret_id):  
    # Create the Secret Manager client.
    client = secretmanager.SecretManagerServiceClient()
    # Build the resource name of the secret.
    name = f"projects/{project_id}/secrets/{secret_id}/versions/latest"
    # Access the secret version.
    response = client.access_secret_version(name=name)
    # Return the decoded payload.
    return response.payload.data.decode('UTF-8')

def orcl_sf_conn():
    sales_oracle_conn  = cx_Oracle.connect("DAASBOT", "n4ts4rv2c4_3034", r"RACORAP16-SCAN.IDC1.LEVEL3.COM:1521/ASL01P_USERS") 
    return sales_oracle_conn

def orcl_daas_conn():
    daas_oracle_conn  = cx_Oracle.connect("DAASBOT", 
                                          get_latest_secret(project_id = "biwf-test", secret_id="dwops01p_users"), 
                                          r"racorap33-scan.corp.intranet:1521/dwops01p_users") 
    return daas_oracle_conn

def martens_conn():
    martens_conn  = cx_Oracle.connect("AC51216", "Mrtns!2024", r"racorap33-scan.corp.intranet:1521/dwpr01p_users") 
    return martens_conn

def sf_conn():
    url = 'https://ctl-fiber.my.salesforce.com/services/oauth2/token'
    params = {"grant_type": "password",
            "username":"qfqhuser_prod@lumen.com",
            "password":"QfQh2023Prod",
            "client_id":"3MVG9nkapUnZB56HQ6OpJKsXNoT64CpeLBR.cvpLL1nVP9RbG41P2_4f3mxPCoRIfA2Q2IsoCJctwQABgt9iK",
            "client_secret":"83FF3BBDB516839F6060A0C240BD545553E6BAAECFC5130F4C3F29420BC3A24D"
            }
    r = requests.post(url,params=params)
    access_token1 = r.json().get("access_token")

    sf=Salesforce(instance_url='https://ctl-fiber.my.salesforce.com',session_id=access_token1)
    return sf
    
def optius_conn():
    optius_oracle_conn = cx_Oracle.connect("IAAPP", "prd$02#JX243", r"racorap45-scan.corp.intranet:1521/svc_o2prod")
    oracle_c = optius_oracle_conn.cursor()
    return optius_oracle_conn

def time_taken(start,end):
    time_diff = end - start
#     rootLogger.info('time-diff',time_diff, sep=':')
    time_taken = f"{int(time_diff/86400)} days ,{int((time_diff%86400)/3600)} hours, {int((time_diff%3600)/60)} minutes, {int(time_diff%60)} seconds "
    return time_taken

def getCurrentDate():
    return date.today()

def getCurrentDateTime():
    dt = datetime.now()
    return dt.strftime('%Y-%m-%d %H:%M:%S')

def getObjType(obj):
    return str(type(obj)).split(' ')[1].split('.')[-1].replace("'","").replace('>','')

def html_parse(html_text) -> dict:
    parse_data = ('\n'.join(bs(html_text,'html.parser').stripped_strings)).split('\n')

    if parse_data[0] == 'LARS':
        parse_data.pop(0)

    # lars_response = { element.split('=')[0].strip() : element.split('=')[1].strip() 
    #                  for element in parse_data if element and element.split('=')}
    lars_response = { element.split('=')[0].strip() : element.split('=')[1].strip() 
                        for element in parse_data if element and element.split('=') and len(element.split('='))>1}
                
        
    if len(lars_response) == 0 and not lars_response :
        print("response in empty")
        return None
    else:
        return lars_response
    
# def sf_select(query : str) -> pd.DataFrame: 
#     rootLogger = logging.getLogger('rootLogger')
#     from json import dumps, loads
#     connection = sf_conn()
#     rootLogger.info(f"\nExecuting Query:\n{query}")
    
#     try:
#         df = pd.DataFrame(connection.query_all(query)['records'])
#         rootLogger.info(f"Query Result:{df.shape}")
#     except Exception as e:
#         rootLogger.info(str(e))
#         print(e)
#     if (df.shape[0]) > 0:
#         df.drop('attributes', axis=1, inplace=True)  # clean up from technical info
        
#         object_list=list(df.keys())
#         rootLogger.info(f"Getting Object List:{object_list}")
#         l=['int','str','float']

#         org_list=[]
#         for i in object_list:
#             k=getObjType(df.loc[0,i])        
#             if(k not in l):
#                 org_list.append(i)

#         if org_list:
#             rootLogger.info(f"Salesforce objects in query result:{org_list}")
#             df_fnl = df.drop(columns=org_list)

#             rootLogger.info("retrieving individual columns from each salesforce object")
#             for table in org_list:    
#                 df[table] = df[table].apply(dumps)
#                 df[table] = df[table].apply(loads)
#                 df_sub = pd.DataFrame(df[table].values.tolist()).drop(columns='attributes')
#                 col_list = df_sub.columns.values.tolist()
#                 col_list = [table+'_'+col for col in col_list]
#                 df_sub.columns = col_list
#                 rootLogger.info(f"Columns:{df_sub.columns.values.tolist()}")
#                 df_fnl = pd.concat([df_fnl,df_sub],axis=1)         
#             rootLogger.info(f"Final dataset result: {df_fnl.shape}")
#             df_fnl = df_fnl.reset_index()
#             return df_fnl
        
#         else:
#             df = df.reset_index()
#             return df
#     else :
#         rootLogger.info('No output from SF')
#         return pd.DataFrame()

def timezone_correction(dt):    
    if dt[0] is None or str(dt[0]) == 'Nil':
        print('Given date value is Null')
        return dt[0]
    if  dt[1] is None or str(dt[1]) == 'Nil' :
        print('Timezone is empty. Defaulting Timezone correction to -5 hours')
        return dt[0]-timedelta(hours=5)
    else:
        pattern = "(GMT[-+][0-9][0-9])"
        hours = re.findall(pattern,dt[1])
        cap = hours[0][3]
        hour = int(hours[0][4:])
        if cap == '-':
            return dt[0]-timedelta(hours=hour)
        elif cap == '+':
            return dt[0]+timedelta(hours=hour)

def sf_select(query : str) -> pd.DataFrame: 
#     rootLogger = logging.getLogger('rootLogger')
    from json import dumps, loads
    from numpy import setdiff1d
    connection = sf_conn()
    
    print(f"\nExecuting Query:\n{query}")
    try:
        sales_df = pd.DataFrame(connection.query_all(query)['records'])
    except Exception as e:
        print(e)
    if (sales_df.shape[0]) > 0:
        sales_df = sales_df.drop('attributes', axis=1)       
        col_list = sales_df.columns.values.tolist()    
        for col in col_list:            
            if any(isinstance(sales_df[col].values[i],dict) for i in range(0,len(sales_df[col].values))):
                sales_df = pd.concat([sales_df.drop(columns=[col]),sales_df[col].apply(pd.Series)\
                                .drop(columns='attributes',axis=1).add_prefix(col+'.')],axis=1)
                [col_list.append(i) for i in setdiff1d(sales_df.columns,col_list)]
        print(f"Query Result:{sales_df.shape}")
        
        if not(sales_df is None or sales_df.empty):
            sales_df.rename(columns={
                #SA columns
                'Appointment_Number_Text__c' : 'SA_NUM',
                'AppointmentNumber':'APPOINTMENT_NUMBER',
                'SchedStartTime' : 'SCHEDULED_START_TIME',
                'SchedEndTime' : 'SCHEDULED_END_TIME',
                'DueDate' : 'SA_DUE_DATE', 
                'ArrivalWindowStartTime':'ARV_WIN_START_TIME',
                'ArrivalWindowEndTime':'ARV_WIN_END_TIME',
                #'CreatedDate':'SA_CREATED_DATE',
                'Order_Number__c' : 'SF_ORDER_NUMBER', 
                # 'Scheduled_Timestamp__c':'SCHEDULED_TIME_STAMP',
                'Dispatch_Timestamp__c':'DISPATCH_TIME_STAMP',
                'ParentRecordId' : 'WO_ID',
                             
                #Account columns
                'AccountId':'ACCT_ID',
                'Account.Account_Number__c' : 'ACCOUNT_NUMBER', 
                'Account.Name' : 'ACCOUNT_NAME',
                'Account.Id' : 'ACCT_ID',
                'Account.CreatedDate' : 'ACCT_CREATED_DT',
                'Account.AccountStatus__c' : 'ACCOUNT_STATUS',
                'Account.Customer_Time_Zone__c' : 'CUST_TIME_ZONE',
                'Account.Migrated__c':'ACCOUNT_MIGRATED',
                'Account.DTN__c':'SF_DTN',
                'Account.SmartNID_Enabled__c':'SMARTNID_ENABLED',
                'Account.Service_Address__c':'ACCT_SERVICE_ADDRESS',
                'Account.Customer_Address__c':'CUSTOMER_ADDRESS',
                'Account.Location__Latitude__s' : 'SF_LAT_VALUE',
                'Account.Location__Longitude__s' : 'SF_LONG_VALUE',
                'Account.Polygon_ID__c':'SF_POLYGON_ID',
                'Account.Polygon_Status__c':'SF_POLYGON_STATUS',
                'Account.Estimated_Completion_Date__c':'SF_ECD',
                'vlocity_cmt__OrchestrationPlanId__r.vlocity_cmt__AccountId__r.Id' : 'ACCT_ID',
                'vlocity_cmt__OrchestrationPlanId__r.vlocity_cmt__AccountId__r.Account_Number__c' : 'ACCOUNT_NUMBER',
                'vlocity_cmt__OrchestrationPlanId__r.vlocity_cmt__AccountId__r.Name' : 'ACCOUNT_NAME',                                             
                'vlocity_cmt__OrchestrationPlanId__r.vlocity_cmt__AccountId__r.CreatedDate' : 'ACCT_CREATED_DT', 
                'vlocity_cmt__OrchestrationPlanId__r.vlocity_cmt__AccountId__r.AccountStatus__c' : 'ACCOUNT_STATUS',
                'vlocity_cmt__OrchestrationPlanId__r.vlocity_cmt__AccountId__r.Customer_Time_Zone__c' : 'CUST_TIME_ZONE',
  
                #Order columns
                'Order__r.Id' : 'ORDER_ID',
                'vlocity_cmt__OrchestrationPlanId__r.vlocity_cmt__OrderId__r.Id' : 'ORDER_ID',
                'vlocity_cmt__OrchestrationPlanId__r.vlocity_cmt__OrderId__r.OrderNumber' : 'ORDERNUMBER',                     
                'vlocity_cmt__OrchestrationPlanId__r.vlocity_cmt__OrderId__r.CreatedDate' : 'ORDER_CREATED_DT',
                'vlocity_cmt__OrchestrationPlanId__r.vlocity_cmt__OrderId__r.vlocity_cmt__OrderStatus__c' : 'ORDER_STATUS',
                'Order__r.OrderNumber':'SF_ORDER_NUMBER',
                'Order__r.vlocity_cmt__DueDate__c' : 'ORDER_DUE_DATE',
                'vlocity_cmt__DueDate__c' : 'ORDER_DUE_DATE',
                'Order__r.Px_Partner_ID__c':'ORDER_PARTNER',
                'Order__r.vlocity_cmt__OrderStatus__c' : 'SF_ORDER_STATUS',
                'Order__r.Service_Address__c' : 'ORDER_SERVICE_ADDRESS',

                #WO Columns  
                'WorkOrderNumber':'WO_NUM',
                'DTNField__c':'WO_DTN',                
                'DTN__c':'WO_DTN1',
                'Due_Date__c': 'WO_DUE_DATE',
                'Optical_Line_Terminal_OLT_CILLI__c':'WO_OLT',
                'Passive_Optical_Network_PON_Port__c':'WO_OLT_PORT',   
                'Wire_Center_CLLI__c':'WO_WIRE_CENTER',
                'Fiber_Distribution_Hub_FDH__c':'WO_FDH',
                'FDH_Feeder_Strand__c':'WO_FDH_FEEDER_STRAND',
                'FDH_Distribution_Strand__c':'WO_FDH_DISTRIBUTION_STRAND',
                'FAP_Distribution_Strand__c':'WO_FAP_DISTRIBUTION_STRAND',
                'Splitter_Port__c':'WO_SPLITTER_PORT',
                'Multiport_Service_Terminal_MST_Name__c':'WO_ACCESS_POINT',
                'Optical_Network_Terminal_ONT_Cust_Port__c':'WO_ONT_PORT',
                'ONT__c':'WO_ONT_TYPE',
                'Installed_ONT_Make__c':'WO_INSTALLED_ONT_MAKE',
                'Serving_Device_Make_Model__c':'WO_SERVING_DEVICE_MAKE_MODEL',
                'RONTA_ID__c':'WO_RONTA_ID',
                'Technology__c':'WO_TECHNOLOGY',
                'Multiport_Service_Terminal_Customer_Port__c':'WO_MST_CUST_PORT',
                'Class_of_Service_Update__c':'WO_PURCHASED_DATA_RATE',
                'OLT_Feeder_Strand__c':'WO_OLT_FEEDER_STRAND'  ,

                #ORCH PLAN 
                'vlocity_cmt__OrchestrationPlanId__c' : 'PLAN_ID'
            },inplace=True)     
            col_list = sales_df.columns.values.tolist()    
            #fixing data 
            if 'SF_DTN' in col_list: 
                sales_df['SF_DTN'] = sales_df['SF_DTN'].fillna('Nil')
                sales_df['SF_DTN'] = sales_df['SF_DTN'].astype(str)
                sales_df['SF_DTN'] = sales_df['SF_DTN'].apply(lambda x:str(x).replace('.0','') if str(x) not in [None,'None','nan',nan,'',' '] else x)
            
            if 'WO_DTN' in col_list and 'WO_DTN1' in col_list:
                sales_df['WO_DTN'] = sales_df['WO_DTN'].fillna('Nil')
                sales_df['WO_DTN'] = sales_df['WO_DTN'].astype(str)
                
                sales_df['WO_DTN1'] = sales_df['WO_DTN1'].fillna('Nil')
                sales_df['WO_DTN1'] = sales_df['WO_DTN1'].astype(str)
                
                sales_df['DTN_FNL'] = where((sales_df['WO_DTN']=='Nil') & (sales_df['WO_DTN1']!='Nil'),
                                                  sales_df['WO_DTN1'],  
                                                  sales_df['WO_DTN'])
                
                sales_df['DTN_FNL'] = sales_df['DTN_FNL'].apply(lambda x:str(x).replace('.0','') if str(x) not in [None,'None','nan',nan,'',' '] else x)
                sales_df.drop(columns=['WO_DTN','WO_DTN1'],inplace=True)
                sales_df.rename(columns={'DTN_FNL' : 'WO_DTN'}, inplace=True)  

            if 'Tech_CUID__c' in col_list and 'Tech_CUID2__c' in col_list:
                sales_df['Tech_CUID__c'] = sales_df['Tech_CUID__c'].fillna('Nil')
                sales_df['Tech_CUID__c'] = sales_df['Tech_CUID__c'].astype(str)
                
                sales_df['Tech_CUID2__c'] = sales_df['Tech_CUID2__c'].fillna('Nil')
                sales_df['Tech_CUID2__c'] = sales_df['Tech_CUID2__c'].astype(str)
                
                sales_df['Tech_CUID_FNL'] = where((sales_df['Tech_CUID__c']=='Nil') & (sales_df['Tech_CUID2__c']!='Nil'),
                                                  sales_df['Tech_CUID2__c'],  
                                                  sales_df['Tech_CUID__c'])
                
                sales_df.drop(columns=['Tech_CUID2__c','Tech_CUID__c'],inplace=True)
                sales_df.rename(columns={'Tech_CUID_FNL' : 'TECH_CUID'}, inplace=True) 
            
            if 'SA_DUE_DATE' in col_list:
                sales_df['SA_DUE_DATE']=pd.to_datetime(sales_df['SA_DUE_DATE'])
                if 'CUST_TIME_ZONE' in col_list:
                    sales_df['SA_DUE_DATE']=sales_df[['SA_DUE_DATE','CUST_TIME_ZONE']].apply(timezone_correction,axis=1)
                else:
                    sales_df['SA_DUE_DATE']=sales_df['SA_DUE_DATE'].apply(lambda x: x-timedelta(hours=5))
                sales_df['SA_DUE_DATE'] = pd.to_datetime(sales_df['SA_DUE_DATE']).dt.date
                sales_df['SA_DUE_DATE'] = sales_df['SA_DUE_DATE'].astype(str)
                sales_df['SA_DUE_DATE'] = sales_df['SA_DUE_DATE'].fillna('Nil')
                sales_df['SA_DUE_DATE'] = sales_df['SA_DUE_DATE'].replace('nan','Nil')
                
            if 'ORDER_DUE_DATE' in col_list:
                sales_df['ORDER_DUE_DATE']=pd.to_datetime(sales_df['ORDER_DUE_DATE'])
                if 'CUST_TIME_ZONE' in col_list:
                    sales_df['ORDER_DUE_DATE']=sales_df[['ORDER_DUE_DATE','CUST_TIME_ZONE']].apply(timezone_correction,axis=1)
                else:
                    sales_df['ORDER_DUE_DATE']=sales_df['ORDER_DUE_DATE'].apply(lambda x: x-timedelta(hours=5))
                sales_df['ORDER_DUE_DATE'] = pd.to_datetime(sales_df['ORDER_DUE_DATE']).dt.date
                sales_df['ORDER_DUE_DATE'] = sales_df['ORDER_DUE_DATE'].astype(str)
                sales_df['ORDER_DUE_DATE'] = sales_df['ORDER_DUE_DATE'].fillna('Nil')
                sales_df['ORDER_DUE_DATE'] = sales_df['ORDER_DUE_DATE'].replace('nan','Nil')
            
            if 'ACCT_CREATED_DT' in col_list:
                sales_df['ACCT_CREATED_DT']=pd.to_datetime(sales_df['ACCT_CREATED_DT'])
                if 'CUST_TIME_ZONE' in col_list:
                    sales_df['ACCT_CREATED_DT']=sales_df[['ACCT_CREATED_DT','CUST_TIME_ZONE']].apply(timezone_correction,axis=1)
                else:
                    sales_df['ACCT_CREATED_DT']=sales_df['ACCT_CREATED_DT'].apply(lambda x: x-timedelta(hours=5))                
                sales_df['ACCT_CREATED_DT'] = sales_df['ACCT_CREATED_DT'].dt.strftime('%Y-%m-%d %H:%M:%S')
                sales_df['ACCT_CREATED_DT'] = sales_df['ACCT_CREATED_DT'].astype(str)
                sales_df['ACCT_CREATED_DT'] = sales_df['ACCT_CREATED_DT'].replace('nan','Nil')
            
            if 'SCHEDULED_START_TIME' in col_list:            
                sales_df['SCHEDULED_START_TIME']=pd.to_datetime(sales_df['SCHEDULED_START_TIME'])
                if 'CUST_TIME_ZONE' in col_list:
                    sales_df['SCHEDULED_START_TIME']=sales_df[['SCHEDULED_START_TIME','CUST_TIME_ZONE']].apply(timezone_correction,axis=1)
                else:
                    sales_df['SCHEDULED_START_TIME']=sales_df['SCHEDULED_START_TIME'].apply(lambda x: x-timedelta(hours=5))
                sales_df['SCHEDULED_START_TIME'] = pd.to_datetime(sales_df['SCHEDULED_START_TIME']).dt.strftime("%Y-%m-%d %H:%M:%S")
                sales_df['SCHEDULED_START_TIME'] = sales_df['SCHEDULED_START_TIME'].astype(str)
                sales_df['SCHEDULED_START_TIME'] = sales_df['SCHEDULED_START_TIME'].replace('nan','Nil')
            
            if 'SCHEDULED_END_TIME' in col_list: 
                sales_df['SCHEDULED_END_TIME']=pd.to_datetime(sales_df['SCHEDULED_END_TIME'])
                if 'CUST_TIME_ZONE' in col_list:
                    sales_df['SCHEDULED_END_TIME']=sales_df[['SCHEDULED_END_TIME','CUST_TIME_ZONE']].apply(timezone_correction,axis=1)
                else:
                    sales_df['SCHEDULED_END_TIME']=sales_df['SCHEDULED_END_TIME'].apply(lambda x: x-timedelta(hours=5))
                sales_df['SCHEDULED_END_TIME'] = pd.to_datetime(sales_df['SCHEDULED_END_TIME']).dt.strftime("%Y-%m-%d %H:%M:%S")
                sales_df['SCHEDULED_END_TIME'] = sales_df['SCHEDULED_END_TIME'].astype(str)
                sales_df['SCHEDULED_END_TIME'] = sales_df['SCHEDULED_END_TIME'].replace('nan','Nil')
                
            if 'ARV_WIN_START_TIME' in col_list: 
                sales_df['ARV_WIN_START_TIME']=pd.to_datetime(sales_df['ARV_WIN_START_TIME'])
                if 'CUST_TIME_ZONE' in col_list:
                    sales_df['ARV_WIN_START_TIME']=sales_df[['ARV_WIN_START_TIME','CUST_TIME_ZONE']].apply(timezone_correction,axis=1)
                else:
                    sales_df['ARV_WIN_START_TIME']=sales_df['ARV_WIN_START_TIME'].apply(lambda x: x-timedelta(hours=5))
                sales_df['ARV_WIN_START_TIME'] = pd.to_datetime(sales_df['ARV_WIN_START_TIME']).dt.date
                sales_df['ARV_WIN_START_TIME'] = sales_df['ARV_WIN_START_TIME'].astype(str)
                sales_df['ARV_WIN_START_TIME'] = sales_df['ARV_WIN_START_TIME'].fillna('Nil')
                sales_df['ARV_WIN_START_TIME'] = sales_df['ARV_WIN_START_TIME'].replace('nan','Nil')
                
            if 'ARV_WIN_END_TIME' in col_list: 
                sales_df['ARV_WIN_END_TIME']=pd.to_datetime(sales_df['ARV_WIN_END_TIME'])
                if 'CUST_TIME_ZONE' in col_list:
                    sales_df['ARV_WIN_END_TIME']=sales_df[['ARV_WIN_END_TIME','CUST_TIME_ZONE']].apply(timezone_correction,axis=1)
                else:
                    sales_df['ARV_WIN_END_TIME']=sales_df['ARV_WIN_END_TIME'].apply(lambda x: x-timedelta(hours=5))
                sales_df['ARV_WIN_END_TIME'] = pd.to_datetime(sales_df['ARV_WIN_END_TIME']).dt.date
                sales_df['ARV_WIN_END_TIME'] = sales_df['ARV_WIN_END_TIME'].astype(str)
                sales_df['ARV_WIN_END_TIME'] = sales_df['ARV_WIN_END_TIME'].fillna('Nil')
                sales_df['ARV_WIN_END_TIME'] = sales_df['ARV_WIN_END_TIME'].replace('nan','Nil')
                
            if 'SA_CREATED_DATE' in col_list: 
                sales_df['SA_CREATED_DATE']=pd.to_datetime(sales_df['SA_CREATED_DATE'])
                if 'CUST_TIME_ZONE' in col_list:
                    sales_df['SA_CREATED_DATE']=sales_df[['SA_CREATED_DATE','CUST_TIME_ZONE']].apply(timezone_correction,axis=1)
                else:
                    sales_df['SA_CREATED_DATE']=sales_df['SA_CREATED_DATE'].apply(lambda x: x-timedelta(hours=5))
                sales_df['SA_CREATED_DATE'] = pd.to_datetime(sales_df['SA_CREATED_DATE']).dt.strftime("%Y-%m-%d %H:%M:%S")
                sales_df['SA_CREATED_DATE'] = sales_df['SA_CREATED_DATE'].astype(str)
                sales_df['SA_CREATED_DATE'] = sales_df['SA_CREATED_DATE'].replace('nan','Nil')
            
            if 'WO_DUE_DATE' in col_list: 
                sales_df['WO_DUE_DATE']=pd.to_datetime(sales_df['WO_DUE_DATE'])
                if 'CUST_TIME_ZONE' in col_list:
                    sales_df['WO_DUE_DATE']=sales_df[['WO_DUE_DATE','CUST_TIME_ZONE']].apply(timezone_correction,axis=1)
                else:
                    sales_df['WO_DUE_DATE']=sales_df['WO_DUE_DATE'].apply(lambda x: x-timedelta(hours=5))
                sales_df['WO_DUE_DATE'] = pd.to_datetime(sales_df['WO_DUE_DATE']).dt.date
                sales_df['WO_DUE_DATE'] = sales_df['WO_DUE_DATE'].astype(str)
                sales_df['WO_DUE_DATE'] = sales_df['WO_DUE_DATE'].fillna('Nil')
                sales_df['WO_DUE_DATE'] = sales_df['WO_DUE_DATE'].replace('NaT','Nil')
            
            if 'SF_ECD' in col_list:
                sales_df['SF_ECD']=pd.to_datetime(sales_df['SF_ECD'])
                if 'CUST_TIME_ZONE' in col_list:
                    sales_df['SF_ECD']=sales_df[['SF_ECD','CUST_TIME_ZONE']].apply(timezone_correction,axis=1)
                else:
                    sales_df['SF_ECD']=sales_df['SF_ECD'].apply(lambda x: x-timedelta(hours=5))
                sales_df['SF_ECD'] = pd.to_datetime(sales_df['SF_ECD']).dt.date
                sales_df['SF_ECD'] = sales_df['SF_ECD'].astype(str)
                sales_df['SF_ECD'] = sales_df['SF_ECD'].fillna('Nil')
                sales_df['SF_ECD'] = sales_df['SF_ECD'].replace('NaT','Nil')
            
            if 'CUST_TIME_ZONE' in col_list and not ('Case_Type__c' in col_list or 'PLAN_ID' in col_list):
                sales_df.drop(columns=['CUST_TIME_ZONE'],inplace=True)
            sales_df.reset_index(drop=True,inplace=True)
        return sales_df
    else :
        print('No output from SF')
        return pd.DataFrame()

def getExeScriptName(fileName):
    if fileName:
        return fileName.split('.')[0]

def logSetup(logFileName : str=None):
    logFileName = logFileName.split('.')[0]
    if not logFileName:
        print("No Log fime name provided. Defaulting it to 'QF_Generic_log.txt")
        logFileName='QF_Generic'
    cur_dtime = str(getCurrentDateTime()).replace(':','_').replace('-','_')
    if not isdir(abspath(join(logFolder,logFileName))):
        #creating a directory for each Script file
        mkdir(abspath(join(logFolder,logFileName)))
        print(f"New Log Folder created -> {abspath(join(logFolder,logFileName))}")
    if not isdir(abspath(join(outputFolder,logFileName))):
        mkdir(abspath(join(outputFolder,logFileName)))
        print(f"New Output Folder created -> {abspath(join(outputFolder,logFileName))}")
    log_file = abspath(join(logFolder,logFileName,f"{logFileName}_{cur_dtime}_log.txt"))
    print(f'Log File -> {log_file}')
    log_configfile_path = abspath(join(codeFolder,'logConfig.conf'))

    logging.config.fileConfig(log_configfile_path, defaults={'logFileName':log_file}, disable_existing_loggers=True)
    return logging.getLogger('rootLogger')

def apiCall(callingAPI,api_input,headers=None):
    rootLogger = logging.getLogger('rootLogger')
    if not callingAPI:
        rootLogger.info('Please provide the API name to initiate the API call')
        raise AttributeError
    if callingAPI and callingAPI not in improv_api_list.keys():
        rootLogger.info(f"""please provide valid API call details.\n{callingAPI} not available in [{', '.join(improv_api_list.keys())}]""")
        raise RuntimeError
    if api_input and not isinstance(api_input,dict):
        rootLogger.info(f'input to api call {callingAPI} should be of type dictionary.\nEntered api input is of type {type(api_input)}')
        raise RuntimeError
        
    improv_fnl_url = improv_url+callingAPI
    method = improv_api_list[callingAPI]
    rootLogger.info(f"api_link:{improv_fnl_url}\nAPI call:'{callingAPI}'\nAPI Input:\n{api_input}")
    try:
        response = requests.request(method, url=improv_fnl_url ,headers=headers, params = api_input, verify=False)
        response.raise_for_status()
    except HTTPError as err:
        rootLogger.info(f"status code:{response.status_code}, message:{response.json()['errorMessage']}")
        return str(response.json()['errorMessage'])
    else:
        return response.json()

def checkFilePath(filename,path=None) -> str:
    rootLogger = logging.getLogger('rootLogger')
    if not filename or len(filename) == 0:
        rootLogger.info('!!! Filename is empty !!!')
        raise RuntimeError
    if path:
        absFilePath = abspath(join(path,filename))
    else:
        absFilePath = abspath(filename)
    if not exists(absFilePath):
        rootLogger.info(f'No such file Exists in the given path -> {absFilePath}')
        return None
    rootLogger.info(f'File {absFilePath} available in path')
    return absFilePath

def cron_dt_frmt():
    my_date=date.today()
    my_day=calendar.day_name[my_date.weekday()] 

    dt = datetime.now()
    hour=dt.strftime('%H')

    day_cnt = 0
    if hour=='05':
        day_cnt =1
    elif hour=='06' and my_day=='Friday':
        day_cnt = 3
    else: 
        day_cnt=0
        
    w_end=(datetime.now()+timedelta(days=day_cnt))
    run_date=w_end.strftime('%Y-%m-%d')    
    return str(run_date)

def sharepointFileUpload(fileList: list,site_name,path):
#     rootLogger = logging.getLogger('rootLogger')    
    if fileList is None or len(fileList) < 1 :
        print('Empty FileList')
        raise RuntimeError
    if not isinstance(fileList,list):
        print('files should be provided in list format')
        raise RuntimeError
    if site_name is None or len(site_name) == 0 :
        print('Sharepoint Site name is missing')
        raise RuntimeError

    cookie=Office365("https://centurylink.sharepoint.com", username="pretheve.vijayan@lumen.com", password="calmboy@12").GetCookies()
    siteLink=Site(f"https://centurylink.sharepoint.com/sites/{site_name}/", version=Version.v365, authcookie=cookie,timeout=3600)
    folder = siteLink.Folder('Shared Documents/General/'+path)
    for file in fileList:
        abspath = checkFilePath(file)
        status = ''
        
        if abspath:
            try:
                with open(file,'rb') as f:
                    out_file=f.read()
                    folder.upload_file(out_file,basename(file))
                    status = f'Uploaded to sharepoint folder --> {folder.info["d"]["ServerRelativeUrl"]}'
            except Exception as e:
                print(e)
                status = 'sharepoint Upload failed!!!'
            finally:
                print(f"{basename(file)} {status}")
        else:
            print(f"{file} not available in path for upload") 

def improv_create_profile(imp_missing_prof : pd.DataFrame) :
    o2_conn=optius_conn()
    o2_platform_id_qry = """
            SELECT DISTINCT CV.VALUE AS PLATFORM_ID,
            C.ID AS SF_DTN
            FROM OPTIPROD.CIRCUIT C
            INNER JOIN OPTIPROD.FACILITY_CIRCUIT FC
            ON FC.CIRCUIT_SYS_ID=C.SYS_ID
            INNER JOIN OPTIPROD.FACILITY_GROUP_KEY FGK ON FGK.SERVICE_FACS_ID=FC.SERVICE_FACS_ID
            INNER JOIN ODINPROD.DISTINGUISHEDNAME DN ON DN.DISTINGUISHEDNAME=FGK.OED_PORT_DN AND DN.DNKEY='PP'
            INNER JOIN ODINPROD.CHARSPEC CS ON CS.PHYSICALRESOURCE_UNIQUEID=DN.ROOTDN_ENTITYID AND CS.NAME='IP_REGION_ID'
            INNER JOIN ODINPROD.CHARVALUE CV ON CV.CHARSPEC_UNIQUEID=CS.UNIQUEID
            WHERE C.ID in (${dtn})
            """

    print(f"{imp_missing_prof.shape[0]} DTNs missing profiles in IMPROV")
    improv_url_fnl = improv_url+'createAccount'
    method = improv_api_list['createAccount']
    
    imp_dtnlist=imp_missing_prof['SF_DTN'].unique().tolist()    
    
    platform_qry = o2_platform_id_qry.replace('${dtn}',str(imp_dtnlist)).replace('[','').replace(']','')
    print(f"\nRunning platform query -->\n{platform_qry}")
    o2_platform_id_rslt = pd.read_sql(platform_qry,con = o2_conn)
    print(f"\nplatform query result -->\n{o2_platform_id_rslt.shape}")
    
    imp_missing_prof=pd.merge(imp_missing_prof,o2_platform_id_rslt,on='SF_DTN',how='left')
    imp_missing_prof = imp_missing_prof.fillna('Nil')
    
#     print(f"\nRunning Speed query -->\n{speed_qry}")
#     imp_missing_prof['dtn_order']=imp_missing_prof['SF_DTN']+"_"+imp_missing_prof['SF_ORDER_NUMBER']
#     speed_qry = o2_speed_qry.replace('${order}',str(imp_order_list)).replace('[','').replace(']','')
#     imp_order_list=imp_missing_prof['dtn_order'].unique().tolist()
#     o2_speed_rslt = pd.read_sql(speed_qry,con = o2_conn)
#     print(f"\speed query result -->\n{o2_speed_rslt.shape}")
    
    for idx,row in imp_missing_prof.iterrows():
        
        message='Nil'
        status='Nil'
        dtn = imp_missing_prof['SF_DTN'][idx]
        pltfrm_id = imp_missing_prof['PLATFORM_ID'][idx]
        speed = imp_missing_prof['WO_PURCHASED_DATA_RATE'][idx]
        print('-'*50,f'Creating profile for {dtn}...',sep='\n')
        if pd.isna(pltfrm_id) or pltfrm_id=='Nil':
            message = 'Platorm Id missing in O2'
            status = 'ERROR'
        elif pd.isna(speed) or speed=='Nil':
            message = 'Speed missing in O2'
            status = 'ERROR'
        else:
            improv_create_payload = {
            "ImprovAccountRequest": {
            "callingSystemName": "SF",
            "correlationId": imp_missing_prof['SF_ORDER_NUMBER'][idx],
            "services": [
                {
                    "name": "DSL",
                    "tn": dtn,
                    "parameters": [
                {
                        "name": "Line",
                        "value": "Routing_gpon"
                },
                      {
                        "name": "Line-Encap",
                        "value": "IPoE"
                      },
                      {
                        "name": "Speed",
                        "value": speed
                      }
                    ]
                  }
                ],
            "userAccount": {
                "orgId": "Biwfiber",
                "platformId": pltfrm_id,
                "classOfService": "BIWFR",
                "customerName": imp_missing_prof['ACCOUNT_NAME'][idx],
                "ensembleBAN": imp_missing_prof['ACCOUNT_NUMBER'][idx],
                "companyOwner": "1"
                }
              }
            }
            try:
                response = requests.request(method = method,
                                            url=improv_url_fnl, json=improv_create_payload,
                                            headers=utils.improv_header,verify=False)
                response.raise_for_status()
            except HTTPError as err:
                print(err) 
            rep_fnl = response.json()["ImprovAccountResponse"]["serviceResponses"][0]['message']
            status=rep_fnl['status']
            message=rep_fnl['message']
        print(f"{status} --> {message}")
        imp_missing_prof['IMPROV_STATUS'][idx] = message
        
    imp_missing_prof.drop(columns = ['PLATFORM_ID'],inplace=True)
    return imp_missing_prof
            
def df_2_excel(filepath,results) -> None:
    rootLogger = logging.getLogger('rootLogger')
    try:        
        with ExcelWriter(path=filepath,mode='w', date_format='YYYY-MM-DD', engine = 'openpyxl') as writer:
            results.to_excel(writer,index=False)
            rootLogger.info(f'{filepath} generated')
            
    except Exception as e:
        rootLogger.exception(e)
        rootLogger.info(f"!-- File {filepath} not generated --!")
    
def run_batch_query(input_query : str,input_params : dict,conn_type,interval_value=None, returnResult=True):
        from math import ceil
#         rootLogger = logging.getLogger('rootLogger')
        result_data = pd.DataFrame()
        process_start = time()
        print(f'process start time : {ctime(process_start)}')
        
        start = 0
        if interval_value:
            interval=interval_value
            end = interval_value
        else:
            interval = 1000
            end = 1000
        if isinstance(input_params,dict) and input_params:
            for k,v in input_params.items():
                replace_string = k
                input_list = input_params[k]
            # rootLogger.info(replace_string)
        
        input_cnt = len(input_list) # total values that will be substituted for a parameter
        batch_cnt = ceil(input_cnt/interval) #total batches to execute

        if input_cnt > 0:
            print(f'Total Batches to run:{batch_cnt}\nInput list Length:{input_cnt}')
            for i in range(0,batch_cnt):
                print(f"{'-'*70}\nRunning Batch -> {i+1}")
                batch_start=time()
                print(f'Batch start time : {ctime(batch_start)}')
                if i+1 == batch_cnt:
                    end = start + (input_cnt - (i*interval))

                print(f'Running query for index : start = {start}, end = {end}')
                sub_list = str(input_list[start:end])
                query = input_query.replace(replace_string,sub_list).replace('[','').replace(']','')
                
                if conn_type == 'SF':
                    batch_result = sf_select(query)
                elif conn_type == 'ORCL_SF':
                    print(f"\nExecuting Query :\n{query}")
                    batch_result = pd.read_sql(query,con=orcl_sf_conn())#.fillna('Nil')
                elif conn_type == 'O2':
                    print(f"\nExecuting Query :\n{query}")
                    batch_result = pd.read_sql(query,con=optius_conn())#.fillna('Nil')
                elif conn_type =='MARTENS':
                    print(f"\nExecuting Query :\n{query}")
                    batch_result=pd.read_sql(query,con=martens_conn())
                if batch_result.shape[0]> 0:
                    result_data = result_data.append(batch_result)
                    print(f'Query result : {batch_result.shape}')
                else:
                    print(f'\n!!! No  records for the below batch of orders !!!\n{str(input_list[start:end])}\n')

                batch_end=time()
                print(f'Batch end time : {ctime(batch_end)}')
                print(f'Time taken : {time_taken(batch_start,batch_end)}')

                start+=interval
                end+=interval

        print(f"{'-'*70}\n Total records:{result_data.shape}")
        process_end = time()
        print(f'Process end time : {ctime(process_end)}')
        print(f"Total Time taken : {time_taken(process_start,process_end)}\n")
        
        if returnResult:
            return result_data

def insert_audit_records(script_name : str, input_cnt : int, fix_cnt : int) -> None :
        
        # from modUtils import getCurrentDate,getCurrentDateTime
        rootLogger = logging.getLogger('rootLogger')
        connection = orcl_daas_conn()
        if script_name is None or len(script_name.strip())==0:
            rootLogger.info("!!!Script name is Empty!!!")
        elif input_cnt is None or input_cnt==0:
            rootLogger.info("!!!Source Count is Empty!!!")
        elif fix_cnt is None or len(str(fix_cnt).strip())==0 :
            rootLogger.info("!!!Target Count is Empty!!!")
        else:
            rootLogger.info(f'Inserting Audit records for Script {script_name}...')    
            audit_qry = """INSERT INTO DAASBOT.QF_QH_FALLOUT_FIX_AUDIT (RUN_DATE,LOAD_TS,SCRIPT_NAME,INPUT_RCD_CNT,FIX_RCD_CNT)
        values (:1,:2,:3,:4,:5)"""
            
            with connection.cursor() as cursor:
                try:
                    cursor.execute(audit_qry, [str(getCurrentDate()),str(getCurrentDateTime()),script_name,input_cnt,fix_cnt])
                except Exception as e :
                    rootLogger.info(e)
            connection.commit()
            rootLogger.info('Audit Records inserted successfully')
            
def orch_data_dump(final_data : pd.DataFrame):
    rootLogger = logging.getLogger('rootLogger')
    if final_data.shape[0] == 0:
        print('Final Dataset has no records to insert')
    else:
        daas_conn = orcl_daas_conn() 
        final_cols=final_data.columns.values.tolist()
        if '_merge' in final_cols:
            final_data.drop(columns=['_merge'],inplace=True)
        if 'RUN_TS' in final_cols:
            final_data.drop(columns=['RUN_TS'],inplace=True)
        final_data.insert(0,'RUN_TS',str(getCurrentDateTime()))        
        if 'SERVICE_FACS_ID' not in final_cols:
            final_data.insert(len(final_cols),'SERVICE_FACS_ID','')
        if 'ORDER_TYPE' not in final_cols:        
            final_data.insert(len(final_cols),'ORDER_TYPE','')
        if 'O2_STATUS' not in final_cols:     
            final_data.insert(len(final_cols),'O2_STATUS','')
            
        final_data['ITEM_CREATED_DT']=pd.to_datetime(final_data['ITEM_CREATED_DT'], format='%Y-%m-%d').dt.strftime('%Y-%m-%d')
        final_data['ACCT_CREATED_DT']=pd.to_datetime(final_data['ACCT_CREATED_DT'], format='%Y-%m-%d').dt.strftime('%Y-%m-%d')
        final_data = final_data.fillna('')
        
        final_data = final_data[['RUN_TS','ITEM_ID', 'ITEM_NM', 'PLAN_ID', 'CURR_ITEM_STATUS','UPDT_ITEM_STATUS','ITEM_CREATED_DT',
                                 'ORDER_ID', 'ORDERNUMBER', 'ORDER_STATUS','ORDER_CREATED_DT','SERVICE_FACS_ID', 'ORDER_TYPE','O2_STATUS',
                                 'ACCT_ID', 'ACCOUNT_NAME', 'ACCOUNT_NUMBER','ACCOUNT_STATUS', 'ACCT_CREATED_DT','FILE_NM' ]]    
        
        orch_fix_qry = """insert into DAASBOT.QF_REPORT_LOG_L1 values (:1,:2,:3,:4,:5,:6,:7,:8,:9,:10,:11,:12,:13,:14,:15,:16,:17,:18,:19,:20)"""
        try:
            with daas_conn.cursor() as cursor:
                ins_list = final_data.values.tolist()
                for row,ins in enumerate(ins_list):
                    print(f"Inserting row {row+1}:{ins}")
                    cursor.execute(orch_fix_qry,ins)
            daas_conn.commit()
            print(f"Inserted {len(ins_list)} records successfully")
        except Exception as e:
            print(e)

def oauth_gen():
    auth_url = "https://api.centurylink.com/oauth/token?grant_type=client_credentials"
    auth_header = {"Authorization" : "Basic dW40dnk5bEV1eE9mSjVKZTBHR0U2RXExU3NkZG9BcUM6Zmx5V0JDTGZEQkJuRG5iYQ=="}
    auth_method = 'post'
    auth_response = requests.request(method = auth_method,url=auth_url,headers=auth_header,verify=False )
    auth_rep_json = auth_response.json()
    token_type = auth_rep_json['token_type']
    access_token = auth_rep_json['access_token']
    access_auth = {'Authorization' : token_type + " " + access_token }    
    return access_auth

def cms_ems_api(olt_list):
    cms_ems_data = pd.DataFrame()
    if not isinstance(olt_list,list):
        print(f"the input to CMS/EMS API should be either a list of OLTs . Entered input is of type {type(olt_list)}")
    if isinstance(olt_list,list) and len(olt_list) == 0:
        print(f"OLT List is empty")
    else:
        ros_url = "https://api.lumen.com/Application/v1/ROS/subscriberManagement/"
        ros_data = {
            'action' : 'ByDSLAM',
            'format' : 'XML',
            'applid' : 'ctag_audit',
            'stats' : '1'
        }
        ros_method = 'get'
        print(f'Total OLTs to run --> {len(olt_list)}')
        for i,olt in enumerate(olt_list):
            print(f"{'-'*10}No:{i+1} -> {olt}{'-'*10} ")
            olt_out=None
            ros_data['p1'] = olt
            try:
                auth = oauth_gen()
                if auth is None:
                    print('Invalid Authentication')
                    break
                cms_res = requests.request(method=ros_method,url = ros_url, params=ros_data,verify=False,headers=auth)
                cms_session_data = xd.parse(cms_res.text)['ROSResponse']            
                status = cms_session_data['ROSServerData']['QueryStatus']
                
                if status.lower() == 'success':
                    print(f'API request successful')
            #         print(cms_session_data['SessionData'])
                    olt_out = pd.DataFrame(list(cms_session_data['SessionData']))
                    olt_out.insert(0,'OLT',olt)
                    print(f"API output --> {olt_out.shape}")
                elif status.lower().startswith('error'):
                    print(f"API request failed with -> '{status}'")

                if not (olt_out is None or olt_out.empty):
                    cms_ems_data = cms_ems_data.append(olt_out)
                
            except Exception as e:
#                 print(e)
                print('a')
    return cms_ems_data

#AFC API Creds
afc_url = 'https://o2prod.corp.intranet/CSF/api/v1/serviceorder'
afc_method='post'
afc_header = {
    "Authorization":"Basic QUQxNTgyODpXZTFjQG1lMw=="
}

#API Payloads
improv_create_payload = {
  "ImprovAccountRequest": {
    "callingSystemName": "SF",
    "correlationId": "${correlationId}",
    "services": [
      {
        "name": "DSL",
        "tn": "${tn}",
        "parameters": [
          {
            "name": "Line",
            "value": "Routing_gpon"
          },
          {
            "name": "Line-Encap",
            "value": "IPoE"
          },
          {
            "name": "Speed",
            "value": "${speed}"
          }
        ]
      }
    ],
    "userAccount": {
      "orgId": "Biwfiber",
      "platformId": "${platformID}",
      "classOfService": "BIWFR",
      "customerName": "${customerName}",
      "ensembleBAN": "${ensembleBAN}",
      "companyOwner": "1"
    }
  }
}

improv_update_payload = {
    "ImprovAccountRequest": {
      "callingSystemName": "MAL",
      "correlationId": "<cor_id>",
      "services": [
        {
          "action": "UPDATE",
          "name": "DSL",
          "tn": "<new_dtn:old_dtn>",
          "newTn": "<new_dtn>"
        }
      ]
    }
  }

wg_update = {
  "ImprovAccountRequest": {
    "callingSystemName": "MTA",
    "correlationId": "{dtn}",
    "services": [
      {
        "action": "ADD",
        "name": "DSL",
        "tn": "{dtn}",
        "parameters": [
          {
            "name": "Walled-Garden",
            "value": "BIWF/Setup"
          }
        ]
      }
    ]
  }
}

o2_canc_payload = """<soapenv:Envelope xmlns:soapenv="http://schemas.xmlsoap.org/soap/envelope/"
    xmlns:ser="http://dto.moi.services.triad.sasktelinternational.com/ServiceOrderCancellationRequest"
    xmlns:moic="http://dto.moi.services.triad.sasktelinternational.com/common/MoiCommonParameters1"
    xmlns:mois="http://dto.moi.services.triad.sasktelinternational.com/common/MoiSupplementaryParameters1"
    xmlns:app="http://dto.moi.services.triad.sasktelinternational.com/common/ApplicationEchoback1"
    xmlns:fnid="http://dto.moi.services.triad.sasktelinternational.com/common/FNIdentity1">
    <soapenv:Header/>
    <soapenv:Body>
        <ser:serviceOrderCancellationRequest>    
            <ser:orderNumber>{0}</ser:orderNumber>
            <ser:lciNumber>{1}</ser:lciNumber>
        </ser:serviceOrderCancellationRequest>
    </soapenv:Body>
    </soapenv:Envelope>"""

o2_disconnect_payload = """<soapenv:Envelope xmlns:soapenv="http://schemas.xmlsoap.org/soap/envelope/" 
xmlns:wsdl="http://sasktelinternational.com/csf/wsdl" 
xmlns:ser="http://sasktelinternational.com/csf/wsdl/serviceOrder" 
xmlns:inv="http://sasktelinternational.com/csf/wsdl/inventory" 
xmlns:dis="http://sasktelinternational.com/csf/wsdl/disconnect">
<soapenv:Header/>
<soapenv:Body>
<wsdl:disconnectRequestWrapper>
<request>
  <ser:serviceOrderReference>{}</ser:serviceOrderReference>
  <ser:dueDate>{}</ser:dueDate>
  <inv:circuitIdentifier>{}</inv:circuitIdentifier>
</request>
</wsdl:disconnectRequestWrapper>
</soapenv:Body>
</soapenv:Envelope>"""

o2_soff_payload="""<soapenv:Envelope xmlns:soapenv="http://schemas.xmlsoap.org/soap/envelope/" 
xmlns:ser="http://dto.moi.services.triad.sasktelinternational.com/ServiceOrderSignOffRequest" 
xmlns:moic="http://dto.moi.services.triad.sasktelinternational.com/common/MoiCommonParameters1"
xmlns:mois="http://dto.moi.services.triad.sasktelinternational.com/common/MoiSupplementaryParameters1"
xmlns:app="http://dto.moi.services.triad.sasktelinternational.com/common/ApplicationEchoback1" 
xmlns:fnid="http://dto.moi.services.triad.sasktelinternational.com/common/FNIdentity1">
<soapenv:Header/>
<soapenv:Body>
  <ser:serviceOrderSignOffRequest>
    <ser:orderNumber>{}</ser:orderNumber>
    <ser:lciNumber>{}</ser:lciNumber>
  </ser:serviceOrderSignOffRequest>
</soapenv:Body>
</soapenv:Envelope>"""

#improv_api_function
async def improv_find_user(input : pd.DataFrame):
    async def session_creator():
        async with aiohttp.ClientSession() as session:    
            tasks = []
            d=list(input.index.values)
            for chunk in chunks(10,d):    
                for i in chunk:
                    task = asyncio.ensure_future(improv_api(session, i))
                    tasks.append(task)
                await asyncio.gather(*tasks)

    async def improv_api(session, i):
        status,speed,wg_status = 'Nil','Nil','Nil'
        dtn = input['SF_DTN'][i]
        url='https://api.corp.intranet/Application/v1/Improv/findUser'
        header = {
            "Authorization": "Basic aW1wcm92YXA6SlRBeGJZR3FjWkFUMnJ2"
            }

        if dtn == 'Nil' or str(dtn) == 'nan':
            status = 'Null SF DTN'
        else:
            data = {
                'WTN':dtn
                }

            async with session.get(url=url, params=data,headers = header,ssl=False) as response:
                response=await response.json()
#                 from json import dumps
#                 print(dumps(response,indent=4))
            if isinstance(response,dict):
                status='Profile available in IMPROV'
                try:
                    wg_status=response['RequesteduserNameDetail']['ISPProvisioningDetail']['SvcDetail']['DSLInfo']['WalledGardenName']
                except:
                    wg_status = 'Key:WalledGardenName Not Found in API response'
                wg_status = 'Nil' if not wg_status else wg_status 

                try:
                    speed=response['RequesteduserNameDetail']['ISPProvisioningDetail']['SvcDetail']['DSLInfo']['TransmissionRate']
                except:
                    speed = 'Key:TransmissionRate Not Found in API response'
                speed = 'Nil' if not speed else speed
            if list(response)[0]=='errorMessage':
                status=response['errorMessage']
            
                
        input.loc[i,'IMPROV_STATUS'] = status
        input.loc[i,'IMPROV_WG_STATUS'] = wg_status
        input.loc[i,'IMPROV_SPEED'] = speed


    await session_creator()
    print(input['IMPROV_STATUS'].value_counts())
    return input



#lars_api_function
async def lars_data(input : list):
    lars_dict={}
    async def session_creator():
        async with aiohttp.ClientSession() as session:    
            tasks = []
            for chunk in chunks(10,input):    
                for i in chunk:
                    task = asyncio.ensure_future(get_lars_data(session, i))
                    tasks.append(task)
                await asyncio.gather(*tasks)

    async def get_lars_data(session, dtn):
        lars_url = 'https://api.corp.intranet/Application/v1/LARS/subscriberManagement/'
        lars_method = 'get'
        lars_header= { # prod
        'X-Application-Key':'H8AM5JUQGaxNEmOZJQbxsMIDJfzoAxbp',    
        }
        lars_data = {
        'action' : 'ByWTN',
        'stat':'1',
        'applid': 'QFQUICKFIX_P'
        }
        lars_data['p1']=dtn
        async with session.request(url=lars_url,method=lars_method,headers=lars_header,params=lars_data,ssl=False) as response:
            lars_df = await response.content.read()
            lars_response = html_parse(lars_df)
            if isinstance(lars_response,dict):
                lars_dict[dtn]=lars_response
            else:
                print(f"Lars Response not generated for DTN:{dtn}")
    await session_creator()
    
    lars_df=pd.DataFrame.from_dict(lars_dict,orient='index')
    lars_df.loc[lars_df['QueryStatus']=='success','LARS_STATUS']='Active'
    lars_df.loc[lars_df['QueryStatus']=='error: no records found','LARS_STATUS']='Not in LARS'
    lars_df.loc[~lars_df['QueryStatus'].isin(['error: no records found','success']),'LARS_STATUS']='misc'
    lars_df.reset_index(inplace=True)
    lars_df.rename(columns={'index':'SF_DTN'},inplace=True)
    lars_df = lars_df[['SF_DTN','LARS_STATUS','CVLAN','DSLAMNode','CallingStationID','DSLAMSSP','SVLAN',
                       'SessionStatus','WTN1','WGName','WGSupportFlag']]
    return lars_df


#uniqual_api
async def uniqual_api(input : pd.DataFrame):
    async def session_creator():
        async with aiohttp.ClientSession() as session:    
            tasks = []
            d=list(input.index.values)
            for chunk in chunks(10,d):
                auth_header = {"Authorization" : "Basic dW40dnk5bEV1eE9mSjVKZTBHR0U2RXExU3NkZG9BcUM6Zmx5V0JDTGZEQkJuRG5iYQ=="}
                auth_url = 'https://api.lumen.com/oauth/token?grant_type=client_credentials'
                auth_method = 'post'
                r=await session.request(method = auth_method,url = auth_url, headers = auth_header)
                resp_json=await r.json()
                uq_header = {"Authorization" : resp_json['token_type']+' '+resp_json['access_token']}
                for i in chunk:
                    task = asyncio.ensure_future(uniqual_resp(session, i,uq_header))
                    tasks.append(task)
                await asyncio.gather(*tasks)

    async def uniqual_resp(session, i,uq_header):
        print(f"{'-'*20}{i+1}:{input['SF_POLYGON_ID'][i]}{'-'*20}")
        
        status='Nil'
        ecd='Nil'
        lat=input['SF_LAT_VALUE'][i]
        long=input['SF_LONG_VALUE'][i]
        
        uq_body = {
                "serviceAddress": {
                "geoPoint": [
                    {
                        "latitude": str(lat),
                        "longitude": str(long)
                    }
                ],
                    "addressLine": ""
                },
                "salesChannel": "PARTNER",
                "referenceNumber": "1669097552006bcc",
                "companyOwnerId": "1",
                "callingSystem": "PX-Lumen",
                "attemptedGoogle": "YES"
            }
        
        uq_url = 'https://api.centurylink.com/Application/v1/BMP/serviceAvailability/bsi/v2/performUnifiedQual'
        uq_method = 'post'
        async with session.request(method=uq_method,url=uq_url,headers = uq_header,json = uq_body,ssl=False) as response:
            u_resp_json=await response.json()
        try:    
            api_stat = u_resp_json['success']
            if api_stat:
                uniqual_res=u_resp_json['unifiedQualResponse']
                status=uniqual_res['status']
                ecd=uniqual_res['availabiltyDate']
            input.loc[i,'UNIQUAL_STATUS']=status 
            input.loc[i,'UNIQUAL_ECD']=ecd
            print(f"POLYGON ID -->{input['SF_POLYGON_ID'][i]}",f"POLYGON STATUS -->{input['UNIQUAL_STATUS'][i]}",f"POLYGON ECD -->{input['UNIQUAL_ECD'][i]}",sep='\n')    
        except:
            status='Response not generated'
            ecd='Response not generated'
            input.loc[i,'UNIQUAL_STATUS']=status 
            input.loc[i,'UNIQUAL_ECD']=ecd
    await session_creator()
    return input

#facility_updation
def sf_facility_updation(input_df):
    sf=sf_conn()
    counter=0
    for i in input_df['WO_ID'].unique(): 
        df=input_df[input_df['WO_ID']==i]
        acct_id=df['ACCT_ID'].to_string(index=False)
        acct_id=acct_id.replace("'","")
        for j in range(len(df)):
            new_dict={}
            key_name = df['Field'].iloc[j]
            value = df['O2_Value'].iloc[j]
            new_dict[key_name] = value
            #print(new_dict)
            try:
                if key_name=='Purchased_Data_Rate__c':
                    sf.Account.update(acct_id,new_dict)
                    print(f"{key_name} updated for {i}")
                else:
                    sf.WorkOrder.update(i,new_dict)
                    print(f"{key_name} updated for {i}")
                status='updated'
                counter=counter+1
            except:
                print(f"{key_name} not updated for {i}")
                status='not updated'
            input_df.loc[input_df['WO_ID']==i,'Updation_Message']=status
    print(f"Facilities Updation Count ---> {counter}")
    return input_df

#pushing facility details to dassbot db
def facility_data_dump(final_data : pd.DataFrame):
    #rootLogger = logging.getLogger('rootLogger')
    if final_data.shape[0] == 0:
        print('Final Dataset has no records to insert')
    else:
        daas_conn = orcl_daas_conn() 
        final_cols=final_data.columns.values.tolist()
        if 'RUN_TS' in final_cols:
            final_data.drop(columns=['RUN_TS'],inplace=True)
        final_data.insert(0,'RUN_TS',str(getCurrentDateTime()))                
        final_data = final_data[['RUN_TS','ACCT_NUM','ORDERNUMBER','WO_NUM','SA_NUM','SA_WORK_TYPE','SF_WO_FIELD_NM','SF_VALUE','O2_VALUE','UPDT_STATUS']]    
        
        orch_fix_qry = """insert into DAASBOT.QF_QH_FCLTY_MISMATCH_FIX values (:1,:2,:3,:4,:5,:6,:7,:8,:9,:10)"""
        try:
            with daas_conn.cursor() as cursor:
                ins_list = final_data.values.tolist()
                for row,ins in enumerate(ins_list):
                    print(f"Inserting row {row+1}:{ins}")
                    cursor.execute(orch_fix_qry,ins)
            daas_conn.commit()
            print(f"Inserted {len(ins_list)} records successfully")
        except Exception as e:
            print(e)