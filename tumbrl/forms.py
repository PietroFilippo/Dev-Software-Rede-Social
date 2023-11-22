# Aqui vão estar os formulários do nosso site

from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, FileField
from wtforms.validators import DataRequired, Email, EqualTo, Length, ValidationError

from tumbrl.models import User
from wtforms.widgets import TextArea
from flask_wtf import FlaskForm
from wtforms import HiddenField, SubmitField


class FormLogin(FlaskForm):
    email = StringField('Email')
    password = PasswordField('Password')
    btn = SubmitField('Login')


class FormCreateNewAccount(FlaskForm):
    email = StringField('Email', validators=[DataRequired(), Email()])
    usarname = StringField('Username', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired(), Length(6, 25)])
    checkPassword = PasswordField('Check Password', validators=[DataRequired(), Length(6, 25), EqualTo('password')])
    btn = SubmitField('Create Account')

    def validate_email(self, email):
        email_of_user = User.query.filter_by(email=email.data).first()
        if email_of_user:
            return ValidationError('~ email já existe ~')


class FormCreateNewPost(FlaskForm):
    text = StringField('PostText', widget=TextArea(), validators=[DataRequired()])
    photo = FileField('Photo', validators=[DataRequired()])
    btn = SubmitField('Publish')


# formulário fazer um comentário em um post na timeline
class FormAddComment(FlaskForm):
    comment_text = StringField('Comment', validators=[DataRequired()])
    submit_comment = SubmitField('Comment')


# formulário para fazer um comentário em um post no perfil do usuario
class FormAddCommentProfile(FlaskForm):
    comment_text = StringField('Comment', validators=[DataRequired()])
    submit_comment = SubmitField('Comment')


# formulário para fazer um like em um post na timeline
class FormAddLike(FlaskForm):
    submit_like = SubmitField('Like')


# formulário para fazer um like em um post no perfil do usuário
class FormAddLikeProfile(FlaskForm):
    submit_like = SubmitField('Like')


