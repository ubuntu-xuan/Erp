# -*- coding:utf-8 -*-
__author__ = 'xuan'

from flask import  Blueprint

main = Blueprint('main',__name__)


from . import repertory,orders,payment,errors,client,employee
