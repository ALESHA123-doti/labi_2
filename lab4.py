from flask import Blueprint, render_template, request, redirect, session
lab4 = Blueprint('lab4', __name__)

@lab4.route('/lab4/')
def lab():
    return render_template('lab4/lab4.html')

@lab4.route('/lab4/div-form')
def div_form():
    return render_template('lab4/div-form.html')

@lab4.route('/lab4/div', methods=['POST'])
def div():
    x1 = request.form.get('x1')
    x2 = request.form.get('x2')
    
    # Проверка, что оба поля заполнены
    if x1 == '' or x2 == '':
        return render_template('lab4/div.html', error='Оба поля должны быть заполнены!')
    try:
        x1 = int(x1)
        x2 = int(x2)
    except ValueError:
        return render_template('lab4/div.html', error='Пожалуйста, введите корректные целые числа.')
    
    # Проверка деления на ноль
    if x2 == 0:
        return render_template('lab4/div.html', error='На ноль делить нельзя!')
    
    result = x1 / x2
    return render_template('lab4/div.html', x1=x1, x2=x2, result=result)

# СЛОЖЕНИЕ
@lab4.route('/lab4/add-form')
def add_form():
    return render_template('lab4/add-form.html')

@lab4.route('/lab4/add', methods=['POST'])
def add():
    x1 = request.form.get('x1') or '0'
    x2 = request.form.get('x2') or '0'
    
    try:
        x1 = int(x1)
        x2 = int(x2)
    except ValueError:
        return render_template('lab4/add.html', error='Пожалуйста, введите корректные целые числа.')
    
    result = x1 + x2
    return render_template('lab4/add.html', x1=x1, x2=x2, result=result)


# УМНОЖЕНИЕ
@lab4.route('/lab4/mul-form')
def mul_form():
    return render_template('lab4/mul-form.html')

@lab4.route('/lab4/mul', methods=['POST'])
def mul():
    x1 = request.form.get('x1') or '1'
    x2 = request.form.get('x2') or '1'
    
    try:
        x1 = int(x1)
        x2 = int(x2)
    except ValueError:
        return render_template('lab4/mul.html', error='Пожалуйста, введите корректные целые числа.')
    
    result = x1 * x2
    return render_template('lab4/mul.html', x1=x1, x2=x2, result=result)


# ВЫЧИТАНИЕ
@lab4.route('/lab4/sub-form')
def sub_form():
    return render_template('lab4/sub-form.html')

@lab4.route('/lab4/sub', methods=['POST'])
def sub():
    x1 = request.form.get('x1')
    x2 = request.form.get('x2')
    
    if x1 == '' or x2 == '':
        return render_template('lab4/sub.html', error='Оба поля должны быть заполнены!')
    
    try:
        x1 = int(x1)
        x2 = int(x2)
    except ValueError:
        return render_template('lab4/sub.html', error='Пожалуйста, введите корректные целые числа.')
    
    result = x1 - x2
    return render_template('lab4/sub.html', x1=x1, x2=x2, result=result)


# ВОЗВЕДЕНИЕ В СТЕПЕНЬ
@lab4.route('/lab4/pow-form')
def pow_form():
    return render_template('lab4/pow-form.html')

@lab4.route('/lab4/pow', methods=['POST'])
def pow_view():
    x1 = request.form.get('x1')
    x2 = request.form.get('x2')
    
    if x1 == '' or x2 == '':
        return render_template('lab4/pow.html', error='Оба поля должны быть заполнены!')
    
    try:
        x1 = int(x1)
        x2 = int(x2)
    except ValueError:
        return render_template('lab4/pow.html', error='Пожалуйста, введите корректные целые числа.')
    
    if x1 == 0 and x2 == 0:
        return render_template('lab4/pow.html', error='0⁰ не определено!')
    
    # Обработка отрицательных степеней — можно использовать float, но для целых лучше ограничиться
    try:
        result = x1 ** x2
    except OverflowError:
        return render_template('lab4/pow.html', error='Результат слишком большой!')
    
    return render_template('lab4/pow.html', x1=x1, x2=x2, result=result)

tree_count = 0

@lab4.route('/lab4/tree', methods=['GET', 'POST'])
def tree():
    global tree_count
    if request.method == 'POST':
        operation = request.form.get('operation')
        if operation == 'cut' and tree_count > 0:
            tree_count -= 1
        elif operation == 'plant' and tree_count < 10:
            tree_count += 1
        return redirect('/lab4/tree')
    
    return render_template('lab4/tree.html', tree_count=tree_count)

users = [
    {'login': 'alex', 'password': '123', 'name': 'Александр Петров', 'gender': 'male'},
    {'login': 'bob', 'password': '555', 'name': 'Боб Марли', 'gender': 'male'},
    {'login': 'anna', 'password': '777', 'name': 'Анна Смирнова', 'gender': 'female'},
    {'login': 'mark', 'password': '321', 'name': 'Марк Цукерберг', 'gender': 'male'}
]


@lab4.route('/lab4/login', methods=['GET', 'POST'])
def login():
    if request.method == 'GET':
        if 'login' in session:
            current_login = session['login']
            user = next((u for u in users if u['login'] == current_login), None)
            if user:
                return render_template(
                    'lab4/login.html',
                    authorized=True,
                    user_name=user['name']
                )
        return render_template('lab4/login.html', authorized=False)

    # Получаем все поля
    login = request.form.get('login', '').strip()
    password = request.form.get('password', '').strip()
    name = request.form.get('name', '').strip()
    gender = request.form.get('gender')

    # Проверка: не введён логин
    if not login or login.strip() == '':
        return render_template(
            'lab4/login.html',
            error='не введён логин',
            login=login or ''
        )

    # Проверка: не введён пароль
    if not password or password.strip() == '':
        return render_template(
            'lab4/login.html',
            error='не введён пароль',
            login=login
        )
    if not name:
        return render_template('lab4/login.html', error='Не введено имя', login=login, name=name, gender=gender)
    if not gender:
        return render_template('lab4/login.html', error='Не выбран пол', login=login, name=name, gender=gender)

    # Поиск существующего пользователя
    user = next((u for u in users if u['login'] == login), None)

    if user:
        # Пользователь существует — проверяем пароль
        if user['password'] == password:
            session['login'] = login
            return redirect('/lab4/login')
        else:
            return render_template('lab4/login.html', error='Неверный пароль', login=login, name=name, gender=gender)
    else:
        # Новый пользователь — регистрируем
        users.append({
            'login': login,
            'password': password,
            'name': name,
            'gender': gender
        })
        session['login'] = login
        return redirect('/lab4/login')

@lab4.route('/lab4/logout', methods=['POST'])
def logout():
    session.pop('login', None)
    return redirect('/lab4/login')
