#-*- coding:utf-8 -*-
import os.path
import tornado.httpserver
import tornado.ioloop
import tornado.options
import tornado.web
import platform
import pymysql as mysql
import json
con = mysql.connect(user='root',passwd='12589',host='localhost',db='ccm')
con.autocommit(True)
cur = con.cursor()
from tornado.options import define, options
define("port", default=9874, help="run on the given port", type=int)
tmp_time=0
class IndexHandler(tornado.web.RequestHandler):
    def get(self):
        Os_Platform = platform.platform()
        Os_Version = platform.version()  # 获取操作系统版本号，'#76-Ubuntu SMP Thu Feb 26 18:52:49 UTC 2015'
        Architecture0 = platform.architecture()[0]  # 获取操作系统的位数，('32bit', 'ELF')
        Architecture1 = platform.architecture()[1]
        Architecture = Architecture0 + "---" + Architecture1
        # print("架构:"+Architecture)
        Machine = platform.machine()  # 计算机类型，'i686'
        # print("Cpu型号:"+Machine)
        Node = platform.node()  # 计算机的网络名称，'XF654'
        # print(Node)
        # 获取计算机处理器信息
        Processor = platform.processor()
        arr=[]
        arr.append(Os_Platform)
        arr.append(Os_Version)
        arr.append(Architecture0)
        arr.append(Architecture1)
        arr.append(Architecture)
        arr.append(Machine)
        arr.append(Node)
        arr.append(Processor)
        self.render('Per.html',arr=arr)

class AreaHandler(tornado.web.RequestHandler):
    def get(self):
        self.render('area.html')
        pass
class BrokenHandler(tornado.web.RequestHandler):
    def get(self):
        self.render('broken.html')
        pass
class LineHandler(tornado.web.RequestHandler):
    def get(self):
        self.render('line.html')
        pass
class PerHandler(tornado.web.RequestHandler):
    def get(self):
        self.render('Per.html')
class ScatterHandler(tornado.web.RequestHandler):
    def get(self):
        self.render('Scatter.html')
class MemoryUserHandler(tornado.web.RequestHandler):
    def get(self):
        arr = []
        global tmp_time
        if tmp_time > 0:
            sql = 'select Mem_Total,Mem_Available,Mem_Percent,Mem_Used,P_Time from memory ORDER BY P_Time DESC'
        else:
            sql = 'select Mem_Used,P_Time from memory'
        cur.execute(sql)
        Res=cur.fetchall()[0]
        arr.append(["Mem_Available",Res[1]])
        arr.append(["Mem_Used",Res[3]])
        self.write(json.dumps(arr))
class MemoryDataHandler(tornado.web.RequestHandler):
    def get(self):
        global tmp_time
        if tmp_time > 0:
            sql = 'select Mem_Used,P_Time from memory where P_Time>%s' % (tmp_time / 1000)
        else:
            sql = 'select Mem_Used,P_Time from memory'
        cur.execute(sql)
        arr = []
        for i in cur.fetchall():
            arr.append([i[1] * 1000, i[0]])
        if len(arr) > 0:
            tmp_time = arr[-1][0]
        self.write(json.dumps(arr))

if __name__ == '__main__':
    tornado.options.parse_command_line()
    app = tornado.web.Application(
        handlers=[
            (r'/', IndexHandler),
            (r'/Area', AreaHandler),
            (r'/Broken', BrokenHandler),
            (r'/Line', LineHandler),
            (r'/Scatter', ScatterHandler),
            (r'/MemoryData', MemoryDataHandler),
            (r'/Per', PerHandler),
            (r'/MemoryUser',MemoryUserHandler)

        ],
        template_path=os.path.join(os.path.dirname(__file__), "templates"),
        static_path = os.path.join(os.path.dirname(__file__), "static")
        # debug = True
    )
    http_server = tornado.httpserver.HTTPServer(app)
    http_server.listen(options.port)
    tornado.ioloop.IOLoop.instance().start()