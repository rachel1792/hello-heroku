import os
import sys

from fabric.colors import green, red, blue
from fabric.context_managers import settings
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

    # TODO: Make the path work generically
    os.environ['PYTHONPATH'] = "/Users/rachelkogan/xword-app"


@task
def test():
    """Load test configuration"""
    _set_current_environment('test')


@task
def dev():
    """Load test configuration"""
    _set_current_environment('dev')


def environment():
    """Bootstrap the environment."""
    local('mkdir -p logs')
    print green('\nInstalling requirements')
    local('pip install -r requirements.txt')
    # local('python setup.py develop')


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


@task
def db():
    """Connect to the database."""
    from xword.utils.configuration import config
    local(
        'psql -h {} -p {} --username {} {}'.format(
            config.get('database.host'),
            config.get('database.port'),
            config.get('database.user'),
            config.get('database.name'),
        ),
    )


@task
def migrate(command='upgrade head'):
    """Database migration."""
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


@task()
def shell():
    """Run the shell."""
    local("python manage.py shell")


@task()
def bootstrap_database(force=False):
    """Bootstrap the database."""

    if fab_env['environment'] == 'prod' and not force:
        raise ValueError('Bootstrapping the production database is not allowed.')

    from xword.utils.configuration import config
    with settings(warn_only=True):
        # Create a new role
        # local(
        #     'psql -h {} -p {} -c "CREATE ROLE {} WITH ENCRYPTED PASSWORD \'{}\' '
        #     'SUPERUSER CREATEDB CREATEROLE LOGIN;"'.format(
        #         config.get('database.host'),
        #         config.get('database.port'),
        #         config.get('database.user'),
        #         config.get('database.password'),
        #     )
        # )
        # Drop the existing database if it exists
        local(
            'dropdb -U {} -h {} -p {} -w {} --if-exists'.format(
                config.get('database.user'),
                config.get('database.host'),
                config.get('database.port'),
                config.get('database.name'),
            )
        )
        # Create the database
        res = local(
            'createdb -h {} -p {} -U {} -w -E UTF8 -O {} {}'.format(
                config.get('database.host'),
                config.get('database.port'),
                config.get('database.user'),
                config.get('database.user'),
                config.get('database.name'),
            )
        )
        if not res.succeeded:
            print red('Failed to bootstrap the database.')
            return

        # Migrate tables
        migrate('upgrade head')
