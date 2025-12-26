from flask import Blueprint, render_template, request, jsonify, session
import random
import string

lab9 = Blueprint('lab9', __name__)

# Изображения коробок и подарков
GIFT_IMAGES = [f"gift{i}.jpg" for i in range(1, 11)]
GIFTS = [f"present{i}.jpg" for i in range(1, 11)]

CONGRATULATIONS = [
    "С Новым годом! Пусть каждый день будет ярче солнца!",
    "Пусть в вашем доме всегда царит тепло и уют!",
    "Желаю вам исполнения всех заветных желаний!",
    "Пусть счастье постучится в вашу дверь и останется навсегда!",
    "Будьте здоровы, счастливы и окружены любовью!",
    "Пусть новый год принесёт вам удачу и вдохновение!",
    "Желаю вам море радости и океан вдохновения!",
    "Пусть все ваши мечты станут реальностью!",
    "Пусть каждый день будет наполнен смехом и добром!",
    "С праздником! Пусть всё будет прекрасно!"
]

USER_STATE = {}

def get_user_id():
    if 'user_id' not in session:
        session['user_id'] = ''.join(random.choices(string.ascii_letters + string.digits, k=12))
    return session['user_id']

def generate_positions():
    positions = []
    attempts_per_box = 50
    min_dist = 140
    container_width = 1120  
    container_height = 520 

    for i in range(10):
        placed = False
        for _ in range(attempts_per_box):
            x = random.randint(40, container_width - 100)
            y = random.randint(40, container_height - 100)
            # Проверка расстояния до уже размещенных
            too_close = False
            for p in positions:
                dx = p['x'] - x
                dy = p['y'] - y
                if (dx * dx + dy * dy) < min_dist * min_dist:
                    too_close = True
                    break
            if not too_close:
                positions.append({'x': x, 'y': y})
                placed = True
                break
        if not placed:
            grid_x = 40 + (i % 5) * 200
            grid_y = 40 + (i // 5) * 250
            positions.append({'x': grid_x, 'y': grid_y})
    return positions

@lab9.route('/lab9/')
def main():
    user_id = get_user_id()
    if user_id not in USER_STATE:
        USER_STATE[user_id] = {
            'opened': {},
            'positions': generate_positions()
        }
    
    user_data = USER_STATE[user_id]
    opened = user_data['opened']
    positions = user_data['positions']

    boxes_data = []
    for i in range(10):
        boxes_data.append({
            'id': i,
            'image': GIFT_IMAGES[i],
            'is_opened': opened.get(i, False),
            'x': positions[i]['x'],
            'y': positions[i]['y']
        })

    opened_count = sum(opened.values())
    remaining_count = 10 - opened_count

    return render_template(
        'lab9/index.html',
        boxes_data=boxes_data,
        gifts=GIFTS,
        opened_count=opened_count,
        remaining_count=remaining_count
    )

@lab9.route('/lab9/open_box', methods=['POST'])
def open_box():
    user_id = get_user_id()
    data = request.get_json()
    
    if not data or 'box_id' not in data:
        return jsonify({'success': False, 'message': 'Неверный запрос.'})
    
    try:
        box_id = int(data['box_id'])
    except (ValueError, TypeError):
        return jsonify({'success': False, 'message': 'Неверный ID коробки.'})
    
    if not (0 <= box_id < 10):
        return jsonify({'success': False, 'message': 'Неверный номер коробки.'})
    
    if user_id not in USER_STATE:
        USER_STATE[user_id] = {'opened': {}, 'positions': generate_positions()}
    user_data = USER_STATE[user_id]
    opened = user_data['opened']

    if opened.get(box_id, False):
        return jsonify({'success': False, 'message': 'Эта коробка уже открыта!'})

    opened_count = sum(opened.values())
    if opened_count >= 3:
        return jsonify({'success': False, 'message': 'Вы уже открыли 3 подарка. Больше нельзя!'})

    opened[box_id] = True

    return jsonify({
        'success': True,
        'congratulation': CONGRATULATIONS[box_id],
        'gift_image': GIFTS[box_id],
        'box_id': box_id,
        'opened_count': opened_count + 1
    })