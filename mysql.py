# -*- coding:utf-8 -*-
__author__ = 'xuan'

import json,MySQLdb,sys

def reset():
    for i in range(43,72):
        print i
        try:

            database = MySQLdb.connect("localhost","root","uroot012","erp_development",charset='utf8')
            cursor = database.cursor()
        except:
            print 'MySQL connect fail...'

        #sql = "alter table fittings_output%s add column belongs char(4);"%i
        #sql = "update  fittings_output%s set belongs=%s;"%(i,i-3)  
        #sql = "update  fittings_input%s set belongs=%s;"%(i,i-3)

        #sql = "insert into fittings_inputs(dates,nums,price,suppliers,examine,sendee,remarks,belongs) select dates,nums,price,suppliers,examine,sendee,remarks,belongs from fittings_input%s;"%i

        #sql = "insert into fittings_outputs(dates,nums,purpose,receiptor,belongs) select dates,nums,purpose,receiptor,belongs from fittings_output%s;"%i
        sql = "drop table fittings_output%s"%i

        print sql
        cursor.execute(sql)
        cursor.close()
        database.commit()
        database.close()

            

reset()
