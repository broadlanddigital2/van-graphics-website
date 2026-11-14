const mobileMenu = document.querySelector('.mobile');
mobileMenu.addEventListener('click', (event) => {
  if (event.target.closest('a')) mobileMenu.open = false;
});
document.addEventListener('keydown', (event) => {
  if (event.key === 'Escape' && mobileMenu.open) {
    mobileMenu.open = false;
    mobileMenu.querySelector('summary').focus();
  }
});

const galleryFilter = document.querySelector('#gallery-model');
if (galleryFilter) {
  const designs = [...document.querySelectorAll('.core-gallery figure')];
  const count = document.querySelector('#gallery-count');
  const updateGallery = () => {
    let visible = 0;
    for (const design of designs) {
      design.hidden = Boolean(galleryFilter.value && design.dataset.model !== galleryFilter.value);
      if (!design.hidden) visible += 1;
    }
    count.textContent = visible === 1 ? '1 design' : `${visible} designs`;
  };
  galleryFilter.addEventListener('change', updateGallery);
  updateGallery();
}

document.querySelectorAll('#service-enquiry, .js-enquiry').forEach((enquiry) => {
  const crm = document.body.dataset;
  enquiry.addEventListener('submit', async (event) => {
    event.preventDefault();
    const values = new FormData(enquiry);
    if (values.get('package') || values.get('size')) {
      values.set('details', [values.get('package') && `Package: ${values.get('package')}`, values.get('size') && `Van size: ${values.get('size')}`, values.get('details')].filter(Boolean).join('\n'));
    }
    const subject = ['Vehicle graphics enquiry', values.get('service'), enquiry.dataset.context]
      .filter(Boolean).join(' – ');
    const fields = [
      `Service: ${values.get('service')}`,
      `Name: ${values.get('name')}`,
      `Email: ${values.get('email')}`,
      values.get('phone') && `Phone: ${values.get('phone')}`,
      values.get('vehicle') && `Vehicle: ${values.get('vehicle')}`,
      values.get('postcode') && `Postcode: ${values.get('postcode')}`,
    ].filter(Boolean);
    const body = [...fields, '', values.get('details')].join('\r\n');
    const status = enquiry.querySelector('[role=status]');
    const button = enquiry.querySelector('button[type=submit]');
    status.hidden = false;
    if (crm.crmEndpoint && crm.crmKey && crm.crmSecret) {
      button.disabled = true;
      status.textContent = 'Sending your enquiry…';
      let source = {};
      try { source = JSON.parse(localStorage.getItem('nvg_source') || '{}'); } catch (e) {}
      try {
        const response = await fetch(crm.crmEndpoint, {
          method: 'POST',
          headers: { 'content-type': 'application/json', 'x-rcg-channel-key': crm.crmKey, 'x-rcg-channel-secret': crm.crmSecret },
          body: JSON.stringify({
            name: values.get('name'), email: values.get('email'), phone: values.get('phone') || '',
            subject, message: [values.get('vehicle') && `Vehicle: ${values.get('vehicle')}`, values.get('postcode') && `Postcode: ${values.get('postcode')}`, `Service: ${values.get('service')}`, '', values.get('details')].filter((x) => x !== null && x !== false).join('\n'),
            source_url: location.href, utm_source: source.utm_source || '', utm_medium: source.utm_medium || '', utm_campaign: source.utm_campaign || '', gclid: source.gclid || '',
          }),
        });
        if (response.ok) {
          enquiry.reset();
          status.textContent = 'Thanks – your enquiry has reached the Norwich team. We will reply as soon as we can.';
          try { (window.dataLayer = window.dataLayer || []).push({ event: 'enquiry_submitted', service: values.get('service') }); } catch (e) {}
          button.disabled = false;
          return;
        }
      } catch (e) {}
      button.disabled = false;
    }
    status.textContent = 'Your email app should open with the draft. If it does not, use the web enquiry form.';
    window.location.href = `mailto:${enquiry.dataset.recipient}?subject=${encodeURIComponent(subject)}&body=${encodeURIComponent(body)}`;
  });
});

(function captureSource() {
  try {
    const q = new URLSearchParams(location.search), keep = {};
    ['utm_source', 'utm_medium', 'utm_campaign', 'gclid'].forEach((k) => { if (q.get(k)) keep[k] = q.get(k); });
    if (Object.keys(keep).length) localStorage.setItem('nvg_source', JSON.stringify(keep));
  } catch (e) {}
})();

document.querySelectorAll('#service-enquiry, .js-enquiry').forEach((f) => { const b = f.querySelector('button[type=submit]'); if (b) b.disabled = false; });

