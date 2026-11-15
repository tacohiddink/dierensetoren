// Mobiel menu
(function () {
  var btn = document.querySelector('.menu-toggle');
  var nav = document.getElementById('nav');
  if (!btn || !nav) return;
  btn.addEventListener('click', function () {
    var open = nav.classList.toggle('open');
    btn.setAttribute('aria-expanded', open ? 'true' : 'false');
  });
  document.addEventListener('keydown', function (e) {
    if (e.key === 'Escape' && nav.classList.contains('open')) {
      nav.classList.remove('open');
      btn.setAttribute('aria-expanded', 'false');
      btn.focus();
    }
  });
})();

// Tijdlijn op de geschiedenispagina
(function () {
  var tl = document.querySelector('[data-tl]');
  if (!tl) return;
  var track = tl.querySelector('.tl-track');
  var slides = tl.querySelectorAll('.tl-slide');
  var years = tl.querySelectorAll('.tl-years a');
  var prev = tl.querySelector('.tl-prev');
  var next = tl.querySelector('.tl-next');
  var count = tl.querySelector('.tl-count');
  var current = 0;

  function go(i) {
    i = Math.max(0, Math.min(slides.length - 1, i));
    track.scrollTo({ left: i * track.clientWidth });
    show(i);
  }

  function show(i) {
    current = i;
    years.forEach(function (a, n) {
      if (n === i) {
        a.setAttribute('aria-current', 'true');
        var bar = a.closest('.tl-years');
        var r = a.getBoundingClientRect(), b = bar.getBoundingClientRect();
        bar.scrollTo({ left: bar.scrollLeft + r.left - b.left - (b.width - r.width) / 2, behavior: 'smooth' });
      } else {
        a.removeAttribute('aria-current');
      }
    });
    prev.disabled = i === 0;
    next.disabled = i === slides.length - 1;
    count.textContent = (i + 1) + ' / ' + slides.length;
  }

  years.forEach(function (a, n) {
    a.addEventListener('click', function (e) { e.preventDefault(); go(n); });
  });
  prev.addEventListener('click', function () { go(current - 1); });
  next.addEventListener('click', function () { go(current + 1); });
  track.addEventListener('keydown', function (e) {
    if (e.key === 'ArrowLeft') { e.preventDefault(); go(current - 1); }
    if (e.key === 'ArrowRight') { e.preventDefault(); go(current + 1); }
  });
  // Na handmatig vegen of scrollen de actieve dia bijwerken
  var settle;
  track.addEventListener('scroll', function () {
    clearTimeout(settle);
    settle = setTimeout(function () {
      var i = Math.round(track.scrollLeft / track.clientWidth);
      if (i !== current) show(i);
    }, 120);
  }, { passive: true });
  window.addEventListener('resize', function () { go(current); });

  tl.classList.add('is-ready');
  show(0);
})();
