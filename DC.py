#-*- coding:utf-8 -*-
import logging
import logging.config
import os.path
import tornado.httpserver
import tornado.ioloop
import tornado.options
import tornado.web
import platform
import pymysql as mysql
import json
con = mysql.connect(user='root',passwd='12589',host='localhost',db='awc')
con.autocommit(True)
cur = con.cursor()
from tornado.options import define, options
define("port", default=8080, help="run on the given port", type=int)
tmp_time=0
# create logger
logger = logging.getLogger('simple_example')
logger.setLevel(logging.DEBUG)
# 获取Ip函数，获取采集的固定信息表进行聚合数据展示
def Arr_Ip():
    arr = []
    sql = 'select Host_Ip from overview'
    cur.execute(sql)
    arr = cur.fetchall()
    return arr
def All_Info():
    arr = []
    sql = 'select * from overview'
    cur.execute(sql)
    arr = cur.fetchall()
    return arr
def StatisticsAll_Info(IP_OPT):
    arr = []
    print IP_OPT
    sql = "select * from overview where Host_ip='%s' "% (IP_OPT)
    cur.execute(sql)
    arr = cur.fetchall()
    return arr
def MemoryInfo():
    arr = []
    C_IP=Get_FistIp()
    sql = 'select * from ' + C_IP+" ORDER BY P_Time DESC limit 1 "
    cur.execute(sql)
    arr = cur.fetchall()
    return arr
def StatisticsInfo(IP_OPT):
    arr = []
    sql = 'select * from ' + IP_OPT+" ORDER BY P_Time DESC limit 1 "
    cur.execute(sql)
    arr = cur.fetchall()
    return arr
# 获取当前主机监控IP地址并赋值在全局变量,使其可以感应到参数变化
def get_IP(IP_OPT):
    print "我可以写数据"
    global C_IP
    C_IP=IP_OPT
    print C_IP

def Ch_IP(IP_OPT):
    global C_IP
    C_IP=IP_OPT.replace(".","_")
    print C_IP
    pass
# 获取第一个Ip
def Get_FistIp():
    IP_OPT = Arr_Ip()[0][0].replace(".", "_");
    return IP_OPT
# 获取其中第一个Ip信息
def get_FistIpMem(IP_OPT):
    arr = []
    sql = "select * from overview WHERE Host_Ip='%s'" % (IP_OPT)
    cur.execute(sql)
    arr = cur.fetchall()
    return arr
#     首页加载文件
class IndexHandler(tornado.web.RequestHandler):
    def get(self):
        print All_Info()
        self.render('index.html',Arr_Ip=Arr_Ip(),All_Info=All_Info(),cur=cur)

# 加载Summary页面信息
class SummaryHandler(tornado.web.RequestHandler):
    def get(self):
        IP_OPT=Get_FistIp()
        IP_OPT =IP_OPT.replace("_",".");
        print IP_OPT
        arr = get_FistIpMem(IP_OPT)
        print arr
        self.render('summary.html',Arr_Ip=Arr_Ip(),arr=arr[0],All_Info=All_Info(),cur=cur)
    def post(self):
        IP_OPT=str(self.get_argument("IP_OPT"))
        get_IP(IP_OPT)
        arr = get_FistIpMem(IP_OPT)
        self.render('summary_base.html',Arr_Ip=Arr_Ip(),arr=arr[0],All_Info=All_Info(),cur=cur)

class StatisticsHandler(tornado.web.RequestHandler):
    def get(self):
        arr = []
        IP_OPT = Get_FistIp()
        arr = MemoryInfo()
        print arr[0]
        self.render('statistics.html',Arr_Ip=Arr_Ip(),arr=arr[0],All_Info=All_Info(),)
    def post(self):
        IP_OPT1=str(self.get_argument("IP_OPT"))
        IP_OPT=Ch_IP(IP_OPT1)
        arr =StatisticsInfo(C_IP)
        self.render('statistics_base.html', Arr_Ip=Arr_Ip(), arr=arr[0],All_Info=StatisticsAll_Info(IP_OPT1))
#    系统处理日志的页面
class LogsHandler(tornado.web.RequestHandler):
    def get(self):
        # self.render('logs.html',Arr_Ip=Arr_Ip())
        self.render('logs.html', Arr_Ip=Arr_Ip())
