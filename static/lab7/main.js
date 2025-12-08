function fillFilmList() {
    fetch('/lab7/rest-api/films/')
        .then(function (response) {
            return response.json();
        })
        .then(function (films) {
            const tbody = document.getElementById('film-list');
            tbody.innerHTML = '';

            for (let i = 0; i < films.length; i++) {
                const tr = document.createElement('tr');

                // 1. Русское название — основное, жирное/обычное
                const tdTitleRu = document.createElement('td');
                tdTitleRu.innerText = films[i].title_ru;

                // 2. Оригинальное название — в скобках, курсивом, серым цветом (если не совпадает)
                const tdTitle = document.createElement('td');
                if (films[i].title && films[i].title !== films[i].title_ru) {
                    const em = document.createElement('em');
                    em.innerText = films[i].title;
                    tdTitle.appendChild(document.createTextNode('('));
                    tdTitle.appendChild(em);
                    tdTitle.appendChild(document.createTextNode(')'));
                    tdTitle.style.color = '#e0f0e0';
                } else {
                    tdTitle.innerText = ''; // если совпадает или пусто — не показываем
                }

                const tdYear = document.createElement('td');
                tdYear.innerText = films[i].year;

                const tdActions = document.createElement('td');

                const editBtn = document.createElement('button');
                editBtn.innerText = 'редактировать';
                editBtn.onclick = function () {
                    editFilm(i);
                };

                const delBtn = document.createElement('button');
                delBtn.innerText = 'удалить';
                delBtn.onclick = function () {
                    deleteFilm(i, films[i].title_ru);
                };

                tdActions.appendChild(editBtn);
                tdActions.appendChild(delBtn);

                // Порядок: русское → оригинальное → год → действия
                tr.appendChild(tdTitleRu);
                tr.appendChild(tdTitle);
                tr.appendChild(tdYear);
                tr.appendChild(tdActions);

                tbody.appendChild(tr);
            }
        });
}

function deleteFilm(id, title) {
    if (!confirm(`Вы точно хотите удалить фильм "${title}"?`)) {
        return;
    }
    fetch(`/lab7/rest-api/films/${id}`, { method: 'DELETE' })
        .then(function () {
            fillFilmList();
        });
}

function editFilm(id) {
    // Очищаем ошибку перед открытием формы
    document.getElementById('description_error').innerText = '';

    fetch(`/lab7/rest-api/films/${id}`)
        .then(function (response) {
            return response.json();
        })
        .then(function (film) {
            document.getElementById('id').value = id;
            document.getElementById('title').value = film.title;
            document.getElementById('title_ru').value = film.title_ru;
            document.getElementById('year').value = film.year;
            document.getElementById('description').value = film.description;
            showModal();
        });
}

function addFilm() {
    // Очищаем форму и ошибки
    document.getElementById('id').value = '';
    document.getElementById('title').value = '';
    document.getElementById('title_ru').value = '';
    document.getElementById('year').value = '';
    document.getElementById('description').value = '';
    document.getElementById('description_error').innerText = '';
    showModal();
}

function showModal() {
    document.querySelector('.modal').style.display = 'block';
}

function hideModal() {
    document.querySelector('.modal').style.display = 'none';
}

function cancel() {
    hideModal();
}

function sendFilm() {
    const id = document.getElementById('id').value;
    const film = {
        title: document.getElementById('title').value,
        title_ru: document.getElementById('title_ru').value,
        year: parseInt(document.getElementById('year').value),
        description: document.getElementById('description').value
    };

    // Определяем метод и URL
    const url = id === '' ? '/lab7/rest-api/films/' : `/lab7/rest-api/films/${id}`;
    const method = id === '' ? 'POST' : 'PUT';

    fetch(url, {
        method: method,
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify(film)
    })
    .then(function (response) {
        if (response.ok) {
            fillFilmList();
            hideModal();
            return {};
        }
        return response.json();
    })
    .then(function (errors) {
        if (errors && errors.description) {
            document.getElementById('description_error').innerText = errors.description;
        }
    });
}

// Запуск при загрузке страницы
document.addEventListener('DOMContentLoaded', fillFilmList);

