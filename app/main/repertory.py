# -*- coding:utf-8 -*-
__author__ = 'xuan'

from flask import render_template,request,current_app,session,redirect,url_for
from  . import  main
from flask.ext.login import login_required,current_user,login_user,logout_user
import json,MySQLdb,sys
from ..models import  Fittings,Semi_finished,End_product,Purchase_List,Goods_price,Fittings_Inputs

from  manage import  db  #不添加这个会不能更新数据库
import  time
from decimal import Decimal

from  configobj import  ConfigObj

reload(sys)
sys.setdefaultencoding('utf8')


@main.route('/repertory',methods = ['GET','POST'])
@login_required
def repertory():

    return render_template('repertory/repertory.html')



@main.route('/repertory/goods_price',methods = ['GET','POST'])
@login_required
def goods_price():

    id = request.form.get('row[id]', '')
    oldValue = request.form.get('oldValue', '')
    name = request.form.get('row[name]', '')
    price = request.form.get('row[price]', '')
    price_oem = request.form.get('row[price_oem]', '')
    price_own = request.form.get('row[price_own]', '')    
    remark = request.form.get('row[remark]', '')
    
    #建立id联系
    try:
        '''warning:这里需要设置为环境获取'''
        database = MySQLdb.connect("localhost","root","uroot012","erp_development",charset='utf8')
        cursor = database.cursor()
    except:
        print 'MySQL connect fail...'

    cursor.execute("SELECT id from goods_price")
    data = cursor.fetchall()
     
   
    if len(data) !=0:
	
        input_get=[]
        output_get=[]

        get_data=[]
        for i,w in enumerate(data):
            get_data.append(w[0])

        #print 'getdata',get_data
        
        id_from_table = []
        id_from_mysql = []
	for i,datas in enumerate(get_data):
        #print 'i',i
	    #print 'datas',datas
            id_from_table.append(i+1)
            id_from_mysql.append(datas)   
 
    '''建立id关联'''
    id_concect = dict(zip(id_from_table,id_from_mysql))
    print id_concect 

   
    if oldValue and id is not None and name != '':
        print 'name修改'
        old_Value = Goods_price.query.filter_by(name=oldValue,id=id_concect[int(id)]).first()
        if old_Value is not None:
            Goods_price.query.filter_by(name=oldValue,id=id_concect[int(id)]).update({"name":name})
            db.session.commit()

    if price and id is not None:
        print 'price修改'
        old_Value = Goods_price.query.filter_by(id=id_concect[int(id)]).first()
        if old_Value is not None:
            Goods_price.query.filter_by(id=id_concect[int(id)]).update({"price":price})
            db.session.commit()

    if price_oem and id is not None:
        print 'price_oem修改'
        old_Value = Goods_price.query.filter_by(id=id_concect[int(id)]).first()
        if old_Value is not None:
            Goods_price.query.filter_by(id=id_concect[int(id)]).update({"price_oem":price_oem})
            db.session.commit()

    if price_own and id is not None:
        print 'price_own修改'
        old_Value = Goods_price.query.filter_by(id=id_concect[int(id)]).first()
        if old_Value is not None:
            Goods_price.query.filter_by(id=id_concect[int(id)]).update({"price_own":price_own})
            db.session.commit()


    if remark and id is not None:
        print 'remark修改'
        old_Value = Goods_price.query.filter_by(id=id_concect[int(id)]).first()
        if old_Value is not None:
            Goods_price.query.filter_by(id=id_concect[int(id)]).update({"remark":remark})
            db.session.commit()

    '''获取商品的实时库存量'''
    #AX700
    if Semi_finished.query.filter_by(name='AX700 瘦客户机 (J192G8G)').first() is not None: 
        num_AX700 = Semi_finished.query.filter_by(name='AX700 瘦客户机 (J192G8G)').first().nums
    else:
        num_AX700 = 0
    
    #AX730
    if Semi_finished.query.filter_by(name='AX730 瘦客户机(E192G8G)').first() is not None: 
        num_AX730 = Semi_finished.query.filter_by(name='AX730 瘦客户机(E192G8G)').first().nums
    else:
        num_AX730 = 0

    #AX800
    if Semi_finished.query.filter_by(name='AX800 迷你电脑').first() is not None: 
        num_AX800 = Semi_finished.query.filter_by(name='AX800 迷你电脑').first().nums
    else:
        num_AX800 = 0

    #C100
    if End_product.query.filter_by(name='C100 云终端').first() is not None:
        num_C100 = End_product.query.filter_by(name='C100 云终端').first().nums
        print "!!!!!!!!!!!",num_C100
    else:
        num_C100 = 0

    #E300
    if End_product.query.filter_by(name='E300 云终端').first() is not None:
        num_E300 = End_product.query.filter_by(name='E300 云终端').first().nums
    else:
        num_E300 = 0

    #更新实时库存量
    Goods_price.query.filter_by(name='AX700 瘦客户机 (J192G8G)').update({"nums":num_AX700})
    Goods_price.query.filter_by(name='C100 云终端').update({"nums":num_C100})
    Goods_price.query.filter_by(name='AX730 瘦客户机(E192G8G)').update({"nums":num_AX730})
    Goods_price.query.filter_by(name='AX800 迷你电脑').update({"nums":num_AX800})
    Goods_price.query.filter_by(name='E300 云终端').update({"nums":num_E300})

    db.session.commit()
    

    def reset_delete(ids):
        print "删除数据"
        app = current_app._get_current_object()
        try:
            
            database = MySQLdb.connect("localhost","root","uroot012","erp_development",charset='utf8')
            cursor = database.cursor()
        except:
            print 'MySQL connect fail...'

        cursor.execute("DELETE FROM goods_price WHERE id=%s"%id_concect[int(ids)])

        #cursor.execute("ALTER TABLE fittings DROP id")
        #cursor.execute("ALTER TABLE fittings ADD id INT( 8 ) NOT NULL FIRST")
        #cursor.execute("ALTER TABLE fittings MODIFY COLUMN id INT( 8 ) NOT NULL AUTO_INCREMENT,ADD PRIMARY KEY(id)")

        cursor.close()
        database.commit()
        database.close()
    

    #删除数据
    ids = request.form.get('ids[]','')
    remove_name = request.form.get('remove_name[]','')

    if ids and remove_name != " ":  
        reset_delete(ids)

    add =request.form.get('add','')
    # id = request.form.get('ids','')

    if add == 'add_true':
        add_item = Goods_price(name='商品名称',price='0.00',price_oem='0.00',price_own='0.00',nums=0,remark='-')
        db.session.add(add_item)
        db.session.commit()
      

    return render_template('repertory/goods_price.html')

@main.route('/repertory/goods_price/return_json',methods = ['GET','POST'])
@login_required
def goods_price_return_json():

        try:
            '''warning:这里需要设置为环境获取'''
            db = MySQLdb.connect("localhost","root","uroot012","erp_development",charset='utf8')
            cursor = db.cursor()
        except:
            print 'MySQL connect fail...'
        cursor.execute("SELECT * from goods_price")
        data = cursor.fetchall()
        cursor.close()
        db.close()
        jsonData = []

        for n,row  in enumerate(data):
            ##print data[0]
            ##print row[1]
            result = {}
            result['id'] = n+1
            result['name'] = row[1]
            result['price'] = row[2]
            result['remark'] = row[3]
            result['nums'] = row[4]
            result['price_oem'] = row[5]
            result['price_own'] = row[6]
           

            jsonData.append(result)

        return json.dumps(jsonData)






