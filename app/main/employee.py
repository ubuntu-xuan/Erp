# -*- coding:utf-8 -*-
__author__ = 'xuan'

from flask import render_template,request,current_app,redirect,url_for,send_from_directory
from  . import  main
from flask.ext.login import login_required,current_user,login_user,logout_user
import json,MySQLdb,sys
from  manage import  db  #不添加这个会不能更新数据库
from ..models import Performance_Related
import json
import time
import string
from manage import app
import os
import simplejson
from config import config

reload(sys) 
sys.setdefaultencoding('utf8') 


get_time = time.strftime('%Y-%m-%d',time.localtime(time.time()))
get_year = time.strftime('%Y',time.localtime(time.time()))
get_month = time.strftime('%m',time.localtime(time.time()))



def getCon():
    try:
        '''warning:这里需要设置为环境获取'''
        conn = MySQLdb.connect("localhost","root","uroot012","erp_development",charset='utf8')
        return conn  

    except:
        print 'MySQL connect fail...'
        import traceback
        traceback.print_exc()
        # 发生错误时会滚
        conn.rollback()


 
#一月
@main.route('/employee/performance_related_Jan',methods = ['GET','POST'])
@login_required
def performance_related_Jan():
    username = current_user.username
    if username == "liangzhixuan":
        username = '梁智轩'
    elif username == "mark":
        username = '梁嘉惠'
    elif username == "jerry":
        username = '黄德欣'
    elif username == "tommy":
        username = '梁嘉和'
    elif username == "yangmujiao":
        username = '杨木娇'
    elif username == "lixiurong":
        username = '李秀荣'
    elif username == "oujie":
        username = '欧捷'
    elif username == "zhuxiaoping":
        username = '朱晓平'

    id = request.form.get('row[id]', '')
    date = request.form.get('row[date]', '')
    name= request.form.get('row[name]', '')
    place= request.form.get('row[place]', '')
    content= request.form.get('row[content]', '')
    complete= request.form.get('row[complete]', '')  
    integration= request.form.get('row[integration]', '')
    remarks= request.form.get('row[remarks]', '')  
    year= request.form.get('row[year]', '') 
    month= request.form.get('row[month]', '') 
 
    """建立表格ID与数据表ID的关联"""  

    #连接数据库
    cursor = getCon().cursor() 
    cursor.execute("SELECT * from performance_related where month='01'  and name='%s' "%username)
    data = cursor.fetchall()
       
    if len(data) !=0:
	
        input_get=[]
        output_get=[]

        get_data=[]
        for i,w in enumerate(data):
            get_data.append(w[0])
      
        id_from_table = []
        id_from_mysql = []
	for i,datas in enumerate(get_data):
            id_from_table.append(i+1)
            id_from_mysql.append(datas)

        id_concect = dict(zip(id_from_table,id_from_mysql))
        print id_concect

    #cursor.close()
    #getCon().close()


    if id !='':
        old_Value = Performance_Related.query.filter_by(id=id_concect[int(id)]).first()
        if  old_Value is not None:
            print "更新数据"
            Performance_Related.query.filter_by(id=id_concect[int(id)]).update({"date":date,"name":name,"place":place,"content":content,"complete":complete,"integration":integration,"remarks":remarks,"year":year,"month":month}) 
        db.session.commit()    

    #增加  
    add =request.form.get('add','')
   
    if add == 'add_true':
        add_item = Performance_Related(date=get_time,name=username,place='',content='',complete='',integration='',remarks='',year=get_year,month='01')

        db.session.add(add_item)
        db.session.commit() 


    '''删除记录'''
    def reset_delete(ids):
        #连接数据库
        try:
            '''warning:这里需要设置为环境获取'''
            conn = MySQLdb.connect("localhost","root","uroot012","erp_development",charset='utf8')
            cursor = conn.cursor()
        except:
            print 'MySQL connect fail...'
            import traceback
            traceback.print_exc()
            # 发生错误时会滚
            conn.rollback()

        print '删除记录',id_concect[int(ids)]
        cursor.execute("DELETE FROM performance_related WHERE id=%s"%id_concect[int(ids)])   
  
        cursor.close()
        conn.commit()
        conn.close()


    #删除数据
    ids = request.form.get('ids[]','')

    if ids != "":
        reset_delete(ids)


    return render_template("employee/performance-related-Jan.html")



@main.route('/employee/performance_related_Jan/return_json',methods = ['GET','POST'])
@login_required
def performance_related_Jan_return_json():
    username = current_user.username
    if username == "liangzhixuan":
        username = '梁智轩'
    elif username == "mark":
        username = '梁嘉惠'
    elif username == "jerry":
        username = '黄德欣'
    elif username == "tommy":
        username = '梁嘉和'
    elif username == "yangmujiao":
        username = '杨木娇'
    elif username == "lixiurong":
        username = '李秀荣'
    elif username == "oujie":
        username = '欧捷'
    elif username == "zhuxiaoping":
        username = '朱晓平'
    #连接数据库
    cursor = getCon().cursor()

    cursor.execute("SELECT * from performance_related where month='01' and name='%s' "%username)
    data = cursor.fetchall()

    cursor.close()
    getCon().close() 

    jsonData = []

    for n,row  in enumerate(data):
        #print data[0]
        ##print row[1]
        result = {}
        result['id'] = n + 1
        result['date'] = row[1].strftime('%Y-%m-%d')
        result['name'] = row[2]
        result['place'] = row[3]
        result['content'] = row[4]
        result['complete'] = row[5]
        result['integration'] = row[6]
        result['year'] = row[7]
        result['month'] = row[8]
        result['remarks'] = row[9]
    
        jsonData.append(result)

    return json.dumps(jsonData)


