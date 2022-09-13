var supported_file_types = ['image/jpeg', 'image/png', 'image/jpg', 'application/vnd.openxmlformats-officedocument.wordprocessingml.document', 'application/pdf'];
var images_types = ['image/jpeg', 'image/png', 'image/jpg'];

// navbar function
function myFunction() {
    const hmenu = document.querySelector(".navlinks");
    hmenu.classList.toggle("responsive")
}

// display or hide log out button
if (localStorage.getItem('USER_TOKEN')) {
  document.querySelector('#log-out').addEventListener('click', () => {
    document.querySelector('#myTopnav > div.navlinks > div:nth-child(3) > a').style.display = 'none';
    localStorage.removeItem('USER_TOKEN');
    window.location.reload();
  });
}else document.querySelector('#log-out').style.display = 'none';


//file input
const realFileBtn = document.getElementById("real-file");
const customBtn = document.getElementById("custom-button");
const customTxt = document.getElementById("custom-text");
const button = document.getElementById("button");
const loading = document.getElementById("wrapperloading");
const passwordInput = document.querySelector('#password-input');
const brandInput = document.querySelector('#input-brand-name');
const googleDocsInput = document.querySelector('#google-docs-link');
const logoUploadBtn = document.querySelector('.logo-upload-btn');
const realUploadBtn = document.querySelector('#real-logo-file');
const logoUploadText = document.querySelector('.logo-upload-text');


customBtn.addEventListener("click", () => realFileBtn.click());
logoUploadBtn.addEventListener('click', () => realUploadBtn.click());

realFileBtn.addEventListener("change", function () {
    if (realFileBtn.value) customTxt.innerHTML = 'File has been chosen';
    else customTxt.innerHTML = "No file chosen, yet.";
    console.log(realFileBtn.files);
});

realUploadBtn.addEventListener('change', function () {
  if (realUploadBtn.value) logoUploadText.innerHTML = 'File has been chosen';
  else logoUploadText.innerHTML = 'No file chosen, yet.';
});


document.querySelector('#flipbook-password').checked = false;
document.querySelector('#access-users').checked = false;
document.querySelector('#right-click-user').checked = false;

var flipbook_password = false,
    access_download_file = false,
    disable_right_click = false;

document.querySelector('#flipbook-password').addEventListener('click', () => {
  //hide or show password input
  flipbook_password = !flipbook_password;
  if (flipbook_password) document.querySelector('.password-field').style.display = 'block';
  else document.querySelector('.password-field').style.display = 'none';
});

document.querySelector('#access-users').addEventListener('click', () => access_download_file = !access_download_file);
document.querySelector('#right-click-user').addEventListener('click', () => disable_right_click = !disable_right_click)







button.addEventListener("click", activeLoad);
function activeLoad() {
  var password = passwordInput.value,
      brand = brandInput.value,
      google_docs_link = googleDocsInput.value,
      token = localStorage.getItem('USER_TOKEN');

  if (!token) {
    alert('Only registered users can upload files');
    return;
  }
  if (brand.length < 6) {
    alert('Brand name can\'t be less than 6 symbols');
    return;
  }

  if (realFileBtn.files.length == 0 && google_docs_link.length == 0) {
    alert('Please upload file or indicate the google docs link for uploading flip book!');
    return;
  }

  if (flipbook_password && password.length < 7) {
    alert("Password for flipbook can't be less than 7 symbols!");
    return;
  }

  if (realUploadBtn.files.length == 0) {
    alert('Please upload the logotype for flipbook');
    return;
  }

  if (realFileBtn.files.length != 0) {
    var file = realFileBtn.files[0];
    var supported_type = false;
    for (let file_type of supported_file_types) if (file.type == file_type) supported_type = true;
    if (!supported_type) {
      alert('Please upload the file with supported file type');
      return;
    }

    var data = new FormData();
    data.append('file', file);
    data.append('google_docs', '');
  }else if (google_docs_link.length != 0) {
    if (!google_docs_link.includes('https://docs.google.com/document/d')) {
      alert('Please make sure that you indicated valid google docs link');
      return;
    }

    var data = new FormData();
    data.append('google_docs', google_docs_link);
  }


  data.append('logo', realUploadBtn.files[0]);
  data.append('token', token);
  data.append('flip_book_password', password);
  data.append('external_download', access_download_file);
  data.append('brand', brand);
  data.append('disable_right_click', `${disable_right_click}`);

  loading.classList.toggle("loadingactive");
  $.ajax({
    url: registerFlipBook,
    type: 'POST',
    data: data,
    processData: false,
    contentType: false
  }).then((res) => {
    res = JSON.parse(res);
    page_id = res['page_id'];
    if (!page_id) {
      alert("please make sure that uploaded file was valid or your account didn't activated");
      window.location.reload();
      return;
    }
    window.location.href = '/flipbook?id=' + page_id;
  });

}

//
