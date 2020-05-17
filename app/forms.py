from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField, TextAreaField, \
    SelectField, FileField
from wtforms.ext.sqlalchemy.fields import QuerySelectField
from wtforms.validators import DataRequired, Length, ValidationError
from app.models import User, Substance
from config import Confpath


class LoginForm(FlaskForm):
    username = StringField('Логин', validators=[DataRequired()])
    password = PasswordField('Пароль', validators=[DataRequired()])
    remember_me = BooleanField('Запомнить меня', default=True)
    submit = SubmitField('Войти')


class EditProfileForm(FlaskForm):
    username = StringField('Логин', validators=[DataRequired()])
    notes = TextAreaField('Заметки', validators=[Length(min=0, max=140)])
    submit = SubmitField('Сохранить')

    def __init__(self, orginal_username, *args, **kwargs):
        super(EditProfileForm, self).__init__(*args, **kwargs)
        self.original_username = orginal_username

    def validate_username(self, username):
        if username.data != self.original_username:
            user = User.query.filter_by(username=self.username.data).first_or_404()
            if user is not None:
                raise ValidationError('Данное имя уже есть в базе')


class RegistrationForm(FlaskForm):
    title = StringField('Название:', validators=[DataRequired()])
    fiz = SelectField('Агрегатное состояние', choices=[
        ("", ""),
        ("жидкий", "жидкий"),
        ("твердый", "твёрдый"),
        ("газообразный", "газообразный"),
        ("газ/жидкость", "газ/жидкость"),
    ], validators=[DataRequired()])
    fiz2 = SelectField('Горючесть', choices=[
        ("", ""),
        ("да", "да"),
        ("нет", "нет")
    ], validators=[DataRequired()])
    put = SelectField('Ингаляционный', choices=[
        ("", ""),
        ("да", "да"),
        ("нет", "нет")
    ], validators=[DataRequired()])
    put2 = SelectField('Резорбтивный', choices=[
        ("", ""),
        ("да", "да"),
        ("нет", "нет")
    ], validators=[DataRequired()])
    put3 = SelectField('Артериально-венозный', choices=[
        ("", ""),
        ("да", "да"),
        ("нет", "нет")
    ], validators=[DataRequired()])
    put4 = SelectField('Пероральный', choices=[
        ("", ""),
        ("да", "да"),
        ("нет", "нет")
    ], validators=[DataRequired()])
    kli = SelectField('Смертельный исход', choices=[
        ("", ""),
        ("да", "да"),
        ("нет", "нет")
    ], validators=[DataRequired()])
    kli2 = SelectField('Раздражение слизистых глаз', choices=[
        ("", ""),
        ("да", "да"),
        ("нет", "нет")
    ], validators=[DataRequired()])
    kli3 = SelectField('Затруднение дыхания', choices=[
        ("", ""),
        ("да", "да"),
        ("нет", "нет")
    ], validators=[DataRequired()])
    kli4 = SelectField('Судороги', choices=[
        ("", ""),
        ("да", "да"),
        ("нет", "нет")
    ], validators=[DataRequired()])
    kli5 = SelectField('Кашель', choices=[
        ("", ""),
        ("да", "да"),
        ("нет", "нет")
    ], validators=[DataRequired()])
    kli6 = SelectField('Головокружение', choices=[
        ("", ""),
        ("да", "да"),
        ("нет", "нет")
    ], validators=[DataRequired()])
    kli7 = SelectField('Тошнота', choices=[
        ("", ""),
        ("да", "да"),
        ("нет", "нет")
    ], validators=[DataRequired()])
    kli8 = SelectField('Нарушение вестибулярного аппарата', choices=[
        ("", ""),
        ("да", "да"),
        ("нет", "нет")
    ], validators=[DataRequired()])
    kli9 = SelectField('Понос', choices=[
        ("", ""),
        ("да", "да"),
        ("нет", "нет")
    ], validators=[DataRequired()])
    kli10 = SelectField('Окраска кожи', choices=[
        ("", ""),
        ("да", "да"),
        ("нет", "нет")
    ], validators=[DataRequired()])
    filename = FileField('Карточка вещества(.pdf)',
                     validators=[DataRequired()])
    submit = SubmitField('Добавить')

    def validate_username(self, substance):
        substance = User.query.filter_by(username=substance.data).first()
        if substance is not None:
            raise ValidationError('Данное вещество уже есть в таблице')

    def allowed_file(filename):
        return '.' in filename and filename.rsplit('.', 1)[1] in Confpath.ALLOWED_EXTENSIONS


def query1():
    return Substance.query


class DeleteForm(FlaskForm):
    title = QuerySelectField('Название вещества', query_factory=query1, allow_blank=False, get_label='title')
    submit = SubmitField('Удалить')


class DeleteSelectForm(FlaskForm):
    submit = SubmitField('Удалить')


