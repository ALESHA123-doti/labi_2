from flask import Flask, url_for, request, redirect, abort, render_template 
import datetime
from werkzeug.exceptions import HTTPException
app = Flask(__name__)

@app.errorhandler(404)
def not_found(err):
    css_url = url_for('static', filename='lab1.css')
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
        <img src="{url_for('static', filename='ppp.jpg')}" alt="Тишина">
        <br>
        <a href="/">Вернуться на главную</a>
    </body>
</html>''', 404

@app.errorhandler(500)
def internal_server_error(err):
    css_url = url_for('static', filename='lab1.css')
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

# Роут для вызова ошибки сервера
@app.route("/lab1/error")
def cause_error():
    # Вызываем ошибку деления на ноль
    result = 1 / 0

# Обычные обработчики для стандартных ошибок
@app.errorhandler(400)
def bad_request(err):
    return "400 Bad Request - Неверный запрос", 400

@app.errorhandler(401)
def unauthorized(err):
    return "401 Unauthorized - Неавторизован", 401

@app.errorhandler(403)
def forbidden(err):
    return "403 Forbidden - Запрещено", 403

@app.errorhandler(405)
def method_not_allowed(err):
    return "405 Method Not Allowed - Метод не разрешен", 405

# Для нестандартных кодов используем обычные роуты
@app.route("/400")
def error_400():
    return "400 Bad Request - Неверный запрос", 400

@app.route("/401")
def error_401():
    return "401 Unauthorized - Неавторизован", 401

@app.route("/402")
def error_402():
    return "402 Payment Required - Необходима оплата", 402

@app.route("/403")
def error_403():
    return "403 Forbidden - Запрощено", 403

@app.route("/405")
def error_405():
    return "405 Method Not Allowed - Метод не разрешен", 405

@app.route("/418")
def error_418():
    return "418 I'm a teapot - Я чайник", 418

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
                </ul>
            </nav>
        </main>

        <footer>
            <hr>
            <p>Алёшкина Варвара Максимовна, ФБИ-34, 3 курс, 2025</p>
        </footer>
    </body>
</html>'''

@app.route("/lab1")
def lab1():
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

@app.route("/lab1/web")
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

@app.route("/lab1/author")
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

@app.route('/lab1/image')
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

@app.route('/lab1/counter')
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

@app.route('/lab1/counter/clear')
def clear_counter():
    global count
    count = 0
    return redirect('/lab1/counter')

@app.route("/lab1/info")
def info():
    return redirect("/lab1/author")

@app.route("/lab1/created")
def created():
    return '''<!doctype html>
<html>
    <body>
        <h1>Создано успешно</h1>
        <div><i>что-то создано...</i></div>
    </body>
</html>''', 201

@app.route('/lab2/a')
def a():
    return 'без слеша'

@app.route('/lab2/a/')
def a2():
    return 'со слешем'


flower_list = ['роза', 'тюльпан', 'незабудка', 'ромашка']

# --- НОВЫЙ: обработчик для /lab2/add_flower/
@app.route('/lab2/add_flower/')
def add_flower_no_name():
    abort(400, description="вы не задали имя цветка")

# --- СТАРЫЙ: добавление цветка с именем
@app.route('/lab2/add_flower/<name>')
def add_flower(name):
    flower_list.append(name)
    return f'''
<!doctype html>
<html>
    <head>
        <title>Цветок добавлен</title>
    </head>
    <body>
        <h1>Добавлен цветок</h1>
        <p>Название нового цветка: {name}</p>
        <p>Всего цветов: {len(flower_list)}</p>
        <p>Полный список: {', '.join(flower_list)}</p>
        <br>
        <a href="/lab2/all_flowers">Посмотреть все цветы</a> |
        <a href="/lab2/">Назад в лабораторную 2</a>
    </body>
</html>
'''

# --- НОВЫЙ: вывод всех цветов 
@app.route('/lab2/all_flowers')
def all_flowers():
    return f'''
<!doctype html>
<html>
    <head>
        <title>Все цветы</title>
    </head>
    <body>
        <h1>Список всех цветов</h1>
        <p>Всего цветов: {len(flower_list)}</p>
        <ul>
            {''.join(f'<li>{flower}</li>' for flower in flower_list)}
        </ul>
        <br>
        <a href="/lab2/clear_flowers">Очистить список</a> |
        <a href="/lab2/">Назад в лабораторную 2</a>
    </body>
</html>
'''

# --- УЛУЧШЕННЫЙ: просмотр одного цветка по ID 
@app.route('/lab2/flowers/<int:flower_id>')
def flowers(flower_id):
    if flower_id >= len(flower_list):
        abort(404)
    flower_name = flower_list[flower_id]
    return f'''
<!doctype html>
<html>
    <head>
        <title>Цветок #{flower_id}</title>
    </head>
    <body>
        <h1>Цветок #{flower_id}</h1>
        <p>Название: <strong>{flower_name}</strong></p>
        <p>Всего цветов в списке: {len(flower_list)}</p>
        <br>
        <a href="/lab2/all_flowers">Посмотреть все цветы</a> |
        <a href="/lab2/">Назад в лабораторную 2</a>
    </body>
</html>
'''

# --- НОВЫЙ: очистка списка цветов
@app.route('/lab2/clear_flowers')
def clear_flowers():
    global flower_list
    flower_list.clear()  
    return f'''
<!doctype html>
<html>
    <head>
        <title>Список очищен</title>
    </head>
    <body>
        <h1>Список цветов очищен!</h1>
        <p>Теперь в списке 0 цветов.</p>
        <br>
        <a href="/lab2/all_flowers">Посмотреть все цветы</a> |
        <a href="/lab2/">Назад в лабораторную 2</a>
    </body>
</html>
'''

@app.errorhandler(400)
def bad_request(err):
    message = err.description if err.description else "вы не задали имя цветка"
    return f"400 Bad Request - {message}", 400

@app.route('/lab2/example')
def example():
    name, lab_num, group, course = 'Алёшкина Варя', 2, 'ФБИ-34', 3
    fruits = [
    {'name': 'яблоки', 'price': 100},
    {'name': 'груши', 'price': 120},
    {'name': 'апельсины', 'price': 80},
    {'name': 'мандарины', 'price': 95},
    {'name': 'манго', 'price': 321}
    ]
    return render_template('example.html',
                           name=name, lab_num=lab_num, group=group,
                           course=course, fruits=fruits)

@app.route('/lab2/')
def lab2():
    return render_template('lab2.html')

@app.route('/lab2/filters')
def filters():
    phrase = "О <b>сколько</b> <u>нам</u> <i>открытий</i> чудных..."
    return render_template('filter.html', phrase=phrase)