# 指向日历的页面
class CalendarHandler(tornado.web.RequestHandler):
    def get(self):
        self.render('calendar.html',Arr_Ip=Arr_Ip())

# 当前内存使用情况
class MemoryUsedLineDataHandler(tornado.web.RequestHandler):
    def get(self):
 # 间隔获取数据
        global tmp_time
        if tmp_time > 0:
            sql = 'select Mem_Used,P_Time from ' + C_IP+' where P_Time>%s ' % (tmp_time / 1000)
        else:
            sql = 'select Mem_Used,P_Time from ' + C_IP
        cur.execute(sql)
        arr = []
        for i in cur.fetchall():
            arr.append([i[1] * 1000, i[0]])
        if len(arr) > 0:
            tmp_time = arr[-1][0]
            print tmp_time
        self.write(json.dumps(arr))

 # 当前内存剩余量情况
class MemoryFreeLineDataHandler(tornado.web.RequestHandler):
    def get(self):
        # 间隔获取数据
        global tmp_time
        if tmp_time > 0:
            sql = 'select Mem_Free,P_Time from ' + C_IP + ' where P_Time>%s ' % (tmp_time / 1000)
        else:
            sql = 'select Mem_Free,P_Time from ' + C_IP
        cur.execute(sql)
        arr = []
        for i in cur.fetchall():
            arr.append([i[1] * 1000, i[0]])
        if len(arr) > 0:
            tmp_time = arr[-1][0]
            print tmp_time
        self.write(json.dumps(arr))

# 当前内存使用情况
class CpuUsedLineDataHandler(tornado.web.RequestHandler):
    def get(self):
        # 间隔获取数据
        global tmp_time
        if tmp_time > 0:
            sql = 'select Cpu_User,P_Time from ' + C_IP + ' where P_Time>%s ' % (tmp_time / 1000)
        else:
            sql = 'select Cpu_User,P_Time from ' + C_IP
        cur.execute(sql)
        arr = []
        for i in cur.fetchall():
            arr.append([i[1] * 1000, i[0]])
        if len(arr) > 0:
            tmp_time = arr[-1][0]
            print tmp_time
        self.write(json.dumps(arr))

# Cpu系统使用情况
class CpuSystemLineDataHandler(tornado.web.RequestHandler):
       def get(self):
                # 间隔获取数据
                global tmp_time
                if tmp_time > 0:
                    sql = 'select Cpu_System,P_Time from ' + C_IP + ' where P_Time>%s ' % (tmp_time / 1000)
                else:
                    sql = 'select Cpu_System,P_Time from ' + C_IP
                cur.execute(sql)
                arr = []
                for i in cur.fetchall():
                    arr.append([i[1] * 1000, i[0]])
                if len(arr) > 0:
                    tmp_time = arr[-1][0]
                    print tmp_time
                self.write(json.dumps(arr))
# 当前Swap内存使用情况
class SwapUserLineDataHandler(tornado.web.RequestHandler):
    def get(self):
        # 间隔获取数据
        global tmp_time
        if tmp_time > 0:
            sql = 'select Swap_Used,P_Time from ' + C_IP + ' where P_Time>%s ' % (tmp_time / 1000)
        else:
            sql = 'select Swap_Used,P_Time from ' + C_IP
        cur.execute(sql)
        arr = []
        for i in cur.fetchall():
            arr.append([i[1] * 1000, i[0]])
        if len(arr) > 0:
            tmp_time = arr[-1][0]
            print tmp_time
        self.write(json.dumps(arr))
# Swap  Free数据
class SwapFreeLineDataHandler(tornado.web.RequestHandler):
    def get(self):
        # 间隔获取数据
        global tmp_time
        if tmp_time > 0:
            sql = 'select Swap_Free,P_Time from ' + C_IP + ' where P_Time>%s ' % (tmp_time / 1000)
        else:
            sql = 'select Swap_Free,P_Time from ' + C_IP
        cur.execute(sql)
        arr = []
        for i in cur.fetchall():
            arr.append([i[1] * 1000, i[0]])
        if len(arr) > 0:
            tmp_time = arr[-1][0]
            print tmp_time
        self.write(json.dumps(arr))

    # 当前Disk已经使用情况
