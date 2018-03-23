# -*- coding:utf-8 -*-
__author__ = 'xuan'

from flask import render_template,request,current_app,redirect,url_for,send_from_directory
from  . import  main
from flask.ext.login import login_required,current_user,login_user,logout_user
import json,MySQLdb,sys
from  manage import  db  #不添加这个会不能更新数据库
from ..models import Orders,Production_Orders,Delivery_which_in,Delivery_Orders,Delivery_Productions,Payment,Receipts,Reimbursement,ContractAccountant,Contract,PayRequest
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

    purchase_order = request.form.get('row[purchase_order]', '')
    freight = request.form.get('row[freight]', '')
    after_sales = request.form.get('row[after_sales]', '')

    '''修改记录'''
    if purchase_order != '':       
        ContractAccountant.query.filter_by(purchase_order=purchase_order).update({"freight":freight,"after_sales":after_sales})
        
	#计算 利润=合同金额-税金-终端成本-服务器成本-配件成本-软件成本-报销费用-杂费-运费-得利税
	order_amount = ContractAccountant.query.filter_by(purchase_order=purchase_order).first().order_amount
	tax = ContractAccountant.query.filter_by(purchase_order=purchase_order).first().tax
	tem_cost = ContractAccountant.query.filter_by(purchase_order=purchase_order).first().tem_cost	
	servers_cost = ContractAccountant.query.filter_by(purchase_order=purchase_order).first().servers_cost
	fittings_cost = ContractAccountant.query.filter_by(purchase_order=purchase_order).first().fittings_cost
	softwares_cost = ContractAccountant.query.filter_by(purchase_order=purchase_order).first().softwares_cost
	reimbursement = ContractAccountant.query.filter_by(purchase_order=purchase_order).first().reimbursement
	consult_cost = ContractAccountant.query.filter_by(purchase_order=purchase_order).first().consult_cost
	freight = float(freight)
	after_sales = float(after_sales)

	print('计算 利润')
	profit = order_amount-tax-tem_cost-servers_cost-fittings_cost-softwares_cost-reimbursement-consult_cost-freight-after_sales
	
        ContractAccountant.query.filter_by(purchase_order=purchase_order).update(
                    {"profit":profit })
	    
	db.session.commit()


    try:
        '''warning:这里需要设置为环境获取'''
        database = MySQLdb.connect("localhost", "root", "uroot012", "erp_development", charset='utf8')
        cursor = database.cursor()
    except:
        print 'MySQL connect fail...'

    get_product_data = request.form.get('get_product_order_data', '')
    if any(get_product_data):
        product_purchase_order = json.loads(get_product_data)["purchase_order"]       

        '''
            由合同号从送货单中获取产品型号 单价 数量 合同金额
        '''
        cursor.execute("SELECT no from delivery_orders where purchase_order='%s'"%(product_purchase_order))
        
	delivery_orders = cursor.fetchall()
	print(delivery_orders)

	pro_mes_all = []
	for order in delivery_orders:
	    print('order',order[0])

	    cursor.execute("SELECT production_name1,nums1,unit1,unit_price1,remarks1 from delivery_%s"%(order[0]))	
	    pro_mes_one = cursor.fetchall()

	    cursor.execute("SELECT production_name2,nums2,unit2,unit_price2,remarks2 from delivery_%s"%(order[0]))	
	    pro_mes_two = cursor.fetchall()

	    cursor.execute("SELECT production_name3, nums3, unit3, unit_price3,remarks3  from delivery_%s"%(order[0]))	
	    pro_mes_three = cursor.fetchall()

	    cursor.execute("SELECT production_name4, nums4, unit4, unit_price4,remarks4 from delivery_%s"%(order[0]))	
	    pro_mes_four = cursor.fetchall()

	    cursor.execute("SELECT production_name5, nums5, unit5, unit_price5,remarks5 from delivery_%s"%(order[0]))	
	    pro_mes_five = cursor.fetchall()

	    cursor.execute("SELECT production_name6, nums6,unit6, unit_price6,remarks6 from delivery_%s"%(order[0]))
	    pro_mes_six = cursor.fetchall()
	
	    pro_mes = []
	    if pro_mes_one[0][0] != '':		
	        pro_mes.append(pro_mes_one[0])
	    	pro_mes.append('\n')
	    if pro_mes_two[0][0] != '':
	        pro_mes.append(pro_mes_two[0])
	    	pro_mes.append('\n')
	    if pro_mes_three[0][0] != '':
	        pro_mes.append(pro_mes_three[0])
	    	pro_mes.append('\n')
	    if pro_mes_four[0][0] != '':
	        pro_mes.append(pro_mes_four[0])
	    	pro_mes.append('\n')
	    if pro_mes_five[0][0] != '':
	        pro_mes.append(pro_mes_five[0])
	    	pro_mes.append('\n')
	    if pro_mes_six[0][0] != '':
		print('pro_mes_six')
		print(pro_mes_six[0][0])
	        pro_mes.append(pro_mes_six[0])
	    	pro_mes.append('\n')
	    
	    pro_mes_all.append(pro_mes)

	    cursor.execute("SELECT amount1,amount2,amount3,amount4,amount5,amount6 from delivery_%s"%(order[0]))
	    amount = cursor.fetchall()


	return simplejson.dumps({"pro_mes": pro_mes_all})

    get_tem_data = request.form.get('get_tem_order_data', '')

    get_tem_all = []
    if any(get_tem_data):
        tem_purchase_order = json.loads(get_tem_data)["purchase_order"] 
		
	cursor.execute("SELECT model,nums,product_price,memory_price,harddisk_price,wireless_price from production_orders where order_number='%s'"%(tem_purchase_order))
	tem_cost_mes = cursor.fetchall()
	
	for cost in tem_cost_mes:
	    get_tem_all.append(cost)
	    get_tem_all.append('\n')


    	return simplejson.dumps({"tem_mes": get_tem_all})


    remove_order = request.form.get('remove_order[]', '')
    


    '''删除合同结算记录'''
    if remove_order != " ":
	print('remove_orderremove_order',remove_order)	

	cursor.execute("delete from contract_accountant where purchase_order='%s' "%(remove_order))
	cursor.execute("delete from reimbursement where purchase_order='%s' "%(remove_order))
	cursor.execute("delete from payrequest where purchase_order='%s' "%(remove_order))
      
        cursor.close()
        database.commit()
        database.close()


    if request.method == 'POST':
    	get_purchase_order_data = request.form.get('get_purchase_order_data', '')

        if get_purchase_order_data != '':
            # 根据返回的number查找contract中的文件名
            if Contract.query.filter_by(number=json.loads(get_purchase_order_data)["purchase_order"]).first() is not None:
                filename = Contract.query.filter_by(number=json.loads(get_purchase_order_data)["purchase_order"]).first().name
            else:
                filename = ''

            print '返回json ', filename

            return simplejson.dumps({"filename": filename})
        else:
            return simplejson.dumps({"filename": ''})
    else:
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
            result = {}
            result['order_date'] = row[0]
	    result['purchase_order'] = row[1]
	    result['client_name'] = row[2]
	    result['tax_type'] = row[3]
	    result['order_amount'] = row[4]
	    result['tem_cost'] = row[5]
	    result['fittings_cost'] = row[6]
 	    result['softwares_cost'] = row[7]
	    result['reimbursement'] = row[8]
	    result['tax'] = row[9]
	    result['consult_cost'] = row[10]
	    result['after_sales'] = row[11] 
	    result['profit'] = row[12]
	    result['freight'] = row[13]
	    result['servers_cost'] = row[14]

            jsonData.append(result)

        return json.dumps(jsonData)



