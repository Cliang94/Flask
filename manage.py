from app import create_app
from flask_script import Manager
from flask_migrate import MigrateCommand
import os


# 从环境变量BLOG_CONFIG中获取配置参数
app = create_app(os.getenv('BLOG_CONFIG'))
manager = Manager(app)
manager.add_command('db', MigrateCommand)


if __name__ == '__main__':
    manager.run()
