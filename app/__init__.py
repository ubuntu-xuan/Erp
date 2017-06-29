# -*- coding:utf-8 -*-
__author__ = 'xuan'

from flask import Flask,session
from flask.ext.mail import Mail
from config import  config
from flask_admin import Admin
from admin.admin import MyView,PerformModelView,ClientModelView
from flask_login import logout_user,login_required,login_user,current_user


# from .models import User
import os.path as op

from flask_babelex import Babel  #在本地上这里有用flask_babelex 服务器上用flask_babel ？

#from Erp.app.models import db,User
#from .models import User

# from .models import User

from models import db,User,login_manager
from flask_admin import AdminIndexView


#from flask.ext.superadmin import Admin,BaseView,expose
# from flask.ext.admin import Admin,BaseView,expose
# from flask.ext.admin import Admins
#from admin.admin import MyView
#from . import  db
from flask.ext.admin.contrib.sqla import ModelView
# from flask.ext.admin.contrib.fileadmin import FileAdmin
from  admin.admin import UserModelView
from  permissions import principals,identity_loaded,UserNeed,RoleNeed

mail = Mail()




# flask_admin.add_view(CustomModelView(db.session, name='Models'))   



my_admin = Admin(name='Admin',template_mode='bootstrap3',
                                    index_view=AdminIndexView(
                                    template='admin/custom.html',
                                    url='/admin'
                                    ))

#my_admin.add_view(MyView(name='myview'))
my_admin.add_view(UserModelView(db.session,name=u"用户",category='Models'))    
my_admin.add_view(PerformModelView(db.session,name=u"绩效",category='Models'))  
my_admin.add_view(ClientModelView(db.session,name=u"客户管理",category='Models'))      


# models_list = [Role, User]
# for model in models_list:
#     my_admin.add_view(CustomModelView(model, db.session, category='Models'))   

def create_app(config_name):
    app = Flask(__name__)
    app.debug = False
    app.config.from_object(config[config_name])
    config[config_name].init_app(app)

    db.init_app(app)
    mail.init_app(app)
    login_manager.init_app(app)
    babel = Babel(app)

    @babel.localeselector
    def get_locale():
        override = 'zh_CN'
        if override:
             session['lang'] = override
        return session.get('lang', 'en')

    my_admin.init_app(app)

    principals.init_app(app)
    @identity_loaded.connect_via(app)
    def on_identity_loaded(sender,identity):
        '''
            Change the role via add the Need object into Role.
            Need the access the app object.
        ''' 
        #Set the identity user object
        identity.user = current_user
    
        # Add the UserNeed to the identity user object
        if hasattr(current_user, 'id'):
            identity.provides.add(UserNeed(current_user.id))

        # Add each role to the identity user object
        if hasattr(current_user, 'roles'):
            for role in current_user.roles:
                identity.provides.add(RoleNeed(role.name))



    from .main import main as main_blueprint
    app.register_blueprint(main_blueprint)

    from .auth import auth as auth_blueprint
    app.register_blueprint(auth_blueprint)

    # from .admin import admin as admin_blueprint
    # app.register_blueprint(admin_blueprint)


    return app