@main.route('/repertory/purchase_list',methods = ['GET','POST'])
@login_required
def purchase_list():

    #采购提醒 X86
    #当各种配件少于一定数量，则添加到提醒数据表中
    fittings_list = ['2GB内存','8GB固态硬盘','外箱']
    
    for name in fittings_list:
        print name
        if Fittings.query.filter_by(name=name).first() is not None:
            nums = Fittings.query.filter_by(name=name).first().nums

            #若配件在提醒数据表中不存在且小于50，添加            
            if nums <= 50 and Purchase_List.query.filter_by(name=name).first() is None:
                add_list = Purchase_List(name=name,num=nums,min_num=50)    
                print '添加fittings-------------------------',nums
                 
                db.session.add(add_list)
                db.session.commit()
            #若配件在提醒数据表中存在且小于50，更新           
            elif nums <= 50 and Purchase_List.query.filter_by(name=name).first() is not None:
                print '存在，更新fittings-------------------------',nums                
                Purchase_List.query.filter_by(name=name).update({'num':nums }) 
                db.session.commit()  
            elif nums > 50 and Purchase_List.query.filter_by(name=name).first() is not None:
                print 'deletefittings'


                delete = Purchase_List.query.filter_by(name=name).first()
                db.session.delete(delete)
                db.session.commit()                  
            else:
                pass
  



    #采购提醒 A9小于500
    #当各种配件少于一定数量，则添加到提醒数据表中
    fittings_500 = ['PCB主板','A9说明书','保修卡','合格证','散热片','A9上壳黑','A9下壳黑',
                   '左右角（L）','左右角（R）','开关PDB板','开关线','A9包装彩盒','包装彩盒（中性）']
    
    for name in fittings_500:
        print name
        if Fittings.query.filter_by(name=name).first() is not None:
            nums = Fittings.query.filter_by(name=name).first().nums

            #若配件在提醒数据表中不存在且小于500，添加            
            if nums <= 500 and Purchase_List.query.filter_by(name=name).first() is None:
                add_list = Purchase_List(name=name,num=nums,min_num=500)    
                print '添加fittings-------------------------',nums
                 
                db.session.add(add_list)
                db.session.commit()
            #若配件在提醒数据表中存在且小于500，更新           
            elif nums <= 500 and Purchase_List.query.filter_by(name=name).first() is not None:
                print '存在，更新fittings-------------------------',nums                
                Purchase_List.query.filter_by(name=name).update({'num':nums }) 
                db.session.commit()  
            elif nums > 500 and Purchase_List.query.filter_by(name=name).first() is not None:
                print 'deletefittings'


                delete = Purchase_List.query.filter_by(name=name).first()
                db.session.delete(delete)
                db.session.commit()                  
            else:
                pass

    #采购提醒 A9小于200
    #当各种配件少于一定数量，则添加到提醒数据表中
    fittings_200 = ['电源5V2A','包装螺丝']
    
    for name in fittings_200:
        print name
        if Fittings.query.filter_by(name=name).first() is not None:
            nums = Fittings.query.filter_by(name=name).first().nums

            #若配件在提醒数据表中不存在且小于200，添加            
            if nums <= 200 and Purchase_List.query.filter_by(name=name).first() is None:
                add_list = Purchase_List(name=name,num=nums,min_num=200)    
                print '添加fittings-------------------------',nums
                 
                db.session.add(add_list)
                db.session.commit()
            #若配件在提醒数据表中存在且小于500，更新           
            elif nums <= 200 and Purchase_List.query.filter_by(name=name).first() is not None:
                print '存在，更新fittings-------------------------',nums                
                Purchase_List.query.filter_by(name=name).update({'num':nums }) 
                db.session.commit()  
            elif nums > 200 and Purchase_List.query.filter_by(name=name).first() is not None:
                print 'deletefittings'


                delete = Purchase_List.query.filter_by(name=name).first()
                db.session.delete(delete)
                db.session.commit()                  
            else:
                pass


    if Semi_finished.query.filter_by(name='AX700 瘦客户机 (J192G8G)').first() is not None:
        num_AX700 =  Semi_finished.query.filter_by(name='AX700 瘦客户机 (J192G8G)').first().nums
        print '++++++++++++++',num_AX700
        #若配件在提醒数据表中不存在且小于50，添加            
        if num_AX700 <= 50 and Purchase_List.query.filter_by(name='AX700 瘦客户机 (J192G8G)').first() is None:
            print '添加AX700 瘦客户机 (J192G8G)-------------------------',num_AX700
            add_AX700 = Purchase_List(name='AX700 瘦客户机 (J192G8G)',num=num_AX700,min_num=50)               
            db.session.add(add_AX700)
            db.session.commit()          
        #若配件在提醒数据表中存在且小于50，更新
        if num_AX700 <= 50 and Purchase_List.query.filter_by(name='AX700 瘦客户机 (J192G8G)').first() is not None:
            print '存在AX700 瘦客户机 (J192G8G)，更新-------------------------',num_AX700                
            Purchase_List.query.filter_by(name='AX700 瘦客户机 (J192G8G)').update({'num':num_AX700 }) 
            db.session.commit() 
        elif num_AX700 > 50 and Purchase_List.query.filter_by(name='AX700 瘦客户机 (J192G8G)').first() is not None:
            print 'delete'


            delete_AX700 = Purchase_List.query.filter_by(name='AX700 瘦客户机 (J192G8G)').first()
            db.session.delete(delete_AX700)
            db.session.commit() 
        else:
            pass

    return render_template('repertory/purchase_list.html')



@main.route('/repertory/purchase_list/return_json',methods = ['GET','POST'])
@login_required
def purchase_list_return_json():

        try:
            '''warning:这里需要设置为环境获取'''
            db = MySQLdb.connect("localhost","root","uroot012","erp_development",charset='utf8')
            cursor = db.cursor()
        except:
            print 'MySQL connect fail...'
        cursor.execute("SELECT * from purchase_list")
        data = cursor.fetchall()
        cursor.close()
        db.close()
        jsonData = []

        for n,row  in enumerate(data):
            ##print data[0]
            ##print row[1]
            result = {}
            result['name'] = row[0]
            result['num'] = row[1]
            result['min_num'] = row[2]

            jsonData.append(result)

        return json.dumps(jsonData)



@main.route('/repertory/fittings',methods = ['GET','POST'])
@login_required
def fittings():
    '''统计配件库存量'''                   

    app = current_app._get_current_object()
    try:
        '''warning:这里需要设置为环境获取'''
        database = MySQLdb.connect("localhost","root","uroot012","erp_development",charset='utf8')
        cursor = database.cursor()
    except:
        print 'MySQL connect fail...'
	database.rollback()

    cursor.execute("SELECT id from fittings")
    fitsId = cursor.fetchall()
    
    #建立id关联

    if len(fitsId) !=0:
	
        input_get=[]
        output_get=[]

        get_data=[]
        for i,w in enumerate(fitsId):
            get_data.append(w[0])

        id_from_table = []
        id_from_mysql = []

        for i,datas in enumerate(get_data):
            id_from_table.append(i+1)
            id_from_mysql.append(datas)
        id_concect = dict(zip(id_from_table,id_from_mysql))
    print 'fittings id关联',id_concect
    
    #更新库存量

    if len(fitsId) !=0:
    
        input_get=[]
        output_get=[]

        get_data=[]
        for i,w in enumerate(fitsId):
            get_data.append(w[0])

        id_from_table = []
        id_from_mysql = []

        for i,datas in enumerate(get_data):
            id_from_table.append(i+1)
            id_from_mysql.append(datas)

            print i+1 ,datas
            cursor.execute("SELECT SUM(nums) from fittings_inputs where belongs=%d"%datas)
            input_data = cursor.fetchone()

            if input_data == (None,):
                input_data = (Decimal(0),)	
            print '获取入库表总和',input_data

            cursor.execute("SELECT SUM(nums) from fittings_outputs  where belongs=%d"%datas)
            output_data = cursor.fetchone()
	    if output_data == (None,):
                output_data = (Decimal(0),)
            print '获取出库表总和',output_data

            input_get.append(list(input_data))
            output_get.append(list(output_data))
        
        stock = []
        if input_get and output_get is not None:
            for i in range(len(input_get)):
                stock_data =input_get[i][0]-output_get[i][0]
                stock.append(stock_data)
	
	print('入库-出库')
	print(stock)



	print(get_data)
	print(len(get_data))
        #这里要提交才能更新值
	try:
            for i,w in enumerate(get_data):
	        print('jjjjjjjjjjjjjjjjjjjj')
	        print(stock[i])
	        print(w)
                cursor.execute("UPDATE fittings SET nums=%s WHERE id=%s"%(stock[i],w))
 	        print('插入成功') 
            database.commit()
	except:
	    print('errorrrr')

    id = request.form.get('row[id]', '')
    nums= request.form.get('row[nums]', '')
    oldValue = request.form.get('oldValue', '')
    name = request.form.get('row[name]', '')
    price= request.form.get('row[price]', '')


    if oldValue and id is not None and name != '':
        print 'name修改'
        old_Value = Fittings.query.filter_by(name=oldValue,id=id_concect[int(id)]).first()
        if old_Value is not None:
            Fittings.query.filter_by(name=oldValue,id=id_concect[int(id)]).update({"name":name})
            db.session.commit()

    if price and id is not None:
        print 'price修改'
        old_Value = Fittings.query.filter_by(id=id_concect[int(id)]).first()
        if old_Value is not None:
            Fittings.query.filter_by(id=id_concect[int(id)]).update({"price":price})
            db.session.commit()


    '''删除记录并删除相关表'''
    def reset_delete(ids):
        app = current_app._get_current_object()

        cursor.execute("DELETE FROM fittings WHERE id=%s"%id_concect[int(ids)])

        cursor.close()
        database.commit()
    
    #删除数据
    ids = request.form.get('ids[]','')
    remove_name = request.form.get('remove_name[]','')

    if ids and remove_name != " ":


        '''不重置id并删除相关表'''
        reset_delete(ids)

    '''增加'''
    add =request.form.get('add','')


    if add == 'add_true':
        add_item = Fittings(name='edit',price='0.00',nums='0')
        db.session.add(add_item)
        db.session.commit()
       	
        db.session.commit()
    
    #判断采购提醒表是否为空，不为空则显示提醒

    cursor.execute("SELECT * FROM  purchase_list")
    data = cursor.fetchall()

    if data == ():
        print '为空'
        tip = "不提示"
    elif  data != ():
        print '不为空',data
        tip = "提示"
    
    cursor.close()
    database.close()

    return render_template('repertory/fittings.html',tip=tip)

