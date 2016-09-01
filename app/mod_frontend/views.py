import requests

from flask import current_app, render_template, url_for, flash
from flask_wtf import Form, RecaptchaField
from wtforms import StringField, PasswordField, SelectField, SubmitField
from wtforms.validators import DataRequired

from app.mod_frontend import mod_frontend


@mod_frontend.route('/', methods=['GET', 'POST'])
def index():
    """Landing page.

    This is the main page when accessing the app through a web browser. It
    gives some basic informations and links to the sourcecode and documentary.
    It also has some kind of API example. You can get a ical link through
    entering credentials in the form.
    """
    class GetIcalForm(Form):
        username = StringField(
            '', description='Username',
            validators=[DataRequired()])

        password = PasswordField(
            '', description='Password',
            validators=[DataRequired()])

        facility = SelectField(
            '', description='Facility',
            choices=[(i, j['metadata']['name'])
                     for i, j in current_app.facilities.items()],
            validators=[DataRequired()])

        if 'RECAPTCHA_PUBLIC_KEY' in current_app.config and \
                'RECAPTCHA_PRIVATE_KEY' in current_app.config:
            recaptcha = RecaptchaField()

        submit = SubmitField()

    form = GetIcalForm()

    if form.validate_on_submit():
        url = url_for('mod_api.get_token', facility=form.facility.data,
                      _external=True)

        r = requests.post(url,
                          json={'username': form.username.data,
                                'password': form.password.data})

        if r.status_code == 200:
            token = r.json().get('token')

            if token:
                token_url = '{}?token={}'.format(
                    url_for('mod_api.lent_ical', facility=form.facility.data),
                    token)
                current_app.logger.info(
                    'created token url: {}'.format(token_url)
                )

                flash(token_url, 'success')

            else:
                flash('No token recieved!', 'danger')

        else:
            flash('Connection problems with the API!', 'danger')

    # create a facility metadata dict
    facilities = {}
    for i, j in current_app.facilities.items():
        facilities[i] = j['metadata']

    return render_template('index.html', form=form, facilities=facilities)
