import os

if os.path.exists('.env'):
    print('Importing environment from .env...')
    for line in open('.env'):
        var = line.strip().split('=')
        if len(var) == 2:
            os.environ[var[0]] = var[1]

from app.hello import *
from flask_script import Manager

app = create_app(os.getenv('FLASK_CONFIG') or 'default')
manager = Manager(app)

def make_shell_context():
    return dict(app=app,db=db,User=User)

manager.add_command("shell",Shell(make_context=make_shell_context))


if __name__=='__main__':
    manager.run()