'''服务器成本'''
@main.route('/payment/server_cost',methods = ['GET','POST'])
@login_required
def server_cost():

    check_order = request.args.get("in")
  
    if check_order is not None:
        try:
            '''warning:这里需要设置为环境获取'''
            database = MySQLdb.connect("localhost", "root", "uroot012", "erp_development", charset='utf8')
            cursor = database.cursor()
        except:
            print 'MySQL connect fail...'

        cursor.execute("SELECT * from server_cost where purchase_order='%s' "%(check_order))
        data = cursor.fetchall()

        jsonData = []
	
	if any(data):
            for n, row in enumerate(data):
        	result = {}
        	result['id'] = row[0]
        	result['server1'] = row[1]
        	result['num1'] = row[2]
                result['unit1'] = row[3]
                result['unit_price1'] = row[4]
                result['remarks1'] = row[5]
                result['server2'] = row[6]
                result['num2'] = row[7]
                result['unit2'] = row[8]
                result['unit_price2'] = row[9]
                result['remarks2'] = row[10]       
                result['server3'] = row[11]
        	result['num3'] = row[12]
        	result['unit3'] = row[13]
        	result['unit_price3'] = row[14]
        	result['remarks3'] = row[15] 
        	result['server4'] = row[16]
        	result['num4'] = row[17]
        	result['unit4'] = row[18]
        	result['unit_price4'] = row[19]
        	result['remarks4'] = row[20]    
	    	result['server5'] = row[21]
        	result['num5'] = row[22]
        	result['unit5'] = row[23]
        	result['unit_price5'] = row[24]
        	result['remarks5'] = row[25] 
        	result['server6'] = row[26]
        	result['num6'] = row[27]
        	result['unit6'] = row[28]
        	result['unit_price6'] = row[29]
        	result['remarks6'] = row[30] 
        	result['server7'] = row[31]
        	result['num7'] = row[32]
        	result['unit7'] = row[33]
        	result['unit_price7'] = row[34]
        	result['remarks7'] = row[35] 
        	result['server8'] = row[36]
        	result['num8'] = row[37]
        	result['unit8'] = row[38]
        	result['unit_price8'] = row[39]
        	result['remarks8'] = row[40] 
        	result['server9'] = row[41]
        	result['num9'] = row[42]
        	result['unit9'] = row[43]
        	result['unit_price9'] = row[44]
        	result['remarks9'] = row[45] 
        	result['server10'] = row[46]
        	result['num10'] = row[47]
        	result['unit10'] = row[48]
        	result['unit_price10'] = row[49]
        	result['remarks10'] = row[50] 
	    	result['purcharse_order'] = row[51]
       		result['server11'] = row[52]
         	result['num11'] = row[53]
            	result['unit11'] = row[54]
            	result['unit_price11'] = row[55]
            	result['remarks11'] = row[56] 
            	result['server12'] = row[57]
            	result['num12'] = row[58]
            	result['unit12'] = row[59]
            	result['unit_price12'] = row[60]
            	result['remarks12'] = row[61] 
	
	    	jsonData.append(result)

            server1 = jsonData[0]['server1']
            nums1 = jsonData[0]['num1']
	    if nums1 == 0:
		nums1 = ' '
            unit1 = jsonData[0]['unit1']
            unit_price1 = jsonData[0]['unit_price1']
	    if unit_price1 == 0:
		unit_price1 = ' '
            remarks1 = jsonData[0]['remarks1']

            server2 = jsonData[0]['server2']
            nums2 = jsonData[0]['num2']
	    if nums2 == 0:
		nums2 = ' '
            unit2 = jsonData[0]['unit2']
            unit_price2 = jsonData[0]['unit_price2']
	    if unit_price2 == 0:
		unit_price2 = ' '
            remarks2 = jsonData[0]['remarks2']

            server3 = jsonData[0]['server3']
            nums3 = jsonData[0]['num3']
	    if nums3 == 0:
		nums3 = ' '
            unit3 = jsonData[0]['unit3']
            unit_price3 = jsonData[0]['unit_price3']
	    if unit_price3 == 0:
		unit_price3 = ' '
            remarks3 = jsonData[0]['remarks3']

            server4 = jsonData[0]['server4']
            nums4 = jsonData[0]['num4']
	    if nums4 == 0:
		nums4 = ' '
            unit4 = jsonData[0]['unit4']
            unit_price4 = jsonData[0]['unit_price4']
	    if unit_price4 == 0:
		unit_price4 = ' '
            remarks4 = jsonData[0]['remarks4']

            server5 = jsonData[0]['server5']
            nums5 = jsonData[0]['num5']
	    if nums5 == 0:
		nums5 = ' '
            unit5 = jsonData[0]['unit5']
            unit_price5 = jsonData[0]['unit_price5']
	    if unit_price5 == 0:
		unit_price5 = ' '
            remarks5 = jsonData[0]['remarks5']

            server6 = jsonData[0]['server6']
            nums6 = jsonData[0]['num6']
	    if nums6 == 0:
		nums6 = ' '
            unit6 = jsonData[0]['unit6']
            unit_price6 = jsonData[0]['unit_price6']
	    if unit_price6 == 0:
		unit_price6 = ' '
            remarks6 = jsonData[0]['remarks6']

            server7 = jsonData[0]['server7']
            nums7 = jsonData[0]['num7']
	    if nums7 == 0:
		nums7 = ' '
            unit7 = jsonData[0]['unit7']
            unit_price7 = jsonData[0]['unit_price7']
	    if unit_price7 == 0:
		unit_price7 = ' '
            remarks7 = jsonData[0]['remarks7']

            server8 = jsonData[0]['server8']
            nums8 = jsonData[0]['num8']
	    if nums8 == 0:
		nums8 = ' '
            unit8 = jsonData[0]['unit8']
            unit_price8 = jsonData[0]['unit_price8']
	    if unit_price8 == 0:
		unit_price8 = ' '
            remarks8 = jsonData[0]['remarks8']

            server9 = jsonData[0]['server9']
            nums9 = jsonData[0]['num9']
	    if nums9 == 0:
		nums9 = ' '
            unit9 = jsonData[0]['unit9']
            unit_price9 = jsonData[0]['unit_price9']
	    if unit_price9 == 0:
		unit_price9 = ' '
            remarks9 = jsonData[0]['remarks9']

            server10 = jsonData[0]['server10']
            nums10 = jsonData[0]['num10']
	    if nums10 == 0:
		nums10 = ' '
            unit10 = jsonData[0]['unit10']
            unit_price10 = jsonData[0]['unit_price10']
	    if unit_price10 == 0:
		unit_price10 = ' '
            remarks10 = jsonData[0]['remarks10']

            server11 = jsonData[0]['server11']
            nums11 = jsonData[0]['num11']
	    if nums11 == 0:
		nums11 = ' '
            unit11 = jsonData[0]['unit11']
            unit_price11 = jsonData[0]['unit_price11']
	    if unit_price11 == 0:
		unit_price11 = ' '
            remarks11 = jsonData[0]['remarks11']

            server12 = jsonData[0]['server12']
            nums12 = jsonData[0]['num12']
	    if nums12 == 0:
		nums12 = ' '
            unit12 = jsonData[0]['unit12']
            unit_price12 = jsonData[0]['unit_price12']
	    if unit_price12 == 0:
		unit_price12 = ' '
            remarks12 = jsonData[0]['remarks12']
	else:
	    print('不存在')
            server1 = ''
            nums1 = ' '
            unit1 = ''
            unit_price1 = ' '
            remarks1 = ''

            server2 = ''
            nums2 = ' '
            unit2 = ''
            unit_price2 = ' '
            remarks2 = ''

            server3 = ''
            nums3 = ' '
            unit3 = ''
            unit_price3 = ' '
            remarks3 = ''

            server4 = ''
            nums4 = ' '
            unit4 = ''
            unit_price4 = ' '
            remarks4 = ''

            server5 = ''
            nums5 = ' '
            unit5 = ''
            unit_price5 = ' '
            remarks5 = ''

            server6 = ''
            nums6 = ' '
            unit6 = ''
            unit_price6 = ' '
            remarks6 = ''

            server7 = ''
            nums7 = ' '
            unit7 = ''
            unit_price7 = ' '
            remarks7 = ''

            server8 = ''
            nums8 = ''
            unit8 = ''
            unit_price8 = ''
            remarks8 = ''

            server9 = ''
            nums9 = ' '
            unit9 = ''
            unit_price9 = ' '
            remarks9 = ''

            server10 = ''
            nums10 = ' '
            unit10 = ''
            unit_price10 = ' '
            remarks10 = ''

            server11 = ''
            nums11 = ' '
            unit11 = ''
            unit_price11 = ' '
            remarks11 = ''

            server12 = ''
            nums12 = ' '
            unit12 = ''
            unit_price12 = ' '
            remarks12 = ''

	    if  ContractAccountant.query.filter_by(purchase_order=check_order).first() is not None:
                print('当对应订单在合同结算表中存在时才insert server_cost ')
                cursor.execute("INSERT INTO server_cost(server1,num1,unit1,unit_price1,remarks1,server2,num2,unit2,unit_price2,remarks2,server3,num3,unit3,unit_price3,remarks3,server4,num4,unit4,unit_price4,remarks4, server5,num5,unit5,unit_price5,remarks5,server6,num6,unit6,unit_price6,remarks6,server7,num7,unit7,unit_price7,remarks7,server8,num8,unit8,unit_price8,remarks8,   server9,num9,unit9,unit_price9,remarks9,server10,num10,unit10,unit_price10,remarks10,server11,num11,unit11,unit_price11,remarks11,server12,num12,unit12,unit_price12,remarks12,purchase_order) VALUE ('%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s')"%(server1,nums1,unit1,unit_price1,remarks1,server2,nums2,unit2,unit_price2,remarks2,server3,nums3,unit3,unit_price3,remarks3,server4,nums4,unit4,unit_price4,remarks4, server5,nums5,unit5,unit_price5,remarks5,server6,nums6,unit6,unit_price6,remarks6,server7,nums7,unit7,unit_price7,remarks7,server8,nums8,unit8,unit_price8,remarks8,   server9,nums9,unit9,unit_price9,remarks9,server10,nums10,unit10,unit_price10,remarks10,server11,nums11,unit11,unit_price11,remarks11,server12,nums12,unit12,unit_price12,remarks12,check_order))
	
	        database.commit()
	    else:
	        return redirect(url_for('main.contract_accountant'))
    else:
	return redirect(url_for('main.contract_accountant'))

    # 接收表单传回的信息
    if request.method == 'POST':

	try:
            '''warning:这里需要设置为环境获取'''
            database = MySQLdb.connect("localhost", "root", "uroot012", "erp_development", charset='utf8')
            cursor = database.cursor()
        except:
            print 'MySQL connect fail...'


        if "server1" in request.form:
            server1 = request.form['server1']
        else:
            server1 = ""
        if "num1" in request.form:
            nums1 = request.form['num1']
            if nums1 == '':
                nums1 = ' '

        if "unit1" in request.form:
            unit1 = request.form['unit1']
        else:
            unit1 = ""
        if "unit_price1" in request.form:
            unit_price1 = request.form['unit_price1']
            if unit_price1 == '': 
                unit_price1 = ' '

        if "remark1" in request.form:
            remarks1 = request.form['remark1']
        else:
            remarks1 = ""	



        if "server2" in request.form:
            server2 = request.form['server2']
        else:
            server2 = ""
        if "num2" in request.form:
            nums2 = request.form['num2']
            if nums2 == '':
                nums2 = ' '
        if "unit2" in request.form:
            unit2 = request.form['unit2']
        else:
            unit2 = ""
        if "unit_price2" in request.form:
            unit_price2 = request.form['unit_price2']
            if unit_price2 == '': 
                unit_price2 = ' '

        if "remark2" in request.form:
            remarks2 = request.form['remark2']
        else:
            remarks2 = ""



        if "server3" in request.form:
            server3 = request.form['server3']
        else:
            server3 = ""
        if "num3" in request.form:
            nums3 = request.form['num3']
            if nums3 == '':
                nums3 = ' '

        if "unit3" in request.form:
            unit3 = request.form['unit3']
        else:
            unit3 = ""
        if "unit_price3" in request.form:
            unit_price3 = request.form['unit_price3']
            if unit_price3 == '': 
                unit_price3 = ' '
        if "remark3" in request.form:
            remarks3 = request.form['remark3']
        else:
            remarks3 = ""


        if "server4" in request.form:
            server4 = request.form['server4']
        else:
            server4 = ""
        if "num4" in request.form:
            nums4 = request.form['num4']
            if nums4 == '':
                nums4 = ' '

        if "unit4" in request.form:
            unit4 = request.form['unit4']
        else:
            unit4 = ""
        if "unit_price4" in request.form:
            unit_price4 = request.form['unit_price4']
            if unit_price4 == '': 
                unit_price4 = ' '
        if "remark4" in request.form:
            remarks4 = request.form['remark4']
        else:
            remarks4 = ""


        if "server5" in request.form:
            server5 = request.form['server5']
        else:
            server5 = ""
        if "num5" in request.form:
            nums5 = request.form['num5']
            if nums5 == '':
                nums5 = ' '

        if "unit5" in request.form:
            unit5 = request.form['unit5']
        else:
            unit5 = ""
        if "unit_price5" in request.form:
            unit_price5 = request.form['unit_price5']
            if unit_price5 == '': 
                unit_price5 = ' '
        if "remark5" in request.form:
            remarks5 = request.form['remark5']
        else:
            remarks5 = ""


        if "server6" in request.form:
            server6 = request.form['server6']
        else:
            server6 = ""
        if "num6" in request.form:
            nums6 = request.form['num6']
            if nums6 == '':
                nums6 = ' '

        if "unit6" in request.form:
            unit6 = request.form['unit6']
        else:
            unit6 = ""
        if "unit_price6" in request.form:
            unit_price6 = request.form['unit_price6']
            if unit_price6 == '': 
                unit_price6 = ' '
        if "remark6" in request.form:
            remarks6 = request.form['remark6']
        else:
            remarks6 = ""


        if "server7" in request.form:
            server7 = request.form['server7']
        else:
            server7 = ""
        if "num7" in request.form:
            nums7 = request.form['num7']
            if nums7 == '':
                nums7 = ' '

        if "unit7" in request.form:
            unit7 = request.form['unit7']
        else:
            unit7 = ""
        if "unit_price7" in request.form:
            unit_price7 = request.form['unit_price7']
            if unit_price7 == '': 
                unit_price7 = ' '
        if "remark7" in request.form:
            remarks7 = request.form['remark7']
        else:
            remarks7 = ""


        if "server8" in request.form:
            server8 = request.form['server8']
        else:
            server8 = ""
	if "num8" in request.form:
            nums8 = request.form['num8']
            if nums8 == '':
                nums8 = ' '

        if "unit8" in request.form:
            unit8 = request.form['unit8']
        else:
            unit8 = ""
        if "unit_price8" in request.form:
            unit_price8 = request.form['unit_price8']
            if unit_price8 == '': 
                unit_price8 = ' '
        if "remark8" in request.form:
            remarks8 = request.form['remark8']
        else:
            remarks8 = ""


        if "server9" in request.form:
            server9 = request.form['server9']
        else:
            server9 = ""
        if "num9" in request.form:
            nums9 = request.form['num9']
            if nums9 == '':
                nums9 = ' '

        if "unit9" in request.form:
            unit9 = request.form['unit9']
        else:
            unit9 = ""
        if "unit_price9" in request.form:
            unit_price9 = request.form['unit_price9']
            if unit_price9 == '': 
                unit_price9 = ' '

        if "remark9" in request.form:
            remarks9 = request.form['remark9']
        else:
            remarks9 = ""


        if "server10" in request.form:
            server10 = request.form['server10']
        else:
            server10 = ""
        if "num10" in request.form:
            nums10 = request.form['num10']
            if nums10 == '':
                nums10 = ' '

        if "unit10" in request.form:
            unit10 = request.form['unit10']
        else:
            unit10 = ""
        if "unit_price10" in request.form:
            unit_price10 = request.form['unit_price10']
            if unit_price10 == '': 
                unit_price10 = ' '

        if "remark10" in request.form:
            remarks10 = request.form['remark10']
        else:
            remarks10 = ""


        if "server11" in request.form:
            server11= request.form['server11']
        else:
            server11 = ""
        if "num11" in request.form:
            nums11 = request.form['num11']
            if nums11 == '':
                nums11 = ' '

        if "unit11" in request.form:
            unit11 = request.form['unit11']
        else:
            unit11 = ""
        if "unit_price11" in request.form:
            unit_price11 = request.form['unit_price11']
            if unit_price11 == '': 
                unit_price11 = ' '
        if "remark11" in request.form:
            remarks11 = request.form['remark11']
        else:
            remarks11 = ""


        if "server12" in request.form:
            server12 = request.form['server12']
        else:
            server12 = ""
        if "num12" in request.form:
            nums12 = request.form['num12']
            if nums12 == '':
                nums12 = ' '

        if "unit12" in request.form:
            unit12 = request.form['unit12']
        else:
            unit12 = ""
        if "unit_price12" in request.form:
            unit_price12 = request.form['unit_price12']
            if unit_price12 == '': 
                unit_price12 = ' '
        if "remark12" in request.form:
            remarks12 = request.form['remark12']
        else:
            remarks12 = ""

        print('更新数据表')
        
	cursor.execute("UPDATE server_cost SET server1='%s',num1='%s',unit1='%s',unit_price1='%s',remarks1='%s',server2='%s',num2='%s',unit2='%s',unit_price2='%s',remarks2='%s',server3='%s',num3='%s',unit3='%s',unit_price3='%s',remarks3='%s',server4='%s',num4='%s',unit4='%s',unit_price4='%s',remarks4='%s', server5='%s',num5='%s',unit5='%s',unit_price5='%s',remarks5='%s',server6='%s',num6='%s',unit6='%s',unit_price6='%s',remarks6='%s',server7='%s',num7='%s',unit7='%s',unit_price7='%s',remarks7='%s',server8='%s',num8='%s',unit8='%s',unit_price8='%s',remarks8='%s',   server9='%s',num9='%s',unit9='%s',unit_price9='%s',remarks9='%s',server10='%s',num10='%s',unit10='%s',unit_price10='%s',remarks10='%s',server11='%s',num11='%s',unit11='%s',unit_price11='%s',remarks11='%s',server12='%s',num12='%s',unit12='%s',unit_price12='%s',remarks12='%s' where purchase_order='%s'"%(server1,nums1,unit1,unit_price1,remarks1,server2,nums2,unit2,unit_price2,remarks2,server3,nums3,unit3,unit_price3,remarks3,server4,nums4,unit4,unit_price4,remarks4, server5,nums5,unit5,unit_price5,remarks5,server6,nums6,unit6,unit_price6,remarks6,server7,nums7,unit7,unit_price7,remarks7,server8,nums8,unit8,unit_price8,remarks8,   server9,nums9,unit9,unit_price9,remarks9,server10,nums10,unit10,unit_price10,remarks10,server11,nums11,unit11,unit_price11,remarks11,server12,nums12,unit12,unit_price12,remarks12,check_order))
	

        ''' 更新结算表上的服务器成本 '''
	nums = [nums1,nums2,nums3,nums4,nums5,nums6,nums7,nums8,nums9,nums10,nums11,nums12]
	nums2int = []
	for num in nums:
	    if num != ' ':
	        nums2int.append(int(num))
	    else:
	   	nums2int.append(0)
	unit_price =[unit_price1,unit_price2,unit_price3,unit_price4,unit_price5,unit_price6,unit_price7,unit_price8,unit_price9,unit_price10,unit_price11,unit_price12]
	price2float = []

	for price in unit_price:
	    if price != ' ':
	        price2float.append(float(price))
	    else:
		price2float.append(0.0)

	def cost_sum(nums,prices):	    
	    server_cost = map(lambda (a,b):a*b, zip(nums,prices))
	    return sum(server_cost)

        cursor.execute("UPDATE contract_accountant SET servers_cost='%s' where purchase_order='%s'"%(cost_sum(nums2int,price2float),check_order))
	
        database.commit()
        database.close()

	#计算 利润=合同金额-税金-终端成本-服务器成本-配件成本-软件成本-报销费用-杂费-运费-得利税
	order_amount = ContractAccountant.query.filter_by(purchase_order=check_order).first().order_amount
	tax = ContractAccountant.query.filter_by(purchase_order=check_order).first().tax
	tem_cost = ContractAccountant.query.filter_by(purchase_order=check_order).first().tem_cost	
	servers_cost = cost_sum(nums2int,price2float)
	fittings_cost = ContractAccountant.query.filter_by(purchase_order=check_order).first().fittings_cost
	softwares_cost = ContractAccountant.query.filter_by(purchase_order=check_order).first().softwares_cost
	reimbursement = ContractAccountant.query.filter_by(purchase_order=check_order).first().reimbursement
	consult_cost = ContractAccountant.query.filter_by(purchase_order=check_order).first().consult_cost
	freight = ContractAccountant.query.filter_by(purchase_order=check_order).first().freight
	after_sales = ContractAccountant.query.filter_by(purchase_order=check_order).first().after_sales

	print('计算 利润')
	profit = order_amount-tax-tem_cost-servers_cost-fittings_cost-softwares_cost-reimbursement-consult_cost-freight-after_sales

        ContractAccountant.query.filter_by(purchase_order=check_order).update(
                    {"profit":profit })

	db.session.commit()


    return render_template('payment/server_cost.html',server1=server1,num1=nums1,unit1=unit1,unit_price1=unit_price1,remark1=remarks1,
				                      server2=server2,num2=nums2,unit2=unit2,unit_price2=unit_price2,remark2=remarks2,
					              server3=server3,num3=nums3,unit3=unit3,unit_price3=unit_price3,remark3=remarks3,
						      server4=server4,num4=nums4,unit4=unit4,unit_price4=unit_price4,remark4=remarks4,
						      server5=server5,num5=nums5,unit5=unit5,unit_price5=unit_price5,remark5=remarks5,
						      server6=server6,num6=nums6,unit6=unit6,unit_price6=unit_price6,remark6=remarks6,
			 	 		      server7=server7,num7=nums7,unit7=unit7,unit_price7=unit_price7,remark7=remarks7,
						      server8=server8,num8=nums8,unit8=unit8,unit_price8=unit_price8,remark8=remarks8,
					 	      server9=server9,num9=nums9,unit9=unit9,unit_price9=unit_price9,remark9=remarks9,
					  	      server10=server10,num10=nums10,unit10=unit10,unit_price10=unit_price10,remark10=remarks10,
						      server11=server11,num11=nums11,unit11=unit11,unit_price11=unit_price11,remark11=remarks11,
				      		      server12=server12,num12=nums12,unit12=unit12,unit_price12=unit_price12,remark12=remarks12)



