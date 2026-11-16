const mobileMenu = document.querySelector('.mobile');
if (mobileMenu) {
  const mm = mobileMenu.querySelector('.mm');
  const root = mm.querySelector('.mm-root');
  const show = (panel) => {
    for (const p of mm.querySelectorAll('.mm-panel:not(.mm-root)')) p.hidden = p !== panel;
    mm.classList.toggle('is-sub', Boolean(panel));
    const target = panel || root;
    target.scrollTop = 0;
    const focus = panel ? panel.querySelector('.mm-back') : null;
    if (focus) setTimeout(() => focus.focus({ preventScroll: true }), 260);
  };
  const place = () => {
    const head = document.querySelector('.main-head');
    mm.style.setProperty('--mm-top', Math.max(0, Math.round(head.getBoundingClientRect().bottom)) + 'px');
  };
  // Lock the page behind the menu without losing the scroll position (body is fixed while open).
  let lockedY = 0;
  const lock = (on) => {
    const b = document.body;
    if (on) {
      lockedY = window.scrollY;
      b.style.position = 'fixed'; b.style.top = -lockedY + 'px'; b.style.left = '0'; b.style.right = '0'; b.style.width = '100%';
    } else {
      b.style.position = ''; b.style.top = ''; b.style.left = ''; b.style.right = ''; b.style.width = '';
      window.scrollTo(0, lockedY);
    }
  };
  mobileMenu.addEventListener('toggle', () => {
    document.documentElement.classList.toggle('mm-open', mobileMenu.open);
    mobileMenu.querySelector('.mm-label').textContent = mobileMenu.open ? 'Close' : 'Menu';
    if (mobileMenu.open) { lock(true); place(); requestAnimationFrame(place); setTimeout(place, 320); }
    else { lock(false); show(null); }
  });
  window.addEventListener('resize', () => { if (mobileMenu.open) place(); });
  mobileMenu.addEventListener('click', (event) => {
    const next = event.target.closest('[data-mm]');
    if (next) { show(mm.querySelector('#mm-' + next.dataset.mm)); return; }
    if (event.target.closest('[data-mm-back]')) {
      const from = event.target.closest('.mm-panel');
      show(null);
      const btn = from && root.querySelector('[data-mm="' + from.id.slice(3) + '"]');
      if (btn) setTimeout(() => btn.focus({ preventScroll: true }), 260);
      return;
    }
    if (event.target.closest('.mm a')) mobileMenu.open = false;
  });
  document.addEventListener('keydown', (event) => {
    if (event.key !== 'Escape' || !mobileMenu.open) return;
    if (mm.classList.contains('is-sub')) { show(null); return; }
    mobileMenu.open = false;
    mobileMenu.querySelector('summary').focus();
  });
}

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
      values.get('registration') && `Registration: ${values.get('registration').toUpperCase()}`,
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
            subject, message: [values.get('vehicle') && `Vehicle: ${values.get('vehicle')}`, values.get('registration') && `Registration: ${values.get('registration').toUpperCase()}`, values.get('postcode') && `Postcode: ${values.get('postcode')}`, `Service: ${values.get('service')}`, '', values.get('details')].filter((x) => x !== null && x !== false).join('\n'),
            registration: (values.get('registration') || '').toUpperCase(), source_url: location.href, utm_source: source.utm_source || '', utm_medium: source.utm_medium || '', utm_campaign: source.utm_campaign || '', gclid: source.gclid || '',
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
    if (!(window.WraptConsent && window.WraptConsent.get().analytics)) return;
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
  const update = () => { if (document.documentElement.classList.contains('mm-open')) return; head.classList.toggle('is-stuck', window.scrollY > 34); };
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
    if (!form.offsetParent && window.openQuoteModal) {
      const svc = (form.querySelector('[name=service]') || {}).value;
      window.openQuoteModal(svc, `Package: ${btn.dataset.package}\nVan size: ${btn.dataset.size}\n`);
      return;
    }
    const set = (name, val) => { const sel = form.querySelector(`[name=${name}]`); if (!sel) return; [...sel.options].forEach((o) => { if (o.text === val) sel.value = o.value || o.text; }); };
    set('package', btn.dataset.package); set('size', btn.dataset.size);
    wrap.querySelectorAll('.pm-pick.is-picked').forEach((b) => b.classList.remove('is-picked')); btn.classList.add('is-picked');
    form.scrollIntoView({ behavior: 'smooth', block: 'center' });
    setTimeout(() => form.querySelector('[name=name]').focus({ preventScroll: true }), 500);
  });
});

