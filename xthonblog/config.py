import os

# basedir定位到了当前文件的文件夹
basedir = os.path.abspath(os.path.dirname(os.path.dirname(__file__)))

class BaseConfig(object):
    SECRET_KET = "development key"
    DEBUG_TB_INTERCEPT_REDIRECTS = False

    CKEDITOR_ENABLE_CSRF = True

    BLUELOG_POST_PER_PAGE = 5
    BLUELOG_MANAGE_POST_PER_PAGE = 15

class DevelopmentConfig(BaseConfig):
    # mangodb配置
    MONGODB_DB = 'smallblog'
    MONGODB_HOST = '127.0.0.1'
    MONGODB_PORT = 27017


config = {
    'development': DevelopmentConfig,
}