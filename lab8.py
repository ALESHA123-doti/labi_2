# lab8.py
from flask import Blueprint, render_template, request, redirect, flash
from db import db
from db.models import users, articles
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import login_user, login_required, logout_user, current_user

lab8 = Blueprint('lab8', __name__)

@lab8.route('/lab8/')
def lab():
    login = current_user.login if current_user.is_authenticated else None
    return render_template('lab8/lab8.html', login=login)


# РЕГИСТРАЦИЯ
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

    # Задание 2: автоматический вход после регистрации
    login_user(new_user, remember=False)
    return redirect('/lab8/')


# ВХОД
@lab8.route('/lab8/login/', methods=['GET', 'POST'])
def login():
    if request.method == 'GET':
        return render_template('lab8/login.html', error=None)

    login = request.form.get('login')
    password = request.form.get('password')
    remember = request.form.get('remember') == 'on'#галочка
    if not login or not password:
        return render_template('lab8/login.html', error="Логин и пароль не могут быть пустыми")
    
    user = users.query.filter_by(login=login).first()

    if user and check_password_hash(user.password, password):
        login_user(user, remember=remember)  #remember=True если галочка
        return redirect('/lab8/')
    
    return render_template('lab8/login.html', error="Неверный логин или пароль")


#ЛОГАУТ
@lab8.route('/lab8/logout/')
@login_required
def logout():
    logout_user()
    return redirect('/lab8/')


#СПИСОК СТАТЕЙ (только для авторизованных)
@lab8.route('/lab8/list/')
@login_required
def article_list():
    user_articles = articles.query.filter_by(login_id=current_user.id).all()
    return render_template('lab8/articles.html', articles=user_articles)


# СОЗДАНИЕ СТАТЬИ. Задание 4
@lab8.route('/lab8/create/', methods=['GET', 'POST'])
@login_required
def create_article():
    if request.method == 'GET':
        return render_template('lab8/create_article.html')

    title = request.form.get('title')
    article_text = request.form.get('article_text')

    if not title or not article_text:
        return render_template('lab8/create_article.html', error="Заголовок и текст обязательны")

    new_article = articles(
        login_id=current_user.id,
        title=title,
        article_text=article_text,
        is_favorite=False,
        is_public=True,
        likes=0
    )
    db.session.add(new_article)
    db.session.commit()
    return redirect('/lab8/articles/')


# РЕДАКТИРОВАНИЕ СТАТЬИ. Задание 5
@lab8.route('/lab8/edit/<int:article_id>/', methods=['GET', 'POST'])
@login_required
def edit_article(article_id):
    article = articles.query.filter_by(id=article_id, login_id=current_user.id).first_or_404()

    if request.method == 'GET':
        return render_template('lab8/edit_article.html', article=article)

    title = request.form.get('title')
    article_text = request.form.get('article_text')

    if not title or not article_text:
        return render_template('lab8/edit_article.html', article=article, error="Заголовок и текст обязательны")

    article.title = title
    article.article_text = article_text
    db.session.commit()
    return redirect('/lab8/articles/')


# УДАЛЕНИЕ СТАТЬИ. Задание 6
@lab8.route('/lab8/delete/<int:article_id>/')
@login_required
def delete_article(article_id):
    article = articles.query.filter_by(id=article_id, login_id=current_user.id).first_or_404()
    db.session.delete(article)
    db.session.commit()
    return redirect('/lab8/articles/')