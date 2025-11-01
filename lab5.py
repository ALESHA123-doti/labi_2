from flask import Blueprint, render_template, request
import psycopg2
lab5 = Blueprint('lab5', __name__)

@lab5.route('/lab5/')
def lab():
    return render_template('lab5/lab5.html')

@lab5.route('/lab5/register', methods=['GET', 'POST'])
def register():
    if request.method == 'GET':
        return render_template('lab5/register.html')

    login = request.form.get('login')
    password = request.form.get('password')

    if not (login or password):
        return render_template('lab5/register.html', error='Заполните все поля')

    try:
        conn = psycopg2.connect(
            host='127.0.0.1',
            database='varya_aleshkina_knowledge_base',
            user='varya_aleshkina_knowledge_base',
            password='111'
        )
        cur = conn.cursor()

        # Проверяем, существует ли пользователь с таким логином (исправлено)
        cur.execute("SELECT login FROM users WHERE login = %s;", (login,))

        if cur.fetchone():
            cur.close()
            conn.close()
            return render_template('lab5/register.html', error="Такой пользователь уже существует")

        # Добавляем нового пользователя (исправлено)
        cur.execute("INSERT INTO users (login, password) VALUES (%s, %s);", (login, password))
        conn.commit()

        cur.close()
        conn.close()
        return render_template('lab5/success.html', login=login)
    
    except Exception as e:
        # Выведем ошибку для отладки
        print(f"Ошибка базы данных: {e}")
        return render_template('lab5/register.html', error=f"Ошибка базы данных: {e}")