#二月
@main.route('/employee/performance_related_Feb',methods = ['GET','POST'])
@login_required
def performance_related_Feb():
    username = current_user.username
    if username == "liangzhixuan":
        username = '梁智轩'
    elif username == "mark":
        username = '梁嘉惠'
    elif username == "jerry":
        username = '黄德欣'
    elif username == "tommy":
        username = '梁嘉和'
    elif username == "yangmujiao":
        username = '杨木娇'
    elif username == "lixiurong":
        username = '李秀荣'
    elif username == "oujie":
        username = '欧捷'
    elif username == "zhuxiaoping":
        username = '朱晓平'

    id = request.form.get('row[id]', '')
    date = request.form.get('row[date]', '')
    name= request.form.get('row[name]', '')
    place= request.form.get('row[place]', '')
    content= request.form.get('row[content]', '')
    complete= request.form.get('row[complete]', '')  
    integration= request.form.get('row[integration]', '') 
    remarks= request.form.get('row[remarks]', '')  
    year= request.form.get('row[year]', '') 
    month= request.form.get('row[month]', '') 
 
    """建立表格ID与数据表ID的关联"""  

    #连接数据库
    cursor = getCon().cursor() 
    cursor.execute("SELECT * from performance_related where month='02' and name='%s' "%username)
    data = cursor.fetchall()
       
    if len(data) !=0:
	
        input_get=[]
        output_get=[]

        get_data=[]
        for i,w in enumerate(data):
            get_data.append(w[0])
      
        id_from_table = []
        id_from_mysql = []
	for i,datas in enumerate(get_data):
            id_from_table.append(i+1)
            id_from_mysql.append(datas)

        id_concect = dict(zip(id_from_table,id_from_mysql))
        print id_concect

    #cursor.close()
    #getCon().close()

    if id !='':
        old_Value = Performance_Related.query.filter_by(id=id_concect[int(id)]).first()
        if  old_Value is not None:
            print "更新数据"
            Performance_Related.query.filter_by(id=id_concect[int(id)]).update({"date":date,"name":name,"place":place,"content":content,"complete":complete,"integration":integration,"remarks":remarks,"year":year,"month":month}) 
        db.session.commit()    

    #增加  
    add =request.form.get('add','')
   
    if add == 'add_true':
        add_item = Performance_Related(date=get_time,name=username,place='',content='',complete='',integration='',remarks='',year=get_year,month='02')

        db.session.add(add_item)
        db.session.commit() 


    '''删除记录'''
    def reset_delete(ids):
        #连接数据库
        try:
            '''warning:这里需要设置为环境获取'''
            conn = MySQLdb.connect("localhost","root","uroot012","erp_development",charset='utf8')
            cursor = conn.cursor()
        except:
            print 'MySQL connect fail...'
            import traceback
            traceback.print_exc()
            # 发生错误时会滚
            conn.rollback()

        print '删除记录',id_concect[int(ids)]
        cursor.execute("DELETE FROM performance_related WHERE id=%s"%id_concect[int(ids)])   
  
        cursor.close()
        conn.commit()
        conn.close()


    #删除数据
    ids = request.form.get('ids[]','')

    if ids != "":
        reset_delete(ids)

    return render_template("employee/performance-related-Feb.html")

@main.route('/employee/performance_related_Feb/return_json',methods = ['GET','POST'])
@login_required
def performance_related_Feb_return_json():

    username = current_user.username
    if username == "liangzhixuan":
        username = '梁智轩'
    elif username == "mark":
        username = '梁嘉惠'
    elif username == "jerry":
        username = '黄德欣'
    elif username == "tommy":
        username = '梁嘉和'
    elif username == "yangmujiao":
        username = '杨木娇'
    elif username == "lixiurong":
        username = '李秀荣'
    elif username == "oujie":
        username = '欧捷'
    elif username == "zhuxiaoping":
        username = '朱晓平'

    #连接数据库
    cursor = getCon().cursor()

    cursor.execute("SELECT * from performance_related where month='02' and name='%s' "%username)
    data = cursor.fetchall()

    cursor.close()
    getCon().close() 

    jsonData = []

    for n,row  in enumerate(data):
        #print data[0]
        ##print row[1]
        result = {}
        result['id'] = n + 1
        result['date'] = row[1].strftime('%Y-%m-%d')
        result['name'] = row[2]
        result['place'] = row[3]
        result['content'] = row[4]
        result['complete'] = row[5]
        result['integration'] = row[6]
        result['year'] = row[7]
        result['month'] = row[8]
        result['remarks'] = row[9]
    
        jsonData.append(result)

    return json.dumps(jsonData)


#三月
@main.route('/employee/performance_related_Mar',methods = ['GET','POST'])
@login_required
def performance_related_Mar():

    username = current_user.username
    if username == "liangzhixuan":
        username = '梁智轩'
    elif username == "mark":
        username = '梁嘉惠'
    elif username == "jerry":
        username = '黄德欣'
    elif username == "tommy":
        username = '梁嘉和'
    elif username == "yangmujiao":
        username = '杨木娇'
    elif username == "lixiurong":
        username = '李秀荣'
    elif username == "oujie":
        username = '欧捷'
    elif username == "zhuxiaoping":
        username = '朱晓平'

    id = request.form.get('row[id]', '')
    date = request.form.get('row[date]', '')
    name= request.form.get('row[name]', '')
    place= request.form.get('row[place]', '')
    content= request.form.get('row[content]', '')
    complete= request.form.get('row[complete]', '')  
    integration= request.form.get('row[integration]', '') 
    remarks= request.form.get('row[remarks]', '')  
    year= request.form.get('row[year]', '') 
    month= request.form.get('row[month]', '') 
 
    """建立表格ID与数据表ID的关联"""  

    #连接数据库
    cursor = getCon().cursor() 
    cursor.execute("SELECT * from performance_related where month='03' and name='%s' "%username)
    data = cursor.fetchall()
       
    if len(data) !=0:
	
        input_get=[]
        output_get=[]

        get_data=[]
        for i,w in enumerate(data):
            get_data.append(w[0])
      
        id_from_table = []
        id_from_mysql = []
	for i,datas in enumerate(get_data):
            id_from_table.append(i+1)
            id_from_mysql.append(datas)

        id_concect = dict(zip(id_from_table,id_from_mysql))
        print id_concect

    #cursor.close()
    #getCon().close()

    if id !='':
        old_Value = Performance_Related.query.filter_by(id=id_concect[int(id)]).first()
        if  old_Value is not None:
            print "更新数据"
            Performance_Related.query.filter_by(id=id_concect[int(id)]).update({"date":date,"name":name,"place":place,"content":content,"complete":complete,"integration":integration,"remarks":remarks,"year":year,"month":month}) 
        db.session.commit()    

    #增加  
    add =request.form.get('add','')
   
    if add == 'add_true':
        add_item = Performance_Related(date=get_time,name=username,place='',content='',complete='',integration='',remarks='',year=get_year,month='03')

        db.session.add(add_item)
        db.session.commit() 


    '''删除记录'''
    def reset_delete(ids):
        #连接数据库
        try:
            '''warning:这里需要设置为环境获取'''
            conn = MySQLdb.connect("localhost","root","uroot012","erp_development",charset='utf8')
            cursor = conn.cursor()
        except:
            print 'MySQL connect fail...'
            import traceback
            traceback.print_exc()
            # 发生错误时会滚
            conn.rollback()

        print '删除记录',id_concect[int(ids)]
        cursor.execute("DELETE FROM performance_related WHERE id=%s"%id_concect[int(ids)])   
  
        cursor.close()
        conn.commit()
        conn.close()


    #删除数据
    ids = request.form.get('ids[]','')

    if ids != "":
        reset_delete(ids)

    return render_template("employee/performance-related-Mar.html")



