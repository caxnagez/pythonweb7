from flask import Flask, render_template, request, redirect, url_for, flash, send_from_directory
from flask_wtf import FlaskForm
from wtforms import StringField, EmailField, SelectField, TextAreaField, BooleanField, FileField, RadioField
from wtforms.validators import DataRequired, Email
import json
import os
import random
from werkzeug.utils import secure_filename

app = Flask(__name__)
app.config['SECRET_KEY'] = 'mars-mission-secret-key'
app.config['UPLOAD_FOLDER'] = 'static/uploads'
os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)

CREW_FILE = 'members/crew.json'

app.jinja_env.filters['random'] = random.choice

def load_crew_data():
    try:
        with open(CREW_FILE, 'r', encoding='utf-8') as f:
            data = json.load(f)
            if not isinstance(data, list):
                print("Ошибка: JSON должен быть массивом.")
                return []
            print(f"Загружено {len(data)} членов экипажа")
            for i, member in enumerate(data[:2], 1):
                print(f"  {i}. {member.get('name')} {member.get('surname')} — фото: {member.get('photo')}")
            return data
    except FileNotFoundError:
        print(f"Файл {CREW_FILE} не найден.")
        return []
    except json.JSONDecodeError as e:
        print(f"Ошибка формата JSON в файле {CREW_FILE}: {e}")
        return []

class AstronautForm(FlaskForm):
    surname = StringField('Фамилия', validators=[DataRequired()])
    name = StringField('Имя', validators=[DataRequired()])
    email = EmailField('Email', validators=[DataRequired(), Email()])
    education = SelectField('Образование', choices=[
        ('начальное', 'Начальное'),
        ('среднее', 'Среднее'),
        ('высшее', 'Высшее'),
        ('учёная степень', 'Учёная степень')
    ], validators=[DataRequired()])
    profession = SelectField('Основная профессия', choices=[
        ('инженер-исследователь', 'Инженер-исследователь'),
        ('пилот', 'Пилот'),
        ('строитель', 'Строитель'),
        ('экзобиолог', 'Экзобиолог'),
        ('врач', 'Врач'),
        ('инженер по терраформированию', 'Инженер по терраформированию'),
        ('климатолог', 'Климатолог'),
        ('специалист по радиационной защите', 'Специалист по радиационной защите'),
        ('астрогеолог', 'Астрогеолог'),
        ('гляциолог', 'Гляциолог'),
        ('инженер жизнеобеспечения', 'Инженер жизнеобеспечения'),
        ('метеоролог', 'Метеоролог'),
        ('оператор марсохода', 'Оператор марсохода'),
        ('киберинженер', 'Киберинженер'),
        ('штурман', 'Штурман'),
        ('пилот дронов', 'Пилот дронов')
    ], validators=[DataRequired()])
    gender = RadioField('Пол', choices=[('male', 'Мужской'), ('female', 'Женский')], validators=[DataRequired()])
    motivation = TextAreaField('Мотивация', validators=[DataRequired()])
    stay = BooleanField('Готовы ли остаться на Марсе?')
    photo = FileField('Фото', validators=[DataRequired()])

@app.route('/')
@app.route('/index')
def index():
    return render_template('index.html', title='Добро пожаловать!')

@app.route('/list_prof/<list_type>')
def list_prof(list_type):
    professions = [
        'Инженер-исследователь', 'Пилот', 'Строитель', 'Экзобиолог', 'Врач',
        'Инженер по терраформированию', 'Климатолог', 'Специалист по радиационной защите',
        'Астрогеолог', 'Гляциолог'
    ]
    return render_template('list_prof.html', title='Список профессий', list_type=list_type, professions=professions)

@app.route('/distribution')
def distribution():
    crew = load_crew_data()
    return render_template('distribution.html', title='Размещение', crew=crew)

@app.route('/member/<int:number>')
def member_by_number(number):
    crew = load_crew_data()
    if 1 <= number <= len(crew):
        selected = crew[number - 1]
        return render_template('member.html', title='Член экипажа', selected=selected, crew=crew)
    else:
        return render_template('member.html', title='Член экипажа', error="Член экипажа с таким номером не найден.", crew=crew)

@app.route('/member/random')
def member_random():
    crew = load_crew_data()
    if not crew:
        return render_template('member.html', title='Член экипажа', error="Список экипажа пуст.")
    return render_template('member.html', title='Член экипажа', crew=crew)

@app.route('/room/<sex>/<int:age>')
def room(sex, age):
    return render_template('room.html', title='Оформление каюты', sex=sex, age=age)

@app.route('/astronaut_selection', methods=['GET', 'POST'])
def astronaut_selection():
    form = AstronautForm()
    if form.validate_on_submit():
        photo = form.photo.data
        filename = secure_filename(photo.filename)
        filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        photo.save(filepath)
        flash('Заявка успешно отправлена!', 'success')
        return redirect(url_for('astronaut_selection'))
    return render_template('astronaut_selection.html', title='Запись добровольцем', form=form)

@app.route('/galery', methods=['GET', 'POST'])
def galery():
    upload_dir = os.path.join(app.static_folder, 'uploads')
    os.makedirs(upload_dir, exist_ok=True)

    image_files = [f for f in os.listdir(upload_dir) if f.lower().endswith(('.png', '.jpg', '.jpeg'))]

    gallery_images = [
        url_for('static', filename=f'uploads/{filename}')
        for filename in image_files
    ]

    if request.method == 'POST':
        photo = request.files.get('new_image')
        if photo and photo.filename:
            filename = secure_filename(photo.filename)
            filepath = os.path.join(upload_dir, filename)
            try:
                photo.save(filepath)
                flash('Изображение успешно добавлено!', 'success')
                image_files = [f for f in os.listdir(upload_dir) if f.lower().endswith(('.png', '.jpg', '.jpeg'))]
                gallery_images = [
                    url_for('static', filename=f'uploads/{filename}')
                    for filename in image_files
                ]
            except Exception as e:
                flash(f'Ошибка при сохранении: {e}', 'danger')

    return render_template(
        'galery.html',
        title='Галерея',
        gallery_images=gallery_images
    )

if __name__ == '__main__':
    app.run(host='127.0.0.1', port=8080, debug=True)