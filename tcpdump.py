"""
利用python实时获取tcpdump的监控数据，并将其发送给服务端：
在网络结构中，主要是监听网卡的网络数据信息
通过抓包就可以知道服务端到客户端的访问，并通过本系统的处理，就可以实现访问认证。
"""

import subprocess
import socket
import time


class GrabBag:
    def __init__(self, ipaddr, port):
        self.ipaddr = ipaddr
        self.port = port

    def py_tcpdump_as1(self):
        c1 = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        c1.connect((self.ipaddr, self.port))
        proc = subprocess.Popen('tcpdump dst host  -l -i  and tcp -n',
                                stdout=subprocess.PIPE, shell=True)

        while True:
            line = proc.stdout.readline().decode(encoding='utf-8')
            line = line.strip()
            if not line:
                print('tcpdump finished...')
                break
            print(line)
            c1.send(line.encode())
            time.sleep(0.3)
