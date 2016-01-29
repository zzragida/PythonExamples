# -*- coding:utf-8 -*-

import os

from flask import Blueprint
from flask import render_template
from flask import abort
from flask import redirect
from flask import request
from flask import session
from flask import url_for
from flask import send_from_directory

from flask.ext.babel import gettext
from flask.ext.login import login_required

from config import ADMIN_UPLOAD_PATH as UPLOAD_PATH

from app import forms
from app import helpers
from app import models

from util import make_pagination


view = Blueprint('apps', __name__, 
                 template_folder='../templates')


@view.route('/')
@login_required
def apps():
    apps = models.apps()
    return render_template('apps/apps.html',
                           apps = apps)


@view.route('/<int:app_id>')
@login_required
def apps_detail(app_id):
    app = models.apps_detail(app_id)
    if not app:
        return abort(404)

    products = models.products(app_id)
    return render_template('apps/apps_detail.html',
                           app = app,
                           products = products)


@view.route('/new', methods=['POST', 'GET'])
@login_required
def apps_new():
    form = forms.AppForm()
    if form.validate_on_submit():
        models.apps_new(form)
        return redirect('/apps')

    form.app_id.data = models.auto_created()
    form.app_id.readonly = True
    form.app_key.data = models.auto_created()
    form.app_key.readonly = True
    form.app_secret.data = models.auto_created()
    form.app_secret.readonly = True
    form.facebook_api_version.choices = models.facebook_api_version_choices()
    form.status.choices = models.app_status_choices()
    
    return render_template('apps/apps_edit.html',
                           form = form, h = helpers)


@view.route('/edit/<int:app_id>', methods=['POST', 'GET'])
@login_required
def apps_edit(app_id):
    app = models.apps_detail(app_id)
    if not app:
        return abort(404)

    form = forms.AppForm()
    if form.validate_on_submit():
        models.apps_edit(form)
        return redirect('/apps')

    form.app_id.data = app['app_id']
    form.app_id.readonly = True
    form.app_key.data = app['app_key']
    form.app_key.readonly = True
    form.app_secret.data = app['app_secret']
    form.app_secret.readonly = True
    form.app_name.data = app['app_name']

    form.support_android.data = app['support_android']
    form.support_playstore.data = app['support_playstore']
    form.playstore_url.data = app['playstore_url']
    form.gcm_sender_id.data = app['gcm_sender_id']
    form.gcm_server_api_key.data = app['gcm_server_api_key']
    form.gcm_config_path.data = app['gcm_config_path']

    form.support_ios.data = app['support_ios']
    form.appstore_url.data = app['appstore_url']

    form.support_gameflier.data = app['support_gameflier']
    form.gameflier_url.data = app['gameflier_url']

    form.facebook_app_id.data = app['facebook_app_id']
    form.facebook_app_name.data = app['facebook_app_name']
    form.facebook_app_secret.data = app['facebook_app_secret']
    form.facebook_api_version.choices = models.facebook_api_version_choices()
    form.facebook_api_version.data = models.facebook_api_version_index(app['facebook_api_version'])

    form.status.choices = models.app_status_choices()
    form.status.data = models.app_status_index(app['status'])

    return render_template('apps/apps_edit.html',
                           form = form, h = helpers)


@view.route('/delete/<int:app_id>', methods=['POST', 'GET'])
@login_required
def apps_delete(app_id):
    models.apps_delete(app_id)
    return redirect('/apps')


@view.route('/file/<int:app_id>/<filename>')
@login_required
def apps_file(app_id, filename):
    upload_path = os.path.join(UPLOAD_PATH, str(app_id))
    return send_from_directory(upload_path, filename)



@view.route('/<int:app_id>/products')
@login_required
def products(app_id):
    products = models.products(app_id)
    return render_template('apps/products.html',
                           app_id = app_id,
                           products = products)


@view.route('/<int:app_id>/products/<int:product_id>')
@login_required
def products_detail(app_id, product_id):
    product = models.products_detail(app_id, product_id)
    if not product:
        abort(404)

    return render_template('apps/products_detail.html',
                           product = product)


