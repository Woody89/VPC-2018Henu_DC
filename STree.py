#!/usr/bin/python
#-*- coding:utf-8 -*-
import socket
import json
import pymysql as mysql
import time
import os
# 链接Mysql数据库
db = mysql.connect(user="root",passwd="12589",db="AWC",host="localhost")
db.autocommit(True)
cur = db.cursor()
# 开始监控操作
print("********Welcome*********")
try:
    Port = input("Open monitoring Port:")
    address = ('', Port)
except:
    print("Monitoring port entered is incorrect! Please re-enter!")
    exit(0)
s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
s.bind(address)
while True:
    # 获取客户端发送过来的系统信息
    json_string, addr = s.recvfrom(2048)
    # 使用json包进行解析加载
    mylist = json.loads(json_string.decode('utf-8'))
    # print mylist
    print "已收到正在解析!"
    Host_Ip=mylist['Host_Ip']
    Out_Ip=mylist['Out_Ip']
    P_Time=mylist['P_Time']
    Host_Mac=mylist['Host_Mac']
    Host_Date=mylist['Host_Date']
    Os_Platform=mylist['Os_Platform']
    Os_Version=mylist['Os_Version']
    Architecture=mylist['Architecture']
    Machine=mylist['Machine']
    Node=mylist['Node']
    Processor=mylist['Processor']
    Sys_Name=mylist['Sys_Name']
    Pc_Name=mylist['Pc_Name']
    Login_Name=mylist['Login_Name']
    terminal=mylist['terminal']
    Cpu_Times_User=mylist['Cpu_Times_User']
    Cpu_CountP=mylist['Cpu_CountP']
    Cpu_CountL=mylist['Cpu_CountL']
    Boot_Time=mylist['Boot_Time']
    Disk_Usage=mylist['Disk_Usage']
    S_Memory=mylist['S_Memory']
    Python_Build=mylist['Python_Build']
    Python_Compiler=mylist['Python_Compiler']
    Python_Implementation=mylist['Python_Implementation']
    Python_Version=mylist['Python_Version']
    Mem_Total = mylist['Mem_Total']
    Mem_Available=mylist['Mem_Available']
    Mem_Percent=mylist['Mem_Percent']
    Mem_Used=mylist['Mem_Used']
    Mem_Free=mylist['Mem_Free']
    Cpu_User=mylist['Cpu_User']
    Cpu_System=mylist['Cpu_System']
    Cpu_Idle=mylist['Cpu_Idle']
    Cpu_Interrupt=mylist['Cpu_Interrupt']
    Cpu_Dpc=mylist['Cpu_Dpc']
    Swap_Used=mylist['Swap_Used']
    Swap_Free=mylist['Swap_Free']
    Swap_Percent=mylist['Swap_Percent']
    Swap_Sin=mylist['Swap_Sin']
    Swap_Sout=mylist['Swap_Sout']
    Disk_Used=mylist['Disk_Used']
    Disk_Free=mylist['Disk_Free']
    Disk_Percent=mylist['Disk_Percent']
    # 动态变化的Disk数据
    Read_Count=mylist['Read_Count']
    Write_Count=mylist['Write_Count']
    Read_Bytes=mylist['Read_Bytes']
    Write_Bytes=mylist['Write_Bytes']
    Read_Time=mylist['Read_Time']
    Write_Time=mylist['Write_Time']
    Bytes_Sent=mylist['Bytes_Sent']
    Bytes_Recv=mylist['Bytes_Recv']
    Packets_Sent=mylist['Packets_Sent']
    Packets_Recv=mylist['Packets_Recv']
    Host_IpS=Host_Ip.replace(".", "_");
    print Host_IpS
    cur.execute("show tables;")
    Row=cur.fetchall()
    if (Host_IpS,) not in Row:
        # 采集内存数据进行
        try:
            sql = """CREATE TABLE if not exists """+Host_IpS+""" (
                        P_Time     double NOT NULL,
                        Mem_Total    double,
                        Mem_Available  double,
                        Mem_Percent   double,
                        Mem_Used      double,
                        Mem_Free     double,
                        Cpu_User     double,
                        Cpu_System   double,
                        Cpu_Idle     double,
                        Cpu_Interrupt    double,
                        Cpu_Dpc        double,
                        Swap_Used      double,
                        Swap_Free      double,
                        Swap_Percent     double,
                        Swap_Sin     double,
                        Swap_Sout      double,
                        Disk_Used      double,
                        Disk_Free      double,
                        Disk_Percent     double,
                        Read_Count       double,
                        Write_Count      double,
                        Read_Bytes       double,
                        Read_Time      double,
                        Write_Time     double,
                        Bytes_Sent     double,
                        Bytes_Recv     double,
                        Packets_Sent     double,
                        Packets_Recv       double
                        )"""
            cur.execute(sql)
            print "成功创建数据库!"
        except IOError:
            print("Create Net_Info Failed!")
        pass

