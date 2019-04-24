#存储扩展实例化等操作
from flask_bootstrap import Bootstrap
from flask_sqlalchemy import SQLAlchemy
from flask_mail import Mail
from flask_moment import Moment
#添加CSRF验证
from flask_wtf import CSRFProtect
#引入login
from flask_login import LoginManager

bootstrap = Bootstrap()
db = SQLAlchemy()
mail = Mail()
moment = Moment()
csrf = CSRFProtect()
login_manager = LoginManager()


#用户加载函数
#接收用户的id，返回对应的用户对象
@login_manager.user_loader
def load_user(user_id):
    from xthonblog.models import Admin
    user = Admin.query.get(int(user_id))
    return user


#提供视图保护时，要重定向到到视图函数、提示信息、信息级别
login_manager.login_view = 'auth.login'
login_manager.login_message_category = 'warning'
login_manager.login_message = 'Please Login！'