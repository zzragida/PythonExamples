# -*- coding:utf-8 -*-

from flask import Blueprint
from flask import session
from flask import request
from flask import redirect
from flask import render_template
from flask import current_app

from flask.ext.babel import gettext

from flask.ext.login import login_required
from flask.ext.login import login_user
from flask.ext.login import logout_user
from flask.ext.login import current_user
from flask.ext.login import UserMixin

from flask.ext.principal import Identity
from flask.ext.principal import identity_changed
from flask.ext.principal import AnonymousIdentity

from app import helpers
from app import forms
from app import models


view = Blueprint('index', __name__,
                 template_folder='../templates')


class User(UserMixin):
    def __init__(self, user_id="", password=""):
        self.user_id = user_id
        self.password = password

    def is_authenticated(self):
        return True

    def is_active(self):
        return True

    def is_anonymous(self):
        return False

    def get_id(self):
        return self.user_id



@view.route('')
@login_required
def index():
    return render_template('index.html')



@view.route('login', methods=['GET', 'POST'])
def login():
    form = forms.LoginForm()
    if form.validate_on_submit():
        admin_id = models.avaliable_admin(form.username.data, form.password.data)
        if admin_id:
            # Keep the user info in the session using Flask-Login
            login_user(User(form.username.data, form.password.data))

            # Tell Flask-Principal the identity changed
            identity_changed.send(current_app._get_current_object(),
                                  identity = Identity(admin_id))
            return redirect('/')

    return render_template('login.html',
                           form = form,
                           h = helpers)


@view.route('logout')
@login_required
def logout():
    # Remove the user information from the session
    logout_user()

    # Remove session keys set by Flask-Principal
    for key in ('identity.name', 'identity.auth_type'):
        session.pop(key, None)

    # Tell Flask-Principal the user is anonymous
    identity_changed.send(current_app._get_current_object(),
                          identity = AnonymousIdentity())
    return redirect('/')


