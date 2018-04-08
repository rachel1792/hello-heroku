import os
import sys

from fabric.colors import green, red, blue, magenta

from fabric.decorators import task, runs_once, parallel
from fabric.operations import prompt, local
from fabric.state import env as fab_env


@task()
def shell():
    """Run the Olympus shell given previously loaded config"""
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
def serve():
    """Start the server."""
    local('python app.py')
