(function () {
  var email = new URL(window.location.href).searchParams.get('email');
  var mailRegex = /^(([^<>()[\]\\.,;:\s@"]+(\.[^<>()[\]\\.,;:\s@"]+)*)|(".+"))@((\[[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\])|(([a-zA-Z\-0-9]+\.)+[a-zA-Z]{2,}))$/;
  var token = localStorage.getItem('USER_TOKEN');

  if (!mailRegex.test(email)) {
    alert("Sorry, we can't activate account without email");
    return;
  }

  if (!token) {
    alert("Sorry, before activate account please login into service");
    return;
  }

  var request_obj = {
    type: 'POST',
    url: serverActivateAccountUrl,
    data: {token: token, email: email}
  }
  $.ajax(request_obj).then((r) => {
    var data = JSON.parse(r);
    if (data.success == false) {
      alert("We can't proccess this account, please make sure that you logged into our service");
      return;
    }

    alert("Your account has been successfully activated");
    window.location.href = '/';
  });

})();
