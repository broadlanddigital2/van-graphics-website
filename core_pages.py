"""Render the shared 17-section service layout."""

from html import escape
from urllib.parse import urlencode

from core_content import BRANDS, CONTENT, FEATURED_SECTORS, GUIDES, MODELS, SECTOR_CARDS, SECTORS, TOWNS, VAN_BRANDS, brand_logo

ARROW = '<span class="arr" aria-hidden="true">↗</span>'
PRICE_SOURCE = 'https://broadlanddigital.co.uk/product/pro-large-van-graphics/'

def section(number, key, label, title, body, style=''):
    colour = 'accent' if 'dark-section' in style else 'blue'
    return f'''<section class="section core-section {style}" id="{key}"><div class="shell">
    <div class="section-head"><div><p class="eyebrow {colour}">{number:02d} / {label}</p><h2>{title}</h2></div></div>{body}</div></section>'''

def link_tiles(entries, destination):
    return '<div class="tile-grid">' + ''.join(
        f'<a class="tile" href="{destination(slug)}"><strong>{escape(record[0])}</strong>{ARROW}'
        + (f'<small>{escape(record[1])}</small>' if len(record)==2 else '') + '</a>'
        for slug,record in entries
    ) + '</div>'

def asset(image):
    name = f'concept-{image}' if isinstance(image,int) else image
    return f'/assets/{name}.webp'

def van_diagram(coverage):
    style = {
        'graphics':'<path d="M165 54h100v17H165zm0 26h69v8h-69zm0 14h51v7h-51z" fill="#4667bf"/>',
        'partial':'<path d="M279 31h83v97h-184z" fill="#4667bf"/><path d="M254 90l54-59h19l-72 81z" fill="#d9f64c"/><path d="M267 107h71v9h-71z" fill="white"/>',
        'full':'<path d="M0 0h365v140H0z" fill="#4667bf"/><path d="M0 103l365-60v94H0z" fill="#182e63"/><path d="M198 134l98-104h23L220 134z" fill="#d9f64c"/><path d="M159 51h115v16H159zm0 23h79v8h-79z" fill="white"/>',
    }[coverage]
    body = 'M20 94l14-14 26-45q6-10 19-10h228q17 0 18 16l9 70q1 11-12 11H31q-13 0-13-10V99q0-3 2-5z'
    # A nested viewport clips artwork to the van without shared SVG IDs.
    body_art = f'<svg x="18" y="25" width="317" height="98" viewBox="18 25 317 98"><path d="{body}" fill="#eef1eb"/>{style}</svg>'
    ident = f'van-{coverage}'
    return f'''<svg viewBox="0 0 350 150" aria-hidden="true" focusable="false"><defs><clipPath id="{ident}"><path d="{body}"/></clipPath></defs>
    <path d="{body}" fill="#eef1eb"/><g clip-path="url(#{ident})">{body_art}</g><path d="{body}" fill="none" stroke="#202c37" stroke-width="3"/>
    <path d="M70 38h41v41H45zm53 1h13v39h-13z" fill="#273b4b"/><path d="M117 36v80m26-83v82m149-78v78m-139-37h15" stroke="#263c49" stroke-width="1.5" fill="none"/>
    <path d="M26 102h14m276-45h9m-9 7h10" stroke="#e18453" stroke-width="4" fill="none"/><circle cx="77" cy="122" r="19" fill="#22303c"/><circle cx="278" cy="122" r="19" fill="#22303c"/><circle cx="77" cy="122" r="8" fill="#acb7b9"/><circle cx="278" cy="122" r="8" fill="#acb7b9"/></svg>'''

def gallery(data):
    models = dict.fromkeys(model for _,model,_ in data['gallery'])
    options = ''.join(f'<option>{escape(model)}</option>' for model in models)
    figures = ''.join(f'''<figure data-model="{escape(model)}"><img src="{asset(image)}" alt="{escape(caption)}" loading="lazy" width="840" height="473"><figcaption><strong>{escape(caption)}</strong><small>{escape(model)}</small></figcaption></figure>'''
                      for image,model,caption in data['gallery'])
    from work_gallery import work_gallery
    return work_gallery() + f'''<div class="gallery-toolbar"><p>Design concepts. Some images show body types where an exact model is unspecified.</p><label>Filter by vehicle model <select id="gallery-model"><option value="">All vehicles</option>{options}</select></label><span id="gallery-count" role="status">{len(data['gallery'])} designs</span></div>
    <div class="core-gallery">{figures}</div>'''

