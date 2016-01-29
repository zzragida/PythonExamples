# -*- coding:utf-8 -*-

from flask import Blueprint
from flask import render_template
from flask import abort
from flask import redirect
from flask import request

from flask.ext.login import login_required
from flask.ext.babel import gettext

from app import models
from app import admin_permission

view = Blueprint('monitor', __name__, 
                 template_folder='../templates')


@view.route('/process')
@login_required
def process():
    memberships = models.get_memberships()
    pushs = models.get_pushs()
    monitor = models.get_monitor()
    members = models.get_members()
    return render_template('monitor/process.html',
                           memberships = memberships,
                           pushs = pushs,
                           monitor = monitor,
                           members = members)


@view.route('/push')
@login_required
def push():
    push_list = models.push_list()
    return render_template('monitor/push.html',
                           push_list = push_list)


@view.route('/cache')
@login_required
def cache():
    pass



@view.route('/reload')
@login_required
def reload():
    results = models.reload()
    return render_template('monitor/reload.html',
                           results = results)