/* Quote pop-up: every "Get a quote" link (#quote) opens a modal form instead of scrolling to the bottom */
(function () {
  const modal = document.getElementById('quote-modal');
  if (!modal || typeof modal.showModal !== 'function') return;
  let lastFocus = null;
  function open(service) {
    lastFocus = document.activeElement;
    const sel = modal.querySelector('[name=service]');
    if (service && sel) [...sel.options].forEach((o) => { if (o.text === service) sel.value = o.value || o.text; });
    modal.showModal();
    document.documentElement.classList.add('modal-open');
    setTimeout(() => modal.querySelector('[name=name]').focus(), 50);
    try { (window.dataLayer = window.dataLayer || []).push({ event: 'quote_popup_open' }); } catch (e) {}
  }
  function close() { modal.close(); }
  modal.addEventListener('close', () => { document.documentElement.classList.remove('modal-open'); if (lastFocus) lastFocus.focus(); });
  modal.addEventListener('click', (e) => { if (e.target === modal || e.target.closest('[data-close-modal]')) close(); });
  document.addEventListener('click', (e) => {
    const a = e.target.closest('a[href$="#quote"]');
    if (!a || a.closest('#quote-modal') || e.metaKey || e.ctrlKey) return;
    const url = new URL(a.href, location.href);
    if (url.pathname !== location.pathname && url.pathname !== '/contact/') return;
    if (location.pathname === '/contact/' && url.pathname === '/contact/') return;
    e.preventDefault();
    const card = a.closest('[data-service]');
    open(card ? card.dataset.service : (document.querySelector('#service-enquiry [name=service] option[selected]') || {}).text);
  });
  // On brand and model pages, pre-fill the vehicle (e.g. "Ford Transit Custom", or "Ford " on a brand page).
  const pageVehicle = (document.querySelector('[data-quote-vehicle]') || {}).dataset;
  if (pageVehicle && pageVehicle.quoteVehicle) {
    document.querySelectorAll('input[name=vehicle]').forEach((input) => { if (!input.value) input.value = pageVehicle.quoteVehicle; });
  }
  window.openQuoteModal = (service, details) => { open(service); if (details) { const d = modal.querySelector('[name=details]'); if (d && !d.value) d.value = details; } };
  if (location.hash === '#quote-popup') open();
})();