def table(caption, headings, rows):
    head = ''.join(f'<th scope="col">{heading}</th>' for heading in headings)
    body = ''.join(f'<tr><th scope="row">{row[0]}</th>' + ''.join(f'<td>{cell}</td>' for cell in row[1:]) + '</tr>' for row in rows)
    return f'<div class="table-wrap" role="region" aria-label="{escape(caption)}" tabindex="0"><table><caption class="sr-only">{caption}</caption><thead><tr>{head}</tr></thead><tbody>{body}</tbody></table></div>'

def pricing(data):
    rows = list(zip(('Small van','Medium van','LWB van','Luton'),('Caddy or Berlingo','Transit Custom or Vivaro','Long-wheelbase Transit or Sprinter','Box body with or without tail lift'),data['pricing']))
    return (table('Price guide by vehicle size',('Vehicle size','Example','Fitted price guide'),rows)
            + f'<p class="core-note">{data["price_note"]} <a href="{PRICE_SOURCE}">View the published package guide {ARROW}</a></p><p class="core-note"><strong>What changes the price?</strong> {data["price_factor"]}</p>')

def comparison(data):
    rows = [
        ('Van signwriting', 'Cut letters and individual graphics', 'Clear logos and contact information', '/van-signwriting-norwich/'),
        ('Partial wrap', 'Selected panels or sections', 'More colour and imagery with some original paint visible', '/vehicle-wraps-norwich/'),
        ('Full wrap', 'Most exterior body panels', 'A broader colour change or printed livery', '/vehicle-wraps-norwich/'),
    ]
    if data['key']=='wraps':
        rows.append(('Paint', 'Repainted panels or body', 'A paint finish or bodywork restoration', '/guides/wrap-vs-paint/'))
    elif data['key']=='fleet':
        rows.append(('Fleet graphics', 'Choose coverage for each vehicle', 'One master design across several vehicles', '/fleet-graphics-norwich/'))
    links = [(f'<a href="{href}">{name}</a>', coverage, purpose) for name,coverage,purpose,href in rows]
    diagrams = ''.join(f'<figure>{van_diagram(kind)}<figcaption>{label}</figcaption></figure>'
                      for kind,label in [('graphics','Individual graphics'),('partial','Partial wrap'),('full','Full wrap')])
    return table('Vehicle graphics and wrap comparison',('Option','Typical coverage','Best suited to'),links)+f'<div class="coverage-diagrams" aria-label="Illustrative van coverage">{diagrams}</div>'

ICON_PATHS = {
    'design':'<path d="m4 17 12-12 3 3L7 20H4zM14 7l3 3"/>',
    'proof':'<rect x="4" y="4" width="16" height="16" rx="2"/><path d="m8 12 3 3 5-6"/>',
    'film':'<path d="m3 8 9-5 9 5-9 5-9-5zm0 4 9 5 9-5m-18 4 9 5 9-5"/>',
    'fit':'<path d="m5 14 6-6 5 5-6 6H5zm6-6 3-3h5v5l-3 3"/>',
    'shield':'<path d="M12 3c2 2 5 3 8 3v5c0 5-4 8-8 10-4-2-8-5-8-10V6c3 0 6-1 8-3z"/><path d="m8 12 3 3 5-5"/>',
    'care':'<path d="M12 3c3 4 6 7 6 11a6 6 0 0 1-12 0c0-4 3-7 6-11z"/><path d="M9 15c0 1 1 2 2 2"/>',
}

def info_cards(entries, icons=False):
    items = []
    for key, title, desc in entries:
        icon = f'<svg class="core-icon" viewBox="0 0 24 24" aria-hidden="true" fill="none" stroke="currentColor" stroke-width="1.7" stroke-linecap="round" stroke-linejoin="round">{ICON_PATHS[key]}</svg>' if icons else f'<b class="core-index">{key}</b>'
        items.append(f'<article>{icon}<h3>{title}</h3><p>{desc}</p></article>')
    return '<div class="info-cards">' + ''.join(items) + '</div>'

