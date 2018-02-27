# -*- coding:utf-8 -*-
__author__ = 'xuan'

from flask import render_template,request,current_app,redirect,url_for,send_from_directory
from  . import  main
from flask.ext.login import login_required,current_user,login_user,logout_user
import json,MySQLdb,sys
from  manage import  db  #不添加这个会不能更新数据库
from ..models import Orders,Production_Orders,Delivery_which_in,Delivery_Orders,Delivery_Productions,Payment,Receipts
import json
import time
import string
#from flask_uploads import UploadSet,IMAGES,configure_uploads
from werkzeug.utils import secure_filename
from manage import app
import PIL
from PIL import Image
import simplejson
import traceback
import os

from werkzeug.utils import secure_filename
from lib.upload_receipts_file  import upload_receipts_file

reload(sys)
sys.setdefaultencoding('utf8')



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


'''已收款'''
@main.route('/payment/received_payment',methods = ['GET','POST'])
@login_required
def received_payment():
    conn = MySQLdb.connect("localhost","root","uroot012","erp_development",charset='utf8')

    cursor = conn.cursor()
    
    '''
	从订单获取日期 税种
        由合同号获取送货单编号，获取型号 单价 数量 合同金额
    '''
    #获取payment中所有订单号
    cursor.execute("SELECT no from payment ORDER BY id")
    delivery_no = cursor.fetchall()
    for no in delivery_no:
	#cursor.execute("SELECT order_date from orders where order_number='%s'"%order[0])
	#print("SELECT production_name1  from delivery_%s"%no[0])
        cursor.execute("SELECT production_name1  from delivery_%s"%no[0])
        pro_mess = cursor.fetchall()   
	print('pro_mess',no,pro_mess[0])    



    #for i in order_data:
    #cursor.execute("SELECT num from payment ORDER BY id")

    #nums = cursor.fetchall()

    #for pay in payment:
	#for num in nums:
	    #print(pay,num)





    #for date in order_date:


    #cursor.execute("UPDATE payment SET tem_cost='%s' where purchase_order='%s'"%(date[0],i[0]))
    #print('update')
    #conn.commit()

    if request.method == 'POST':
        #修改数据
        id = request.form.get('row[id]', '')
        received_payment = request.form.get('row[received_payment]', '')
        delivery_no = request.form.get('delivery_no', '')
        status = request.form.get('row[status]', '')
   
        print 'delivery_no',delivery_no
        print status   
        if delivery_no and received_payment != '':
            Payment.query.filter_by(no=delivery_no).update({'received_payment':received_payment})
    
        if delivery_no and status != '':
            Payment.query.filter_by(no=delivery_no).update({'status':status})


        db.session.commit() 
      
        """建立表格ID与数据表ID的关联"""  

        #连接数据库
        cursor = getCon().cursor() 
    	cursor.execute("SELECT * from payment where status='已收款' ")
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


        '''删除记录重置id'''
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

            cursor.execute("DELETE FROM payment WHERE id=%s"%id_concect[int(ids)])

            #cursor.execute("ALTER TABLE payment DROP id")
            #cursor.execute("ALTER TABLE payment ADD id INT( 8 ) NOT NULL FIRST")
            #cursor.execute("ALTER TABLE payment MODIFY COLUMN id INT( 8 ) NOT NULL AUTO_INCREMENT,ADD PRIMARY KEY(id)")

        
            cursor.close()
            conn.commit()
            conn.close()

        #删除数据
        ids = request.form.get('ids[]','')
        remove_no = request.form.get('remove_no[]','')
        remove_order = request.form.get('remove_order[]','')   
        #print remove_order

        if ids and remove_no != " ":
            reset_delete(ids)


        data = request.form.get('data','')
        print "++++++--++",json.loads(data)["no"]
        
        #根据返回的number查找contract中的文件名
        if json.loads(data)["no"] is not None:
            if Receipts.query.filter_by(number=json.loads(data)["no"]).first() is not None:
                filename = Receipts.query.filter_by(number=json.loads(data)["no"]).first().name
            else:
                filename = ''

            print '返回json ',filename    
     
            return simplejson.dumps({"filename": filename}) 
        else:
            return simplejson.dumps({"filename": ''})  

    else:
        return render_template('payment/received_payment.html')



