from flask_wtf import FlaskForm
from wtforms import BooleanField, StringField, PasswordField, SubmitField,DateField, SelectField
from wtforms.validators import DataRequired, Email, Length, EqualTo

class LoginForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    remember = BooleanField('Remember Me')
    submit = SubmitField('Login')

class RegistrationForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired(), Length(min=2, max=20)])
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired(), Length(min=6)])
    confirm_password = PasswordField('Confirm Password', validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Sign Up')

class ParcelForm(FlaskForm):
    sender = StringField('Sender', validators=[DataRequired()])
    parcel_name = StringField('Parcel Name', validators=[DataRequired()])
    recipient = StringField('Recipient', validators=[DataRequired()])
    status = SelectField('Status', choices=[('Pending', 'Pending'), ('In Transit', 'In Transit'), ('Delivered', 'Delivered')], validators=[DataRequired()])
    estimated_date = DateField('Estimated Date', format='%Y-%m-%d', validators=[DataRequired()])
    location = StringField('Location', validators=[DataRequired()])
    submit = SubmitField('Add Parcel')

class UpdateParcelForm(FlaskForm):
    status = SelectField(
        'Status',
        choices=[
            ('Pending', 'Pending'),
            ('Received', 'Received'),
            ('In Transit', 'In Transit'),
            ('Delivered', 'Delivered')
        ],
        validators=[DataRequired()]
    )
    estimated_date = StringField('Estimated Date')   
    location = StringField('Location')
    submit = SubmitField('Update Parcel')