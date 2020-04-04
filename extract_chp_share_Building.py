#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Mar 30 22:53:46 2020

@author: rowena
"""

import os
os.system('pip install pandas')
os.system('pip install requests')
os.system('pip install pathlib')
os.system('pip install tabula-py')


import sys

old_stdout = sys.stdout

log_file = open("test.log","w")
sys.stdout = log_file

print("this will be written to message.log")

#pip install tabula-py

import pandas as pd 
from pathlib import Path
import requests
import tabula
import numpy as np

from tabula import read_pdf
from pandas import DataFrame
from pandas.api.types import is_string_dtype
from pandas.api.types import is_numeric_dtype

import time
timestr = time.strftime("%Y%m%d")

from datetime import datetime, timedelta
ytd=datetime.strftime(datetime.now() - timedelta(1), '%Y%m%d')

import smtplib
gmail_user = 'trinsaur@gmail.com'
gmail_password = 'gyhrwnenvkcugzwo'

sent_from = gmail_user
to = ['trinsaur@gmail.com']
subject = 'CHP File Update'

print("Finish Define Variable")

df_log=[]

def extract_chp(url,output,str1):
    filename = Path('tmp_chp_'+str1+'.pdf')
    response = requests.get(url)
    filename.write_bytes(response.content)
    
    df=read_pdf('tmp_chp_'+str1+'.pdf', multiple_tables=True, pages="all", lattice=True)
    #df=tabula.read_pdf('tmp_chp_'+str1+'.pdf', spreadsheet=True)
    
    new_col_name_0=df[0].columns
    new_col_name_0_1=[x.replace('\n', ' ').replace('\r', ' ') for x in new_col_name_0]
    
    #df_all.rename(columns=dict(zip(df_all.columns[0:], new_col_name1)),inplace=True)
    
    df[0].columns = np.arange(len(df[0].columns))
    df_all_row=df[0].select_dtypes(include=['object']).replace({'\r':' '},regex=True).replace({'\n':' '},regex=True)
    case_no=df[0][0]
    
    df_all_0=pd.concat([case_no, df_all_row], axis=1)  
    df_all_0=df_all_0.loc[:, ~df_all_0.columns.duplicated()]
    
    j=0
    
    df_log=len(df_all_0)
    new_col_name=new_col_name_0
    
    df_all_tmp=df_all_0
    df_all_1=df_all_tmp
    df_all_2=df_all_tmp
    df_all_append=df_all_row

    for i in range(1,len(df),1):      
        if len(df[i].columns)==len(new_col_name) or len(df[i].columns)==len(df[i-1].columns):
            df[i].columns = np.arange(len(df[i].columns)) 
            for m in range(len(df[i].columns)):      
                if not(is_string_dtype(df[i][m])):
                    df[i][m] = df[i][m].astype(str)
            df_all_row=df[i].select_dtypes(include=['object']).replace({'\r':' '},regex=True).replace({'\n':' '},regex=True)
            case_no=df[i][0]
                
            df_all_append=pd.concat([case_no, df_all_row],axis=1)  
            df_all_append=df_all_append.loc[:, ~df_all_append.columns.duplicated()]
            exec('df_all_'+str(j)+'=df_all_'+str(j)+'.append(df_all_append)')
            df_log=df_log+len(df_all_append)
        
        else:   
            new_col_name=df[i].columns
            new_col_name_1=[x.replace('\n', ' ').replace('\r', ' ') for x in new_col_name]
            exec('new_col_name_'+str(j)+'=new_col_name')
            exec('new_col_name_'+str(j)+'_1=new_col_name_1')
            df[i].columns = np.arange(len(df[i].columns)) 
            for m in range(len(df[i].columns)):      
                if not(is_string_dtype(df[i][m])):
                    df[i][m] = df[i][m].astype(str)
            
            df_all_row=df[i].select_dtypes(include=['object']).replace({'\r':' '},regex=True).replace({'\n':' '},regex=True)
            case_no=df[i][0]
            
            df_all_tmp=pd.concat([case_no, df_all_row],axis=1)
            df_all_tmp=df_all_tmp.loc[:, ~df_all_tmp.columns.duplicated()]
            
            code="""
df_all_"""+str(j)+"""=df_all_tmp
                """
            exec(code) 
            
            df_log=df_log+len(df_all_row)  
            j=j+1 

    tmp_log = pd.read_csv("./data/df_log_"+str1+".csv",header=0,index_col=False ) 
    lst_log=tmp_log.loc[0,'0']
    
    for k in range(0,j+1):
        code="""
for i in range(len(df_all_"""+str(k)+""")):
   if pd.isna(df_all_"""+str(k)+""".iloc[i,2]):
           for j1 in range(len(new_col_name_"""+str(k)+""")-1):
               if pd.isna(df_all_"""+str(k)+""".iloc[i,j1])==False and pd.isna(df_all_"""+str(k)+""".iloc[i-1,1])==False:
                   if pd.isna(df_all_"""+str(k)+""".iloc[i-1,j1])==False:
                       df_all_"""+str(k)+""".iloc[i-1,j1]=df_all_"""+str(k)+""".iloc[i-1,j1] +' ' + df_all_"""+str(k)+""".iloc[i,j1]
                   else:
                       df_all_"""+str(k)+""".iloc[i-1,j1]=df_all_"""+str(k)+""".iloc[i,j1]  
df_all_"""+str(k)+"""=df_all_"""+str(k)+""".loc[:, ~df_all_"""+str(k)+""".columns.duplicated(keep='first')]
df_all_export_"""+str(k)+"""=df_all_"""+str(k)+"""[pd.isna(df_all_"""+str(k)+"""[1])==False]
df_all_export_"""+str(k)+""".rename(columns=dict(zip(df_all_export_"""+str(k)+""".columns[0:], new_col_name_"""+str(k)+""")),inplace=True)
      
        """ 
        exec(code)
        
    if df_log != lst_log: 
        for k in range(0,j+1):
            code="""
df_all_export_"""+str(k)+""".to_csv(r'~/Documents/chf_"""+str1+"""_"""+timestr+"""_"""+str(k)+""".csv')
                """
            exec(code)
    
    os.system('chmod 750 '+"~/Documents/df_log_"+str1+".csv")
    df_log=pd.DataFrame([df_log])
    df_log.to_csv("~/Documents/df_log_"+str1+".csv")

#print("Finish Processing building list")
#extract_chp('https://www.chp.gov.hk/files/pdf/local_situation_covid19_tc.pdf','~/Documents/case'+timestr+'.csv','case_tc')
#extract_chp('https://www.chp.gov.hk/files/pdf/local_situation_covid19_en.pdf','~/Documents/case'+timestr+'.csv','case_en')

extract_chp('https://www.chp.gov.hk/files/pdf/building_list_chi.pdf','~/Documents/case'+timestr+'.csv','building_tc')
extract_chp('https://www.chp.gov.hk/files/pdf/building_list_eng.pdf','~/Documents/case'+timestr+'.csv','building_en')



#extract_chp('https://www.chp.gov.hk/files/pdf/599c_tc.pdf','~/Documents/confinee'+timestr+'.csv','confinee')

sys.stdout = old_stdout
log_file.close()