@main.route('/employee/performance_related_Mar/return_json',methods = ['GET','POST'])
@login_required
def performance_related_Mar_return_json():

    username = current_user.username
    if username == "liangzhixuan":
        username = '梁智轩'
    elif username == "mark":
        username = '梁嘉惠'
    elif username == "jerry":
        username = '黄德欣'
    elif username == "tommy":
        username = '梁嘉和'
    elif username == "yangmujiao":
        username = '杨木娇'
    elif username == "lixiurong":
        username = '李秀荣'
    elif username == "oujie":
        username = '欧捷'
    elif username == "zhuxiaoping":
        username = '朱晓平'

    #连接数据库
    cursor = getCon().cursor()

    cursor.execute("SELECT * from performance_related where month='03' and name='%s' "%username)
    data = cursor.fetchall()

    cursor.close()
    getCon().close() 

    jsonData = []

    for n,row  in enumerate(data):
        #print data[0]
        ##print row[1]
        result = {}
        result['id'] = n + 1
        result['date'] = row[1].strftime('%Y-%m-%d')
        result['name'] = row[2]
        result['place'] = row[3]
        result['content'] = row[4]
        result['complete'] = row[5]
        result['integration'] = row[6]
        result['year'] = row[7]
        result['month'] = row[8]
        result['remarks'] = row[9]
    
        jsonData.append(result)

    return json.dumps(jsonData)


#四月
@main.route('/employee/performance_related_Apr',methods = ['GET','POST'])
@login_required
def performance_related_Apr():

    username = current_user.username
    if username == "liangzhixuan":
        username = '梁智轩'
    elif username == "mark":
        username = '梁嘉惠'
    elif username == "jerry":
        username = '黄德欣'
    elif username == "tommy":
        username = '梁嘉和'
    elif username == "yangmujiao":
        username = '杨木娇'
    elif username == "lixiurong":
        username = '李秀荣'
    elif username == "oujie":
        username = '欧捷'
    elif username == "zhuxiaoping":
        username = '朱晓平'

    id = request.form.get('row[id]', '')
    date = request.form.get('row[date]', '')
    name= request.form.get('row[name]', '')
    place= request.form.get('row[place]', '')
    content= request.form.get('row[content]', '')
    complete= request.form.get('row[complete]', '')  
    integration= request.form.get('row[integration]', '') 
    remarks= request.form.get('row[remarks]', '')  
    year= request.form.get('row[year]', '') 
    month= request.form.get('row[month]', '') 
 
    """建立表格ID与数据表ID的关联"""  

    #连接数据库
    cursor = getCon().cursor() 
    cursor.execute("SELECT * from performance_related where month='04' and name='%s' "%username)
    data = cursor.fetchall()
       
    if len(data) !=0:
	
        input_get=[]
        output_get=[]

        get_data=[]
        for i,w in enumerate(data):
            get_data.append(w[0])
      
        id_from_table = []
        id_from_mysql = []
	for i,datas in enumerate(get_data):
            id_from_table.append(i+1)
            id_from_mysql.append(datas)

        id_concect = dict(zip(id_from_table,id_from_mysql))
        print id_concect

    #cursor.close()
    #getCon().close()

    if id !='':
        old_Value = Performance_Related.query.filter_by(id=id_concect[int(id)]).first()
        if  old_Value is not None:
            print "更新数据"
            Performance_Related.query.filter_by(id=id_concect[int(id)]).update({"date":date,"name":name,"place":place,
             "content":content,"complete":complete,"integration":integration,"remarks":remarks,"year":year,"month":month}) 
        db.session.commit()    

    #增加  
    add =request.form.get('add','')
   
    if add == 'add_true':
        add_item = Performance_Related(date=get_time,name=username,place='',content='',complete='',integration='',remarks='',year=get_year,month='04')

        db.session.add(add_item)
        db.session.commit() 


    '''删除记录'''
    def reset_delete(ids):
        #连接数据库
        try:
            '''warning:这里需要设置为环境获取'''
            conn = MySQLdb.connect("localhost","root","uroot012","erp_development",charset='utf8')
            cursor = conn.cursor()
        except:
            print 'MySQL connect fail...'
            import traceback
            traceback.print_exc()
            # 发生错误时会滚
            conn.rollback()

        print '删除记录',id_concect[int(ids)]
        cursor.execute("DELETE FROM performance_related WHERE id=%s"%id_concect[int(ids)])   
  
        cursor.close()
        conn.commit()
        conn.close()


    #删除数据
    ids = request.form.get('ids[]','')

    if ids != "":
        reset_delete(ids)

    return render_template("employee/performance-related-Apr.html")


@main.route('/employee/performance_related_Apr/return_json',methods = ['GET','POST'])
@login_required
def performance_related_Apr_return_json():

    username = current_user.username
    if username == "liangzhixuan":
        username = '梁智轩'
    elif username == "mark":
        username = '梁嘉惠'
    elif username == "jerry":
        username = '黄德欣'
    elif username == "tommy":
        username = '梁嘉和'
    elif username == "yangmujiao":
        username = '杨木娇'
    elif username == "lixiurong":
        username = '李秀荣'
    elif username == "oujie":
        username = '欧捷'
    elif username == "zhuxiaoping":
        username = '朱晓平'

    #连接数据库
    cursor = getCon().cursor()

    cursor.execute("SELECT * from performance_related where month='04' and name='%s' "%username)
    data = cursor.fetchall()

    cursor.close()
    getCon().close() 

    jsonData = []

    for n,row  in enumerate(data):
        #print data[0]
        ##print row[1]
        result = {}
        result['id'] = n + 1
        result['date'] = row[1].strftime('%Y-%m-%d')
        result['name'] = row[2]
        result['place'] = row[3]
        result['content'] = row[4]
        result['complete'] = row[5]
        result['integration'] = row[6]
        result['year'] = row[7]
        result['month'] = row[8]
        result['remarks'] = row[9]
    
        jsonData.append(result)

    return json.dumps(jsonData)


#五月
@main.route('/employee/performance_related_May',methods = ['GET','POST'])
@login_required
def performance_related_May():

    username = current_user.username
    if username == "liangzhixuan":
        username = '梁智轩'
    elif username == "mark":
        username = '梁嘉惠'
    elif username == "jerry":
        username = '黄德欣'
    elif username == "tommy":
        username = '梁嘉和'
    elif username == "yangmujiao":
        username = '杨木娇'
    elif username == "lixiurong":
        username = '李秀荣'
    elif username == "oujie":
        username = '欧捷'
    elif username == "zhuxiaoping":
        username = '朱晓平'

    id = request.form.get('row[id]', '')
    date = request.form.get('row[date]', '')
    name= request.form.get('row[name]', '')
    place= request.form.get('row[place]', '')
    content= request.form.get('row[content]', '')
    complete= request.form.get('row[complete]', '')  
    integration= request.form.get('row[integration]', '') 
    remarks= request.form.get('row[remarks]', '')  
    year= request.form.get('row[year]', '') 
    month= request.form.get('row[month]', '') 
 
    """建立表格ID与数据表ID的关联"""  

    #连接数据库
    cursor = getCon().cursor() 
    cursor.execute("SELECT * from performance_related where month='05' and name='%s' "%username)
    data = cursor.fetchall()
       
    if len(data) !=0:
	
        input_get=[]
        output_get=[]

        get_data=[]
        for i,w in enumerate(data):
            get_data.append(w[0])
      
        id_from_table = []
        id_from_mysql = []
	for i,datas in enumerate(get_data):
            id_from_table.append(i+1)
            id_from_mysql.append(datas)

        id_concect = dict(zip(id_from_table,id_from_mysql))
        print id_concect

    #cursor.close()
    #getCon().close()


    if id !='':
        old_Value = Performance_Related.query.filter_by(id=id_concect[int(id)]).first()
        if  old_Value is not None:
            print "更新数据"
            Performance_Related.query.filter_by(id=id_concect[int(id)]).update({"date":date,"name":name,"place":place,
             "content":content,"complete":complete,"integration":integration,"remarks":remarks,"year":year,"month":month}) 
        db.session.commit()    

    #增加  
    add =request.form.get('add','')
   
    if add == 'add_true':
        add_item = Performance_Related(date=get_time,name=username,place='',content='',complete='',integration='',remarks='',year=get_year,month='05')

        db.session.add(add_item)
        db.session.commit() 


    '''删除记录'''
    def reset_delete(ids):
        #连接数据库
        try:
            '''warning:这里需要设置为环境获取'''
            conn = MySQLdb.connect("localhost","root","uroot012","erp_development",charset='utf8')
            cursor = conn.cursor()
        except:
            print 'MySQL connect fail...'
            import traceback
            traceback.print_exc()
            # 发生错误时会滚
            conn.rollback()

        print '删除记录',id_concect[int(ids)]
        cursor.execute("DELETE FROM performance_related WHERE id=%s"%id_concect[int(ids)])   
  
        cursor.close()
        conn.commit()
        conn.close()


    #删除数据
    ids = request.form.get('ids[]','')

    if ids != "":
        reset_delete(ids)


    return render_template("employee/performance-related-May.html")


