from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileAllowed
from flask_login import current_user
from wtforms import StringField, PasswordField, SubmitField, BooleanField, TextAreaField
from wtforms.validators import DataRequired, Length, Email, EqualTo, ValidationError
from flaskapp.models import User

class RegistrationForm(FlaskForm):
  username = StringField('Käyttäjänimi', validators=[DataRequired(), Length(min=2, max=20)])
  email = StringField('Sähköposti', validators=[DataRequired(), Email()])
  password = PasswordField('Salasana', validators=[DataRequired()])
  confirm_password = PasswordField('Vahvista salasana', validators=[DataRequired(), EqualTo('password')])
  submit = SubmitField('Rekisteröidy')

  def validate_username(self, username):
    user = User.query.filter_by(username=username.data).first()
    if user:
      raise ValidationError('Antamasi käyttäjätunnus on varattu. Valitse toinen käyttäjänimi.')
  
  def validate_email(self, email):
    user = User.query.filter_by(email=email.data).first()
    if user:
      raise ValidationError('Antamasi sähköposti on jo olemassa. Valitse toinen sähköposti.')

class LoginForm(FlaskForm):
  email = StringField('Sähköposti', validators=[DataRequired(), Email()])
  password = PasswordField('Salasana', validators=[DataRequired()])
  remember = BooleanField('Muista minut')
  submit = SubmitField('Kirjaudu')

class UpdateAccountForm(FlaskForm):
  username = StringField('Käyttäjänimi', validators=[DataRequired(), Length(min=2, max=20)])
  email = StringField('Sähköposti', validators=[DataRequired(), Email()])
  picture = FileField('Päivitä profiilikuvasi', validators=[FileAllowed(['jpg', 'png'])])
  submit = SubmitField('Päivitä')

  def validate_username(self, username):
    if username.data != current_user.username:
      user = User.query.filter_by(username=username.data).first()
      if user:
        raise ValidationError('Antamasi käyttäjätunnus on varattu. Valitse toinen käyttäjänimi.')
  
  def validate_email(self, email):
    if email.data != current_user.email:
      user = User.query.filter_by(email=email.data).first()
      if user:
        raise ValidationError('Antamasi sähköposti on jo olemassa. Valitse toinen sähköposti.')


class PostForm(FlaskForm):
  title = StringField('Otsikko', validators=[DataRequired()])
  content = TextAreaField('Sisältö', validators=[DataRequired()])
  submit = SubmitField('Kirjoitus')