#开始插入循环数据信息
    try:
        sql = 'insert into '+Host_IpS+' value (%d,%d,%d,%d,%d,%d,%d,%d,%d,%d,%d,%d,%d,%d,%d,%d,%d,%d,%d,%d,%d,%d,%d,%d,%d,%d,%d,%d)' % (P_Time,Mem_Total,Mem_Available,Mem_Percent,Mem_Used,
               Mem_Free,Cpu_User,Cpu_System,Cpu_Idle,Cpu_Interrupt,Cpu_Dpc,Swap_Used,Swap_Free,Swap_Percent,Swap_Sin,Swap_Sout,
            Disk_Used,Disk_Free,Disk_Percent,Read_Count,Write_Count,Read_Bytes,Read_Time,Write_Time,Bytes_Sent,Bytes_Recv,Packets_Sent,Packets_Recv)
        cur.execute(sql)
        print "Ok！"
    except IOError:
        print("Create Net_Info Failed!")

#创建初始化总表
    cur.execute("show tables;")
    Row = cur.fetchall()
    if ('overview',) not in Row:
        print "没有存在的是数据表!"
        # 创建数据表SQL语句
        try:
            sql = """CREATE TABLE if not exists overview (
                     P_Time  double NOT NULL,
                     Host_Ip  CHAR(30),
                     Host_Mac CHAR(30),
                     Out_Ip   CHAR(30),
                     Host_Date  CHAR(30),
                     Os_Platform  CHAR(100),
                     Os_Version   CHAR(100),
                     Architecture CHAR(30),
                     Machine  CHAR(30),
                     Node  CHAR(30),
                     Processor   CHAR(60),
                     Sys_Name CHAR(30),
                     Pc_Name  CHAR(30),
                     Login_Name  CHAR(30),
                     terminal   CHAR(30),
                     Cpu_Times_User  double,
                     Cpu_CountP   int(11),
                     Cpu_CountL   int(11),
                     Boot_Time double,
                     Mem_Total  double,
                     Disk_Usage  double,
                     S_Memory   double,
                     Python_Build CHAR(30),
                     Python_Compiler  CHAR(30),
                     Python_Implementation  CHAR(30),
                     Python_Version   CHAR(30)
                     )"""
            cur.execute(sql)
            print "成功创建数据库!"
        except IOError:
            print("Create Net_Info Failed!")
            #开始查询是否已经存在记录
    cur.execute("select Host_Ip,Host_Mac from Overview")
    M=cur.fetchall()
    Host_Ip=str(Host_Ip)
    Host_Mac=str(Host_Mac)
    tup1 = (Host_Ip,Host_Mac)
    if tup1 not in M:
        print "新连接已经接入!"
        try:
            sql = "insert into Overview  value (%d,'%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s',%d,%s,%s,%d,%d,%d,%d,'%s','%s','%s','%s')" % (P_Time,Host_Ip,Host_Mac,Out_Ip,Host_Date,Os_Platform,Os_Version,Architecture,Machine,Node,Processor,Sys_Name,Pc_Name,Login_Name,terminal,Cpu_Times_User,Cpu_CountP,Cpu_CountL,Boot_Time,Mem_Total,Disk_Usage,S_Memory,Python_Build,Python_Compiler,Python_Implementation,Python_Version)
            cur.execute(sql)
            print "插入成功!"
        except IOError, e:
            print("Create Net_Info Failed!" + e)
connect.commit()
s.close()