class FilterForm(FlaskForm):
    fiz = SelectField('Агрегатное состояние', choices=[
        ("", "<неизвестно>"),
        ("жидкий", "жидкий"),
        ("твердый", "твёрдый"),
        ("газообразный", "газообразный"),
        ("газ/жидкость", "газ/жидкость"),
    ])
    fiz2 = SelectField('Горючесть', choices=[
        ('', "<неизвестно>"),
        ("да", "да"),
        ("нет", "нет")
    ])
    put = SelectField('Ингаляционный', choices=[
        ('', "<неизвестно>"),
        ("да", "да"),
        ("нет", "нет")
    ])
    put2 = SelectField('Резорбтивный', choices=[
        ('', "<неизвестно>"),
        ("да", "да"),
        ("нет", "нет")
    ])
    put3 = SelectField('Артериально-венозный', choices=[
        ('', "<неизвестно>"),
        ("да", "да"),
        ("нет", "нет")
    ])
    put4 = SelectField('Пероральный', choices=[
        ('', "<неизвестно>"),
        ("да", "да"),
        ("нет", "нет")
    ])
    kli = SelectField('Смертельный исход', choices=[
        ('', "<неизвестно>"),
        ("да", "да"),
        ("нет", "нет")
    ])
    kli2 = SelectField('Раздражение слизистых глаз', choices=[
        ('', "<неизвестно>"),
        ("да", "да"),
        ("нет", "нет")
    ])
    kli3 = SelectField('Затруднение дыхания', choices=[
        ('', "<неизвестно>"),
        ("да", "да"),
        ("нет", "нет")
    ])
    kli4 = SelectField('Судороги', choices=[
        ('', "<неизвестно>"),
        ("да", "да"),
        ("нет", "нет")
    ])
    kli5 = SelectField('Кашель', choices=[
        ('', "<неизвестно>"),
        ("да", "да"),
        ("нет", "нет")
    ])
    kli6 = SelectField('Головокружение', choices=[
        ('', "<неизвестно>"),
        ("да", "да"),
        ("нет", "нет")
    ])
    kli7 = SelectField('Тошнота', choices=[
        ('', "<неизвестно>"),
        ("да", "да"),
        ("нет", "нет")
    ])
    kli8 = SelectField('Нарушение вестибулярного аппарата', choices=[
        ('', "<неизвестно>"),
        ("да", "да"),
        ("нет", "нет")
    ])
    kli9 = SelectField('Понос', choices=[
        ('', "<неизвестно>"),
        ("да", "да"),
        ("нет", "нет")
    ])
    kli10 = SelectField('Окраска кожи', choices=[
        ('', "<неизвестно>"),
        ("да", "да"),
        ("нет", "нет")
    ])
    submit = SubmitField('Поиск')


class EditSubstanceForm(FlaskForm):
    newtitle = StringField('Новое название:', validators=[DataRequired()])
    fiz = SelectField('Агрегатное состояние', choices=[
        ("жидкий", "жидкий"),
        ("твердый", "твёрдый"),
        ("газообразный", "газообразный"),
        ("газ/жидкость", "газ/жидкость"),
    ])
    fiz2 = SelectField('Горючесть', choices=[
        ("да", "да"),
        ("нет", "нет")
    ])
    put = SelectField('Ингаляционный', choices=[
        ("да", "да"),
        ("нет", "нет")
    ])
    put2 = SelectField('Резорбтивный', choices=[
        ("да", "да"),
        ("нет", "нет")
    ])
    put3 = SelectField('Артериально-венозный', choices=[
        ("да", "да"),
        ("нет", "нет")
    ])
    put4 = SelectField('Пероральный', choices=[
        ("да", "да"),
        ("нет", "нет")
    ])
    kli = SelectField('Смертельный исход', choices=[
        ("да", "да"),
        ("нет", "нет")
    ])
    kli2 = SelectField('Раздражение слизистых глаз', choices=[
        ("да", "да"),
        ("нет", "нет")
    ])
    kli3 = SelectField('Затруднение дыхания', choices=[
        ("да", "да"),
        ("нет", "нет")
    ])
    kli4 = SelectField('Судороги', choices=[
        ("да", "да"),
        ("нет", "нет")
    ])
    kli5 = SelectField('Кашель', choices=[
        ("да", "да"),
        ("нет", "нет")
    ])
    kli6 = SelectField('Головокружение', choices=[
        ("да", "да"),
        ("нет", "нет")
    ])
    kli7 = SelectField('Тошнота', choices=[
        ("да", "да"),
        ("нет", "нет")
    ])
    kli8 = SelectField('Нарушение вестибулярного аппарата', choices=[
        ("да", "да"),
        ("нет", "нет")
    ])
    kli9 = SelectField('Понос', choices=[
        ("да", "да"),
        ("нет", "нет")
    ])
    kli10 = SelectField('Окраска кожи', choices=[
        ("да", "да"),
        ("нет", "нет")
    ])
    submit = SubmitField('Применить')


class AddCardForm(FlaskForm):
    title = QuerySelectField('Название вещества', query_factory=query1, allow_blank=False, get_label='title')
    filename = FileField('Карточка вещества(.pdf)',
                         validators=[DataRequired()])
    submit = SubmitField('Сохранить')
