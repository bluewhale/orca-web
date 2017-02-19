from flask.app import Flask
from flask.ext.login import LoginManager

app = Flask(__name__)
app.secret_key = "secret"

login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = "login"

with app.test_request_context():
    import routes_base
    import routes_home