@main.route('/employee/performance_related_May/return_json',methods = ['GET','POST'])
@login_required
def performance_related_May_return_json():

    username = current_user.username
    if username == "liangzhixuan":
        username = '梁智轩'
    elif username == "mark":
        username = '梁嘉惠'
    elif username == "jerry":
        username = '黄德欣'
    elif username == "tommy":
        username = '梁嘉和'
    elif username == "yangmujiao":
        username = '杨木娇'
    elif username == "lixiurong":
        username = '李秀荣'
    elif username == "oujie":
        username = '欧捷'
    elif username == "zhuxiaoping":
        username = '朱晓平'

    #连接数据库
    cursor = getCon().cursor()

    cursor.execute("SELECT * from performance_related where month='05' and name='%s' "%username)
    data = cursor.fetchall()

    cursor.close()
    getCon().close() 

    jsonData = []

    for n,row  in enumerate(data):
        #print data[0]
        ##print row[1]
        result = {}
        result['id'] = n + 1
        result['date'] = row[1].strftime('%Y-%m-%d')
        result['name'] = row[2]
        result['place'] = row[3]
        result['content'] = row[4]
        result['complete'] = row[5]
        result['integration'] = row[6]
        result['year'] = row[7]
        result['month'] = row[8]
        result['remarks'] = row[9]
    
        jsonData.append(result)

    return json.dumps(jsonData)

#六月
@main.route('/employee/performance_related_Jun',methods = ['GET','POST'])
@login_required
def performance_related_Jun():

    username = current_user.username
    if username == "liangzhixuan":
        username = '梁智轩'
    elif username == "mark":
        username = '梁嘉惠'
    elif username == "jerry":
        username = '黄德欣'
    elif username == "tommy":
        username = '梁嘉和'
    elif username == "yangmujiao":
        username = '杨木娇'
    elif username == "lixiurong":
        username = '李秀荣'
    elif username == "oujie":
        username = '欧捷'
    elif username == "zhuxiaoping":
        username = '朱晓平'

    id = request.form.get('row[id]', '')
    date = request.form.get('row[date]', '')
    name= request.form.get('row[name]', '')
    place= request.form.get('row[place]', '')
    content= request.form.get('row[content]', '')
    complete= request.form.get('row[complete]', '')  
    integration= request.form.get('row[integration]', '') 
    remarks= request.form.get('row[remarks]', '')  
    year= request.form.get('row[year]', '') 
    month= request.form.get('row[month]', '') 
 
    """建立表格ID与数据表ID的关联"""  

    #连接数据库
    cursor = getCon().cursor() 
    cursor.execute("SELECT * from performance_related where month='06' and name='%s' "%username)
    data = cursor.fetchall()
       
    if len(data) !=0:
	
        input_get=[]
        output_get=[]

        get_data=[]
        for i,w in enumerate(data):
            get_data.append(w[0])
      
        id_from_table = []
        id_from_mysql = []
	for i,datas in enumerate(get_data):
            id_from_table.append(i+1)
            id_from_mysql.append(datas)

        id_concect = dict(zip(id_from_table,id_from_mysql))
        print id_concect

    #cursor.close()
    #getCon().close()


    if id !='':
        old_Value = Performance_Related.query.filter_by(id=id_concect[int(id)]).first()
        if  old_Value is not None:
            print "更新数据"
            Performance_Related.query.filter_by(id=id_concect[int(id)]).update({"date":date,"name":name,"place":place,
              "content":content,"complete":complete,"integration":integration,"remarks":remarks,"year":year,"month":month}) 
        db.session.commit()    

    #增加  
    add =request.form.get('add','')
   
    if add == 'add_true':
        add_item = Performance_Related(date=get_time,name=username,place='',content='',complete='',integration='',remarks='',year=get_year,month='06')

        db.session.add(add_item)
        db.session.commit() 


    '''删除记录'''
    def reset_delete(ids):
        #连接数据库
        try:
            '''warning:这里需要设置为环境获取'''
            conn = MySQLdb.connect("localhost","root","uroot012","erp_development",charset='utf8')
            cursor = conn.cursor()
        except:
            print 'MySQL connect fail...'
            import traceback
            traceback.print_exc()
            # 发生错误时会滚
            conn.rollback()

        print '删除记录',id_concect[int(ids)]
        cursor.execute("DELETE FROM performance_related WHERE id=%s"%id_concect[int(ids)])   
  
        cursor.close()
        conn.commit()
        conn.close()


    #删除数据
    ids = request.form.get('ids[]','')

    if ids != "":
        reset_delete(ids)


    return render_template("employee/performance-related-Jun.html")


@main.route('/employee/performance_related_Jun/return_json',methods = ['GET','POST'])
@login_required
def performance_related_Jun_return_json():

    username = current_user.username
    if username == "liangzhixuan":
        username = '梁智轩'
    elif username == "mark":
        username = '梁嘉惠'
    elif username == "jerry":
        username = '黄德欣'
    elif username == "tommy":
        username = '梁嘉和'
    elif username == "yangmujiao":
        username = '杨木娇'
    elif username == "lixiurong":
        username = '李秀荣'
    elif username == "oujie":
        username = '欧捷'
    elif username == "zhuxiaoping":
        username = '朱晓平'

    #连接数据库
    cursor = getCon().cursor()

    cursor.execute("SELECT * from performance_related where month='06' and name='%s' "%username)
    data = cursor.fetchall()

    cursor.close()
    getCon().close() 

    jsonData = []

    for n,row  in enumerate(data):
        #print data[0]
        ##print row[1]
        result = {}
        result['id'] = n + 1
        result['date'] = row[1].strftime('%Y-%m-%d')
        result['name'] = row[2]
        result['place'] = row[3]
        result['content'] = row[4]
        result['complete'] = row[5]
        result['integration'] = row[6]
        result['year'] = row[7]
        result['month'] = row[8]
        result['remarks'] = row[9]
    
        jsonData.append(result)

    return json.dumps(jsonData)


