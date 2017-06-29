# -*- coding:utf-8 -*-
__author__ = 'xuan'

import  os



class Config:
    SECRET_KEY  = os.environ.get('SECRET_KEY') or 'hard to guess string'
    SQLALCHEMY_COMMIT_ON_TEARDOWM = True
    #配置邮件
    MAIL_SERVER = 'smtp.qq.com'
    MAIL_PORT = 587
    MAIL_USE_TLS = True
    MAIL_USERNAME = os.environ.get('MAIL_USERNAME')
    MAIL_PASSWORD = os.environ.get('MAIL_PASSWORD')
    ADMIN_MAIL_SENDER = os.environ.get('ADMIN_MAIL_SENDER')
    ADMIN_MAIL = os.environ.get('ADMIN_MAIL')
    MYSQL_PWD = os.environ.get('MYSQL_PWD')
    
    #合同上传

    UPLOAD_FOLDER = '/var/www/Erp/data/'
    THUMBNAIL_FOLDER = '/var/www/Erp/data/thumbnail/'
    #回执单上传
    UPLOADED_RECEIPT_FOLDER = '/var/www/Erp/data/receipts/'
    THUMBNAIL_RECEIPT_FOLDER = '/var/www/Erp/data/receipts/receipts_thumbnail/'





    MAX_CONTENT_LENGTH = 50 * 1024 * 1024

  






    @staticmethod
    def init_app(app):
        pass


class DevelopmentConfig(Config):
    DEBUG = True
    SQLALCHEMY_DATABASE_URI = os.environ.get('DEV_DATABASE_RUL') or \
        'mysql://root:uroot012@localhost:8808/erp_development'


class TestingConfig(Config):
    TESTING = True
    SQLALCHEMY_DATABASE_URI = os.environ.get('TEST_DATABASE_URL') or \
        'mysql://root:uroot012@localhost:8808/erp_testing'


class ProductionConfig(Config):
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or \
         'mysql://root:uroot012@localhost:8808/erp_production'

config = {
    'development': DevelopmentConfig,
    'testing': TestingConfig,
    'production': ProductionConfig,

    'default': DevelopmentConfig
}
