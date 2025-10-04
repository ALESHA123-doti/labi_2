from flask import Blueprint, url_for, request
import datetime
from werkzeug.exceptions import HTTPException
lab1 = Blueprint('lab1', __name__)

@lab1.route("/lab1")
def lab():
    return '''<!doctype html>
<html>
    <head>
        <title>Лабораторная 1</title>
    </head>
    <body>
        <h1>Лабораторная 1</h1>
        <p>Flask — фреймфорк для создания веб-приложений на языке
программирования Python, использующий набор инструментов
Werkzeug, а также шаблонизатор Jinja2. Относится к категории так
называемых микрофреймворков — минималистичных каркасов
веб-приложений, сознательно предоставляющих лишь самые базовые возможности.</p>
        <a href="/">На главную</a>
        
        <h2>Список роутов</h2>
        <ul>
            <li><a href="/lab1/web">/lab1/web</a> - Web сервер</li>
            <li><a href="/lab1/author">/lab1/author</a> - Информация об авторе</li>
            <li><a href="/lab1/image">/lab1/image</a> - Изображение со стилями</li>
            <li><a href="/lab1/counter">/lab1/counter</a> - Счетчик посещений</li>
            <li><a href="/lab1/counter/clear">/lab1/counter/clear</a> - Очистка счетчика</li>
            <li><a href="/lab1/info">/lab1/info</a> - Перенаправление на автора</li>
            <li><a href="/lab1/created">/lab1/created</a> - Страница создания (201)</li>
            <li><a href="/lab1/error">/lab1/error</a> - Вызов ошибки сервера</li>
            <li><a href="/400">/400</a> - Bad Request</li>
            <li><a href="/401">/401</a> - Unauthorized</li>
            <li><a href="/402">/402</a> - Payment Required</li>
            <li><a href="/403">/403</a> - Forbidden</li>
            <li><a href="/405">/405</a> - Method Not Allowed</li>
            <li><a href="/418">/418</a> - I'm a teapot</li>
            <li><a href="/404">/404</a> - Not found</li>
        </ul>
    </body>
</html>'''

@lab1.route("/lab1/web")
def web():
    return """<!doctype html> 
        <html> 
            <body> 
                 <h1>web-сервер на flask</h1> 
                 <a href="/lab1/author">author</a>
            </body> 
        </html>""", 200, {
            'X-Server': 'sample',
            'Content-Type':'text/plan; charset=utf-8'
            }

@lab1.route("/lab1/author")
def author():
    name = "Алёшкина Варвара Максимовна"
    group = "ФБИ-34"
    faculty = "ФБ"
    return """
<!doctype html>
<html>
    <body>
        <p>Студент: """ + name + """</p>
        <p>Группа: """ + group + """</p>
        <p>Факультет: """ + faculty + """</p>
        <a href="/lab1/web">web</a>
    </body>
</html>"""

@lab1.route('/lab1/image')
def image():
    css_url = url_for('static', filename='lab1.css')
    path = url_for("static", filename="silent.jpg")
    content = '''
<!doctype html>
<html>
    <head>
        <link rel="stylesheet" href="''' + css_url + '''">
    </head>
    <body>
        <h1>Тишина</h1>
        <img src="''' + path + '''">
    </body>
</html>'''
    
    # Возвращаем ответ с кастомными заголовками
    return content, 200, {
        'Content-Language': 'ru-RU',  # Язык контента - русский (Россия)
        'X-Student-Name': 'Alyoshkina Varvara',  # Кастомный заголовок с именем студента
        'X-Lab-Number': '1',  # Кастомный заголовок с номером лабораторной
        'X-Server-Technology': 'Flask Python Framework'  # Кастомный заголовок с технологией
    }

count = 0

@lab1.route('/lab1/counter')
def counter():
    global count
    count += 1
    time = str(datetime.datetime.today())
    url = request.url
    client_ip = request.remote_addr
    return '''
<!doctype html>
<html>
    <body>
        Сколько раз вы сюда заходили: ''' + str(count) + '''
        <hr>
        Дата и время: ''' + time + '''<br>
        Запрошенный адрес: ''' + url + '''<br>
        Ваш IP-адрес: ''' + client_ip + '''<br>
        <a href="/lab1/counter/clear">Очистить счётчик</a>
    </body>
</html>'''

@lab1.route('/lab1/counter/clear')
def clear_counter():
    global count
    count = 0
    return redirect('/lab1/counter')

@lab1.route("/lab1/info")
def info():
    return redirect("/lab1/author")

@lab1.route("/lab1/created")
def created():
    return '''<!doctype html>
<html>
    <body>
        <h1>Создано успешно</h1>
        <div><i>что-то создано...</i></div>
    </body>
</html>''', 201