def included(service, data):
    return info_cards([
        ('design','Design',f'Artwork planned for {service["label"].lower()} and the panels you want to use.'),
        ('proof','Proofs','Review your wording, placement and coverage before signing off the layout.'),
        ('film','Vinyl specification',data['materials']),
        ('fit','Fitting','Production and fitting are arranged with our Norwich team.'),
        ('shield','Warranty terms','Ask which manufacturer and installation terms apply to the specified film, panels and vehicle condition.'),
        ('care','Aftercare','Get care instructions for the chosen film and advice on cleaning around edges and joins.'),
    ], True)

def benefits(data):
    reach = {'signwriting':'Make your name and contact details visible between jobs.',
             'wraps':'Give promotional artwork a larger space to be seen when parked or on the move.',
             'fleet':'Put a recognisable brand on vehicles across different routes.'}[data['key']]
    return info_cards([
        ('01','Advertising reach',reach),
        ('02','Covered paint','Film forms a layer over covered panels. Coverage and film type determine the level of protection.'),
        ('03','Resale flexibility','Professional removal can make a vehicle easier to present for resale. The result depends on the condition of the paint and film.'),
        ('04','Lease handback','Confirm the lease provider’s requirements first and plan removal in advance.'),
        ('05','Brand consistency','Repeat approved colours, logos and contact details across vehicles and other signage.'),
        ('06','Business expense','Ask your accountant how to treat vehicle branding for your business. <a href="https://www.gov.uk/expenses-if-youre-self-employed/marketing-entertainment">HMRC guidance for the self-employed</a>.'),
    ])

def materials(data):
    return f'''<div class="core-prose"><p>{data["materials"]}</p><dl class="spec-list">
    <div><dt>Cast vs calendered</dt><dd>Cast vinyl conforms to more complex bodywork. Suitable calendered film can work on flatter areas and simpler curves. The exact product and surface determine suitability.</dd></div>
    <div><dt>Brands used</dt><dd>3M and Metamark are examples to discuss. Ask for the product and finish on your quote.</dd></div>
    <div><dt>Lifespan</dt><dd>Film, panel angle, care and exposure all matter. As one product example, 3M 2080 lists up to eight years on qualifying vertical applications and up to three on horizontal applications. Check the applicable product terms.</dd></div>
    <div><dt>Finishes</dt><dd>Ask about gloss, matt, satin, chrome-effect or reflective film. Speciality finishes can have different fitting, care and durability requirements.</dd></div></dl>
    <a class="text-link" href="https://broadlanddigital.co.uk/vehicle-graphics/">Broadland Digital material guidance {ARROW}</a></div>'''

def timeline(data):
    proof, fit = data['timing']
    entries = [('Consultation','Day 1 or by arrangement','Send photos, model, coverage and your preferred fitting dates.'),
               ('Design &amp; proof','Time varies by artwork',proof),
               ('Production','After proof approval','The team confirms the production window after checking the film, printing and any laminate.'),
               ('Fitting','By appointment in Norwich',fit),
               ('Handover','On completion','Check the work with the team and get cleaning and care instructions.')]
    return '<ol class="timeline">' + ''.join(f'<li><span>{i:02d}</span><h3>{h}</h3><b>{when}</b><p>{detail}</p></li>'
                                                for i,(h,when,detail) in enumerate(entries,1))+'</ol><p class="core-note">Planning estimates only. The workshop confirms dates and downtime with your quote.</p>'

def case_study(data):
    title, brief, outcome, pictures = data['case']
    images = ''.join(f'<img src="{asset(pic)}" alt="Vehicle graphics concept used to illustrate this brief" loading="lazy" width="840" height="473">' for pic in pictures)
    return f'''<div class="study"><div><h3>{title}</h3><p><strong>The brief</strong><br>{brief}</p><p><strong>The design outcome</strong><br>{outcome}</p></div><div class="study-images">{images}</div></div>'''

REVIEWS_WIDGET = 'https://www.local-marketing-reports.com/external/showcase-reviews/widgets/1e3e700f5ddf21a13ff257d1f4ef7f02c7237aef'
REVIEWS_EMBED = 'https://www.local-marketing-reports.com/external/showcase-reviews/embed/1e3e700f5ddf21a13ff257d1f4ef7f02c7237aef?id=18987'