@main.route('/payment/received_payment/return_json',methods = ['GET','POST'])
@login_required
def received_payment_return_json():
        app = current_app._get_current_object()
        try:
            '''warning:这里需要设置为环境获取'''
            db = MySQLdb.connect("localhost","root","uroot012","erp_development",charset='utf8')
            cursor = db.cursor()
        except:
            print 'MySQL connect fail...'
        cursor.execute("SELECT * from payment where status='已收款' ")
        data = cursor.fetchall()
        cursor.close()
        db.close()
        jsonData = []

        for n,row  in enumerate(data):
            ##print row[1]
            result = {}
            result['id'] = n + 1
            result['no'] = row[1]  
            result['purchase_order'] = row[2]
            result['client_name'] = row[3]
            result['saler'] = row[4]
            result['payment'] = row[5]
            result['received_payment'] = row[6]
            result['commission'] = row[7]
            result['cost'] = row[8]
            result['iftax'] = row[9]
            result['profit'] = row[10]
            result['tax'] = row[11]
            result['status'] = row[12]
            result['date'] = row[13]
	    result['type'] = row[14]
	    result['price'] = row[15]
	    result['num'] = row[16]
	    result['tem_cost'] = row[17]
	    result['server_cost'] = row[18]
	    result['consult_cost'] = row[19]
	    result['after_sales'] = row[20]
	    result['tax_type'] = row[21]

            jsonData.append(result)

        return json.dumps(jsonData)


'''未收款'''
@main.route('/payment/not_received_payment',methods = ['GET','POST'])
@login_required
def not_received_payment():
       
    if request.method == 'POST':

        #修改数据
        id = request.form.get('row[id]', '')
        received_payment = request.form.get('row[received_payment]', '')
        delivery_no = request.form.get('delivery_no', '')
        status = request.form.get('row[status]', '')
   
        print 'delivery_no',delivery_no
        print status   
        if delivery_no and received_payment != '':
            Payment.query.filter_by(no=delivery_no).update({'received_payment':received_payment})
    
        if delivery_no and status != '':
            Payment.query.filter_by(no=delivery_no).update({'status':status})


        db.session.commit() 
      
        """建立表格ID与数据表ID的关联"""  

        #连接数据库
        cursor = getCon().cursor() 
    	cursor.execute("SELECT * from payment where status='未收款' ")
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


        '''删除记录重置id'''
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

            cursor.execute("DELETE FROM payment WHERE id=%s"%id_concect[int(ids)])

            #cursor.execute("ALTER TABLE payment DROP id")
            #cursor.execute("ALTER TABLE payment ADD id INT( 8 ) NOT NULL FIRST")
            #cursor.execute("ALTER TABLE payment MODIFY COLUMN id INT( 8 ) NOT NULL AUTO_INCREMENT,ADD PRIMARY KEY(id)")

        
            cursor.close()
            conn.commit()
            conn.close()

        #删除数据
        ids = request.form.get('ids[]','')
        remove_no = request.form.get('remove_no[]','')
        remove_order = request.form.get('remove_order[]','')   
        #print remove_order

        if ids and remove_no != " ":
            reset_delete(ids)


        data = request.form.get('data','')
        print "++++++--++",json.loads(data)["no"]
        
        #根据返回的number查找receipts中的文件名
        if json.loads(data)["no"] is not None:
            if Receipts.query.filter_by(number=json.loads(data)["no"]).first() is not None:
                filename = Receipts.query.filter_by(number=json.loads(data)["no"]).first().name
            else:
                filename = ''

            print '返回json ',filename    
     
            return simplejson.dumps({"filename": filename}) 
        else:
            return simplejson.dumps({"filename": ''})  

    else:
        return render_template('payment/not_received_payment.html')



@main.route('/payment/not_received_payment/return_json',methods = ['GET','POST'])
@login_required
def not_received_payment_return_json():
        app = current_app._get_current_object()
        try:
            '''warning:这里需要设置为环境获取'''
            db = MySQLdb.connect("localhost","root","uroot012","erp_development",charset='utf8')
            cursor = db.cursor()
        except:
            print 'MySQL connect fail...'
        cursor.execute("SELECT * from payment where status='未收款' ")
        data = cursor.fetchall()
        cursor.close()
        db.close()
        jsonData = []

        for n,row  in enumerate(data):
            print data[0]
            ##print row[1]
            result = {}
            result['id'] = n + 1
            result['no'] = row[1]  
            result['purchase_order'] = row[2]
            result['client_name'] = row[3]
            result['saler'] = row[4]
            result['payment'] = row[5]
            result['received_payment'] = row[6]
            result['commission'] = row[7]
            result['cost'] = row[8]
            result['iftax'] = row[9]
            result['profit'] = row[10]
            result['tax'] = row[11]
            result['status'] = row[12]
            result['date'] = row[13]
            result['type'] = row[14]
            result['price'] = row[15]
            result['num'] = row[16]
            result['tem_cost'] = row[17]
            result['server_cost'] = row[18]
            result['consult_cost'] = row[19]
            result['after_sales'] = row[20]
            result['tax_type'] = row[21]
     

            jsonData.append(result)

        return json.dumps(jsonData)


