// Функция переключения темы
function toggleTheme() {
    const body = document.body;
    const root = document.documentElement;
    const current = body.classList.contains('dark') ? 'dark' : 'light';
    const newTheme = current === 'dark' ? 'light' : 'dark';

    // Sync both body and html to avoid mismatched states during toasts/modals
    body.classList.remove(current);
    body.classList.add(newTheme);
    root.classList.remove(current);
    root.classList.add(newTheme);
    localStorage.setItem('theme', newTheme);
    updateThemeIcon(newTheme);
}

// Обновление иконки темы
function updateThemeIcon(theme) {
    const btn = document.getElementById('theme-btn');
    btn.textContent = theme === 'dark' ? '☀️' : '🌙';
}

// Открытие модального окна для выбора шаблона
function openModal() {
    document.getElementById('docModal').style.display = 'block';
}

// Закрытие модального окна
function closeModal() {
    document.getElementById('docModal').style.display = 'none';
}

// Закрытие модального окна при клике вне его
window.onclick = function(event) {
    const modal = document.getElementById('docModal');
    if (event.target == modal) {
        closeModal();
    }
}

// Показать предупреждение о редактировании
function showEditWarning() {
    // Проверяем, не открыто ли уже сообщение
    if (!document.querySelector('.swal2-container')) {
        Swal.fire({
            toast: true,
            position: 'top-end',
            icon: 'info',
            title: 'Для изменения данных нажмите кнопку "Редактировать"',
            showConfirmButton: false,
            timer: 3000,
            timerProgressBar: true
        });
    }
}

// Включение режима редактирования
function enableEditing() {
    const inputs = document.querySelectorAll('input');
    inputs.forEach(input => {
        input.removeAttribute('readonly');
        input.style.pointerEvents = 'auto';
    });
            document.getElementById('edit-btn').style.display = 'none';
        document.getElementById('save-btn').classList.remove('hidden-btn');
    document.getElementById('avatar-label').classList.remove('disabled');
    const choosePhoto = document.getElementById('choose-photo');
    if (choosePhoto) {
        choosePhoto.classList.remove('disabled');
    }
    
    Swal.fire({
        toast: true,
        position: 'top-end',
        icon: 'success',
        title: 'Режим редактирования включен',
        showConfirmButton: false,
        timer: 3000
    });
}

