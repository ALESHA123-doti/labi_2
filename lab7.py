from flask import Blueprint, render_template, jsonify, request

lab7 = Blueprint('lab7', __name__)

films = [
    {
        "title": "Five Nights at Freddy's 2",
        "title_ru": "Пять ночей с Фредди 2",
        "year": 2025,
        "description": "Прошёл год с момента страшных событий в пиццерии Freddy Fazbear`s, и слухи о произошедшем уже превратились в местную легенду.\
        Легенда стала настолько популярной, что в честь событий в городе планируется провести фестиваль. Бывший охранник пиццерии Майк и офицер полиции Ванесса скрывают от Эбби, 11-летней сестры\
        Майка, правду о судьбе её друзей-аниматроников. Однако когда девочка сбегает, чтобы снова встретиться с Фредди, Бонни,\
        Чикой и Фокси, она вызывает цепь пугающих событий."
    },
    {
        "title": "Avatar: Fire and Ash",
        "title_ru": "Аватар: Пламя и пепел",
        "year": 2025,
        "description": "Джейк Салли, Нейтири и их дети переживают смерть Нетейама. Противостояние с корпорацией RDA обостряется,\
        и теперь семье предстоит столкнуться с враждебным племенем На`ви во главе с Варанг."
    },
    {
        "title": "Zootopia 2",
        "title_ru": "Зверополис 2",
        "year": 2025,
        "description": "Кролик-полицейский Джуди и лис Ник идут по следу загадочной рептилии, чьё прибытие в Зверополис переворачивает жизнь города с ног на голову.\
        Чтобы раскрыть дело, Джуди и Ник вынуждены работать под прикрытием в разных районах города."
    },
]

@lab7.route('/lab7/')
def main():
    return render_template('lab7/index.html')

@lab7.route('/lab7/rest-api/films/', methods=['GET'])
def get_films():
    return jsonify(films)  

# REST API для получения конкретного фильма по ID
@lab7.route('/lab7/rest-api/films/<int:id>', methods=['GET'])
def get_film(id):
    if id < 0 or id >= len(films):
        return {"error": "Фильм не найден"}, 404
    return jsonify(films[id])

@lab7.route('/lab7/rest-api/films/<int:id>', methods=['DELETE'])
def del_film(id):
    del films[id]
    return '', 204

@lab7.route('/lab7/rest-api/films/<int:id>', methods=['PUT'])
def edit_film(id):
    # Проверяем, что id находится в допустимом диапазоне
    if id < 0 or id >= len(films):
        return jsonify({'error': 'Film not found'}), 404
    # Получаем данные из тела запроса
    film_data = request.get_json()
    # Проверяем, что JSON был передан и это словарь
    if not isinstance(film_data, dict):
        return jsonify({'error': 'Invalid JSON data'}), 400
    # Обязательные поля (по заданию — все 4)
    required_fields = ['title', 'title_ru', 'year', 'description']
    for field in required_fields:
        if field not in film_data:
            return jsonify({'error': f'Missing required field: {field}'}), 400
    # Обновляем фильм
    films[id] = {
        'title': film_data['title'],
        'title_ru': film_data['title_ru'],
        'year': film_data['year'],
        'description': film_data['description']
    }
    return jsonify(films[id]), 200

@lab7.route('/lab7/rest-api/films/', methods=['POST'])
def add_film():
    # Получаем данные из тела запроса
    film_data = request.get_json()
    # Проверяем, что JSON был передан и это словарь
    if not isinstance(film_data, dict):
        return jsonify({'error': 'Invalid JSON data'}), 400
    # Обязательные поля (по заданию — все 4)
    required_fields = ['title', 'title_ru', 'year', 'description']
    for field in required_fields:
        if field not in film_data:
            return jsonify({'error': f'Missing required field: {field}'}), 400
    # Добавляем новый фильм в конец списка
    films.append({
        'title': film_data['title'],
        'title_ru': film_data['title_ru'],
        'year': film_data['year'],
        'description': film_data['description']
    })
    # Возвращаем ID нового фильма (индекс в списке)
    new_id = len(films) - 1
    return jsonify({'id': new_id}), 201