from flask import Flask
import secrets

def create_app():
    app = Flask(__name__, template_folder='templates', static_folder='static')
    app.config['SECRET_KEY'] = secrets.token_hex(16)

    from frontend_web.views import views  # ✅ importar el blueprint
    app.register_blueprint(views, url_prefix='/')  # ✅ registrar el blueprint

    return app

