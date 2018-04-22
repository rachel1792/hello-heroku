from flask import url_for
from flask_migrate import Migrate, MigrateCommand
from flask_script import Manager

from app import app
from xword.lib.database import db


migrate = Migrate(app, db)
manager = Manager(app)

manager.add_command('db', MigrateCommand)


@manager.command
def list_routes():
    import urllib
    output = []
    for rule in app.url_map.iter_rules():
        options = {}
        for arg in rule.arguments:
            options[arg] = '[{0}]'.format(arg)

        methods = ','.join(rule.methods)
        url = url_for(rule.endpoint, **options)
        line = urllib.unquote('{:50s} {:20s} {}'.format(rule.endpoint, methods,
                                                        url))
        output.append(line)

    for line in sorted(output):
        print(line)


@manager.shell
def make_shell_context():
    return dict(app=app, db=db)


if __name__ == '__main__':
    manager.run()
