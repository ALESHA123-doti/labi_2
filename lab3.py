from flask import Blueprint, render_template, request, make_response, redirect

lab3 = Blueprint('lab3', __name__)

@lab3.route('/lab3/')
def lab():
    name = request.cookies.get('name')
    name_color = request.cookies.get('name_color')
    age = request.cookies.get('age')
    if name is None:
        name = 'аноним'
    if age is None:
        age = 'возраст не указан'

    return render_template('lab3.html', name=name, name_color=name_color, age=age)

@lab3.route('/lab3/cookie')
def cookie():
    resp = make_response(redirect('/lab3/'))
    resp.set_cookie('name', 'Alex', max_age=5)  
    resp.set_cookie('age', '20')
    resp.set_cookie('name_color', 'magenta')
    return resp

@lab3.route('/lab3/del_cookie')
def del_cookie():
    resp = make_response(redirect('/lab3/'))
    resp.delete_cookie('name')
    resp.delete_cookie('age')
    resp.delete_cookie('name_color')
    return resp

@lab3.route('/lab3/form1')
def form1():
    errors = {}
    user = request.args.get('user')
    age = request.args.get('age')
    sex = request.args.get('sex')

    if user == '':
        errors['user'] = 'Заполните поле!'
    if age == '' or age is None:
        errors['age'] = 'Заполните поле!'

    return render_template('lab3/form1.html', user=user, age=age, sex=sex, errors=errors)

@lab3.route('/lab3/order')
def order():
    return render_template('lab3/order.html')
    
@lab3.route('/lab3/pay')
def pay():
    price = 0
    drink = request.args.get('drink')
    milk = request.args.get('milk')
    sugar = request.args.get('sugar')

    # Определяем базовую стоимость напитка
    drink_prices = {
        'cofee': 120,
        'black-tea': 80,
        'green-tea': 70
    }
    price += drink_prices.get(drink, 0)

    # Добавки
    if milk == 'on':
        price += 30
    if sugar == 'on':
        price += 10

    return render_template('lab3/pay.html', price=price, drink=drink, milk=milk, sugar=sugar)

@lab3.route('/lab3/success')
def success():
    price = request.args.get('price', '0')
    return render_template('lab3/success.html', price=price)

from flask import request, make_response, redirect, render_template

from flask import request, make_response, redirect, render_template

@lab3.route('/lab3/settings')
def settings():
    # Получаем новые значения из формы (если есть)
    color = request.args.get('color')
    bg_color = request.args.get('bg_color')
    font_size = request.args.get('font_size')
    font_style = request.args.get('font_style')

    # Если хотя бы один параметр передан — сохраняем в куки и перенаправляем
    if any([color, bg_color, font_size, font_style]):
        resp = make_response(redirect('/lab3/settings'))
        if color is not None:
            resp.set_cookie('color', color)
        if bg_color is not None:
            resp.set_cookie('bg_color', bg_color)
        if font_size is not None:
            resp.set_cookie('font_size', font_size)
        if font_style is not None:
            resp.set_cookie('font_style', font_style)
        return resp

    # Иначе — читаем текущие настройки из кук и отображаем форму
    color = request.cookies.get('color', '#000000')
    bg_color = request.cookies.get('bg_color', '#ffffff')
    font_size = request.cookies.get('font_size', '16')
    font_style = request.cookies.get('font_style', 'normal')

    return render_template(
        'lab3/settings.html',
        color=color,
        bg_color=bg_color,
        font_size=font_size,
        font_style=font_style
    )

@lab3.route('/lab3/ticket')
def ticket_form():
    errors = {}
    # Получаем данные из GET-параметров (если форма уже отправлялась)
    fio = request.args.get('fio', '').strip()
    berth = request.args.get('berth')
    bedding = request.args.get('bedding') == 'on'
    baggage = request.args.get('baggage') == 'on'
    age_str = request.args.get('age', '').strip()
    departure = request.args.get('departure', '').strip()
    destination = request.args.get('destination', '').strip()
    travel_date = request.args.get('travel_date')
    insurance = request.args.get('insurance') == 'on'

    # Валидация
    if not fio:
        errors['fio'] = 'Введите ФИО пассажира'
    if not berth:
        errors['berth'] = 'Выберите полку'
    if not age_str:
        errors['age'] = 'Укажите возраст'
    else:
        try:
            age = int(age_str)
            if age < 1 or age > 120:
                errors['age'] = 'Возраст должен быть от 1 до 120 лет'
            else:
                # Сохраняем корректный возраст для расчёта
                pass
        except ValueError:
            errors['age'] = 'Возраст должен быть числом'
            age = None
    if not departure:
        errors['departure'] = 'Укажите пункт выезда'
    if not destination:
        errors['destination'] = 'Укажите пункт назначения'
    if not travel_date:
        errors['travel_date'] = 'Выберите дату поездки'

    # Если есть ошибки — возвращаем форму с подсветкой
    if errors:
        return render_template(
            'lab3/ticket_form.html',
            fio=fio,
            berth=berth,
            bedding=bedding,
            baggage=baggage,
            age=age_str,
            departure=departure,
            destination=destination,
            travel_date=travel_date,
            insurance=insurance,
            errors=errors
        )

    # Если всё в порядке — рассчитываем билет
    age = int(age_str)
    is_child = age < 18
    base_price = 700 if is_child else 1000

    # Доплаты
    price = base_price
    if berth in ['lower', 'side_lower']:
        price += 100
    if bedding:
        price += 75
    if baggage:
        price += 250
    if insurance:
        price += 150

    ticket_type = "Детский билет" if is_child else "Взрослый билет"

    # Передаём данные в шаблон билета
    return render_template(
        'lab3/ticket.html',
        fio=fio,
        berth=berth,
        bedding=bedding,
        baggage=baggage,
        age=age,
        departure=departure,
        destination=destination,
        travel_date=travel_date,
        insurance=insurance,
        price=price,
        ticket_type=ticket_type
    )