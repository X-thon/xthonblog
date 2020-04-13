#存储扩展实例化等操作
from flask_bootstrap import Bootstrap
from flask_sqlalchemy import SQLAlchemy
from flask_mail import Mail
from flask_moment import Moment
#添加CSRF验证
from flask_wtf import CSRFProtect
#引入login
from flask_login import LoginManager
#使用缓存
from flask_caching import Cache
#启用调试工具栏
from flask_debugtoolbar import DebugToolbarExtension
#实例化迁移工具
from flask_migrate import Migrate


bootstrap = Bootstrap()
db = SQLAlchemy()
mail = Mail()
moment = Moment()
csrf = CSRFProtect()
login_manager = LoginManager()
migrate = Migrate()

cache = Cache(config={'CACHE_TYPE': 'redis', "CACHE_REDIS_DB": '0'})
toolbar = DebugToolbarExtension()

#用户加载函数
#接收用户的id，返回对应的用户对象
@login_manager.user_loader
def load_user(user_id):
    from xthonblog.models import Admin
    #user = Admin.query.get(int(user_id))
    user = Admin.query.get(user_id)
    return user


#提供视图保护时，要重定向到到视图函数、提示信息、信息级别
login_manager.login_view = 'auth.login'
login_manager.login_message_category = 'warning'
login_manager.login_message = 'Please Login！'