@main.route('/repertory/fittings/return_json',methods = ['GET','POST'])
@login_required
def fittings_return_json():
        app = current_app._get_current_object()
        try:
            '''warning:这里需要设置为环境获取'''
            db = MySQLdb.connect("localhost","root","uroot012","erp_development",charset='utf8')
            cursor = db.cursor()
        except:
            print 'MySQL connect fail...'
        cursor.execute("SELECT * from fittings")
        data = cursor.fetchall()
        cursor.close()
        db.close()
        jsonData = []

        for n,row  in enumerate(data):
       
            result = {}
            result['id'] = n+1
            result['name'] = row[1]
            result['price'] = row[2]
            result['nums'] = row[3]


            jsonData.append(result)

        return json.dumps(jsonData)


@main.route('/repertory/fittings_in',methods = ['GET','POST'])
@login_required
def fittings_in():
    if request.method == 'POST':
        dates = request.form.get('row[dates]','')
        id = request.form.get('row[id]','')
        price = request.form.get('row[price]','')
        nums = request.form.get('row[nums]','')
        examine = request.form.get('row[examine]','')
        suppliers = request.form.get('row[suppliers]','')
        sendee = request.form.get('row[sendee]','')
        remarks = request.form.get('row[remarks]','')

        """  建立fittings表格ID与数据表Fittngs ID的关联"""  
        try:
            '''warning:这里需要设置为环境获取'''
            database = MySQLdb.connect("localhost","root","uroot012","erp_development",charset='utf8')
            cursor = database.cursor()
        except:
            print 'MySQL connect fail...'
   
        cursor.execute("SELECT id from fittings")
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

            fittings_id_concect = dict(zip(id_from_table,id_from_mysql))
        print 'fittings_id_concect 关联',fittings_id_concect

        cursor.close()
        database.commit()
        database.close()

        write_in = request.form.get('write_in','')
        print 'write_in',write_in
        if write_in !='':
            """建立fittings_inputs表格 与fittings_inputs 的关联"""  
            try:
                '''warning:这里需要设置为环境获取'''
                database = MySQLdb.connect("localhost","root","uroot012","erp_development",charset='utf8')
                cursor = database.cursor()
            except:
                print 'MySQL connect fail...'
   
            cursor.execute("SELECT id from fittings_inputs where belongs=%s"%fittings_id_concect[int(write_in)])
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

                fittings_inputs_id_concect = dict(zip(id_from_table,id_from_mysql))
            print 'fittings_inputs id(write)关联',fittings_inputs_id_concect

            print '更新数据'
        
            try:
                db = MySQLdb.connect("localhost","root","uroot012","erp_development",charset='utf8')
                cursor = db.cursor()
            except:
                print 'MySQL connect fail...'
            table_name = 'fittings_inputs'
            sql = " UPDATE " + table_name + \
              " SET dates = '%s',nums = %d,price = %s,examine = '%s',suppliers = '%s',sendee = '%s',remarks = '%s' WHERE id = %s "%(dates,int(nums),price,examine,suppliers,sendee,remarks,fittings_inputs_id_concect[int(id)])
            cursor.execute(sql)
            cursor.close()
            db.commit()
            db.close()

        #删除点击的id
        ids = request.form.get('ids[]','')
        del_in = request.form.get('del_in','')

        if  ids and del_in !='':
            """建立fittings_inputs表格 与fittings_inputs 的关联"""  
            try:
                '''warning:这里需要设置为环境获取'''
                database = MySQLdb.connect("localhost","root","uroot012","erp_development",charset='utf8')
                cursor = database.cursor()
            except:
                print 'MySQL connect fail...'
   
            cursor.execute("SELECT id from fittings_inputs where belongs=%s"%fittings_id_concect[int(del_in)])
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


                fittings_inputs_id_concect = dict(zip(id_from_table,id_from_mysql))
            print 'fittings_inputs id(del)关联',fittings_inputs_id_concect

            cursor.close()
            database.commit()
            database.close()

            print '删除数据'

            try:
                '''warning:这里需要设置为环境获取'''
                db = MySQLdb.connect("localhost","root","uroot012","erp_development",charset='utf8')
                cursor = db.cursor()
            except:
                print 'MySQL connect fail...'

            sql_remove = " DELETE FROM  fittings_inputs"  + " WHERE id = %s "%fittings_inputs_id_concect[int(ids)]
            print  sql_remove

            cursor.execute(sql_remove)
  
            # cursor.execute("ALTER TABLE %s DROP id"%del_table_name)
            # cursor.execute("ALTER TABLE %s ADD id INT( 8 ) NOT NULL FIRST"%del_table_name)
            # cursor.execute("ALTER TABLE %s MODIFY COLUMN id INT( 8 ) NOT NULL AUTO_INCREMENT,ADD PRIMARY KEY(id)"%del_table_name)

            cursor.close()
            db.commit()
            db.close()


        add =request.form.get('add','')
        belogns =request.form.get('add_in','')
        get_time = time.strftime('%Y-%m-%d',time.localtime(time.time()))
        
        if add == 'add_true':
            print "添加数据" 
            
            #获取belongs值
            try:
                '''warning:这里需要设置为环境获取'''
                database = MySQLdb.connect("localhost","root","uroot012","erp_development",charset='utf8')
                cursor = database.cursor()
            except:
                print 'MySQL connect fail...'
   
            cursor.execute("SELECT id from fittings")
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
            print 'fittings_belongs id关联',id_concect    

            print 'belongs',id_concect[int(belogns)]

            #添加哪一个数据表 
            #add_in = request.form.get('add_in','')    
            try:
                '''warning:这里需要设置为环境获取'''
                db = MySQLdb.connect("localhost","root","uroot012","erp_development",charset='utf8')
                cursor = db.cursor()
            except:
                print 'MySQL connect fail...'
 
            sql_add= "insert into fittings_inputs"  + "(dates,nums,price,suppliers,examine,sendee,remarks,belongs)" + " values('%s',0,0,'edit','是','edit','',%s) "%(get_time,id_concect[int(belogns)])
            cursor.execute(sql_add)

            cursor.close()
            db.commit()
            db.close()
        return render_template('repertory/fittings_in.html')

    else:
        get_name = request.args.get('name')
        print 'get_name',get_name
        return render_template('repertory/fittings_in.html',get_name=get_name)




@main.route('/repertory/fittings_in/return_json',methods = ['GET','POST'])
@login_required
def fittings_in_return_json():

    #if request.method == 'GET':
    '''后台可直接获取url？参数'''
    query_in = request.args.get('in')
    print "query_in",query_in

    """建立表格ID与数据表ID的关联"""  

    try:
        '''warning:这里需要设置为环境获取'''
        database = MySQLdb.connect("localhost","root","uroot012","erp_development",charset='utf8')
        cursor = database.cursor()
    except:
        print 'MySQL connect fail...'

    cursor.execute("SELECT id from fittings")
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
        #print 'fittings_inputs关联',id_concect

    try:

        db = MySQLdb.connect("localhost","root","uroot012","erp_development",charset='utf8')
        cursor = db.cursor()
    except:
        print 'MySQL connect fail...'

    cursor.execute("SELECT * from fittings_inputs where belongs=%s"%id_concect[int(query_in)])
    data = cursor.fetchall()
    cursor.close()
    db.close()
    jsonData = []

    for n,row  in enumerate(data):
        result = {}
        result['id'] = n + 1
        result['dates'] = row[1]
        result['nums'] = row[2]
        result['price'] = row[3]
        result['suppliers'] = row[4]
        result['examine'] = row[5]
        result['sendee'] = row[6]
        result['remarks'] = row[7]

        jsonData.append(result)
    return json.dumps(jsonData)
    #else:
        #return render_template('repertory/fittings_in.html')