const roadReveal = document.querySelector('#road-reveal');
if (roadReveal) {
  const render = roadReveal.closest('.road-render');
  const stage = render.closest('.road-stage');
  const progress = stage.querySelector('[data-wrap-progress]');

  function updateRoadReveal() {
    const value = Number(roadReveal.value);
    stage.style.setProperty('--road-reveal', `${value}%`);
    progress.textContent = `${value}%`;
    roadReveal.setAttribute('aria-valuetext', value === 0 ? 'Plain van' : value === 100 ? 'Full wrap' : `${value}% of the wrap revealed`);
  }

  roadReveal.addEventListener('input', updateRoadReveal);
  updateRoadReveal();
  stage.querySelectorAll('[data-reveal]').forEach((button) => {
    button.addEventListener('click', () => {
      roadReveal.value = button.dataset.reveal;
      updateRoadReveal();
    });
  });
}

const roadViews = document.querySelector('.road-views');
if (roadViews) {
  const stage = roadViews.closest('.road-stage');
  const views = [...roadViews.querySelectorAll('[data-road-view]')];
  const turntable = stage.querySelector('.road-turntable');
  const turnImage = turntable.querySelector('img');
  const counter = stage.querySelector('[data-road-angle]');
  const spinButton = stage.querySelector('[data-spin]');
  const angles = [
    'Front view',
    'Front three-quarter view, nose to the right',
    'Side profile, nose to the right',
    'Rear three-quarter view, rear doors to the left',
    'Rear view',
    'Rear three-quarter view, rear doors to the right',
    'Side profile, nose to the left',
    'Front three-quarter view, nose to the left',
  ];
  const frameIds = JSON.parse(turntable.dataset.frames);
  const frames = frameIds.map((id) => `/assets/transit-custom-msrt-spin-${id}.webp`);
  let angle = frameIds.indexOf('1');
  let drag = null;
  let frameCache = null;
  let spin = null;

  function showAngle(index) {
    const next = (index + frames.length) % frames.length;
    if (next === angle) return;
    angle = next;
    turnImage.src = frames[angle];
    const [view, intermediate] = frameIds[angle].split('-');
    turnImage.alt = intermediate
      ? `Between ${angles[Number(view)].toLowerCase()} and ${angles[(Number(view) + 1) % angles.length].toLowerCase()}`
      : angles[Number(view)];
    counter.textContent = `${angle + 1} / ${frames.length}`;
  }

  function stopSpin() {
    window.clearInterval(spin);
    spin = null;
    spinButton.textContent = 'Play full turn';
    spinButton.setAttribute('aria-pressed', 'false');
  }

  spinButton.addEventListener('click', () => {
    if (spin !== null) {
      stopSpin();
      return;
    }
    let remaining = frames.length;
    spinButton.textContent = 'Stop rotation';
    spinButton.setAttribute('aria-pressed', 'true');
    spin = window.setInterval(() => {
      showAngle(angle + 1);
      remaining -= 1;
      if (!remaining) stopSpin();
    }, 2600 / frames.length);
  });

  views.forEach((view) => {
    view.addEventListener('click', () => {
      if (view.dataset.roadView !== 'rotate') stopSpin();
      views.forEach((control) => {
        const active = control === view;
        control.setAttribute('aria-pressed', String(active));
        document.getElementById(control.getAttribute('aria-controls')).hidden = !active;
      });
      if (view.dataset.roadView === 'rotate' && !frameCache) {
        frameCache = frames.map((src) => {
          const image = new Image();
          image.src = src;
          return image;
        });
      }
    });
  });

  stage.querySelectorAll('[data-rotate]').forEach((button) => {
    button.addEventListener('click', () => {
      stopSpin();
      showAngle(angle + Number(button.dataset.rotate));
    });
  });
  turntable.addEventListener('keydown', (event) => {
    if (event.key !== 'ArrowLeft' && event.key !== 'ArrowRight') return;
    event.preventDefault();
    stopSpin();
    showAngle(angle + (event.key === 'ArrowRight' ? 1 : -1));
  });
  turntable.addEventListener('pointerdown', (event) => {
    if (event.button !== 0 || !event.isPrimary) return;
    stopSpin();
    drag = { pointer: event.pointerId, startX: event.clientX, angle };
    turntable.setPointerCapture(event.pointerId);
  });
  turntable.addEventListener('pointermove', (event) => {
    if (drag?.pointer !== event.pointerId) return;
    const step = Math.max(7, turntable.clientWidth / (frames.length * 1.35));
    showAngle(drag.angle + Math.round((event.clientX - drag.startX) / step) % frames.length);
  });
  turntable.addEventListener('lostpointercapture', () => { drag = null; });
}

