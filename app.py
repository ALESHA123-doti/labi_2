from flask import Flask, url_for, render_template
import os
from os import path
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager

from lab1 import lab1
from lab2 import lab2
from lab3 import lab3
from lab4 import lab4
from lab5 import lab5
from lab6 import lab6
from lab7 import lab7
from lab8 import lab8

from db.models import users

app = Flask(__name__)
app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY', 'секретно-секретный секрет')

IS_ON_PYTHONANYWHERE = 'PYTHONANYWHERE' in os.environ

if IS_ON_PYTHONANYWHERE:
    # На хостинге — SQLite
    dir_path = path.dirname(path.realpath(__file__))
    db_path = path.join(dir_path, "varya_aleshkina_orm.db")
    app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///{db_path}'
else:
    # Локально — тоже SQLite для простоты
    dir_path = path.dirname(path.realpath(__file__))
    db_path = path.join(dir_path, "varya_aleshkina_orm_local.db")
    app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///{db_path}'

from db import db
db.init_app(app)

app.register_blueprint(lab1)
app.register_blueprint(lab2)
app.register_blueprint(lab3)
app.register_blueprint(lab4)
app.register_blueprint(lab5)
app.register_blueprint(lab6)
app.register_blueprint(lab7)
app.register_blueprint(lab8)

# === Настройка Flask-Login ===
login_manager = LoginManager()
login_manager.login_view = 'lab8.login'  # роут для входа
login_manager.init_app(app)

@login_manager.user_loader
def load_user(user_id):
    return users.query.get(int(user_id))

# === Обработчики ошибок ===
@app.errorhandler(404)
def not_found(err):
    css_url = url_for('static', filename='lab1/lab1.css')
    img_url = url_for('static', filename='lab1/ppp.jpg')
    home_url = url_for('index')
    return f'''<!doctype html>
<html>
    <head>
        <title>Страница не найдена</title>
        <link rel="stylesheet" href="{css_url}">
    </head>
    <body>
        <h1>404 - Страница потерялась в тишине</h1>
        <p>К сожалению, запрашиваемая страница не найдена.</p>
        <p>Возможно, она переехала или никогда не существовала.</p>
        <img src="{img_url}" alt="Тишина">
        <br>
        <a href="{home_url}">Вернуться на главную</a>
    </body>
</html>''', 404

@app.errorhandler(500)
def internal_server_error(err):
    css_url = url_for('static', filename='lab1/lab1.css')
    return f'''<!doctype html>
<html>
    <head>
        <title>Ошибка сервера</title>
        <link rel="stylesheet" href="{css_url}">
    </head>
    <body>
        <h1>500 - Внутренняя ошибка сервера</h1>
        <p>На сервере произошла непредвиденная ошибка.</p>
        <p>Пожалуйста, попробуйте позже или обратитесь к администратору.</p>
        <br>
        <a href="/">Вернуться на главную</a>
    </body>
</html>''', 500

# === Главная страница ===
@app.route("/")
@app.route("/index")
def index():
    return '''<!doctype html>
<html>
    <head>
        <title>НГТУ, ФБ, Лабораторные работы</title>
    </head>
    <body>
        <header>
            <h1>НГТУ, ФБ, WEB-программирование, часть 2. Список лабораторных</h1>
        </header>
        <main>
            <nav>
                <ul>
                    <li><a href="/lab1">Первая лабораторная</a></li>
                    <li><a href="/lab2">Вторая лабораторная</a></li>
                    <li><a href="/lab3/">Третья лабораторная</a></li>
                    <li><a href="/lab4/">Четвертая лабораторная</a></li>
                    <li><a href="/lab5/">Пятая лабораторная</a></li>
                    <li><a href="/lab6/">Шестая лабораторная</a></li>
                    <li><a href="/lab7/">Седьмая лабораторная</a></li>
                    <li><a href="/lab8/">Восьмая лабораторная</a></li>
                </ul>
            </nav>
        </main>
        <footer>
            <hr>
            <p>Алёшкина Варвара Максимовна, ФБИ-34, 3 курс, 2025</p>
        </footer>
    </body>
</html>'''