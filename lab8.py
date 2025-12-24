from flask import Blueprint, render_template, request, redirect, session
from db import db
from db.models import users, articles
lab8 = Blueprint('lab8', __name__)
from werkzeug.security import generate_password_hash
from flask_login import login_user, login_required, current_user
from werkzeug.security import check_password_hash

@lab8.route('/lab8/')
def lab():
    login = current_user.login if current_user.is_authenticated else None
    return render_template('lab8/lab8.html', login=login)

@lab8.route('/lab8/register/', methods=['GET', 'POST'])
def register():
    if request.method == 'GET':
        return render_template('lab8/register.html', error=None)

    login = request.form.get('login')
    password = request.form.get('password')

    if not login or not password:
        return render_template('lab8/register.html', error="Логин и пароль не могут быть пустыми")

    existing_user = users.query.filter_by(login=login).first()
    if existing_user:
        return render_template('lab8/register.html', error="Логин уже занят")

    hashed_password = generate_password_hash(password)
    new_user = users(login=login, password=hashed_password)
    db.session.add(new_user)
    db.session.commit()

    return redirect('/lab8/')

@lab8.route('/lab8/login/', methods=['GET', 'POST'])
def login():
    if request.method == 'GET':
        return render_template('lab8/login.html', error=None)

    login = request.form.get('login')
    password = request.form.get('password')

    # Проверка на пустые поля
    if not login or not password:
        return render_template('lab8/login.html', error="Логин и пароль не могут быть пустыми")

    # Ищем пользователя
    user = users.query.filter_by(login=login).first()

    # Проверяем пароль
    if user and check_password_hash(user.password, password):
        login_user(user, remember=False)  # авторизуем
        return redirect('/lab8/')

    # Если не найден или пароль не совпал
    return render_template('lab8/login.html', error="Неверный логин или пароль")

@lab8.route('/lab8/articles/')
@login_required
def article_list():
    return "список статей"