@main.route('/payment/receipts',methods = ['GET','POST'])
@login_required
def receipts():


    return render_template('payment/receipts.html')


#回执单上传
ALLOWED_RECEIPT_EXTENSIONS = set(['gif', 'png', 'jpg', 'jpeg', 'bmp','pdf', 'PDF'])
IGNORED_FILES = set(['.gitignore'])

def allowed_file(filename):
    return '.' in filename and \
        filename.rsplit('.', 1)[1].lower() in ALLOWED_RECEIPT_EXTENSIONS

def gen_file_name(filename):
    """
        If file was exist already, rename it and return a new name
    """
    i = 1
    while os.path.exists(os.path.join(app.config['UPLOADED_RECEIPT_FOLDER'], filename)):
        name, extension = os.path.splitext(filename)
        filename = '%s_%s%s' % (name, str(i), extension)
        i = i + 1

    return filename           

def create_thumbnai(image):
    try:
        basewidth = 80
        img = Image.open(os.path.join(app.config['UPLOADED_RECEIPT_FOLDER'], image))
        wpercent = (basewidth/float(img.size[0]))
        hsize = int((float(img.size[1])*float(wpercent)))
        img = img.resize((basewidth,hsize), PIL.Image.ANTIALIAS)
        img.save(os.path.join(app.config['THUMBNAIL_RECEIPT_FOLDER'], image))

        return True
    
    except:
        print traceback.format_exc()
        return False



@main.route("/payment/upload", methods=['GET', 'POST'])
def receipts_upload():
    if request.method == 'POST':
        print "上传文件"
        file = request.files['file']
        #pprint (vars(objectvalue))

        if file:
            filename = secure_filename(file.filename)
            filename = gen_file_name(filename)
            mimetype = file.content_type


            if not allowed_file(file.filename):
                result = upload_receipts_file(name=filename, type=mimetype, size=0, not_allowed_msg="Filetype not allowed")

            else:
                # save file to disk
                print "保存文件", os.path.join(app.config['UPLOADED_RECEIPT_FOLDER'], filename)
                uploaded_file_path = os.path.join(app.config['UPLOADED_RECEIPT_FOLDER'], filename)
                file.save(uploaded_file_path)

                # create thumbnail after saving
                if mimetype.startswith('image'):
                    create_thumbnai(filename)
                
                # get file size after saving
                size = os.path.getsize(uploaded_file_path)

                #在saving后保存上传日期和路径
        	#获取系统时间 
        	get_time = time.strftime('%Y-%m-%d',time.localtime(time.time()))

                upload_date = get_time

                if '.' in filename:
                    number = filename.rsplit('.', 1)[0]


                add_receipts = Receipts(name=filename,path=uploaded_file_path,upload_date=get_time,number=number)
                db.session.add(add_receipts)
                db.session.commit()

                # return json for js call back
                result = upload_receipts_file(name=filename, type=mimetype, size=size,upload_date=upload_date)
            
            return simplejson.dumps({"files": [result.get_file()]})

    if request.method == 'GET':
        # get all file in ./data directory
        print  'GET',app.config['UPLOADED_RECEIPT_FOLDER']
        files = [ f for f in os.listdir(app.config['UPLOADED_RECEIPT_FOLDER']) if os.path.isfile(os.path.join(app.config['UPLOADED_RECEIPT_FOLDER'],f)) and f not in IGNORED_FILES ]
        
        file_display = []

        for f in files:
            #print os.path.join(app.config['UPLOADED_RECEIPT_FOLDER'], f)

            #获取每个回执单文件的上传日期
            if Receipts.query.filter_by(name=f).first() is not None:
                upload_date_display = Receipts.query.filter_by(name=f).first().upload_date
            else:
                upload_date_display = '-'

            size = os.path.getsize(os.path.join(app.config['UPLOADED_RECEIPT_FOLDER'], f))
            file_saved = upload_receipts_file(name=f, size=size, upload_date=upload_date_display)
            #print file_saved.get_file()
            file_display.append(file_saved.get_file())

        print 'file_display',file_display
        return simplejson.dumps({"files": file_display})

    #return redirect(url_for('index'))


