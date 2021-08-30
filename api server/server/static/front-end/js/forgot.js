if (localStorage.getItem('USER_TOKEN')) {
  alert("You have already logged into our service");
  window.location.href = '/';
}



document.querySelector('#button').addEventListener('click', recover_password);

function recover_password() {
  var email = document.querySelector('#email').value,
      emailRegex = /^(([^<>()[\]\\.,;:\s@"]+(\.[^<>()[\]\\.,;:\s@"]+)*)|(".+"))@((\[[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\])|(([a-zA-Z\-0-9]+\.)+[a-zA-Z]{2,}))$/;
  if (!emailRegex.test(email)) {
    alert('Please make sure that your email is valid');
    return;
  }

  var request_obj = {
    url: recoverPasswordUrl,
    type: 'POST',
    data: {email: email}
  }
  $.ajax(request_obj).then((response) => {
    var data = JSON.parse(response);
    if (!data.success) {
      alert("Sorry, we don't have the indicated email");
      return;
    }

    alert("Instructions for recover email was sent in your email");
    window.location.href = '/';
  });
}