class DiskUserLineDataHandler(tornado.web.RequestHandler):
         def get(self):
            # 间隔获取数据
            global tmp_time
            if tmp_time > 0:
                sql = 'select Disk_Used,P_Time from ' + C_IP + ' where P_Time>%s ' % (tmp_time / 1000)
            else:
                sql = 'select Disk_Used,P_Time from ' + C_IP
            cur.execute(sql)
            arr = []
            for i in cur.fetchall():
                arr.append([i[1] * 1000, i[0]])
            if len(arr) > 0:
                tmp_time = arr[-1][0]
                print tmp_time
            self.write(json.dumps(arr))

    #硬盘剩余情况明细
class DiskFreeLineDataHandler(tornado.web.RequestHandler):
        def get(self):
            # 间隔获取数据
            global tmp_time
            if tmp_time > 0:
                sql = 'select Disk_Free,P_Time from ' + C_IP + ' where P_Time>%s ' % (tmp_time / 1000)
            else:
                sql = 'select Disk_Free,P_Time from ' + C_IP
            cur.execute(sql)
            arr = []
            for i in cur.fetchall():
                arr.append([i[1] * 1000, i[0]])
            if len(arr) > 0:
                tmp_time = arr[-1][0]
                print tmp_time
            self.write(json.dumps(arr))

        # 当前ReadCount内存使用情况
class ReadCountLineDataHandler(tornado.web.RequestHandler):
    def get(self):
                # 间隔获取数据
                global tmp_time
                if tmp_time > 0:
                    sql = 'select Read_Count,P_Time from ' + C_IP + ' where P_Time>%s ' % (tmp_time / 1000)
                else:
                    sql = 'select Read_Count,P_Time from ' + C_IP
                cur.execute(sql)
                arr = []
                for i in cur.fetchall():
                    arr.append([i[1] * 1000, i[0]])
                if len(arr) > 0:
                    tmp_time = arr[-1][0]
                    print tmp_time
                self.write(json.dumps(arr))

# WriteCountLine数据
class WriteCountLineDataHandler(tornado.web.RequestHandler):
    def get(self):
            # 间隔获取数据
            global tmp_time
            if tmp_time > 0:
                sql = 'select Write_Count,P_Time from ' + C_IP + ' where P_Time>%s ' % (tmp_time / 1000)
            else:
                sql = 'select Write_Count,P_Time from ' + C_IP
                cur.execute(sql)
                arr = []
            for i in cur.fetchall():
                arr.append([i[1] * 1000, i[0]])
            if len(arr) > 0:
                tmp_time = arr[-1][0]
                print tmp_time
            self.write(json.dumps(arr))

# Bytes_SendLine数据
class Bytes_SendLineDataHandler(tornado.web.RequestHandler):
    def get(self):
            # 间隔获取数据
            global tmp_time
            if tmp_time > 0:
                sql = 'select Bytes_Sent,P_Time from ' + C_IP + ' where P_Time>%s ' % (tmp_time / 1000)
            else:
                sql = 'select Bytes_Sent,P_Time from ' + C_IP
                cur.execute(sql)
                arr = []
            for i in cur.fetchall():
                arr.append([i[1] * 1000, i[0]])
            if len(arr) > 0:
                tmp_time = arr[-1][0]
                print tmp_time
            self.write(json.dumps(arr))
# WriteCountLine数据
class BytesRecvLineDataHandler(tornado.web.RequestHandler):
    def get(self):
            # 间隔获取数据
            global tmp_time
            if tmp_time > 0:
                sql = 'select Bytes_Recv,P_Time from ' + C_IP + ' where P_Time>%s ' % (tmp_time / 1000)
            else:
                sql = 'select Bytes_Recv,P_Time from ' + C_IP
                cur.execute(sql)
                arr = []
            for i in cur.fetchall():
                arr.append([i[1] * 1000, i[0]])
            if len(arr) > 0:
                tmp_time = arr[-1][0]
                print tmp_time
            self.write(json.dumps(arr))

# WriteCountLine数据
class PacketsSendLineDataHandler(tornado.web.RequestHandler):
    def get(self):
            # 间隔获取数据
            global tmp_time
            if tmp_time > 0:
                sql = 'select Pakets_Sent,P_Time from ' + C_IP + ' where P_Time>%s ' % (tmp_time / 1000)
            else:
                sql = 'select Pakets_Sent,P_Time from ' + C_IP
                cur.execute(sql)
                arr = []
            for i in cur.fetchall():
                arr.append([i[1] * 1000, i[0]])
            if len(arr) > 0:
                tmp_time = arr[-1][0]
                print tmp_time
            self.write(json.dumps(arr))
