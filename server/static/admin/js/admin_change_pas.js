document.querySelector('#sub').onclick = function() {
  form = document.querySelector('.form');
  if (form.new_password.value == form.repeat_password.value) form.submit()
  else alert('Please make sure that password the same in both input')
}
