if (localStorage.getItem('USER_TOKEN')) {
  alert("You have already logged into our service");
  window.location.href = '/';
}

const emailRegex = /^(([^<>()[\]\\.,;:\s@"]+(\.[^<>()[\]\\.,;:\s@"]+)*)|(".+"))@((\[[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\])|(([a-zA-Z\-0-9]+\.)+[a-zA-Z]{2,}))$/;
const loginText = document.querySelector(".title-text .login");
const loginForm = document.querySelector("form.login");
const loginBtn = document.querySelector("label.login");
const signupBtn = document.querySelector("label.signup");
const signupLink = document.querySelector("form .signup-link a");
signupBtn.onclick = (()=>{
  loginForm.style.marginLeft = "-50%";
  loginText.style.marginLeft = "-50%";
});
loginBtn.onclick = (()=>{
  loginForm.style.marginLeft = "0%";
  loginText.style.marginLeft = "0%";
});
signupLink.onclick = (()=>{
  signupBtn.click();
  return false;
});


// validate the forms
document.querySelector('#login-button').addEventListener('click', validateLoginForm);
document.querySelector('#sign-up-button').addEventListener('click', validateSignupForm);

function validateLoginForm() {
  var email = document.querySelector('#login-email').value,
      password = document.querySelector('#login-password').value

  if (!password || !email) {
    alert('Please enter the login form!');
    return;
  }
  if (!emailRegex.test(email)) {
    alert('Invalid email please make sure that email right');
    return;
  }
  if (password.length < 7) {
    alert('Password too short');
    return;
  }

  // send request to get the user token if user has
  var request_obj = {
    url: serverLoginUrl,
    type: 'POST',
    data: {email: email, password: password}
  }
  $.ajax(request_obj).then((response) => {
    var data = JSON.parse(response);
    if (!data.token) {
      alert("Sorry, we don't have this user in our services");
      return;
    }

    localStorage.setItem('USER_TOKEN', data.token);
    alert("We found your account, you've successfully logged in into account");
    window.location.href = '/';
  });
}


function validateSignupForm() {
  var email = document.querySelector('#sign-up-email').value,
      password = document.querySelector('#sign-up-password').value,
      passwordAgain = document.querySelector('#sign-up-again-password').value;

  if (password != passwordAgain) {
    alert('Please make sure that you entered the same password twice correctly');
    return;
  }
  if (password < 7) {
    alert('Passwort too short');
    return;
  }
  if (!emailRegex.test(email)) {
    alert('Invalid email please make sure that email right');
    return;
  }

  var request_obj = {
    url: serverSignupUrl,
    type: 'POST',
    data: {email: email, password: password}
  }

  $.ajax(request_obj).then((response) => {
    var data = JSON.parse(response);
    if (data.token == '') {
      alert('User with this email has already in our services, please try another email to sign up');
      return;
    }

    localStorage.setItem('USER_TOKEN', data.token);
    alert('User successfully registered, we sent to your email the activator link of your email to confirm account');
    window.location.href = '/';
  });
}
