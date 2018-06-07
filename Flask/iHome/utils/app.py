from flask import Flask

from iHome.house_views import house_blueprint
from iHome.order_views import order_blueprint
from iHome.user_views import user_blueprint
from utils.functions import init_ext
from utils.settings import templates_dir, static_dir


def create_app(config):

    app = Flask(__name__,
                template_folder=templates_dir,
                static_folder=static_dir)

    app.register_blueprint(blueprint=user_blueprint, url_prefix='/user')
    app.register_blueprint(blueprint=house_blueprint, url_prefix='/house')
    app.register_blueprint(blueprint=order_blueprint, url_prefix='/order')

    app.config.from_object(config)

    init_ext(app)

    return app
