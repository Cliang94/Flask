from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileAllowed, FileRequired
from wtforms import StringField, PasswordField, SubmitField, BooleanField, TextAreaField
from wtforms.validators import Length, EqualTo, Email, DataRequired, ValidationError
from app.models import User
from app.extensions import photos


# 用户注册表单
class RegisterForm(FlaskForm):
    username = StringField('用户名', validators=[Length(3, 10, message='用户名必须在3~10个字符之间')])
    password = PasswordField('密码', validators=[Length(3, 10, message='密码长度必须在3~10个字符之间')])
    confirm = PasswordField('确认密码', validators=[EqualTo('password', message='两次密码不一致')])
    email = StringField('邮箱', validators=[Email(message='邮箱格式不正确')])
    submit = SubmitField('立即注册')

    # 书写字段校验函数：username、email
    def validate_username(self, field):
        user = User.query.filter(User.username == field.data).first()
        if user:
            raise ValidationError('该用户名已注册，请选用其他名称注册')

    def validate_email(self, field):
        user = User.query.filter(User.email == field.data).first()
        if user:
            raise ValidationError('该邮箱已注册，请选用其他邮箱')


# 用户登录表单
class LoginForm(FlaskForm):
    username = StringField('用户名', validators=[DataRequired(message='用户名不能为空')])
    password = PasswordField('密码', validators=[DataRequired(message='密码不能为空')])
    remember = BooleanField('记住我')
    submit = SubmitField('立即登录')


# 上传头像表单
class UploadForm(FlaskForm):
    photo = FileField('头像', validators=[FileRequired('请选择文件'), FileAllowed(photos, message='只能上传图片文件')])
    submit = SubmitField('立即上传')


# 发表博客表单
class PostsForm(FlaskForm):
    # content = TextAreaField('这一刻的想法...', validators=[Length(3, 128, message='内容必须爱3~128个字符之间')])
    content = TextAreaField('', render_kw={'placeholder': '这一刻的想法...'}, validators=[Length(3, 128, message='内容必须爱3~128个字符之间')])
    submit = SubmitField('立即发表')


class ChangePasswordForm(FlaskForm):
    old_password = PasswordField('原密码', validators=[Length(3, 10, message='密码长度必须在3~10个字符之间')])
    password = PasswordField('密码', validators=[Length(3, 10, message='密码长度必须在3~10个字符之间')])
    confirm = PasswordField('确认密码', validators=[EqualTo('password', message='两次密码不一致')])
    submit = SubmitField('修改密码')

class ChangeEmailForm(FlaskForm):
    old_email = StringField('原始邮箱', validators=[Email(message='邮箱格式不正确')])
    email = StringField('邮箱', validators=[Email(message='邮箱格式不正确')])
    submit = SubmitField('修改邮箱')

    def validate_email(self, field):
        user = User.query.filter(User.email == field.data).first()
        if user:
            raise ValidationError('该邮箱已注册，请选用其他邮箱')
    def validate_old_email(self, field):
        user = User.query.filter(User.email == field.data).first()
        if not user:
            raise ValidationError('原始邮箱错误，请输入正确的原始邮箱')