GOOGLE_REVIEWS = [  # Broadland Digital's Google reviews (vehicle graphics jobs)
    ('Daniel Ellert', 'September 2025', 'Helpful and professional. Now have a great new livery on my van. Reasonable price, and good quality, even overcame a small issue with my van on the day!'),
    ('Andy', 'August 2025', 'From first contact, taking vehicle to the guys to choose what type of wrap and get their suggestions to the fitment the whole process was friendly and professional and at a reasonable price. Would definitely use again. Thank you.'),
    ('Simon Bainbridge', 'July 2025', 'Friendly staff, quick installation of van graphics and they look awesome. I highly recommend Race Car Graphics and their sister company Broadland Digital to everyone!'),
    ('Iwan Utting', 'November 2025', 'Brilliant service, quickly and very good quality! Also very welcoming!'),
]
GOOGLE_URL = 'https://www.google.com/maps/place/Broadland+Digital,+Signs+%26+Graphics/@52.6610201,1.2806856,17z/'

def reviews(data=None):
    """Summary panel plus four Google review cards for Broadland Digital, our parent company."""
    cards = ''.join(f'''<article class="review-card"><p class="review-card__stars" aria-label="5 out of 5">★★★★★</p><blockquote>{escape(text)}</blockquote>
    <footer><span class="review-card__avatar" aria-hidden="true">{escape(name[0])}</span><span><b>{escape(name)}</b><small>Google review · {when}</small></span></footer></article>''' for name, when, text in GOOGLE_REVIEWS)
    return (f'''<div class="reviews-block"><div class="reviews-block__summary"><p class="reviews-stars" aria-label="Rated 5 out of 5">★★★★★</p>
    <p class="reviews-score"><b>5.0</b> on Google</p><p>From 23 reviews of Broadland Digital, the Norwich workshop that designs, prints and fits our vehicle graphics.</p>
    <a class="text-link" href="{GOOGLE_URL}" target="_blank" rel="noopener">Read all reviews on Google {ARROW}</a></div>
    <div class="review-cards">{cards}</div></div>''')

def enquiry(service, services, phone, tel, email, quote_url, *, context='', contact=False):
    options = '' if service else '<option>General enquiry</option>'
    options += ''.join(f'<option{" selected" if item == service else ""}>{item["label"]}</option>' for item in services)
    heading = 'How can we help?' if contact else 'Tell us about the vehicle.'
    eyebrow = 'Contact the team' if contact else '16 / Get a free quote' if service else 'Get a free quote'
    vehicle_required = ' required' if service else ''
    return f'''<section class="quote" id="quote"><div class="shell quote-grid core-quote">
    <div><p class="eyebrow">{eyebrow}</p><h2>{heading}</h2>
    <p>Send us a few details and we’ll come back with design ideas and a fitted price. Prefer to talk? Call the Norwich team.</p>
    <ul class="quote-ticks"><li>Free design visual on your exact vehicle</li><li>Fitted price in writing, VAT shown</li><li>Designed, printed and fitted in Norwich</li></ul>
    <div class="quote-contacts"><a href="{tel}"><small>Call</small><b>{phone}</b></a><a href="mailto:{email}"><small>Email</small><b>{email}</b></a></div>
    <p class="quote-alt"><a class="text-link" href="{quote_url}">Or use the Broadland Digital web form {ARROW}</a></p></div>
    <form id="service-enquiry" class="quote-card" data-recipient="{email}" data-context="{escape(context)}">
    <div class="quote-card__head"><b>Quote request</b><span>Takes about a minute</span></div>
    <label>Service<select name="service">{options}</select></label>
    <div class="field-row"><label>Name<input name="name" autocomplete="name" required maxlength="100"></label><label>Email<input type="email" name="email" autocomplete="email" required maxlength="150"></label></div>
    <div class="field-row"><label>Phone (optional)<input type="tel" name="phone" autocomplete="tel" maxlength="30"></label>
    <label>Vehicle make and model{'' if service else ' (optional)'}<input name="vehicle"{vehicle_required} maxlength="120" placeholder="e.g. Ford Transit Custom"></label></div>
    <label>Postcode (optional)<input name="postcode" autocomplete="postal-code" maxlength="10" placeholder="e.g. NR6 6AQ"></label>
    <label>{'How can we help?' if contact else 'Project details'}<textarea name="details" rows="4" maxlength="1200" required placeholder="Tell us what you need"></textarea></label>
    <button class="btn dark" type="submit" disabled>Submit request {ARROW}</button><p id="enquiry-status" role="status" hidden></p>
    <p class="form-privacy"><a href="https://broadlanddigital.co.uk/privacy-policy/">Privacy policy</a></p>
    <noscript><p><a href="{quote_url}">Use the web enquiry form</a>.</p></noscript>
    </form></div></section>'''