@view.route('/<int:app_id>/products/new', methods=['POST', 'GET'])
@login_required
def products_new(app_id):
    form = forms.ProductForm()
    if form.validate_on_submit():
        models.products_new(form)
        return redirect('/apps/%d/products' % (app_id))

    form.app_id.data = app_id
    form.app_id.readonly = True
    form.product_id.data = models.auto_created()
    form.product_id.readonly = True
    form.service_platform.choices = models.service_platform_choices()
    form.currency.choices = models.currency_type_choices()
    form.status.choices = models.product_status_choices()

    return render_template('apps/products_edit.html',
                           app_id = app_id,
                           form = form, h = helpers)


@view.route('/<int:app_id>/products/edit/<int:product_id>', methods=['POST', 'GET'])
@login_required
def products_edit(app_id, product_id):
    product = models.products_detail(app_id, product_id)
    if not product:
        return abort(404)

    form = forms.ProductForm()
    if form.validate_on_submit():
        models.products_edit(form)
        return redirect('/apps/%d/products' % (app_id))

    form.app_id.data = product['app_id']
    form.app_id.readonly = True
    form.product_id.data = product['product_id']
    form.product_id.readonly = True
    form.product_name.data = product['product_name']
    form.product_detail.data = product['product_detail']
    form.product_price.data = product['product_price']
    form.inapp_id.data = product['inapp_id']
    form.service_platform.choices = models.service_platform_choices()
    form.service_platform.data = models.service_platform_index(product['service_platform'])
    form.currency.choices = models.currency_type_choices()
    form.currency.data = models.currency_type_index(product['currency'])
    form.status.choices = models.product_status_choices()
    form.status.data = models.product_status_index(product['status'])
    
    return render_template('apps/products_edit.html',
                           app_id = app_id,
                           form = form, h = helpers)


@view.route('/<int:app_id>/products/delete/<int:product_id>', methods=['POST', 'GET'])
@login_required
def products_delete(app_id, product_id):
    models.products_delete(app_id, product_id)
    return redirect('/apps/%d/products' % (app_id))


@view.route('/<int:app_id>/payments', defaults={'page':1})
@view.route('/<int:app_id>/payments/page=<int:page>')
@login_required
def payments(app_id, page):
    # 검색 조건 가져오기
    # TODO: 검색 조건 추가
    member_id = request.args.get('member_id', None)
    product_id = request.args.get('product_id', None)

    # 멤버 아이디로 검색
    if member_id:
        total, payments = models.payments(app_id, page-1, member_id=long(member_id))

    # 상품 아이디로 검색
    elif product_id:
        total, payments = models.payments(app_id, page-1, product_id=long(product_id))

    # 총 결제정보
    else:
        total, payments = models.payments(app_id, page-1)

    pagination = make_pagination(page, total, 'payments')
    return render_template('apps/payments.html',
                           app_id = app_id,
                           total = total,
                           payments = payments,
                           pagination = pagination)


@view.route('/<int:app_id>/payments/<int:payment_id>')
@login_required
def payments_detail(app_id, payment_id):
    payment = models.payments_detail(app_id, payment_id)
    if not payment:
        return abort(404)

    return render_template('apps/payments_detail.html',
                           payment = payment)



@view.route('/<int:app_id>/members', defaults={'page':1})
@view.route('/<int:app_id>/members/page=<int:page>')
@login_required
def members(app_id, page):
    # 검색 조건 가져오기
    member_id = request.args.get('member_id', None)
    facebook_id = request.args.get('facebook_id', None)

    # 멤버 아이디로 검색
    if member_id:
        total, members = models.members(app_id, page-1, member_id=long(member_id))

    # 페이스북 아이디로 검색
    elif facebook_id:
        total, members = models.members(app_id, page-1, facebook_id=long(facebook_id))

    # 총 멤버정보
    else:
        total, members = models.members(app_id, page-1)

    pagination = make_pagination(page, total, 'members')
    return render_template('apps/members.html',
                           app_id = app_id,
                           total = total,
                           members = members,
                           pagination = pagination)


@view.route('/<int:app_id>/members/<int:member_id>')
@login_required
def members_detail(app_id, member_id):
    member = models.members_detail(app_id, member_id)
    if not member:
        abort(404)

    return render_template('apps/members_detail.html',
                           app_id = app_id,
                           member = member)


@view.route('/<int:app_id>/members/<int:member_id>/history')
@login_required
def members_history(app_id, member_id):
    access, payment, push = models.members_history(app_id, member_id)
    return render_template('apps/members_history.html',
                           app_id = app_id,
                           member_id = member_id,
                           access = access,
                           payment = payment,
                           push = push)
