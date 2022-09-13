// before loading the page, check if it has the password
var flipbookId = new URL(window.location.href).searchParams.get('id'),
    defaultColor = "#0000ff",
    color,
    text_pages = [],
    pages_links = [],
    scale = 1;


const button = document.getElementById("fullscreen");
const customise=document.getElementById("customise");
const share= document.getElementsByClassName("at-expanding-share-button-toggle-bg");
const Book=document.getElementById("bookcontainer");
const brandBlock = document.querySelector('#brand');
const externalFileBlock = document.querySelector('#external-file');
const pageWrapper = document.querySelector('.b-load');
const viewsBlock = document.querySelector('.views-block > span');
const bookPages = document.querySelector('.book-pages');
const bookLinks = document.querySelector('.pages-links');
const searchInput = document.querySelector('#search_input');
const logoImage = document.querySelector('#logotype-block > img');


if (!flipbookId) {
  alert('Please enter the id of flipbook');
  window.location.href = '/';
}


$.ajax({
  url: hasFlipBook,
  type: 'POST',
  data: {flipbookId: flipbookId},
  success: (r) => {
    var data = JSON.parse(r);
    if (!data.has) {
      alert('Sorry, we don\'t have the requested flipbook');
      window.location.href = '/';
    }

    start_preload_page();
  }
});

function start_preload_page() {
  $.ajax({
    url: flipBookPassword,
    type: 'POST',
    data: {flipbookId: flipbookId},
    success: function (res) {
      res = JSON.parse(res);
      if (!res) {
        alert("Our service not available for now, please try again throught time");
        return;
      }

      if (res.has_password) requestPassword();
      else loadFlipBook('', flipbookId);
    }
  });
}



function requestPassword() {
  var password = prompt("The author setted the password for this flipbook! Please enter the password", "");
  $.ajax({
    url: flipBookCheckPassword,
    type: 'POST',
    data: {password: password, flipbookId: flipbookId},
    success: function(r) {
      r = JSON.parse(r);
      if (r.password_right == true) loadFlipBook(password, flipbookId);
      else requestPassword();
    }
  });
}


function loadFlipBook(password, id) {
  $.ajax({
    url: getFlipBook,
    type: 'POST',
    data: {flipBookId: id, password: password},
    success: function(data) {
      data = JSON.parse(data);
      if (!data) {
        alert("Flip Book not available now, please try again throught time");
        window.location.href = '/';
      }


      if (data.disable_right_click == "true") document.addEventListener('contextmenu', disableRightClick);
      // show data
      text_pages = data.text_pages;
      viewsBlock.innerHTML = `Views: ${data.views}`;
      brandBlock.innerHTML = data.brand;
      logoImage.src = data.logotype;
      externalFileBlock.setAttribute('href', data.external_file_link);
      if (data.external_file_link == '') externalFileBlock.style.display = 'none';

      for (let image_src of data.images) pageWrapper.innerHTML += `<div class="content"><img src="${image_src}" alt='page'></div>`;
      for (var i = 0; i < data.images.length; i++) bookPages.innerHTML += `<div class="page"><span> ${(i + 1)} </span></div>`;

      // show the links for each page
      pages_links = data.links;
      bookLinks.style.display = 'none';
      for (var page_count = 0; page_count < pages_links.length; page_count++) {
        page_links = pages_links[page_count];
        if (page_links.length == 0) continue;

        page_content = document.createElement('div');
        page_content.classList.add('page-content');
        page_content.innerHTML += `<div class="page-title"> Page ${(page_count + 1)} </div>`;
        for (i = 0; i < page_links.length; i++) page_content.innerHTML += `<div>Link ${(i + 1)}: ${page_links[i]} </div>`;
        bookLinks.append(page_content);
        bookLinks.style.display = 'block';
      }

    loadPage();
    }
  });
}


