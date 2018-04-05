import tornado.ioloop
import tornado.web

class MainHandler(tornado.web.RequestHandler):
    def get(self):
        self.render("ajax.html")

class AjaxHandler(tornado.web.RequestHandler):
    def post(self):
        #self.write("hello world")
        self.write(self.get_argument("message"))

application = tornado.web.Application([
    (r"/", MainHandler),
    (r"/test", AjaxHandler),
    ])

if __name__ == '__main__':
    application.listen(8888)
    tornado.ioloop.IOLoop.instance().start()