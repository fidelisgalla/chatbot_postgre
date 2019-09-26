# -*- coding: utf-8 -*-
"""
Created on Fri Jul 12 22:25:25 2019

@author: admin1/fidelis galla limbong (fidelgalla@gmail.com)
"""

import matplotlib.pyplot as plt
import io
import base64
import pandas as pd
import re
from sqlalchemy import create_engine

DATABASE_URL = 'postgres://jzjiblrwsoxiqa:5960f609af6b9f98035a0ae36df9c04ca3745cba8e75bacdf6afd3210711b8d8@ec2-54-83-55-122.compute-1.amazonaws.com:5432/d1j0qdp9aik676'
engine = create_engine(DATABASE_URL)


def pie_chart():
    df = pd.read_sql_query('select tag,date,nde_v_vel, nde_h_vel,nde_h_env, nde_h_acc,de_v_vel, de_h_vel, de_h_env,de_h_acc,rekom from vibration order by (date) desc',con=engine)
    tags = ['220-PM-1A','220-PM-1B','220-PM-2A','220-PM-2B','220-PM-3A','220-PM-3B','220-PM-4A','220-PM-4B','220-PM-5A','220-PM-5B','220-PM-6A','220-PM-6B','220-PM-7A'] #please add the tags anymore
    series_list = []
    for tag in tags:
        df1 = df[df['tag']==tag].iloc[0]
        series_list.append(df1)
    df_series = pd.DataFrame(series_list)
    df2 = df_series
    for i in df2.index:
        if df2['nde_v_vel'][i]<6 and df2['nde_h_vel'][i]<6 and df2['nde_h_env'][i]<5 and df2['nde_h_acc'][i]<5 and df2['de_v_vel'][i]<6 and df2['de_h_vel'][i]<6 and df2['de_h_env'][i]<5 and df2['de_h_acc'][i]<5: 
            if df2['nde_v_vel'][i]<3.25 and df2['nde_h_vel'][i]<3.25 and df2['nde_h_env'][i]<3 and df2['nde_h_acc'][i]<3 and df2['de_v_vel'][i]<3.25 and df2['de_h_vel'][i]<3.25 and df2['de_h_env'][i]<3 and df2['de_h_acc'][i]<3:
                df2.at[i,'STATUS'] = 'normal'
            else :
                df2.at[i,'STATUS'] = 'alert high'
        else :
            df2.at[i,'STATUS'] = 'danger high'
        df3 = df2
    
    
    normal = len(df3[df3['STATUS']=='normal'])
    alert_high = len(df3[df3['STATUS']=='alert high'])
    danger_high = len(df3[df3['STATUS']=='danger high'])
    
    labels = ['Normal','Alert High','Danger High']
    sizes = [normal, alert_high, danger_high]
    colors = ['#ff9999','#66b3ff','#99ff99','#ffcc99']
 
    
    fig1, ax1 = plt.subplots()
    patches, texts, autotexts = ax1.pie(sizes, colors = colors, labels=labels, autopct='%1.1f%%', startangle=90)
    for text in texts:
        text.set_color('grey')
    for autotext in autotexts:
        autotext.set_color('grey')
# Equal aspect ratio ensures that pie is drawn as a circle
    ax1.axis('equal')  
    plt.tight_layout()
    img = io.BytesIO()
    plt.savefig(img, format='jpg')
    img.seek(0)
    graph_url = base64.b64encode(img.getvalue()).decode()
    plt.close()
    return 'data:image/png;base64,{}'.format(graph_url)


