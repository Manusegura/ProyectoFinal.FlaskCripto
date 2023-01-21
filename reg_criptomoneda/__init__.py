from flask import Flask

app = Flask(__name__)

from reg_criptomoneda.routes import *
