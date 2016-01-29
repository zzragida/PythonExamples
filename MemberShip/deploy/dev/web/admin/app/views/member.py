# -*- coding:utf-8 -*-

from flask import Blueprint
from flask import render_template
from flask import abort
from flask import redirect
from flask import request
from flask import session
from flask import url_for

from flask.ext.babel import gettext
from flask.ext.login import login_required


from app import forms
from app import helpers
from app import models


view = Blueprint('member', __name__, 
                 template_folder='../templates')


@view.route('/')
@login_required
def members():
    pass


@view.route('/<member_id>')
@login_required
def members_detail(member_id):
    pass
