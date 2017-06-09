import os
from flask import Flask, url_for, redirect, render_template, request, abort, flash
from flask_sqlalchemy import SQLAlchemy
from flask_security import Security, SQLAlchemyUserDatastore, \
    UserMixin, RoleMixin, login_required, current_user, LoginForm
from flask_security.utils import encrypt_password
import flask_admin
from flask_admin.contrib import sqla
from flask_admin import helpers as admin_helpers
from flask_admin import AdminIndexView, expose
from flask_login import LoginManager, login_user
from werkzeug.security import check_password_hash, generate_password_hash
from wtforms import StringField, PasswordField, SubmitField, validators
from flask_wtf import FlaskForm

from model import *


# Create Flask application
app = Flask(__name__)
app.config.from_pyfile('config.py')
#db = SQLAlchemy(app)
db.init_app(app)
login_manager = LoginManager()
login_manager.init_app(app)
user = current_user




@login_manager.user_loader
def load_user(user_id):
    return User.get(user_id)

class LoginForm(FlaskForm):
    username = StringField('Username', [validators.DataRequired()])
    password = PasswordField('Password', [validators.DataRequired()])
    #submit = SubmitField()

    def __init__(self, *args, **kwargs):
        FlaskForm.__init__(self, *args, **kwargs)
        self.user = None

    def validate(self):
        rv = FlaskForm.validate(self)
        if not rv:
            return False

        user = User.query.filter_by(
            username=self.username.data).first()
        if user is None:
            self.username.errors.append('Unknown username')
            return False

        if not user.check_password(self.password.data):
            self.password.errors.append('Invalid password')
            return False

        self.user = user
        return True

# Setup Flask-Security
user_datastore = SQLAlchemyUserDatastore(db, User, Role)
security = Security(app, user_datastore)


# Create customized model view class for admin page
class MyModelView(sqla.ModelView):

    def is_accessible(self):
        if not current_user.is_active or not current_user.is_authenticated:
            return False

        if current_user.has_role('superuser'):
            return True

        return False

    def _handle_view(self, name, **kwargs):
        """
        Override builtin _handle_view in order to redirect users when a view is not accessible.
        """
        if not self.is_accessible():
            if current_user.is_authenticated:
                # permission denied
                abort(403)
            else:
                # login
                return redirect(url_for('security.login', next=request.url))

# Flask views
@app.route('/')
def index():
    return render_template('test.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    # Here we use a class of some kind to represent and validate our
    # client-side form data. For example, WTForms is a library that will
    # handle this for us, and we use a custom LoginForm to validate.
    form = LoginForm()
    # if form.is_submitted():
    if form.validate_on_submit():
        # Login and validate the user.
        # user should be an instance of your `User` class
        login_user(user)

        flash('Logged in successfully.')

        next = request.args.get('next')
        # is_safe_url should check if the url is safe for redirects.
        # See http://flask.pocoo.org/snippets/62/ for an example.
        # if not is_safe_url(next):
            # return flask.abort(400)

        return redirect(next or url_for('index'))
    return render_template('login.html', form=form)

class MyHomeView(AdminIndexView):
    @expose('/')
    def index(self):
        arg1 = 'Hello'
        return self.render('admin/index.html', arg0=arg1) 


# Create admin
admin = flask_admin.Admin(
    app,
    'Example: Auth',
    base_template='my_master.html',
    template_mode='bootstrap3',
)

# Add model views
admin.add_view(MyModelView(Role, db.session))
admin.add_view(MyModelView(User, db.session))

# define a context processor for merging flask-admin's template context into the
# flask-security views.
@security.context_processor
def security_context_processor():
    return dict(
        admin_base_template=admin.base_template,
        admin_view=admin.index_view,
        h=admin_helpers,
        get_url=url_for
    )


#Add last modified time stamp for static resources
@app.context_processor
def override_url_for():
    return dict(url_for=dated_url_for)

def dated_url_for(endpoint, **values):
    if endpoint == 'static':
        filename = values.get('filename', None)
        if filename:
            file_path = os.path.join(app.root_path,
                                     endpoint, filename)
            values['q'] = int(os.stat(file_path).st_mtime)
    return url_for(endpoint, **values)


if __name__ == '__main__':

    # Build a sample db on the fly, if one does not exist yet.
    app_dir = os.path.realpath(os.path.dirname(__file__))
    database_path = os.path.join(app_dir, app.config['DATABASE_FILE'])

    # Start app
    app.run(debug=True)
