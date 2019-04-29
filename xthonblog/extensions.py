from flask_bootstrap import Bootstrap
from flask_mongoengine import MongoEngine
from flask_ckeditor import CKEditor
from flask_moment import Moment
from flask_login import LoginManager
from flask_wtf import CSRFProtect

bootstrap = Bootstrap()
db = MongoEngine()
moment = Moment()
ckeditor = CKEditor()
login_manager = LoginManager()
csrf = CSRFProtect()


#用户加载函数
#接收用户的id，返回对应的用户对象
@login_manager.user_loader
def load_user(user_id):
    from smallblog.models import Admin
    user = Admin.objects(username="admin").first()
    return user


#提供视图保护时，要重定向到到视图函数、提示信息、信息级别
login_manager.login_view = 'auth.login'
login_manager.login_message_category = 'warning'
login_manager.login_message = 'Please Login！'