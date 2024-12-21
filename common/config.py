from oslo_config import cfg

conf = cfg.CONF

database_opts = [
    cfg.StrOpt('host', default='localhost', help='The host in which the database is currently running.'),
    cfg.IntOpt('port', default=27017, help='The port in which the database is running.'),
    cfg.StrOpt('username', default=None, help='The username with which the database can connect to.'),
    cfg.StrOpt('password', default=None, help='The password with which the database can connect to'),
    cfg.StrOpt('database', default='admin', help='The auth database to which the connection is made.'),
    cfg.StrOpt('name', default='crypto_db', help='The auth database to which the connection is made.'),
    cfg.StrOpt('collection_name', default='coin_details', help='The auth database to which the connection is made.')
]

token_opts = [
    cfg.StrOpt('JWT_SECRET_KEY', default="", help="jwt secret key")
]
conf.register_opts(database_opts, group='database')
conf.register_opts(token_opts, group='token')


def startup_sanity_checks():
    if not any([cfg.CONF.database.username, cfg.CONF.database.password]):
        raise Exception("You must specify both a username and a password.")
