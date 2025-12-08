from flask import Blueprint, render_template, request, jsonify

lab7 = Blueprint('lab7', __name__)

# Исходный список фильмов
films = [
    {
        "title": "Five Nights at Freddy's 2",
        "title_ru": "Пять ночей с Фредди 2",
        "year": 2025,
        "description": "Прошёл год с момента страшных событий в пиццерии Freddy Fazbear`s, и слухи о произошедшем уже превратились в местную легенду. Легенда стала настолько популярной, что в честь событий в городе планируется провести фестиваль. Бывший охранник пиццерии Майк и офицер полиции Ванесса скрывают от Эбби, 11-летней сестры Майка, правду о судьбе её друзей-аниматроников. Однако когда девочка сбегает, чтобы снова встретиться с Фредди, Бонни, Чикой и Фокси, она вызывает цепь пугающих событий."
    },
    {
        "title": "Avatar: Fire and Ash",
        "title_ru": "Аватар: Пламя и пепел",
        "year": 2025,
        "description": "Джейк Салли, Нейтири и их дети переживают смерть Нетейама. Противостояние с корпорацией RDA обостряется, и теперь семье предстоит столкнуться с враждебным племенем На`ви во главе с Варанг."
    },
    {
        "title": "Zootopia 2",
        "title_ru": "Зверополис 2",
        "year": 2025,
        "description": "Кролик-полицейский Джуди и лис Ник идут по следу загадочной рептилии, чьё прибытие в Зверополис переворачивает жизнь города с ног на голову. Чтобы раскрыть дело, Джуди и Ник вынуждены работать под прикрытием в разных районах города."
    }
]

# Главная страница
@lab7.route('/lab7/')
def main():
    return render_template('lab7/index.html')

# Получить все фильмы
@lab7.route('/lab7/rest-api/films/', methods=['GET'])
def get_films():
    return jsonify(films)

# Получить один фильм по ID
@lab7.route('/lab7/rest-api/films/<int:id>', methods=['GET'])
def get_film(id):
    if 0 <= id < len(films):
        return jsonify(films[id])
    return jsonify({"error": "Фильм не найден"}), 404

# Удалить фильм по ID
@lab7.route('/lab7/rest-api/films/<int:id>', methods=['DELETE'])
def del_film(id):
    if 0 <= id < len(films):
        del films[id]
        return '', 204
    return jsonify({"error": "Фильм не найден"}), 404

# Изменить фильм по ID (PUT)
@lab7.route('/lab7/rest-api/films/<int:id>', methods=['PUT'])
def put_film(id):
    if 0 <= id < len(films):
        film = request.get_json()
        films[id] = film
        return jsonify(films[id])
    return jsonify({"error": "Фильм не найден"}), 404

# Добавить новый фильм (POST)
@lab7.route('/lab7/rest-api/films/', methods=['POST'])
def add_film():
    film = request.get_json()
    films.append(film)
    return jsonify({"id": len(films) - 1})