// Sticky header: add a shadow and a slimmer bar once the page has scrolled past the utility strip.
(function stickyHeader() {
  const head = document.querySelector('.main-head');
  if (!head) return;
  const update = () => head.classList.toggle('is-stuck', window.scrollY > 34);
  window.addEventListener('scroll', update, { passive: true });
  update();
})();
;(function(){
  var tiles=[].slice.call(document.querySelectorAll('.work-tile')); if(!tiles.length) return;
  var box=document.createElement('div'); box.className='lightbox'; box.hidden=true; box.setAttribute('role','dialog'); box.setAttribute('aria-modal','true');
  box.innerHTML='<img alt=""><p></p><button class="lb-close" aria-label="Close">×</button><button class="lb-prev" aria-label="Previous">‹</button><button class="lb-next" aria-label="Next">›</button>';
  document.body.appendChild(box);
  var img=box.querySelector('img'), cap=box.querySelector('p'), group=[], i=0;
  function show(n){ i=(n+group.length)%group.length; var t=group[i]; img.src=t.href; img.alt=t.querySelector('img').alt; cap.textContent=t.dataset.caption||''; }
  function close(){ box.hidden=true; document.body.style.overflow=''; }
  tiles.forEach(function(t){ t.addEventListener('click',function(e){ e.preventDefault(); group=[].slice.call(t.closest('.work-grid').querySelectorAll('.work-tile')); show(group.indexOf(t)); box.hidden=false; document.body.style.overflow='hidden'; box.querySelector('.lb-close').focus(); }); });
  box.querySelector('.lb-close').onclick=close; box.querySelector('.lb-prev').onclick=function(){show(i-1)}; box.querySelector('.lb-next').onclick=function(){show(i+1)};
  box.addEventListener('click',function(e){ if(e.target===box) close(); });
  document.addEventListener('keydown',function(e){ if(box.hidden) return; if(e.key==='Escape') close(); if(e.key==='ArrowLeft') show(i-1); if(e.key==='ArrowRight') show(i+1); });
})();

/* Home banner slider: 4 banners, auto-advances, pauses on hover/focus, dots to jump */
(function(){
  var root=document.querySelector('.home-slider'); if(!root) return;
  var copies=root.querySelectorAll('.slide-copy'), imgs=root.querySelectorAll('.slide-img'), dots=root.querySelectorAll('.slide-dot');
  var n=copies.length, cur=0, ms=6500, timer=null, paused=false;
  var reduce=window.matchMedia&&window.matchMedia('(prefers-reduced-motion: reduce)').matches;
  root.style.setProperty('--slide-ms', ms+'ms');
  function show(i){
    cur=(i+n)%n;
    [copies,imgs,dots].forEach(function(list){list.forEach(function(el,k){el.classList.toggle('is-active',k===cur);});});
    copies.forEach(function(el,k){ if(k===cur){el.removeAttribute('aria-hidden');} else {el.setAttribute('aria-hidden','true');} el.querySelectorAll('a').forEach(function(a){a.tabIndex=k===cur?0:-1;}); });
    dots.forEach(function(d,k){ if(k===cur) d.setAttribute('aria-current','true'); else d.removeAttribute('aria-current'); });
    var img=imgs[cur]; if(img && img.loading==='lazy') img.loading='eager';
    schedule();
  }
  function schedule(){ clearTimeout(timer); if(!paused && !reduce) timer=setTimeout(function(){show(cur+1);}, ms); }
  dots.forEach(function(d){ d.addEventListener('click', function(){ show(+d.dataset.go); }); });
  root.addEventListener('mouseenter', function(){ paused=true; root.classList.add('is-paused'); clearTimeout(timer); });
  root.addEventListener('mouseleave', function(){ paused=false; root.classList.remove('is-paused'); show(cur); });
  root.addEventListener('focusin', function(){ paused=true; root.classList.add('is-paused'); clearTimeout(timer); });
  root.addEventListener('focusout', function(){ paused=false; root.classList.remove('is-paused'); schedule(); });
  document.addEventListener('visibilitychange', function(){ if(document.hidden) clearTimeout(timer); else schedule(); });
  copies.forEach(function(el,k){ if(k) el.querySelectorAll('a').forEach(function(a){a.tabIndex=-1;}); });
  imgs.forEach(function(img,k){ if(k) setTimeout(function(){ img.loading='eager'; }, 1500); });
  schedule();
})();

/* Price matrix: choosing a price fills the quick quote form */
document.querySelectorAll('.pm-pick').forEach((btn) => {
  btn.addEventListener('click', () => {
    const wrap = btn.closest('section') || document;
    const form = wrap.querySelector('.price-quote'); if (!form) return;
    const set = (name, val) => { const sel = form.querySelector(`[name=${name}]`); if (!sel) return; [...sel.options].forEach((o) => { if (o.text === val) sel.value = o.value || o.text; }); };
    set('package', btn.dataset.package); set('size', btn.dataset.size);
    wrap.querySelectorAll('.pm-pick.is-picked').forEach((b) => b.classList.remove('is-picked')); btn.classList.add('is-picked');
    form.scrollIntoView({ behavior: 'smooth', block: 'center' });
    setTimeout(() => form.querySelector('[name=name]').focus({ preventScroll: true }), 500);
  });
});
