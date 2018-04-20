import os
import requests
import json
from yelp_key import key
from flask import Flask, render_template, session, redirect, request, url_for, flash
from flask_script import Manager, Shell
from flask import jsonify
from flask_wtf import FlaskForm
from wtforms import StringField, RadioField, SubmitField, FileField, PasswordField, BooleanField, SelectMultipleField, ValidationError
from wtforms.validators import Required, Length, Email, Regexp, EqualTo
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate, MigrateCommand
from werkzeug.security import generate_password_hash, check_password_hash

from flask_login import LoginManager, login_required, logout_user, login_user, UserMixin, current_user
from werkzeug.security import generate_password_hash, check_password_hash

app = Flask(__name__)
app.debug = True
app.use_reloader = True
# app.config['HEROKU_ON'] = os.environ.get('HEROKU')
app.config['SECRET_KEY'] = 'hard to guess string from si364'
app.config["SQLALCHEMY_DATABASE_URI"] = os.environ.get('DATABASE_URL') or "postgresql://localhost/SI364projectplanJESSVU"
app.config['SQLALCHEMY_COMMIT_ON_TEARDOWN'] = True
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

manager = Manager(app)
db = SQLAlchemy(app)
migrate = Migrate(app, db)
manager.add_command('db', MigrateCommand)

login_manager = LoginManager()
login_manager.session_protection = 'strong'
login_manager.login_view = 'login'
login_manager.init_app(app)

tags = db.Table('tags', db.Column('search_id', db.Integer, db.ForeignKey('searches.id')), db.Column('business_id', db.Integer, db.ForeignKey('businesses.id')))

user_list = db.Table('user_list', db.Column('businesses_id', db.Integer, db.ForeignKey('businesses.id')),db.Column('list_id',db.Integer, db.ForeignKey('lists.id')))



########################
######## Models ########
########################
class User(UserMixin, db.Model):
    __tablename__ = "users"
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(255), unique=True, index=True)
    email = db.Column(db.String(64), unique=True, index=True)
    password_hash = db.Column(db.String(128))
    list = db.relationship('BusinessList', backref='User')

    @property
    def password(self):
        raise AttributeError('password is not a readable attribute')

    @password.setter
    def password(self, password):
        self.password_hash = generate_password_hash(password)

    def verify_password(self, password):
        return check_password_hash(self.password_hash, password)

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id)) 
#lines 45-66 modeled after Hw4


class Business(db.Model):
    __tablename__ = "businesses"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(128))
    business_location = db.Column(db.String(128))
    url = db.Column(db.String(256))

    def __repr__(self):
        return "{} in {} (url: {})".format(self.name,self.business_location,self.url)

class BusinessRating(db.Model):
    __tablename__ = "ratings"
    id = db.Column(db.Integer, primary_key=True)
    businessName = db.Column(db.String(128))
    businessLocation = db.Column(db.String(128))
    businessRating = db.Column(db.Integer)

    def __repr__(self):
        return "{}, {} (Stars: {})".format(self.businessName, self.businessLocation, self.businessRating)

class BusinessList(db.Model):
    __tablename__ = "lists"
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(255))
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    businesses = db.relationship('Business', secondary=user_list,backref=db.backref('lists', lazy='dynamic'),lazy='dynamic')

    def __repr__(self):
        return "{} (id: {})".format(self.title, self.user_id)

class SearchTerm(db.Model):
    __tablename__ = "searches"
    id = db.Column(db.Integer, primary_key=True)
    business_search = db.Column(db.String(32), unique=True)
    location_search = db.Column(db.String(32), unique=True)
    businesses = db.relationship('Business', secondary=tags,backref=db.backref('searches', lazy='dynamic'),lazy='dynamic')

    def __repr__(self):
        return "{}, {}".format(self.business_search, self.location_search)

########################
######## Forms #########
########################
class RegistrationForm(FlaskForm):
    email = StringField('Email:', validators=[Required(),Length(1,64),Email()])
    username = StringField('Username:',validators=[Required(),Length(1,64),Regexp('^[A-Za-z][A-Za-z0-9_.]*$',0,'Usernames must have only letters, numbers, dots or underscores')])
    password = PasswordField('Password:',validators=[Required(),EqualTo('password2',message="Passwords must match")])
    password2 = PasswordField("Confirm Password:",validators=[Required()])
    submit = SubmitField('Register User')

    def validate_email(self,field):
        if User.query.filter_by(email=field.data).first():
            raise ValidationError('Email already registered.')

    def validate_username(self,field):
        if User.query.filter_by(username=field.data).first():
            raise ValidationError('Username already taken')

class LoginForm(FlaskForm):
    email = StringField('Email', validators=[Required(), Length(1,64), Email()])
    password = PasswordField('Password', validators=[Required()])
    remember_me = BooleanField('Keep me logged in')
    submit = SubmitField('Log In')
#lines 113-132 from HW4

