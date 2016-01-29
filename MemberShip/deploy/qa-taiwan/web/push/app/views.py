# -*- coding: utf-8 -*-

from flask import abort
from flask import request
from flask import jsonify
from flask import Response

from app import logger
from app import models

import app

import simplejson as json
import datetime


def _debug(request, message):
    logger.debug('%s;{remote_addr:%s}' % (message, request.remote_addr))

def _info(request, message):
    logger.info('%s;{remote_addr:%s}' % (message, request.remote_addr))

def _warn(request, message):
    logger.warning('%s;{remote_addr:%s}' % (message, request.remote_addr))

def _error(request, message, code=None, err=None):
    if err:
        logger.error('%s;{remote_addr:%s};%s' % (message, request.remote_addr, err))
    else:
        logger.error('%s;{remote_addr:%s}' % (message, request.remote_addr))
    if code:
        abort(code, message)

def _make_error(message, status_code):
    response = jsonify(message=message)
    response.status_code = status_code
    return response


@app.app.errorhandler(400)
def bad_request(error):
    message = error.description if hasattr(error, 'description') else 'Bad request'
    return _make_error(message, 400)


@app.app.errorhandler(401)
def unauthorized(error):
    message = error.description if hasattr(error, 'description') else 'Unauthroized'
    return _make_error(message, 401)


@app.app.errorhandler(404)
def not_found(error):
    message = error.description if hasattr(error, 'description') else 'Not found'
    return _make_error(message, 404)


@app.app.errorhandler(406)
def not_acceptable(error):
    message = error.description if hasattr(error, 'description') else 'Not acceptable'
    return _make_error(message, 406)


@app.app.errorhandler(500)
def internal_server_error(error):
    message = error.description if hasattr(error, 'description') else 'Internal Server Error'
    return _make_error(message, 500)


def _verify_push(request):
    # gcm_sender_id
    gcm_sender_id = request.form['gcm_sender_id']
    if not gcm_sender_id:
        _error(request, 'GCM Sender Id is not found', 404)

    # gcm_server_api_key
    gcm_server_api_key = request.form['gcm_server_api_key']
    if not gcm_server_api_key:
        _error(request, 'GCM Server API key is not found', 404)

    # app_id
    app_id = request.form['app_id']
    if not app_id:
        _error(request, 'Application Id is not found', 404)
    app_id = int(app_id)

    # member_ids
    member_ids = request.form['member_ids']
    if not member_ids:
        _error(request, 'Member Ids is not found', 404)

    # verify member_ids
    members = member_ids.split(',')
    if len(members) == 0:
        _error(request, 'MMember Ids is required: %s' % (member_ids), 404)

    # message
    message = request.form['message']
    if not message:
        _error(request, 'Message is not found', 404)

    # verify message json format
    try:
        json.loads(message)
    except ValueError as err:
        _error(request, 'Invalid message for: %s' % (message), 404, err)

    # time
    time = request.form['time']
    if not time:
        _error(request, 'Time is not found', 404)

    # verify time format (YYYY-MM-DD HH:mm:SS)
    try:
        time = datetime.datetime.strptime(time, '%Y-%m-%d %H:%M:%S')
    except ValueError as err:
        _error(request, 'Invalid time format: %s' % (time), 404, err)

    # now < time
    now = datetime.datetime.now()

    return gcm_sender_id, gcm_server_api_key, app_id, member_ids, message, time


@app.app.route('/api/push', methods=['POST'])
def push():
    _debug(request, 'push api requested')

    # verify push
    gcm_sender_id, gcm_server_api_key, app_id, member_ids, message, time = _verify_push(request)

    # register push message
    models.push(gcm_sender_id, gcm_server_api_key, app_id, member_ids, message, time)

    return jsonify(result='OK')


@app.app.route('/api/monitor', methods=['GET'])
def monitor():
    _debug(request, 'monitor api requested')

    push_list = models.monitor()

    return Response(json.dumps(push_list), mimetype='application/json')


