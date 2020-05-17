from flask import render_template, flash, redirect, url_for, request
from app import app, db
from app.forms import LoginForm, EditProfileForm, EditSubstanceForm, \
    RegistrationForm, FilterForm, DeleteSelectForm, DeleteForm, AddCardForm
from flask_login import current_user, login_user, logout_user, login_required
from werkzeug.urls import url_parse
from datetime import datetime
from app.models import User, Substance
from werkzeug.utils import secure_filename
from config import Confpath
import os


@app.before_request
def before_request():
    if current_user.is_authenticated:
        current_user.last_seen = datetime.utcnow()
        db.session.commit()


@app.route('/')
@app.route('/index')
def index():
    substances = Substance.query.all()
    return render_template('index.html', title='Главная', substances=substances)


@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first_or_404()
        if user is None or not user.check_password(form.password.data):
            flash('Неверный логин или пароль')
            return redirect(url_for('login'))
        login_user(user, remember=form.remember_me.data)
        next_page = request.args.get('next')
        if not next_page or url_parse(next_page).netloc != '':
            next_page = url_for('index')
        return redirect(next_page)
    return render_template('login.html', title='Авторизация', form=form)


@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('index'))


@app.route('/user/<username>')
@login_required
def user(username):
    user = User.query.filter_by(username=username).first_or_404()
    return render_template('user.html', user=user)


@app.route('/edit_profile', methods=['GET', 'POST'])
@login_required
def edit_profile():
    form = EditProfileForm(current_user.username)
    if form.validate_on_submit():
        current_user.username = form.username.data
        current_user.notes = form.notes.data
        db.session.commit()
        flash('Изменения сохранены.')
        return redirect(url_for('edit_profile'))
    elif request.method == 'GET':
        form.username.data = current_user.username
        form.notes.data = current_user.notes
    return render_template('edit_profile.html', title='Редактировать профиль',
                           form=form)


@app.route('/result')
def result(substances):
    render_template('result.html', title='Результат запроса', substances=substances)


def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in Confpath.ALLOWED_EXTENSIONS


@app.route('/register', methods=['GET', 'POST'])
@login_required
def register():
    form = RegistrationForm()
    if form.validate_on_submit():
        substance = Substance(title=form.title.data,
                              fiz=form.fiz.data,
                              fiz2=form.fiz2.data,
                              put=form.put.data,
                              put2=form.put2.data,
                              put3=form.put3.data,
                              put4=form.put4.data,
                              kli=form.kli.data,
                              kli2=form.kli2.data,
                              kli3=form.kli3.data,
                              kli4=form.kli4.data,
                              kli5=form.kli5.data,
                              kli6=form.kli6.data,
                              kli7=form.kli7.data,
                              kli8=form.kli8.data,
                              kli9=form.kli9.data,
                              kli10=form.kli10.data,
                              )
        db.session.add(substance)
        db.session.commit()
        file = form.filename.data
        try:
            if file and allowed_file(file.filename):
                filename = secure_filename(str(substance.id) + ".pdf")
                file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
                flash("Успешно")
            else:
                db.session.delete(substance)
                db.session.commit()
                flash("Добавление вещества не удалось, проверьте тип файла, он должен быть '.pdf'")
        except Exception as ex:
            flash(ex)
        return redirect(url_for('register'))
    return render_template('register.html', title='Добавить вещества', form=form)


@app.route('/table')
def table():
    substances = Substance.query.all()
    return render_template('table.html', title='Все вещества', substances=substances)


@app.route('/substance/<title>', methods=['GET', 'POST'])
def substance(title):
    form = DeleteSelectForm()
    substance = Substance.query.filter_by(title=title).first_or_404()
    if form.validate_on_submit():
        filename = secure_filename(str(substance.id) + '.pdf')
        try:
            os.remove(os.path.join(app.config['UPLOAD_FOLDER'], filename))
        except Exception as ex:
            app.logger.error("Подобного файла в базе нет", ex)
            flash("Карточки вещества в базе не оказалось")
        db.session.delete(substance)
        db.session.commit()
        flash('Вещество удалено')
        return redirect(url_for('index'))
    return render_template('substance.html', title='Краткая информация по ' + substance.title, substance=substance,
                           form=form)


@app.route('/delete', methods=['GET', 'POST'])
@login_required
def delete():
    form = DeleteForm()
    if form.validate_on_submit():
        substance = Substance.query.filter_by(title=form.title.data.title).first_or_404()
        filename = secure_filename(str(substance.id) + '.pdf')
        try:
            os.remove(os.path.join(app.config['UPLOAD_FOLDER'], filename))
        except Exception as ex:
            app.logger.error("Подобного файла в базе нет", ex)
            flash("Карточки вещества в базе не оказалось")
        db.session.delete(substance)
        db.session.commit()
        flash('Вещество удалено')
        return redirect(url_for('delete'))
    return render_template('delete.html', title='Удалить вещества', form=form)


