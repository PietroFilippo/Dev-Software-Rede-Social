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
                               # renderiza o perfil do adicionando os comentários e curtidas nos posts
                               form_add_comment_profile=form_add_comment_profile,
                               form_add_like_profile=form_add_like_profile)


# route para exibir a timeline com os posts
@app.route('/timeline')
def timeline():
    # pega todos os posts do banco de dados
    timeline = Posts.query.all()
    # atribui aos formulários a opção para adicionar comentários e likes nos posts na timeline
    form_add_comment = FormAddComment()
    form_add_like = FormAddLike()

    # renderiza a página da tieline com todos os posts
    return render_template('timeline.html', all_posts=timeline, form_add_comment=form_add_comment,
                           form_add_like=form_add_like)


# route para fazer um comentário a um post
@app.route('/add_comment/<post_id>', methods=['POST'])
@login_required
def add_comment(post_id):
    # pega o post com o id
    post = Posts.query.get(post_id)

    if post:
        # pega o texto do comentário do formulário
        comment_text = request.form.get('comment_text')
        # cria um novo objeto de comentário no banco de dados
        new_comment = Comment(text=comment_text, user_id=current_user.id, post_id=post.id)
        database.session.add(new_comment)
        database.session.commit()

    # redireciona de volta  ao perfil ou pra timeline
    return redirect(request.referrer or url_for('timeline'))


# route para adicionar um like a um post
@app.route('/add_like/<post_id>', methods=['POST'])
@login_required
def add_like(post_id):
    # pega o post com o id
    post = Posts.query.get(post_id)

    if post:
        # verifica se o usuário já deu like no post
        existing_like = Like.query.filter_by(user_id=current_user.id, post_id=post.id).first()
        if not existing_like:
            # caso não cria um novo objeto de like no banco de dados
            new_like = Like(user_id=current_user.id, post_id=post.id)
            database.session.add(new_like)
            database.session.commit()

    # redireciona de volta ao perfil ou pra timeline
    return redirect(request.referrer or url_for('timeline'))


