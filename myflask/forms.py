from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, TextAreaField,PasswordField,BooleanField
from wtforms.validators import DataRequired, Length, Email

class ValidateContact(FlaskForm):
    firstname= StringField('First Name',validators=[DataRequired(),Length(min=2,max=20)])
    lastname= StringField('Last Name',validators=[DataRequired(),Length(min=2,max=20)])
    youremail = StringField("Your Email",validators=[DataRequired(),Email()])

    yourmessage = TextAreaField('Your message for me',validators=[DataRequired(),Length(min=10,max=200)])

    submit = SubmitField("Send message")   

class LoginForm(FlaskForm):

    email = StringField("Email",validators=[DataRequired(),Email()])

    password = PasswordField("Password",validators=[DataRequired()])

    remember = BooleanField("Remember Me")

    submit = SubmitField("Login")  

class PostForm(FlaskForm):
    title = StringField("Title", validators = [DataRequired()])
    content = TextAreaField("Content" , validators=[DataRequired()])

    submit = SubmitField("Post")