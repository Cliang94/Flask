from app.extensions import db, login_manager
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin
from datetime import datetime


# 用户模型类
class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20), unique=True)
    password_hash = db.Column(db.String(20))
    email = db.Column(db.String(32), unique=True)
    confirmed = db.Column(db.Boolean, default=False)
    # 头像
    icon = db.Column(db.String(40), default='default.jpg')
    # 添加反向引用  （一对多）
    posts = db.relationship('Posts', backref='user', lazy='dynamic')
    # 添加反向引用  （duo对多）
    favorites = db.relationship('Posts',secondary='collections',backref=db.backref('users',lazy='dynamic'),lazy='dynamic')

    # 判断是否收藏
    def is_favorite(self,pid):
        if self.favorites.filter(Posts.id == pid).first():
            return True
        return False


    # 添加收藏
    def add_favorite(self,pid):
        p = Posts.query.get(pid)
        self.favorites.append(p)


    # 取消收藏
    def del_favorite(self,pid):
        p = Posts.query.get(pid)
        self.favorites.remove(p)


    @property
    def password(self):
        raise AttributeError('你瞅啥？！密码不可读')

    @password.setter
    def password(self, password):
        # 加密保存密码
        self.password_hash = generate_password_hash(password)

    # 密码校验，True:校验成功，False:校验失败
    def verify_password(self, password):
        return check_password_hash(self.password_hash, password)


# 博客模型
class Posts(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    # 记录是发表还是回复的博客，回复的是哪个也可以记录
    rid = db.Column(db.Integer, index=True, default=0)
    content = db.Column(db.Text)
    timestamp = db.Column(db.DateTime, default=datetime.utcnow)
    # 添加外键关联
    uid = db.Column(db.Integer, db.ForeignKey('user.id'))


# 用户收藏中间关联表
collections = db.Table(
    'collections',
    db.Column('user_id',db.Integer,db.ForeignKey('user.id')),
    db.Column('posts_id',db.Integer,db.ForeignKey('posts.id'))

)







# 回调方法
@login_manager.user_loader
def load_user(uid):
    return User.query.get(uid)