#七月
@main.route('/employee/performance_related_Jul',methods = ['GET','POST'])
@login_required
def performance_related_Jul():

    username = current_user.username
    if username == "liangzhixuan":
        username = '梁智轩'
    elif username == "mark":
        username = '梁嘉惠'
    elif username == "jerry":
        username = '黄德欣'
    elif username == "tommy":
        username = '梁嘉和'
    elif username == "yangmujiao":
        username = '杨木娇'
    elif username == "lixiurong":
        username = '李秀荣'
    elif username == "oujie":
        username = '欧捷'
    elif username == "zhuxiaoping":
        username = '朱晓平'

    id = request.form.get('row[id]', '')
    date = request.form.get('row[date]', '')
    name= request.form.get('row[name]', '')
    place= request.form.get('row[place]', '')
    content= request.form.get('row[content]', '')
    complete= request.form.get('row[complete]', '')  
    integration= request.form.get('row[integration]', '') 
    remarks= request.form.get('row[remarks]', '')  
    year= request.form.get('row[year]', '') 
    month= request.form.get('row[month]', '') 
 
    """建立表格ID与数据表ID的关联"""  

    #连接数据库
    cursor = getCon().cursor() 
    cursor.execute("SELECT * from performance_related where month='07' and name='%s' "%username)
    data = cursor.fetchall()
       
    if len(data) !=0:
	
        input_get=[]
        output_get=[]

        get_data=[]
        for i,w in enumerate(data):
            get_data.append(w[0])
      
        id_from_table = []
        id_from_mysql = []
	for i,datas in enumerate(get_data):
            id_from_table.append(i+1)
            id_from_mysql.append(datas)

        id_concect = dict(zip(id_from_table,id_from_mysql))
        print id_concect

    #cursor.close()
    #getCon().close()


    if id !='':
        old_Value = Performance_Related.query.filter_by(id=id_concect[int(id)]).first()
        if  old_Value is not None:
            print "更新数据"
            Performance_Related.query.filter_by(id=id_concect[int(id)]).update({"date":date,"name":name,"place":place,
               "content":content,"complete":complete,"integration":integration,"remarks":remarks,"year":year,"month":month}) 
        db.session.commit()    

    #增加  
    add =request.form.get('add','')
   
    if add == 'add_true':
        add_item = Performance_Related(date=get_time,name=username,place='',content='',complete='',integration='',remarks='',year=get_year,month='07')

        db.session.add(add_item)
        db.session.commit() 


    '''删除记录'''
    def reset_delete(ids):
        #连接数据库
        try:
            '''warning:这里需要设置为环境获取'''
            conn = MySQLdb.connect("localhost","root","uroot012","erp_development",charset='utf8')
            cursor = conn.cursor()
        except:
            print 'MySQL connect fail...'
            import traceback
            traceback.print_exc()
            # 发生错误时会滚
            conn.rollback()

        print '删除记录',id_concect[int(ids)]
        cursor.execute("DELETE FROM performance_related WHERE id=%s"%id_concect[int(ids)])   
  
        cursor.close()
        conn.commit()
        conn.close()


    #删除数据
    ids = request.form.get('ids[]','')

    if ids != "":
        reset_delete(ids)


    return render_template("employee/performance-related-Jul.html")



@main.route('/employee/performance_related_Jul/return_json',methods = ['GET','POST'])
@login_required
def performance_related_Jul_return_json():

    username = current_user.username
    if username == "liangzhixuan":
        username = '梁智轩'
    elif username == "mark":
        username = '梁嘉惠'
    elif username == "jerry":
        username = '黄德欣'
    elif username == "tommy":
        username = '梁嘉和'
    elif username == "yangmujiao":
        username = '杨木娇'
    elif username == "lixiurong":
        username = '李秀荣'
    elif username == "oujie":
        username = '欧捷'
    elif username == "zhuxiaoping":
        username = '朱晓平'

    #连接数据库
    cursor = getCon().cursor()

    cursor.execute("SELECT * from performance_related where month='07' and name='%s' "%username)
    data = cursor.fetchall()

    cursor.close()
    getCon().close() 

    jsonData = []

    for n,row  in enumerate(data):
        #print data[0]
        ##print row[1]
        result = {}
        result['id'] = n + 1
        result['date'] = row[1].strftime('%Y-%m-%d')
        result['name'] = row[2]
        result['place'] = row[3]
        result['content'] = row[4]
        result['complete'] = row[5]
        result['integration'] = row[6]
        result['year'] = row[7]
        result['month'] = row[8]
        result['remarks'] = row[9]
    
        jsonData.append(result)

    return json.dumps(jsonData)

#八月
@main.route('/employee/performance_related_Aug',methods = ['GET','POST'])
@login_required
def performance_related_Aug():

    username = current_user.username
    if username == "liangzhixuan":
        username = '梁智轩'
    elif username == "mark":
        username = '梁嘉惠'
    elif username == "jerry":
        username = '黄德欣'
    elif username == "tommy":
        username = '梁嘉和'
    elif username == "yangmujiao":
        username = '杨木娇'
    elif username == "lixiurong":
        username = '李秀荣'
    elif username == "oujie":
        username = '欧捷'
    elif username == "zhuxiaoping":
        username = '朱晓平'

    id = request.form.get('row[id]', '')
    date = request.form.get('row[date]', '')
    name= request.form.get('row[name]', '')
    place= request.form.get('row[place]', '')
    content= request.form.get('row[content]', '')
    complete= request.form.get('row[complete]', '')  
    integration= request.form.get('row[integration]', '') 
    remarks= request.form.get('row[remarks]', '')  
    year= request.form.get('row[year]', '') 
    month= request.form.get('row[month]', '') 
 
    """建立表格ID与数据表ID的关联"""  

    #连接数据库
    cursor = getCon().cursor() 
    cursor.execute("SELECT * from performance_related where month='08' and name='%s' "%username)
    data = cursor.fetchall()
       
    if len(data) !=0:
	
        input_get=[]
        output_get=[]

        get_data=[]
        for i,w in enumerate(data):
            get_data.append(w[0])
      
        id_from_table = []
        id_from_mysql = []
	for i,datas in enumerate(get_data):
            id_from_table.append(i+1)
            id_from_mysql.append(datas)

        id_concect = dict(zip(id_from_table,id_from_mysql))
        print id_concect

    #cursor.close()
    #getCon().close()


    if id !='':
        old_Value = Performance_Related.query.filter_by(id=id_concect[int(id)]).first()
        if  old_Value is not None:
            print "更新数据"
            Performance_Related.query.filter_by(id=id_concect[int(id)]).update({"date":date,"name":name,"place":place,
              "content":content,"complete":complete,"integration":integration,"remarks":remarks,"year":year,"month":month}) 
        db.session.commit()    

    #增加  
    add =request.form.get('add','')
   
    if add == 'add_true':
        add_item = Performance_Related(date=get_time,name=username,place='',content='',complete='',integration='',remarks='',year=get_year,month='08')

        db.session.add(add_item)
        db.session.commit() 


    '''删除记录'''
    def reset_delete(ids):
        #连接数据库
        try:
            '''warning:这里需要设置为环境获取'''
            conn = MySQLdb.connect("localhost","root","uroot012","erp_development",charset='utf8')
            cursor = conn.cursor()
        except:
            print 'MySQL connect fail...'
            import traceback
            traceback.print_exc()
            # 发生错误时会滚
            conn.rollback()

        print '删除记录',id_concect[int(ids)]
        cursor.execute("DELETE FROM performance_related WHERE id=%s"%id_concect[int(ids)])   
  
        cursor.close()
        conn.commit()
        conn.close()


    #删除数据
    ids = request.form.get('ids[]','')

    if ids != "":
        reset_delete(ids)


    return render_template("employee/performance-related-Aug.html")



