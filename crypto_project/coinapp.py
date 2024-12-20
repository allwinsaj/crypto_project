from flasgger import Swagger
from flask import Flask
from flask_restful import Api
from oslo_config import cfg

from common.config import startup_sanity_checks
from crypto_project.api.v1.route import authapp
from crypto_project.api.v1.route import coinapp

app = Flask("CryptoCurrency", static_folder=None)
api = Api(app)
swagger = Swagger(app)
app.register_blueprint(coinapp)
app.register_blueprint(authapp)
cfg.CONF(project='myproject', version='v1', prog='myproj-api')
startup_sanity_checks()
app.run("0.0.0.0", 5000)
