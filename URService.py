from socket import *
import struct
#参考文档   https://www.universal-robots.com/articles/ur/interface-communication/remote-control-via-tcpip/
#          请先仔细阅读 "UR机器人与PC通讯.pdf" 非常重要！！！
#          按钮命令：Dashborad.pdf port:29999
#          机器人语言:Script.pdf(e/cb) port:30003
#          realtime 实时返回端口：Client_Interfaces.excel
#          author：王海峰 plutohfw@gmail.com
#          创建时间:   2023/4/21
#          最后维护时间:2023/4/11
#          注意：30003的realtime服务需要注意接收字长，字典里"MessageSize""的值

class urip():
    def __init__(self,ip):
        self.robot_ip=ip
    
    def UR_29999(self,function):
        soc = socket(AF_INET,SOCK_STREAM) 
        soc.connect((self.robot_ip,29999))
        msg = soc.recv(1024).decode()
        message ="%s\r\n"%function
        soc.send(message.encode())
        msg = soc.recv(1024).decode()
        print(msg)
        soc.close()

    def UR_30003Script(self,function):
        soc = socket(AF_INET,SOCK_STREAM) 
        soc.connect((self.robot_ip,30003))
        soc.send(function.encode('utf8'))
        soc.close()

    def UR_30003rt(self,Meaning):
        soc = socket(AF_INET,SOCK_STREAM) 
        soc.connect((self.robot_ip,30003))   
        dic= {'MessageSize': 'i', 'Time': 'd', 'q target': '6d', 'qd target': '6d', 'qdd target': '6d','I target': '6d',
            'M target': '6d', 'q actual': '6d', 'qd actual': '6d', 'I actual': '6d', 'I control': '6d',
            'Tool vector actual': '6d', 'TCP speed actual': '6d', 'TCP force': '6d', 'Tool vector target': '6d',
            'TCP speed target': '6d', 'Digital input bits': 'd', 'Motor temperatures': '6d', 'Controller Timer': 'd',
            'Test value': 'd', 'Robot Mode': 'd', 'Joint Modes': '6d', 'Safety Mode': 'd', 'empty1': '6d', 'Tool Accelerometer values': '3d',
            'empty2': '6d', 'Speed scaling': 'd', 'Linear momentum norm': 'd', 'SoftwareOnly': 'd', 'softwareOnly2': 'd', 'V main': 'd',
            'V robot': 'd', 'I robot': 'd', 'V actual': '6d', 'Digital outputs': 'd', 'Program state': 'd', 'Elbow position': '3d', 'Elbow velocity': '3d'}
        data=soc.recv(1220) 
        ii=range(len(dic))
        for key,i in zip(dic,ii):
            fmtsize=struct.calcsize(dic[key])
            info,data=data[0:fmtsize],data[fmtsize:]
            fmt="!"+dic[key]
            dic[key]=dic[key],struct.unpack(fmt, info)

        print(dic[Meaning])
        soc.close()
        return dic[Meaning]