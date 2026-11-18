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

// Vergrote foto's in de galerij
(function () {
  var links = document.querySelectorAll('a[data-lightbox]');
  if (!links.length || typeof HTMLDialogElement !== 'function') return;
  var icon = function (d) {
    return '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="' + d + '"/></svg>';
  };
  var dlg = document.createElement('dialog');
  dlg.className = 'lightbox';
  dlg.setAttribute('aria-label', 'Vergrote foto');
  dlg.innerHTML =
    '<figure><picture><source type="image/avif"><img alt=""></picture><figcaption></figcaption></figure>' +
    '<button class="lb-close" type="button" aria-label="Sluiten">' + icon('M18 6 6 18M6 6l12 12') + '</button>' +
    '<button class="lb-prev" type="button" aria-label="Vorige foto">' + icon('m15 18-6-6 6-6') + '</button>' +
    '<button class="lb-next" type="button" aria-label="Volgende foto">' + icon('m9 18 6-6-6-6') + '</button>';
  document.body.appendChild(dlg);
  var img = dlg.querySelector('img');
  var avif = dlg.querySelector('source');
  var cap = dlg.querySelector('figcaption');
  var current = 0;

  function show(i) {
    current = (i + links.length) % links.length;
    var thumb = links[current].querySelector('img');
    var groot = links[current].getAttribute('href');
    // AVIF is veel kleiner; de JPG blijft de terugval voor oudere browsers
    avif.srcset = groot.replace(/\.jpg(\?|$)/, '.avif$1');
    img.src = groot;
    img.alt = thumb.alt;
    cap.textContent = thumb.alt + ' (' + (current + 1) + ' / ' + links.length + ')';
  }

  links.forEach(function (a, n) {
    a.addEventListener('click', function (e) {
      e.preventDefault();
      show(n);
      dlg.showModal();
    });
  });
  dlg.querySelector('.lb-close').addEventListener('click', function () { dlg.close(); });
  dlg.querySelector('.lb-prev').addEventListener('click', function () { show(current - 1); });
  dlg.querySelector('.lb-next').addEventListener('click', function () { show(current + 1); });
  // Klik naast de foto sluit
  dlg.addEventListener('click', function (e) {
    if (e.target === dlg || e.target.tagName === 'FIGURE') dlg.close();
  });
  dlg.addEventListener('keydown', function (e) {
    if (e.key === 'ArrowLeft') show(current - 1);
    if (e.key === 'ArrowRight') show(current + 1);
  });
  dlg.addEventListener('close', function () { links[current].focus(); });
})();

// Google Maps pas laden na toestemming (klik)
(function () {
  var box = document.querySelector('.map-consent');
  if (!box) return;
  box.querySelector('button').addEventListener('click', function () {
    var frame = document.createElement('iframe');
    frame.src = box.getAttribute('data-map-src');
    frame.title = box.getAttribute('data-map-title');
    frame.height = 460;
    frame.setAttribute('allowfullscreen', '');
    box.innerHTML = '';
    box.appendChild(frame);
    box.classList.add('is-loaded');
    frame.focus();
  });
})();
