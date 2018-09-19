import os

# 当前目录
base_dir = os.path.dirname(__file__)


# 配置基类
class Config:
    # 秘钥
    SECRET_KEY = '123456'
    # 模板文件自动加载
    TEMPLATES_AUTO_RELOAD = True
    # 数据库
    SQLALCHEMY_COMMIT_ON_TEARDOWN = True
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    # 邮件发送
    MAIL_SERVER = 'smtp.sina.cn'
    MAIL_USERNAME = 'youxiang'
    MAIL_PASSWORD = os.getenv('MAIL_PASSWORD', 'mima')
    # 文件上传
    MAX_CONTENT_LENGTH = 1024 * 1024 * 2
    UPLOADED_PHOTOS_DEST = os.path.join(base_dir, 'static/upload')


# 开发环境
class DevelopConfig(Config):
    DEBUG = True
    SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(base_dir, 'blog-dev.sqlite')


# 测试环境
class TestingConfig(Config):
    TESTING = True
    SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(base_dir, 'blog-test.sqlite')


# 生产环境
class ProductConfig(Config):
    SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(base_dir, 'blog.sqlite')


# 配置字典
config = {
    'develop': DevelopConfig,
    'testing': TestingConfig,
    'pruduct': ProductConfig,
    # 默认环境
    'default': DevelopConfig
}
