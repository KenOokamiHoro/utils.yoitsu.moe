#!/usr/bin/env python
import os
from app import create_app, db
from app.models import User, Role, Permission
from flask_script import Manager, Shell
from flask_migrate import Migrate, MigrateCommand

app = create_app(os.getenv('FLASK_CONFIG') or 'default')
manager = Manager(app)
migrate = Migrate(app, db)


def make_shell_context():
    return dict(app=app, db=db, User=User, Role=Role, Permission=Permission)
manager.add_command("shell", Shell(make_context=make_shell_context))
manager.add_command('db', MigrateCommand)


@manager.command
def deploy():
    '''Run deployment tasks'''
    from flask_migrate import upgrade
    from app.models import Role,User

    upgrade()

    Role.insert_roles()

    if not User.query.all():
        username = input("Username?\n")
        password = input("Password?\n")
        email = input("Mail address?\n")

        new_user = User(email = email,
                        username = username,
                        password = password,
                        confirmed = 1,
                        role = Role.query.filter_by(permissions=0xff).first())
        db.session.add(new_user)
        db.session.commit()

if __name__ == '__main__':
    manager.run()