@main.route('/repertory/fittings_out',methods = ['GET','POST'])
@login_required
def fittings_out():
    if request.method == 'POST':
        dates = request.form.get('row[dates]','')
        nums = request.form.get('row[nums]','')
        id = request.form.get('row[id]','')
        purpose = request.form.get('row[purpose]','')
        receiptor = request.form.get('row[receiptor]','')
        remarks = request.form.get('row[remarks]','')

        """  建立fittings表格ID与数据表Fittngs ID的关联"""  
        try:
            '''warning:这里需要设置为环境获取'''
            database = MySQLdb.connect("localhost","root","uroot012","erp_development",charset='utf8')
            cursor = database.cursor()
        except:
            print 'MySQL connect fail...'
   
        cursor.execute("SELECT id from fittings")
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

            fittings_id_concect = dict(zip(id_from_table,id_from_mysql))
        print 'fittings_id_concect 关联',fittings_id_concect

        cursor.close()
        database.commit()
        database.close()

        write_out = request.form.get('write_out','')
        print 'write_out',write_out
        if write_out !='':
            """建立fittings_inputs表格 与fittings_inputs 的关联"""  
            try:
                '''warning:这里需要设置为环境获取'''
                database = MySQLdb.connect("localhost","root","uroot012","erp_development",charset='utf8')
                cursor = database.cursor()
            except:
                print 'MySQL connect fail...'
   
            cursor.execute("SELECT id from fittings_outputs where belongs=%s"%fittings_id_concect[int(write_out)])
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

                fittings_outputs_id_concect = dict(zip(id_from_table,id_from_mysql))
            print 'fittings_outputs id(write)关联',fittings_outputs_id_concect

            print '更新数据'
        
            try:
                db = MySQLdb.connect("localhost","root","uroot012","erp_development",charset='utf8')
                cursor = db.cursor()
            except:
                print 'MySQL connect fail...'
            table_name = 'fittings_outputs'
            sql = " UPDATE " + table_name + \
              " SET dates = '%s',nums = %d,purpose = '%s',receiptor = '%s',remarks = '%s'  WHERE id = %s "%(dates,int(nums),purpose,receiptor,remarks,fittings_outputs_id_concect[int(id)])
            cursor.execute(sql)
            cursor.close()
            db.commit()
            db.close()

        #删除点击的id
        ids = request.form.get('ids[]','')
        del_out = request.form.get('del_out','')

        if  ids and del_out !='':
            """建立fittings_inputs表格 与fittings_inputs 的关联"""  
            try:
                '''warning:这里需要设置为环境获取'''
                database = MySQLdb.connect("localhost","root","uroot012","erp_development",charset='utf8')
                cursor = database.cursor()
            except:
                print 'MySQL connect fail...'
   
            cursor.execute("SELECT id from fittings_outputs where belongs=%s"%fittings_id_concect[int(del_out)])
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


                fittings_outputs_id_concect = dict(zip(id_from_table,id_from_mysql))
            print 'fittings_outputs id(del)关联',fittings_outputs_id_concect

            cursor.close()
            database.commit()
            database.close()

            print '删除数据'

            try:
                '''warning:这里需要设置为环境获取'''
                db = MySQLdb.connect("localhost","root","uroot012","erp_development",charset='utf8')
                cursor = db.cursor()
            except:
                print 'MySQL connect fail...'

            sql_remove = " DELETE FROM  fittings_outputs"  + " WHERE id = %s "%fittings_outputs_id_concect[int(ids)]
            print  sql_remove

            cursor.execute(sql_remove)
  
            # cursor.execute("ALTER TABLE %s DROP id"%del_table_name)
            # cursor.execute("ALTER TABLE %s ADD id INT( 8 ) NOT NULL FIRST"%del_table_name)
            # cursor.execute("ALTER TABLE %s MODIFY COLUMN id INT( 8 ) NOT NULL AUTO_INCREMENT,ADD PRIMARY KEY(id)"%del_table_name)

            cursor.close()
            db.commit()
            db.close()


        add =request.form.get('add','')
        belogns =request.form.get('add_out','')
        get_time = time.strftime('%Y-%m-%d',time.localtime(time.time()))
        
        if add == 'add_true':
            print "添加数据" 
            
            #获取belongs值
            try:
                '''warning:这里需要设置为环境获取'''
                database = MySQLdb.connect("localhost","root","uroot012","erp_development",charset='utf8')
                cursor = database.cursor()
            except:
                print 'MySQL connect fail...'
   
            cursor.execute("SELECT id from fittings")
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
            print 'fittings_belongs id关联',id_concect    

            print 'belongs',id_concect[int(belogns)]

            #添加哪一个数据表 
            #add_in = request.form.get('add_in','')    
            try:
                '''warning:这里需要设置为环境获取'''
                db = MySQLdb.connect("localhost","root","uroot012","erp_development",charset='utf8')
                cursor = db.cursor()
            except:
                print 'MySQL connect fail...'
 
            sql_add= "insert into fittings_outputs"  + "(dates,nums,purpose,receiptor,status,remarks,belongs)" + " values('%s',0,'edit','edit','','',%s) "%(get_time,id_concect[int(belogns)])
            cursor.execute(sql_add)

            cursor.close()
            db.commit()
            db.close()
        return render_template('repertory/fittings_out.html')

    else:
        get_name = request.args.get('name')
        print 'get_name',get_name
        return render_template('repertory/fittings_out.html',get_name=get_name)

@main.route('/repertory/fittings_out/return_json',methods = ['GET','POST'])
@login_required
def fittings_out_return_json():

    '''后台可直接获取url？参数'''
    query_out = request.args.get('out')
    print "query_out",query_out

    """建立表格ID与数据表ID的关联"""  

    try:
        '''warning:这里需要设置为环境获取'''
        database = MySQLdb.connect("localhost","root","uroot012","erp_development",charset='utf8')
        cursor = database.cursor()
    except:
        print 'MySQL connect fail...'

    cursor.execute("SELECT id from fittings")
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
        print 'fittings_id关联',id_concect

    try:
        '''warning:这里需要设置为环境获取'''
        db = MySQLdb.connect("localhost","root","uroot012","erp_development",charset='utf8')
        cursor = db.cursor()
    except:
        print 'MySQL connect fail...'

    cursor.execute("SELECT * from fittings_outputs  where belongs=%s"%id_concect[int(query_out)])
    data = cursor.fetchall()
    cursor.close()
    db.close()
    jsonData = []

    for n,row  in enumerate(data):
        ##print data[0]
        ##print row[1]
        result = {}
        result['id'] = n + 1
        result['dates'] = row[1]
        result['nums'] = row[2]
        result['purpose'] = row[3]
        result['receiptor'] = row[4]
        result['remarks'] = row[6]
        result['from_which'] = row[7]
        result['status'] = row[8]

        jsonData.append(result)

    return json.dumps(jsonData)

