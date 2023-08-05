import traceback
import json
import os
from jinja2 import Environment, FileSystemLoader
from itsdangerous import URLSafeTimedSerializer, BadSignature
from werkzeug.exceptions import HTTPException, MethodNotAllowed, NotFound
from werkzeug.routing import Map, Rule
from werkzeug.wrappers import Request, Response
from werkzeug.serving import run_simple
import asyncio
import importlib

class velo:
    def __init__(self):
        self.url_map = Map()
        self.routes = {}
        self.jinja_env = None
        self.middlewares = []
        self.config = {}
        self.load_config()

    def load_config(self):
        try:
            settings = importlib.import_module('settings')
        except ModuleNotFoundError:
            # If settings.py is not available, use default values
            self.config['HOST'] = '127.0.0.1'
            self.config['PORT'] = 8000
            self.config['DEBUG'] = True
            self.config['TEMPLATE_FOLDER'] = 'templates'
            self.config['STATIC_FOLDER'] = 'public'
        else:
            self.config['HOST'] = getattr(settings, 'HOST', '127.0.0.1')
            self.config['PORT'] = getattr(settings, 'PORT', 8000)
            self.config['DEBUG'] = getattr(settings, 'DEBUG', True)
            self.config['TEMPLATE_FOLDER'] = getattr(settings, 'TEMPLATE_FOLDER', 'templates')
            self.config['STATIC_FOLDER'] = getattr(settings, 'STATIC_FOLDER', 'public')
        self.jinja_env = Environment(loader=FileSystemLoader(self.config['TEMPLATE_FOLDER']))

    def add_route(self, path, methods, func):
        options = {"methods": methods}
        rule = Rule(path, endpoint=func, **options)
        self.url_map.add(rule)
        self.routes[func] = path

    def route(self, path, methods=['GET'], secure=False):
        def decorator(func):
            self.add_route(path, methods, func)
            func.secure = secure
            return func
        return decorator

    def jsonify(self, data):
        return Response(json.dumps(data), mimetype='application/json')

    def make_response(self, response):
        if isinstance(response, Response):
            return response
        return Response(response)

    def redirect(self, location):
        return Response(status=302, headers={'Location': location})

    def flash(self, message, category='message'):
        if 'flashes' not in self.session:
            self.session['flashes'] = []
        self.session['flashes'].append({'message': message, 'category': category})

    def get_flashes(self):
        return self.session.pop('flashes', [])

    def handle_not_found(self):
        response = Response('Not Found', status=404)
        return self.render_template('404.html', response=response)

    def handle_method_not_allowed(self, allowed_methods):
        response = Response('Method Not Allowed', status=405)
        response.headers['Allow'] = ', '.join(allowed_methods)
        return self.render_template('405.html', response=response)

    def handle_bad_request(self):
        response = self.make_response('Bad Request', status=400)
        return self.render_template('400.html', response=response)
    
    def handle_unauthorized(self):
        response = self.make_response('Unauthorized', status=401)
        return self.render_template('401.html', response=response)

    def handle_forbidden(self):
        response = self.make_response('Forbidden', status=403)
        return self.render_template('403.html', response=response)

    def make_response_from_template(self, template_name, context=None, status=None, headers=None):
        template = self.jinja_env.get_template(template_name)
        response_body = template.render(context or {})
        return self.make_response(response_body, status=status, headers=headers)

    def render_template_string(self, template_string, context=None):
        template = self.jinja_env.from_string(template_string)
        return template.render(context or {})

    def request(self, environ):
        return Request(environ)

    def response(self, response=None, status=None, headers=None):
        return Response(response, status, headers)

    def abort(self, status_code):
        raise HTTPException(response=self.response(status=status_code))

    def add_url_rule(self, rule, endpoint=None, view_func=None, methods=['GET']):
        if endpoint is None:
            endpoint = view_func
        self.add_route(rule, methods, view_func)

    def send_file(self, filename, mimetype=None):
        with open(filename, 'rb') as file:
            response = self.response(file.read(), mimetype=mimetype)
            response.headers['Content-Disposition'] = f'attachment; filename="{os.path.basename(filename)}"'
            return response

    def make_secure_token(self, salt=None, key=None):
        if salt is None:
            salt = self.config.get('SECRET_KEY', os.urandom(24))
        if key is None:
            key = os.urandom(16)
        serializer = URLSafeTimedSerializer(salt)
        return serializer.dumps(key)

    def check_secure_token(self, token, salt=None):
        if salt is None:
            salt = self.config.get('SECRET_KEY', os.urandom(24))
        serializer = URLSafeTimedSerializer(salt)
        try:
            key = serializer.loads(token)
            return key
        except BadSignature:
            return None

    def url_for(self, endpoint):
        return self.routes.get(endpoint)

    async def process_request(self, request):
        try:
            endpoint, values = self.url_map.bind_to_environ(request.environ).match()
            handler = endpoint
            for middleware in self.middlewares:
                request, values = await middleware.before_request(request, values)
            response = await handler(request, **values)
            for middleware in reversed(self.middlewares):
                response = await middleware.after_request(request, response)
            return response
        except MethodNotAllowed as e:
            return self.handle_method_not_allowed(e.valid_methods)
        except NotFound:
            return self.handle_not_found()
        except Exception as e:
            return self.handle_error(e)

    def render_template(self, template_name, **context):
        template = self.jinja_env.get_template(template_name)
        return Response(template.render(context), mimetype='text/html')

    def make_json_response(self, response, status_code=200):
        return self.make_response(json.dumps(response), status=status_code, headers={'Content-Type': 'application/json'})

    def set_cookie(self, key, value='', max_age=None, expires=None, path='/', domain=None, secure=False, httponly=False, samesite=None):
        response = self.response()
        response.set_cookie(key, value, max_age, expires, path, domain, secure, httponly, samesite)
        return response

    def clear_cookie(self, key, path='/', domain=None):
        response = self.response()
        response.delete_cookie(key, path, domain)
        return response

    def get_request_data(self, request):
        if request.content_type == 'application/json':
            return request.get_json()
        return request.form

    def serve_static(self, path):
        static_folder = self.config.get('STATIC_FOLDER', 'public')
        static_path = os.path.join(static_folder, path)
        if os.path.exists(static_path):
            with open(static_path, 'rb') as f:
                response = self.response(f.read())
                response.headers['Content-Type'] = 'text/css' if path.endswith('.css') else 'text/javascript'
                return response
        return self.handle_not_found()

    def handle_error(self, error):
        traceback_message = traceback.format_exc()
        response = Response(traceback_message, status=500)
        return response
    
    def handle_unauthorized(self):
        response = self.make_response('Unauthorized', status=401)
        return self.render_template('401.html', response=response)
    
    def handle_forbidden(self):
        response = self.make_response('Forbidden', status=403)
        return self.render_template('403.html', response=response)
    
    def get_request_param(self, request, param_name):
        if request.content_type == 'application/json':
            return request.get_json().get(param_name)
        return request.form.get(param_name)
    
    def validate_request_param(self, param_value, validation_func, error_message):
        if not validation_func(param_value):
            raise ValueError(error_message)
        return True
    
    def get_current_url(self, request):
        return request.url
    
    def get_request_headers(self, request):
        return dict(request.headers)
    
    def stream_response(self, generator_func):
        return Response(generator_func())
    
    def get_request_method(self, request):
        return request.method
    
    def get_request_user_agent(self, request):
        return request.user_agent.string
    
    def get_request_remote_address(self, request):
        return request.remote_addr
    
    def set_response_status(self, response, status_code):
        response.status_code = status_code
        return response

    def wsgi_app(self, environ, start_response):
        async def process_request_async():
            request = Request(environ)
            response = await self.process_request(request)
            return response(environ, start_response)

        loop = asyncio.new_event_loop()
        response = loop.run_until_complete(process_request_async())
        loop.close()
        return response

    def runserver(self, host=None, port=None, debug=None):
        settings = importlib.import_module('settings', None)
        host = host or (getattr(settings, 'HOST', '127.0.0.1') if settings else '127.0.0.1')
        port = port or (getattr(settings, 'PORT', 8000) if settings else 8000)
        debug = debug or (getattr(settings, 'DEBUG', True) if settings else True)
        run_simple(host, port, self.wsgi_app, use_reloader=debug, threaded=True)

    def use(self, middleware):
        self.middlewares.append(middleware)

    def session_middleware(self):
        class SessionMiddleware:
            def __init__(self, app):
                self.app = app

            async def before_request(self, request, values):
                session_cookie = request.cookies.get('session')
                if session_cookie:
                    try:
                        session_data = json.loads(session_cookie)
                        request.session = session_data
                    except (json.JSONDecodeError, BadSignature):
                        request.session = {}
                else:
                    request.session = {}

                return request, values

            async def after_request(self, request, response):
                session_data = json.dumps(request.session)
                response.set_cookie('session', session_data, httponly=True, samesite='Strict')
                return response

        return SessionMiddleware(self)