/* Van model shop pages: variant -> option -> colours -> artwork, live price; graphics go in the basket, wraps open the quote form */
(function () {
  const root = document.querySelector('.ms'); if (!root) return;
  const form = root.querySelector('.ms-form');
  const sel = form.querySelector('[name=variant]');
  const main = document.getElementById('ms-main-img');
  const cta = form.querySelector('.ms-cta');
  root.querySelectorAll('.ms-thumb').forEach((t) => t.addEventListener('click', () => {
    main.src = t.dataset.src; main.parentElement.classList.toggle('is-photo', !t.dataset.src.includes('/rcg/'));
    root.querySelectorAll('.ms-thumb').forEach((x) => x.classList.toggle('is-active', x === t));
  }));
  const names = { single: 'Single colour', two: 'Two colour', full: 'Full colour' };
  const optNames = { graphics: 'Simple graphics', half: 'Half wrap', full: 'Full wrap' };
  const routeNames = { upload: 'I have artwork', service: 'Design service' };
  const ROUTE_ADD = { upload: 0, service: 50 };
  const gbp = (n) => '£' + Number(n).toLocaleString('en-GB', { minimumFractionDigits: Number(n) % 1 ? 2 : 0, maximumFractionDigits: 2 });
  function state() {
    const o = sel.options[sel.selectedIndex];
    const option = form.querySelector('[name=option]:checked').value;
    const colour = (form.querySelector('[name=colour]:checked') || {}).value || 'single';
    const route = (form.querySelector('[name=route]:checked') || {}).value || 'upload';
    const qty = Math.max(1, Math.min(20, parseInt(form.querySelector('[name=qty]').value, 10) || 1));
    const unit = option === 'graphics' && o.dataset[colour] ? Number(o.dataset[colour]) + ROUTE_ADD[route] : null;
    return { o, option, colour, route, qty, unit, variant: o.text, sku: o.dataset.sku };
  }
  function update() {
    const s = state();
    ['single', 'two', 'full'].forEach((k) => { const el = form.querySelector(`[data-price-for="${k}"]`); if (el) el.textContent = s.o.dataset[k] ? gbp(s.o.dataset[k]) : '–'; });
    const from = form.querySelector('[data-from]'); if (from && s.o.dataset.single) from.textContent = gbp(s.o.dataset.single);
    const g = s.option === 'graphics';
    form.querySelector('.ms-colours').hidden = !g; form.querySelector('.ms-routes').hidden = !g;
    form.querySelector('.ms-qty').hidden = !g;
    form.querySelector('.ms-sum-name').textContent = s.variant;
    form.querySelector('.ms-sum-opt').textContent = optNames[s.option] + (g ? ` · ${names[s.colour]} · ${routeNames[s.route]}${s.qty > 1 ? ' · ×' + s.qty : ''}` : '');
    const p = form.querySelector('.ms-sum-price');
    if (s.unit) { const t = s.unit * s.qty; p.querySelector('b').textContent = gbp(t); p.querySelector('small').textContent = '+ VAT'; p.querySelector('.ms-sum-inc').textContent = gbp(Math.round(t * 120) / 100) + ' inc VAT'; }
    else { p.querySelector('b').textContent = 'Quote'; p.querySelector('small').textContent = 'per van'; p.querySelector('.ms-sum-inc').textContent = 'Fitted price in writing'; }
    cta.textContent = g ? 'Add to basket' : 'Get my ' + optNames[s.option].toLowerCase() + ' quote';
  }
  function openQuote(extra) {
    const s = state();
    const vehicle = (root.dataset.quoteModel || '') + ' – ' + s.variant;
    const details = `Option: ${optNames[s.option]}\n` + (extra || '');
    if (window.openQuoteModal) {
      window.openQuoteModal(s.option === 'graphics' ? 'Van signwriting' : 'Vehicle wraps', details);
      const v = document.querySelector('#quote-modal [name=vehicle]'); if (v) v.value = vehicle;
      const d = document.querySelector('#quote-modal [name=details]'); if (d) d.value = details;
    }
  }
  form.addEventListener('change', update);
  form.addEventListener('input', update);
  cta.addEventListener('click', () => {
    const s = state();
    if (s.option !== 'graphics') return openQuote();
    if (!window.WraptBasket || !s.sku || !s.unit) return openQuote();
    window.WraptBasket.add({
      sku: s.sku, title: cta.dataset.title, variant: s.variant, colour: s.colour, route: s.route, quantity: s.qty,
      unitEx: s.unit, image: cta.dataset.image, path: cta.dataset.path,
    });
  });
  form.querySelector('.ms-ask').addEventListener('click', () => openQuote());
  update();
})();

/* Site search + AI assistant (CRM site-search embed): show the Ask AI buttons once the widget is ready,
   and close the mobile menu before the search panel opens. */
(() => {
  const closeMenu = () => { const m = document.querySelector('.main-head details.mobile'); if (m && m.open) { m.open = false; m.dispatchEvent(new Event('toggle')); } };
  document.addEventListener('click', (e) => {
    const ai = e.target.closest('[data-ask-ai]');
    if (ai && window.SiteSearch) { e.preventDefault(); closeMenu(); window.SiteSearch.ask(); return; }
    if (e.target.closest('.mm [data-site-search]')) closeMenu();
  }, true);
  const ready = () => document.querySelectorAll('[data-ask-ai][hidden],[data-ask-ai-wrap][hidden]').forEach((el) => el.removeAttribute('hidden'));
  if (window.SiteSearch) ready(); else window.addEventListener('site-search-ready', ready, { once: true });
})();

/* Ex VAT / Inc VAT toggle. Every Wrapt price on the site is written ex VAT; this re-writes the price text in place
   (and anything the shop scripts add later) when the visitor picks Inc VAT. The choice is remembered in this browser. */