@main.route('/repertory/semi_finished',methods = ['GET','POST'])
@login_required
def semi_finished():

    '''统计库存量'''
    try:
        '''warning:这里需要设置为环境获取'''
        database = MySQLdb.connect("localhost","root","uroot012","erp_development",charset='utf8')
        cursor = database.cursor()
    except:
        print 'MySQL connect fail...'

    cursor.execute("SELECT id from semi_finished")
    data = cursor.fetchall()

    if len(data) !=0:
	
        input_get=[]
        output_get=[]

        get_data=[]
        for i,w in enumerate(data):
            get_data.append(w[0])

        print '半成品数据表的id',get_data
        
        id_from_table = []
        id_from_mysql = []
	for i,datas in enumerate(get_data):
            print 'i',i+1
	    print 'datas',datas
            id_from_table.append(i+1)
            id_from_mysql.append(datas)
	
            '''计算库存量'''
            cursor.execute("SELECT SUM(nums) from semi_finished_input%s"%(datas))
            input_data = cursor.fetchone()
            #print input_data
	    if input_data == (None,):
                input_data = (Decimal(0),)	
                #print '+++++++',input_data
	    #print type(input_data)


            cursor.execute("SELECT SUM(nums) from semi_finished_output%s"%(datas))
            output_data = cursor.fetchone()
	    if output_data == (None,):
                output_data = (Decimal(0),)
                #print '+++++++',output_data


            #print list(input_data),list(output_data)
            input_get.append(list(input_data))
            output_get.append(list(output_data))

            print input_data     
            print output_data                   
        
        '''建立id关联'''
        id_concect = dict(zip(id_from_table,id_from_mysql))
        print id_concect
        
        stock = []
        if input_get and output_get is not None:
            for i in range(len(input_get)):
                stock_data =input_get[i][0]-output_get[i][0]
                stock.append(stock_data)

        '''这里要提交才能更新值'''
        for i,w in enumerate(get_data):
            cursor.execute("UPDATE semi_finished SET nums=%s WHERE id=%s"%(stock[i],w))
        database.commit()
        

    # if request.method == 'POST':
    id = request.form.get('row[id]', '')
    nums= request.form.get('row[nums]', '')
    oldValue = request.form.get('oldValue', '')
    name = request.form.get('row[name]', '')
    remarks = request.form.get('row[remarks]', '')
    price = request.form.get('row[price]', '')
    
    print id,nums,oldValue,name,price,remarks


    if id !='':
        old_Value = Semi_finished.query.filter_by(id=id_concect[int(id)]).first()
        if  old_Value is not None:
            print "更新数据"
            Semi_finished.query.filter_by(id=id_concect[int(id)]).update({"name":name,"price":price,"remarks":remarks })

            db.session.commit()



    '''删除记录并删除相关表'''
    def reset_delete(ids):
        app = current_app._get_current_object()
        try:
            '''warning:这里需要设置为环境获取'''
            database = MySQLdb.connect("localhost","root","uroot012","erp_development",charset='utf8')
            cursor = database.cursor()
        except:
            print 'MySQL connect fail...'

        cursor.execute("DELETE FROM semi_finished WHERE id=%s"%id_concect[int(ids)])

        #cursor.execute("ALTER TABLE fittings DROP id")
        #cursor.execute("ALTER TABLE fittings ADD id INT( 8 ) NOT NULL FIRST")
        #cursor.execute("ALTER TABLE fittings MODIFY COLUMN id INT( 8 ) NOT NULL AUTO_INCREMENT,ADD PRIMARY KEY(id)")

        cursor.execute("DROP TABLE semi_finished_input%s"%id_concect[int(ids)])
        cursor.execute("DROP TABLE semi_finished_output%s"%id_concect[int(ids)])

        cursor.close()
        database.close()

    def create_tables():
        get_time = time.strftime('%Y-%m-%d',time.localtime(time.time()))
        app = current_app._get_current_object()
        try:
            '''warning:这里需要设置为环境获取'''
            database = MySQLdb.connect("localhost","root","uroot012","erp_development",charset='utf8')
            cursor = database.cursor()
        except:
            print 'MySQL connect fail...'


        cursor.execute("SELECT id from semi_finished")
        data = cursor.fetchall()
        get_data=[]
        for i,w in enumerate(data):
            get_data.append(w[0])
        #print get_data
        #n = len(data)
	#print 'max!!!!!!!!',max(get_data)

        cursor.execute("CREATE TABLE semi_finished_input%s(id int PRIMARY KEY NOT NULL AUTO_INCREMENT ,dates varchar(64),nums INT,price varchar(64),response varchar(64),remarks varchar(64)) "%(max(get_data)))
        cursor.execute("INSERT INTO semi_finished_input%s(dates,nums,price,response,remarks) VALUE ('%s',0,'0.00','edit','')"%(max(get_data),get_time))
        cursor.execute("CREATE TABLE semi_finished_output%s(id int PRIMARY KEY NOT NULL AUTO_INCREMENT ,dates varchar(64),nums INT,price varchar(64),purpose varchar(64),response varchar(64),remarks varchar(64)) " %(max(get_data)))
        cursor.execute("INSERT INTO semi_finished_output%s(dates,nums,price,purpose,response,remarks) VALUE ('%s',0,'0.00','edit','','')"%(max(get_data),get_time))
        cursor.close()
        database.commit()
        database.close()

    #删除数据
    ids = request.form.get('ids[]','')
    remove_name = request.form.get('remove_name[]','')

    if ids and remove_name != " ":


        '''重置id并删除相关表'''
        reset_delete(ids)

    '''增加'''
    #get_time = time.strftime('%Y-%m-%d',time.localtime(time.time()))
    add =request.form.get('add','')
    # id = request.form.get('ids','')

    if add == 'add_true':
        

        add_item = Semi_finished(name='edit',nums=0,price='0.00')
        db.session.add(add_item)
        db.session.commit()
        create_tables()


    #判断采购提醒表是否为空，不为空则显示提醒
    try:                 
        database = MySQLdb.connect("localhost","root","uroot012","erp_development",charset='utf8')
        cursor = database.cursor()
    except:
        print 'MySQL connect fail...'

    cursor.execute("SELECT * FROM  purchase_list")
    data = cursor.fetchall()
    print '/////////',data
    if data == ():
        print '为空'
        tip = "不提示"
    elif  data != ():
        print '不为空',data
        tip = "提示"

    return render_template('repertory/semi_finished.html',tip=tip)


@main.route('/repertory/semi_finished/return_json',methods = ['GET','POST'])
@login_required
def semi_return_json():
    app = current_app._get_current_object()
    try:
        '''warning:这里需要设置为环境获取'''
        db = MySQLdb.connect("localhost","root","uroot012","erp_development",charset='utf8')
        cursor = db.cursor()
    except:
        print 'MySQL connect fail...'
    cursor.execute("SELECT * from semi_finished")
    data = cursor.fetchall()
    cursor.close()
    db.close()
    jsonData = []

    for n,row  in enumerate(data):
        ##print data[0]
        ##print row[1]
        result = {}
        result['id'] = n+1
        result['name'] = row[1]
        result['nums'] = row[2]
        result['price'] = row[3]
        result['remarks'] = row[4]

        jsonData.append(result)

    return json.dumps(jsonData)


@main.route('/repertory/semi_finished_in',methods = ['GET','POST'])
@login_required
def semi_finished_in():
    if request.method == 'POST':
        print 'POST'
        #oldValue = request.form.get('oldValue','')
        id = request.form.get('row[id]','')
        dates = request.form.get('row[dates]','')
        nums = request.form.get('row[nums]','')
        price = request.form.get('row[price]','') 
        response = request.form.get('row[response]','')
        remarks = request.form.get('row[remarks]','')

        """建立表格ID与数据表ID的关联"""  

        try:
            '''warning:这里需要设置为环境获取'''
            database = MySQLdb.connect("localhost","root","uroot012","erp_development",charset='utf8')
            cursor = database.cursor()
        except:
            print 'MySQL connect fail...'
   
        cursor.execute("SELECT id from semi_finished")
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
            print 'semi_finished_in_id关联',id_concect

        #修改哪一个数据表 write_in
        write_in = request.form.get('write_in','')     
        print "修改数据库的名字",write_in 
        table_name = 'semi_finished_input%s'%id_concect[int(write_in)]

        #这里id不能写成not None
        if id !='':
            try:

                db = MySQLdb.connect("localhost","root","uroot012","erp_development",charset='utf8')
                cursor = db.cursor()
            except:
                print 'MySQL connect fail...'

            sql = " UPDATE " + table_name + \
              " SET dates = '%s',nums = %d,price= '%s',response= '%s', remarks= '%s' WHERE id = %s "%(dates,int(nums),price,response,remarks,id)
            print  sql
            cursor.execute(sql)
            cursor.close()
            db.commit()
            db.close()



        #删除数据并重置id
        ids = request.form.get('ids[]','')
        remove_name = request.form.get('remove_name[]','')
        del_in = request.form.get('del_in','')     

        if ids and remove_name != " ":
            print "删除数据",del_in 

            del_table_name = table_name

            try:
                '''warning:这里需要设置为环境获取'''
                db = MySQLdb.connect("localhost","root","uroot012","erp_development",charset='utf8')
                cursor = db.cursor()
            except:
                print 'MySQL connect fail...'

            sql_remove = " DELETE FROM " + del_table_name + " WHERE id = %s "%int(ids)
            #print  sql_remove
            cursor.execute(sql_remove)

            cursor.execute("ALTER TABLE %s DROP id"%del_table_name)
            cursor.execute("ALTER TABLE %s ADD id INT( 8 ) NOT NULL FIRST"%del_table_name)
            cursor.execute("ALTER TABLE %s MODIFY COLUMN id INT( 8 ) NOT NULL AUTO_INCREMENT,ADD PRIMARY KEY(id)"%del_table_name)

            cursor.close()
            db.commit()
            db.close()

        #添加数据
        add =request.form.get('add','')
        get_time = time.strftime('%Y-%m-%d',time.localtime(time.time()))

        if add == 'add_true':

            #添加哪一个数据表 
            add_in = request.form.get('add_in','')    
            print "添加数据",add_in 

            add_table_name = table_name

            try:
                '''warning:这里需要设置为环境获取'''
                db = MySQLdb.connect("localhost","root","uroot012","erp_development",charset='utf8')
                cursor = db.cursor()
            except:
                print 'MySQL connect fail...'

            sql_add= "insert into " + add_table_name + "(dates,nums,price,response,remarks)" + " values('%s',0,'0.00','','') "%(get_time)
            print  sql_add
            cursor.execute(sql_add)

            cursor.close()
            db.commit()
            db.close()

        return render_template('repertory/semi_finished_in.html')

    else:
        print 'GET'
        get_name = request.args.get('name')
        print 'get_name',get_name

        return render_template('repertory/semi_finished_in.html',get_name=get_name)


