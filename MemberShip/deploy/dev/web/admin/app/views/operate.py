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
from app import admin_permission


view = Blueprint('operate', __name__, 
                 template_folder='../templates')


@view.route('/maintenance', methods=['POST', 'GET'])
@login_required
@admin_permission.require(http_exception=403)
def maintenance():
    if request.args.has_key('unlock'):
        models.admin_log(session['user_id'], u"[%s] 점검 즉시 해지를 수행하였습니다." % (request.remote_addr))
        models.end_maintenance()

    # 이미 메인터넌스 모드일 경우, 점검 정보를 보여주고, 해지 여부 결정
    maint = models.maintenance()
    if maint:
        return render_template('operate/maintenance_unlock.html', 
                               maint = maint)

    form = forms.MaintenanceForm()
    if form.validate_on_submit():
        models.admin_log(session['user_id'], u"[%s] 점검 시작(종료예정:%s):%s" % (request.remote_addr, form.end_date.data, form.reason.data))
        models.start_maintenance(form.reason.data, form.end_date.data)
        return redirect(url_for('operate.maintenance'))

    return render_template('operate/maintenance_lock.html', 
                           form=form, h=helpers)



@view.route('/notice')
@login_required
@admin_permission.require(http_exception=403)
def notice():
    notices = models.notices()
    return render_template('operate/notice.html', 
                           notices=notices)


@view.route('/notice/new', methods=['POST', 'GET'])
@login_required
@admin_permission.require(http_exception=403)
def notice_new():
    form = forms.NoticePostForm()
    if form.validate_on_submit():
        models.post_notice(form.title.data,
                           form.mosttop.data,
                           form.start_date.data,
                           form.end_date.data,
                           form.content.data)
        models.admin_log(session['user_id'], u'[%s] 공지사항 생성: %s (%s ~ %s)' % (request.remote_addr, form.title.data, form.start_date.data, form.end_date.data))
        return redirect(url_for('operate.notice'))

    return render_template('operate/notice_edit.html', 
                           form=form, h=helpers)


@view.route('/notice/edit/<int:notice_id>', methods=['POST', 'GET'])
@login_required
@admin_permission.require(http_exception=403)
def notice_edit(notice_id):
    form = forms.NoticePostForm()
    if form.validate_on_submit():
        models.update_notice(notice_id,
                             form.title.data,
                             form.mosttop.data,
                             form.start_date.data,
                             form.end_date.data,
                             form.content.data)
        models.admin_log(session['user_id'], u"[%s] 공지사항 수정: %s" % (request.remote_addr, notice_id))
        return redirect(url_for('operate.notice'))
    else:
        notice = models.notice(notice_id)
        if not notice:
            return abort(404)

        form.title.data = notice['title']
        form.mosttop.data = notice['mosttop']
        form.start_date.data = notice['start_date']
        form.end_date.data = notice['finish_date']
        form.content.data = notice['content']

    return render_template('operate/notice_edit.html', 
                           form=form, h=helpers)



@view.route('/notice/delete/<int:notice_id>')
@login_required
@admin_permission.require(http_exception=403)
def notice_delete(notice_id):
    models.delete_notice(notice_id)
    models.admin_log(session['user_id'], u"[%s] 공지사항 삭제: %s" % (request.remote_addr, notice_id))
    return redirect(url_for('operate.notice'))



@view.route('/admin')
@login_required
@admin_permission.require(http_exception=403)
def admin():
    admins = models.admins()
    return render_template('operate/admin.html',
                           admins = admins)
