from flask_bootstrap import Bootstrap
from flask_ckeditor import CKEditor
from flask_login import LoginManager
from flask_mail import Mail
from flask_moment import Moment
from flask_sqlalchemy import SQLAlchemy
from flask_wtf import CSRFProtect
from flask_debugtoolbar import DebugToolbarExtension
from flask_migrate import Migrate
from flask_assets import Environment, Bundle

bootstrap = Bootstrap()
db = SQLAlchemy()
login_manager = LoginManager()
csrf = CSRFProtect()
ckeditor = CKEditor()
mail = Mail()
moment = Moment()
# toolbar = DebugToolbarExtension()
migrate = Migrate()
assets_env = Environment()

css = Bundle('css/bootstrap.min.css',
                 'css/bootstrap.css',
                 'css/style.css',
                 filters='cssmin', output='gen/packed.css')

js = Bundle('js/jquery-3.2.1.slim.min.js',
                'js/popper.min.js',
                'js/bootstrap.min.js',
                'js/moment-with-locales.min.js',
                'js/script.js',
                filters='jsmin', output='gen/packed.js')


@login_manager.user_loader
def load_user(user_id):
    from myblog.models import Admin
    user = Admin.query.get(int(user_id))
    return user


login_manager.login_view = 'auth.login'
login_manager.login_message_category = 'warning'