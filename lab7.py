from flask import Blueprint, render_template, jsonify, request
from datetime import datetime

lab7 = Blueprint('lab7', __name__)

# Список фильмов
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

@lab7.route('/lab7/')
def main():
    return render_template('lab7/index.html')

@lab7.route('/lab7/rest-api/films/', methods=['GET'])
def get_films():
    return jsonify(films)

@lab7.route('/lab7/rest-api/films/<int:id>', methods=['GET'])
def get_film(id):
    if id < 0 or id >= len(films):
        return jsonify({"error": "Фильм не найден"}), 404
    return jsonify(films[id])

@lab7.route('/lab7/rest-api/films/<int:id>', methods=['DELETE'])
def del_film(id):
    if id < 0 or id >= len(films):
        return jsonify({"error": "Фильм не найден"}), 404
    del films[id]
    return '', 204

def _normalize_film_data(data):
    """Вспомогательная функция: нормализует и валидирует данные фильма."""
    if not isinstance(data, dict):
        return None, {"error": "Неверный формат данных"}

    # Обязательные поля
    title_ru = data.get('title_ru', '').strip()
    description = data.get('description', '').strip()

    if not title_ru:
        return None, {"title_ru": "Русское название обязательно"}
    if not description:
        return None, {"description": "Заполните описание"}

    # Опциональное: оригинальное название
    title = data.get('title', '').strip()
    if not title:
        title = title_ru  # ← основная логика задания

    # Год
    try:
        year = int(data.get('year', 0))
    except (TypeError, ValueError):
        return None, {"year": "Год должен быть числом"}

    return {
        "title": title,
        "title_ru": title_ru,
        "year": year,
        "description": description
    }, None

@lab7.route('/lab7/rest-api/films/<int:id>', methods=['PUT'])
def put_film(id):
    if id < 0 or id >= len(films):
        return jsonify({"error": "Фильм не найден"}), 404

    film_data = request.get_json()
    normalized, error = _normalize_film_data(film_data)
    if error:
        return jsonify(error), 400

    films[id] = normalized
    return jsonify(films[id])

@lab7.route('/lab7/rest-api/films/', methods=['POST'])
def add_film():
    film_data = request.get_json()
    normalized, error = _normalize_film_data(film_data)
    if error:
        return jsonify(error), 400

    films.append(normalized)
    return jsonify(len(films) - 1)