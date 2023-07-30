signUpButton = document.getElementById('sign-up-button');
backToLogin = document.getElementById('back-to-login');
loginContainer =document.getElementById('login-container');
createAccountContainer = document.getElementById('create-account-container');

signUpButton.addEventListener('click', e => {
    loginContainer.classList.add('hidden');
    createAccountContainer.classList.remove('hidden')
});

backToLogin.addEventListener('click', e => {
    loginContainer.classList.remove('hidden');
    createAccountContainer.classList.add('hidden')
})