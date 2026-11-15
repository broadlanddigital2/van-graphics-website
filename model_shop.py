"""Van model product pages (shop-style): pick a variant, then simple graphics (priced from Race Car Graphics),
a half wrap or a full wrap (both quoted). Families, variants and prices come from rcg_vans.json
(refresh with: python3 tools/import_rcg_vans.py /path/to/rcg-website)."""
import json, re
from html import escape
from pathlib import Path

DATA = json.loads(Path('rcg_vans.json').read_text(encoding='utf-8'))
KEYMAP = {'mercedes-benz': 'mercedes'}
RENAME = {('ford', 'custom'): 'Transit Custom', ('ford', 'connect'): 'Transit Connect', ('ford', 'courier'): 'Transit Courier',
          ('ford', 'custom ms-rt'): 'Transit Custom MS-RT'}
COLOURS = [('single', 'Single colour', 'Clean cut-vinyl graphics in one colour.'),
           ('two', 'Two colour', 'Two vinyl colours for more contrast and depth.'),
           ('full', 'Full colour', 'Printed gradients, textures and unlimited colours.')]


def clean_name(make_slug, name):
    n = re.sub(r'\s*(?:cab)?(?:19|20)\d{2}.*$', '', name, flags=re.I)
    n = re.sub(r'\s+(?:nsld|nld|reg)\b.*$', '', n, flags=re.I).strip() or name
    return RENAME.get((make_slug, n.lower()), n)


def families(brand_key, label, family_pages, image_for):
    """All model families for a brand, with their page path, images and variants."""
    src = next((b for k, b in DATA.items() if KEYMAP.get(k, k) == brand_key), None)
    if not src:
        return []
    out, seen = [], set()
    for f in src['families']:
        make_slug = next(k for k, b in DATA.items() if b is src)
        display = clean_name(make_slug, f['name'])
        if display.lower() in seen:
            display = f'{display} ({f["name"]})'
        seen.add(display.lower())
        dedicated = family_pages.get((label.lower(), display.lower()))
        path = f'/vehicles/{dedicated}/' if dedicated else f'/vehicles/{f["slug"]}-van-graphics/'
        ours = image_for(label, display)
        big = [f'/assets/vehicles/{dedicated}-{v}.webp' for v in ('hero', 'side') if dedicated and Path(f'dist/assets/vehicles/{dedicated}-{v}.webp').exists()]
        if not big and ours:
            fam_full = Path('dist' + ours.replace('/thumbs/', '/families/'))
            big = ['/' + str(fam_full).removeprefix('dist/')] if fam_full.exists() else [ours]
        images = big  # only Get It Wrapt's own photos; Race Car Graphics product images are not used here
        prices = [v['prices'].get('single') for v in f['variants'] if v['prices'].get('single')]
        out.append(dict(name=display, full=f'{label} {display}', slug=f['slug'], path=path, dedicated=dedicated,
                        images=images, variants=f['variants'], rcg_url=f.get('rcg_url'), from_price=min(prices) if prices else None))
    return sorted(out, key=lambda x: (not x['dedicated'], -len(x['variants']), x['name']))


def variant_label(v):
    body = v['body'] if v['body'] and v['body'].lower() not in v['model'].lower() else ''
    return f'{v["model"]} {body}'.strip()