'''配件成本'''
@main.route('/payment/fittings_cost',methods = ['GET','POST'])
@login_required
def fittings_cost():

    check_order = request.args.get("in")
  
    if check_order is not None:
        try:
            '''warning:这里需要设置为环境获取'''
            database = MySQLdb.connect("localhost", "root", "uroot012", "erp_development", charset='utf8')
            cursor = database.cursor()
        except:
            print 'MySQL connect fail...'

        cursor.execute("SELECT * from fitting_cost where purchase_order='%s' "%(check_order))
        data = cursor.fetchall()

        jsonData = []
	
	if any(data):
            for n, row in enumerate(data):
        	result = {}
        	result['id'] = row[0]
        	result['fitting1'] = row[1]
        	result['num1'] = row[2]
                result['unit1'] = row[3]
                result['unit_price1'] = row[4]
                result['remarks1'] = row[5]
                result['fitting2'] = row[6]
                result['num2'] = row[7]
                result['unit2'] = row[8]
                result['unit_price2'] = row[9]
                result['remarks2'] = row[10]       
                result['fitting3'] = row[11]
        	result['num3'] = row[12]
        	result['unit3'] = row[13]
        	result['unit_price3'] = row[14]
        	result['remarks3'] = row[15] 
        	result['fitting4'] = row[16]
        	result['num4'] = row[17]
        	result['unit4'] = row[18]
        	result['unit_price4'] = row[19]
        	result['remarks4'] = row[20]    
	    	result['fitting5'] = row[21]
        	result['num5'] = row[22]
        	result['unit5'] = row[23]
        	result['unit_price5'] = row[24]
        	result['remarks5'] = row[25] 
        	result['fitting6'] = row[26]
        	result['num6'] = row[27]
        	result['unit6'] = row[28]
        	result['unit_price6'] = row[29]
        	result['remarks6'] = row[30] 
        	result['fitting7'] = row[31]
        	result['num7'] = row[32]
        	result['unit7'] = row[33]
        	result['unit_price7'] = row[34]
        	result['remarks7'] = row[35] 
        	result['fitting8'] = row[36]
        	result['num8'] = row[37]
        	result['unit8'] = row[38]
        	result['unit_price8'] = row[39]
        	result['remarks8'] = row[40] 
        	result['fitting9'] = row[41]
        	result['num9'] = row[42]
        	result['unit9'] = row[43]
        	result['unit_price9'] = row[44]
        	result['remarks9'] = row[45] 
        	result['fitting10'] = row[46]
        	result['num10'] = row[47]
        	result['unit10'] = row[48]
        	result['unit_price10'] = row[49]
        	result['remarks10'] = row[50] 
       		result['fitting11'] = row[51]
         	result['num11'] = row[52]
            	result['unit11'] = row[53]
            	result['unit_price11'] = row[54]
            	result['remarks11'] = row[55] 
            	result['fitting12'] = row[56]
            	result['num12'] = row[57]
            	result['unit12'] = row[58]
            	result['unit_price12'] = row[59]
            	result['remarks12'] = row[60] 
	  	result['purcharse_order'] = row[61]
	
	    	jsonData.append(result)

            fitting1 = jsonData[0]['fitting1']
            nums1 = jsonData[0]['num1']
	    if nums1 == 0:
		nums1 = ' '
            unit1 = jsonData[0]['unit1']
            unit_price1 = jsonData[0]['unit_price1']
	    if unit_price1 == 0:
		unit_price1 = ' '
            remarks1 = jsonData[0]['remarks1']

            fitting2 = jsonData[0]['fitting2']
            nums2 = jsonData[0]['num2']
	    if nums2 == 0:
		nums2 = ' '
            unit2 = jsonData[0]['unit2']
            unit_price2 = jsonData[0]['unit_price2']
	    if unit_price2 == 0:
		unit_price2 = ' '
            remarks2 = jsonData[0]['remarks2']

            fitting3 = jsonData[0]['fitting3']
            nums3 = jsonData[0]['num3']
	    if nums3 == 0:
		nums3 = ' '
            unit3 = jsonData[0]['unit3']
            unit_price3 = jsonData[0]['unit_price3']
	    if unit_price3 == 0:
		unit_price3 = ' '
            remarks3 = jsonData[0]['remarks3']

            fitting4 = jsonData[0]['fitting4']
            nums4 = jsonData[0]['num4']
	    if nums4 == 0:
		nums4 = ' '
            unit4 = jsonData[0]['unit4']
            unit_price4 = jsonData[0]['unit_price4']
	    if unit_price4 == 0:
		unit_price4 = ' '
            remarks4 = jsonData[0]['remarks4']

            fitting5 = jsonData[0]['fitting5']
            nums5 = jsonData[0]['num5']
	    if nums5 == 0:
		nums5 = ' '
            unit5 = jsonData[0]['unit5']
            unit_price5 = jsonData[0]['unit_price5']
	    if unit_price5 == 0:
		unit_price5 = ' '
            remarks5 = jsonData[0]['remarks5']

            fitting6 = jsonData[0]['fitting6']
            nums6 = jsonData[0]['num6']
	    if nums6 == 0:
		nums6 = ' '
            unit6 = jsonData[0]['unit6']
            unit_price6 = jsonData[0]['unit_price6']
	    if unit_price6 == 0:
		unit_price6 = ' '
            remarks6 = jsonData[0]['remarks6']

            fitting7 = jsonData[0]['fitting7']
            nums7 = jsonData[0]['num7']
	    if nums7 == 0:
		nums7 = ' '
            unit7 = jsonData[0]['unit7']
            unit_price7 = jsonData[0]['unit_price7']
	    if unit_price7 == 0:
		unit_price7 = ' '
            remarks7 = jsonData[0]['remarks7']

            fitting8 = jsonData[0]['fitting8']
            nums8 = jsonData[0]['num8']
	    if nums8 == 0:
		nums8 = ' '
            unit8 = jsonData[0]['unit8']
            unit_price8 = jsonData[0]['unit_price8']
	    if unit_price8 == 0:
		unit_price8 = ' '
            remarks8 = jsonData[0]['remarks8']

            fitting9 = jsonData[0]['fitting9']
            nums9 = jsonData[0]['num9']
	    if nums9 == 0:
		nums9 = ' '
            unit9 = jsonData[0]['unit9']
            unit_price9 = jsonData[0]['unit_price9']
	    if unit_price9 == 0:
		unit_price9 = ' '
            remarks9 = jsonData[0]['remarks9']

            fitting10 = jsonData[0]['fitting10']
            nums10 = jsonData[0]['num10']
	    if nums10 == 0:
		nums10 = ' '
            unit10 = jsonData[0]['unit10']
            unit_price10 = jsonData[0]['unit_price10']
	    if unit_price10 == 0:
		unit_price10 = ' '
            remarks10 = jsonData[0]['remarks10']

            fitting11 = jsonData[0]['fitting11']
            nums11 = jsonData[0]['num11']
	    if nums11 == 0:
		nums11 = ' '
            unit11 = jsonData[0]['unit11']
            unit_price11 = jsonData[0]['unit_price11']
	    if unit_price11 == 0:
		unit_price11 = ' '
            remarks11 = jsonData[0]['remarks11']

            fitting12 = jsonData[0]['fitting12']
            nums12 = jsonData[0]['num12']
	    if nums12 == 0:
		nums12 = ' '
            unit12 = jsonData[0]['unit12']
            unit_price12 = jsonData[0]['unit_price12']
	    if unit_price12 == 0:
		unit_price12 = ' '
            remarks12 = jsonData[0]['remarks12']
	else:
	    print('不存在')
            fitting1 = ''
            nums1 = ' '
            unit1 = ''
            unit_price1 = ' '
            remarks1 = ''

            fitting2 = ''
            nums2 = ' '
            unit2 = ''
            unit_price2 = ' '
            remarks2 = ''

            fitting3 = ''
            nums3 = ' '
            unit3 = ''
            unit_price3 = ' '
            remarks3 = ''

            fitting4 = ''
            nums4 = ' '
            unit4 = ''
            unit_price4 = ' '
            remarks4 = ''

            fitting5 = ''
            nums5 = ' '
            unit5 = ''
            unit_price5 = ' '
            remarks5 = ''

            fitting6 = ''
            nums6 = ' '
            unit6 = ''
            unit_price6 = ' '
            remarks6 = ''

            fitting7 = ''
            nums7 = ' '
            unit7 = ''
            unit_price7 = ' '
            remarks7 = ''

            fitting8 = ''
            nums8 = ''
            unit8 = ''
            unit_price8 = ''
            remarks8 = ''

            fitting9 = ''
            nums9 = ' '
            unit9 = ''
            unit_price9 = ' '
            remarks9 = ''

            fitting10 = ''
            nums10 = ' '
            unit10 = ''
            unit_price10 = ' '
            remarks10 = ''

            fitting11 = ''
            nums11 = ' '
            unit11 = ''
            unit_price11 = ' '
            remarks11 = ''

            fitting12 = ''
            nums12 = ' '
            unit12 = ''
            unit_price12 = ' '
            remarks12 = ''

	    if  ContractAccountant.query.filter_by(purchase_order=check_order).first() is not None:
                print('当对应订单在合同结算表中存在时才insert fitting_cost ')
                cursor.execute("INSERT INTO fitting_cost(fitting1,num1,unit1,unit_price1,remarks1,fitting2,num2,unit2,unit_price2,remarks2,fitting3,num3,unit3,unit_price3,remarks3,fitting4,num4,unit4,unit_price4,remarks4, fitting5,num5,unit5,unit_price5,remarks5,fitting6,num6,unit6,unit_price6,remarks6,fitting7,num7,unit7,unit_price7,remarks7,fitting8,num8,unit8,unit_price8,remarks8,   fitting9,num9,unit9,unit_price9,remarks9,fitting10,num10,unit10,unit_price10,remarks10,fitting11,num11,unit11,unit_price11,remarks11,fitting12,num12,unit12,unit_price12,remarks12,purchase_order) VALUE ('%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s')"%(fitting1,nums1,unit1,unit_price1,remarks1,fitting2,nums2,unit2,unit_price2,remarks2,fitting3,nums3,unit3,unit_price3,remarks3,fitting4,nums4,unit4,unit_price4,remarks4, fitting5,nums5,unit5,unit_price5,remarks5,fitting6,nums6,unit6,unit_price6,remarks6,fitting7,nums7,unit7,unit_price7,remarks7,fitting8,nums8,unit8,unit_price8,remarks8,   fitting9,nums9,unit9,unit_price9,remarks9,fitting10,nums10,unit10,unit_price10,remarks10,fitting11,nums11,unit11,unit_price11,remarks11,fitting12,nums12,unit12,unit_price12,remarks12,check_order))
	
	        database.commit()
            else:
		return redirect(url_for('main.contract_accountant'))


    else:
	return redirect(url_for('main.contract_accountant'))

    # 接收表单传回的信息
    if request.method == 'POST':

	try:
            '''warning:这里需要设置为环境获取'''
            database = MySQLdb.connect("localhost", "root", "uroot012", "erp_development", charset='utf8')
            cursor = database.cursor()
        except:
            print 'MySQL connect fail...'


        if "fitting1" in request.form:
            fitting1 = request.form['fitting1']
        else:
            fitting1 = ""
        if "num1" in request.form:
            nums1 = request.form['num1']
            if nums1 == '':
                nums1 = ' '

        if "unit1" in request.form:
            unit1 = request.form['unit1']
        else:
            unit1 = ""
        if "unit_price1" in request.form:
            unit_price1 = request.form['unit_price1']
            if unit_price1 == '': 
                unit_price1 = ' '

        if "remark1" in request.form:
            remarks1 = request.form['remark1']
        else:
            remarks1 = ""	

        if "fitting2" in request.form:
            fitting2 = request.form['fitting2']
        else:
            fitting2 = ""
        if "num2" in request.form:
            nums2 = request.form['num2']
            if nums2 == '':
                nums2 = ' '
        if "unit2" in request.form:
            unit2 = request.form['unit2']
        else:
            unit2 = ""
        if "unit_price2" in request.form:
            unit_price2 = request.form['unit_price2']
            if unit_price2 == '': 
                unit_price2 = ' '

        if "remark2" in request.form:
            remarks2 = request.form['remark2']
        else:
            remarks2 = ""



        if "fitting3" in request.form:
            fitting3 = request.form['fitting3']
        else:
            fitting3 = ""
        if "num3" in request.form:
            nums3 = request.form['num3']
            if nums3 == '':
                nums3 = ' '

        if "unit3" in request.form:
            unit3 = request.form['unit3']
        else:
            unit3 = ""
        if "unit_price3" in request.form:
            unit_price3 = request.form['unit_price3']
            if unit_price3 == '': 
                unit_price3 = ' '
        if "remark3" in request.form:
            remarks3 = request.form['remark3']
        else:
            remarks3 = ""


        if "fitting4" in request.form:
            fitting4 = request.form['fitting4']
        else:
            fitting4 = ""
        if "num4" in request.form:
            nums4 = request.form['num4']
            if nums4 == '':
                nums4 = ' '

        if "unit4" in request.form:
            unit4 = request.form['unit4']
        else:
            unit4 = ""
        if "unit_price4" in request.form:
            unit_price4 = request.form['unit_price4']
            if unit_price4 == '': 
                unit_price4 = ' '
        if "remark4" in request.form:
            remarks4 = request.form['remark4']
        else:
            remarks4 = ""


        if "fitting5" in request.form:
            fitting5 = request.form['fitting5']
        else:
            fitting5 = ""
        if "num5" in request.form:
            nums5 = request.form['num5']
            if nums5 == '':
                nums5 = ' '

        if "unit5" in request.form:
            unit5 = request.form['unit5']
        else:
            unit5 = ""
        if "unit_price5" in request.form:
            unit_price5 = request.form['unit_price5']
            if unit_price5 == '': 
                unit_price5 = ' '
        if "remark5" in request.form:
            remarks5 = request.form['remark5']
        else:
            remarks5 = ""


        if "fitting6" in request.form:
            fitting6 = request.form['fitting6']
        else:
            fitting6 = ""
        if "num6" in request.form:
            nums6 = request.form['num6']
            if nums6 == '':
                nums6 = ' '

        if "unit6" in request.form:
            unit6 = request.form['unit6']
        else:
            unit6 = ""
        if "unit_price6" in request.form:
            unit_price6 = request.form['unit_price6']
            if unit_price6 == '': 
                unit_price6 = ' '
        if "remark6" in request.form:
            remarks6 = request.form['remark6']
        else:
            remarks6 = ""


        if "fitting7" in request.form:
            fitting7 = request.form['fitting7']
        else:
            fitting7 = ""
        if "num7" in request.form:
            nums7 = request.form['num7']
            if nums7 == '':
                nums7 = ' '

        if "unit7" in request.form:
            unit7 = request.form['unit7']
        else:
            unit7 = ""
        if "unit_price7" in request.form:
            unit_price7 = request.form['unit_price7']
            if unit_price7 == '': 
                unit_price7 = ' '
        if "remark7" in request.form:
            remarks7 = request.form['remark7']
        else:
            remarks7 = ""


        if "fitting8" in request.form:
            fitting8 = request.form['fitting8']
        else:
            fitting8 = ""
	if "num8" in request.form:
            nums8 = request.form['num8']
            if nums8 == '':
                nums8 = ' '

        if "unit8" in request.form:
            unit8 = request.form['unit8']
        else:
            unit8 = ""
        if "unit_price8" in request.form:
            unit_price8 = request.form['unit_price8']
            if unit_price8 == '': 
                unit_price8 = ' '
        if "remark8" in request.form:
            remarks8 = request.form['remark8']
        else:
            remarks8 = ""


        if "fitting9" in request.form:
            fitting9 = request.form['fitting9']
        else:
            fitting9 = ""
        if "num9" in request.form:
            nums9 = request.form['num9']
            if nums9 == '':
                nums9 = ' '

        if "unit9" in request.form:
            unit9 = request.form['unit9']
        else:
            unit9 = ""
        if "unit_price9" in request.form:
            unit_price9 = request.form['unit_price9']
            if unit_price9 == '': 
                unit_price9 = ' '

        if "remark9" in request.form:
            remarks9 = request.form['remark9']
        else:
            remarks9 = ""


        if "fitting10" in request.form:
            fitting10 = request.form['fitting10']
        else:
            fitting10 = ""
        if "num10" in request.form:
            nums10 = request.form['num10']
            if nums10 == '':
                nums10 = ' '

        if "unit10" in request.form:
            unit10 = request.form['unit10']
        else:
            unit10 = ""
        if "unit_price10" in request.form:
            unit_price10 = request.form['unit_price10']
            if unit_price10 == '': 
                unit_price10 = ' '

        if "remark10" in request.form:
            remarks10 = request.form['remark10']
        else:
            remarks10 = ""


        if "fitting11" in request.form:
            fitting11= request.form['fitting11']
        else:
            fitting11 = ""
        if "num11" in request.form:
            nums11 = request.form['num11']
            if nums11 == '':
                nums11 = ' '

        if "unit11" in request.form:
            unit11 = request.form['unit11']
        else:
            unit11 = ""
        if "unit_price11" in request.form:
            unit_price11 = request.form['unit_price11']
            if unit_price11 == '': 
                unit_price11 = ' '
        if "remark11" in request.form:
            remarks11 = request.form['remark11']
        else:
            remarks11 = ""


        if "fitting12" in request.form:
            fitting12 = request.form['fitting12']
        else:
            fitting12 = ""
        if "num12" in request.form:
            nums12 = request.form['num12']
            if nums12 == '':
                nums12 = ' '

        if "unit12" in request.form:
            unit12 = request.form['unit12']
        else:
            unit12 = ""
        if "unit_price12" in request.form:
            unit_price12 = request.form['unit_price12']
            if unit_price12 == '': 
                unit_price12 = ' '
        if "remark12" in request.form:
            remarks12 = request.form['remark12']
        else:
            remarks12 = ""

        print('更新数据表')
        
	cursor.execute("UPDATE fitting_cost SET fitting1='%s',num1='%s',unit1='%s',unit_price1='%s',remarks1='%s',fitting2='%s',num2='%s',unit2='%s',unit_price2='%s',remarks2='%s',fitting3='%s',num3='%s',unit3='%s',unit_price3='%s',remarks3='%s',fitting4='%s',num4='%s',unit4='%s',unit_price4='%s',remarks4='%s', fitting5='%s',num5='%s',unit5='%s',unit_price5='%s',remarks5='%s',fitting6='%s',num6='%s',unit6='%s',unit_price6='%s',remarks6='%s',fitting7='%s',num7='%s',unit7='%s',unit_price7='%s',remarks7='%s',fitting8='%s',num8='%s',unit8='%s',unit_price8='%s',remarks8='%s',fitting9='%s',num9='%s',unit9='%s',unit_price9='%s',remarks9='%s',fitting10='%s',num10='%s',unit10='%s',unit_price10='%s',remarks10='%s',fitting11='%s',num11='%s',unit11='%s',unit_price11='%s',remarks11='%s',fitting12='%s',num12='%s',unit12='%s',unit_price12='%s',remarks12='%s' where purchase_order='%s'"%(fitting1,nums1,unit1,unit_price1,remarks1,fitting2,nums2,unit2,unit_price2,remarks2,fitting3,nums3,unit3,unit_price3,remarks3,fitting4,nums4,unit4,unit_price4,remarks4, fitting5,nums5,unit5,unit_price5,remarks5,fitting6,nums6,unit6,unit_price6,remarks6,fitting7,nums7,unit7,unit_price7,remarks7,fitting8,nums8,unit8,unit_price8,remarks8,   fitting9,nums9,unit9,unit_price9,remarks9,fitting10,nums10,unit10,unit_price10,remarks10,fitting11,nums11,unit11,unit_price11,remarks11,fitting12,nums12,unit12,unit_price12,remarks12,check_order))
	

        ''' 更新结算表上的配件成本 '''
	print('更新结算表上的配件成本')
	nums = [nums1,nums2,nums3,nums4,nums5,nums6,nums7,nums8,nums9,nums10,nums11,nums12]
	nums2int = []
	for num in nums:
	    if num != ' ':
	        nums2int.append(int(num))
	    else:
	   	nums2int.append(0)
	unit_price =[unit_price1,unit_price2,unit_price3,unit_price4,unit_price5,unit_price6,unit_price7,unit_price8,unit_price9,unit_price10,unit_price11,unit_price12]
	price2float = []

	for price in unit_price:
	    if price != ' ':
	        price2float.append(float(price))
	    else:
		price2float.append(0.0)

	def cost_sum(nums,prices):	    
	    fitting_cost = map(lambda (a,b):a*b, zip(nums,prices))
	    return sum(fitting_cost)

        cursor.execute("UPDATE contract_accountant SET fittings_cost='%s' where purchase_order='%s'"%(cost_sum(nums2int,price2float),check_order))

        database.commit()
        database.close()

	#计算 利润=合同金额-税金-终端成本-服务器成本-配件成本-软件成本-报销费用-杂费-运费-得利税
	order_amount = ContractAccountant.query.filter_by(purchase_order=check_order).first().order_amount
	tax = ContractAccountant.query.filter_by(purchase_order=check_order).first().tax
	tem_cost = ContractAccountant.query.filter_by(purchase_order=check_order).first().tem_cost	
	servers_cost = ContractAccountant.query.filter_by(purchase_order=check_order).first().servers_cost
	fittings_cost = cost_sum(nums2int,price2float)
	softwares_cost = ContractAccountant.query.filter_by(purchase_order=check_order).first().softwares_cost
	reimbursement = ContractAccountant.query.filter_by(purchase_order=check_order).first().reimbursement
	consult_cost = ContractAccountant.query.filter_by(purchase_order=check_order).first().consult_cost
	freight = ContractAccountant.query.filter_by(purchase_order=check_order).first().freight
	after_sales = ContractAccountant.query.filter_by(purchase_order=check_order).first().after_sales

	print('计算 利润')
	profit = order_amount-tax-tem_cost-servers_cost-fittings_cost-softwares_cost-reimbursement-consult_cost-freight-after_sales
        ContractAccountant.query.filter_by(purchase_order=check_order).update(
                    {"profit":profit })

	db.session.commit()




    return render_template('payment/fittings_cost.html',fitting1=fitting1,num1=nums1,unit1=unit1,unit_price1=unit_price1,remark1=remarks1,
				                      fitting2=fitting2,num2=nums2,unit2=unit2,unit_price2=unit_price2,remark2=remarks2,
					              fitting3=fitting3,num3=nums3,unit3=unit3,unit_price3=unit_price3,remark3=remarks3,
						      fitting4=fitting4,num4=nums4,unit4=unit4,unit_price4=unit_price4,remark4=remarks4,
						      fitting5=fitting5,num5=nums5,unit5=unit5,unit_price5=unit_price5,remark5=remarks5,
						      fitting6=fitting6,num6=nums6,unit6=unit6,unit_price6=unit_price6,remark6=remarks6,
			 	 		      fitting7=fitting7,num7=nums7,unit7=unit7,unit_price7=unit_price7,remark7=remarks7,
						      fitting8=fitting8,num8=nums8,unit8=unit8,unit_price8=unit_price8,remark8=remarks8,
					 	      fitting9=fitting9,num9=nums9,unit9=unit9,unit_price9=unit_price9,remark9=remarks9,
					  	      fitting10=fitting10,num10=nums10,unit10=unit10,unit_price10=unit_price10,remark10=remarks10,
						      fitting11=fitting11,num11=nums11,unit11=unit11,unit_price11=unit_price11,remark11=remarks11,
				      		      fitting12=fitting12,num12=nums12,unit12=unit12,unit_price12=unit_price12,remark12=remarks12)


