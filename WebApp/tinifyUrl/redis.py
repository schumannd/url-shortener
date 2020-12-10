from redis import Redis

import click
from flask import g
from flask.cli import with_appcontext


def get_redis():
    """
    Connect to redis. The connection is unique for each request and will be reused if this is called again.
    """
    if 'redis' not in g:
        g.redis = Redis(host='redis', port=6379)

    return g.redis


@click.command('init-redis')
@with_appcontext
def init_redis_command():
    """Clear existing data and create new tables."""
    get_redis()
    click.echo("Initialized redis.")


def init_app(app):
    """Register database functions with the Flask app. This is called by
    the application factory.
    """
    app.cli.add_command(init_redis_command)
