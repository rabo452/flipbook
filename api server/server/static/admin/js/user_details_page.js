import 'https://code.jquery.com/jquery-3.6.0.min.js';
import 'https://cdn.jsdelivr.net/npm/slick-carousel@1.8.1/slick/slick.min.js';


$('.slider-block').slick({
  arrows: false,
  slidesToShow: 3,
  slidesToScroll: 3,
});

$('#delete_button').on('click', function() {
  var agree = confirm('Delete this user? (with all flip books and files)'),
      user_id = document.querySelector('#delete_button').getAttribute('user-id');

  if (!agree) return;

  var request_obj = {
    url: '/delete-user',
    type: 'POST',
    data: {user_id: user_id}
  }

  $.ajax(request_obj).then(() => {
    alert('User was successfully deleted');
    window.location.href = '/administrator';
  });

});

document.querySelectorAll('.delete-flip-book').forEach((item) => {
  item.addEventListener('click', (e) => {
    var id = e.target.getAttribute('flip-book-id'),
        directory_id = e.target.getAttribute('flip-book-directory-id');
    var agree = confirm('Delete this flip book? (with all flip book files)');

    if (!agree) return;

    var request_obj = {
      url: '/flip-book-delete',
      type: 'POST',
      data: {flip_book_id: id, directory_id: directory_id}
    }

    $.ajax(request_obj).then(() => {
      alert('Flip book was deleted');
      window.location.reload();
    });

  });
});