OTHER_ICON = ('<svg viewBox="0 0 64 40" aria-hidden="true" focusable="false"><circle cx="32" cy="20" r="15" fill="none" stroke="#273b4b" stroke-width="3"/>'
              '<path d="M27 16a5 5 0 1 1 7 4.6c-1.4.6-2 1.4-2 2.9V25" fill="none" stroke="#273b4b" stroke-width="3" stroke-linecap="round"/><circle cx="32" cy="30" r="1.9" fill="#273b4b"/></svg>')


def brand_card(href, logo, name, action):
    return (f'<a class="brand-card" href="{href}" role="listitem"><span class="brand-card__logo">{logo}</span>'
            f'<span class="brand-card__copy"><strong>{escape(name)}</strong><b>{action} <span aria-hidden="true">→</span></b></span></a>')


def brand_img(key, label, size=480):
    logo = brand_logo(key)
    if logo:
        return f'<img src="{logo}" alt="{escape(label)} van graphics Norwich" width="{size}" height="{size}" decoding="async">'
    return f'<span class="brand-wordmark" aria-hidden="true">{escape(label)}</span>'


def vehicle_picker():
    """Manufacturer grid in the Race Car Graphics style: square logo tiles, 4 across, each opening a brand page."""
    cards = ''.join(brand_card(f'/vehicles/{key}/', brand_img(key, label), label, 'Explore graphics') for key, label in VAN_BRANDS)
    cards += brand_card('#quote', OTHER_ICON, 'Other makes', 'Tell us what you drive')
    return f'''<div class="vehicle-picker">
    <p>Choose your van manufacturer to see its models, then pick your model for layout advice.</p>
    <div class="brand-grid" role="list" aria-label="Van manufacturers">{cards}</div></div>'''


import json as _json, re as _re
from pathlib import Path as _P
_VAN_MODELS = _json.loads(_P('van_models.json').read_text(encoding='utf-8'))
_STOP_FAM = _re.compile(r'^(\d{4}\+?|\d{2,4}-\d{2,4}|onwards|cab\d.*|L[1-5]|H[1-3]|SWB|MWB|LWB|ELWB|HR|MR|SHR|EHR|EXHR|NSLD|NLD|Dropside|Chassis|Luton|Crew|Box|Low|Double|Single|Extended|UTE|First|Reg|Club|Tailgate)$', _re.I)
FAMILY_RENAME = {('ford', 'custom'): 'Transit Custom', ('ford', 'custom ms-rt'): 'Transit Custom MS-RT', ('ford', 'connect'): 'Transit Connect', ('ford', 'courier'): 'Transit Courier'}
FAMILY_PAGES = {('ford', 'transit custom'): 'transit-custom', ('ford', 'transit connect'): 'transit-connect', ('ford', 'transit'): 'ford-transit',
                ('vauxhall', 'vivaro'): 'vivaro', ('vauxhall', 'combo'): 'vauxhall-combo', ('vauxhall', 'movano'): 'vauxhall-movano',
                ('volkswagen', 'caddy'): 'caddy', ('volkswagen', 'transporter'): 'vw-transporter', ('volkswagen', 'crafter'): 'vw-crafter',
                ('citroën', 'berlingo'): 'berlingo', ('citroën', 'dispatch'): 'citroen-dispatch', ('citroën', 'relay'): 'citroen-relay',
                ('peugeot', 'partner'): 'partner', ('peugeot', 'expert'): 'peugeot-expert', ('peugeot', 'boxer'): 'peugeot-boxer',
                ('mercedes-benz', 'sprinter'): 'sprinter', ('mercedes-benz', 'vito'): 'mercedes-vito', ('mercedes-benz', 'citan'): 'mercedes-citan'}