@main.route('/employee/performance_related_Aug/return_json',methods = ['GET','POST'])
@login_required
def performance_related_Aug_return_json():

    username = current_user.username
    if username == "liangzhixuan":
        username = '梁智轩'
    elif username == "mark":
        username = '梁嘉惠'
    elif username == "jerry":
        username = '黄德欣'
    elif username == "tommy":
        username = '梁嘉和'
    elif username == "yangmujiao":
        username = '杨木娇'
    elif username == "lixiurong":
        username = '李秀荣'
    elif username == "oujie":
        username = '欧捷'
    elif username == "zhuxiaoping":
        username = '朱晓平'

    #连接数据库
    cursor = getCon().cursor()

    cursor.execute("SELECT * from performance_related where month='08' and name='%s' "%username)
    data = cursor.fetchall()

    cursor.close()
    getCon().close() 

    jsonData = []

    for n,row  in enumerate(data):
        #print data[0]
        ##print row[1]
        result = {}
        result['id'] = n + 1
        result['date'] = row[1].strftime('%Y-%m-%d')
        result['name'] = row[2]
        result['place'] = row[3]
        result['content'] = row[4]
        result['complete'] = row[5]
        result['integration'] = row[6]
        result['year'] = row[7]
        result['month'] = row[8]
        result['remarks'] = row[9]
    
        jsonData.append(result)

    return json.dumps(jsonData)

#九月
@main.route('/employee/performance_related_Sep',methods = ['GET','POST'])
@login_required
def performance_related_Sep():

    username = current_user.username
    if username == "liangzhixuan":
        username = '梁智轩'
    elif username == "mark":
        username = '梁嘉惠'
    elif username == "jerry":
        username = '黄德欣'
    elif username == "tommy":
        username = '梁嘉和'
    elif username == "yangmujiao":
        username = '杨木娇'
    elif username == "lixiurong":
        username = '李秀荣'
    elif username == "oujie":
        username = '欧捷'
    elif username == "zhuxiaoping":
        username = '朱晓平'

    id = request.form.get('row[id]', '')
    date = request.form.get('row[date]', '')
    name= request.form.get('row[name]', '')
    place= request.form.get('row[place]', '')
    content= request.form.get('row[content]', '')
    complete= request.form.get('row[complete]', '')  
    integration= request.form.get('row[integration]', '') 
    remarks= request.form.get('row[remarks]', '')  
    year= request.form.get('row[year]', '') 
    month= request.form.get('row[month]', '') 
 
    """建立表格ID与数据表ID的关联"""  

    #连接数据库
    cursor = getCon().cursor() 
    cursor.execute("SELECT * from performance_related where month='09' and name='%s' "%username)
    data = cursor.fetchall()
       
    if len(data) !=0:
	
        input_get=[]
        output_get=[]

        get_data=[]
        for i,w in enumerate(data):
            get_data.append(w[0])
      
        id_from_table = []
        id_from_mysql = []
	for i,datas in enumerate(get_data):
            id_from_table.append(i+1)
            id_from_mysql.append(datas)

        id_concect = dict(zip(id_from_table,id_from_mysql))
        print id_concect

    #cursor.close()
    #getCon().close()


    if id !='':
        old_Value = Performance_Related.query.filter_by(id=id_concect[int(id)]).first()
        if  old_Value is not None:
            print "更新数据"
            Performance_Related.query.filter_by(id=id_concect[int(id)]).update({"date":date,"name":name,"place":place,
                "content":content,"complete":complete,"integration":integration,"remarks":remarks,"year":year,"month":month}) 
        db.session.commit()    

    #增加  
    add =request.form.get('add','')
   
    if add == 'add_true':
        add_item = Performance_Related(date=get_time,name=username,place='',content='',complete='',integration='',remarks='',year=get_year,month='09')

        db.session.add(add_item)
        db.session.commit() 


    '''删除记录'''
    def reset_delete(ids):
        #连接数据库
        try:
            '''warning:这里需要设置为环境获取'''
            conn = MySQLdb.connect("localhost","root","uroot012","erp_development",charset='utf8')
            cursor = conn.cursor()
        except:
            print 'MySQL connect fail...'
            import traceback
            traceback.print_exc()
            # 发生错误时会滚
            conn.rollback()

        print '删除记录',id_concect[int(ids)]
        cursor.execute("DELETE FROM performance_related WHERE id=%s"%id_concect[int(ids)])   
  
        cursor.close()
        conn.commit()
        conn.close()


    #删除数据
    ids = request.form.get('ids[]','')

    if ids != "":
        reset_delete(ids)


    return render_template("employee/performance-related-Sep.html")



@main.route('/employee/performance_related_Sep/return_json',methods = ['GET','POST'])
@login_required
def performance_related_Sep_return_json():

    username = current_user.username
    if username == "liangzhixuan":
        username = '梁智轩'
    elif username == "mark":
        username = '梁嘉惠'
    elif username == "jerry":
        username = '黄德欣'
    elif username == "tommy":
        username = '梁嘉和'
    elif username == "yangmujiao":
        username = '杨木娇'
    elif username == "lixiurong":
        username = '李秀荣'
    elif username == "oujie":
        username = '欧捷'
    elif username == "zhuxiaoping":
        username = '朱晓平'

    #连接数据库
    cursor = getCon().cursor()

    cursor.execute("SELECT * from performance_related where month='09' and name='%s' "%username)
    data = cursor.fetchall()

    cursor.close()
    getCon().close() 

    jsonData = []

    for n,row  in enumerate(data):
        #print data[0]
        ##print row[1]
        result = {}
        result['id'] = n + 1
        result['date'] = row[1].strftime('%Y-%m-%d')
        result['name'] = row[2]
        result['place'] = row[3]
        result['content'] = row[4]
        result['complete'] = row[5]
        result['integration'] = row[6]
        result['year'] = row[7]
        result['month'] = row[8]
        result['remarks'] = row[9]
    
        jsonData.append(result)

    return json.dumps(jsonData)

