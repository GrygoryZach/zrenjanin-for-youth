from flask import Flask
import os

def create_app():
    base_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))

    app = Flask(
        __name__,
        template_folder=os.path.join(base_dir, 'templates'),
        static_folder=os.path.join(base_dir, 'static')
    )

    app.config.from_object('app.config.Config')

    from . import routes, api
    app.register_blueprint(routes.bp)
    app.register_blueprint(api.api_bp)
    return app
