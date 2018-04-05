#!/usr/bin/python2.7
#-*- coding:utf-8 -*-
import socket
import json
import psutil
import time
import os
import uuid
import platform
import requests
try:
    IP = raw_input("Master point IP:")
    Port = input("Master point Port:")
    address = (IP, Port)
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
except:
    pass

# 获取外网IP
def get_out_ip():
    url = r'http://1212.ip138.com/ic.asp'
    # r = requests.get(url)
    # txt = r.text
    # ip = txt[txt.find("[") + 1: txt.find("]")]
    ip='8.8.8.8'
    print('ip:' + ip)
    return ip

# 获取主机局域网ip地址
def get_host_ip():
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.connect(('8.8.8.8', 80))
        ip = s.getsockname()[0]
    finally:
        s.close()
    return ip
def get_host_Time():
    try:
        time_local = time.localtime(time.time())
        dt = time.strftime("%Y-%m-%d %H:%M:%S", time_local)
    finally:
        pass
    return dt
def get_mac():
  mac_num = hex(uuid.getnode()).replace('0x', '').upper()
  mac = ':'.join(mac_num[i : i + 2] for i in range(0, 11, 2))
  return mac
if __name__ == '__main__':

     Out_Ip = get_out_ip()  # 获取外网Ip
     Host_Ip = get_host_ip()  # 获取计算机内网IP
     Host_Mac = get_mac()  # 获取Mac地址
     Os_Platform = platform.platform()  # 获取操作系统名称及版本号，'Linux-3.13.0-46-generic-i686-with-Deepin-2014.2-trusty'
     Os_Version = platform.version()  # 获取操作系统版本号，'#76-Ubuntu SMP Thu Feb 26 18:52:49 UTC 2015'
     Architecture0 = platform.architecture()[0]  # 获取操作系统的位数，('32bit', 'ELF')
     Architecture1 = platform.architecture()[1]  # 获取操作系统的位数，('32bit', 'ELF')
     Architecture = Architecture0 + "---" + Architecture1  # print("架构:"+Architecture)
     Machine = platform.machine()  # 计算机类型，'i686'
     Node = platform.node()  # 计算机的网络名称，'XF654'
     Processor = platform.processor()  # 计算机处理器信息，''i686'（名称）
     Sys_Name = platform.system()  # 系统名称
     Pc_Name = socket.getfqdn(socket.gethostname())  # 获取本机电脑名
     # 关于python的信息
     Python_Build = platform.python_build()  # python版本发行日期
     Python_Compiler = platform.python_compiler()  # python发行版本的编译环境
     Python_Implementation = platform.python_implementation()  # 编译条约
     Python_Version = platform.python_version()  # python的发行版本
     while 1:
         # 通过函数获取网卡信息暂时不会使用其中的信息
         P_Time=time.time()#时间戳
         Host_Date = get_host_Time()  # 获取计算机日期
         #获取动态变化的参数信息留作后用
         Mem= psutil.virtual_memory()#所有的内存信息
         Cpu_Times = psutil.cpu_times()  # Cpu所有可见信息
         Swap_Memory=psutil.swap_memory()#交换分区的信息
         D_Usage = psutil.disk_usage('C:/')#获取所有分区的信息(Window平台 )
         # D_Usage = psutil.disk_usage('/')  # 获取所有分区的信息(Linux平台)
         Users = psutil.users()  # 系统使用的用户
         Disk_Io_Counters=psutil.disk_io_counters()  # 使用psutil.disk_io_counters获取硬盘总的IO个数、 读写信息
         Net_Io_Counters=psutil.net_io_counters()#使用psutil.net_io_counters获取网络总的IO信息，默认pernic=False
         # 开始采集系统的Cpu  内存    disk 网络 固定的信息参数
         Login_Name = Users[0][0]  # 登录的用户名
         terminal = Users[0][1]  # terminal名称
         Pid = Users[0][4]  # 使用中的PId
         Cpu_Times_User=psutil.cpu_times().user #获取单项数据信息，如用户user的CPU时间比
         Cpu_CountP=psutil.cpu_count() #获取CPU的逻辑个数，默认logical=True4
         Cpu_CountL=psutil.cpu_count(logical=False)#获取Cpu逻辑个f数
         Boot_Time=psutil.boot_time()#获取系统开机时间
         Mem_Total=Mem.total#PC的总内存
         Disk_Usage=D_Usage[0]#主区的总存储量
         S_Memory=Swap_Memory[0]#交换分区的容量
         # 将数据存储到字典中之后将数据发送到中心数据采集点
         mylist = dict()
         mylist['P_Time']=P_Time
         mylist['Host_Ip']=Host_Ip
         mylist['Host_Mac']=Host_Mac
         mylist['Out_Ip']=Out_Ip
         mylist['Host_Date']=Host_Date
         mylist['Os_Platform']=Os_Platform
         mylist['Os_Version']=Os_Version
         mylist['Architecture']=Architecture
         mylist['Machine']=Machine
         mylist['Node']=Node
         mylist['Processor']=Processor
         mylist['Sys_Name']=Sys_Name
         mylist['Pc_Name']=Pc_Name
         mylist['Login_Name']=Login_Name
         mylist['terminal']=terminal
         mylist['Pid']=Pid
         mylist['Cpu_Times_User']=Cpu_Times_User
         mylist['Cpu_CountP']=Cpu_CountP
         mylist['Cpu_CountL']=Cpu_CountL
         mylist['Boot_Time']=Boot_Time
         mylist['Mem_Total']=Mem_Total
         mylist['Disk_Usage']=Disk_Usage
         mylist['S_Memory']=S_Memory
         mylist['Python_Build']=Python_Build[1]
         mylist['Python_Compiler']=Python_Compiler
         mylist['Python_Implementation']=Python_Implementation
         mylist['Python_Version']=Python_Version
         #动态变化的内存信息
         mylist['Mem_Available']=Mem[1]
         mylist['Mem_Percent'] = Mem[2]
         mylist['Mem_Used'] = Mem[3]
         mylist['Mem_Free'] = Mem[4]
         #动态变化的Cpu
         mylist['Cpu_User']=Cpu_Times[0]
         mylist['Cpu_System'] = Cpu_Times[0]
         mylist['Cpu_Idle'] = Cpu_Times[0]
         mylist['Cpu_Interrupt'] = Cpu_Times[0]
         mylist['Cpu_Dpc'] = Cpu_Times[0]
         # 动态变化的Swap信息
         mylist['Swap_Used']=Swap_Memory[1]
         mylist['Swap_Free'] = Swap_Memory[2]
         mylist['Swap_Percent'] = Swap_Memory[3]
         mylist['Swap_Sin'] = Swap_Memory[4]
         mylist['Swap_Sout'] = Swap_Memory[5]
         #动态变化的磁盘情况
         mylist['Disk_Used']=D_Usage[1]
         mylist['Disk_Free'] = D_Usage[2]
         mylist['Disk_Percent'] = D_Usage[3]
         #动态变化的Disk数据
         mylist['Read_Count']=Disk_Io_Counters[0]
         mylist['Write_Count'] = Disk_Io_Counters[1]
         mylist['Read_Bytes'] = Disk_Io_Counters[2]
         mylist['Write_Bytes'] = Disk_Io_Counters[3]
         mylist['Read_Time'] = Disk_Io_Counters[4]
         mylist['Write_Time'] = Disk_Io_Counters[5]
         #网络流量速度
         mylist['Bytes_Sent'] =Net_Io_Counters[0]
         mylist['Bytes_Recv'] = Net_Io_Counters[1]
         mylist['Packets_Sent'] = Net_Io_Counters[2]
         mylist['Packets_Recv'] = Net_Io_Counters[3]
         print "正在采集数据信息!"
         json_string = json.dumps(mylist)  # 使用json文件进行传输
         s.sendto(json_string.encode('utf-8'), address)
         time.sleep(3)
s.close()