@main.route('/repertory/semi_finished_in/return_json',methods = ['GET','POST'])
@login_required
def semi_in_return_json():

    #if request.method == 'GET':

    '''后台可直接获取url？参数'''
    query_in = request.args.get('in')
    print "query_in",query_in


    """建立表格ID与数据表ID的关联"""  

    try:
        '''warning:这里需要设置为环境获取'''
        database = MySQLdb.connect("localhost","root","uroot012","erp_development",charset='utf8')
        cursor = database.cursor()
    except:
        print 'MySQL connect fail...'

    cursor.execute("SELECT id from semi_finished")
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
        print 'semi_finished_id关联',id_concect

    try:

        db = MySQLdb.connect("localhost","root","uroot012","erp_development",charset='utf8')
        cursor = db.cursor()
    except:
        print 'MySQL connect fail...'

    cursor.execute("SELECT * from semi_finished_input%s"%id_concect[int(query_in)])
    data = cursor.fetchall()
    cursor.close()
    db.close()
    jsonData = []

    for n,row  in enumerate(data):
        ##print data[0]
        ##print row[1]
        result = {}
        result['id'] = row[0]
        result['dates'] = row[1]
        result['nums'] = row[2]
        result['price'] = row[3]   
        result['response'] = row[4]
        result['remarks'] = row[5]

        jsonData.append(result)

    return json.dumps(jsonData)

@main.route('/repertory/semi_finished_out',methods = ['GET','POST'])
@login_required
def semi_finished_out():
    if request.method == 'POST':
        #oldValue = request.form.get('oldValue','') dates,nums,purpose,response,remarks
        dates = request.form.get('row[dates]','')
        nums = request.form.get('row[nums]','')
        price = request.form.get('row[price]','')
        id = request.form.get('row[id]','')
        purpose = request.form.get('row[purpose]','')
        response = request.form.get('row[response]','')
        remarks = request.form.get('row[remarks]','')

        """建立表格ID与数据表ID的关联"""  

        try:
            '''warning:这里需要设置为环境获取'''
            database = MySQLdb.connect("localhost","root","uroot012","erp_development",charset='utf8')
            cursor = database.cursor()
        except:
            print 'MySQL connect fail...'
   
        cursor.execute("SELECT id from semi_finished")
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
            print 'semi_finished_in_id关联',id_concect


        #修改哪一个数据表 write_out
        write_out = request.form.get('write_out','')     
        print "修改数据库的id",write_out  
        table_name = 'semi_finished_output%s'%id_concect[int(write_out)]

        #这里id不能写成not None
        if id !='':
            try:

                db = MySQLdb.connect("localhost","root","uroot012","erp_development",charset='utf8')
                cursor = db.cursor()
            except:
                print 'MySQL connect fail...'


            sql = " UPDATE " + table_name + \
              " SET dates = '%s',nums = %d,price = '%s',purpose = '%s',response = '%s',remarks = '%s' WHERE id = %s "%(dates,int(nums),price,purpose,response,remarks,id)
            #print  sql

            cursor.execute(sql)
            cursor.close()
            db.commit()
            db.close()

        #删除数据并重置id
        ids = request.form.get('ids[]','')
        remove_name = request.form.get('remove_name[]','')
        del_out = request.form.get('del_out','')     

        if ids and remove_name != " ":
            print "删除数据",del_out 
            del_table_name = table_name

            try:
                '''warning:这里需要设置为环境获取'''
                db = MySQLdb.connect("localhost","root","uroot012","erp_development",charset='utf8')
                cursor = db.cursor()
            except:
                print 'MySQL connect fail...'

            sql_remove = " DELETE FROM " + del_table_name + " WHERE id = %s "%int(ids)
            print  sql_remove
            cursor.execute(sql_remove)

            cursor.execute("ALTER TABLE %s DROP id"%del_table_name)
            cursor.execute("ALTER TABLE %s ADD id INT( 8 ) NOT NULL FIRST"%del_table_name)
            cursor.execute("ALTER TABLE %s MODIFY COLUMN id INT( 8 ) NOT NULL AUTO_INCREMENT,ADD PRIMARY KEY(id)"%del_table_name)

            cursor.close()
            db.commit()
            db.close()

        #添加数据
        add =request.form.get('add','')
        get_time = time.strftime('%Y-%m-%d',time.localtime(time.time()))

        if add == 'add_true':

            #添加哪一个数据表 
            add_out = request.form.get('add_out','')    
            print "添加数据",add_out 
            
            add_table_name = table_name
            try:
                '''warning:这里需要设置为环境获取'''
                db = MySQLdb.connect("localhost","root","uroot012","erp_development",charset='utf8')
                cursor = db.cursor()
            except:
                print 'MySQL connect fail...'


            sql_add= "insert into " + add_table_name + "(dates,nums,price,purpose,response,remarks)" + " values('%s',0,'0.00','edit','edit','') "%(get_time)
            print  sql_add
            cursor.execute(sql_add)

            cursor.close()
            db.commit()
            db.close()

        return render_template('repertory/semi_finished_out.html')
    else:
        get_name = request.args.get('name')
        print 'get_name',get_name

        return render_template('repertory/semi_finished_out.html',get_name=get_name)

@main.route('/repertory/semi_finished_out/return_json',methods = ['GET','POST'])
@login_required
def semi_finished_out_return_json():
    '''后台可直接获取url？参数'''
    query_out = request.args.get('out')
    print "query_out",query_out

    """建立表格ID与数据表ID的关联"""  

    try:
        '''warning:这里需要设置为环境获取'''
        database = MySQLdb.connect("localhost","root","uroot012","erp_development",charset='utf8')
        cursor = database.cursor()
    except:
        print 'MySQL connect fail...'

    cursor.execute("SELECT id from semi_finished")
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
        print 'semi_finished_id关联',id_concect

    try:
        '''warning:这里需要设置为环境获取'''
        db = MySQLdb.connect("localhost","root","uroot012","erp_development",charset='utf8')
        cursor = db.cursor()
    except:
        print 'MySQL connect fail...'

    cursor.execute("SELECT * from semi_finished_output%s"%id_concect[int(query_out)])
    data = cursor.fetchall()
    cursor.close()
    db.close()
    jsonData = []

    for n,row  in enumerate(data):

        result = {}
        result['id'] = row[0]
        result['dates'] = row[1]
        result['nums'] = row[2]
        result['price'] = row[3]
        result['purpose'] = row[4]			
        result['response'] = row[5]
        result['remarks'] = row[6]
        jsonData.append(result)

    return json.dumps(jsonData)

