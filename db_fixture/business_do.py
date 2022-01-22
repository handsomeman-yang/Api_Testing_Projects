#!/usr/bin/env python
# _*_ coding:utf-8 _*_
__author__ = 'syang'

import os,sys
sys.path.append(os.path.dirname(os.path.dirname(__file__)))
from config import setting
from pymysql import connect,cursors
from pymysql.err import OperationalError
import configparser as cparser

# --------- 读取config.ini配置文件 ---------------
cf = cparser.ConfigParser()
cf.read(setting.TEST_CONFIG,encoding='UTF-8')
host = cf.get("mysqlconf","host")
port = cf.get("mysqlconf","port")
user = cf.get("mysqlconf","user")
password = cf.get("mysqlconf","password")
#指定库
db = cf.get("mysqlconf","db_name")

class Mysqlhelper:

    def __init__(self):
        try:
            # 连接数据库
            self.conn = connect(host = host,
                                user = user,
                                password = password,
                                db = db,
                                charset = 'utf8mb4',
                                cursorclass = cursors.DictCursor
                                )
            self.cur = self.conn.cursor()
        except OperationalError as e:
            print("Mysql Error %d: %s" % (e.args[0],e.args[1]))

    # 查找tenantid
    def findtenent(self,company_id):
        real_sql = "select tenant_id from sme_company where id =" + company_id
        cur = self.cur
        cur.execute(real_sql)
        result = cur.fetchone()
        return result

    # 根据公司编码查id
    def findcompanyid(self,client_code):
        real_sql = "select id from sme_company where client_code =" + client_code
        cur = self.cur
        cur.execute(real_sql)
        result = cur.fetchone()
        return result

    # 查询公司corehr同步配置
    def find_corehrsync_config(self,company_id):
        real_sql = "select a.core_hr_rule from sme_core_config a inner join sme_core_client b on a.client_id = b.id\
        where b.company_id =" + company_id + " and b.client_type = 2"
        cur = self.cur
        cur.execute(real_sql)
        result = cur.fetchone()
        return result

    # 查找员工一对多信息
    def findEmployeeInfo(self,company_id,emp_id):
        real_sql = "select count(*) from "
        cur = self.cur
        cur.execute(real_sql)
        result = cur.fetchone()
        return result