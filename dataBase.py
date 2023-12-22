import pymysql
import redis
from pymysql import MySQLError
import time, datetime

class FindAuth:
    def __init__(self):
        # 连接MySQL数据库
        try:
            self.conn = pymysql.connect(host='127.0.0.1', port=3306,
                                        user='root', password='123456',
                                        database='data_db', charset='utf8')
        except Exception as error:
            print('连接MySQL出现问题！')
            print('失败原因：', error)
            exit()

        try:
            # 建立redis连接池
            self.conn_pool = redis.ConnectionPool(host='1.1.1.1', port=6379, db=0, decode_responses=True,
                                                  password='111111')
            # 客户端0连接数据库
            self.r0 = redis.StrictRedis(connection_pool=self.conn_pool)
        except Exception as error:
            print('连接redis出现问题！')
            print('失败原因：', error)
            exit()

# 查询连接权限
def get_data(self, src_ip, dst_ip, dst_port):
    src_ip, dst_ip, dst_port = str(src_ip), str(dst_ip), str(dst_port)
    # redis string表key
    find_info = src_ip + ':' + dst_ip + ':' + dst_port
    # print(find_info)

    # 先查询redis数据库是否存在数据,如果存在数据则返回输出，若不存在则去MySQL中查询，然后再将结果更新到redis中
    result = self.r0.get(find_info)
    # 结果不为空 即redis存在查询的信息，直接输出信息,否则redis中不存在，需要查询MySQL
    if result:
        """
        每次在redis中更新或者写入数据都需要设置过期时间10分钟，然后每查询到一次就重置过期时间10分钟，
        若10分钟没有查询到这个数据，就会被清除。这样设置过期时间主要防止redis缓存数据过多，清除不常用缓存数据"""
        self.r0.expire(find_info, 600)
        # print(result)
        # 返回查询的权限结果
        return result
    else:
        with self.conn.cursor() as cursor:
            try:
                # 执行MySQL的查询操作
                cursor.execute('SELECT acc_auth FROM tb_as WHERE '
                               'src_ip=%s AND dst_ip=%s AND dst_port=%s', (src_ip, dst_ip, dst_port))
                result_sql = cursor.fetchall()
                # print(result_sql)
                if result_sql:
                    # 将查询结果更新写入redis数据库中
                    auth_res = result_sql[0][0]
                    # print(auth_res)
                    self.r0.set(find_info, auth_res)
                    self.r0.expire(find_info, 600)  # 设置过期时间
                    # 返回查询的权限结果
                    return auth_res
                else:
                    return 'NULL'
            except Exception as error:
                print(error)
            # finally:
            #     self.conn.close()

#获取数据库的所有记录并返回src_ip, dst_ip

def get_as(self, src_ip):
        with self.conn.cursor() as cursor:
            try:
                # 执行MySQL的查询操作
                cursor.execute('SELECT asc_as FROM tb_as_ascription WHERE ip=%s', (src_ip,))
                result_sql = cursor.fetchall()
                # print(result_sql)
                if result_sql:
                    print(result_sql[0][0])
                    return result_sql[0][0]
                else:
                    return 'NULL'
            except Exception as error:
                print(error)
            # finally:
            #     self.conn.close()