(() => {
  const KEY = 'wrapt-vat';
  let mode = 'ex'; try { mode = localStorage.getItem(KEY) === 'inc' ? 'inc' : 'ex'; } catch {}
  const orig = new WeakMap(); let busy = false;
  const SKIP = 'script,style,noscript,textarea,input,select,option,.care-card,.care,.co-totals,.co-delivery,.ms-sum-inc,.vat-toggle,[data-vat-skip]';
  const PRICE = /£\s?(\d{1,3}(?:,\d{3})*|\d+)(\.\d{1,2})?/g;
  const fmt = (n) => '£' + (Math.abs(n - Math.round(n)) < 0.005 ? Math.round(n).toLocaleString('en-GB') : n.toLocaleString('en-GB', { minimumFractionDigits: 2, maximumFractionDigits: 2 }));
  const convert = (s) => {
    const exact = /^\s*\+?\s*£[\d,]+(\.\d{1,2})?\s*$/.test(s);
    const hasVat = /\+\s*VAT|ex(c|cl)?\.?\s*VAT/i.test(s);
    if (!exact && !hasVat) return null;
    let out = s.replace(PRICE, (m, a, b) => fmt(Math.round(parseFloat(a.replace(/,/g, '') + (b || '')) * 120) / 100));
    out = out.replace(/\+\s*VAT/g, 'inc VAT').replace(/\bex(c|cl)?\.?\s*VAT\b/gi, 'inc VAT');
    return out;
  };
  const relevant = (t) => /£|VAT/.test(t.nodeValue) && !t.parentElement?.closest(SKIP);
  const apply = (rootEl) => {
    busy = true;
    const w = document.createTreeWalker(rootEl, NodeFilter.SHOW_TEXT);
    for (let t; (t = w.nextNode());) {
      if (!orig.has(t)) { if (!relevant(t)) continue; const inc = convert(t.nodeValue); if (inc == null) continue; orig.set(t, { ex: t.nodeValue, inc }); }
      const o = orig.get(t), want = mode === 'inc' ? o.inc : o.ex;
      if (t.nodeValue !== want) t.nodeValue = want;
    }
    document.documentElement.dataset.vat = mode;
    document.querySelectorAll('.vat-toggle button').forEach((b) => b.setAttribute('aria-pressed', String(b.dataset.vat === mode)));
    busy = false;
  };
  const scope = () => [document.querySelector('main'), document.querySelector('.qm, .quote-modal'), document.querySelector('.mm')].filter(Boolean);
  const run = () => scope().forEach(apply);
  document.addEventListener('click', (e) => {
    const b = e.target.closest('.vat-toggle button'); if (!b) return;
    mode = b.dataset.vat === 'inc' ? 'inc' : 'ex'; try { localStorage.setItem(KEY, mode); } catch {}
    run();
  });
  // Shop scripts replace price text as options change: forget the old text and re-apply to what they wrote.
  new MutationObserver((list) => {
    if (busy) return;
    const roots = new Set();
    for (const m of list) {
      if (m.type === 'characterData') { const t = m.target; const o = orig.get(t); if (o && t.nodeValue !== o.ex && t.nodeValue !== o.inc) orig.delete(t); if (t.parentElement) roots.add(t.parentElement); }
      else m.addedNodes.forEach((n) => roots.add(n.nodeType === 3 ? n.parentElement : n));
    }
    roots.forEach((r) => r && r.isConnected && apply(r));
  }).observe(document.body, { childList: true, characterData: true, subtree: true });
  if (document.readyState === 'loading') document.addEventListener('DOMContentLoaded', run); else run();
})();

/* Vehicle search (like Race Car Graphics): make, model or SKU -> the model page (variant pre-selected). Header car
   button on desktop, top of the burger menu on phones. Index: /assets/vehicle-index.json, loaded on first use. */
