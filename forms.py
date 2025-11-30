from flask_wtf import FlaskForm
from wtforms import StringField, SelectField, TextAreaField, BooleanField, FileField, SubmitField
from wtforms.validators import DataRequired, Email, Length

class AstronautSelectionForm(FlaskForm):
    surname = StringField('Фамилия', validators=[DataRequired(), Length(min=2, max=50)])
    name = StringField('Имя', validators=[DataRequired(), Length(min=2, max=50)])
    email = StringField('Email', validators=[DataRequired(), Email()])
    education = SelectField('Образование', choices=[
        ('secondary', 'Среднее'),
        ('specialized_secondary', 'Среднее специальное'),
        ('higher', 'Высшее')
    ], validators=[DataRequired()])
    profession = SelectField('Профессия', choices=[
        ('engineer_researcher', 'инженер-исследователь'),
        ('pilot', 'пилот'),
        ('builder', 'строитель'),
        ('exobiologist', 'экзобиолог'),
        ('doctor', 'врач'),
        ('terraform_engineer', 'инженер по терраформированию'),
        ('climatologist', 'климатолог'),
        ('radiation_specialist', 'специалист по радиационной защите'),
        ('astrogeologist', 'астрогеолог'),
        ('glaciologist', 'гляциолог'),
        ('life_support_engineer', 'инженер жизнеобеспечения'),
        ('meteorologist', 'метеоролог'),
        ('rover_operator', 'оператор марсохода'),
        ('cyber_engineer', 'киберинженер'),
        ('navigator', 'штурман'),
        ('drone_pilot', 'пилот дронов')
    ], validators=[DataRequired()])
    gender = SelectField('Пол', choices=[('male', 'Мужской'), ('female', 'Женский')], validators=[DataRequired()])
    motivation = TextAreaField('Мотивация', validators=[DataRequired(), Length(min=10)])
    ready = BooleanField('Готовы ли остаться на Марсе?')
    photo = FileField('Фото')
    submit = SubmitField('Отправить')