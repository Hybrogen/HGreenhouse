#-*- coding:utf-8 -*-

import time
import json

import pymysql

class HSQL(object):
    def __init__(self, data_base: str):
        self.data_base = data_base
        self.con = self.get_sql_connection()
        self.port_table = 'ports'
        self.port_fields = ['id', 'name', 'local']
        self.data_table = 'datas'
        self.data_fields = {
            'dht': ['temperature', 'humidity', 'check_datetime'],
            'light': ['light', 'check_datetime'],
        }

    def get_sql_connection(self):
        con = pymysql.connect(host = 'zinchon.com', port = 336, user = 'zinc', passwd = 'zinchon.cn', db = self.data_base, charset = 'utf8')
        return con

#####################          插入操作          ##########################

    def sql_insert(self, sql: str, save_data: list):
        try:
            cur = self.con.cursor()
            cur.execute(sql, save_data)
            self.con.commit()
            cur.close()
            return True
        except pymysql.err.OperationalError:
            return False
        except pymysql.err.InterfaceError:
            if cur: cur.close()
            if self.con: self.con.close()
            self.con = self.get_sql_connection()
            
    def dht_save(self, data: dict) -> bool:
        try:
            save_data = list()
            for k in ['pid', 'temperature', 'humidity']:
                save_data.append(data[k])
            save_data.append(time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time())))
        except KeyError:
            return False

        sql = f"insert into `dht_{self.data_table}`(`pid`, `temperature`, `humidity`, `check_datetime`) values(%s, %s, %s, %s)"
        return self.sql_insert(sql, save_data)

    def add_port(self, name: str, local: str):
        save_data = [name, local]

        sql = f"insert into `{self.port_table}`(`name`, `local`) values(%s, %s)"
        return self.sql_insert(sql, save_data)

#####################          查询操作          ##########################

    def sql_select(self, sql: str):
        try:
            cur = self.con.cursor()
            cur.execute(sql)
            rdata = cur.fetchall()
            cur.close()
            return rdata
        except Exception as e:
            # print(e)
            return None

    def get_ports(self, query_data: dict = None) -> dict:
        sql = f"select * from `{self.port_table}`"
        if query_data:
            for k in self.port_fields:
                if k in query_data:
                    sql += f" where `{k}` = {query_data[k]}"
                    break
        data = self.sql_select(sql)
        data = [dict(zip(self.port_fields, d)) for d in data]
        return data

    def get_data(self, query_data: dict) -> dict:
        data = dict()
        # 检查数据正确性
        if 'data_type' not in query_data:
            data['state'] = 'error'
            data['error_info']  = "缺少数据类型 (data_type = dht/light)"
            data['error_info'] += "\nLack data of (data_type = dht/light)"
            return data
        if 'pid' in query_data:
            pid = query_data['pid']
        else:
            ports_data = self.get_ports(query_data)
            if len(ports_data) > 1:
                data['state'] = 'error'
                data['error_info']  =  "数据库中存在重复 节点名或地点，请尝试用节点 id 搜索"
                data['error_info'] +=  "\nThere are multiple port_name or port_local in database, please try search by port_id"
                data['error_info'] += f"\n{json.dumps(ports_data)}"
                return data
            pid = ports_data[0]['id']

        # 生成 sql 语句
        fields = ', '.join([f"`{field}`" for field in self.data_fields[query_data['data_type']]])
        sql = f"SELECT {fields} FROM `{query_data['data_type']}_{self.port_table}` WHERE pid = {pid}"
        if 'query_num' in query_data:
            sql += f" ORDER BY id DESC LIMIT {query_data['query_num']}"
        elif 'start_date' in query_data and 'end_date' in query_data:
            sql += f" AND `check_datetime` BETWEEN '{query_data['start_date']}' AND '{query_data['end_date']}'"

        # 获取并返回数据
        rdata = self.sql_select(sql)
        data['data'] = [dict(zip(self.data_fields[query_data['data_type']], d)) for d in rdata]
        data['state'] = 'ok'
        return data

    def __del__(self):
        self.con.close()

if __name__ == '__main__':
    s = HSQL('HGreenhouse')
    # s.add_port('海洋神庙', '西弗纳海底')
    print(s.get_ports())
    # s.dht_save({
    #     'pid': 2,
    #     'temperature': 34.5,
    #     'humidity': 45,
    #     })