def van_families(label):
    """All van models we hold templates for (the Race Car Graphics catalogue), grouped by model family."""
    models = next((v for k, v in _VAN_MODELS.items() if k.lower() == label.lower()), [])
    fams = {}
    for m in models:
        words = m.split()
        i = 0
        while i < len(words) and not _STOP_FAM.match(words[i]):
            i += 1
        fam = ' '.join(words[:i]) or words[0]
        variant = ' '.join(words[i:]) if i else ' '.join(words[1:])
        fam = FAMILY_RENAME.get((label.lower(), fam.lower()), fam)
        fams.setdefault(fam, []).append(variant or 'All years')
    return sorted(fams.items(), key=lambda kv: (-len(kv[1]), kv[0]))

def brand_page(key):
    """A manufacturer page: its models as cards (where we have model pages), plus routes to the Van Designer and a quote."""
    label = dict(VAN_BRANDS)[key]
    slugs = BRANDS.get(key, (label, ()))[1]
    families = van_families(label)
    if families:
        cards = ''
        for fam, variants in families:
            slug = FAMILY_PAGES.get((label.lower(), fam.lower()))
            shown = variants[:8]
            chips = ''.join(f'<li>{escape(v)}</li>' for v in shown)
            more = (f'<details><summary>+{len(variants) - 8} more</summary><ul class="fam-chips">' + ''.join(f'<li>{escape(v)}</li>' for v in variants[8:]) + '</ul></details>') if len(variants) > 8 else ''
            link = (f'<a class="text-link" href="/vehicles/{slug}/">{escape(label)} {escape(fam)} graphics {ARROW}</a>' if slug
                    else f'<a class="text-link" href="#quote">Quote for my {escape(fam)} {ARROW}</a>')
            cards += (f'<article class="fam-card{" has-page" if slug else ""}"><div class="fam-card__head"><h3>{escape(label)} {escape(fam)}</h3>'
                      f'<small>{len(variants)} version{"s" if len(variants) != 1 else ""}</small></div>'
                      + (f'<ul class="fam-chips">{chips}</ul>{more}' if any(variants) else '') + link + '</article>')
        total = sum(len(v) for _, v in families)
        models_block = f'''<div class="section-head"><div><p class="eyebrow blue">Every {escape(label)} model</p><h2>{escape(label)} models we fit.</h2></div>
    <p>Signwriting, wraps and fleet graphics for {total} {escape(label)} body styles and model years. Find yours, then send the photos for a fitted quote.</p></div><div class="fam-grid">{cards}</div>
    <p class="core-note">Model not listed? <a href="#quote">Tell us what you drive</a> and we will plan the layout for it.</p>'''
    elif slugs:
        models = ''.join(
            f'<a class="model-card" href="/vehicles/{slug}/"><small>{escape(MODELS[slug][1])}</small><h3>{escape(MODELS[slug][0])}</h3>'
            f'<p>{escape(MODELS[slug][2].split(". ")[0])}.</p><b>View graphics {ARROW}</b></a>'
            for slug in slugs)
        models_block = f'''<div class="section-head"><div><p class="eyebrow blue">Choose your model</p><h2>{escape(label)} models.</h2></div>
    <p>Pick your model for layout advice, then send the year, wheelbase and photos for a fitted quote.</p></div><div class="model-grid">{models}</div>
    <p class="core-note">Model not listed? <a href="#quote">Tell us what you drive</a> and we will plan the layout for it.</p>'''
    else:
        models_block = f'''<div class="section-head"><div><p class="eyebrow blue">Your {escape(label)} van</p><h2>Graphics planned for your model.</h2></div>
    <p>We lay out every design around the exact model, year, wheelbase and body style.</p></div>
    <div class="info-cards"><article><b class="core-index">01</b><h3>Tell us the model</h3><p>Send the model, year, wheelbase or body length and photos of both sides and the rear.</p></article>
    <article><b class="core-index">02</b><h3>Try a look online</h3><p>Use the free <a href="/design-your-van/">Van Designer</a> to compare graphics and a full wrap before you brief us.</p></article>
    <article><b class="core-index">03</b><h3>Approve your proof</h3><p>We send a proof for your {escape(label)} and fit the graphics at our Norwich workshop.</p></article></div>'''
    return f'''<section class="support-hero brand-hero"><div class="shell"><nav class="crumb" aria-label="Breadcrumb"><a href="/">Home</a><span aria-hidden="true">/</span><a href="/vehicles/">Van manufacturers</a><span aria-hidden="true">/</span><span>{escape(label)}</span></nav>
    <div class="brand-hero__grid"><div><p class="eyebrow accent">Van graphics by manufacturer</p><h1>{escape(label)} van graphics in Norwich.</h1>
    <p class="brand-hero__lede">Signwriting, partial and full wraps and fleet graphics designed around your {escape(label)} van, then produced and fitted at our Norwich workshop.</p>
    <div class="actions"><a class="btn" href="#models">{'Choose your model' if (slugs or families) else 'Plan your graphics'} {ARROW}</a><a class="btn outline" href="/design-your-van/#designer">Design your van {ARROW}</a></div></div>
    <span class="brand-hero__logo">{brand_img(key, label)}</span></div></div></section>
    <section class="section core-section" id="models"><div class="shell">{models_block}</div></section>
    <section class="section core-section"><div class="shell"><div class="section-head"><div><p class="eyebrow blue">What we fit</p><h2>{escape(label)} van wraps and signwriting.</h2></div>
    <p>{escape(label)} vehicle graphics for businesses across Norwich and Norfolk, designed in-house and fitted at our workshop on Vulcan Road North.</p></div>
    <div class="info-cards"><article><h3>{escape(label)} signwriting</h3><p>Cut vinyl lettering for your name, services and contact details, placed around the doors, handles and panel lines of your {escape(label)}. From £149 for a small van.</p></article>
    <article><h3>{escape(label)} van wraps</h3><p>Partial wraps over selected panels or a full wrap for maximum impact, printed in-house on quality cast film.</p></article>
    <article><h3>{escape(label)} fleet graphics</h3><p>One consistent livery adapted to every {escape(label)} model you run, with fleet numbers and files kept on record.</p></article></div></div></section>
    <section class="section core-section tint"><div class="shell"><div class="section-head"><div><p class="eyebrow blue">Other manufacturers</p><h2>Browse another brand.</h2></div></div>{vehicle_picker()}</div></section>'''


