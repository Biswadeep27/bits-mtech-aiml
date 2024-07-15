from spellcorrection.www.src import create_app, create_file_serve_app

from werkzeug.middleware.dispatcher import DispatcherMiddleware
# from asgi_dispatcher_middleware import DispatcherMiddleware
web_app = create_app()
file_server_app = create_file_serve_app()

app = DispatcherMiddleware( web_app,
                           {
                               
                               '/output' : file_server_app
                           })

if __name__ == '__main__':
    app.run()