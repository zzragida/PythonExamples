# -*- coding:utf-8 -*-

from flask import Blueprint
from flask import render_template
from flask import abort
from flask import request
from flask import redirect
from flask import url_for

from flask.ext.login import login_required
from flask.ext.babel import gettext

from config import MONGODB_HOST as HOST
from config import MONGODB_PORT as PORT
from config import MONGODB_DB as DB
from config import PER_PAGE

from mongoengine import Document
from mongoengine import IntField
from mongoengine import StringField
from mongoengine import DateTimeField

from app import forms
from app import helpers

from util import make_pagination

import re
import pymongo
import datetime

view = Blueprint('log', __name__, 
                 template_folder='../templates')


@view.route('/collections')
@login_required
def collections():
    db = connect_db()

    collections = []
    for col in db.collection_names():
        if col == 'system.indexes': continue
        try:
            #col = int(col)
            collections.append(col)
        except ValueError:
            pass

    collections.sort()
    return render_template('log/collections.html', 
                           collections = collections)


@view.route('/collection/<collection>', methods=['GET'])
@login_required
def collection(collection):
    db = connect_db()
    doc = db[collection]

    pid = request.args.get('pid', None)
    level = request.args.get('level', None)
    name = request.args.get('name', None)
    find = request.args.get('find', None)
    page = int(request.args.get('page', 1))

    search_options = []
    if pid: search_options.append({'process': int(pid)})
    if level: search_options.append({'levelname': level})
    if name: search_options.append({'name': name})
    if find:
        find_search = re.compile(".*"+find+".*", re.IGNORECASE)
        search_options.append({'msg': find_search})

    if len(search_options) > 1:
        search = { "$and": search_options }
    elif len(search_options) == 1:
        search = search_options[0]
    else:
        search = {}

    total = doc.find(search).count()
    pagination = make_pagination(page, total, 'records')

    results = doc.find(search).sort("time", pymongo.DESCENDING).skip((page-1) * PER_PAGE).limit(PER_PAGE)

    url = request.path + "?"
    if pid: url += "pid=%s&" % pid
    if level: url += "level=%s&" % level
    if name: url += "name=%s&" % name
    if find: url += "find=%s&" % find

    records = []
    for r in results:
        try:
            r['tags']
        except KeyError:
            r['tags'] = ''

        records.append({
          'level': r['levelname'],
          'time': r['time'],
          'pid': r['process'],
          'message': r['msg'],
          'host': r['host'],
          'pathname': r['pathname'],
          'lineno': r['lineno'],
          'name': r['name'],
        })

    return render_template('log/list.html',
                           uri = request.path,
                           url = url,
                           pagination = pagination,
                           collection = collection,
                           records = records,
                           time = dispTime,
                           pid = pid,
                           level = level,
                           name = name,
                           find = find)



@view.route('/indexed')
@login_required
def indexed():
    db = connect_db()

    for col in db.collection_names():
        if col == 'system.indexes': continue
        try:
            #if col.isdigit():
            db[col].ensure_index("logging_time")
        except ValueError:
            pass

    return redirect(url_for('log.collections'))


@view.route('/config')
@login_required
def config():
    db = connect_db()

    collections = []
    for col in db.collection_names():
        if col == 'system.indexes': continue
        try:
            info = db.command('collstats', col)
            collections.append({
                 #'name': int(col),
                 'name': col,
                 'count': info['count'],
                 'ns': info['ns'],
                 'size': int(info['storageSize'])
            })
        except ValueError:
            pass

    collections.sort(key=lambda k: k['name'])
    return render_template('log/config.html',
                           collections = collections)


@view.route('/config/<collection>', methods=['POST', 'GET'])
@login_required
def config_edit(collection):
    db = connect_db()
    form = forms.LogConfigEditForm()
    if form.validate_on_submit():
        # 새롭게 설정된 크기로 변경함
        try:
            db.command('convertToCapped', 
                       collection, 
                       size = int(form.value.data))
        except ValueError:
            pass
        return redirect(url_for('log.config'))
    else:
        if collection.isdigit() == False:
            return redirect(url_for('log.config'))

        # 현재 컬랙션의 크기를 보여줌
        try:
            info = db.command('collstats', collection)
            form.value.data = info['storageSize']
        except ValueError:
            pass

    return render_template('log/config_edit.html',
                           form = form,
                           collection = collection,
                           h = helpers)



@view.route('/delete/<collection>', methods=['POST'])
@login_required
def delete(collection):
    db = connect_db()
    try:
        db[collection].drop()
    except ValueError:
        pass
    return redirect(url_for('log.config'))




def dispTime(time):
    return datetime.datetime.strptime(time, "%Y%m%dT%H%M%S.%f")


def connect_db():
    mongo = pymongo.Connection(HOST, PORT)
    db = mongo[DB]
    return db


class Log(Document):
    service_id = IntField(required=True)
    pid = IntField(required=True)
    service_name = StringField(required=True)
    service_port = IntField(required=True)
    ip = StringField(required=True)
    logging_time = DateTimeField(required=True)
    level = IntField(required=True)
    time = DateTimeField(required=True)
    filename = StringField(required=True)
    line = IntField(required=True)
    logger = StringField()
    tags = StringField()
    message = StringField()

