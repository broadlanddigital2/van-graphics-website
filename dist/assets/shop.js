/* Get It Wrapt shop: basket (localStorage), checkout and order confirmation.
   Orders go to the CRM's shop checkout (same as Race Car Graphics), which re-prices every line,
   creates the order and invoice on the Get It Wrapt business and returns a Stripe payment page. */
(function () {
  const CRM = 'https://dipjypzrfigkzuarlsov.supabase.co/functions/v1/booking-order-flow';
  const KEY = 'sb_publishable_KLK1Ucd9ilVSwzSGL1vkug_3SGGh4NF'; // public (publishable) key
  const BUSINESS = '19fee7a6-55b9-428a-a9eb-35967e6a45ef';
  const STORE = 'wrapt-basket';
  const VAT = 0.2;
  const DELIVERY = [
    { id: '65a1e7d6-c259-44aa-80a7-35f0f6cae8d8', name: 'Standard delivery', detail: 'Tracked UK delivery, 3–5 working days', price: 0 },
    { id: 'fa30ffc3-a966-4684-b25d-d488ddb7dcd6', name: 'Express delivery', detail: 'Priority tracked UK delivery, 1–2 working days', price: 9.95 },
  ];
  const COLOUR = { single: 'Single colour', two: 'Two colour', full: 'Full colour' };
  const ROUTE = { upload: 'Artwork upload', service: 'Design service' };
  const gbp = (n) => '£' + Number(n).toLocaleString('en-GB', { minimumFractionDigits: 2, maximumFractionDigits: 2 });
  const esc = (v) => String(v ?? '').replace(/[&<>"]/g, (c) => ({ '&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;' }[c]));

  function read() { try { const b = JSON.parse(localStorage.getItem(STORE) || '[]'); return Array.isArray(b) ? b : []; } catch (e) { return []; } }
  function write(items) { try { localStorage.setItem(STORE, JSON.stringify(items)); } catch (e) {} paintCount(); window.dispatchEvent(new Event('wrapt:basket')); }
  function count() { return read().reduce((t, i) => t + (i.quantity || 1), 0); }
  function paintCount() {
    const n = count();
    document.querySelectorAll('[data-basket-count]').forEach((el) => { el.textContent = n; el.hidden = !n; });
  }

  async function crm(action, body) {
    const r = await fetch(CRM, { method: 'POST', headers: { apikey: KEY, 'Content-Type': 'application/json' }, body: JSON.stringify({ action, ...body }) });
    const data = await r.json().catch(() => ({}));
    if (!r.ok || data.error) throw new Error(data.error || 'Something went wrong. Please try again or call 01603 407786.');
    return data;
  }

  /* Added-to-basket toast */
  function toast(item) {
    let t = document.querySelector('.basket-toast');
    if (!t) { t = document.createElement('div'); t.className = 'basket-toast'; t.setAttribute('role', 'status'); document.body.appendChild(t); }
    t.innerHTML = `<img src="${esc(item.image)}" alt=""><div><b>Added to your basket</b><span>${esc(item.title)} · ${esc(item.variant)}</span></div>`
      + `<a class="btn" href="/checkout/">Checkout</a><button type="button" aria-label="Close">×</button>`;
    t.classList.add('show');
    t.querySelector('button').onclick = () => t.classList.remove('show');
    clearTimeout(t._h); t._h = setTimeout(() => t.classList.remove('show'), 7000);
  }

  window.WraptBasket = {
    items: read,
    add(item) {
      const items = read();
      const same = items.find((i) => i.sku === item.sku && i.colour === item.colour && i.route === item.route);
      if (same) same.quantity = Math.min(20, (same.quantity || 1) + (item.quantity || 1));
      else items.push({ ...item, id: Date.now().toString(36) + Math.random().toString(36).slice(2, 6), uploads: [] });
      write(items); toast(item);
      try { (window.dataLayer = window.dataLayer || []).push({ event: 'add_to_cart', ecommerce: { currency: 'GBP', value: item.unitEx * item.quantity, items: [{ item_id: item.sku, item_name: item.title + ' ' + item.variant, price: item.unitEx, quantity: item.quantity }] } }); } catch (e) {}
    },
  };
  paintCount();
  window.addEventListener('storage', paintCount);

  /* ---------- Checkout page ---------- */
  const co = document.getElementById('checkout');
  if (co) {
    const params = new URLSearchParams(location.search);
    const list = co.querySelector('.co-items');
    const form = co.querySelector('.co-form');
    const totals = co.querySelector('.co-totals');
    const status = co.querySelector('.co-status');
    if (params.get('payment') === 'cancelled') { status.hidden = false; status.className = 'co-status is-info'; status.textContent = 'Payment not completed. You have not been charged – check your details and try again when you are ready.'; }

    function fulfilment() { return (form.querySelector('[name=fulfilment]:checked') || {}).value || 'delivery'; }
    function deliveryOpt() { const id = (form.querySelector('[name=delivery]:checked') || {}).value; return DELIVERY.find((d) => d.id === id) || DELIVERY[0]; }

    function render() {
      const items = read();
      co.classList.toggle('is-empty', !items.length);
      list.innerHTML = items.map((i) => `<article class="co-item" data-id="${i.id}">
        <a href="${esc(i.path)}"><img src="${esc(i.image)}" alt=""></a>
        <div class="co-item__body"><b>${esc(i.title)}</b><span>${esc(i.variant)}</span><small>${COLOUR[i.colour] || ''} · ${ROUTE[i.route] || ''}</small>
          ${i.route === 'upload' ? `<div class="co-upload"><label class="btn outline small"><input type="file" multiple accept=".pdf,.ai,.eps,.svg,.jpg,.jpeg,.png,.tif,.tiff,.psd,.cdr,.zip,.webp">Upload artwork</label>
            <ul>${(i.uploads || []).map((u, k) => `<li>${esc(u.name)} <button type="button" data-remove-upload="${k}">Remove</button></li>`).join('')}</ul>
            <small class="co-upload__hint">${(i.uploads || []).length ? '' : 'Add your logo or artwork (PDF, AI, EPS, SVG, PNG or JPG, up to 50 MB). You can also email it after ordering.'}</small></div>`
            : `<label class="co-brief">Design brief<textarea rows="2" maxlength="1500" placeholder="Business name, services, phone, website, colours…">${esc(i.notes || '')}</textarea></label>`}
        </div>
        <div class="co-item__side"><label class="co-qty"><span class="sr-only">Quantity</span><input type="number" min="1" max="20" value="${i.quantity}"></label>
          <b>${gbp(i.unitEx * i.quantity)}</b><small>+ VAT</small><button type="button" class="co-remove">Remove</button></div></article>`).join('')
        || '<div class="co-empty"><b>Your basket is empty.</b><p>Choose your van to add graphics.</p><a class="btn" href="/vehicles/">Choose your van</a></div>';
      const goodsEx = items.reduce((t, i) => t + i.unitEx * i.quantity, 0);
      const goodsInc = Math.round(goodsEx * (1 + VAT) * 100) / 100;
      const del = fulfilment() === 'delivery' && items.length ? deliveryOpt().price : 0;
      const total = Math.round((goodsInc + del) * 100) / 100;
      const vat = Math.round((total - goodsEx - del / (1 + VAT)) * 100) / 100;
      totals.innerHTML = `<div><span>Graphics</span><b>${gbp(goodsEx)}</b></div>`
        + `<div><span>${fulfilment() === 'delivery' ? deliveryOpt().name : 'Fitting at our workshop'}</span><b>${fulfilment() === 'delivery' ? (del ? gbp(del) : 'Free') : 'Quoted after order'}</b></div>`
        + `<div><span>VAT (20%)</span><b>${gbp(vat)}</b></div><div class="co-total"><span>Total to pay</span><b>${gbp(items.length ? total : 0)}</b></div>`;
      co.querySelector('.co-pay').disabled = !items.length;
      co.querySelectorAll('[data-for-fulfilment]').forEach((el) => { el.hidden = el.dataset.forFulfilment !== fulfilment(); });
    }

    list.addEventListener('change', async (e) => {
      const card = e.target.closest('.co-item'); if (!card) return;
      const items = read(); const item = items.find((i) => i.id === card.dataset.id); if (!item) return;
      if (e.target.matches('.co-qty input')) { item.quantity = Math.max(1, Math.min(20, parseInt(e.target.value, 10) || 1)); write(items); render(); }
      if (e.target.matches('.co-brief textarea')) { item.notes = e.target.value.slice(0, 1500); write(items); }
      if (e.target.matches('.co-upload input[type=file]')) {
        const files = [...e.target.files].slice(0, 10 - (item.uploads || []).length);
        const hint = card.querySelector('.co-upload__hint');
        for (const file of files) {
          hint.textContent = `Uploading ${file.name}…`;
          try {
            const slot = await crm('public_artwork_upload_url', { file_name: file.name, size: file.size, type: file.type });
            const put = await fetch(slot.signed_url, { method: 'PUT', headers: { 'Content-Type': file.type || 'application/octet-stream', 'x-upsert': 'false' }, body: file });
            if (!put.ok) throw new Error(`${file.name} didn't upload. Please try again.`);
            item.uploads = [...(item.uploads || []), { path: slot.path, name: file.name, size: file.size, type: file.type }];
            write(items);
          } catch (err) { hint.textContent = err.message; return; }
        }
        render();
      }
    });
    list.addEventListener('click', (e) => {
      const card = e.target.closest('.co-item'); if (!card) return;
      let items = read();
      if (e.target.matches('.co-remove')) { items = items.filter((i) => i.id !== card.dataset.id); write(items); render(); }
      if (e.target.matches('[data-remove-upload]')) { const it = items.find((i) => i.id === card.dataset.id); it.uploads.splice(+e.target.dataset.removeUpload, 1); write(items); render(); }
    });
    form.addEventListener('change', (e) => { if (e.target.name === 'fulfilment' || e.target.name === 'delivery') render(); });

    form.addEventListener('submit', async (e) => {
      e.preventDefault();
      const items = read(); if (!items.length) return;
      const fd = new FormData(form); const v = (k) => String(fd.get(k) || '').trim();
      const missing = ['first_name', 'last_name', 'email', 'mobile', 'address_line_1', 'city', 'postcode'].filter((k) => !v(k));
      if (missing.length || !/^\S+@\S+\.\S+$/.test(v('email'))) {
        status.hidden = false; status.className = 'co-status is-error'; status.textContent = 'Please fill in your name, email, mobile and address.';
        form.querySelector(`[name=${missing[0] || 'email'}]`).focus(); return;
      }
      if (!fd.get('terms')) { status.hidden = false; status.className = 'co-status is-error'; status.textContent = 'Please accept the terms to continue.'; return; }
      const btn = co.querySelector('.co-pay'); btn.disabled = true; btn.textContent = 'Opening secure payment…';
      status.hidden = true;
      try {
        const fit = fulfilment() === 'fit';
        const result = await crm('public_graphics_order', {
          business_unit_id: BUSINESS,
          items: items.map((i) => ({ sku: i.sku, product: `${i.title} ${i.variant}`, graphicsType: COLOUR[i.colour], designRoute: ROUTE[i.route], quantity: i.quantity,
            artworkUploads: i.uploads || [], notes: i.notes || '', image: location.origin + i.image })),
          fulfilment: fit ? 'fit' : 'delivery', delivery_id: fit ? '' : deliveryOpt().id,
          first_name: v('first_name'), last_name: v('last_name'), email: v('email').toLowerCase(), mobile: v('mobile'),
          address_line_1: v('address_line_1'), address_line_2: v('address_line_2'), city: v('city'), postcode: v('postcode').toUpperCase(),
          notes: [v('vehicle_reg') && `Vehicle registration: ${v('vehicle_reg').toUpperCase()}`, v('notes')].filter(Boolean).join('\n'),
          website: v('website'), marketing_email_consent: fd.get('marketing') === 'on', source_url: location.href.split('#')[0],
          success_url: `${location.origin}/checkout/complete/?session_id={CHECKOUT_SESSION_ID}`,
          cancel_url: `${location.origin}/checkout/?payment=cancelled`,
        });
        const url = result.checkout && result.checkout.url || '';
        if (!/^https:\/\/([a-z0-9-]+\.)*stripe\.com\//.test(url)) throw new Error("We couldn't open the secure payment page. Please try again or call 01603 407786.");
        try { sessionStorage.setItem('wrapt-pending', JSON.stringify({ order: result.order_number, total: result.total })); } catch (err) {}
        location.assign(url);
      } catch (err) {
        status.hidden = false; status.className = 'co-status is-error'; status.textContent = err.message;
        btn.disabled = false; btn.textContent = 'Pay securely';
      }
    });
    render();
  }

  /* ---------- Order complete page ---------- */
  const done = document.getElementById('order-complete');
  if (done) {
    const sid = new URLSearchParams(location.search).get('session_id') || '';
    const msg = done.querySelector('.oc-message');
    if (!/^cs_[A-Za-z0-9_]+$/.test(sid)) { msg.textContent = 'We could not find your payment reference. If you have paid, check your email for the confirmation or call 01603 407786.'; }
    else crm('public_booking_status', { session_id: sid }).then((r) => {
      write([]);
      const ref = r.order_number || (r.order && r.order.order_number) || '';
      done.querySelector('.oc-ref').textContent = ref ? `Order ${ref}` : '';
      msg.textContent = 'Thank you – your payment has been received. We have emailed your confirmation and will be in touch about your artwork proof and delivery or fitting.';
      try { (window.dataLayer = window.dataLayer || []).push({ event: 'purchase', ecommerce: { transaction_id: ref || sid, currency: 'GBP', value: r.total || r.amount || undefined } }); } catch (e) {}
    }).catch(() => { msg.textContent = 'Your payment is being confirmed. You will receive an email shortly – if not, call 01603 407786 with your name and we will check.'; });
  }
})();
