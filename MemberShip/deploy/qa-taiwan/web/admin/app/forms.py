# -*- coding: utf-8 -*- 

import os.path
import datetime

from flask.ext.wtf import Form

from wtforms.fields import TextField
from wtforms.fields import SelectField
from wtforms.fields import BooleanField
from wtforms.fields import SubmitField
from wtforms.fields import IntegerField
from wtforms.fields import DateTimeField
from wtforms.fields import FileField
from wtforms.fields import PasswordField
from wtforms.fields import HiddenField
from wtforms.fields import TextAreaField

from wtforms.validators import Required
from wtforms.validators import ValidationError
from wtforms.validators import Optional

from wtforms import widgets
from wtforms import validators
from wtforms.widgets import TextArea


class DateTimePickerWidget(widgets.TextInput):
    """
      Datetime picker widget.
      You must include bootstrap-datepicker.js and form.js for styling to work.
    """
    def __call__(self, field, **kwargs):
        kwargs['data-role'] = u'datetimepicker'
        return super(DateTimePickerWidget, self).__call__(field, **kwargs)


class LoginForm(Form):
    username = TextField(u"Username", validators = [Required(),])
    password = PasswordField(u"Password", validators = [Required(),])

    def validate_on_submit(self):
        if not self.username.data: return False
        if not self.password.data: return False
        return True


class AppForm(Form):
    app_id = TextField(u'App ID', validators = [Required(),])
    app_key = TextField(u'App Key', validators = [Required(),])
    app_secret = TextField(u'App Secret', validators = [Required(),])
    app_name = TextField(u'App Name', validators = [Required(),])

    support_android = BooleanField(u'Android support')
    support_playstore = BooleanField(u'PlayStore support')
    playstore_url = TextField(u'PlayStore URL')

    gcm_sender_id = TextField(u'GCM Sender ID')
    gcm_server_api_key = TextField(u'GCM Server API Key')
    gcm_config_path = FileField(u'GCM Config File Path')

    support_ios = BooleanField(u'iOS support')
    support_appstore = BooleanField(u'AppStore support')
    appstore_url = TextField(u'AppStore URL')

    support_gameflier = BooleanField(u'GameFlier support')
    gameflier_url = TextField(u'GameFlier URL')

    facebook_app_name = TextField(u'Facebook APP Name')
    facebook_app_id = TextField(u'Facebook APP ID')
    facebook_app_secret = TextField(u'Facebook APP Secret')
    facebook_api_version = SelectField(u'Facebook API Version', choices=[], coerce=int, validators=[Required(),])

    status = SelectField(u'Status', choices=[], coerce=int, validators=[Required(),])

    def validate_on_submit(self):
        if not self.app_id.data: return False
        if not self.app_name.data: return False
        return True



class ProductForm(Form):
    app_id = TextField(u'App ID', validators = [Required(),])
    product_id = TextField(u'Product ID', validators = [Required(),])
    inapp_id = TextField(u'InApp ID', validators = [Required(),])
    product_name = TextField(u'Name', validators = [Required(),])
    product_detail = TextField(u'Detail', validators=[Required(),])
    product_price = TextField(u'Price', validators = [Required(),])
    service_platform = SelectField(u'Service Platform', choices=[], coerce=int, validators=[Required(),])
    currency = SelectField(u'Currency', choices=[], coerce=int, validators=[Required(),])
    status = SelectField(u'Status', choices=[], coerce=int, validators=[Required(),])

    def validate_on_submit(self):
        if not self.app_id.data: return False
        if not self.product_id.data: return False
        if not self.inapp_id.data: return False
        if not self.product_name.data: return False
        return True




