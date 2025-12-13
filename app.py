from flask import Flask, url_for, request, redirect, abort, render_template
import datetime
import os
from os import path
from flask_sqlalchemy import SQLAlchemy
from db import db
from werkzeug.exceptions import HTTPException
from lab1 import lab1
from lab2 import lab2
from lab3 import lab3
from lab4 import lab4
from lab5 import lab5
from lab6 import lab6
from lab7 import lab7
from lab8 import lab8

app = Flask(__name__)
app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY', 'секретно-секретный секрет')
app.config['DB_TYPE'] = os.getenv('DB_TYPE', 'sqlite')

db_name = 'varya_aleshkina_orm'
db_user = 'varya_aleshkina_orm'
db_password = '333'
host_ip = '127.0.0.1'
host_port = 5432

app.config['SQLALCHEMY_DATABASE_URI'] = f'postgresql://{db_user}:{db_password}@{host_ip}:{host_port}/{db_name}'

if app.config['DB_TYPE'] == 'postgres':
    db_name = 'varya_aleshkina_orm'
    db_user = 'varya_aleshkina_orm'
    db_password = '333'
    host_ip = '127.0.0.1'
    host_port = 5432
    app.config['SQLALCHEMY_DATABASE_URI'] = \
        f'postgresql://{db_user}:{db_password}@{host_ip}:{host_port}/{db_name}'
else:
    dir_path = path.dirname(path.realpath(__file__))
    db_path = path.join(dir_path, "varya_aleshkina_orm.db")
    app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///{db_path}'

db.init_app(app)

app.register_blueprint(lab1)
app.register_blueprint(lab2)
app.register_blueprint(lab3)
app.register_blueprint(lab4)
app.register_blueprint(lab5)
app.register_blueprint(lab6)
app.register_blueprint(lab7)
app.register_blueprint(lab8)

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

