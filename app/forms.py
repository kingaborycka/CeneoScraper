from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, PasswordField
from wtforms.validators import DataRequired, Length, Regexp, EqualTo
from app import users


class ProductForm(FlaskForm):
    
    product_code = StringField(
        'Podaj kod produktu',
        validators = [
            DataRequired(message = 'Musisz podać kod produktu'),
            Length(min=8,max=8,message='Kod produktu składa się z 8 znaków'),
            Regexp(regex='^[0-9]+$',message='Kod produktu może zawierać tylko cyfry')
        ]
    )
    submit = SubmitField('Pobierz opinie')

class LoginForm(FlaskForm):
    username = StringField(
        'Podaj nazwę użytkownika',
        validators = [
            DataRequired(message = 'Musisz podać nazwę użytkownika'),
        ]
    )
    password = PasswordField(
        "Hasło",
        validators = [
                DataRequired(message = 'Podaj hasło'),
            ]
    )
    error = False
    submit = SubmitField('Zaloguj się')
    
class AccountForm(FlaskForm):
    username = StringField('Podaj nazwę użytkownika',
        validators = [
            DataRequired(message = 'Musisz podać nazwę użytkownika'),
        ]
    )

    password = PasswordField('Podaj hasło',
        validators = [
            DataRequired(message = 'Podaj hasło')
        ]
    )

    password2 = PasswordField('Powtórz hasło',
        validators = [
            DataRequired(message = 'Powtórz hasło'),
            EqualTo('password',message='Hasła nie są takie same.')
        ]
    )
    error = False
    submit = SubmitField('Utwórz konto')

            