@main.route("/payment/delete/<string:filename>", methods=['DELETE'])
def receipts_delete(filename):
    file_path = os.path.join(app.config['UPLOADED_RECEIPT_FOLDER'], filename)
    file_thumb_path = os.path.join(app.config['THUMBNAIL_RECEIPT_FOLDER'], filename)

    #删除receipts对应记录
    del_filename = Receipts.query.filter_by(name=filename).first()
    db.session.delete(del_filename)
    db.session.commit()

    if os.path.exists(file_path):
        try:
            os.remove(file_path)

            if os.path.exists(file_thumb_path):
                os.remove(file_thumb_path)
            
            return simplejson.dumps({filename: 'True'})
        except:
            return simplejson.dumps({filename: 'False'})


# serve static files
'''这里的路径要构造成与uploadfile返回的url一致'''
@main.route("/payment/data/receipts/receipts_thumbnail/<string:filename>", methods=['GET'])
def get_receipts_thumbnail(filename):
    print "获取静态文件",app.config['THUMBNAIL_FOLDER']
    return send_from_directory(app.config['THUMBNAIL_RECEIPT_FOLDER'], filename=filename)


@main.route("/payment/data/receipts/<string:filename>", methods=['GET'])
def get_receipts_file(filename):
    print "获取上传文件：",filename
    return send_from_directory(os.path.join(app.config['UPLOADED_RECEIPT_FOLDER']), filename=filename)




'''合同结算'''
@main.route('/payment/contract_accountant',methods = ['GET','POST'])
@login_required
def contract_accountant():
    conn = MySQLdb.connect("localhost","root","uroot012","erp_development",charset='utf8')

    cursor = conn.cursor()

    '''
        从订单获取日期 税种
        由合同号获取送货单编号，获取型号 单价 数量 合同金额
    '''
    #获取payment中所有订单号
    cursor.execute("SELECT order_number,company_name,tax_type,order_date from orders ORDER BY id")
    delivery_no = cursor.fetchall()
    for no in set(delivery_no):
	print 'no',no
	print('number',no[0],'client',no[1])
	#Payment.query.filter_by(no=delivery_no).update({'received_payment':received_payment})
	cursor.execute("INSERT INTO   contract_accountant(purchase_order,client_name,tax_type,order_date) VALUES('%s','%s','%s','%s')"%(no[0],no[1],no[2],no[3]))
	conn.commit()


        #cursor.execute("SELECT order_date from orders where order_number='%s'"%order[0])
        #print("SELECT production_name1  from delivery_%s"%no[0])
        #cursor.execute("SELECT production_name1  from delivery_%s"%no[0])
        #pro_mess = cursor.fetchall()
        #print('pro_mess',no,pro_mess[0])
   







    return render_template('payment/contract_accountant.html')





@main.route('/payment/contract_accountant/return_json',methods = ['GET','POST'])
@login_required
def contract_accountant_return_json():
        app = current_app._get_current_object()
        try:
            '''warning:这里需要设置为环境获取'''
            db = MySQLdb.connect("localhost","root","uroot012","erp_development",charset='utf8')
            cursor = db.cursor()
        except:
            print 'MySQL connect fail...'
        cursor.execute("SELECT * from contract_accountant")
        data = cursor.fetchall()
        cursor.close()

        db.close()
        jsonData = []

        for n,row  in enumerate(data):
            print data[0]
            ##print row[1]
            result = {}
            result['order_date'] = row[0]
	    result['purchase_order'] = row[1]
	    result['client_name'] = row[2]
	    result['product_type'] = row[3]
	    result['product_price'] = row[4]
	    result['product_num'] = row[5]
	    result['tax_type'] = row[6]
	    result['order_amount'] = row[7]
	    result['tem_cost'] = row[8]
	    result['server_cost'] = row[9]
	    result['tax'] = row[10]
	    result['consult_cost'] = row[11]
	    result['after_sales'] = row[12]
	    result['profit'] = row[13]

            jsonData.append(result)

        return json.dumps(jsonData)

