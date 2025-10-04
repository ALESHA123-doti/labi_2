from flask import Flask, url_for, request, redirect, abort, render_template 
import datetime
from werkzeug.exceptions import HTTPException
from lab1 import lab1 

app = Flask(__name__)
app.register_blueprint(lab1)

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
                    <li><a href="/lab2">Вторая лабораторная</a></li>
                </ul>
            </nav>
        </main>

        <footer>
            <hr>
            <p>Алёшкина Варвара Максимовна, ФБИ-34, 3 курс, 2025</p>
        </footer>
    </body>
</html>'''

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

# --- МАТЕМАТИЧЕСКИЙ КАЛЬКУЛЯТОР

@app.route('/lab2/calc/<int:a>/<int:b>')
def calc(a, b):
    return render_template('calc.html', a=a, b=b)

# Редирект: /lab2/calc/ -> /lab2/calc/1/1
@app.route('/lab2/calc/')
def calc_default():
    return redirect('/lab2/calc/1/1')

# Редирект: /lab2/calc/<a> -> /lab2/calc/a/1
@app.route('/lab2/calc/<int:a>')
def calc_with_one_param(a):
    return redirect(f'/lab2/calc/{a}/1')

# Список книг
books = [
    {"author": "Фёдор Достоевский", "title": "Преступление и наказание", "genre": "Роман", "pages": 672},
    {"author": "Лев Толстой", "title": "Война и мир", "genre": "Роман-эпопея", "pages": 1225},
    {"author": "Антуан де Сент-Экзюпери", "title": "Маленький принц", "genre": "Философская сказка", "pages": 96},
    {"author": "Джордж Оруэлл", "title": "1984", "genre": "Антиутопия", "pages": 328},
    {"author": "Рэй Брэдбери", "title": "451 градус по Фаренгейту", "genre": "Антиутопия", "pages": 256},
    {"author": "Габриэль Гарсиа Маркес", "title": "Сто лет одиночества", "genre": "Магический реализм", "pages": 416},
    {"author": "Михаил Булгаков", "title": "Мастер и Маргарита", "genre": "Фантастика, сатира", "pages": 448},
    {"author": "Джейн Остин", "title": "Гордость и предубеждение", "genre": "Роман", "pages": 432},
    {"author": "Харпер Ли", "title": "Убить пересмешника", "genre": "Драма", "pages": 324},
    {"author": "Эрнест Хемингуэй", "title": "Старик и море", "genre": "Повесть", "pages": 128},
    {"author": "Агата Кристи", "title": "Убийство в Восточном экспрессе", "genre": "Детектив", "pages": 256},
    {"author": "Виктор Пелевин", "title": "Чапаев и Пустота", "genre": "Постмодернизм", "pages": 352}
]

@app.route('/lab2/books')
def books_list():
    return render_template('books.html', books=books)

# Список котиков 
cats = [
    {
        "name": "Сиамская кошка",
        "description": "Элегантная кошка с короткой шерстью и выразительными голубыми глазами. Известна своим голосом и любовью к общению.",
        "image": "siamese.jpg"
    },
    {
        "name": "Мейн-кун",
        "description": "Один из крупнейших пород домашних кошек. Обладает пушистой шерстью и дружелюбным характером.",
        "image": "maine_coon.jpg"
    },
    {
        "name": "Британская короткошерстная",
        "description": "Спокойная, уравновешенная кошка с плотной шерстью и круглым лицом. Отличный компаньон для семьи.",
        "image": "british_shorthair.jpg"
    },
    {
        "name": "Персидская кошка",
        "description": "Имеет длинную шелковистую шерсть и плоское лицо. Требует регулярного ухода за шерстью.",
        "image": "persian.jpg"
    },
    {
        "name": "Рэгдолл",
        "description": "Нежная и ласковая кошка, которая расслабляется при поднятии — отсюда и название. Очень привязана к хозяину.",
        "image": "ragdoll.jpg"
    },
    {
        "name": "Сфинкс",
        "description": "Безшерстная кошка с теплой кожей и необычным внешним видом. Очень активная и игривая.",
        "image": "sphynx.jpg"
    },
    {
        "name": "Бенгальская кошка",
        "description": "Порода с диким окрасом, напоминающим леопарда. Энергичная, любит воду и активные игры.",
        "image": "bengal.jpg"
    },
    {
        "name": "Шотландская вислоухая",
        "description": "Узнаваема по загнутым вниз ушкам. Мягкий, спокойный характер и любовь к детям.",
        "image": "scottish_fold.jpg"
    },
    {
        "name": "Норвежская лесная кошка",
        "description": "Дикая красота с густой шерстью, приспособленной к холодному климату. Ловкач и отличный лазатель.",
        "image": "norwegian_forest.jpg"
    },
    {
        "name": "Абиссинская кошка",
        "description": "Грациозная, энергичная кошка с тонкой шерстью и «диким» окрасом. Любопытна и умна.",
        "image": "abyssinian.jpg"
    },
    {
        "name": "Турецкая ангора",
        "description": "Элегантная кошка с длинной шелковистой шерстью и пушистым хвостом. Любит высоту и игру.",
        "image": "turkish_angora.jpg"
    },
    {
        "name": "Ориентальная кошка",
        "description": "Худощавая, с большими ушами и ярким характером. Очень разговорчивая и требует внимания.",
        "image": "oriental.jpg"
    },
    {
        "name": "Русская голубая",
        "description": "Кошка с серебристо-серой шерстью и зелёными глазами. Скромна, но очень преданна хозяину.",
        "image": "russian_blue.jpg"
    },
    {
        "name": "Манчкин",
        "description": "Кошка с короткими лапками — «коротышка». Не теряет в подвижности, зато выглядит забавно.",
        "image": "munchkin.jpg"
    },
    {
        "name": "Экзотическая короткошерстная",
        "description": "Похожа на персидскую, но с короткой шерстью. Спокойная, нежная и идеальна для квартир.",
        "image": "exotic_shorthair.jpg"
    },
    {
        "name": "Бирманская кошка",
        "description": "Священная кошка Бирмы с голубыми глазами и белыми лапками. Очень дружелюбна и ласкова.",
        "image": "birman.jpg"
    },
    {
        "name": "Девон-рекс",
        "description": "Кошка с волнистой шерстью и большими ушами. Очень игрива и ласковая, почти как собака.",
        "image": "devon_rex.jpg"
    },
    {
        "name": "Корниш-рекс",
        "description": "Имеет уникальную волнистую шерсть и элегантное телосложение. Активна и любит общение.",
        "image": "cornish_rex.jpg"
    },
    {
        "name": "Тайская кошка",
        "description": "Близкая родственница сиамской, но с более мягким характером. Голосистая и общительная.",
        "image": "thai.jpg"
    },
    {
        "name": "Американская короткошерстная",
        "description": "Здоровая, жизнерадостная кошка с крепким телосложением. Неприхотлива и отлично подходит для новичков.",
        "image": "american_shorthair.jpg"
    }

]

@app.route('/lab2/cats')
def cats_list():
    return render_template('cats.html', cats=cats)