class BusinessSearchForm(FlaskForm):
    business = StringField('Search by type of business or by business name', validators=[Required()])
    business_location = StringField('What city are you looking in?', validators=[Required()])
    submit = SubmitField('Submit')

class PersonalRatingForm(FlaskForm):
    name_business = StringField('Business name: ', validators=[Required()])
    location_business = StringField('City business is located: ', validators=[Required()])
    rating = RadioField('How many stars do you give this business? ', choices=[('1', '1 star'),('2', '2 stars'),('3', '3 stars'), ('4', '4 stars'), ('5','5 stars')], validators=[Required()])
    submit = SubmitField('Submit')

class ListCreateForm(FlaskForm):
    name = StringField('List Name',validators=[Required()])
    business_picks = SelectMultipleField('Businesses to include')
    submit = SubmitField('Create List')

    def validate_name(self,field):
        form = ListCreateForm()
        invalid = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O', 'P', 'Q', 'R','S','T','U','V','W','X','Y','Z']
        for char in field.data.split():
            if char[0] not in invalid:
                raise ValidationError('Case Sensitive!')
# validation error from Midterm

class UpdateButtonForm(FlaskForm):
    submit = SubmitField('Update')

class UpdateInfoForm(FlaskForm):
    updateList = StringField("Enter new name for your list: ", validators=[Required()])
    submit = SubmitField('Update')

    def validate_updateList(self,field):
        form = ListCreateForm()
        invalid = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O', 'P', 'Q', 'R','S','T','U','V','W','X','Y','Z']
        for char in field.data.split():
            if char[0] not in invalid:
                raise ValidationError('Case Sensitive!')
#validation error from Midterm

class DeleteButtonForm(FlaskForm):
    deleteBusiness = StringField("TYPE 'YES' TO DELETE BUSINESS: ", validators=[Required()])
    submit = SubmitField('Delete')

    def validate_deleteBusiness(self,field):
        form = DeleteButtonForm()
        validator = 'YES'
        for char in field.data.split():
            if char != validator:
                raise ValidationError('Please confirm with YES (case sensitive)!')


def get_businesses(business, location):
    headers = {}
    headers['Authorization'] = 'Bearer {}'.format(key)
    baseurl = "https://api.yelp.com/v3/businesses/search"
    params = {}
    params['term'] = business
    params['location'] = location
    params['limit'] = 10
    params['sort_by'] = "best_match"
    resp = requests.get(baseurl, headers=headers, params=params)
    data = json.loads(resp.text)
    return data['businesses']

def get_businesses_by_id(id):
    b = Business.query.filter_by(id=id).first()
    return b
#lines 198-200 from HW4

def get_or_create_business(db_session, name, url, location):
    business = db_session.query(Business).filter_by(name=name, business_location=location).first()
    if business:
        return business
    else:
        business = Business(name=name, url=url, business_location=location)
        db_session.add(business)
        db_session.commit()
        return business

def get_or_create_search_term(db_session, name, location, business_list=[]):
    search = db_session.query(SearchTerm).filter_by(business_search=name, location_search=location).first()
    if search:
        print("Found term")
        return search
    else:
        print("Added term")
        search = SearchTerm(business_search=name, location_search=location)
        business_list = get_businesses(name, location)
        for b in business_list:
            business = get_or_create_business(db_session, name = b['name'], url = b['url'], location=b['location']['display_address'][0])
            search.businesses.append(business)
        db_session.add(search)
        db_session.commit()
        return search

def get_or_create_list(db_session, title, current_user, business_list):
    biz_list = db_session.query(BusinessList).filter_by(title=title, user_id=current_user.id).first()
    if biz_list:
        return biz_list
    else:
        biz_list = BusinessList(title=title, user_id=current_user.id, businesses=[])
        for b in business_list:
            biz_list.businesses.append(b)
        db_session.add(biz_list)
        db_session.commit()
        return biz_list

@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404

@app.errorhandler(500)
def internal_server_error(e):
    return render_template('500.html'), 500

@app.route('/login',methods=["GET","POST"])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user is not None and user.verify_password(form.password.data):
            login_user(user, form.remember_me.data)
            return redirect(request.args.get('next') or url_for('index'))
        flash('Invalid username or password.')
    return render_template('login.html',form=form)

@app.route('/logout')
@login_required
def logout():
    logout_user()
    flash('You have been logged out')
    return redirect(url_for('index'))

@app.route('/register',methods=["GET","POST"])
def register():
    form = RegistrationForm()
    if form.validate_on_submit():
        user = User(email=form.email.data,username=form.username.data,password=form.password.data)
        db.session.add(user)
        db.session.commit()
        flash('You can now log in!')
        return redirect(url_for('login'))
    return render_template('register.html',form=form)

@app.route('/secret')
@login_required
def secret():
    return "Only authenticated users can do this! Try to log in or contact the site admin."
#lines 249-281 from HW4

@app.route('/', methods=['GET', 'POST'])
def index():
    form = BusinessSearchForm()
    if form.validate_on_submit():
        search_term = get_or_create_search_term(db.session, form.business.data, form.business_location.data)
        return redirect(url_for('search_results', name=form.business.data, location=form.business_location.data))

    return render_template('base.html', form=form)


