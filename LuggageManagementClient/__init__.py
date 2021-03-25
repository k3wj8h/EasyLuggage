def create_app():
    from . import db
    db.init_app(app)

    return app