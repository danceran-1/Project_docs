document.addEventListener('DOMContentLoaded', function() {
    const passwordField = document.getElementById('password');
    const passwordToggle = document.getElementById('passwordToggle');
    const toggleIcon = document.getElementById('toggleIcon');
    const errorContainer = document.getElementById('errorContainer');
    const errorMessage = document.getElementById('errorMessage');
    const loginForm = document.querySelector('.login-form');
    
    // Состояние видимости пароля
    let isPasswordVisible = false;
    
    // Функция для показа ошибки
    function showError(message) {
        errorMessage.textContent = message;
        errorContainer.style.display = 'block';
        
        // Автоматически скрыть ошибку через 5 секунд
        setTimeout(() => {
            hideError();
        }, 5000);
    }
    
    // Функция для скрытия ошибки
    function hideError() {
        errorContainer.style.display = 'none';
    }
    
    // Обработчик клика по кнопке показа/скрытия пароля
    passwordToggle.addEventListener('click', function() {
        if (isPasswordVisible) {
            // Скрываем пароль
            passwordField.type = 'password';
            toggleIcon.src = '/static/main/UnvisiblePass.png';
            toggleIcon.alt = 'Показать пароль';
            isPasswordVisible = false;
        } else {
            // Показываем пароль
            passwordField.type = 'text';
            toggleIcon.src = '/static/main/VisiblePass.png';
            toggleIcon.alt = 'Скрыть пароль';
            isPasswordVisible = true;
        }
    });
    
    // Обработчик отправки формы
    loginForm.addEventListener('submit', function(e) {
        const email = document.getElementById('username').value;
        const password = passwordField.value;
        
        // Скрываем предыдущую ошибку
        hideError();
        
        // Валидация на стороне клиента
        if (!email || !password) {
            e.preventDefault();
            showError('Пожалуйста, заполните все поля');
            return;
        }
        
        // Проверка формата email
        const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
        if (!emailRegex.test(email)) {
            e.preventDefault();
            showError('Пожалуйста, введите корректный email');
            return;
        }
        
        // Проверка длины пароля
        if (password.length < 8) {
            e.preventDefault();
            showError('Пароль должен содержать минимум 6 символов');
            return;
        }
        
        // Если валидация прошла успешно, форма отправится на сервер
        // Показываем индикатор загрузки
        const submitButton = loginForm.querySelector('.login-button');
        const originalText = submitButton.textContent;
        submitButton.textContent = 'Вход...';
        submitButton.disabled = true;
        
        // Восстанавливаем кнопку через 3 секунды (на случай ошибки)
        setTimeout(() => {
            submitButton.textContent = originalText;
            submitButton.disabled = false;
        }, 3000);
    });
    
    // Дополнительные улучшения UX
    const inputFields = document.querySelectorAll('.input-field');
    
    inputFields.forEach(field => {
        // Добавляем класс при фокусе
        field.addEventListener('focus', function() {
            this.parentElement.classList.add('focused');
            // Скрываем ошибку при начале ввода
            hideError();
        });
        
        // Убираем класс при потере фокуса
        field.addEventListener('blur', function() {
            if (!this.value) {
                this.parentElement.classList.remove('focused');
            }
        });
        
        // Добавляем класс если поле уже заполнено при загрузке
        if (field.value) {
            field.parentElement.classList.add('focused');
        }
    });
    
    // Скрытие ошибки при клике вне формы
    document.addEventListener('click', function(e) {
        if (!loginForm.contains(e.target) && !errorContainer.contains(e.target)) {
            hideError();
        }
    });
    
    // Обработка Enter в полях ввода
    inputFields.forEach(field => {
        field.addEventListener('keypress', function(e) {
            if (e.key === 'Enter') {
                e.preventDefault();
                loginForm.dispatchEvent(new Event('submit'));
            }
        });
    });
    
    // Обработчик для галочки "Запомнить меня"
    const rememberMeCheckbox = document.getElementById('rememberMe');
    const rememberMeLabel = document.querySelector('.remember-me-label');
    
    if (rememberMeCheckbox) {
        // Добавляем звуковой эффект при клике (опционально)
        rememberMeCheckbox.addEventListener('change', function() {
            if (this.checked) {
                // Можно добавить звук или другую обратную связь
                console.log('Запомнить меня активировано');
            } else {
                console.log('Запомнить меня деактивировано');
            }
        });
        
        // Добавляем анимацию при клике на текст
        rememberMeLabel.addEventListener('click', function(e) {
            // Небольшая задержка для визуального эффекта
            setTimeout(() => {
                rememberMeCheckbox.checked = !rememberMeCheckbox.checked;
                rememberMeCheckbox.dispatchEvent(new Event('change'));
            }, 50);
        });
    }
}); 