function loadPage() {
  $(function () {
      var $mybook = $('#mybook');
      var $bttn_next = $('#next_page_button');
      var $bttn_prev = $('#prev_page_button');
      var $loading = $('#loading');
      var $mybook_images = $mybook.find('img');
      var cnt_images = $mybook_images.length;
      var loaded = 0;

      $mybook_images.each(function () {
          var $img = $(this);
          var source = $img.attr('src');
          $('<img/>').load(function () {
              ++loaded;
              if (loaded == cnt_images) {
                  $loading.hide();
                  $bttn_next.show();
                  $bttn_prev.show();
                  $mybook.show().booklet({
                      name: null,
                      width: 900,
                      height: 600,
                      speed: 600,
                      direction: 'LTR',

                      next: $bttn_next,
                      prev: $bttn_prev,
                  });
              }
          }).attr('src', source);
      });

  });

  //full screen toggle

  if (!Element.prototype.requestFullscreen) {
  	Element.prototype.requestFullscreen = Element.prototype.mozRequestFullscreen || Element.prototype.webkitRequestFullscreen || Element.prototype.msRequestFullscreen;
  }


  if (!document.exitFullscreen) {
  	document.exitFullscreen = document.mozExitFullscreen || document.webkitExitFullscreen || document.msExitFullscreen;
      customise.style.display="block";
  }

  if (!document.fullscreenElement) {

  	Object.defineProperty(document, 'fullscreenElement', {
  		get: function() {
  			return document.mozFullScreenElement || document.msFullscreenElement || document.webkitFullscreenElement;
  		}
  	});

  	Object.defineProperty(document, 'fullscreenEnabled', {
  		get: function() {
  			return document.mozFullScreenEnabled || document.msFullscreenEnabled || document.webkitFullscreenEnabled;
  		}
  	});
  }

  document.addEventListener('click', function (event) {
  	if (!event.target.hasAttribute('data-toggle-fullscreen')) return;

  	if (document.fullscreenElement) {
  		document.exitFullscreen();
          button.innerText="Toggle Fullscreen";
  	} else {
  		document.documentElement.requestFullscreen();
  	}

  }, false);

  //hide customize box on fullscreen

  document.addEventListener("fullscreenchange",(e)=>{
      if (document.fullscreenElement) {
          customise.style.display="none";
          share[0].style.display="none";
        } else {
          customise.style.display="flex";
          share[0].style.display="block";
        }
  });


  startup();


  searchInput.addEventListener('input', find_phrase);

}

function startup() {
  color = document.querySelector("#color");
  color.value = defaultColor;
  color.addEventListener("input", updateFirst, false);
}
function updateFirst(event) {
  var body = document.body;
  if (body) {
    body.style.backgroundColor = event.target.value;
  }
}


function myZoomIn(){
  if (scale < 3.2) scale += .3;
  Book.style.transform=`scale(${scale})`;
}
function myZoomOut(){
  if (scale > 1) scale -= .3;
  Book.style.transform=`scale(${scale})`;
}
//sound on page swipe
function pageSound(){
  document.getElementById("page").play();
}

function disableRightClick(e) {
  e.preventDefault();
}


function find_phrase(e) {
  document.querySelectorAll(`#bookcontainer > div.book-pages > div`).forEach((item) => item.classList.remove('active'));

  var phrase = e.target.value.toLowerCase();
  if (phrase.length < 4 || text_pages.length == 0) return;

  // find phrase in pages
  for (var i = 0; i < text_pages.length; i++) {
    text = text_pages[i].toLowerCase()
    // if page has phrase highlight page
    if (text.includes(phrase)) document.querySelector(`#bookcontainer > div.book-pages > div:nth-child(${(i + 1)})`).classList.add('active');
  }
}

document.querySelector('#get-html-block').addEventListener('click', function() {
  var input = document.createElement('input');
  var link = window.location.href;
  input.value = `<iframe src='${link}' width='1920' height='1080' title='Flip book page'></iframe>`;
  document.body.append(input);
  input.select();
  document.execCommand('copy');
  input.remove();
  alert('The embed code copied into your clipboard');
});