'''软件成本'''
@main.route('/payment/softwares_cost',methods = ['GET','POST'])
@login_required
def softwares_cost():

    check_order = request.args.get("in")
  
    if check_order is not None:
        try:
            '''warning:这里需要设置为环境获取'''
            database = MySQLdb.connect("localhost", "root", "uroot012", "erp_development", charset='utf8')
            cursor = database.cursor()
        except:
            print 'MySQL connect fail...'

        cursor.execute("SELECT * from software_cost where purchase_order='%s' "%(check_order))
        data = cursor.fetchall()

        jsonData = []
	
	if any(data):
            for n, row in enumerate(data):
        	result = {}
        	result['id'] = row[0]
        	result['software1'] = row[1]
        	result['num1'] = row[2]
                result['unit1'] = row[3]
                result['unit_price1'] = row[4]
                result['remarks1'] = row[5]
                result['software2'] = row[6]
                result['num2'] = row[7]
                result['unit2'] = row[8]
                result['unit_price2'] = row[9]
                result['remarks2'] = row[10]       
                result['software3'] = row[11]
        	result['num3'] = row[12]
        	result['unit3'] = row[13]
        	result['unit_price3'] = row[14]
        	result['remarks3'] = row[15] 
        	result['software4'] = row[16]
        	result['num4'] = row[17]
        	result['unit4'] = row[18]
        	result['unit_price4'] = row[19]
        	result['remarks4'] = row[20]    
	    	result['software5'] = row[21]
        	result['num5'] = row[22]
        	result['unit5'] = row[23]
        	result['unit_price5'] = row[24]
        	result['remarks5'] = row[25] 
        	result['software6'] = row[26]
        	result['num6'] = row[27]
        	result['unit6'] = row[28]
        	result['unit_price6'] = row[29]
        	result['remarks6'] = row[30] 
        	result['software7'] = row[31]
        	result['num7'] = row[32]
        	result['unit7'] = row[33]
        	result['unit_price7'] = row[34]
        	result['remarks7'] = row[35] 
        	result['software8'] = row[36]
        	result['num8'] = row[37]
        	result['unit8'] = row[38]
        	result['unit_price8'] = row[39]
        	result['remarks8'] = row[40] 
        	result['software9'] = row[41]
        	result['num9'] = row[42]
        	result['unit9'] = row[43]
        	result['unit_price9'] = row[44]
        	result['remarks9'] = row[45] 
        	result['software10'] = row[46]
        	result['num10'] = row[47]
        	result['unit10'] = row[48]
        	result['unit_price10'] = row[49]
        	result['remarks10'] = row[50] 
       		result['software11'] = row[51]
         	result['num11'] = row[52]
            	result['unit11'] = row[53]
            	result['unit_price11'] = row[54]
            	result['remarks11'] = row[55] 
            	result['software12'] = row[56]
            	result['num12'] = row[57]
            	result['unit12'] = row[58]
            	result['unit_price12'] = row[59]
            	result['remarks12'] = row[60] 
	  	result['purcharse_order'] = row[61]
	
	    	jsonData.append(result)

            software1 = jsonData[0]['software1']
            nums1 = jsonData[0]['num1']
	    if nums1 == 0:
		nums1 = ' '
            unit1 = jsonData[0]['unit1']
            unit_price1 = jsonData[0]['unit_price1']
	    if unit_price1 == 0:
		unit_price1 = ' '
            remarks1 = jsonData[0]['remarks1']

            software2 = jsonData[0]['software2']
            nums2 = jsonData[0]['num2']
	    if nums2 == 0:
		nums2 = ' '
            unit2 = jsonData[0]['unit2']
            unit_price2 = jsonData[0]['unit_price2']
	    if unit_price2 == 0:
		unit_price2 = ' '
            remarks2 = jsonData[0]['remarks2']

            software3 = jsonData[0]['software3']
            nums3 = jsonData[0]['num3']
	    if nums3 == 0:
		nums3 = ' '
            unit3 = jsonData[0]['unit3']
            unit_price3 = jsonData[0]['unit_price3']
	    if unit_price3 == 0:
		unit_price3 = ' '
            remarks3 = jsonData[0]['remarks3']

            software4 = jsonData[0]['software4']
            nums4 = jsonData[0]['num4']
	    if nums4 == 0:
		nums4 = ' '
            unit4 = jsonData[0]['unit4']
            unit_price4 = jsonData[0]['unit_price4']
	    if unit_price4 == 0:
		unit_price4 = ' '
            remarks4 = jsonData[0]['remarks4']

            software5 = jsonData[0]['software5']
            nums5 = jsonData[0]['num5']
	    if nums5 == 0:
		nums5 = ' '
            unit5 = jsonData[0]['unit5']
            unit_price5 = jsonData[0]['unit_price5']
	    if unit_price5 == 0:
		unit_price5 = ' '
            remarks5 = jsonData[0]['remarks5']

            software6 = jsonData[0]['software6']
            nums6 = jsonData[0]['num6']
	    if nums6 == 0:
		nums6 = ' '
            unit6 = jsonData[0]['unit6']
            unit_price6 = jsonData[0]['unit_price6']
	    if unit_price6 == 0:
		unit_price6 = ' '
            remarks6 = jsonData[0]['remarks6']

            software7 = jsonData[0]['software7']
            nums7 = jsonData[0]['num7']
	    if nums7 == 0:
		nums7 = ' '
            unit7 = jsonData[0]['unit7']
            unit_price7 = jsonData[0]['unit_price7']
	    if unit_price7 == 0:
		unit_price7 = ' '
            remarks7 = jsonData[0]['remarks7']

            software8 = jsonData[0]['software8']
            nums8 = jsonData[0]['num8']
	    if nums8 == 0:
		nums8 = ' '
            unit8 = jsonData[0]['unit8']
            unit_price8 = jsonData[0]['unit_price8']
	    if unit_price8 == 0:
		unit_price8 = ' '
            remarks8 = jsonData[0]['remarks8']

            software9 = jsonData[0]['software9']
            nums9 = jsonData[0]['num9']
	    if nums9 == 0:
		nums9 = ' '
            unit9 = jsonData[0]['unit9']
            unit_price9 = jsonData[0]['unit_price9']
	    if unit_price9 == 0:
		unit_price9 = ' '
            remarks9 = jsonData[0]['remarks9']

            software10 = jsonData[0]['software10']
            nums10 = jsonData[0]['num10']
	    if nums10 == 0:
		nums10 = ' '
            unit10 = jsonData[0]['unit10']
            unit_price10 = jsonData[0]['unit_price10']
	    if unit_price10 == 0:
		unit_price10 = ' '
            remarks10 = jsonData[0]['remarks10']

            software11 = jsonData[0]['software11']
            nums11 = jsonData[0]['num11']
	    if nums11 == 0:
		nums11 = ' '
            unit11 = jsonData[0]['unit11']
            unit_price11 = jsonData[0]['unit_price11']
	    if unit_price11 == 0:
		unit_price11 = ' '
            remarks11 = jsonData[0]['remarks11']

            software12 = jsonData[0]['software12']
            nums12 = jsonData[0]['num12']
	    if nums12 == 0:
		nums12 = ' '
            unit12 = jsonData[0]['unit12']
            unit_price12 = jsonData[0]['unit_price12']
	    if unit_price12 == 0:
		unit_price12 = ' '
            remarks12 = jsonData[0]['remarks12']
	else:
	    print('不存在')
            software1 = ''
            nums1 = ' '
            unit1 = ''
            unit_price1 = ' '
            remarks1 = ''

            software2 = ''
            nums2 = ' '
            unit2 = ''
            unit_price2 = ' '
            remarks2 = ''

            software3 = ''
            nums3 = ' '
            unit3 = ''
            unit_price3 = ' '
            remarks3 = ''

            software4 = ''
            nums4 = ' '
            unit4 = ''
            unit_price4 = ' '
            remarks4 = ''

            software5 = ''
            nums5 = ' '
            unit5 = ''
            unit_price5 = ' '
            remarks5 = ''

            software6 = ''
            nums6 = ' '
            unit6 = ''
            unit_price6 = ' '
            remarks6 = ''

            software7 = ''
            nums7 = ' '
            unit7 = ''
            unit_price7 = ' '
            remarks7 = ''

            software8 = ''
            nums8 = ''
            unit8 = ''
            unit_price8 = ''
            remarks8 = ''

            software9 = ''
            nums9 = ' '
            unit9 = ''
            unit_price9 = ' '
            remarks9 = ''

            software10 = ''
            nums10 = ' '
            unit10 = ''
            unit_price10 = ' '
            remarks10 = ''

            software11 = ''
            nums11 = ' '
            unit11 = ''
            unit_price11 = ' '
            remarks11 = ''

            software12 = ''
            nums12 = ' '
            unit12 = ''
            unit_price12 = ' '
            remarks12 = ''

	    if  ContractAccountant.query.filter_by(purchase_order=check_order).first() is not None:
                print('当对应订单在合同结算表中存在时才insert software_cost ')

                cursor.execute("INSERT INTO software_cost(software1,num1,unit1,unit_price1,remarks1,software2,num2,unit2,unit_price2,remarks2,software3,num3,unit3,unit_price3,remarks3,software4,num4,unit4,unit_price4,remarks4, software5,num5,unit5,unit_price5,remarks5,software6,num6,unit6,unit_price6,remarks6,software7,num7,unit7,unit_price7,remarks7,software8,num8,unit8,unit_price8,remarks8,   software9,num9,unit9,unit_price9,remarks9,software10,num10,unit10,unit_price10,remarks10,software11,num11,unit11,unit_price11,remarks11,software12,num12,unit12,unit_price12,remarks12,purchase_order) VALUE ('%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s')"%(software1,nums1,unit1,unit_price1,remarks1,software2,nums2,unit2,unit_price2,remarks2,software3,nums3,unit3,unit_price3,remarks3,software4,nums4,unit4,unit_price4,remarks4, software5,nums5,unit5,unit_price5,remarks5,software6,nums6,unit6,unit_price6,remarks6,software7,nums7,unit7,unit_price7,remarks7,software8,nums8,unit8,unit_price8,remarks8,   software9,nums9,unit9,unit_price9,remarks9,software10,nums10,unit10,unit_price10,remarks10,software11,nums11,unit11,unit_price11,remarks11,software12,nums12,unit12,unit_price12,remarks12,check_order))
	
	        database.commit()
            else:
	        return redirect(url_for('main.contract_accountant'))

    else:
	return redirect(url_for('main.contract_accountant'))

    # 接收表单传回的信息
    if request.method == 'POST':

	try:
            '''warning:这里需要设置为环境获取'''
            database = MySQLdb.connect("localhost", "root", "uroot012", "erp_development", charset='utf8')
            cursor = database.cursor()
        except:
            print 'MySQL connect fail...'


        if "software1" in request.form:
            software1 = request.form['software1']
        else:
            software1 = ""
        if "num1" in request.form:
            nums1 = request.form['num1']
            if nums1 == '':
                nums1 = ' '

        if "unit1" in request.form:
            unit1 = request.form['unit1']
        else:
            unit1 = ""
        if "unit_price1" in request.form:
            unit_price1 = request.form['unit_price1']
            if unit_price1 == '': 
                unit_price1 = ' '

        if "remark1" in request.form:
            remarks1 = request.form['remark1']
        else:
            remarks1 = ""	

        if "software2" in request.form:
            software2 = request.form['software2']
        else:
            software2 = ""
        if "num2" in request.form:
            nums2 = request.form['num2']
            if nums2 == '':
                nums2 = ' '
        if "unit2" in request.form:
            unit2 = request.form['unit2']
        else:
            unit2 = ""
        if "unit_price2" in request.form:
            unit_price2 = request.form['unit_price2']
            if unit_price2 == '': 
                unit_price2 = ' '

        if "remark2" in request.form:
            remarks2 = request.form['remark2']
        else:
            remarks2 = ""

        if "software3" in request.form:
            software3 = request.form['software3']
        else:
            software3 = ""
        if "num3" in request.form:
            nums3 = request.form['num3']
            if nums3 == '':
                nums3 = ' '

        if "unit3" in request.form:
            unit3 = request.form['unit3']
        else:
            unit3 = ""
        if "unit_price3" in request.form:
            unit_price3 = request.form['unit_price3']
            if unit_price3 == '': 
                unit_price3 = ' '
        if "remark3" in request.form:
            remarks3 = request.form['remark3']
        else:
            remarks3 = ""


        if "software4" in request.form:
            software4 = request.form['software4']
        else:
            software4 = ""
        if "num4" in request.form:
            nums4 = request.form['num4']
            if nums4 == '':
                nums4 = ' '

        if "unit4" in request.form:
            unit4 = request.form['unit4']
        else:
            unit4 = ""
        if "unit_price4" in request.form:
            unit_price4 = request.form['unit_price4']
            if unit_price4 == '': 
                unit_price4 = ' '
        if "remark4" in request.form:
            remarks4 = request.form['remark4']
        else:
            remarks4 = ""


        if "software5" in request.form:
            software5 = request.form['software5']
        else:
            software5 = ""
        if "num5" in request.form:
            nums5 = request.form['num5']
            if nums5 == '':
                nums5 = ' '

        if "unit5" in request.form:
            unit5 = request.form['unit5']
        else:
            unit5 = ""
        if "unit_price5" in request.form:
            unit_price5 = request.form['unit_price5']
            if unit_price5 == '': 
                unit_price5 = ' '
        if "remark5" in request.form:
            remarks5 = request.form['remark5']
        else:
            remarks5 = ""

        if "software6" in request.form:
            software6 = request.form['software6']
        else:
            software6 = ""
        if "num6" in request.form:
            nums6 = request.form['num6']
            if nums6 == '':
                nums6 = ' '

        if "unit6" in request.form:
            unit6 = request.form['unit6']
        else:
            unit6 = ""
        if "unit_price6" in request.form:
            unit_price6 = request.form['unit_price6']
            if unit_price6 == '': 
                unit_price6 = ' '
        if "remark6" in request.form:
            remarks6 = request.form['remark6']
        else:
            remarks6 = ""

        if "software7" in request.form:
            software7 = request.form['software7']
        else:
            software7 = ""
        if "num7" in request.form:
            nums7 = request.form['num7']
            if nums7 == '':
                nums7 = ' '

        if "unit7" in request.form:
            unit7 = request.form['unit7']
        else:
            unit7 = ""
        if "unit_price7" in request.form:
            unit_price7 = request.form['unit_price7']
            if unit_price7 == '': 
                unit_price7 = ' '
        if "remark7" in request.form:
            remarks7 = request.form['remark7']
        else:
            remarks7 = ""

        if "software8" in request.form:
            software8 = request.form['software8']
        else:
            software8 = ""
	if "num8" in request.form:
            nums8 = request.form['num8']
            if nums8 == '':
                nums8 = ' '

        if "unit8" in request.form:
            unit8 = request.form['unit8']
        else:
            unit8 = ""
        if "unit_price8" in request.form:
            unit_price8 = request.form['unit_price8']
            if unit_price8 == '': 
                unit_price8 = ' '
        if "remark8" in request.form:
            remarks8 = request.form['remark8']
        else:
            remarks8 = ""


        if "software9" in request.form:
            software9 = request.form['software9']
        else:
            software9 = ""
        if "num9" in request.form:
            nums9 = request.form['num9']
            if nums9 == '':
                nums9 = ' '

        if "unit9" in request.form:
            unit9 = request.form['unit9']
        else:
            unit9 = ""
        if "unit_price9" in request.form:
            unit_price9 = request.form['unit_price9']
            if unit_price9 == '': 
                unit_price9 = ' '

        if "remark9" in request.form:
            remarks9 = request.form['remark9']
        else:
            remarks9 = ""


        if "software10" in request.form:
            software10 = request.form['software10']
        else:
            software10 = ""
        if "num10" in request.form:
            nums10 = request.form['num10']
            if nums10 == '':
                nums10 = ' '

        if "unit10" in request.form:
            unit10 = request.form['unit10']
        else:
            unit10 = ""
        if "unit_price10" in request.form:
            unit_price10 = request.form['unit_price10']
            if unit_price10 == '': 
                unit_price10 = ' '

        if "remark10" in request.form:
            remarks10 = request.form['remark10']
        else:
            remarks10 = ""


        if "software11" in request.form:
            software11= request.form['software11']
        else:
            software11 = ""
        if "num11" in request.form:
            nums11 = request.form['num11']
            if nums11 == '':
                nums11 = ' '

        if "unit11" in request.form:
            unit11 = request.form['unit11']
        else:
            unit11 = ""
        if "unit_price11" in request.form:
            unit_price11 = request.form['unit_price11']
            if unit_price11 == '': 
                unit_price11 = ' '
        if "remark11" in request.form:
            remarks11 = request.form['remark11']
        else:
            remarks11 = ""


        if "software12" in request.form:
            software12 = request.form['software12']
        else:
            software12 = ""
        if "num12" in request.form:
            nums12 = request.form['num12']
            if nums12 == '':
                nums12 = ' '

        if "unit12" in request.form:
            unit12 = request.form['unit12']
        else:
            unit12 = ""
        if "unit_price12" in request.form:
            unit_price12 = request.form['unit_price12']
            if unit_price12 == '': 
                unit_price12 = ' '
        if "remark12" in request.form:
            remarks12 = request.form['remark12']
        else:
            remarks12 = ""

        print('更新数据表')
        
	cursor.execute("UPDATE software_cost SET software1='%s',num1='%s',unit1='%s',unit_price1='%s',remarks1='%s',software2='%s',num2='%s',unit2='%s',unit_price2='%s',remarks2='%s',software3='%s',num3='%s',unit3='%s',unit_price3='%s',remarks3='%s',software4='%s',num4='%s',unit4='%s',unit_price4='%s',remarks4='%s', software5='%s',num5='%s',unit5='%s',unit_price5='%s',remarks5='%s',software6='%s',num6='%s',unit6='%s',unit_price6='%s',remarks6='%s',software7='%s',num7='%s',unit7='%s',unit_price7='%s',remarks7='%s',software8='%s',num8='%s',unit8='%s',unit_price8='%s',remarks8='%s',   software9='%s',num9='%s',unit9='%s',unit_price9='%s',remarks9='%s',software10='%s',num10='%s',unit10='%s',unit_price10='%s',remarks10='%s',software11='%s',num11='%s',unit11='%s',unit_price11='%s',remarks11='%s',software12='%s',num12='%s',unit12='%s',unit_price12='%s',remarks12='%s' where purchase_order='%s'"%(software1,nums1,unit1,unit_price1,remarks1,software2,nums2,unit2,unit_price2,remarks2,software3,nums3,unit3,unit_price3,remarks3,software4,nums4,unit4,unit_price4,remarks4, software5,nums5,unit5,unit_price5,remarks5,software6,nums6,unit6,unit_price6,remarks6,software7,nums7,unit7,unit_price7,remarks7,software8,nums8,unit8,unit_price8,remarks8,   software9,nums9,unit9,unit_price9,remarks9,software10,nums10,unit10,unit_price10,remarks10,software11,nums11,unit11,unit_price11,remarks11,software12,nums12,unit12,unit_price12,remarks12,check_order))
	

        ''' 更新结算表上的软件成本 '''
	print('更新结算表上的软件成本')
	nums = [nums1,nums2,nums3,nums4,nums5,nums6,nums7,nums8,nums9,nums10,nums11,nums12]
	nums2int = []
	for num in nums:
	    if num != ' ':
	        nums2int.append(int(num))
	    else:
	   	nums2int.append(0)
	unit_price =[unit_price1,unit_price2,unit_price3,unit_price4,unit_price5,unit_price6,unit_price7,unit_price8,unit_price9,unit_price10,unit_price11,unit_price12]
	price2float = []

	for price in unit_price:
	    if price != ' ':
	        price2float.append(float(price))
	    else:
		price2float.append(0.0)

	def cost_sum(nums,prices):	    
	    software_cost = map(lambda (a,b):a*b, zip(nums,prices))
	    return sum(software_cost)


        cursor.execute("UPDATE contract_accountant SET softwares_cost='%s' where purchase_order='%s'"%(cost_sum(nums2int,price2float),check_order))

        database.commit()
        database.close()

	#计算 利润=合同金额-税金-终端成本-服务器成本-配件成本-软件成本-报销费用-杂费-运费-得利税
	order_amount = ContractAccountant.query.filter_by(purchase_order=check_order).first().order_amount
	tax = ContractAccountant.query.filter_by(purchase_order=check_order).first().tax
	tem_cost = ContractAccountant.query.filter_by(purchase_order=check_order).first().tem_cost	
	servers_cost = ContractAccountant.query.filter_by(purchase_order=check_order).first().servers_cost
	fittings_cost = ContractAccountant.query.filter_by(purchase_order=check_order).first().fittings_cost
	softwares_cost = cost_sum(nums2int,price2float)
	reimbursement = ContractAccountant.query.filter_by(purchase_order=check_order).first().reimbursement
	consult_cost = ContractAccountant.query.filter_by(purchase_order=check_order).first().consult_cost
	freight = ContractAccountant.query.filter_by(purchase_order=check_order).first().freight
	after_sales = ContractAccountant.query.filter_by(purchase_order=check_order).first().after_sales

	print('计算 利润')
	profit = order_amount-tax-tem_cost-servers_cost-fittings_cost-softwares_cost-reimbursement-consult_cost-freight-after_sales
	

        ContractAccountant.query.filter_by(purchase_order=check_order).update(
                    {"profit":profit })

	db.session.commit()

    return render_template('payment/software_cost.html',software1=software1,num1=nums1,unit1=unit1,unit_price1=unit_price1,remark1=remarks1,				                      software2=software2,num2=nums2,unit2=unit2,unit_price2=unit_price2,remark2=remarks2,					              software3=software3,num3=nums3,unit3=unit3,unit_price3=unit_price3,remark3=remarks3,						      software4=software4,num4=nums4,unit4=unit4,unit_price4=unit_price4,remark4=remarks4,						      software5=software5,num5=nums5,unit5=unit5,unit_price5=unit_price5,remark5=remarks5,						      software6=software6,num6=nums6,unit6=unit6,unit_price6=unit_price6,remark6=remarks6,			 	software7=software7,num7=nums7,unit7=unit7,unit_price7=unit_price7,remark7=remarks7,						     software8=software8,num8=nums8,unit8=unit8,unit_price8=unit_price8,remark8=remarks8,					software9=software9,num9=nums9,unit9=unit9,unit_price9=unit_price9,remark9=remarks9,					 software10=software10,num10=nums10,unit10=unit10,unit_price10=unit_price10,remark10=remarks10,					      software11=software11,num11=nums11,unit11=unit11,unit_price11=unit_price11,remark11=remarks11,			      software12=software12,num12=nums12,unit12=unit12,unit_price12=unit_price12,remark12=remarks12)



