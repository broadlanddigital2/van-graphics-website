/* Wrapt cookie consent: banner, settings panel, and consent-gated scripts (analytics, chat tracking). */
(function () {
  var KEY = 'wrapt-cookie-consent', VERSION = 1, GA = document.body.dataset.ga || '';
  function read() { try { var c = JSON.parse(localStorage.getItem(KEY) || 'null'); return c && c.v === VERSION ? c : null; } catch (e) { return null; } }
  function save(c) { c.v = VERSION; c.ts = new Date().toISOString(); try { localStorage.setItem(KEY, JSON.stringify(c)); } catch (e) {} apply(c); }
  var state = read();
  function get() { return state || { analytics: false, marketing: false }; }

  window.dataLayer = window.dataLayer || [];
  function gtag() { dataLayer.push(arguments); }
  gtag('consent', 'default', { analytics_storage: 'denied', ad_storage: 'denied', ad_user_data: 'denied', ad_personalization: 'denied', functionality_storage: 'granted', security_storage: 'granted' });
  var gaLoaded = false;
  function loadGA() {
    if (gaLoaded || !GA) return; gaLoaded = true;
    var s = document.createElement('script'); s.async = true; s.src = 'https://www.googletagmanager.com/gtag/js?id=' + encodeURIComponent(GA); document.head.appendChild(s);
    gtag('js', new Date()); gtag('config', GA);
  }
  function apply(c) {
    state = c;
    gtag('consent', 'update', { analytics_storage: c.analytics ? 'granted' : 'denied', ad_storage: c.marketing ? 'granted' : 'denied', ad_user_data: c.marketing ? 'granted' : 'denied', ad_personalization: c.marketing ? 'granted' : 'denied' });
    if (c.analytics) loadGA();
    if (!c.analytics) { try { localStorage.removeItem('nvg_source'); } catch (e) {} }
    window.__crmBotTracking = !!c.analytics;
    window.dispatchEvent(new CustomEvent('rcg-enquiry-bot-consent', { detail: { tracking: !!c.analytics } }));
    window.dispatchEvent(new CustomEvent('wrapt:consent', { detail: c }));
    hideBanner();
  }
  window.__crmBotTracking = !!get().analytics;
  window.WraptConsent = { get: get, open: openPanel };

  var banner, panel;
  function el(html) { var d = document.createElement('div'); d.innerHTML = html.trim(); return d.firstChild; }
  function showBanner() {
    if (banner) return;
    banner = el('<section class="cookie-banner" role="region" aria-label="Cookie consent"><div class="cookie-banner__inner">' +
      '<div class="cookie-banner__text"><p class="cookie-banner__title">Cookies on Wrapt</p><p>We use essential cookies to make this site work. With your permission we would also like to use analytics cookies to see how the site is used and improve it. <a href="/cookie-policy/">Cookie policy</a></p></div>' +
      '<div class="cookie-banner__actions"><button type="button" class="btn" data-c="all">Accept all</button><button type="button" class="btn outline" data-c="none">Reject non-essential</button><button type="button" class="link-btn" data-c="settings">Settings</button></div></div></section>');
    banner.addEventListener('click', function (e) {
      var b = e.target.closest('[data-c]'); if (!b) return;
      if (b.dataset.c === 'all') save({ analytics: true, marketing: true });
      if (b.dataset.c === 'none') save({ analytics: false, marketing: false });
      if (b.dataset.c === 'settings') openPanel();
    });
    document.body.appendChild(banner);
  }
  function hideBanner() { if (banner) { banner.remove(); banner = null; } }
  function openPanel() {
    var c = get();
    if (panel) panel.remove();
    panel = el('<div class="cookie-panel" role="dialog" aria-modal="true" aria-labelledby="cookie-panel-title"><div class="cookie-panel__box">' +
      '<button type="button" class="cookie-panel__close" aria-label="Close cookie settings">×</button>' +
      '<h2 id="cookie-panel-title">Cookie settings</h2><p>Choose which cookies we can use. You can change this at any time from the link in the footer.</p>' +
      '<div class="cookie-opt"><div><b>Strictly necessary</b><small>Remember your cookie choice and keep the Van Designer working. Always on.</small></div><span class="cookie-always">Always on</span></div>' +
      '<label class="cookie-opt"><div><b>Analytics</b><small>Google Analytics and enquiry source tracking, so we can see which pages help and improve the site.</small></div><input type="checkbox" name="analytics"' + (c.analytics ? ' checked' : '') + '><span class="cookie-switch" aria-hidden="true"></span></label>' +
      '<label class="cookie-opt"><div><b>Marketing</b><small>Measures our Google ads so we spend less showing them to the wrong people.</small></div><input type="checkbox" name="marketing"' + (c.marketing ? ' checked' : '') + '><span class="cookie-switch" aria-hidden="true"></span></label>' +
      '<div class="cookie-panel__actions"><button type="button" class="btn" data-p="save">Save choices</button><button type="button" class="btn outline" data-p="all">Accept all</button></div></div></div>');
    function close() { panel.remove(); panel = null; }
    panel.addEventListener('click', function (e) {
      if (e.target === panel || e.target.closest('.cookie-panel__close')) return close();
      var b = e.target.closest('[data-p]'); if (!b) return;
      if (b.dataset.p === 'all') save({ analytics: true, marketing: true });
      else save({ analytics: panel.querySelector('[name=analytics]').checked, marketing: panel.querySelector('[name=marketing]').checked });
      close();
    });
    panel.addEventListener('keydown', function (e) { if (e.key === 'Escape') close(); });
    document.body.appendChild(panel);
    panel.querySelector('input,button').focus();
  }
  document.addEventListener('click', function (e) {
    var t = e.target.closest('[data-cookie-settings]'); if (!t) return;
    e.preventDefault(); openPanel();
  });
  if (state) apply(state); else showBanner();
})();