// Инициализация при загрузке страницы
document.addEventListener('DOMContentLoaded', function() {
    // Обработка загрузки аватара
    const avatarInput = document.getElementById('avatar-input');
    const avatarPreview = document.getElementById('avatar-preview');
    const avatarForm = document.getElementById('avatar-form');
    const choosePhoto = document.getElementById('choose-photo');
    
    if (choosePhoto && avatarInput) {
        // Клик по ссылке "Выбрать фото" открывает файловый диалог
        choosePhoto.addEventListener('click', function() {
            if (!choosePhoto.classList.contains('disabled')) {
                avatarInput.click();
            }
        });
    }

    if (avatarInput) {
        avatarInput.addEventListener('change', function(event) {
            const file = event.target.files[0];
            if (file) {
                const reader = new FileReader();
                reader.onload = function(e) {
                    avatarPreview.src = e.target.result;
                };
                reader.readAsDataURL(file);
                
                const formData = new FormData(avatarForm);
                
                fetch(avatarForm.action, {
                    method: 'POST',
                    body: formData,
                    headers: {
                        'X-CSRFToken': document.querySelector('[name=csrfmiddlewaretoken]').value || document.querySelector('input[name="csrfmiddlewaretoken"]').value
                    }
                })
                .then(response => response.json())
                .then(data => {
                    if (data.success) {
                        avatarPreview.src = data.avatar_url + '?t=' + new Date().getTime();
                        Swal.fire({
                            toast: true,
                            position: 'top-end',
                            icon: 'success',
                            title: 'Аватар успешно обновлен',
                            showConfirmButton: false,
                            timer: 3000
                        });
                    }
                })
                .catch(error => {
                    console.error('Error:', error);
                    Swal.fire({
                        toast: true,
                        position: 'top-end',
                        icon: 'error',
                        title: 'Ошибка при загрузке аватара',
                        showConfirmButton: false,
                        timer: 3000
                    });
                });
            }
        });
    }

    // Улучшенные обработчики событий для полей ввода
    const formContainer = document.querySelector('.form-container');
    
    // Обработчик для всей формы (делегирование событий)
    formContainer.addEventListener('click', function(e) {
        // Проверяем, кликнули ли на поле ввода или его label
        const target = e.target;
        if (target.matches('input[readonly]') || 
            (target.tagName === 'LABEL' && document.getElementById(target.getAttribute('for'))?.hasAttribute('readonly'))) {
            e.preventDefault();
            showEditWarning();
        }
    });

    // Обработчики для клавиатурных событий
    document.addEventListener('keydown', function(e) {
        if (e.target.matches('input[readonly]')) {
            e.preventDefault();
            showEditWarning();
        }
    });

    // Обработчик для вставки текста
    document.addEventListener('paste', function(e) {
        if (e.target.matches('input[readonly]')) {
            e.preventDefault();
            showEditWarning();
        }
    });

    // Обработчик для фокуса
    document.addEventListener('focus', function(e) {
        if (e.target.matches('input[readonly]')) {
            e.preventDefault();
            e.target.blur();
            showEditWarning();
        }
    }, true); // Используем capture phase

    // Автодополнение для города
    const input = document.getElementById('city-input');
    if (input) {
        const suggestionsBox = document.createElement('div');
        suggestionsBox.id = 'city-suggestions';
        input.parentNode.appendChild(suggestionsBox);

        let timer = null;

        input.addEventListener('input', function() {
            clearTimeout(timer);
            const query = this.value.trim();
            suggestionsBox.innerHTML = '';

            if (query.length < 2) return;

            timer = setTimeout(() => {
                fetch(`/city-autocomplete/?q=${encodeURIComponent(query)}`)
                    .then(response => response.json())
                    .then(data => {
                        suggestionsBox.innerHTML = '';
                        data.forEach(city => {
                            const div = document.createElement('div');
                            div.textContent = city;
                            div.addEventListener('click', () => {
                                input.value = city;
                                suggestionsBox.innerHTML = '';
                            });
                            suggestionsBox.appendChild(div);
                        });
                    });
            }, 300);
        });

        document.addEventListener('click', function(e) {
            if (e.target !== input) {
                suggestionsBox.innerHTML = '';
            }
        });
    }

    // Обработка системных сообщений - перенесена в отдельную функцию
    // чтобы вызывать её после применения темы
    function processSystemMessages() {
        const messages = document.querySelectorAll('[data-message]');
        messages.forEach(messageElement => {
            const messageData = JSON.parse(messageElement.dataset.message);
            // Определяем правильную иконку на основе тега сообщения
            let icon = 'info'; // по умолчанию
            if (messageData.tags === 'success') {
                icon = 'success';
            } else if (messageData.tags === 'error') {
                icon = 'error';
            } else if (messageData.tags === 'warning') {
                icon = 'warning';
            }
            
            Swal.fire({
                toast: true,
                position: 'top-end',
                icon: icon,
                title: messageData.text,
                showConfirmButton: false,
                timer: 3000,
                timerProgressBar: true
            });
        });
    }
    
    // Вызываем обработку сообщений после небольшой задержки,
    // чтобы тема успела примениться
    setTimeout(processSystemMessages, 200);
});

// Применить сохранённую тему при загрузке - применяем сразу
// (тема уже применена в HTML, но обновляем иконку)
(function() {
    const saved = localStorage.getItem('theme') || 'light';
    const body = document.body;
    const root = document.documentElement;
    // Normalize classes on both root and body to the saved theme
    ['light', 'dark'].forEach(cls => {
        root.classList.remove(cls);
        body.classList.remove(cls);
    });
    root.classList.add(saved);
    body.classList.add(saved);
    updateThemeIcon(saved);
})();

// Обработка модального окна согласия
document.addEventListener('DOMContentLoaded', function () {
    const saveBtn = document.getElementById('save-btn');
    const consentModal = document.getElementById('consent-modal');

    // Значение из Django шаблона, true если нужно показать модалку
    const shouldShowConsentModal = document.body.dataset.showConsentModal === 'true';

    if (saveBtn) {
        saveBtn.addEventListener('click', function (e) {
            if (shouldShowConsentModal) {
                e.preventDefault(); // отменяем стандартное поведение (отправку формы)
                consentModal.style.display = 'block'; // показываем модальное окно с согласием
            }
            // иначе форма отправится сразу
        });
    }

    // Обработчик закрытия модалки
    const closeModalBtn = document.getElementById('close-modal');
    if (closeModalBtn) {
        closeModalBtn.addEventListener('click', function () {
            consentModal.style.display = 'none';
        });
    }

    // Если пользователь нажал "Принять"
    const acceptConsentBtn = document.getElementById('accept-consent');
    if (acceptConsentBtn) {
        acceptConsentBtn.addEventListener('click', function () {
            consentModal.style.display = 'none';
            document.getElementById('consent-form').submit();
        });
    }

    // Закрыть модалку при клике вне её
    if (consentModal) {
        window.addEventListener('click', function (e) {
            if (e.target === consentModal) {
                consentModal.style.display = 'none';
            }
        });
    }
});