'''费用报销单'''
@main.route('/payment/reimbursement',methods = ['GET','POST'])
@login_required
def reimbursement():

    get_number_data = request.form.get('get_number_data', '')
    if any(get_number_data):
        reimbursement_number = json.loads(get_number_data)["number"]  

        try:
            '''warning:这里需要设置为环境获取'''
            conn = MySQLdb.connect("localhost","root","uroot012","erp_development",charset='utf8')
            cursor = conn.cursor()
        except:
            print 'MySQL connect fail...'

        cursor.execute("SELECT * from reimbursement where number='%s'"%reimbursement_number)
        data = cursor.fetchall()
        cursor.close()

        conn.close()
        jsonData = []
	
        for n,row  in enumerate(data):
            result = {}
            result['purpose1'] = row[9]
	    if row[10] != 0.0:
	        result['amount1'] = row[10]    
	    else:
	        result['amount1'] = ' '
	    result['purpose2'] = row[11]
	    if row[12] != 0.0:
	        result['amount2'] = row[12]    
	    else:
	        result['amount2'] = ' '

	    result['purpose3'] = row[13]
	    if row[14] != 0.0:
	        result['amount3'] = row[14]    
	    else:
	        result['amount3'] = ' '
	    result['purpose4'] = row[15]
	    if row[16] != 0.0:
	        result['amount4'] = row[16]    
	    else:
	        result['amount4'] = ' '

            jsonData.append(result)
	
        return json.dumps(jsonData)


    number = request.form.get('row[number]', '')
    date = request.form.get('row[date]', '')
    purchase_order = request.form.get('row[purchase_order]', '')
    remark = request.form.get('row[remark]', '')
    loan = request.form.get('row[loan]', '')
    residue = request.form.get('row[residue]', '')
    rei_name = request.form.get('row[rei_name]', '')
    payee = request.form.get('row[payee]', '')
    oldValue = request.form.get('oldValue', '')

    '''修改记录'''
    if number is not None:       
        Reimbursement.query.filter_by(number=number).update({"date":date,"purchase_order":purchase_order.strip(),"remark":remark,"loan":loan,"residue":residue,"rei_name":rei_name,"payee":payee})
        
	db.session.commit()

    '''增加记录'''  
    add = request.form.get('add', '')

    if add == 'add_true':
        '''编号从001开始'''		
	list_reimbursement = []
        for i in db.session.query(Reimbursement.number).all():
            list_reimbursement.append(i[0])
        print '个数:', len(list_reimbursement)
	
	if len(list_reimbursement) == 0:
	    reimbursement_number = '0001'
	else:
            # 获取报销单中编号的最大值
            try:
                '''warning:这里需要设置为环境获取'''
                database = MySQLdb.connect("localhost", "root", "uroot012", "erp_development", charset='utf8')
                cursor = database.cursor()
            except:
                print 'MySQL connect fail...'

            cursor.execute("SELECT number from reimbursement")
            data = cursor.fetchall()
            get_data = []
            for i, w in enumerate(data):
                get_data.append(w[0])

            reimbursement_number = "%04d" %(long(max(get_data)) + 1)
    
	
        get_date = time.strftime('%Y-%m-%d', time.localtime(time.time()))
	add_item = Reimbursement(number=reimbursement_number,date=get_date,purchase_order='edit',sum_amount=0.0,remark='edit',loan=0.0,residue=0.0,
rei_name='edit',payee='edit',purpose_all='',purpose1='',amount1=0.0,purpose2='',amount2=0.0,purpose3='',amount3=0.0,purpose4='',amount4=0.0)
      
        db.session.add(add_item)
        db.session.commit()

    '''删除记录'''
    remove_number = request.form.get('remove_number[]', '')
    remove_order = request.form.get('remove_order[]', '')

    if remove_number != "":
	del_number = Reimbursement.query.filter_by(number=remove_number).first()

	db.session.delete(del_number)
	db.session.commit()

    if remove_order != "":
	print('删除了一份报销单')
	print('remove_order',remove_order)
	if Reimbursement.query.filter_by(purchase_order=remove_order).first() is not None:

	    '''同一合同的所有报销单的金额相加'''
	    get_amount = Reimbursement.query.filter_by(purchase_order=remove_order).all()


	    sum_amount = []
	    for n,amount in enumerate(get_amount):
		print(get_amount[n].sum_amount)
		sum_amount.append(get_amount[n].sum_amount) 	
	    
	    print('sum(sum_amount)sum(sum_amount)',sum(sum_amount))

	    ContractAccountant.query.filter_by(purchase_order=remove_order).update({"reimbursement":sum(sum_amount)})  
	    db.session.commit()

	    #计算 利润=合同金额-税金-终端成本-服务器成本-配件成本-软件成本-报销费用-杂费-运费-得利税
	    order_amount = ContractAccountant.query.filter_by(purchase_order=remove_order).first().order_amount
	    tax = ContractAccountant.query.filter_by(purchase_order=remove_order).first().tax
	    tem_cost = ContractAccountant.query.filter_by(purchase_order=remove_order).first().tem_cost	
	    servers_cost = ContractAccountant.query.filter_by(purchase_order=remove_order).first().servers_cost
	    fittings_cost = ContractAccountant.query.filter_by(purchase_order=remove_order).first().fittings_cost
	    softwares_cost = ContractAccountant.query.filter_by(purchase_order=remove_order).first().softwares_cost
	    reimbursement = sum(sum_amount)
	    consult_cost = ContractAccountant.query.filter_by(purchase_order=remove_order).first().consult_cost
	    freight = ContractAccountant.query.filter_by(purchase_order=remove_order).first().freight
	    after_sales = ContractAccountant.query.filter_by(purchase_order=remove_order).first().after_sales

	    print('计算 利润')
	    profit = order_amount-tax-tem_cost-servers_cost-fittings_cost-softwares_cost-reimbursement-consult_cost-freight-after_sales
	

            ContractAccountant.query.filter_by(purchase_order=remove_order).update(
                    {"profit":profit })

	    db.session.commit()

	else:
	    print('该合同中的报销单不存在')
	    ContractAccountant.query.filter_by(purchase_order=remove_order).update({"reimbursement":0.0})

	    #计算 利润=合同金额-税金-终端成本-服务器成本-配件成本-软件成本-报销费用（ 为0）-杂费-运费-得利税
	    order_amount = ContractAccountant.query.filter_by(purchase_order=remove_order).first().order_amount
	    tax = ContractAccountant.query.filter_by(purchase_order=remove_order).first().tax
	    tem_cost = ContractAccountant.query.filter_by(purchase_order=remove_order).first().tem_cost	
	    servers_cost = ContractAccountant.query.filter_by(purchase_order=remove_order).first().servers_cost
	    fittings_cost = ContractAccountant.query.filter_by(purchase_order=remove_order).first().fittings_cost
	    softwares_cost = ContractAccountant.query.filter_by(purchase_order=remove_order).first().softwares_cost
	    consult_cost = ContractAccountant.query.filter_by(purchase_order=remove_order).first().consult_cost
	    freight = ContractAccountant.query.filter_by(purchase_order=remove_order).first().freight
	    after_sales = ContractAccountant.query.filter_by(purchase_order=remove_order).first().after_sales

	    print('计算 利润')
	    profit = order_amount-tax-tem_cost-servers_cost-fittings_cost-softwares_cost-consult_cost-freight-after_sales
	

            ContractAccountant.query.filter_by(purchase_order=remove_order).update(
                    {"profit":profit })

	    db.session.commit()
  	


    # 接收表单传回的信息
    if request.method == 'POST':

	try:
            '''warning:这里需要设置为环境获取'''
            database = MySQLdb.connect("localhost", "root", "uroot012", "erp_development", charset='utf8')
            cursor = database.cursor()
        except:
            print 'MySQL connect fail...'


        if "purpose1" in request.form:
            purpose1 = request.form['purpose1']
        else:
            purpose1 = ""
        if "amount1" in request.form:
            amount1 = request.form['amount1']
            if amount1 == ' ':
                amount1 = 0.0


        if "purpose2" in request.form:
            purpose2 = request.form['purpose2']
        else:
            purpose2 = ""
        if "amount2" in request.form:
            amount2 = request.form['amount2']
            if amount2 == ' ':
                amount2 = 0.0

        if "purpose3" in request.form:
            purpose3 = request.form['purpose3']
        else:
            purpose3 = ""
        if "amount3" in request.form:
            amount3 = request.form['amount3']
            if amount3 == ' ':
                amount3 = 0.0

        if "purpose4" in request.form:
            purpose4 = request.form['purpose4']
        else:
            purpose4 = ""
        if "amount4" in request.form:
            amount4 = request.form['amount4']
            if amount4 == ' ':
                amount4 = 0.0

        if "reimbursement_number" in request.form:
            reimbursement_number = request.form['reimbursement_number']
	else:
	    reimbursement_number = ""
	purpose_all = purpose1 + '  ' + purpose2 + '  ' + purpose3 + '  ' + purpose4
	print('purpose_all',purpose_all)

	if reimbursement_number != "":

            ''' 更新报销单上的总金额 '''
	    print('更新报销单上的总金额')

	    unit_amount =[amount1,amount2,amount3,amount4]
	    amount2float = []

	    for amount in unit_amount:
	        if amount != ' ':
	            amount2float.append(float(amount))
	        else:
		    amount2float.append(0.0)

	    def amount_sum(amount2float):	    
	        amount_sum = sum(amount2float)
	        return amount_sum

	    sum_amount = amount_sum(amount2float)

            Reimbursement.query.filter_by(number=reimbursement_number).update({"purpose_all":purpose_all,"purpose1":purpose1,"amount1":amount1,"purpose2":purpose2,"amount2":amount2,"purpose3":purpose3,"amount3":amount3,"purpose4":purpose4,"amount4":amount4,"sum_amount":sum_amount})  
	    db.session.commit()

            ''' 更新合同结算表上的报销金额 '''
	    purchase_order = Reimbursement.query.filter_by(number=reimbursement_number).first().purchase_order
	    if purchase_order != "":	

                if ContractAccountant.query.filter_by(purchase_order=purchase_order).first() is not None:
		    '''当合同编号存在时'''
	            '''同一合同的所有报销单的金额相加'''
	            get_amount = Reimbursement.query.filter_by(purchase_order=purchase_order).all()


	            sum_amount = []
	            for n,amount in enumerate(get_amount):
		        sum_amount.append(get_amount[n].sum_amount) 	
	    	   
	            ContractAccountant.query.filter_by(purchase_order=purchase_order).update({"reimbursement":sum(sum_amount)})  
		    db.session.commit()

		    #计算 利润=合同金额-税金-终端成本-服务器成本-配件成本-软件成本-报销费用-杂费-运费-得利税
		    order_amount = ContractAccountant.query.filter_by(purchase_order=purchase_order).first().order_amount
		    tax = ContractAccountant.query.filter_by(purchase_order=purchase_order).first().tax
		    tem_cost = ContractAccountant.query.filter_by(purchase_order=purchase_order).first().tem_cost	
		    servers_cost = ContractAccountant.query.filter_by(purchase_order=purchase_order).first().servers_cost
		    fittings_cost = ContractAccountant.query.filter_by(purchase_order=purchase_order).first().fittings_cost
		    softwares_cost = ContractAccountant.query.filter_by(purchase_order=purchase_order).first().softwares_cost
		    reimbursement = sum(sum_amount)
	 	    consult_cost = ContractAccountant.query.filter_by(purchase_order=purchase_order).first().consult_cost
	 	    freight = ContractAccountant.query.filter_by(purchase_order=purchase_order).first().freight
		    after_sales = ContractAccountant.query.filter_by(purchase_order=purchase_order).first().after_sales

		    profit = order_amount-tax-tem_cost-servers_cost-fittings_cost-softwares_cost-reimbursement-consult_cost-freight-after_sales

        	    ContractAccountant.query.filter_by(purchase_order=purchase_order).update(
                    {"profit":profit })

 	    
		    db.session.commit()

    return render_template('payment/reimbursement.html')


