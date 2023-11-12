$(function () {

    let loginError = document.getElementById("loginErrorHidden").value;
    let registerError = document.getElementById("registerErrorHidden").value;
    if (loginError !== "") {
        let loginModal = new bootstrap.Modal(document.getElementById('logInModal'))
        loginModal.show();
    }
    if (registerError !== "") {
        let registerModal = new bootstrap.Modal(document.getElementById('registerModal'))
        registerModal.show();
    }
});