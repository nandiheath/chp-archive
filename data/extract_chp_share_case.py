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
timestr1 = time.strftime("%Y-%m-%d")

from datetime import datetime, timedelta
ytd=datetime.strftime(datetime.now() - timedelta(1), '%Y%m%d')


print("Finish Define Variable")

df_log=[]

def extract_chp(url,str1):
    os.system('mkdir -p ./'+timestr1 )
    filename = Path('./'+timestr1+'/tmp_'+str1+'.pdf')
    response = requests.get(url)
    filename.write_bytes(response.content)
    
    df=read_pdf('./'+timestr1+'/tmp_'+str1+'.pdf', multiple_tables=True, pages="all", lattice=True)
    #df=tabula.read_pdf('tmp_chp_'+str1+'.pdf', spreadsheet=True)
    
    new_col_name=df[0].columns
    new_col_name1=[x.replace('\n', '').replace('\r', '') for x in new_col_name]
    
    #df_all.rename(columns=dict(zip(df_all.columns[0:], new_col_name1)),inplace=True)
    #df[0].columns = np.arange(len(df[0].columns))
    for m in range(len(df[0].columns)):      
        if not(is_string_dtype(df[0].iloc[:,m])):
            df[0].iloc[:,m] = df[0].iloc[:,m].astype(str)
    df_all_row=df[0].select_dtypes(include=['object']).replace({'\r':' '},regex=True).replace({'\n':' '},regex=True)
    case_no=df[0].iloc[:,0]
    
    df[0].columns=new_col_name1
    df_all=pd.concat([case_no, df_all_row], axis=1)  
    
    for i in range(1,len(df),1):
        #if len(df[i].columns)==len(new_col_name):
            #df[i].columns = np.arange(len(df[i].columns))
            new_col_name=df[i].columns
            new_col_name1=[x.replace('\n', '').replace('\r', '') for x in new_col_name]
            df[i].columns=new_col_name1
            
            for m in range(len(df[i].columns)):      
                if not(is_string_dtype(df[i].iloc[:,m])):
                    df[i].iloc[:,m] = df[i].iloc[:,m].astype(str)
            df_all_row=df[i].select_dtypes(include=['object']).replace({'\r':' '},regex=True).replace({'\n':' '},regex=True)
            case_no=df[i].iloc[:,0]
            df_all_append=pd.concat([case_no, df_all_row], axis=1)  
            #df_all1=df_all.append(df_all_append)
            df_all = pd.concat([df_all.loc[:, ~df_all.columns.duplicated()], df_all_append.loc[:, ~df_all_append.columns.duplicated()]], ignore_index=True)
    
    for i in range(len(df_all)):
        if pd.isna(df_all.iloc[i,2]):
            for j in range(len(new_col_name)-1):
                if pd.isna(df_all.iloc[i,j])==False and pd.isna(df_all.iloc[i-1,1])==False:
                    if pd.isna(df_all.iloc[i-1,j])==False:
                        print(df_all.iloc[i-1,j] + df_all.iloc[i,j])
                        df_all.iloc[i-1,j]=df_all.iloc[i-1,j] +' ' + df_all.iloc[i,j]
                    else:
                        df_all.iloc[i-1,j]=df_all.iloc[i,j]
    
    
    df_all_export=df_all[pd.isna(df_all.iloc[:,1])==False]
    df_all_export=df_all_export.loc[:, ~df_all_export.columns.duplicated()]
    
    #df_all1=df_all[df_all['Unnamed: 0'].notnull()]
    df_log=DataFrame([len(df_all)])
    
    os.system('chmod 750 '+"./logs/df_log_"+str1+".csv")
    tmp_log = pd.read_csv("./logs/df_log_"+str1+".csv",header=0,index_col=False ) 
    lst_log=tmp_log.loc[0,'0']
  
    if df_log.loc[0,0] != lst_log:
        #df_all1.to_csv(output)
        #df_all = df_all.rename(columns=new_col_name1, axis='index')
        os.system('mkdir -p ./'+timestr1 )
        df_all_export.rename(columns=dict(zip(df_all_export.columns[0:], new_col_name1)),inplace=True)
        os.rename('./'+timestr1+'/tmp_'+str1+'.pdf', './'+timestr1+'/'+str1+'.pdf')
        #df_all.to_excel(r'~/Documents/chf_'+str1+'_'+timestr+'.xlsx')
        df_all_export.to_csv(r'./'+timestr1+'/'+str1+'.csv')
        df_log.to_csv("./logs/df_log_"+str1+".csv")
        
    else:
        #print ('No Update')
        os.remove('./'+timestr1+'/tmp_'+str1+'.pdf')
#extract_chp();

#print("Finish Processing building list")
extract_chp('https://www.chp.gov.hk/files/pdf/local_situation_covid19_tc.pdf','local_situation_covid19_tc')
extract_chp('https://www.chp.gov.hk/files/pdf/local_situation_covid19_en.pdf','local_situation_covid19_en')

extract_chp('https://www.chp.gov.hk/files/pdf/building_list_chi.pdf','building_list_tc')
extract_chp('https://www.chp.gov.hk/files/pdf/building_list_eng.pdf','building_list_en')

extract_chp('https://www.chp.gov.hk/files/pdf/flights_trains_tc.pdf','flights_trains_tc')
extract_chp('https://www.chp.gov.hk/files/pdf/flights_trains_en.pdf','flights_trains_en')



#extract_chp('https://www.chp.gov.hk/files/pdf/599c_tc.pdf','~/Documents/confinee'+timestr+'.csv','confinee')

sys.stdout = old_stdout
log_file.close()
