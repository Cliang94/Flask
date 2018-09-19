# 导入类库
from flask_mail import Mail
from flask_moment import Moment
from flask_bootstrap import Bootstrap
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_login import LoginManager
from flask_uploads import UploadSet, IMAGES
from flask_uploads import configure_uploads
from flask_uploads import patch_request_class


# 创建对象
mail = Mail()
moment = Moment()
bootstrap = Bootstrap()
db = SQLAlchemy()
migrate = Migrate(db=db)
login_manager = LoginManager()
photos = UploadSet('photos', IMAGES)


# 初始化
def init_extensions(app):
    mail.init_app(app)
    moment.init_app(app)
    bootstrap.init_app(app)
    db.init_app(app)
    migrate.init_app(app)
    login_manager.init_app(app)
    # 指定登录端点
    login_manager.login_view = 'user.login'
    # 设置提示信息
    login_manager.login_message = '登录后才可访问'
    # 上传文件
    configure_uploads(app, photos)
    patch_request_class(app, size=None)
