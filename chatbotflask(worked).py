# -*- coding: utf-8 -*-
"""
Created on Mon Jun 24 20:28:32 2019

@author: admin1/fidelis galla limbong (fidelgalla@gmail.com)
"""
from flask import Flask, request, jsonify, make_response,send_file
from vibra import fig_webhook,data_last, data_last_tag,trending_motor, filter_tag,trending_motor_word, pie_chart_word

app = Flask(__name__)
    
def vib_chatbot():
    req = request.get_json(force = True)
    action = req.get('queryResult').get('action')
    tag_motor = req.get('queryResult').get('parameters').get('tag_motor')
    parameter = req.get('queryResult').get('parameters').get('vibration_parameter')
    result = {}
    
    if action == 'overview':
        df = pie_chart_word()
        normal = df[0]
        alert_high = df[1]
        danger_high = df[2]
        
        result = {}
        result['fulfillmentText'] = "Overview kondisi vibrasi plant 220 adalah normal :  "+str(normal)+' unit motor, alert high : '+str(alert_high)+ ' unit motor, dan danger high '+str(danger_high)+ ' unit motor'    
    
    elif action == 'last_measurement':
        data_recent = data_last()
        tag = data_recent[0]
        NDE_V_VEL = data_recent[1]
        NDE_H_VEL = data_recent[2]
        NDE_H_ENV = data_recent[3]
        NDE_H_ACC = data_recent[4]
        DE_V_VEL = data_recent[5]
        DE_H_VEL = data_recent[6]
        DE_H_ENV = data_recent[7]
        DE_H_ACC = data_recent[8]
        rekom = data_recent[9]
        
        result = {}
        result['fulfillmentText'] = "Pengukuran terbaru vibrasi menunjukkan motor "+tag+' memiliki nilai vibrasi NDE_V_VEL : '+str(NDE_V_VEL)+ ', NDE_H_VEL : '+str(NDE_H_VEL)+', NDE_H_ENV : '+str(NDE_H_ENV)+', NDE_H_ACC : '+str(NDE_H_ACC)+', DE_V_VEL : '+str(DE_V_VEL)+', DE_H_VEL : '+str(DE_H_VEL)+', DE_H_ENV : '+str(DE_H_ENV)+', NDE_H_ACC : '+str(DE_H_ACC)+' dengan rekomendasi : '+rekom                                       
    #return fullfillment responses
    
    elif action == 'last_measurement_motor':
        tag_last = data_last_tag(tag_motor)
        tag = tag_last[0]
        NDE_V_VEL = tag_last[1]
        NDE_H_VEL = tag_last[2]
        NDE_H_ENV = tag_last[3]
        NDE_H_ACC = tag_last[4]
        DE_V_VEL = tag_last[5]
        DE_H_VEL = tag_last[6]
        DE_H_ENV = tag_last[7]
        DE_H_ACC = tag_last[8]
        rekom = tag_last[9]
        date = tag_last[10]
        
        
        result = {}
        result['fulfillmentText'] = "Pengukuran terbaru vibrasi tanggal "+str(date)+" menunjukkan motor "+tag+' dengan hasil nilai vibrasi NDE_V_VEL : '+str(NDE_V_VEL)+ ', NDE_H_VEL : '+str(NDE_H_VEL)+', NDE_H_ENV : '+str(NDE_H_ENV)+', NDE_H_ACC : '+str(NDE_H_ACC)+', DE_V_VEL : '+str(DE_V_VEL)+', DE_H_VEL : '+str(DE_H_VEL)+', DE_H_ENV : '+str(DE_H_ENV)+', NDE_H_ACC : '+str(DE_H_ACC)+' dengan rekomendasi : '+rekom
        
    elif action == 'trending':
        tag_motor1 = filter_tag(tag_motor)
        trending_motor = trending_motor_word(tag_motor1,parameter)
        
        date1 = trending_motor[0][0]
        data1 = trending_motor[0][1]
        
        date2 = trending_motor[1][0]
        data2 = trending_motor[1][1]
        
        date3 = trending_motor[2][0]
        data3 = trending_motor[2][1]
        
        
        result = {}
        result['fulfillmentText'] = "Pengukuran pada "+str(date1)+" menunjukkan "+str(data1)+ ". Pengukuran pada "+str(date2)+" menunjukkan "+str(data2)+". Pengukuran pada "+str(date3)+" menunjukkan "+str(data3)
    
    return make_response(jsonify(result))

@app.route('/webhook',methods = ['GET','POST'])
def index():
    return vib_chatbot()

#this will be the end of the chatbot function session
 #----------------------------------------------------------------------------------------------#
#for returning the overview of the system
@app.route('/plots/overview_vibration', methods=['GET'])
def fig_telegram_overview():
    img = fig_webhook()
    return send_file(img,
                     attachment_filename='plot.jpg',
                     mimetype='image/jpg')
    
#for returning the overview of the trending of certain motor
@app.route('/plots/trending_motor', methods=['GET'])
def fig_telegram_trending():
    req = request.get_json(force = True)
    tag_motor = filter_tag(req.get('queryResult').get('parameters').get('tag_motor'))
    parameter = req.get('queryResult').get('parameters').get('vibration_parameter')
    img2 = trending_motor(tag_motor,parameter)
    return send_file(img2,
                     attachment_filename='trending_motor.jpg',
                     mimetype='image/jpg')



if __name__ == '__main__':
   app.run(debug = True)


