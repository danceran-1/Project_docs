document.addEventListener('DOMContentLoaded', function() {
    const passInput = document.getElementById('password');
    const confirmInput = document.getElementById('confirm_password');
    const toggleBtn = document.getElementById('togglePass');
    let visible = false;

    toggleBtn.addEventListener('click', function() {
        visible = !visible;
        passInput.type = visible ? 'text' : 'password';
        confirmInput.type = visible ? 'text' : 'password';
        toggleBtn.src = visible
            ? "/static/main/VisiblePass.png"
            : "/static/main/UnvisiblePass.png";
    });
});
