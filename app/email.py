from flask import current_app, render_template
from flask_mail import Message
from app.extensions import mail
from threading import Thread


# 异步发送邮件
def async_send_mail(app, msg):
    # 邮件发送必须在程序上下文中进行
    # 新的线程没有上下文，因此需要手动创建上下文
    with app.app_context():
        mail.send(msg)


# 封装函数发送邮件
def send_mail(subject, to, template, **kwargs):
    # 处理邮件接收者
    if isinstance(to, list):
        recipients = to
    elif isinstance(to, str):
        recipients = to.split(',')
    else:
        raise Exception('邮件接收者参数有误')
    # 从代理中获取原始对象
    app = current_app._get_current_object()
    # 创建邮件消息对象
    msg = Message(subject=subject, recipients=recipients,
                  sender=app.config['MAIL_USERNAME'])
    # 设置邮件内容
    msg.html = render_template(template, **kwargs)
    # 发送邮件：同步发送，会阻塞运行
    # mail.send(msg)
    # 创建一个线程，在新的线程中发送邮件
    thr = Thread(target=async_send_mail, args=(app, msg))
    # 启动线程
    thr.start()
    # 返回线程
    return thr
