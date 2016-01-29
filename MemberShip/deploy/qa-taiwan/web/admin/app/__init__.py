# -*- coding:utf-8 -*-

import os
import sys
sys.path.insert(0, '../')

from flask import Flask
from flask import g
from flask import request
from flask import session
from flask import abort
from flask import render_template
from flask import redirect

from flask.ext.login import LoginManager
from flask.ext.login import login_required

from flask.ext.principal import Principal
from flask.ext.principal import Permission
from flask.ext.principal import RoleNeed
from flask.ext.principal import identity_loaded

from flask.ext.babel import Babel

from config import ADMIN_SERVICE_NAME as SERVICE_NAME
from config import ADMIN_HOST as HOST
from config import ADMIN_PORT as PORT
from config import ADMIN_SECRET_KEY as SECRET_KEY
from config import ADMIN_DEBUG as DEBUG
from config import ADMIN_LOG_LEVEL as LOG_LEVEL
from config import ADMIN_LOG_FILENAME as LOG_FILENAME

from config import MONGODB_HOST
from config import MONGODB_PORT
from config import MONGODB_DB

# initialize flask
app = Flask(__name__, static_folder='static')
app.debug = DEBUG
app.secret_key = SECRET_KEY


from logger import get_logger

import config
import db
import nosql
import models


# initialize logger
logger = get_logger(app, SERVICE_NAME, LOG_LEVEL, LOG_FILENAME,
                    MONGODB_HOST, MONGODB_PORT, MONGODB_DB, SERVICE_NAME)

# initialize flask principal
principals = Principal(app)
be_admin = RoleNeed('admin')
admin_permission = Permission(be_admin)

@identity_loaded.connect_via(app)
def on_identity_loaded(sender, identity):
    if identity.id == u'admin':
        identity.provides.add(be_admin)


# initialize flask login
login_manager = LoginManager()
login_manager.login_view = 'index.login'
login_manager.init_app(app)

@login_manager.user_loader
def load_user(user_id):
    return index.User()

# initialize Bable for i18n
babel = Babel(app)

@babel.localeselector
def get_locale():
    lang = session.get('lang', 'ko')
    setattr(g, 'lang', lang)
    logger.info('get_locale lang: %s' % (lang))
    return lang


@app.route('/lang/<language>')
@login_required
def lang(language=None):
    if not language: language = 'ko'
    setattr(g, 'lang', language)
    session['lang'] = language
    # TODO(kjs): refresh current page
    logger.info('lang: %s' % (session.get('lang')))
    return redirect('/')


@app.route('/sitemap')
@login_required
@admin_permission.require(http_exception=403)
def sitemap():
    return render_template('sitemap.html',
                           rules = app.url_map.iter_rules())


@app.errorhandler(404)
def page_not_found(e):
    return render_template('error/404.html'), 404


@app.errorhandler(403)
def forbidden(e):
    return render_template('error/403.html'), 403


@app.errorhandler(500)
def internal_server_error(e):
    return render_template('error/500.html'), 500


# register blueprint
from views import index
from views import operate
from views import log
from views import monitor
from views import apps
from views import member

app.register_blueprint(index.view, url_prefix='/')
app.register_blueprint(operate.view, url_prefix='/operate')
app.register_blueprint(log.view, url_prefix='/log')
app.register_blueprint(monitor.view, url_prefix='/monitor')
app.register_blueprint(apps.view, url_prefix='/apps')
app.register_blueprint(member.view, url_prefix='/member')


