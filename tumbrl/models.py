# Aqui vai a estrutura do nosso banco de dados (classes e tals)
from tumbrl import database
from datetime import datetime
from tumbrl import login_manager
from flask_login import UserMixin
from flask_wtf import FlaskForm
from wtforms import SubmitField, HiddenField
from datetime import datetime
from sqlalchemy.orm import relationship


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


class User(database.Model, UserMixin):
    id = database.Column(database.Integer, primary_key=True)
    username = database.Column(database.String, nullable=False, unique=True)
    email = database.Column(database.String, nullable=False, unique=True)
    password = database.Column(database.String, nullable=False)
    posts = database.Relationship("Posts", backref='user', lazy=True)


class Posts(database.Model):
    id = database.Column(database.Integer, primary_key=True)
    post_text = database.Column(database.String, default='')
    post_img = database.Column(database.String, default='default.png')

    # adição dos atributos para a adição de comentários e likes
    comments = database.relationship("Comment", backref="post", lazy="dynamic")
    likes = database.relationship("Like", backref="post", lazy="dynamic")

    creation_date = database.Column(database.DateTime, nullable=False, default=datetime.utcnow())
    user_id = database.Column(database.Integer, database.ForeignKey('user.id'), nullable=False)


# classe para adicionar os comentários no banco de dados
class Comment(database.Model):
    id = database.Column(database.Integer, primary_key=True)
    text = database.Column(database.String, nullable=False)
    user_id = database.Column(database.Integer, database.ForeignKey('user.id'), nullable=False)  # chave estrangeira para o usuário que fez o comentário
    post_id = database.Column(database.Integer, database.ForeignKey('posts.id'), nullable=False)  # chave estrangeira para o post associado ao comentário
    timestamp = database.Column(database.DateTime, default=datetime.utcnow)


# classe para adicionar os likes no banco de dados
class Like(database.Model):
    id = database.Column(database.Integer, primary_key=True)
    user_id = database.Column(database.Integer, database.ForeignKey('user.id'), nullable=False)  # chave estrangeira para o usuário que deu o like
    post_id = database.Column(database.Integer, database.ForeignKey('posts.id'), nullable=False)  # chave estrangeira para a postagem associada ao like