@main.route('/payment/reimbursement/return_json',methods = ['GET','POST'])
@login_required
def reimbursement_return_json():
        app = current_app._get_current_object()
        try:
            '''warning:这里需要设置为环境获取'''
            db = MySQLdb.connect("localhost","root","uroot012","erp_development",charset='utf8')
            cursor = db.cursor()
        except:
            print 'MySQL connect fail...'
        cursor.execute("SELECT * from reimbursement")
        data = cursor.fetchall()
        cursor.close()
        jsonData = []

        for n,row  in enumerate(data):
            result = {}
            result['number'] = row[0]
	    result['date'] = row[1]
	    result['purchase_order'] = row[2]
	    result['sum_amount'] = row[3]
	    result['remark'] = row[4]
	    result['loan'] = row[5]
	    result['residue'] = row[6]
 	    result['rei_name'] = row[7]
	    result['payee'] = row[8]
	    result['purpose1'] = row[9]
	    result['amount1'] = row[10]
	    result['purpose2'] = row[11] 
	    result['amount2'] = row[12]
	    result['purpose3'] = row[13]
	    result['amount3'] = row[14]
	    result['purpose4'] = row[15]
	    result['amount4'] = row[16]
 	    result['purpose_all'] = row[17]

            jsonData.append(result)

        return json.dumps(jsonData)



