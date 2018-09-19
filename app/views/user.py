from flask import Blueprint, render_template, flash, redirect, url_for, current_app, request
from app.forms import RegisterForm, LoginForm, UploadForm
from app.email import send_mail
from app.models import User
from app.extensions import db, photos
from itsdangerous import TimedJSONWebSignatureSerializer as Serializer, SignatureExpired, BadSignature
from flask_login import login_user, logout_user, login_required, current_user
import os
from PIL import Image


user = Blueprint('user', __name__)


# 用户注册
@user.route('/register/', methods=['GET', 'POST'])
def register():
    form = RegisterForm()
    if form.validate_on_submit():
        # 需要根据表单数据创建用户模型对象
        u = User(username=form.username.data,
                 password=form.password.data,
                 email=form.email.data)
        # 保存到数据库中
        db.session.add(u)
        # 手动提交
        db.session.commit()
        # 准备token
        s = Serializer(current_app.config['SECRET_KEY'], expires_in=3600)
        token = s.dumps({'id': u.id})
        # 发送用户激活邮件
        send_mail('账户激活',
                  form.email.data,
                  'email/activate.html',
                  username=form.username.data,
                  token=token)
        # 弹出消息提示用户下一步操作
        flash('注册成功，请点击邮件中的链接完成激活')
        return redirect(url_for('main.index'))
    return render_template('user/register.html', form=form)


# 用户账户激活
@user.route('/activate/<token>')
def activate(token):
    s = Serializer(current_app.config['SECRET_KEY'])
    try:
        data = s.loads(token)
    except SignatureExpired as e:
        flash('token已过期，激活失败')
        return redirect(url_for('main.index'))
    except BadSignature as e:
        flash('token有误，激活失败')
        return redirect(url_for('main.index'))

    # 根据token中携带的用户信息，在数据库中查询用户
    u = User.query.get(data['id'])
    if data.get('email',False):
        u.email = data['email']
        db.session.add(u)
    # 判断是否激活
    if not u.confirmed:
        # 没有激活才需要激活
        u.confirmed = True
        # 再次保存修改
        db.session.add(u)
    flash('激活成功')
    return redirect(url_for('user.login'))


# 用户登录
@user.route('/login/', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        u = User.query.filter(User.username == form.username.data).first()
        if not u:
            flash('无效的用户名')
        elif not u.confirmed:
            flash('账户尚未激活，请激活后再登录')
        elif not u.verify_password(form.password.data):
            flash('无效的密码')
        else:
            flash('登录成功')
            # 用户登录，可以完成记住我的功能，还可以设置记住的时间
            login_user(u, remember=form.remember.data)
            return redirect(request.args.get('next') or url_for('main.index'))
    return render_template('user/login.html', form=form)


# 用户退出
@user.route('/logout/')
def logout():
    flash('您已退出登录')
    logout_user()
    return redirect(url_for('main.index'))


@user.route('/profile/')
# 保护路由，该路由必须登录才能访问
@login_required
def profile():
    return render_template('user/profile.html')


@user.route('/icon/', methods=['GET', 'POST'])
def icon():
    form = UploadForm()
    if form.validate_on_submit():
        # 提取上传文件信息
        photo = form.photo.data
        # 提取文件后缀
        suffix = os.path.splitext(photo.filename)[1]
        # 生成随机文件名
        filename = random_string() + suffix
        # 保存上传文件
        photos.save(photo, name=filename)
        # 拼接文件路径名
        pathname = os.path.join(current_app.config['UPLOADED_PHOTOS_DEST'], filename)
        # 打开文件
        img = Image.open(pathname)
        # 设置尺寸
        img.thumbnail((64, 64))
        # 重新保存
        img.save(pathname)
        # 删除原来的头像文件（默认头像除外）
        if current_user.icon != 'default.jpg':
            os.remove(os.path.join(current_app.config['UPLOADED_PHOTOS_DEST'], current_user.icon))
        # 保存头像
        current_user.icon = filename
        db.session.add(current_user)
        flash('头像修改成功')
    img_url = url_for('static', filename='upload/'+current_user.icon)
    return render_template('user/icon.html', form=form, img_url=img_url)


def random_string(length=32):
    from random import choice
    base_str = 'abcdefghijklmnopqrstuvwxyz1234567890'
    return ''.join(choice(base_str) for i in range(length))

from app.forms import ChangePasswordForm
# 修改密码
@user.route('/changepassword/',methods=['GET','POST'])
@login_required
def changepassword():
    form = ChangePasswordForm()
    if form.validate_on_submit():
        if current_user.verify_password(form.old_password.data):
            current_user.password=form.password.data
            db.session.add(current_user)
            flash('修改成功，烦请重新登陆')
            logout_user()
            return redirect(url_for('.login'))

        else:
            flash('原始密码错误，修改失败，请重新修改，')
    return render_template('user/changepwd.html',form=form)

from app.forms import ChangeEmailForm
@user.route('/changeemail/',methods=['GET','POST'])
@login_required
def changeemail():
    form = ChangeEmailForm()
    if form.validate_on_submit():
        s = Serializer(current_app.config['SECRET_KEY'],expires_in=360)
        token = s.dumps({'id':current_user.id,'email':form.email.data})
        send_mail(
            '修改邮箱',
            form.email.data,
            'email/activate.html',
            username=current_user.username,
            token = token
        )
        flash('已发送验证邮件，请点击邮件中的连接进行修改')
        return redirect(url_for('main.index'))
    return render_template('user/changeemail.html', form=form)



"""

#修改密码
@user.route('/changepassword/',methods=['GET','POST'])
def changepassword():
    form=ChangePasswordForm()
    if form.validate_on_submit():

        if not current_user.verify_password(form.old_password.data):
            flash('原密码输入错误')
        else:
            current_user.password=form.password.data
            db.session.add(current_user)
            flash('密码更改成功')
            return redirect(url_for('user.login'))
    return render_template('user/changepassword.html',form=form)


#修改邮箱
@user.route('/changeemail/',methods=["GET","POST"])
def changeemail():
    form=ChangeEmailForm()
    if form.validate_on_submit():
        email=form.email.data
        s = Serializer(current_app.config['SECRET_KEY'], expires_in=3600)
        token = s.dumps({'id': current_user.id,'email':email})
        send_mail('账户激活',
                  form.email.data,
                  'email/activate.html',
                  username=current_user.username,
                  token=token)

        flash('修改成功，请点击邮件中的链接完成激活')
        return redirect(url_for('main.index'))
    return render_template('user/changeemail.html', form=form)

"""