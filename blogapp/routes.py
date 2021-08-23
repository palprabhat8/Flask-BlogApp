from flask import render_template, redirect, url_for, flash, request
from passlib.hash import sha256_crypt
from blogapp import app, db
from blogapp.models import User, Post
from blogapp.forms import RegistrationForm, LoginForm, PostForm
from flask_login import login_user, current_user, logout_user, login_required


@app.route('/')
@app.route('/home')
def home():
    return render_template("home.html")


@app.route('/blogs')
def blogs():
	blogs_list = Post.query.all()
	return render_template("blogs.html", blogs_list=blogs_list)

@app.route("/blog/new", methods=['GET', 'POST'])
@login_required
def new_blog():
    form = PostForm()
    if form.validate_on_submit():
        post = Post(title=form.title.data, text=form.text.data, author=current_user)
        db.session.add(post)
        db.session.commit()
        flash('Your post has been created!', category='success')
        return redirect(url_for('blogs'))
    return render_template('create_blog.html', form=form)


@app.route('/blog/<int:id>')
def blog(id):
	post = Post.query.filter_by(id=id).first()
	return render_template("blog.html", post=post)


@app.route('/register', methods=['GET', 'POST'])
def register():
    form = RegistrationForm()
    if form.validate_on_submit():
        hashed_password = sha256_crypt.encrypt(str(form.password.data))
        user = User(username=form.username.data,
                    email=form.email.data, password=hashed_password)
        db.session.add(user)
        db.session.commit()
        flash(f'Your account has been created succesfully! You can Login now!',
              category="success")
        return redirect(url_for('login'))

    return render_template("register.html", form=form)


@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm(request.form)
    if form.validate_on_submit():
        password_input = request.form['password']
        user = User.query.filter_by(email=form.email.data).first()
        if user and sha256_crypt.verify(password_input, user.password):
        	login_user(user)
        	return redirect(url_for('home'))
        else:
        	flash('Login Unsuccessful. Please check email and password',category='danger')

    return render_template("login.html", form=form)


@app.route("/logout")
def logout():
    logout_user()
    return redirect(url_for('home'))
