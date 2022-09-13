import 'https://code.jquery.com/jquery-3.6.0.min.js';

$('#submit').on('click', () => {
  var username = document.querySelector('#username').value,
      password = document.querySelector('#password').value,
      password_again = document.querySelector('#username_again').value,
      email_regex = /^(([^<>()[\]\\.,;:\s@"]+(\.[^<>()[\]\\.,;:\s@"]+)*)|(".+"))@((\[[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\])|(([a-zA-Z\-0-9]+\.)+[a-zA-Z]{2,}))$/;;

  if (!username || password != password_again) {
    alert('Please make sure that you entered all fields right');
    return;
  }

  if (username.length < 7 || password.length < 7) {
    alert("The username or password too short");
    return;
  }
  if (!email_regex.test(username)) {
    alert('Please make sure that this email is valid');
    return;
  }

  var request_obj = {
    url: '/admin-create-user',
    type: 'POST',
    data: {'username': username, 'password': password}
  }

  $.ajax(request_obj).then( (data) => {
    if (JSON.parse(data).token == '') alert("This username has already, user didn't registered")
    else alert('User successfully registered')
    window.location.href = '/administrator';
  })

});