@app.route('/filter', methods=['GET', 'POST'])
def filter():
    form = FilterForm()
    if form.validate_on_submit():
        fiz = form.fiz.data
        fiz2 = form.fiz2.data
        put = form.put.data
        put2 = form.put2.data
        put3 = form.put3.data
        put4 = form.put4.data
        kli = form.kli.data
        kli2 = form.kli2.data
        kli3 = form.kli3.data
        kli4 = form.kli4.data
        kli5 = form.kli5.data
        kli6 = form.kli6.data
        kli7 = form.kli7.data
        kli8 = form.kli8.data
        kli9 = form.kli9.data
        kli10 = form.kli10.data
        substances = Substance.query.filter(
            Substance.fiz.endswith(fiz),
            Substance.fiz2.endswith(fiz2),
            Substance.put.endswith(put),
            Substance.put2.endswith(put2),
            Substance.put3.endswith(put3),
            Substance.put4.endswith(put4),
            Substance.kli.endswith(kli),
            Substance.kli2.endswith(kli2),
            Substance.kli3.endswith(kli3),
            Substance.kli4.endswith(kli4),
            Substance.kli5.endswith(kli5),
            Substance.kli6.endswith(kli6),
            Substance.kli7.endswith(kli7),
            Substance.kli8.endswith(kli8),
            Substance.kli9.endswith(kli9),
            Substance.kli10.endswith(kli10),
        ).all()
        if result:
            flash('РЕЗУЛЬТАТ:')
            return render_template('result.html', substances=substances)
    return render_template('filter.html', title='Поиск по свойствам', form=form)


@app.route('/edit_substance/<id_sub>', methods=['GET', 'POST'])
@login_required
def edit_substance(id_sub):
    form = EditSubstanceForm()
    if form.validate_on_submit():
        substance = Substance.query.get(id_sub)
        try:
            substance.title = form.newtitle.data
            substance.fiz = form.fiz.data
            substance.fiz2 = form.fiz2.data
            substance.put = form.put.data
            substance.put2 = form.put2.data
            substance.put3 = form.put3.data
            substance.put4 = form.put4.data
            substance.kli = form.kli.data
            substance.kli2 = form.kli2.data
            substance.kli3 = form.kli3.data
            substance.kli4 = form.kli4.data
            substance.kli5 = form.kli5.data
            substance.kli6 = form.kli6.data
            substance.kli7 = form.kli7.data
            substance.kli8 = form.kli8.data
            substance.kli9 = form.kli9.data
            substance.kli10 = form.kli10.data
            db.session.commit()
            flash('Успешно!')
        except Exception:
            flash('Такое название уже используется')
    elif request.method == 'GET':
        substance = Substance.query.get(id_sub)
        form.newtitle.data = substance.title
        form.fiz.data = substance.fiz
        form.fiz2.data = substance.fiz2
        form.put.data = substance.put
        form.put2.data = substance.put2
        form.put3.data = substance.put3
        form.put4.data = substance.put4
        form.kli.data = substance.kli
        form.kli.data = substance.kli2
        form.kli.data = substance.kli3
        form.kli.data = substance.kli4
        form.kli.data = substance.kli5
        form.kli.data = substance.kli6
        form.kli.data = substance.kli7
        form.kli.data = substance.kli8
        form.kli.data = substance.kli9
        form.kli.data = substance.kli10
        return render_template('edit_substance.html', form=form)
    return render_template('edit_substance.html', form=form)


@app.route('/addcard', methods=['GET', 'POST'])
@login_required
def addcard():
    form = AddCardForm()
    if form.validate_on_submit():
        substance = Substance.query.filter_by(title=form.title.data.title).first_or_404()
        file = form.filename.data
        oldfilename = secure_filename(str(substance.id) + '.pdf')
        try:
            os.remove(os.path.join(app.config['UPLOAD_FOLDER'], oldfilename))
            flash("Старая карточка удалена!")
        except Exception as ex:
            app.logger.error("Подобного файла в базе нет", ex)
            flash("Старой карточки в базе не было")
        if file and allowed_file(file.filename):
            filename = secure_filename(str(substance.id) + ".pdf")
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            flash("Успешно")
        else:
            flash("Загрузка новой карточки не удалась (проверьте формат файла, он должен быть '.pdf'")
        return redirect(url_for('addcard'))
    return render_template('addcard.html', title='Добавить карточку вещества', form=form)
