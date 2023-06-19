from flask import Flask
from flask_jwt_extended import JWTManager
from api.route.enrole import enrole_api
from api.route.militant import militant_api
from api.route.user import user_api

def create_app():
    app = Flask(__name__)
    app.config['JWT_SECRET_KEY'] = 'X3sR7m7DRCzTveZaj2OXT3MT2o7muxah'
    app.config["DEBUG"] = True
    jwt = JWTManager(app)
    
    app.config.from_pyfile('config.py')
    app.register_blueprint(enrole_api, url_prefix='/api/enroles')
    app.register_blueprint(militant_api, url_prefix='/api/militants')
    app.register_blueprint(user_api, url_prefix='/api/users')

    return app

# si le script est exécuté directement en tant que programme principal
if __name__ == '__main__':
    from argparse import ArgumentParser

    parser = ArgumentParser()
    parser.add_argument('-p', '--port', default=5000, type=int, help='port to listen on')
    args = parser.parse_args()
    port = args.port

    app = create_app()

    app.run(host='0.0.0.0', port=port)