@main.route('/repertory/end_product',methods = ['GET','POST'])
@login_required
def end_product():

    '''统计配件库存量'''

    app = current_app._get_current_object()
    try:
        '''warning:这里需要设置为环境获取'''
        database = MySQLdb.connect("localhost","root","uroot012","erp_development",charset='utf8')
        cursor = database.cursor()
    except:
        print 'MySQL connect fail...'

    cursor.execute("SELECT id from end_product")
    data = cursor.fetchall()
     
    #建立id关联
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

    print 'end_product id关联',id_concect
    
    #更新库存量
    try:
        '''warning:这里需要设置为环境获取'''
        database = MySQLdb.connect("localhost","root","uroot012","erp_development",charset='utf8')
        cursor = database.cursor()
    except:
        print 'MySQL connect fail...'

    cursor.execute("SELECT id from end_product")
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

            print i+1 ,datas
            cursor.execute("SELECT SUM(nums) from end_product_inputs where belongs=%d"%datas)
            input_data = cursor.fetchone()
            if input_data == (None,):
                input_data = (Decimal(0),)	
            print '获取入库表总和',input_data
            
            cursor.execute("SELECT SUM(nums) from end_product_outputs where belongs=%d"%datas)
            output_data = cursor.fetchone()
            if output_data == (None,):
                output_data = (Decimal(0),)
            print '获取出库表总和',output_data

            input_get.append(list(input_data))
            output_get.append(list(output_data))
        
        '''建立id关联'''
        id_concect = dict(zip(id_from_table,id_from_mysql))
        print id_concect
        
        stock = []
        if input_get and output_get is not None:
            for i in range(len(input_get)):
                stock_data =input_get[i][0]-output_get[i][0]
                stock.append(stock_data)

        '''这里要提交才能更新值'''
        for i,w in enumerate(get_data):
            cursor.execute("UPDATE end_product SET nums=%s WHERE id=%s"%(stock[i],w))
        database.commit()
        

    # if request.method == 'POST':
    id = request.form.get('row[id]', '')
    nums= request.form.get('row[nums]', '')
    price= request.form.get('row[price]', '')
    oldValue = request.form.get('oldValue', '')
    name = request.form.get('row[name]', '')
    remarks = request.form.get('row[remarks]', '')
    print id,nums,name,price

    if id !='':
        old_Value = End_product.query.filter_by(id=id_concect[int(id)]).first()
        if old_Value is not None:
            print '更新数据'
            End_product.query.filter_by(id=id_concect[int(id)]).update({"name":name,"price":price,"remarks":remarks })
            db.session.commit()

    '''删除记录并删除相关表'''
    def reset_delete(ids):
        app = current_app._get_current_object()
        try:
            '''warning:这里需要设置为环境获取'''
            database = MySQLdb.connect("localhost","root","uroot012","erp_development",charset='utf8')
            cursor = database.cursor()
        except:
            print 'MySQL connect fail...'

        cursor.execute("DELETE FROM end_product WHERE id=%s"%id_concect[int(ids)])

        cursor.close()
        database.commit()
        database.close()

    #删除数据
    ids = request.form.get('ids[]','')
    remove_name = request.form.get('remove_name[]','')

    if ids and remove_name != " ":
        '''不重置id并删除相关表'''
        reset_delete(ids)

    '''增加'''
    #get_time = time.strftime('%Y-%m-%d',time.localtime(time.time()))
    add =request.form.get('add','')
    # id = request.form.get('ids','')

    if add == 'add_true':
        add_item = End_product(name='edit',nums=0,price='0.00')
        db.session.add(add_item)
        db.session.commit()

    #判断采购提醒表是否为空，不为空则显示提醒
    try:                 
        database = MySQLdb.connect("localhost","root","uroot012","erp_development",charset='utf8')
        cursor = database.cursor()
    except:
        print 'MySQL connect fail...'

    cursor.execute("SELECT * FROM  purchase_list")
    data = cursor.fetchall()

    if data == ():
        print '为空'
        tip = "不提示"
    elif  data != ():
        print '不为空',data
        tip = "提示"        

    return render_template('repertory/end_product.html',tip=tip)


@main.route('/repertory/end_product/return_json',methods = ['GET','POST'])
@login_required
def end_product_return_json():
        app = current_app._get_current_object()
        try:
            '''warning:这里需要设置为环境获取'''
            db = MySQLdb.connect("localhost","root","uroot012","erp_development",charset='utf8')
            cursor = db.cursor()
        except:
            print 'MySQL connect fail...'
        cursor.execute("SELECT * from end_product")
        data = cursor.fetchall()
        cursor.close()
        db.close()
        jsonData = []

        for n,row  in enumerate(data):
            ##print data[0]
            ##print row[1]
            result = {}
            result['id'] = n+1
            result['name'] = row[1]
            result['nums'] = row[2]
            result['price'] = row[3]
            result['remarks'] = row[4]

            jsonData.append(result)

        return json.dumps(jsonData)


@main.route('/repertory/end_product_in',methods = ['GET','POST'])
@login_required
def end_product_in():

    if request.method == 'POST':
        #oldValue = request.form.get('oldValue','')
        id = request.form.get('row[id]','')
        dates = request.form.get('row[dates]','')
        nums = request.form.get('row[nums]','')
        price = request.form.get('row[price]','')
        response = request.form.get('row[response]','')
        remarks = request.form.get('row[remarks]','')

        """建立表格ID与数据表ID的关联"""  
        try:
            '''warning:这里需要设置为环境获取'''
            database = MySQLdb.connect("localhost","root","uroot012","erp_development",charset='utf8')
            cursor = database.cursor()
        except:
            print 'MySQL connect fail...'
   
        cursor.execute("SELECT id from end_product")
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

                end_product_id_concect = dict(zip(id_from_table,id_from_mysql))
        print 'end_product_id关联',end_product_id_concect

        cursor.close()
        database.commit()
        database.close()

        write_in = request.form.get('write_in','')     

        print 'write_in',write_in
        if write_in !='':
            """建立end_product表格 与end_product_inputs 的关联"""  
            try:
                '''warning:这里需要设置为环境获取'''
                database = MySQLdb.connect("localhost","root","uroot012","erp_development",charset='utf8')
                cursor = database.cursor()
            except:
                print 'MySQL connect fail...'
   
            cursor.execute("SELECT id from end_product_inputs where belongs=%s"%end_product_id_concect[int(write_in)])
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

                end_product_inputs_id_concect = dict(zip(id_from_table,id_from_mysql))
            print 'end_product_inputs id(write)关联',end_product_inputs_id_concect

            print '更新数据'
        
            try:
                db = MySQLdb.connect("localhost","root","uroot012","erp_development",charset='utf8')
                cursor = db.cursor()
            except:
                print 'MySQL connect fail...'
            table_name = 'end_product_inputs'
            sql = " UPDATE " + table_name + \
              " SET dates = '%s',nums = %d,price= '%s',response= '%s', remarks= '%s' WHERE id = %s "%(dates,int(nums),price,response,remarks,end_product_inputs_id_concect[int(id)] )
            print  sql
            cursor.execute(sql)
            cursor.close()
            db.commit()
            db.close()

        #删除点击的id
        ids = request.form.get('ids[]','')
        del_in = request.form.get('del_in','')

        if  ids and del_in !='':
            """建立fittings_inputs表格 与fittings_inputs 的关联"""  
            try:
                '''warning:这里需要设置为环境获取'''
                database = MySQLdb.connect("localhost","root","uroot012","erp_development",charset='utf8')
                cursor = database.cursor()
            except:
                print 'MySQL connect fail...'
   
            cursor.execute("SELECT id from end_product_inputs where belongs=%s"%end_product_id_concect[int(del_in)])
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


                end_product_inputs_id_concect = dict(zip(id_from_table,id_from_mysql))
            print 'end_product_inputs id(del)关联',end_product_inputs_id_concect

            cursor.close()
            database.commit()
            database.close()

            print '删除数据'

            try:
                '''warning:这里需要设置为环境获取'''
                db = MySQLdb.connect("localhost","root","uroot012","erp_development",charset='utf8')
                cursor = db.cursor()
            except:
                print 'MySQL connect fail...'

            sql_remove = " DELETE FROM end_product_inputs"  + " WHERE id = %s "%end_product_inputs_id_concect[int(ids)]
            print  sql_remove

            cursor.execute(sql_remove)
  
            # cursor.execute("ALTER TABLE %s DROP id"%del_table_name)
            # cursor.execute("ALTER TABLE %s ADD id INT( 8 ) NOT NULL FIRST"%del_table_name)
            # cursor.execute("ALTER TABLE %s MODIFY COLUMN id INT( 8 ) NOT NULL AUTO_INCREMENT,ADD PRIMARY KEY(id)"%del_table_name)

            cursor.close()
            db.commit()
            db.close()

        add =request.form.get('add','')
        belogns =request.form.get('add_in','')
        get_time = time.strftime('%Y-%m-%d',time.localtime(time.time()))            

        if add == 'add_true':
            print "添加数据" 
            
            #获取belongs值
            try:
                '''warning:这里需要设置为环境获取'''
                database = MySQLdb.connect("localhost","root","uroot012","erp_development",charset='utf8')
                cursor = database.cursor()
            except:
                print 'MySQL connect fail...'
   
            cursor.execute("SELECT id from end_product")
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
            print 'end_product_belongs id关联',id_concect    

            print 'belongs',id_concect[int(belogns)]

            #添加哪一个数据表 
            #add_in = request.form.get('add_in','')    
            try:
                '''warning:这里需要设置为环境获取'''
                db = MySQLdb.connect("localhost","root","uroot012","erp_development",charset='utf8')
                cursor = db.cursor()
            except:
                print 'MySQL connect fail...'
 
            sql_add= "insert into end_product_inputs"  + "(dates,nums,price,response,remarks,belongs)" + " values('%s',0,0,'','',%s) "%(get_time,id_concect[int(belogns)])
            cursor.execute(sql_add)

            cursor.close()
            db.commit()
            db.close()
        return render_template('repertory/end_product_in.html')        
    else:
        print 'GET'
        get_name = request.args.get('name')
        print 'get_name',get_name
        return render_template('repertory/end_product_in.html',get_name=get_name)

