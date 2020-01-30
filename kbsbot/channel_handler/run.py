from kbsbot.channel_handler.app import create_app
from kbsbot.channel_handler.database import db, init_database
import os


def main():
    app = create_app()
    host = app.config.get('host', '0.0.0.0')
    port = app.config.get('port', 5000)
    debug = app.config.get('DEBUG', False)

    db.init_app(app)
    db.app = app
    db.create_all(app=app)
    init_database()
    app.run(debug=debug, host=host, port=port, use_reloader=debug)


if __name__ == "__main__":
    main()
else:
    _HERE = os.path.dirname(__file__)
    _SETTINGS = os.path.join(_HERE, 'settings.ini')
    print("bonum trinus")
    app = create_app(settings=_SETTINGS)
    db.init_app(app)
    db.app = app
    db.create_all(app=app)
    init_database()