#function to return the overview of the entire plant( the overview is in the figure format)
def fig_webhook():
    df = pd.read_sql_query('select tag,date,nde_v_vel, nde_h_vel,nde_h_env, nde_h_acc,de_v_vel, de_h_vel, de_h_env,de_h_acc,rekom from vibration ORDER BY date DESC',con=engine)
    tags = ['220-PM-1A','220-PM-1B','220-PM-2A','220-PM-2B','220-PM-3A','220-PM-3B','220-PM-4A','220-PM-4B','220-PM-5A','220-PM-5B','220-PM-6A','220-PM-6B','220-PM-7A']
    series_list = []
    for tag in tags:
        df1 = df[df['tag']==tag].iloc[0]
        series_list.append(df1)
    df_series = pd.DataFrame(series_list)
    df2 = df_series
    for i in df2.index:
        if df2['nde_v_vel'][i]<6 and df2['nde_h_vel'][i]<6 and df2['nde_h_env'][i]<5 and df2['nde_h_acc'][i]<5 and df2['de_v_vel'][i]<6 and df2['de_h_vel'][i]<6 and df2['de_h_env'][i]<5 and df2['de_h_acc'][i]<5: 
            if df2['nde_v_vel'][i]<3.25 and df2['nde_h_vel'][i]<3.25 and df2['nde_h_env'][i]<3 and df2['nde_h_acc'][i]<3 and df2['de_v_vel'][i]<3.25 and df2['de_h_vel'][i]<3.25 and df2['de_h_env'][i]<3 and df2['de_h_acc'][i]<3:
                df2.at[i,'STATUS'] = 'normal'
            else :
                df2.at[i,'STATUS'] = 'alert high'
        else :
            df2.at[i,'STATUS'] = 'danger high'
        df3 = df2
    
    normal = len(df3[df3['STATUS']=='normal'])
    alert_high = len(df3[df3['STATUS']=='alert high'])
    danger_high = len(df3[df3['STATUS']=='danger high'])

    #process of making figure
    
    labels = ['Normal','Alert High','Danger High']
    sizes = [normal, alert_high, danger_high]
    colors = ['#ff9999','#66b3ff','#99ff99','#ffcc99']
 
    img = io.BytesIO()
    fig1, ax1 = plt.subplots()
    patches, texts, autotexts = ax1.pie(sizes, colors = colors, labels=labels, autopct='%1.1f%%', startangle=90)
    for text in texts:
        text.set_color('grey')
    for autotext in autotexts:
        autotext.set_color('grey')
# Equal aspect ratio ensures that pie is drawn as a circle
    ax1.axis('equal')  
    plt.tight_layout()
    plt.savefig(img, format='png')
    img.seek(0)
    return img

#function to return the latest value of measurement
def data_last():
    df_last = pd.read_sql_query('select tag,date,nde_v_vel, nde_h_vel,nde_h_env, nde_h_acc,de_v_vel, de_h_vel, de_h_env,de_h_acc,rekom from vibration ORDER BY date DESC',con=engine)
    tag = df_last.iloc[0]['tag']
    NDE_V_VEL = df_last.iloc[0]['nde_v_vel']
    NDE_H_VEL = df_last.iloc[0]['nde_h_vel']
    NDE_H_ENV = df_last.iloc[0]['nde_h_env']
    NDE_H_ACC = df_last.iloc[0]['nde_h_acc']
    DE_V_VEL = df_last.iloc[0]['de_v_vel']
    DE_H_VEL = df_last.iloc[0]['nde_h_vel']
    DE_H_ENV = df_last.iloc[0]['de_h_env']
    DE_H_ACC = df_last.iloc[0]['de_h_acc']
    rekom = df_last.iloc[0]['rekom']
    return tag, NDE_V_VEL, NDE_H_VEL, NDE_H_ENV, NDE_H_ACC, DE_V_VEL, DE_H_VEL, DE_H_ENV, DE_H_ACC, rekom

