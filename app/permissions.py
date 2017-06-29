# -*- coding:utf-8 -*-
__author__ = 'xuan'

from flask_principal import  Principal,Permission,RoleNeed,UserNeed,identity_loaded

principals = Principal()

admin_permission =  Permission(RoleNeed('admin'))
moderator_permission =  Permission(RoleNeed('moderator'))
default_permission =  Permission(RoleNeed('defalut'))