@main.route('/repertory/end_product_in/return_json',methods = ['GET','POST'])
@login_required
def end_product_in_return_json():

    '''后台可直接获取url？参数'''
    query_in = request.args.get('in')
    print "query_in",query_in

    """建立表格ID与数据表ID的关联"""  
    try:
        '''warning:这里需要设置为环境获取'''
        database = MySQLdb.connect("localhost","root","uroot012","erp_development",charset='utf8')
        cursor = database.cursor()
    except:
        print 'MySQL connect fail...'

    cursor.execute("SELECT id from end_product")
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
        print 'end_product_id关联',id_concect

    try:
        '''warning:这里需要设置为环境获取'''
        db = MySQLdb.connect("localhost","root","uroot012","erp_development",charset='utf8')
        cursor = db.cursor()
    except:
        print 'MySQL connect fail...'

    cursor.execute("SELECT * from end_product_inputs where belongs=%s"%id_concect[int(query_in)])
    data = cursor.fetchall()
    cursor.close()
    db.close()
    jsonData = []

    for n,row  in enumerate(data):
        ##print data[0]
        ##print row[1]
        result = {}
        result['id'] = n + 1
        result['dates'] = row[1]
        result['nums'] = row[2]
        result['price'] = row[3]
        result['response'] = row[4]
        result['remarks'] = row[5]
        jsonData.append(result)

    return json.dumps(jsonData)




@main.route('/repertory/end_product_out',methods = ['GET','POST'])
@login_required
def end_product_out():
    if request.method == 'POST':
        dates = request.form.get('row[dates]','')
        nums = request.form.get('row[nums]','')
        id = request.form.get('row[id]','')
        purpose = request.form.get('row[purpose]','')
        response = request.form.get('row[response]','')
        remarks = request.form.get('row[remarks]','')

        """  建立end_product表格ID与数据表end_product ID的关联"""  
        try:
            '''warning:这里需要设置为环境获取'''
            database = MySQLdb.connect("localhost","root","uroot012","erp_development",charset='utf8')
            cursor = database.cursor()
        except:
            print 'MySQL connect fail...'
   
        cursor.execute("SELECT id from end_product")
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

            end_product_id_concect = dict(zip(id_from_table,id_from_mysql))
        print 'end_product_id_concect 关联',end_product_id_concect

        cursor.close()
        database.commit()
        database.close()

        write_out = request.form.get('write_out','')
        print 'write_out',write_out
        if write_out !='':
            """建立end_product_outputs表格 与end_product_outputs 的关联"""  
            try:
                '''warning:这里需要设置为环境获取'''
                database = MySQLdb.connect("localhost","root","uroot012","erp_development",charset='utf8')
                cursor = database.cursor()
            except:
                print 'MySQL connect fail...'
   
            cursor.execute("SELECT id from end_product_outputs where belongs=%s"%end_product_id_concect[int(write_out)])
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

                end_product_outputs_id_concect = dict(zip(id_from_table,id_from_mysql))
            print 'end_product_outputs id(write)关联',end_product_outputs_id_concect

            print '更新数据'
        
            try:
                db = MySQLdb.connect("localhost","root","uroot012","erp_development",charset='utf8')
                cursor = db.cursor()
            except:
                print 'MySQL connect fail...'
            table_name = 'end_product_outputs'
            sql = " UPDATE " + table_name + \
              " SET dates = '%s',nums = %d,purpose = '%s',response = '%s',remarks = '%s'  WHERE id = %s "%(dates,int(nums),purpose,response,remarks,end_product_outputs_id_concect[int(id)])
            cursor.execute(sql)
            cursor.close()
            db.commit()
            db.close()

        #删除点击的id
        ids = request.form.get('ids[]','')
        del_out = request.form.get('del_out','')

        if  ids and del_out !='':
            """建立end_product_outputs表格 与end_product_outputs 的关联"""  
            try:
                '''warning:这里需要设置为环境获取'''
                database = MySQLdb.connect("localhost","root","uroot012","erp_development",charset='utf8')
                cursor = database.cursor()
            except:
                print 'MySQL connect fail...'
   
            cursor.execute("SELECT id from end_product_outputs where belongs=%s"%end_product_id_concect[int(del_out)])
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


                end_product_outputs_id_concect = dict(zip(id_from_table,id_from_mysql))
            print 'end_product_outputs id(del)关联',end_product_outputs_id_concect

            cursor.close()
            database.commit()
            database.close()

            print '删除数据'

            try:
                '''warning:这里需要设置为环境获取'''
                db = MySQLdb.connect("localhost","root","uroot012","erp_development",charset='utf8')
                cursor = db.cursor()
            except:
                print 'MySQL connect fail...'

            sql_remove = " DELETE FROM  end_product_outputs"  + " WHERE id = %s "%end_product_outputs_id_concect[int(ids)]
            print  sql_remove

            cursor.execute(sql_remove)
  
            # cursor.execute("ALTER TABLE %s DROP id"%del_table_name)
            # cursor.execute("ALTER TABLE %s ADD id INT( 8 ) NOT NULL FIRST"%del_table_name)
            # cursor.execute("ALTER TABLE %s MODIFY COLUMN id INT( 8 ) NOT NULL AUTO_INCREMENT,ADD PRIMARY KEY(id)"%del_table_name)

            cursor.close()
            db.commit()
            db.close()


        add =request.form.get('add','')
        belogns =request.form.get('add_out','')
        get_time = time.strftime('%Y-%m-%d',time.localtime(time.time()))
        
        if add == 'add_true':
            print "添加数据" 
            
            #获取belongs值
            try:
                '''warning:这里需要设置为环境获取'''
                database = MySQLdb.connect("localhost","root","uroot012","erp_development",charset='utf8')
                cursor = database.cursor()
            except:
                print 'MySQL connect fail...'
   
            cursor.execute("SELECT id from end_product")
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
            print 'end_product_belongs id关联',id_concect    

            print 'belongs',id_concect[int(belogns)]

            #添加哪一个数据表 
            #add_in = request.form.get('add_in','')    
            try:
                '''warning:这里需要设置为环境获取'''
                db = MySQLdb.connect("localhost","root","uroot012","erp_development",charset='utf8')
                cursor = db.cursor()
            except:
                print 'MySQL connect fail...'
 
            sql_add= "insert into end_product_outputs"  + "(dates,nums,purpose,response,remarks,belongs)" + " values('%s',0,'','','',%s) "%(get_time,id_concect[int(belogns)])
            cursor.execute(sql_add)

            cursor.close()
            db.commit()
            db.close()
        return render_template('repertory/end_product_out.html')

    else:
        get_name = request.args.get('name')
        print 'get_name',get_name
        return render_template('repertory/end_product_out.html',get_name=get_name)


@main.route('/repertory/end_product_out/return_json',methods = ['GET','POST'])
@login_required
def end_product_out_return_json():
    '''后台可直接获取url？参数'''
    query_out = request.args.get('out')
    print "query_out",query_out

    """建立表格ID与数据表ID的关联"""  
    try:
        '''warning:这里需要设置为环境获取'''
        database = MySQLdb.connect("localhost","root","uroot012","erp_development",charset='utf8')
        cursor = database.cursor()
    except:
        print 'MySQL connect fail...'

    cursor.execute("SELECT id from end_product")
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
        print 'end_product_id关联',id_concect

    try:
        '''warning:这里需要设置为环境获取'''
        db = MySQLdb.connect("localhost","root","uroot012","erp_development",charset='utf8')
        cursor = db.cursor()
    except:
        print 'MySQL connect fail...'

    cursor.execute("SELECT * from end_product_outputs where belongs=%s"%id_concect[int(query_out)])
    data = cursor.fetchall()
    cursor.close()
    db.close()
    jsonData = []

    for n,row  in enumerate(data):
        ##print data[0]
        ##print row[1]
        result = {}
        result['id'] = n + 1
        result['dates'] = row[1]
        result['nums'] = row[2]
        result['purpose'] = row[3]
        result['response'] = row[4]
        result['remarks'] = row[5]

        jsonData.append(result)

    return json.dumps(jsonData)