#function to return the latest value of measurement based on specific tag
def data_last_tag(tag):
    df_last = pd.read_sql_query('select tag,date,nde_v_vel, nde_h_vel,nde_h_env, nde_h_acc,de_v_vel, de_h_vel, de_h_env,de_h_acc,rekom from vibration ORDER BY date DESC',con=engine)
    tag_selected = df_last[df_last['tag']==tag]
    date = tag_selected.iloc[0]['date']
    NDE_V_VEL = tag_selected.iloc[0]['nde_v_vel']
    NDE_H_VEL = tag_selected.iloc[0]['nde_h_vel']
    NDE_H_ENV = tag_selected.iloc[0]['nde_h_env']
    NDE_H_ACC = tag_selected.iloc[0]['nde_h_acc']
    DE_V_VEL = tag_selected.iloc[0]['de_v_vel']
    DE_H_VEL = tag_selected.iloc[0]['de_h_vel']
    DE_H_ENV = tag_selected.iloc[0]['de_h_env']
    DE_H_ACC = tag_selected.iloc[0]['de_h_acc']
    rekom = tag_selected.iloc[0]['rekom']
    
    return tag, NDE_V_VEL, NDE_H_VEL, NDE_H_ENV, NDE_H_ACC, DE_V_VEL, DE_H_VEL, DE_H_ENV, DE_H_ACC, rekom,date


#function to return the trending of motor
def trending_motor(tag,parameter):
    df = pd.read_sql_query('select tag,date,nde_v_vel, nde_h_vel,nde_h_env, nde_h_acc,de_v_vel, de_h_vel, de_h_env,de_h_acc,rekom from vibration ORDER BY date DESC',con=engine)
    a = df[df['tag']==tag][['date',parameter]]
    
    date = a['date']
    value = a[parameter]
    
    img2 = io.BytesIO()
    plt.plot(date,value)
    plt.savefig(img2, format='jpg')
    img2.seek(0)
    return img2

#additional function for regular expression for filtering the tag of motor
def filter_tag(tag):
    pattern = r'\d{3}-\w{2}-\d\w'
    match = re.search(pattern,str(tag))
    return match.group()

def trending_motor_word(tag,parameter):
    df = pd.read_sql_query('select tag,date,nde_v_vel, nde_h_vel,nde_h_env, nde_h_acc,de_v_vel, de_h_vel, de_h_env,de_h_acc,rekom from vibration ORDER BY date DESC',con=engine)
    b = df[df['tag']==tag][['date',parameter]]
    data1 = b.iloc[0]
    data2 = b.iloc[1]
    data3 = b.iloc[2]
    
    return data1, data2, data3

def pie_chart_word():
    df = pd.read_sql_query('select tag,date,nde_v_vel, nde_h_vel,nde_h_env, nde_h_acc,de_v_vel, de_h_vel, de_h_env,de_h_acc,rekom from vibration ORDER BY date DESC',con=engine)
    tags = ['220-PM-1A','220-PM-1B','220-PM-2A','220-PM-2B','220-PM-3A','220-PM-3B','220-PM-4A','220-PM-4B','220-PM-5A','220-PM-5B','220-PM-6A','220-PM-6B','220-PM-7A']
    series_list = []
    for tag in tags:
        df1 = df[df['tag']==tag].iloc[0]
        series_list.append(df1)
    df_series = pd.DataFrame(series_list)
    df2 = df_series
    for i in df2.index:
        if df2['nde_v_vel'][i]<6 and df2['nde_h_vel'][i]<6 and df2['nde_h_env'][i]<5 and df2['nde_h_acc'][i]<5 and df2['de_v_vel'][i]<6 and df2['de_h_vel'][i]<6 and df2['de_h_env'][i]<5 and df2['de_h_acc'][i]<5: 
            if df2['nde_v_vel'][i]<3.25 and df2['nde_h_vel'][i]<3.25 and df2['nde_h_env'][i]<3 and df2['nde_h_acc'][i]<3 and df2['de_v_vel'][i]<3.25 and df2['de_h_vel'][i]<3.25 and df2['de_h_env'][i]<3 and df2['de_h_acc'][i]<3:
                df2.at[i,'STATUS'] = 'normal'
            else :
                df2.at[i,'STATUS'] = 'alert high'
        else :
            df2.at[i,'STATUS'] = 'danger high'
        df3 = df2
    
    normal = len(df3[df3['STATUS']=='normal'])
    alert_high = len(df3[df3['STATUS']=='alert high'])
    danger_high = len(df3[df3['STATUS']=='danger high'])

    return normal, alert_high, danger_high


    
    