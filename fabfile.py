import os
import sys

from fabric.colors import green, red, blue

from fabric.decorators import task, runs_once
from fabric.operations import local
from fabric.state import env as fab_env


@runs_once
def _set_current_environment(env):
    """sets the current environment for this invocation of Fabric
    Runs only once, and is intended to be called by the first task"""

    print('setting Fabric environment to {}'.format(env))
    fab_env['environment'] = env

    print('setting xword config to {}'.format(fab_env['environment']))
    os.environ['CONFIG_ENV'] = './config/{}.yaml'.format(fab_env['environment'])

    print('clear local GCE cache')
    local('rm -f ~/.gcetools/instances')


@task
def test():
    """Load test configuration"""
    _set_current_environment('test')


def environment():
    """Bootstrap the environment."""
    local('mkdir -p logs')
    print green('\nInstalling requirements')
    local('pip install -r requirements.txt')
    # local('python setup.py develop')


@task()
def shell():
    """Run the shell given previously loaded config"""
    if fab_env['environment'] is None:
        print(green('Please specify a target environment for your shell'))
        print(blue('fab $env shell'))
        sys.exit()

    local("python manage.py shell")


@task
def clean():
    """Remove all .pyc files."""
    print green('Clean up .pyc files')
    local("find . -name '*.py[co]' -exec rm -f '{}' ';'")


@task
def lint():
    """Check for lints"""
    print green('Checking for lints')
    return local('flake8').succeeded

#
# @task
# def db():
#     """Connect to the database."""
#     from xword.utils.configuration import config
#     local(
#         'psql -h {} -p {} --username {} {}'.format(
#             config.get('database.host'),
#             config.get('database.port'),
#             config.get('database.user'),
#             config.get('database.name'),
#         ),
#     )


@task
def migrate(command='upgrade head'):
    print green('Running migrations'.format(fab_env['environment']))

    # Migrate tables
    res = local('python manage.py db {}'.format(command))
    if not res.succeeded:
        print red('Failed to migrate tables.')
        return

    print green('Successfully migrated the database.')


@task
def serve():
    """Start the server."""
    local('python app.py')
