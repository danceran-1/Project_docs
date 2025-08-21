// JavaScript для улучшения работы видео и анимации
document.addEventListener('DOMContentLoaded', function() {
    const videos = document.querySelectorAll('.tooltip-gif');
    const bgElements = document.querySelectorAll('.bg-element');
    
    // Анимация слогана
    initTaglineAnimation();
    
    // Управление видео
    videos.forEach(function(video) {
        // Воспроизводим видео при наведении
        video.parentElement.parentElement.parentElement.addEventListener('mouseenter', function() {
            video.play().catch(function(error) {
                console.log('Ошибка воспроизведения видео:', error);
            });
        });
        
        // Останавливаем видео при уходе курсора
        video.parentElement.parentElement.parentElement.addEventListener('mouseleave', function() {
            video.pause();
            video.currentTime = 0;
        });
    });
    
    // Управление анимацией фоновых элементов
    // Анимации работают постоянно, без приостановки
    
    // Добавляем плавное появление элементов при загрузке страницы
    bgElements.forEach(function(element, index) {
        element.style.opacity = '0';
        element.style.transform = 'translateY(20px)';
        
        // Уменьшаем задержку для более быстрого появления
        setTimeout(function() {
            element.style.transition = 'opacity 0.5s ease, transform 0.5s ease';
            element.style.opacity = '0.2';
            element.style.transform = 'translateY(0)';
        }, index * 100);
    });
    
    // Функция инициализации анимации слогана
    function initTaglineAnimation() {
        const cursor = document.getElementById('cursor');
        const word1 = document.getElementById('word1');
        const word2 = document.getElementById('word2');
        const word3 = document.getElementById('word3');
        const saveIcon = document.getElementById('save-icon');
        
        if (!cursor || !word1 || !word2 || !word3 || !saveIcon) {
            console.log('Элементы анимации не найдены');
            return;
        }
        
        // Проверяем, что пути к изображениям доступны
        if (!window.staticImages) {
            console.log('Пути к изображениям не найдены');
            return;
        }
        
        // Скрываем оригинальный слоган
        const originalTagline = document.querySelector('.tagline');
        if (originalTagline) {
            originalTagline.style.display = 'none';
        }
        
        // Начинаем анимацию через 1 секунду после загрузки
        setTimeout(() => {
            startTaglineAnimation();
        }, 1000);
        
        // Добавляем возможность перезапуска анимации по клику на слоган
        const taglineContainer = document.querySelector('.tagline-container');
        if (taglineContainer) {
            taglineContainer.addEventListener('click', () => {
                resetAnimation();
                setTimeout(() => {
                    startTaglineAnimation();
                }, 800); // Увеличиваем задержку для полного сброса
            });
            
            // Добавляем подсказку после завершения анимации
            setTimeout(() => {
                taglineContainer.title = 'Кликните, чтобы повторить анимацию';
            }, 15000); // Через 15 секунд после начала
        }
        
        function startTaglineAnimation() {
            // Шаг 1: Появляется курсор внизу по центру
            cursor.style.opacity = '1';
            cursor.classList.add('position-start');
            
            setTimeout(() => {
                // Шаг 2: Курсор перемещается к первому слову
                cursor.classList.remove('position-start');
                cursor.classList.add('position-word1');
                
                setTimeout(() => {
                    // Шаг 3: Курсор меняется на ICursor и задерживается
                    cursor.src = window.staticImages.iCursor;
                    
                                            setTimeout(() => {
                            // Шаг 4: Курсор исчезает и начинается печатание первого слова
                            cursor.style.opacity = '0';
                            word1.classList.add('visible', 'typing');
                            
                            // Эмулируем печатание по буквам
                            const text = word1.textContent;
                            word1.textContent = '';
                            word1.style.opacity = '1';
                            
                            let i = 0;
                            const typeInterval = setInterval(() => {
                                if (i < text.length) {
                                    word1.textContent += text[i];
                                    i++;
                                } else {
                                    clearInterval(typeInterval);
                                    word1.classList.remove('typing');
                                }
                            }, 100);
                        
                        setTimeout(() => {
                            // Шаг 5: Появляется второе слово справа
                            word2.classList.add('visible', 'initial-position');
                            word2.style.transition = 'none'; // Отключаем transition для установки начальной позиции
                            word2.style.transform = 'translateX(50px)'; // Явно устанавливаем начальную позицию
                            word2.style.opacity = '0'; // Начинаем с прозрачности 0
                            
                            // Плавно показываем слово
                            setTimeout(() => {
                                word2.style.transition = 'opacity 0.5s ease-in-out';
                                word2.style.opacity = '1';
                            }, 10);
                            
                                                            setTimeout(() => {
                                    // Шаг 6: Появляется курсор и перемещается ко второму слову
                                    cursor.style.opacity = '1';
                                    cursor.src = window.staticImages.cursor;
                                cursor.classList.remove('position-word1');
                                cursor.classList.add('position-word2');
                                
                                setTimeout(() => {
                                    // Шаг 7: Курсор меняется на CursorMove
                                    cursor.src = window.staticImages.cursorMove;
                                    
                                    setTimeout(() => {
                                        // Шаг 8: Курсор и второе слово перемещаются вместе
                                        cursor.classList.add('moving-with-word');
                                        word2.classList.remove('initial-position');
                                        word2.classList.add('moving');
                                        
                                        // Небольшая задержка перед включением transition
                                        setTimeout(() => {
                                            word2.style.transition = 'transform 1s ease-in-out';
                                            word2.style.transform = 'translateX(0)';
                                        }, 10);
                                        
                                        setTimeout(() => {
                                            // Шаг 9: Курсор возвращается к обычному и перемещается к третьему слову
                                            cursor.src = window.staticImages.cursor;
                                            cursor.classList.remove('position-word2', 'moving-with-word');
                                            cursor.classList.add('position-word3');
                                            
                                            setTimeout(() => {
                                                // Шаг 10: Появляется иконка сохранения
                                                saveIcon.classList.add('visible');
                                                
                                                setTimeout(() => {
                                                    // Шаг 11: Курсор перемещается к иконке сохранения
                                                    cursor.classList.remove('position-word3');
                                                    cursor.classList.add('position-save');
                                                    
                                                    setTimeout(() => {
                                                        // Шаг 12: Курсор меняется на CursorClick
                                                        cursor.src = window.staticImages.cursorClick;
                                                        
                                                        setTimeout(() => {
                                                            // Шаг 13: Курсор и иконка исчезают, появляется третье слово
                                                            cursor.style.opacity = '0';
                                                            saveIcon.classList.remove('visible');
                                                            word3.classList.add('visible');
                                                            word3.style.opacity = '1';
                                                            
                                                                                                                         // Запускаем повтор анимации через 30 секунд
                                                             setTimeout(() => {
                                                                 resetAnimation();
                                                                 setTimeout(() => {
                                                                     startTaglineAnimation();
                                                                 }, 800);
                                                             }, 30000);
                                                            
                                                        }, 500); // Задержка для CursorClick
                                                    }, 500); // Задержка перед кликом
                                                }, 500); // Задержка перед перемещением к иконке
                                            }, 500); // Задержка перед появлением иконки
                                        }, 1000); // Задержка после перемещения слова
                                    }, 1000); // Задержка для CursorMove
                                }, 1000); // Задержка для ICursor
                            }, 500); // Задержка перед появлением курсора
                        }, 1000); // Задержка для печати первого слова
                    }, 1000); // Задержка для ICursor
                }, 1000); // Задержка для перемещения курсора
            }, 1000); // Задержка для появления курсора
        }
        
        function resetAnimation() {
            // Сбрасываем все состояния
            cursor.style.opacity = '0';
            cursor.classList.remove('position-word1', 'position-word2', 'position-word3', 'position-save', 'position-start', 'moving-with-word');
            cursor.src = window.staticImages.cursor;
            
            word1.classList.remove('visible', 'typing');
            word1.textContent = 'Заполняй';
            word1.style.opacity = '0';
            
            word2.classList.remove('visible', 'moving', 'initial-position');
            word2.textContent = 'Управляй';
            word2.style.opacity = '0';
            word2.style.transform = 'translateX(0)'; // Сбрасываем transform
            word2.style.transition = 'none'; // Отключаем transition при сбросе
            
            word3.classList.remove('visible');
            word3.textContent = 'Сохраняй';
            word3.style.opacity = '0';
            
            saveIcon.classList.remove('visible');
            
            // Принудительно перерисовываем элементы
            word1.offsetHeight;
            word2.offsetHeight;
            word3.offsetHeight;
        }
    }
});
