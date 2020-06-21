from myflask import app, db
from datetime import datetime
from flask import Flask , render_template, url_for, flash, request, redirect
from myflask.forms import ValidateContact,LoginForm,PostForm
from myflask.models import Post, User
from flask_login import login_user, current_user ,logout_user,login_required


import os
import smtplib
from email.message import EmailMessage



@app.route("/")
@app.route("/home")
def home_page():
    posts = Post.query.order_by(Post.date_posted.desc())[0:2]
    return render_template('home.html', posts=posts)

@app.route('/about')
def about_page():
    return render_template('about.html',title='About')

@app.route('/Articles')
def articles_page():
    page = request.args.get('page', 1, type=int)
    posts = Post.query.order_by(Post.date_posted.desc()).paginate(page=page)
    return render_template('articles.html', posts=posts)

@app.route('/Contact',methods=['GET','POST'])
def contact_page():
    form = ValidateContact()
    if form.validate_on_submit():
        flash('Message succesfully send !','success')
        message = request.form
        
        name = message['firstname']+' '+message['lastname']
        email = message['youremail']
        mes = message['yourmessage']
        
        with smtplib.SMTP_SSL('smtp.gmail.com', port=465) as smtp:

            smtp.login(EMAIL_ADRESS,EMAIL_PASSWORD)

            msg = EmailMessage()
            msg['From'] = email
            msg['To'] = EMAIL_ADRESS
            msg['Subject'] = 'Mail from your blog'
            msg.set_content(f'Message from {name}\n{mes}')


            smtp.send_message(msg)
            
        return redirect(url_for("home_page"))

    return render_template('contact.html',title='Contact',form=form)

@app.route("/login", methods=['GET', 'POST'])
def login_page():
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.all()[0]
        if form.email.data == user.email and form.password.data == user.password:
            login_user(user)
            flash('Welcome admin!','success')
            return redirect(url_for('home_page'))
        else:
            flash('Admin only!', 'danger')
    return render_template('login.html', title='Login', form=form)

@app.route("/logout")
@login_required
def logout():
    logout_user()
    return redirect(url_for('home_page'))

@app.route("/post", methods=['GET', 'POST'])
@login_required
def new_post():
    form = PostForm()
    if form.validate_on_submit():
        post = Post(title = form.title.data , content = form.content.data ,author = current_user)
        db.session.add(post)
        db.session.commit()
        flash("Your post thas been created!" , 'success')
        return redirect(url_for('home_page'))
    return render_template('post_create.html', title='New Post', 
                           form = form, legend = 'New Post')

@app.route("/post/<int:post_id>")
def post(post_id):
    post = Post.query.get_or_404(post_id)
    return render_template("post.html", title = post.title , post = post)


@app.route("/user/<string:username>")
def user_posts(username):
    page = request.args.get('page', 1, type=int)
    user = User.query.filter_by(username=username).first_or_404()
    posts = Post.query.filter_by(author=user)\
        .order_by(Post.date_posted.desc())\
        .paginate(page=page, per_page=5)
    return render_template('user_posts.html', posts=posts, user=user)