(() => {
  let index = null, loading = null;
  const norm = (s) => String(s || '').toLowerCase().normalize('NFD').replace(/[̀-ͯ]/g, '').replace(/[^a-z0-9]+/g, ' ').trim();
  const load = () => loading || (loading = fetch('/assets/vehicle-index.json').then((r) => r.json()).then((d) => { index = d.map((x) => ({ ...x, h: norm(x.k + ' ' + x.n + ' ' + (x.s || '')), nn: norm(x.n) })); }).catch(() => { loading = null; }));
  const esc = (s) => String(s).replace(/[&<>"]/g, (c) => ({ '&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;' }[c]));
  function find(q) {
    const words = norm(q).split(' ').filter(Boolean); if (!words.length || !index) return [];
    const sku = norm(q).replace(/ /g, '');
    const hits = [];
    for (const x of index) {
      if (x.s && norm(x.s) === sku) { hits.push([-10, x]); continue; }
      if (!words.every((w) => x.h.includes(w))) continue;
      let score = x.t === 'b' ? 0 : x.t === 'm' ? 1 : 3;
      if (x.nn.startsWith(words[0])) score -= 0.5;
      if (words.every((w) => x.nn.includes(w))) score -= 0.5;
      hits.push([score + x.n.length / 200, x]);
    }
    return hits.sort((a, b) => a[0] - b[0]).slice(0, 8).map((h) => h[1]);
  }
  function render(box, q) {
    if (norm(q).length < 2) { box.innerHTML = ''; box.hidden = true; return; }
    const r = find(q); box.hidden = false;
    box.innerHTML = r.length ? r.map((x) => `<a href="${esc(x.p)}" role="option"><span class="veh-img">${x.i ? `<img src="${esc(x.i)}" alt="" width="82" height="49" loading="lazy">` : ''}</span><span><strong>${esc(x.n)}</strong><small>${esc(x.s ? x.s + ' · ' + x.d : x.d)}</small></span></a>`).join('')
      : (window.SiteSearch ? '<p>No vehicles match. Search the whole site or ask our assistant below.</p>' : '<p>No matching vehicles. Try a make, model or SKU, or <a href="#quote">ask for a quote</a>.</p>');
  }
  document.querySelectorAll('[data-veh-input]').forEach((input) => {
    const box = input.closest('.veh-pop, .mm-veh').querySelector('.veh-results');
    input.addEventListener('focus', load);
    input.addEventListener('input', () => { const q = input.value; (index ? Promise.resolve() : load()).then(() => { if (input.value === q) render(box, q); }); });
    input.addEventListener('keydown', (e) => {
      if (e.key === 'Enter') { e.preventDefault(); const a = box.querySelector('a[role=option]'); if (a) location.href = a.href; else if (window.SiteSearch && input.value.trim()) { closePop(); window.SiteSearch.open(input.value.trim()); } }
      if (e.key === 'Escape') closePop();
    });
  });
  const wrap = document.querySelector('.veh-find'), btn = wrap && wrap.querySelector('.head-find'), pop = wrap && wrap.querySelector('.veh-pop');
  function closePop() { if (!pop) return; pop.hidden = true; btn.setAttribute('aria-expanded', 'false'); }
  if (btn) {
    btn.addEventListener('click', () => { const open = pop.hidden; pop.hidden = !open; btn.setAttribute('aria-expanded', String(open)); if (open) { load(); setTimeout(() => pop.querySelector('input').focus(), 0); } });
    pop.querySelector('.veh-x').addEventListener('click', closePop);
    const q = () => pop.querySelector('[data-veh-input]').value.trim();
    pop.querySelector('[data-q-site]').addEventListener('click', () => { if (!window.SiteSearch) return; const v = q(); closePop(); window.SiteSearch.open(v); });
    pop.querySelector('[data-q-ai]').addEventListener('click', () => { if (!window.SiteSearch) return; const v = q(); closePop(); window.SiteSearch.ask(v); });
    document.addEventListener('pointerdown', (e) => { if (!pop.hidden && !wrap.contains(e.target)) closePop(); });
  }
  // Model page opened from a variant result: pre-select that variant.
  const sku = new URLSearchParams(location.search).get('sku'), sel = document.querySelector('.ms [name=variant]');
  if (sku && sel) { const o = [...sel.options].find((x) => x.dataset.sku === sku); if (o) { sel.value = o.value; sel.dispatchEvent(new Event('change', { bubbles: true })); } }
})();
