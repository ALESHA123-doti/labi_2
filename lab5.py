from flask import Blueprint, render_template, request, session, redirect, current_app
import psycopg2
from psycopg2.extras import RealDictCursor
from werkzeug.security import check_password_hash, generate_password_hash
import sqlite3
from os import path

lab5 = Blueprint('lab5', __name__)

@lab5.route('/lab5/')
def lab():
    return render_template('lab5/lab5.html', login=session.get('login'))

def db_connect():
    try:
        # На PythonAnywhere используем только SQLite
        dir_path = path.dirname(path.realpath(__file__))
        db_path = path.join(dir_path, "database.db")
        conn = sqlite3.connect(db_path)
        conn.row_factory = sqlite3.Row
        cur = conn.cursor()
        return conn, cur
    except Exception as e:
        print(f"Ошибка подключения к БД: {e}")
        raise

def db_close(conn, cur):
    conn.commit()
    cur.close()
    conn.close()

@lab5.route('/lab5/register', methods=['GET', 'POST'])
def register():
    if request.method == 'GET':
        return render_template('lab5/register.html')

    login = request.form.get('login')
    password = request.form.get('password')

    if not login or not password:
        return render_template('lab5/register.html', error='Заполните все поля')

    try:
        conn, cur = db_connect()

        # Проверяем, существует ли пользователь с таким логином
        cur.execute("SELECT login FROM users WHERE login = ?;", (login,))

        if cur.fetchone():
            db_close(conn, cur)
            return render_template('lab5/register.html', error="Такой пользователь уже существует")

        password_hash = generate_password_hash(password)
        cur.execute("INSERT INTO users (login, password) VALUES (?, ?);", (login, password_hash))
        
        db_close(conn, cur)
        return render_template('lab5/success.html', login=login)
    
    except Exception as e:
        print(f"Ошибка базы данных: {e}")
        return render_template('lab5/register.html', error=f"Ошибка базы данных: {e}")

@lab5.route('/lab5/login', methods=['GET', 'POST'])
def login():
    if request.method == 'GET':
        return render_template('lab5/login.html')

    login = request.form.get('login')
    password = request.form.get('password')

    if not login or not password:
        return render_template('lab5/login.html', error='Заполните все поля')

    try:
        conn, cur = db_connect()

        cur.execute("SELECT * FROM users WHERE login = ?;", (login,))
        user = cur.fetchone()

        if not user:
            db_close(conn, cur)
            return render_template('lab5/login.html', error='Логин и/или пароль неверны')

        if not check_password_hash(user['password'], password):
            db_close(conn, cur)
            return render_template('lab5/login.html', error='Логин и/или пароль неверны')

        session['login'] = login
        db_close(conn, cur)
        return render_template('lab5/success_login.html', login=login)
    
    except Exception as e:
        print(f"Ошибка при входе: {e}")
        return render_template('lab5/login.html', error='Ошибка сервера')

@lab5.route('/lab5/create', methods=['GET', 'POST'])
def create():
    login = session.get('login')
    if not login:
        return redirect('/lab5/login')
    
    if request.method == 'GET':
        return render_template('lab5/create_article.html')
    
    title = request.form.get('title')
    article_text = request.form.get('article_text')

    if not title or not article_text:
        return render_template('lab5/create_article.html', error='Заполните все поля')

    try:
        conn, cur = db_connect()

        # Получаем ID пользователя
        cur.execute("SELECT id FROM users WHERE login = ?;", (login,))
        user = cur.fetchone()
        if not user:
            db_close(conn, cur)
            return render_template('lab5/create_article.html', error='Пользователь не найден')

        login_id = user["id"]

        # Вставляем статью
        cur.execute("INSERT INTO articles (user_id, title, article_text) VALUES (?, ?, ?);", 
                   (login_id, title, article_text))

        db_close(conn, cur)
        return redirect('/lab5')
    
    except Exception as e:
        print(f"Ошибка при создании статьи: {e}")
        return render_template('lab5/create_article.html', error='Ошибка при создании статьи')

@lab5.route('/lab5/list')
def list_articles():
    login = session.get('login')
    if not login:
        return redirect('/lab5/login')
        
    try:
        conn, cur = db_connect()

        # Получаем ID пользователя
        cur.execute("SELECT id FROM users WHERE login = ?;", (login,))
        user = cur.fetchone()
        if not user:
            db_close(conn, cur)
            return redirect('/lab5/login')

        login_id = user["id"]

        # Получаем статьи пользователя
        cur.execute("SELECT * FROM articles WHERE user_id = ?;", (login_id,))
        articles = cur.fetchall()

        db_close(conn, cur)
        return render_template('lab5/articles.html', articles=articles, login=login)
    
    except Exception as e:
        print(f"Ошибка при получении статей: {e}")
        return render_template('lab5/articles.html', articles=[], login=login)