# WriteCountLine数据
class PacketsRecvLineDataHandler(tornado.web.RequestHandler):
    def get(self):
            # 间隔获取数据
            global tmp_time
            if tmp_time > 0:
                sql = 'select Pakets_Recv,P_Time from ' + C_IP + ' where P_Time>%s ' % (tmp_time / 1000)
            else:
                sql = 'select Pakets_Recv,P_Time from ' + C_IP
                cur.execute(sql)
                arr = []
            for i in cur.fetchall():
                arr.append([i[1] * 1000, i[0]])
            if len(arr) > 0:
                tmp_time = arr[-1][0]
                print tmp_time
            self.write(json.dumps(arr))

#内存饼图展示数据
class MemoryPerHandler(tornado.web.RequestHandler):
    def get(self):
        # 间隔获取数据
        global tmp_time
        IP_OPT=Get_FistIp()
        if tmp_time > 0:
            sql = 'select Mem_Percent,P_Time from '+IP_OPT+' where P_Time>%s limit 1 ' % (tmp_time / 1000)
            print "数据更新"
        else:
            sql = 'select Mem_Percent,P_Time from '+IP_OPT+' ORDER BY P_Time DESC limit 1 '
            print "数据未更新"
        cur.execute(sql)
        arr = []
        Res = cur.fetchall()[0]
        arr.append(["Mem_Available", Res[0]])
        arr.append(["Mem_Used", (100-Res[0])])
        tmp_time=Res[1]*1000
        self.write(json.dumps(arr))

# Swap  饼状图容量使用情况
class SwapPerHandler(tornado.web.RequestHandler):
    def get(self):
        # 间隔获取数据
        global tmp_time
        IP_OPT=Get_FistIp()
        if tmp_time > 0:
            sql = 'select Swap_Percent,P_Time from '+IP_OPT+' where P_Time>%s limit 1' % (tmp_time / 1000)
        else:
            sql = 'select Swap_Percent,P_Time from '+IP_OPT+' ORDER BY P_Time DESC limit 1'
        cur.execute(sql)
        arr = []
        Res = cur.fetchall()[0]
        arr.append(["Swap_Available", Res[0]])
        arr.append(["Swap_Used", (100-Res[0])])
        tmp_time=Res[1]*1000
        self.write(json.dumps(arr))
# Disk 硬盘容量使用情况
class DiskPerHandler(tornado.web.RequestHandler):
    def get(self):
        # 间隔获取数据
        global tmp_time
        IP_OPT=Get_FistIp()
        if tmp_time > 0:
            sql = 'select Disk_Percent,P_Time from '+IP_OPT+' where P_Time>%s limit 1' % (tmp_time / 1000)
        else:
            sql = 'select Disk_Percent,P_Time from '+IP_OPT+' ORDER BY P_Time DESC limit 1'
        cur.execute(sql)
        arr = []
        Res = cur.fetchall()[0]
        arr.append(["Disk_Available", Res[0]])
        arr.append(["Disk_Used", (100-Res[0])])
        tmp_time=Res[1]*1000
        self.write(json.dumps(arr))

# Disk 硬盘容量使用情况
class RW_TimePerHandler(tornado.web.RequestHandler):
    def get(self):
        # 间隔获取数据
        global tmp_time
        IP_OPT=Get_FistIp()
        if tmp_time > 0:
            sql = 'select Read_Time,Write_Time,P_Time from '+IP_OPT+' where P_Time>%s limit 1' % (tmp_time / 1000)
        else:
            sql = 'select Read_Time,Write_Time,P_Time from '+IP_OPT+' ORDER BY P_Time DESC limit 1'
        cur.execute(sql)
        arr = []
        Res = cur.fetchall()[0]
        arr.append(["Read_Time", Res[0]])
        arr.append(["Write_Time", Res[1]])
        tmp_time=Res[2]*1000
        self.write(json.dumps(arr))

