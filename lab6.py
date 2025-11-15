from flask import Blueprint, render_template, request, session, jsonify

lab6 = Blueprint('lab6', __name__)

offices = []
for i in range(1, 11):
    offices.append({"number": i, "tenant": "", "price": 1000})

@lab6.route('/lab6/')
def main():
    return render_template('lab6/lab6.html')

@lab6.route('/json-rpc-api', methods=['POST'])
def api():
    data = request.json
    method = data.get('method')
    params = data.get('params')

    if method == 'info':
        return jsonify({"jsonrpc": "2.0", "result": offices, "id": data.get('id')})

    elif method == 'booking':
        if 'login' not in session:
            return jsonify({
                "jsonrpc": "2.0",
                "error": {"code": 1, "message": "Вы не авторизованы"},
                "id": data.get('id')
            })

        if not isinstance(params, int):
            return jsonify({
                "jsonrpc": "2.0",
                "error": {"code": -32602, "message": "Неверный параметр: номер кабинета должен быть числом"},
                "id": data.get('id')
            })

        office_num = params
        
        office_found = False
        for office in offices:
            if office["number"] == office_num:
                office_found = True
                if office["tenant"] != "":
                    return jsonify({
                        "jsonrpc": "2.0",
                        "error": {"code": 2, "message": "Кабинет уже забронирован"},
                        "id": data.get('id')
                    })
                office["tenant"] = session['login']
                break
        
        if not office_found:
            return jsonify({
                "jsonrpc": "2.0",
                "error": {"code": 4, "message": "Кабинет с таким номером не существует"},
                "id": data.get('id')
            })

        return jsonify({"jsonrpc": "2.0", "result": "success", "id": data.get('id')})

    elif method == 'cancellation':
        # Проверка на авторизацию
        if 'login' not in session:
            return jsonify({
                "jsonrpc": "2.0",
                "error": {"code": 1, "message": "Вы не авторизованы"},
                "id": data.get('id')
            })

        # Проверка на корректность параметра
        if not isinstance(params, int):
            return jsonify({
                "jsonrpc": "2.0",
                "error": {"code": -32602, "message": "Неверный параметр: номер кабинета должен быть числом"},
                "id": data.get('id')
            })

        office_num = params
        
        office_found = False
        for office in offices:
            if office["number"] == office_num:
                office_found = True
                # Проверка, что кабинет арендован
                if office["tenant"] == "":
                    return jsonify({
                        "jsonrpc": "2.0",
                        "error": {"code": 3, "message": "Кабинет не забронирован"},
                        "id": data.get('id')
                    })
                # Проверка, что кабинет арендован текущим пользователем
                if office["tenant"] != session['login']:
                    return jsonify({
                        "jsonrpc": "2.0",
                        "error": {"code": 3, "message": "Кабинет забронирован другим пользователем"},
                        "id": data.get('id')
                    })
                # Освобождаем кабинет
                office["tenant"] = ""
                break

        if not office_found:
            return jsonify({
                "jsonrpc": "2.0",
                "error": {"code": 4, "message": "Кабинет с таким номером не существует"},
                "id": data.get('id')
            })

        return jsonify({"jsonrpc": "2.0", "result": "success", "id": data.get('id')})

    else:
        return jsonify({
            "jsonrpc": "2.0",
            "error": {"code": -32601, "message": "Метод не найден"},
            "id": data.get('id')
        })