#十月
@main.route('/employee/performance_related_Oct',methods = ['GET','POST'])
@login_required
def performance_related_Oct():

    username = current_user.username
    if username == "liangzhixuan":
        username = '梁智轩'
    elif username == "mark":
        username = '梁嘉惠'
    elif username == "jerry":
        username = '黄德欣'
    elif username == "tommy":
        username = '梁嘉和'
    elif username == "yangmujiao":
        username = '杨木娇'
    elif username == "lixiurong":
        username = '李秀荣'
    elif username == "oujie":
        username = '欧捷'
    elif username == "zhuxiaoping":
        username = '朱晓平'

    id = request.form.get('row[id]', '')
    date = request.form.get('row[date]', '')
    name= request.form.get('row[name]', '')
    place= request.form.get('row[place]', '')
    content= request.form.get('row[content]', '')
    complete= request.form.get('row[complete]', '')  
    integration= request.form.get('row[integration]', '') 
    remarks= request.form.get('row[remarks]', '')  
    year= request.form.get('row[year]', '') 
    month= request.form.get('row[month]', '') 
 
    """建立表格ID与数据表ID的关联"""  

    #连接数据库
    cursor = getCon().cursor() 
    cursor.execute("SELECT * from performance_related where month='10' and name='%s' "%username)
    data = cursor.fetchall()
       
    if len(data) !=0:
	
        input_get=[]
        output_get=[]

        get_data=[]
        for i,w in enumerate(data):
            get_data.append(w[0])
      
        id_from_table = []
        id_from_mysql = []
	for i,datas in enumerate(get_data):
            id_from_table.append(i+1)
            id_from_mysql.append(datas)

        id_concect = dict(zip(id_from_table,id_from_mysql))
        print id_concect

    #cursor.close()
    #getCon().close()


    if id !='':
        old_Value = Performance_Related.query.filter_by(id=id_concect[int(id)]).first()
        if  old_Value is not None:
            print "更新数据"
            Performance_Related.query.filter_by(id=id_concect[int(id)]).update({"date":date,"name":name,"place":place, 
             "content":content,"complete":complete,"integration":integration,"remarks":remarks,"year":year,"month":month}) 
        db.session.commit()    

    #增加  
    add =request.form.get('add','')
   
    if add == 'add_true':
        add_item = Performance_Related(date=get_time,name=username,place='',content='',complete='',integration='',remarks='',year=get_year,month='10')

        db.session.add(add_item)
        db.session.commit() 


    '''删除记录'''
    def reset_delete(ids):
        #连接数据库
        try:
            '''warning:这里需要设置为环境获取'''
            conn = MySQLdb.connect("localhost","root","uroot012","erp_development",charset='utf8')
            cursor = conn.cursor()
        except:
            print 'MySQL connect fail...'
            import traceback
            traceback.print_exc()
            # 发生错误时会滚
            conn.rollback()

        print '删除记录',id_concect[int(ids)]
        cursor.execute("DELETE FROM performance_related WHERE id=%s"%id_concect[int(ids)])   
  
        cursor.close()
        conn.commit()
        conn.close()


    #删除数据
    ids = request.form.get('ids[]','')

    if ids != "":
        reset_delete(ids)


    return render_template("employee/performance-related-Oct.html")



@main.route('/employee/performance_related_Oct/return_json',methods = ['GET','POST'])
@login_required
def performance_related_Oct_return_json():

    username = current_user.username
    if username == "liangzhixuan":
        username = '梁智轩'
    elif username == "mark":
        username = '梁嘉惠'
    elif username == "jerry":
        username = '黄德欣'
    elif username == "tommy":
        username = '梁嘉和'
    elif username == "yangmujiao":
        username = '杨木娇'
    elif username == "lixiurong":
        username = '李秀荣'
    elif username == "oujie":
        username = '欧捷'
    elif username == "zhuxiaoping":
        username = '朱晓平'

    #连接数据库
    cursor = getCon().cursor()

    cursor.execute("SELECT * from performance_related where month='10' and name='%s' "%username)
    data = cursor.fetchall()

    cursor.close()
    getCon().close() 

    jsonData = []

    for n,row  in enumerate(data):
        #print data[0]
        ##print row[1]
        result = {}
        result['id'] = n + 1
        result['date'] = row[1].strftime('%Y-%m-%d')
        result['name'] = row[2]
        result['place'] = row[3]
        result['content'] = row[4]
        result['complete'] = row[5]
        result['integration'] = row[6]
        result['year'] = row[7]
        result['month'] = row[8]
        result['remarks'] = row[9]
    
        jsonData.append(result)

    return json.dumps(jsonData)

#十一月
@main.route('/employee/performance_related_Nov',methods = ['GET','POST'])
@login_required
def performance_related_Nov():

    username = current_user.username
    if username == "liangzhixuan":
        username = '梁智轩'
    elif username == "mark":
        username = '梁嘉惠'
    elif username == "jerry":
        username = '黄德欣'
    elif username == "tommy":
        username = '梁嘉和'
    elif username == "yangmujiao":
        username = '杨木娇'
    elif username == "lixiurong":
        username = '李秀荣'
    elif username == "oujie":
        username = '欧捷'
    elif username == "zhuxiaoping":
        username = '朱晓平'

    id = request.form.get('row[id]', '')
    date = request.form.get('row[date]', '')
    name= request.form.get('row[name]', '')
    place= request.form.get('row[place]', '')
    content= request.form.get('row[content]', '')
    complete= request.form.get('row[complete]', '')  
    integration= request.form.get('row[integration]', '') 
    remarks= request.form.get('row[remarks]', '')  
    year= request.form.get('row[year]', '') 
    month= request.form.get('row[month]', '') 
 
    """建立表格ID与数据表ID的关联"""  

    #连接数据库
    cursor = getCon().cursor() 
    cursor.execute("SELECT * from performance_related where month='11' and name='%s' "%username)
    data = cursor.fetchall()
       
    if len(data) !=0:
	
        input_get=[]
        output_get=[]

        get_data=[]
        for i,w in enumerate(data):
            get_data.append(w[0])
      
        id_from_table = []
        id_from_mysql = []
	for i,datas in enumerate(get_data):
            id_from_table.append(i+1)
            id_from_mysql.append(datas)

        id_concect = dict(zip(id_from_table,id_from_mysql))
        print id_concect

    #cursor.close()
    #getCon().close()


    if id !='':
        old_Value = Performance_Related.query.filter_by(id=id_concect[int(id)]).first()
        if  old_Value is not None:
            print "更新数据"
            Performance_Related.query.filter_by(id=id_concect[int(id)]).update({"date":date,"name":name,"place":place,
              "content":content,"complete":complete,"integration":integration,"remarks":remarks,"year":year,"month":month}) 
        db.session.commit()    

    #增加  
    add =request.form.get('add','')
   
    if add == 'add_true':
        add_item = Performance_Related(date=get_time,name=username,place='',content='',complete='',integration='',remarks='',year=get_year,month='11')

        db.session.add(add_item)
        db.session.commit() 


    '''删除记录'''
    def reset_delete(ids):
        #连接数据库
        try:
            '''warning:这里需要设置为环境获取'''
            conn = MySQLdb.connect("localhost","root","uroot012","erp_development",charset='utf8')
            cursor = conn.cursor()
        except:
            print 'MySQL connect fail...'
            import traceback
            traceback.print_exc()
            # 发生错误时会滚
            conn.rollback()

        print '删除记录',id_concect[int(ids)]
        cursor.execute("DELETE FROM performance_related WHERE id=%s"%id_concect[int(ids)])   
  
        cursor.close()
        conn.commit()
        conn.close()


    #删除数据
    ids = request.form.get('ids[]','')

    if ids != "":
        reset_delete(ids)


    return render_template("employee/performance-related-Nov.html")



