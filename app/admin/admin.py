# -*- coding:utf-8 -*-
__author__ = 'xuan'

from flask.ext import admin


# from flask_admin import Admin


from flask_login import logout_user,login_required,login_user,current_user
#from flask.ext.superadmin import Admin,BaseView,expose
# from flask.ext.admin import BaseView,expose
from flask_admin import BaseView,expose,AdminIndexView

from flask.ext.admin.contrib.fileadmin import FileAdmin
from flask.ext.admin.contrib.sqla import ModelView

# from flask.ext.admin.contrib.sqla import ModelView

# from ..models import  Fittings,Semi_finished,End_product,Purchase_List,Goods_price,Fittings_Inputs,User,Role
#from  ..import flask_admin
#from  manage import  db
# from ..import flask_admin

import os.path as op
from ..models import User,Performance_Related,Clients
from ..forms import CKTextAreaField


# from ..models import User


# from .. import my_admin
# from app import my_admin



# path = op.join(op.dirname(__file__), 'static')
# print 'path',path
# my_admin.add_view(FileAdmin(path, '/static/', name='Static Files'))



class MyView(BaseView):
        # def is_accessible(self):
        # if current_user.is_authenticated:
        #     #print 'Ture1'
        #     print current_user.username
        #     return True
    # @admin.expose('/')
    @admin.expose('/')    
    def index(self):
        print 'admin'
        return self.render('admin/custom.html')

    # @admin.expose('/second_page')
    # def second_page(self): 

    #     return self.render('admin/custom.html')

# my_admin.add_view(MyView(name='myview'))


# print '!!!!!!!!!!!!!!!!'
# my_admin.add_view(MyView(name='myview'))


# path = op.join(op.dirname(__file__), 'static')
# print 'path',path
# my_admin.add_view(FileAdmin(path, '/static/', name='Static Files'))



# class MyAdminIndexView(AdminIndexView):
#     def is_accessible(self):
#         return current_user.is_authenticated



class UserModelView(ModelView):
    """View function of Flask-Admin for Models page."""

    def is_accessible(self):
        if current_user.is_authenticated and current_user.username =='admin':
        	return True

    #can_create = False
    column_labels = dict(email=u'邮箱', username=u'用户')
    column_list = ('email','username','password_hash')
    column_searchable_list = ('username', 'email')
    column_filters = ('username', 'email')

    def __init__(self, session, **kwargs):
        	   super(UserModelView, self).__init__(User, session, **kwargs)
   
class PerformModelView(ModelView):
    """View function of Flask-Admin for Models page."""
    def is_accessible(self):
        if current_user.is_authenticated and current_user.username =='admin':
        	return True

    # Using the CKTextAreaField to replace the Field name is ``
    form_overrides = {
        'content': CKTextAreaField,
	'complete':CKTextAreaField,
	'remarks':CKTextAreaField,
    }

    #可以联网时用
    #extra_js = ['http://cdn.ckeditor.com/4.6.0/full/ckeditor.js']

    #不可联网时
    create_template = 'admin/edit_client.html'
    edit_template = 'admin/edit_client.html'

    column_labels = dict(date=u'日期',name=u'姓名',place=u'工作地点',content=u'工作内容',complete=u'完成情况',integration=u'积分',remarks=u'备注')
    column_list = ('date','name','place','content','complete','integration','remarks')
    column_searchable_list = ('name', 'date')
    column_filters = ('name', 'date')
    def __init__(self, session, **kwargs):
        super(PerformModelView, self).__init__(Performance_Related, session, **kwargs)



class ClientModelView(ModelView):
    """View function of Flask-Admin for Models page."""
    def is_accessible(self):
        if current_user.is_authenticated and current_user.username =='admin':
        	return True

    # Using the CKTextAreaField to replace the Field name is ``
    form_overrides = {
        'tract': CKTextAreaField
    }

    #可以联网时用
    #extra_js = ['http://cdn.ckeditor.com/4.6.0/full/ckeditor.js']

    #不可联网时
    create_template = 'admin/edit_client.html'
    edit_template = 'admin/edit_client.html'


    column_labels = dict(client_no=u'客户编号',service_no=u'服务编号',company_name=u'公司名称',license=u'执照编号',contact=u'联系人',position=u'职位',telephone=u'手机号码',cellphone=u'固定电话',email=u'邮箱',qq=u'QQ或微信',adress=u'详细地址',saler=u'业务代表',status=u'状态',tract=u'跟踪')
    column_list =('client_no','service_no','company_name','license','contact','position','telephone','cellphone','email','qq','adress','saler','status','tract')
    column_searchable_list = ('saler','company_name','status')
    column_filters = ('company_name','saler','status')
    def __init__(self, session, **kwargs):
        super(ClientModelView, self).__init__(Clients, session, **kwargs)








# models_list = [Role, User]
# for model in models_list:

# flask_admin.add_view(ModelView(User,db.session))    