def sector_cards(keys=SECTOR_CARDS):
    cards = ''.join(
        f'<a class="card" href="/sectors/{key}/"><div class="card-image">'
        f'<img src="{asset(image)}" alt="{escape(alt)}" width="840" height="473" loading="lazy"></div>'
        f'<div class="card-copy"><h3>{escape(SECTORS[key][0])}</h3><p>{escape(description)}</p>'
        f'<strong>Explore sector {ARROW}</strong></div></a>'
        for key in keys
        for image, alt, description in (SECTOR_CARDS[key],)
    )
    return f'<div class="cards sector-cards">{cards}</div>'


def core_sections(service, faq):
    data = CONTENT[service['slug']]
    intro = '<div class="core-prose">' + ''.join(f'<p>{line}</p>' for line in data['intro']) + '</div>'
    towns = [(key, (label, 'Fitting in Norwich')) for key,(label,_) in TOWNS.items()]
    guides = [(key,(GUIDES[key][0],)) for key in data['guides']]
    return ''.join([
        section(2,'intro','The service',service['heading'],intro),
        section(3,'gallery','Design gallery','Explore the possibilities.',gallery(data),'dark-section'),
        section(4,'included','What’s included','From first proof to fitted finish.',included(service,data)),
        section(5,'pricing','Price guide','Budget by vehicle size.',pricing(data),'tint'),
        section(6,'comparison','Compare your options','Choose your coverage.',comparison(data)),
        section(7,'benefits','Benefits','Make more of your vehicle.',benefits(data),'tint'),
        section(8,'materials','Vinyl &amp; materials','Choose the right film.',materials(data)),
        section(9,'timeline','Fitting timeline','Plan the work around your vehicle.',timeline(data),'tint'),
        section(10,'vehicles','Vehicles we work on','Choose by brand and model.',vehicle_picker()),
        section(11,'sectors','Sectors','Graphics for your line of work.',sector_cards(FEATURED_SECTORS)+f'<p class="core-note"><a class="text-link" href="/sectors/">See all {len(SECTORS)} sectors {ARROW}</a></p>','tint'),
        section(12,'reviews','Customer reviews','Published customer feedback.',reviews(data)),
        section(13,'areas','Norwich &amp; Norfolk','Serving businesses across Norfolk.',link_tiles(towns,lambda slug:f'/norfolk/{slug}/#{data["key"]}'),'local'),
        section(14,'guides','Related guides','Get ready for your project.',link_tiles(guides,lambda slug:f'/guides/{slug}/')),
        faq(service['questions']+data['faq']),
    ])