@main.route('/employee/performance_related_Nov/return_json',methods = ['GET','POST'])
@login_required
def performance_related_Nov_return_json():

    username = current_user.username
    if username == "liangzhixuan":
        username = '梁智轩'
    elif username == "mark":
        username = '梁嘉惠'
    elif username == "jerry":
        username = '黄德欣'
    elif username == "tommy":
        username = '梁嘉和'
    elif username == "yangmujiao":
        username = '杨木娇'
    elif username == "lixiurong":
        username = '李秀荣'
    elif username == "oujie":
        username = '欧捷'
    elif username == "zhuxiaoping":
        username = '朱晓平'

    #连接数据库
    cursor = getCon().cursor()

    cursor.execute("SELECT * from performance_related where month='11' and name='%s' "%username)
    data = cursor.fetchall()

    cursor.close()
    getCon().close() 

    jsonData = []

    for n,row  in enumerate(data):
        #print data[0]
        ##print row[1]
        result = {}
        result['id'] = n + 1
        result['date'] = row[1].strftime('%Y-%m-%d')
        result['name'] = row[2]
        result['place'] = row[3]
        result['content'] = row[4]
        result['complete'] = row[5]
        result['integration'] = row[6]
        result['year'] = row[7]
        result['month'] = row[8]
        result['remarks'] = row[9]
    
        jsonData.append(result)

    return json.dumps(jsonData)

#十二月
@main.route('/employee/performance_related_Dec',methods = ['GET','POST'])
@login_required
def performance_related_Dec():

    username = current_user.username
    if username == "liangzhixuan":
        username = '梁智轩'
    elif username == "mark":
        username = '梁嘉惠'
    elif username == "jerry":
        username = '黄德欣'
    elif username == "tommy":
        username = '梁嘉和'
    elif username == "yangmujiao":
        username = '杨木娇'
    elif username == "lixiurong":
        username = '李秀荣'
    elif username == "oujie":
        username = '欧捷'
    elif username == "zhuxiaoping":
        username = '朱晓平'

    id = request.form.get('row[id]', '')
    date = request.form.get('row[date]', '')
    name= request.form.get('row[name]', '')
    place= request.form.get('row[place]', '')
    content= request.form.get('row[content]', '')
    complete= request.form.get('row[complete]', '')  
    integration= request.form.get('row[integration]', '') 
    remarks= request.form.get('row[remarks]', '')  
    year= request.form.get('row[year]', '') 
    month= request.form.get('row[month]', '') 
 
    """建立表格ID与数据表ID的关联"""  

    #连接数据库
    cursor = getCon().cursor() 
    cursor.execute("SELECT * from performance_related where month='12' and name='%s' "%username)
    data = cursor.fetchall()
       
    if len(data) !=0:
	
        input_get=[]
        output_get=[]

        get_data=[]
        for i,w in enumerate(data):
            get_data.append(w[0])
      
        id_from_table = []
        id_from_mysql = []
	for i,datas in enumerate(get_data):
            id_from_table.append(i+1)
            id_from_mysql.append(datas)

        id_concect = dict(zip(id_from_table,id_from_mysql))
        print id_concect

    #cursor.close()
    #getCon().close()


    if id !='':
        old_Value = Performance_Related.query.filter_by(id=id_concect[int(id)]).first()
        if  old_Value is not None:
            print "更新数据"
            Performance_Related.query.filter_by(id=id_concect[int(id)]).update({"date":date,"name":name,"place":place,
              "content":content,"complete":complete,"integration":integration,"remarks":remarks,"year":year,"month":month}) 
        db.session.commit()    

    #增加  
    add =request.form.get('add','')
   
    if add == 'add_true':
        add_item = Performance_Related(date=get_time,name=username,place='',content='',complete='',integration='',remarks='',year=get_year,month='12')

        db.session.add(add_item)
        db.session.commit() 


    '''删除记录'''
    def reset_delete(ids):
        #连接数据库
        try:
            '''warning:这里需要设置为环境获取'''
            conn = MySQLdb.connect("localhost","root","uroot012","erp_development",charset='utf8')
            cursor = conn.cursor()
        except:
            print 'MySQL connect fail...'
            import traceback
            traceback.print_exc()
            # 发生错误时会滚
            conn.rollback()

        print '删除记录',id_concect[int(ids)]
        cursor.execute("DELETE FROM performance_related WHERE id=%s"%id_concect[int(ids)])   
  
        cursor.close()
        conn.commit()
        conn.close()


    #删除数据
    ids = request.form.get('ids[]','')

    if ids != "":
        reset_delete(ids)


    return render_template("employee/performance-related-Dec.html")



@main.route('/employee/performance_related_Dec/return_json',methods = ['GET','POST'])
@login_required
def performance_related_Dec_return_json():

    username = current_user.username
    if username == "liangzhixuan":
        username = '梁智轩'
    elif username == "mark":
        username = '梁嘉惠'
    elif username == "jerry":
        username = '黄德欣'
    elif username == "tommy":
        username = '梁嘉和'
    elif username == "yangmujiao":
        username = '杨木娇'
    elif username == "lixiurong":
        username = '李秀荣'
    elif username == "oujie":
        username = '欧捷'
    elif username == "zhuxiaoping":
        username = '朱晓平'

    #连接数据库
    cursor = getCon().cursor()

    cursor.execute("SELECT * from performance_related where month='12' and name='%s' "%username)
    data = cursor.fetchall()

    cursor.close()
    getCon().close() 

    jsonData = []

    for n,row  in enumerate(data):
        #print data[0]
        ##print row[1]
        result = {}
        result['id'] = n + 1
        result['date'] = row[1].strftime('%Y-%m-%d')
        result['name'] = row[2]
        result['place'] = row[3]
        result['content'] = row[4]
        result['complete'] = row[5]
        result['integration'] = row[6]
        result['year'] = row[7]
        result['month'] = row[8]
        result['remarks'] = row[9]
    
        jsonData.append(result)

    return json.dumps(jsonData)




