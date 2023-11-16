# Aqui vão as rotas e os links
from tumbrl import app
from flask import render_template, url_for, redirect
from flask_login import login_required, login_user, current_user
from tumbrl.models import load_user
from tumbrl.forms import FormLogin, FormCreateNewAccount, FormCreateNewPost
from tumbrl.forms import FormAddLike, FormAddComment, FormAddCommentProfile, FormAddLikeProfile
from tumbrl import bcrypt
from tumbrl.models import User, Posts
from tumbrl.models import Comment, Like
from tumbrl import database
from flask import Flask, render_template, redirect, request, url_for


import os
from werkzeug.utils import secure_filename


# @app.route('/home')
@app.route('/', methods=['POST', 'GET'])
def homepage():
    _formLogin = FormLogin()
    if _formLogin.validate_on_submit():
        userToLogin = User.query.filter_by(email=_formLogin.email.data).first()
        if userToLogin and bcrypt.check_password_hash(userToLogin.password, _formLogin.password.data):
            login_user(userToLogin)
            return redirect(url_for("profile", user_id=userToLogin.id))

    return render_template('home.html', form=_formLogin)


@app.route('/new', methods=['POST', 'GET'])
def createAccount():
    _formCreateNewAccount = FormCreateNewAccount()

    if _formCreateNewAccount.validate_on_submit():
        password = _formCreateNewAccount.password.data
        password_cr = bcrypt.generate_password_hash(password)
        # print(password)
        # print(password_cr)

        newUser = User(
            username=_formCreateNewAccount.usarname.data,
            email=_formCreateNewAccount.email.data,
            password=password_cr
        )

        database.session.add(newUser)
        database.session.commit()

        login_user(newUser, remember=True)
        return redirect(url_for('profile', user_id=newUser.id))

    return render_template('new.html', form=_formCreateNewAccount)


@app.route('/perry')
def perry():
    return render_template('perry.html')


@app.route('/teste')
def teste():
    return render_template('teste.html')


@app.route('/profile/<user_id>', methods=['POST', 'GET'])
@login_required
def profile(user_id):
    form_add_comment_profile = FormAddCommentProfile()
    form_add_like_profile = FormAddLikeProfile()

    if int(user_id) == int(current_user.id):
        _formCreateNewPost = FormCreateNewPost()

        if _formCreateNewPost.validate_on_submit():
            photo_file = _formCreateNewPost.photo.data
            photo_name = secure_filename(photo_file.filename)

            photo_path = f'{os.path.abspath(os.path.dirname(__file__))}/{app.config["UPLOAD_FOLDER"]}/{photo_name}'
            photo_file.save(photo_path)

            _postText = _formCreateNewPost.text.data

            newPost = Posts(post_text=_postText, post_img=photo_name, user_id=int(current_user.id))
            database.session.add(newPost)
            database.session.commit()

        return render_template('profile.html', user=current_user, form=_formCreateNewPost,
                               form_add_comment_profile=form_add_comment_profile, form_add_like_profile=form_add_like_profile)

    else:
        _user = User.query.get(int(user_id))
        pass

        return render_template('profile.html', user=_user, form=None,
                               form_add_comment_profile=form_add_comment_profile, form_add_like_profile=form_add_like_profile)



@app.route('/timeline')
def timeline():
    timeline = Posts.query.all()
    form_add_comment = FormAddComment()
    form_add_like = FormAddLike()
    return render_template('timeline.html', all_posts=timeline, form_add_comment=form_add_comment, form_add_like=form_add_like)


@app.route('/add_comment/<post_id>', methods=['POST'])
@login_required
def add_comment(post_id):
    post = Posts.query.get(post_id)
    if post:
            comment_text = request.form.get('comment_text')
            new_comment = Comment(text=comment_text, user_id=current_user.id, post_id=post.id)
            database.session.add(new_comment)
            database.session.commit()

    return redirect(request.referrer or url_for('timeline'))


@app.route('/add_like/<post_id>', methods=['POST'])
@login_required
def add_like(post_id):
    post = Posts.query.get(post_id)

    if post:
        existing_like = Like.query.filter_by(user_id=current_user.id, post_id=post.id).first()
        if not existing_like:
            new_like = Like(user_id=current_user.id, post_id=post.id)
            database.session.add(new_like)
            database.session.commit()

    return redirect(request.referrer or url_for('timeline'))


