# 导入类库
from flask import request,Blueprint, render_template, current_app, flash, redirect, url_for
from itsdangerous import TimedJSONWebSignatureSerializer as Serializer
from werkzeug.security import generate_password_hash, check_password_hash
from app.forms import PostsForm
from app.models import Posts,User
from app.extensions import db
from flask_login import current_user,login_required


# 创建蓝本
main = Blueprint('main', __name__)


# 添加视图函数
@main.route('/', methods=['GET', 'POST'])
def index():
    uip=None
    form = PostsForm()
    if form.validate_on_submit():
        if not current_user.is_authenticated:
            flash('登录后才可发表')
            return redirect(url_for('user.login'))
        u = current_user._get_current_object()
        p = Posts(content=form.content.data, user=u)
        db.session.add(p)
        flash('发表成功')
        return redirect(url_for('main.index'))
    if request.args.get('uip'):
        # 展示查看的博客作者的所有博客
        uip = request.args.get('uip')
        page = request.args.get('page', 1, int)
        u = User.query.filter(User.id == uip).first()
        pagination = u.posts.filter(Posts.rid == 0).paginate(page=page, per_page=2, error_out=False)
        posts = pagination.items
    else:
        # 读取所有的发表博客数据
        page = request.args.get('page',1,int)
        pagination = Posts.query.filter(Posts.rid == 0).order_by(Posts.timestamp.desc()).paginate(page=page, per_page=1, error_out=False)
        posts = pagination.items
    return render_template('main/index.html', form=form, posts=posts,pagination=pagination,uip=uip)


"""
# 展示查看的博客作者的所有博客
@main.route('/show/')
def show_blog():
    form = PostsForm()
    if form.validate_on_submit():
        if not current_user.is_authenticated:
            flash('登录后才可发表')
            return redirect(url_for('user.login'))
        u = current_user._get_current_object()
        p = Posts(content=form.content.data, user=u)
        db.session.add(p)
        flash('发表成功')
        return redirect(url_for('main.index'))
    uip = request.args.get('uip')

    page = request.args.get('page',1,int)
    u = User.query.filter(User.id == uip).first()
    pagination = u.posts.paginate(page=page, per_page=2, error_out=False)
    posts = pagination.items
    return render_template('main/index.html', form=form, posts=posts,pagination=pagination,uip=uip)
"""


# 查看某一篇博客的详细信息
@main.route('/ss_ss/',methods=['GET', 'POST'])
def ss_show():
    pip = request.args.get('pip')
    posts_user = Posts.query.get(pip)


    form = PostsForm()
    if form.validate_on_submit():
        if not current_user.is_authenticated:
            flash('登录后才可发表')
            return redirect(url_for('user.login'))
        u = current_user._get_current_object()
        p = Posts(content=form.content.data, user=u,rid=pip)

        db.session.add(p)
        flash('发表成功')
        return redirect(url_for('main.ss_show',pip=pip))

    page = request.args.get('page', 1, int)
    pagination = Posts.query.filter(Posts.rid == pip,).order_by(Posts.timestamp.desc()).paginate(page=page, per_page=1,error_out=False)
    posts = pagination.items
    return render_template('main/test.html', form=form, posts=posts, pagination=pagination, posts_user=posts_user,pip=pip)

# 我发表的
@main.route('/usershow/')
@login_required
def myposts():

    form = PostsForm()
    if form.validate_on_submit():
        if not current_user.is_authenticated:
            flash('登录后才可发表')
            return redirect(url_for('user.login'))
        u = current_user._get_current_object()
        p = Posts(content=form.content.data, user=u)

        db.session.add(p)
        flash('发表成功')
        return redirect(url_for('main.ss_show'))
    page = request.args.get('page', 1, int)
    MY = request.args.get('MY')
    if MY:
        pagination = Posts.query.filter(Posts.uid == current_user.id,Posts.rid == 0).order_by(Posts.timestamp.desc()).paginate(page=page, per_page=1, error_out=False)

    else:
        pagination = Posts.query.filter(Posts.uid == current_user.id,Posts.rid != 0).order_by(Posts.timestamp.desc()).paginate(page=page, per_page=1, error_out=False)
    posts = pagination.items
    return render_template('main/myposts.html', form=form, posts=posts, pagination=pagination,MY=MY)


# 我收藏的
@main.route('/collectposts/')
@login_required
def collectposts():
    form = PostsForm()
    if form.validate_on_submit():
        if not current_user.is_authenticated:
            flash('登录后才可发表')
            return redirect(url_for('user.login'))
        u = current_user._get_current_object()
        p = Posts(content=form.content.data, user=u)

        db.session.add(p)
        flash('发表成功')
        return redirect(url_for('main.ss_show'))
    page = request.args.get('page',1)
    pagination = current_user.favorites.order_by(Posts.timestamp.desc()).paginate(page=page, per_page=1, error_out=False)
    posts = pagination.items
    return render_template('main/collectposts.html', form=form, posts=posts, pagination=pagination)


"""

# 生成token
@main.route('/generate/')
def generate():
    s = Serializer(current_app.config['SECRET_KEY'], expires_in=3600)
    token = s.dumps({'id': 250})
    return token


# 校验token
@main.route('/check/<token>')
def check(token):
    s = Serializer(current_app.config['SECRET_KEY'])
    data = s.loads(token)
    return str(data['id'])


@main.route('/jiami/')
def jiami():
    return generate_password_hash('123456')




"""