def support_page(label, heading, paragraphs, services, context='', extra=''):
    copy = ''.join(f'<p>{escape(p)}</p>' for p in paragraphs)
    cards = ''.join(f'''<article id="{CONTENT[s["slug"]]["key"]}"><h3>{s["label"]}</h3><p>{escape(s["short"])} {escape(context)}</p>
    <a class="text-link" href="/{s["slug"]}/">{s["label"]} in Norwich {ARROW}</a></article>''' for s in services)
    return f'''<section class="support-hero"><div class="shell"><a class="crumb" href="/">← Vehicle graphics home</a>
    <p class="eyebrow accent">{label}</p><h1>{escape(heading)}</h1></div></section><section class="section core-section"><div class="shell">
    <div class="core-prose">{copy}</div>{extra}<h2 class="support-links__title">Related services</h2><div class="info-cards support-links">{cards}</div></div></section>'''


def care_upsell(vehicle='your van'):
    """Before-and-after care from Auto Opulence, our sister vehicle care business."""
    v = escape(vehicle)
    before = [('Decontamination wash', f'A deep clean, including a clay bar treatment, removes the road film and wax that stop vinyl bonding properly to your {v}.'),
              ('Machine polish', 'Tired, dull paint can be machine polished before signwriting or a partial wrap, so the paint left on show looks as good as the new graphics.')]
    after = [('Ceramic coating', 'Protect the painted panels around your graphics with a long-lasting ceramic coating that makes washing quicker and keeps the gloss.'),
             ('Regular hand wash', 'Gentle hand washing that is safe for vinyl, so your graphics and paint stay clean without brushes or harsh chemicals.')]
    col = lambda items: ''.join(f'<div class="care-item"><h4>{t}</h4><p>{d}</p></div>' for t, d in items)
    return (f'<section class="section care-upsell"><div class="shell"><div class="section-head"><div><p class="eyebrow accent">Before &amp; after your graphics</p>'
            f'<h2>Prep and protect your {v}.</h2></div><p>Our sister business Auto Opulence offers valeting, polishing and ceramic coating in Norwich. Add it to your booking and your {v} arrives ready for graphics and leaves protected.</p></div>'
            f'<div class="care-grid"><div class="care-col"><p class="care-label">Before fitting</p>{col(before)}</div>'
            f'<div class="care-col is-after"><p class="care-label">After fitting</p>{col(after)}</div></div>'
            f'<div class="care-actions"><a class="btn" href="#quote">Add vehicle care to my quote {ARROW}</a><a class="btn outline" href="https://autoopulence.co.uk/" target="_blank" rel="noopener">See Auto Opulence services ↗</a>'
            '<span class="care-note">Washing from £30 · Valeting from £40 · Polishing from £295, prices from Auto Opulence.</span></div></div></section>')


def repair_block(vehicle='your van'):
    """Panel repairs organised as part of the graphics job."""
    v = escape(vehicle)
    points = ['Dents, scrapes and scuffed panels', 'Rust spots and chipped paint', 'Damaged bumpers and trims']
    return (f'<section class="section repair-block"><div class="shell"><div class="repair-card">'
            f'<div class="repair-card__icon" aria-hidden="true"><svg viewBox="0 0 24 24" width="34" height="34" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M14.7 6.3a4 4 0 0 0-5.4 5.4L3 18l3 3 6.3-6.3a4 4 0 0 0 5.4-5.4l-2.5 2.5-2.4-.6-.6-2.4z"/></svg></div>'
            f'<div class="repair-card__copy"><p class="eyebrow accent">Vehicle damaged?</p><h2>We can organise panel repairs.</h2>'
            f'<p>Graphics look their best on straight, sound panels, and vinyl cannot hide dents or rust. If your {v} needs some bodywork first, we can organise panel repairs as part of the service, so it comes back repaired and branded in one go.</p>'
            f'<ul>{"".join(f"<li>{p}</li>" for p in points)}</ul></div>'
            f'<div class="repair-card__cta"><a class="btn" href="#quote">Ask for details and a quote {ARROW}</a><span>Send photos of the damage with your enquiry and we will include the repair in your quote.</span></div>'
            '</div></div></section>')
