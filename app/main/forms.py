# -*- coding:utf-8 -*-

from flask_wtf import Form
import re
from wtforms import StringField,SubmitField,PasswordField,SelectField, RadioField, BooleanField, IntegerField





#新建系统设置表单
class Production_Forms(Form):
    company_name = StringField('company_name')
    order_number = StringField('company_name')
    adress = StringField('company_name')
    client_name = StringField('company_name')
    client_tel = StringField('company_name')
    saler_name = StringField('company_name')
    saler_tel = StringField('company_name')
    
    delivery_way1 = BooleanField('delivery_way1',default=False)
    delivery_way2 = BooleanField('delivery_way2',default=False)
    delivery_way3 = BooleanField('delivery_way3',default=False)
    delivery_way4 = BooleanField('delivery_way4',default=False)
    delivery_way5 = BooleanField('delivery_way5',default=False)




























    resolution = SelectField('Resolution',choices=[(1,'Auto'),(2,'1024 x 768'),(3,'1280 x720'),(4,'1280 x 1024'),(5,'1366 x 768'),(6,'1440 x 900'),
                                                   (7,'1600 x900'),(8,'1680 x 1050'),(9,'1920 x 1080')])
    vsy = RadioField('Vsy',choices=[(1,u'60赫兹'),(2,u'70赫兹'),(3,u'75赫兹'),(4,u'85赫兹')])
    color = SelectField('Color',choices=[(1,u'32位真彩色'),(2,u'24位真彩色'),(3,u'16位真彩色'),(4,u'256色')])
    standby = SelectField('standby',choices=[(1,'0'),(2,'10'),(3,'20'),(4,'30'),(5,'40'),(6,'50'),(7,'60')])
    offtime = SelectField('offtime',choices=[(1,'0'),(2,'10'),(3,'20'),(4,'30'),(5,'40'),(6,'50'),(7,'60')])
    mu = RadioField('Vsy',choices=[(1,u'中文简体'),(2,u'中文繁体'),(3,'English')])
    print1 = BooleanField('Print1',default=False)
    p1port = SelectField('p1port',choices=[(1,'LPT'),(2,'COM'),(3,('USB'))])
    p1drv = StringField('P1drv')
    print2 = BooleanField('Print2',default=False)
    p2port = SelectField('p2port',choices=[(1,'USB'),(2,'COM')])
    p2drv = StringField('P2drv')
    pwdoption = RadioField('pwdoption',choices=[(1,u'使用密码'),(2,u'无需密码')])
    password1 = PasswordField('password1')
    password2 = PasswordField('password2')
    name = StringField('Name') #设备名称
    mac = StringField('MAC') #网卡物理地址
    type = BooleanField('type',default=False)
    ip = StringField('IP')
    subnet = StringField('Subnet')
    gateway = StringField('Gateway')
    dns1 = StringField('Dns1')
    dns2 = StringField('Dns2')
    nettype = BooleanField('NetType',default=False)
    ssid = StringField('Ssid')
    wpassword1 = PasswordField('wpassword1')
    wpassword2 = PasswordField('wpassword2')


    submit = SubmitField('submit')



