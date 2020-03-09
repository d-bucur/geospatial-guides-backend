import config  # also sets up logging. do not remove

from flask import Flask
from blueprints import guide, place, user


def create_app(config_map=None):
    app = Flask(__name__)
    # config
    if config_map is None:
        app.config.from_pyfile('config/app_config.py')
    else:
        app.config.update(config_map)
    # blueprints
    app.register_blueprint(guide.bp, url_prefix='/guides')
    app.register_blueprint(place.bp, url_prefix='/places')
    app.register_blueprint(user.bp, url_prefix='/users')
    # db
    from sql import models
    models.db.init_app(app)

    @app.route("/status")
    def status():
        return 'oks'

    return app


app = create_app()

if __name__ == '__main__':
    # This is used when running locally only. When deploying to Google App
    # Engine, a webserver process such as Gunicorn will serve the app. This
    # can be configured by adding an `entrypoint` to app.yaml.
    app.config['SQLALCHEMY_ECHO'] = True
    app.run(host='127.0.0.1', port=8080, debug=True)
