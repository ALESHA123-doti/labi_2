from flask import Flask, url_for, request, redirect, abort, render_template 
import datetime
from werkzeug.exceptions import HTTPException
from lab1 import lab1
from lab2 import lab2
from lab3 import lab3

app = Flask(__name__)
app.register_blueprint(lab1)
app.register_blueprint(lab2)
app.register_blueprint(lab3)

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
                </ul>
            </nav>
        </main>

        <footer>
            <hr>
            <p>Алёшкина Варвара Максимовна, ФБИ-34, 3 курс, 2025</p>
        </footer>
    </body>
</html>'''

