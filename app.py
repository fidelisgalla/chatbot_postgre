# -*- coding: utf-8 -*-
"""
Created on Sat Aug 31 19:00:35 2019

@author: admin1
"""

from flask import Flask, request, render_template
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
from vibra import pie_chart
from sqlalchemy import desc

app = Flask(__name__)
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_DATABASE_URI'] = "postgresql://postgres:1807fidel@localhost/vib2"
db = SQLAlchemy(app)

class Vibration(db.Model): 
    id = db.Column(db.Integer,primary_key = True)
    tag = db.Column(db.String(120),unique = False)
    date = db.Column(db.DateTime, unique = False)
    nde_v_vel = db.Column(db.Float, unique = False)
    nde_h_vel = db.Column(db.Float, unique = False)
    nde_h_env = db.Column(db.Float,unique=False)
    nde_h_acc = db.Column(db.Float, unique = False)
    de_v_vel = db.Column(db.Float,unique=False)
    de_h_vel = db.Column(db.Float,unique=False)
    de_h_env = db.Column(db.Float,unique=False)
    de_h_acc = db.Column(db.Float,unique=False)
    rekom = db.Column(db.String(120),unique=False)

    def __init__(self,tag,date,nde_v_vel,nde_h_vel,nde_h_env,nde_h_acc,de_v_vel,de_h_vel,de_h_env,de_h_acc,rekom):
        self.tag = tag
        self.date= date
        self.nde_v_vel = nde_v_vel
        self.nde_h_vel = nde_h_vel
        self.nde_h_env = nde_h_env
        self.nde_h_acc = nde_h_acc
        self.de_v_vel = de_v_vel
        self.de_h_vel = de_h_vel
        self.de_h_env = de_h_env
        self.de_h_acc = de_h_acc
        self.rekom = rekom

    def __repr__(self):
    	return '<Tag %r>' %self.tag

@app.route('/')
def home():
    graph1_url = pie_chart()
    return render_template('home.html',
    graph1=graph1_url)

@app.route('/form')
def form():
   return render_template('form.html')

@app.route('/add',methods = ['POST'])
def add():
    date = datetime.now().strftime("%Y-%m-%d %H:%M:%S")     
    if request.method=='POST':
        
        if not request.form['tag'] or not request.form['nde_v_vel'] or not request.form['nde_h_vel'] or not request.form['nde_h_env'] or not request.form['nde_h_acc'] or not request.form['de_v_vel'] or not request.form['de_h_vel'] or not request.form['de_h_env'] or not request.form['de_h_acc'] or not request.form['rekom']:
            msg = 'Please enter all the fields', 'error'
        else:
            data = Vibration(request.form['tag'], date, request.form['nde_v_vel'], request.form['nde_h_vel'], request.form['nde_h_env'], request.form['nde_h_acc'], request.form['de_v_vel'], request.form['de_h_vel'], request.form['de_h_env'], request.form['de_h_acc'], request.form['rekom'])
            db.session.add(data)
            db.session.commit()
            msg = 'Record was successfully added'
    else:
        pass
    return render_template('result.html', msg = msg)

@app.route('/list')
def list():
    return render_template('list.html', vibs = Vibration.query.order_by(desc(Vibration.date)).limit(30) )
        
if __name__ == '__main__':
    db.create_all()
    app.run(debug = True)