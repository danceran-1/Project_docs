document.addEventListener("DOMContentLoaded", function() {
    const fieldsContainer = document.getElementById('fieldsContainer');
    const saveButton = document.getElementById('saveButton');

    // Генерация полей ввода для каждого критерия
    for (let i = 1; i <= 18; i++) {
        const fieldPair = document.createElement('div');
        fieldPair.classList.add('field-pair');
        fieldPair.innerHTML = `
            <label for="fieldA_${i}">Критерий ${i} A:</label>
            <input type="number" id="fieldA_${i}" class="fieldA">
            <label for="fieldB_${i}">B:</label>
            <input type="number" id="fieldB_${i}" class="fieldB">
            <span>Баллы: <span id="points_${i}">0</span></span>
        `;
        fieldsContainer.appendChild(fieldPair);
    }

    fieldsContainer.addEventListener('input', function() {
        let totalPoints = 0;
        let allFilled = true;

        for (let i = 1; i <= 18; i++) {
            const A = parseFloat(document.getElementById(`fieldA_${i}`).value) || 0;
            const B = parseFloat(document.getElementById(`fieldB_${i}`).value) || 0;
            let points = 0;

            if (A !== 0 && B !== 0) {
                points = (A / B) * 100; // Примерная формула расчёта
            } else {
                allFilled = false;
            }

            document.getElementById(`points_${i}`).textContent = points.toFixed(2);
            totalPoints += points;
        }

        document.getElementById('totalPoints').textContent = totalPoints.toFixed(2);
        saveButton.disabled = !allFilled;
    });

    saveButton.addEventListener('click', function() {
        const totalScore = parseFloat(document.getElementById('totalPoints').textContent);
        fetch('/rating/', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'X-CSRFToken': document.cookie.split('; ').find(row => row.startsWith('csrftoken=')).split('=')[1]
            },
            body: JSON.stringify({ total_score: totalScore })
        })
        .then(response => {
            if (!response.ok) {
                throw new Error('Network response was not ok ' + response.statusText);
            }
            return response.json();
        })
        .then(data => {
            alert('Rating saved successfully!');
        })
        .catch(error => {
            console.error('Error:', error.message);
            alert('Failed to save the rating. Please check the console for more details.');
        });
    });
});