def product_page(fam, label, brand_key, brand_logo, others, copy=None, hero=None):
    """Shop-style model page. copy = (intro, panels, tip, faqs) bespoke text when we have it."""
    full = escape(fam['full'])
    imgs = fam['images']
    main = imgs[0] if imgs else ''
    thumbs = ''.join(f'<button type="button" class="ms-thumb{" is-active" if i == 0 else ""}{"" if "/rcg/" in src else " is-photo"}" data-src="{src}" aria-label="Show image {i + 1}"><img src="{src}" alt="" loading="lazy"></button>'
                     for i, src in enumerate(imgs[:6])) if len(imgs) > 1 else ''
    variants = fam['variants']
    opts = ''.join(f'<option value="{i}" data-sku="{v["sku"]}" data-single="{v["prices"].get("single", "")}" data-two="{v["prices"].get("two", "")}" data-full="{v["prices"].get("full", "")}">{escape(variant_label(v))}</option>'
                   for i, v in enumerate(variants))
    first = variants[0]['prices']
    fp = fam['from_price']
    colour_cards = ''.join(f'<label class="ms-colour"><input type="radio" name="colour" value="{k}"{" checked" if k == "single" else ""}>'
                           f'<span><b>{t}</b><small>{d}</small><em data-price-for="{k}">£{first.get(k, "")}</em></span></label>' for k, t, d in COLOURS)
    intro = escape(copy[0]) if copy else (f'Graphics, half wraps and full wraps designed on the exact {full} template: choose your year and body style, '
                                           f'then pick simple vinyl graphics at a fixed price or ask us to quote a wrap.')
    panels = escape(copy[1]) if copy else (f'Every {full} variant has its own door gaps, handles, swage lines and glazing, so we lay your graphics out on the '
                                           f'matching template rather than a generic van shape. Tell us about roof racks, ladders or bodywork changes and we will allow for them.')
    tip = escape(copy[2]) if copy else 'Send a photo of each side and the back with your order, so we can check the template against your actual van before anything is printed.'
    rows = ''.join(f'<tr><td>{escape(variant_label(v))}</td>' + ''.join(f'<td>£{v["prices"].get(k, "–")}</td>' for k, _, _ in COLOURS) + '<td>Quote</td><td>Quote</td></tr>' for v in variants)
    related = ''.join(f'<a class="ms-rel" href="{o["path"]}">' + (f'<img src="{o["images"][0]}" alt="" loading="lazy">' if o["images"] else f'<span class="ms-rel__logo">{brand_logo}</span>') + '<span><b>{escape(o["name"])}</b>'
                      f'<small>{("From £" + str(o["from_price"]) + " + VAT") if o["from_price"] else "Quoted"}</small></span></a>' for o in others[:8])
    rcg = ''
    _unused = (f'<p class="ms-diy">Fitting it yourself? Buy the same graphics as a DIY kit from our sister site '
           f'<a href="{fam["rcg_url"]}" target="_blank" rel="noopener">Race Car Graphics</a>.</p>') if fam.get('rcg_url') else ''
    return f'''<section class="ms" data-quote-model="{full}">
<div class="shell ms-grid">
  <div class="ms-gallery">
    <div class="ms-main{' is-photo' if main else ' is-logo'}">{f'<img id="ms-main-img" src="{main}" alt="{full} van graphics" width="1200" height="675" fetchpriority="high">' if main else brand_logo}</div>
    <div class="ms-thumbs">{thumbs}</div>
  </div>
  <div class="ms-buy">
    <nav class="crumb" aria-label="Breadcrumb"><a href="/">Home</a><span aria-hidden="true">/</span><a href="/vehicles/">Vans</a><span aria-hidden="true">/</span><a href="/vehicles/{brand_key}-van-graphics/">{escape(label)}</a><span aria-hidden="true">/</span><span>{escape(fam["name"])}</span></nav>
    <div class="ms-brand">{brand_logo}<span>{len(variants)} variant{"s" if len(variants) != 1 else ""}</span></div>
    <h1>{full} graphics &amp; wraps</h1>
    <p class="ms-rating"><span aria-hidden="true">★★★★★</span> 5.0 on Google · Designed &amp; fitted in Norwich</p>
    <p class="ms-price"><span class="ms-price__label">Graphics from</span><b>£{fp}</b><small>+ VAT</small></p>
    <p class="ms-lede">{intro}</p>
    <form class="ms-form" onsubmit="return false">
      <fieldset class="ms-step"><legend><span>1</span>Select your {escape(fam["name"])}</legend>
        <select name="variant" class="ms-select" aria-label="Variant">{opts}</select></fieldset>
      <fieldset class="ms-step"><legend><span>2</span>Choose your option</legend>
        <div class="ms-options">
          <label class="ms-opt"><input type="radio" name="option" value="graphics" checked><span><b>Simple graphics</b><small>Vinyl graphics on your exact template</small><em>From <i data-from>£{first.get("single", fp)}</i> + VAT</em></span></label>
          <label class="ms-opt"><input type="radio" name="option" value="half"><span><b>Half wrap</b><small>Printed colour on selected panels</small><em>Quoted</em></span></label>
          <label class="ms-opt"><input type="radio" name="option" value="full"><span><b>Full wrap</b><small>The whole van in printed vinyl</small><em>Quoted</em></span></label>
        </div></fieldset>
      <fieldset class="ms-step ms-colours"><legend><span>3</span>Choose your colours</legend><div class="ms-colour-grid">{colour_cards}</div></fieldset>
      <fieldset class="ms-step ms-routes"><legend><span>4</span>Your artwork</legend><div class="ms-options ms-options--2">
        <label class="ms-opt"><input type="radio" name="route" value="upload" checked><span><b>I have artwork</b><small>Upload your logo and wording at checkout. We check it and send a proof.</small><em>Included</em></span></label>
        <label class="ms-opt"><input type="radio" name="route" value="service"><span><b>Design it for me</b><small>Our team designs your graphics from your brief, with a proof to approve.</small><em>+ £50 + VAT</em></span></label>
      </div></fieldset>
      <div class="ms-summary" aria-live="polite">
        <div><small>Your selection</small><b class="ms-sum-name">{escape(variant_label(variants[0]))}</b><span class="ms-sum-opt">Simple graphics · Single colour</span></div>
        <div class="ms-sum-price"><b>£{first.get("single", fp)}</b><small>+ VAT</small><span class="ms-sum-inc"></span></div>
      </div>
      <p class="ms-earn" data-earn-points hidden></p>
      <div class="ms-buyrow"><label class="ms-qty"><span>Qty</span><input type="number" name="qty" value="1" min="1" max="20" inputmode="numeric"></label>
      <button type="button" class="btn ms-cta" data-image="{main}" data-path="{fam['path']}" data-title="{full}">Add to basket</button></div>
      <button type="button" class="btn outline ms-ask">Ask a question about this van</button>
      <p class="ms-note">Pay securely online. At checkout choose delivery as a DIY kit, or fitting at our Norwich workshop (fitting is booked and priced after your order). Half and full wraps are quoted per van.</p>
      {rcg}
    </form>
    <ul class="ms-ticks"><li>Laid out on your exact model template</li><li>Proof to approve before anything is printed</li><li>Premium cast vinyl, printed in-house</li><li>Fitted at our St Faiths Road workshop</li></ul>
  </div>
</div></section>
<section class="section ms-details"><div class="shell ms-details__grid">
  <div><p class="eyebrow blue">About this model</p><h2>Graphics planned around the {full}.</h2><p>{panels}</p><div class="tip-box"><b>Fitting tip</b><p>{tip}</p></div></div>
  <div class="ms-included"><h3>What each option includes</h3>
    <dl><dt>Simple graphics</dt><dd>Your name, logo, services and contact details with stripes or shapes in one, two or full colour, laid out on the {full} template. Fixed price by variant.</dd>
    <dt>Half wrap</dt><dd>Printed colour over the rear half, lower sides or a sweep, with lettering on the paint. Quoted once we know the coverage. <a href="/partial-van-wraps-norwich/">About partial wraps</a></dd>
    <dt>Full wrap</dt><dd>Printed imagery or a colour change across almost every painted panel. Quoted per van. <a href="/full-van-wraps-norwich/">About full wraps</a></dd></dl></div>
</div></section>
<section class="section ms-table tint"><div class="shell"><p class="eyebrow blue">Variants &amp; prices</p><h2>Every {full} we have templates for.</h2>
<div class="table-wrap"><table class="ms-variants"><thead><tr><th>Variant</th><th>Single colour</th><th>Two colour</th><th>Full colour</th><th>Half wrap</th><th>Full wrap</th></tr></thead><tbody>{rows}</tbody></table></div>
<p class="core-note">Graphics prices + VAT. Wraps are quoted per van. Can’t see your variant? Send the registration and we’ll check.</p></div></section>
{f'<section class="section ms-related"><div class="shell"><p class="eyebrow blue">More {escape(label)} models</p><h2>Other {escape(label)} vans.</h2><div class="ms-rel-grid">{related}</div></div></section>' if related else ''}'''