# 3d散点数据
class DDHandler(tornado.web.RequestHandler):
    def get(self):
        # 间隔获取数据
        global tmp_time
        IP_OPT=Get_FistIp()
        if tmp_time > 0:
            sql = 'select Mem_Used,Cpu_User,P_Time from '+IP_OPT+' where P_Time>%s limit 1' % (tmp_time / 1000)
        else:
            sql = 'select Mem_Used,Cpu_User,P_Time from '+IP_OPT+' ORDER BY P_Time DESC limit 1'
        cur.execute(sql)
        arr = []
        Res = cur.fetchall()[0]
        arr.append([Res[0]])
        arr.append([Res[1]])
        arr.append([Res[2]])
        tmp_time=Res[2]*1000
        self.write(json.dumps(arr))

class AjaxHandler(tornado.web.RequestHandler):
    def post(self):
        print self.get_argument("message")
        self.write(self.get_argument("message"))
        self.render('tt.html')

# Overview测试页面
class OverviewHandler(tornado.web.RequestHandler):
    def get(self):
        # IP= self.get_argument("message")
        self.render('Overview.html')

class CpuHandler(tornado.web.RequestHandler):
    def get(self):
        # IP= self.get_argument("message")
        self.render('Cpu.html')

class MemeryHandler(tornado.web.RequestHandler):
    def get(self):
        # IP= self.get_argument("message")
        self.render('Memery.html')

class SwapHandler(tornado.web.RequestHandler):
    def get(self):
        # IP= self.get_argument("message")
        self.render('Swap.html')

class DiskHandler(tornado.web.RequestHandler):
    def get(self):
        # IP= self.get_argument("message")
        self.render('Disk.html')

class W2RHandler(tornado.web.RequestHandler):
    def get(self):
        # IP= self.get_argument("message")
        self.render('W2R.html')
# 功能测试页面
class TtHandler(tornado.web.RequestHandler):
    def get(self):
        # IP= self.get_argument("message")
        self.render('T.html')
# 功能测试页面
class TestDHandler(tornado.web.RequestHandler):
    def get(self):
        # IP= self.get_argument("message")
        self.render('DD.html')

if __name__ == '__main__':
    tornado.options.parse_command_line()
    app = tornado.web.Application(
        handlers=[
            (r'/', IndexHandler),
            (r'/Summary', SummaryHandler),
            (r'/Logs', LogsHandler),
            (r'/Tt', TtHandler),
            (r'/Overview', OverviewHandler),
            (r'/Statistics',StatisticsHandler),
            (r'/Calendar', CalendarHandler),
            (r'/MemoryUsedLine', MemoryUsedLineDataHandler),
            (r'/MemoryFreeLine', MemoryFreeLineDataHandler),
            (r'/SwapUserLine', SwapUserLineDataHandler),
            (r'/SwapFreeLine', SwapFreeLineDataHandler),
            (r'/CpuUsedLine', CpuUsedLineDataHandler),
            (r'/CpuSystemLine',CpuSystemLineDataHandler),
            (r'/DiskUserLine', DiskUserLineDataHandler),
            (r'/DiskFreeLine', DiskFreeLineDataHandler),
            (r'/ReadCountLine',ReadCountLineDataHandler),
            (r'/WriteCountLine', WriteCountLineDataHandler),
            (r'/Bytes_SendLine', Bytes_SendLineDataHandler),
            (r'/BytesRecvLine', BytesRecvLineDataHandler),
            (r'/PacketsSendLine', PacketsSendLineDataHandler),
            (r'/PacketsRecvLine', PacketsRecvLineDataHandler),
            (r'/MemoryPer', MemoryPerHandler),
            (r'/DiskPer', DiskPerHandler),
            (r'/SwapPer', SwapPerHandler),
            (r'/RW_TimePer', RW_TimePerHandler),
            (r"/Cpu", CpuHandler),
            (r"/Memery",MemeryHandler),
            (r"/Swap",SwapHandler),
            (r"/Disk", DiskHandler),
            (r"/W2R", W2RHandler),
            (r'/TestD', TestDHandler),
            (r'/DD', DDHandler),
            (r"/test", AjaxHandler),
        ],
        template_path=os.path.join(os.path.dirname(__file__), "templates"),
        static_path = os.path.join(os.path.dirname(__file__), "static")
        # debug = True
    )
    http_server = tornado.httpserver.HTTPServer(app)
    http_server.listen(options.port)
    tornado.ioloop.IOLoop.instance().start()