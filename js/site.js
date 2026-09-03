// Imagination PR — small enhancements only. The site works without JavaScript.
(function () {
  var toggle = document.querySelector('.menu-toggle');
  var nav = document.getElementById('mobile-nav');
  if (toggle && nav) {
    toggle.addEventListener('click', function () {
      var open = toggle.getAttribute('aria-expanded') === 'true';
      toggle.setAttribute('aria-expanded', String(!open));
      nav.hidden = open;
      toggle.querySelector('.menu-label').textContent = open ? 'Menu' : 'Close';
    });
  }
})();
