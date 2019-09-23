# -*- coding: utf-8 -*-
"""
Created on Sat Sep  7 18:50:58 2019

@author: admin1
"""

from vibra import db,Vibration

data1= Vibration('220-PM-1A',2.1,3,5,0.9,0.5,0.2,0.3,0.4,'agar dilakukan perbaikan')
db.session.add(data1)
db.session.commit()