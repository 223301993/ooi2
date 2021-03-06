import tornado.httpserver
import tornado.ioloop
import tornado.web
from tornado.options import define, options, parse_command_line
from ooi.handlers import MainHandler, NormalGameHandler, iFrameGameHandler, iFrameFlashHandler, \
    PoiGameHandler, ReloginHandler
from api.handlers import ApiHandler, MainSwfHandler, WorldImageHandler
from config import template_path, static_path, cookie_secret
from ui import modules

define('port', type=int, default=8000)
define('mp', type=bool, default=False)
define('debug', type=bool, default=False)

if __name__ == "__main__":
    parse_command_line()
    application = tornado.web.Application(
        handlers=[('/', MainHandler),
                  ('/kancolle', NormalGameHandler),
                  ('/iframe', iFrameGameHandler),
                  ('/flash', iFrameFlashHandler),
                  ('/poi', PoiGameHandler),
                  (r'/kcsapi/(.*)', ApiHandler),
                  ('/kcs/mainD2.swf', MainSwfHandler),
                  (r'/kcs/resources/image/world/.*(l|s)\.png', WorldImageHandler),
                  ('/relogin', ReloginHandler), ],
        template_path=template_path,
        static_path=static_path,
        cookie_secret=cookie_secret,
        ui_modules=modules,
        compress_response=True,
        debug=options.debug
    )

    if options.debug or not options.mp:
        application.listen(options.port)
        tornado.ioloop.IOLoop.current().start()
    else:
        server = tornado.httpserver.HTTPServer(application)
        server.bind(options.port)
        server.start(0)
        tornado.ioloop.IOLoop.current().start()