'''付款申请单'''
@main.route('/payment/pay_request',methods = ['GET','POST'])
@login_required
def pay_request():
    
    get_number_data = request.form.get('get_number_data', '')
    if any(get_number_data):
        request_number = json.loads(get_number_data)["number"]  


        try:
            '''warning:这里需要设置为环境获取'''
            conn = MySQLdb.connect("localhost","root","uroot012","erp_development",charset='utf8')
            cursor = conn.cursor()
        except:
            print 'MySQL connect fail...'

        cursor.execute("SELECT * from payrequest where number='%s'"%request_number)
        data = cursor.fetchall()
        cursor.close()

        conn.close()
        jsonData = []
	
        for n,row  in enumerate(data):
            result = {}
            result['purpose1'] = row[12]
	    if row[13] != 0.0:
	        result['amount1'] = row[13]    
	    else:
	        result['amount1'] = ' '
	    result['purpose2'] = row[14]
	    if row[15] != 0.0:
	        result['amount2'] = row[15]    
	    else:
	        result['amount2'] = ' '

	    result['purpose3'] = row[16]
	    if row[17] != 0.0:
	        result['amount3'] = row[17]    
	    else:
	        result['amount3'] = ' '
	    result['purpose4'] = row[18]
	    if row[19] != 0.0:
	        result['amount4'] = row[19]    
	    else:
	        result['amount4'] = ' '

	    result['deposit_bank'] = row[21]
	    result['deposit_account'] = row[22]
            result['tax_number'] = row[23]


            jsonData.append(result)
	
        return json.dumps(jsonData)


    number = request.form.get('row[number]', '')
    date = request.form.get('row[date]', '')
    project_name = request.form.get('row[project_name]', '')
    receivable_company = request.form.get('row[receivable_company]', '')
    abstract = request.form.get('row[abstract]', '')
    purchase_order = request.form.get('row[purchase_order]', '')
    project_amount = request.form.get('row[project_amount]', '')
    payed = request.form.get('row[payed]', '')
    pay_way = request.form.get('row[pay_way]', '')
    remark = request.form.get('row[remark]', '')
    operator = request.form.get('row[operator]', '')




    '''修改记录'''
    if number is not None and purchase_order is not None:       
        PayRequest.query.filter_by(number=number).update({"date":date,"project_name":project_name,"receivable_company":receivable_company,"abstract":abstract,"purchase_order":purchase_order.strip(),
"project_amount":project_amount,"payed":payed,"pay_way":pay_way,"remark":remark,"operator":operator})
       
	#获取该合同的总金额
	print('purchase_orderpurchase_order',purchase_order)
	get_order_amount = Orders.query.filter_by(order_number=purchase_order).first()
	print('get_order_amount',get_order_amount)
	if get_order_amount is not None:
	    order_amount = Orders.query.filter_by(order_number=purchase_order).first().order_amount
	    PayRequest.query.filter_by(number=number).update({"project_amount":order_amount}) 


	db.session.commit()



    '''增加记录'''  
    add = request.form.get('add', '')

    if add == 'add_true':
        '''编号从001开始'''		
	list_request = []
        for i in db.session.query(PayRequest.number).all():
            list_request.append(i[0])
        print '个数:', len(list_request)
	
	if len(list_request) == 0:
	    request_number = '0001'
	else:
            # 获取报销单中编号的最大值
            try:
                '''warning:这里需要设置为环境获取'''
                database = MySQLdb.connect("localhost", "root", "uroot012", "erp_development", charset='utf8')
                cursor = database.cursor()
            except:
                print 'MySQL connect fail...'

            cursor.execute("SELECT number from payrequest")
            data = cursor.fetchall()
            get_data = []
            for i, w in enumerate(data):
                get_data.append(w[0])

            request_number = "%04d" %(long(max(get_data)) + 1)
    
        get_date = time.strftime('%Y-%m-%d', time.localtime(time.time()))
	add_item = PayRequest(number=request_number,date=get_date,project_name='edit',receivable_company='edit',
abstract='',purchase_order='edit',project_amount=0.0,sum_payed=0.0,payed=0.0,pay_way='',remark='edit',operator='',purpose_all='',purpose1='',
amount1=0.0,purpose2='',amount2=0.0,purpose3='',amount3=0.0,purpose4='',amount4=0.0,deposit_bank='',deposit_account='',tax_number='')
      
        db.session.add(add_item)
        db.session.commit()

    '''删除记录'''
    remove_number = request.form.get('remove_number[]', '')
    remove_order = request.form.get('remove_order[]', '')

    if remove_number != "":
	del_number = PayRequest.query.filter_by(number=remove_number).first()

	db.session.delete(del_number)
	db.session.commit()



    if remove_order != "":
	print('删除了一份付款单')
	print('remove_order',remove_order)

	if PayRequest.query.filter_by(purchase_order=remove_order).first() is not None:
            ''' 更新合同结算表上的杂费 '''

	    '''同一合同编号的所有报销申请单的金额相加'''
	    get_amount = PayRequest.query.filter_by(purchase_order=remove_order).all()

	    sum_amount = []
	    for n,amount in enumerate(get_amount):
		sum_amount.append(get_amount[n].sum_payed) 	
	    
	    ContractAccountant.query.filter_by(purchase_order=remove_order).update({"consult_cost":sum(sum_amount)})
	    db.session.commit()

	    #计算 利润=合同金额-税金-终端成本-服务器成本-配件成本-软件成本-报销费用-杂费-运费-得利税
	    order_amount = ContractAccountant.query.filter_by(purchase_order=remove_order).first().order_amount
	    tax = ContractAccountant.query.filter_by(purchase_order=remove_order).first().tax
	    tem_cost = ContractAccountant.query.filter_by(purchase_order=remove_order).first().tem_cost	
	    servers_cost = ContractAccountant.query.filter_by(purchase_order=remove_order).first().servers_cost
	    fittings_cost = ContractAccountant.query.filter_by(purchase_order=remove_order).first().fittings_cost
	    softwares_cost = ContractAccountant.query.filter_by(purchase_order=remove_order).first().softwares_cost
	    reimbursement = ContractAccountant.query.filter_by(purchase_order=remove_order).first().reimbursement
	    consult_cost = sum(sum_amount)

	    freight = ContractAccountant.query.filter_by(purchase_order=remove_order).first().freight
	    after_sales = ContractAccountant.query.filter_by(purchase_order=remove_order).first().after_sales

	    print('计算 利润')
	    profit = order_amount-tax-tem_cost-servers_cost-fittings_cost-softwares_cost-reimbursement-consult_cost-freight-after_sales
	

       	    ContractAccountant.query.filter_by(purchase_order=remove_order).update(
                   {"profit":profit })

	    db.session.commit()
	else:
	    print('该合同下的付款不存在')
	    ContractAccountant.query.filter_by(purchase_order=remove_order).update({"consult_cost":0.0})

	    #计算 利润=合同金额-税金-终端成本-服务器成本-配件成本-软件成本-报销费用-杂费(为0)-运费-得利税
	    order_amount = ContractAccountant.query.filter_by(purchase_order=remove_order).first().order_amount
	    tax = ContractAccountant.query.filter_by(purchase_order=remove_order).first().tax
	    tem_cost = ContractAccountant.query.filter_by(purchase_order=remove_order).first().tem_cost	
	    servers_cost = ContractAccountant.query.filter_by(purchase_order=remove_order).first().servers_cost
	    fittings_cost = ContractAccountant.query.filter_by(purchase_order=remove_order).first().fittings_cost
	    softwares_cost = ContractAccountant.query.filter_by(purchase_order=remove_order).first().softwares_cost
	    reimbursement = ContractAccountant.query.filter_by(purchase_order=remove_order).first().reimbursement

	    freight = ContractAccountant.query.filter_by(purchase_order=remove_order).first().freight
	    after_sales = ContractAccountant.query.filter_by(purchase_order=remove_order).first().after_sales

	    print('计算 利润')
	    profit = order_amount-tax-tem_cost-servers_cost-fittings_cost-softwares_cost-reimbursement-freight-after_sales
	

       	    ContractAccountant.query.filter_by(purchase_order=remove_order).update(
                   {"profit":profit })

	    db.session.commit()


        # 接收表单传回的信息
    if request.method == 'POST':

	try:
            '''warning:这里需要设置为环境获取'''
            database = MySQLdb.connect("localhost", "root", "uroot012", "erp_development", charset='utf8')
            cursor = database.cursor()
        except:
            print 'MySQL connect fail...'


        if "purpose1" in request.form:
            purpose1 = request.form['purpose1']
        else:
            purpose1 = ""
        if "amount1" in request.form:
            amount1 = request.form['amount1']
            if amount1 == ' ':
                amount1 = 0.0

        if "purpose2" in request.form:
            purpose2 = request.form['purpose2']
        else:
            purpose2 = ""
        if "amount2" in request.form:
            amount2 = request.form['amount2']
            if amount2 == ' ':
                amount2 = 0.0

        if "purpose3" in request.form:
            purpose3 = request.form['purpose3']
        else:
            purpose3 = ""
        if "amount3" in request.form:
            amount3 = request.form['amount3']
            if amount3 == ' ':
                amount3 = 0.0

        if "purpose4" in request.form:
            purpose4 = request.form['purpose4']
        else:
            purpose4 = ""
        if "amount4" in request.form:
            amount4 = request.form['amount4']
            if amount4 == ' ':
                amount4 = 0.0

        if "pay_request_number" in request.form:
            pay_request_number = request.form['pay_request_number']
	else:
	    pay_request_number = ""

        if "deposit_bank" in request.form:
            deposit_bank = request.form['deposit_bank']
	else:
	    deposit_bank = ""

        if "deposit_account" in request.form:
            deposit_account = request.form['deposit_account']
	else:
	    deposit_account = ""

        if "tax_number" in request.form:
            tax_number = request.form['tax_number']
	else:
	    tax_number = ""

	purpose_all = purpose1 + '  ' + purpose2 + '  ' + purpose3 + '  ' + purpose4


	if pay_request_number != "":

            ''' 更新付款申请单上的付款总金额 '''
	    print('更新付款申请单上的付款总金额')

	    unit_amount =[amount1,amount2,amount3,amount4]
	    amount2float = []

	    for amount in unit_amount:
	        if amount != ' ':
	            amount2float.append(float(amount))
	        else:
		    amount2float.append(0.0)

	    def amount_sum(amount2float):	    
	        amount_sum = sum(amount2float)
	        return amount_sum

	    sum_payed = amount_sum(amount2float)

            PayRequest.query.filter_by(number=pay_request_number).update({"purpose_all":purpose_all,"purpose1":purpose1,"amount1":amount1,"purpose2":purpose2,"amount2":amount2,
"purpose3":purpose3,"amount3":amount3,"purpose4":purpose4,"amount4":amount4,"sum_payed":sum_payed,"deposit_bank":deposit_bank,
"deposit_account":deposit_account,"tax_number":tax_number})  
	    db.session.commit()

	    print('更新合同结算表上的杂费')
            ''' 更新合同结算表上的杂费 '''
	    #根据返回的申请单编号找出对应的合同号
	    if PayRequest.query.filter_by(number=pay_request_number).first() is not None:
	        purchase_order = PayRequest.query.filter_by(number=pay_request_number).first().purchase_order

	        if purchase_order != "":
                    if ContractAccountant.query.filter_by(purchase_order=purchase_order).first() is not None:
		        '''当合同编号存在时
	                同一合同编号的所有报销申请单的金额相加'''
	                get_amount = PayRequest.query.filter_by(purchase_order=purchase_order).all()

	    	        sum_amount = []
	                for n,amount in enumerate(get_amount):
		            sum_amount.append(get_amount[n].sum_payed) 	
	    
	                ContractAccountant.query.filter_by(purchase_order=purchase_order).update({"consult_cost":sum(sum_amount)})
	                db.session.commit()
	
		        #计算 利润=合同金额-税金-终端成本-服务器成本-配件成本-软件成本-报销费用-杂费-运费-得利税
		        order_amount = ContractAccountant.query.filter_by(purchase_order=purchase_order).first().order_amount
		        tax = ContractAccountant.query.filter_by(purchase_order=purchase_order).first().tax
		        tem_cost = ContractAccountant.query.filter_by(purchase_order=purchase_order).first().tem_cost	
		        servers_cost = ContractAccountant.query.filter_by(purchase_order=purchase_order).first().servers_cost
		        fittings_cost = ContractAccountant.query.filter_by(purchase_order=purchase_order).first().fittings_cost
		        softwares_cost = ContractAccountant.query.filter_by(purchase_order=purchase_order).first().softwares_cost
		        reimbursement = ContractAccountant.query.filter_by(purchase_order=purchase_order).first().reimbursement
		        consult_cost = sum(sum_amount)

		        freight = ContractAccountant.query.filter_by(purchase_order=purchase_order).first().freight
		        after_sales = ContractAccountant.query.filter_by(purchase_order=purchase_order).first().after_sales

		        profit = order_amount-tax-tem_cost-servers_cost-fittings_cost-softwares_cost-reimbursement-consult_cost-freight-after_sales
	

        	        ContractAccountant.query.filter_by(purchase_order=purchase_order).update(
                        {"profit":profit })

		    db.session.commit()

    return render_template('payment/pay_request.html')



@main.route('/payment/pay_request/return_json',methods = ['GET','POST'])
@login_required
def pay_request_return_json():
        app = current_app._get_current_object()
        try:
            '''warning:这里需要设置为环境获取'''
            db = MySQLdb.connect("localhost","root","uroot012","erp_development",charset='utf8')
            cursor = db.cursor()
        except:
            print 'MySQL connect fail...'
        cursor.execute("SELECT * from payrequest")
        data = cursor.fetchall()
        cursor.close()
        jsonData = []

        for n,row  in enumerate(data):
            result = {}
            result['number'] = row[0]
	    result['date'] = row[1]
	    result['project_name'] = row[2]
	    result['receivable_company'] = row[3]
	    result['abstract'] = row[4]
	    result['purchase_order'] = row[5]
	    result['project_amount'] = row[6]
 	    result['payed'] = row[7]
	    result['pay_way'] = row[8]
	    result['remark'] = row[9]
	    result['operator'] = row[10]
            result['purpose_all'] = row[11]
	    result['sum_payed'] = row[20]


            jsonData.append(result)

        return json.dumps(jsonData)