@app.route('/businesses_searched/<name>/<location>')
def search_results(name, location):
    term = SearchTerm.query.filter_by(business_search=name, location_search=location).first()
    results = term.businesses.all()
    return render_template('searched_businesses.html', businesses=results, business_search=name, location_search=location)

@app.route('/getrating', methods = ['GET', 'POST'])
@login_required
def get_rating():
    form = PersonalRatingForm()
    if request.method == 'GET':
        business = request.args.get('name_business')
        location = request.args.get('location_business')
        rating = request.args.get('rating')

        r = BusinessRating.query.filter_by(businessName=business, businessLocation=location)
        if r: 
            print('rating already exists')
        flash('This business has already been rated')

        b = BusinessRating(businessName=business, businessLocation=location, businessRating=rating)
        db.session.add(b)
        db.session.commit()

        flash('Rating successfully saved!')
    return render_template('get_rating.html', form=form)

@app.route('/all_ratings')
def businesses_and_ratings():
    all_ratings = BusinessRating.query.all()
    return render_template('ratings.html', ratings=all_ratings)

@app.route('/search_terms')
def search_terms():
    all_terms = SearchTerm.query.all()
    return render_template('search_terms.html', all_terms=all_terms)

@app.route('/all_businesses')
def all_businesses():
    businesses = Business.query.all()
    return render_template('all_businesses.html', all_businesses=businesses)

@app.route('/create_business_list',methods=["GET","POST"])
@login_required
def create_list():
    form = ListCreateForm()
    choices = []
    for x in Business.query.all():
        choices.append((x.id, x.name))
    form.business_picks.choices = choices
    if request.method == 'POST':
        businesses_selected = form.business_picks.data
        print("BUSINESSES SELECTED", businesses_selected)
        business_objects = [get_businesses_by_id(int(id)) for id in businesses_selected]
        print("BUSINESSES RETURNED", business_objects)
        get_or_create_list(db.session, current_user=current_user,title=form.name.data, business_list=business_objects)
        return redirect(url_for('lists'))

    else:    
        errors = [v for v in form.errors.values()]
        if len(errors) > 0:
            flash(str(errors))
    return render_template('create_business_list.html', form=form)

@app.route('/lists',methods=["GET","POST"])
@login_required
def lists():
    form1 = UpdateButtonForm()
    form2 = DeleteButtonForm()
    all_lists = []
    lists = BusinessList.query.filter_by(user_id=current_user.id).all()
    for l in lists:
        all_lists.append(l.title)
    print(lists)
    return render_template('lists.html', lists=lists, form1=form1, form2=form2)

@app.route('/list/<id_num>')
def single_list(id_num):
    form = DeleteButtonForm()
    id_num = int(id_num)
    business_items = []
    L = BusinessList.query.filter_by(id=id_num).first()
    print(L)
    businesses = L.businesses.all()
    for b in businesses:
        business_items.append(b.name)
    print(businesses)
    return render_template('list.html', L=L, businesses=businesses, form=form)
#lines 326-381 modeled after HW4

@app.route('/update/<lst>', methods=["GET", "POST"])
def update(lst):
    form = UpdateInfoForm()
    if form.validate_on_submit():
        list_update = form.updateList.data
        b = BusinessList.query.filter_by(title=lst).first()
        b.title = list_update
        db.session.commit()
        flash("LIST UPDATED")
    return render_template('update_business.html', lst_title=lst, form=form)

@app.route('/delete_business/<business>', methods=["GET", "POST"])
def delete_business(business):
    print('hello')
    form = DeleteButtonForm()
    if form.validate_on_submit():
        delete = form.deleteBusiness.data
        d = Business.query.filter_by(name=business).first()
        db.session.delete(d)
        db.session.commit()
        flash(business + " successfully deleted.")
    else:
        
        errors = [v for v in form.errors.values()]
        if len(errors) > 0:
            flash(str(errors))
    return render_template('delete_business.html', business_name=business, form=form)

@app.route('/delete/<lst>', methods=["GET", "POST"])
def delete(lst):
    form = DeleteButtonForm()
    if form.validate_on_submit():
        delete = form.deleteBusiness.data
        d = BusinessList.query.filter_by(title=lst).first()
        db.session.delete(d)
        db.session.commit()
        flash(lst + " successfully deleted.")
    else:   
        errors = [v for v in form.errors.values()]
        if len(errors) > 0:
            flash(str(errors))
    return render_template('delete_list.html', lst_title=lst, form=form)
#lines 384-425 modeled after HW5

@app.route('/ajax')
def great_search():
    x = jsonify({"ann_arbor" : [{'name' : business['name']} for business in get_businesses("Restaurants", "Ann Arbor, MI")]})
    return x
#lines 428-431 modeled after Lecture12 example

if __name__ == '__main__':
    db.create_all()
    manager.run()
