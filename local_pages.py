"""Page sections for sector, location and contact routes.

town_page()   -> 18-section location template (see scope doc, Locations).
sector_page() -> sector template (challenge, must-haves, gallery, package,
                 prices, tips, featured design, designer strip, related).
sectors_hub() -> grouped /sectors/ index.
"""

from html import escape
from urllib.parse import urlencode

from areas import TOWN_LIST, TOWNS_BY_KEY
from core_content import CONTENT, SECTOR_CARDS, SECTORS
from core_pages import ARROW, asset, case_study, info_cards, link_tiles, pricing, reviews, section, sector_cards, table
from sector_data import GROUPS, SECTOR_LIST, SECTORS_BY_KEY, cap

ADDRESS = 'Vulcan House, Vulcan Road North, Norwich NR6 6AQ'
MAP_QUERY = f'Broadland Digital, {ADDRESS}'


def directions(town=None, county='Norfolk'):
    if town:
        return 'https://www.google.com/maps/dir/?' + urlencode(
            {'api': 1, 'origin': f'{town}, {county}, UK', 'destination': MAP_QUERY, 'travelmode': 'driving'})
    return 'https://www.google.com/maps/search/?' + urlencode({'api': 1, 'query': MAP_QUERY})


def workshop_map(phone, tel, email, town=None, county='Norfolk'):
    source = 'https://maps.google.com/maps?' + urlencode({'q': MAP_QUERY, 'output': 'embed'})
    return f'''<div class="workshop-map"><div class="workshop-details">
    <p class="eyebrow blue">Norwich workshop</p><h3>Norwich Vehicle Graphics</h3>
    <address>Vulcan House<br>Vulcan Road North<br>Norwich, Norfolk NR6 6AQ</address>
    <p><a href="{tel}">{phone}</a><br><a href="mailto:{email}">{email}</a></p>
    <p>Call ahead to confirm your fitting appointment and drop-off arrangements.</p>
    <a class="btn dark" href="{escape(directions(town, county))}">{f'Directions from {escape(town)}' if town else 'Get directions'} {ARROW}</a>
    </div><iframe title="Map of the Norwich vehicle graphics workshop" src="{escape(source)}"
    width="640" height="360" loading="lazy" referrerpolicy="strict-origin-when-cross-origin" allowfullscreen></iframe></div>'''


def page_jumps(links):
    return '<nav class="page-jumps" aria-label="On this page"><div class="shell">' + ''.join(
        f'<a href="#{key}">{label}</a>' for key, label in links
    ) + '</div></nav>'


def design_examples(entries):
    grid = 'core-gallery four' if len(entries) == 4 else 'core-gallery'
    return f'<div class="{grid}">' + ''.join(
        f'<figure><img src="{asset(image)}" alt="{escape(caption)}" loading="lazy" width="840" height="473">'
        f'<figcaption><strong>{escape(caption)}</strong></figcaption></figure>'
        for image, caption in entries
    ) + '</div>'


def designer_strip(context):
    return f'''<section class="designer-strip"><div class="shell"><div><p class="eyebrow accent">Free Van Designer</p>
    <h2>See it on your van before you {escape(context)}.</h2><p>Pick your van and colour, add your logo and details, and get three designs in about a minute. Spin it in 360° or picture it on the road.</p></div>
    <a class="btn" href="/design-your-van/#designer">Start designing, free {ARROW}</a></div></section>'''


def process_steps(last):
    return info_cards([
        ('01', 'Send photos or use the Van Designer', 'Share both sides and the rear, your logo and what you want the van to say. Or start with the free Van Designer.'),
        ('02', 'Approve your proof', 'We send a visual of the layout on your vehicle. Changes are made before anything is printed.'),
        ('03', 'Production', 'Graphics are printed, laminated and cut in-house in Norwich.'),
        ('04', last, 'Drop the vehicle at Vulcan Road North on the agreed date and collect it branded and ready to work.'),
    ]).replace('class="info-cards"', 'class="info-cards four"', 1)


# ---------------------------------------------------------------- locations

def town_questions(t):
    name = t['name']
    return t['questions'] + [
        (f'How far is the workshop from {name}?', f'Our workshop at {ADDRESS} is about {t["miles"]} miles from {name}, roughly {t["time"]} by car outside peak times.'),
        (f'Can I start my quote from {name}?', 'Yes. Send photos, the make and model, the coverage you want and your artwork if you have it, or use the free Van Designer. We agree the design before you bring the vehicle in.'),
        ('How much downtime should I plan?', 'Lettering is often done in a day. Partial and full wraps usually take longer, depending on vehicle size and whether old graphics need removing. We confirm timings with your quote.'),
        ('Do you offer fitting at my premises?', 'Standard fitting is at the Norwich workshop, where temperature and lighting are controlled. If you need on-site fitting, tell us your postcode and requirements and we will discuss what is possible.'),
    ]


def town_hero(t, image, alt, phone, tel):
    """Full-bleed hero, same pattern as the sector pages. Uses assets/towns/{key}-hero.webp when added."""
    from pathlib import Path
    dedicated = Path(f'dist/assets/towns/{t["key"]}-hero.webp').exists()
    if dedicated:
        image, alt = f'towns/{t["key"]}-hero', f'Branded work van in {t["name"]}'
    name = escape(t['name'])
    chips = ''.join(f'<li>{c}</li>' for c in (f'{t["miles"]} miles to our workshop', f'About {t["time"]} drive', f'Via the {escape(t["roads"][0])}'))
    focus = ''.join(f'<li><a href="/sectors/{k}/">{escape(SECTORS[k][0])}</a></li>' for k in t['focus'])
    return f'''<section class="sector-hero town-hero{' is-dedicated' if dedicated else ''}">
    <img class="sector-hero__img" src="{asset(image)}" alt="{escape(alt)}" fetchpriority="high" width="2400" height="1100">
    <div class="shell sector-hero__inner"><div class="sector-hero__copy">
    <nav class="crumb" aria-label="Breadcrumb"><a href="/">Home</a><span aria-hidden="true">/</span><a href="/norfolk/">Areas we cover</a><span aria-hidden="true">/</span><span>{name}</span></nav>
    <p class="eyebrow accent">Vehicle graphics · {name}, {escape(t["county"])}</p><h1>Van graphics<span>in {name}.</span></h1>
    <p class="lede">{escape(t["lede"])}</p>
    <div class="actions"><a class="btn" href="#quote">Get a free quote{ARROW}</a><a class="btn outline" href="{escape(directions(t["name"], t["county"]))}">Directions from {name}{ARROW}</a></div>
    <ul class="sector-hero__chips">{chips}</ul></div></div>
    <div class="sector-hero__bar"><div class="shell"><p>Popular in {name}</p><ul>{focus}</ul></div></div></section>'''


def town_page(key, phone, tel, email):
    t = TOWNS_BY_KEY[key]
    name = escape(t['name'])
    focus = t['focus']
    image, alt, _ = SECTOR_CARDS[focus[0]]

    facts = (f'<dl class="fact-list"><div><dt>Distance</dt><dd>{t["miles"]} miles to Vulcan Road North</dd></div>'
             f'<div><dt>Typical drive</dt><dd>About {t["time"]} outside peak hours</dd></div>'
             f'<div><dt>Main roads</dt><dd>{escape(", ".join(t["roads"]))}</dd></div></dl>')
    intro = f'''<div class="intro-grid"><div class="core-prose"><p>{escape(t["intro"])}</p><p>Everything is designed, printed and fitted by our own team in Norwich. You can start with the free <a href="/design-your-van/">Van Designer</a>, send us photos for a quote, or call {phone}.</p></div>{facts}</div>'''

    tiles = [
        ('signwriting', 'Van signwriting', 'Cut vinyl lettering, logos and contact details. The fastest, most affordable way to brand a work van.', '/van-signwriting-norwich/'),
        ('wraps', 'Partial wraps', 'Printed panels or colour across selected areas, using your van’s paint as part of the design.', '/vehicle-wraps-norwich/#comparison'),
        ('full-wrap', 'Full wraps', 'Printed imagery or a complete colour change across the main exterior panels.', '/vehicle-wraps-norwich/'),
        ('fleet', 'Fleet graphics', 'One design adapted to every make and model, fitted in batches around your schedule.', '/fleet-graphics-norwich/'),
    ]
    services = '<div class="info-cards support-links service-grid">' + ''.join(
        f'<article id="{k}"><h3>{label}</h3><p>{copy}</p><a class="text-link" href="{href}">{label} for {name} {ARROW}</a></article>'
        for k, label, copy, href in tiles) + '</div>'

    prices = price_cards(None) + '<p class="core-note">Signwriting prices are Broadland Digital’s <a href="/van-signwriting-norwich/#pricing">published fitted packages</a>. Wraps and fleets get a written quote covering your vehicle size, artwork, film, coverage and VAT.</p>'

    designs = []
    for sector in focus:
        designs.extend(SECTORS_BY_KEY[sector]['gallery'][:1])
    gallery = design_examples(designs[:4])

    focus_links = ''.join(f'<li><a href="/sectors/{k}/">{escape(SECTORS[k][0])}</a></li>' for k in focus)
    nearby_links = ''.join(f'<li><a href="/norfolk/{k}/">{escape(TOWNS_BY_KEY[k]["name"])}</a></li>' for k in t['nearby'])
    profile = f'''<div class="profile-grid">
    <article><h3>{name} at a glance</h3><p>{escape(t["profile"])}</p></article>
    <article><h3>Getting here</h3><p>{t["miles"]} miles, about {t["time"]} via the {escape(t["roads"][0])}. Fitting is at our Norwich workshop, so design and approval happen before you travel.</p></article>
    <article><h3>What we do most</h3><ul>{focus_links}</ul></article>
    <article><h3>Areas nearby</h3><ul>{nearby_links}</ul></article></div>'''

    getting_here = workshop_map(phone, tel, email, None if key == 'norwich' else t['name'], t['county']) + f'''
    <div class="route-notes"><article><h3>Directions from {name}</h3><p>{escape(t["directions"])}</p></article>
    <article><h3>Arrival &amp; drop-off</h3><p>{escape(t["arrival"])}</p></article></div>'''

    business = f'<p class="core-prose">{escape(t["business"])} Here are the sectors we design for most in and around {name}.</p>' + sector_cards(focus[:3])

    head, copy = t['spotlight']
    spotlight = f'<div class="spotlight"><h3>{escape(head)}</h3><p>{escape(copy)}</p></div>'

    nearby = link_tiles([(k, (TOWNS_BY_KEY[k]['name'], f'{TOWNS_BY_KEY[k]["miles"]} miles · {TOWNS_BY_KEY[k]["time"]}')) for k in t['nearby']], lambda k: f'/norfolk/{k}/').replace('class="tile-grid"', 'class="tile-grid four"', 1)

    parts = [
        ('intro', 'Overview', f'Vehicle graphics for {escape(t["area"])}.', intro, ''),
        ('services', 'Services', f'Van signwriting, wraps and fleet graphics in {name}.', services, 'tint'),
        ('pricing', 'Starting prices', f'Van signwriting prices for {name}.', prices, ''),
        ('gallery', 'Design ideas', f'Vehicle wrap ideas for {name} businesses.', gallery, 'dark-section'),
        ('local', 'Local profile', f'Working in and around {name}.', profile, 'tint'),
        ('getting-here', 'Map &amp; directions', f'From {name} to our workshop.', getting_here, ''),
        ('businesses', 'Business vehicles', f'Fleet graphics for {name} firms.', business, 'tint'),
        ('spotlight', 'Local spotlight', f'Why it matters in {name}.', spotlight, ''),
    ]
    if t.get('work'):  # only real, approved local jobs
        parts.append(('local-work', 'Local work', f'Recent jobs from {name}.', design_examples(t['work']), 'dark-section'))
    jumps = [('services', 'Services'), ('pricing', 'Prices'), ('gallery', 'Designs'), ('getting-here', 'Directions'), ('businesses', 'Businesses'), ('faq', 'FAQs'), ('quote', 'Get a quote')]
    html = page_jumps(jumps)
    for n, (k, label, title, body, style) in enumerate(parts, 1):
        html += section(n, k, label, title, body, style)
    html += designer_strip('drive over')
    n = len(parts)
    html += section(n + 1, 'process', 'How it works', 'From brief to fitted.', process_steps(f'Fitting in Norwich'), 'tint')
    html += section(n + 2, 'nearby', 'Nearby towns', f'Also serving towns near {name}.', nearby)
    html += section(n + 3, 'reviews', 'Customer reviews', 'Published customer feedback.', reviews(CONTENT['van-signwriting-norwich']), 'tint')
    return town_hero(t, image, alt, phone, tel) + html


# ---------------------------------------------------------------- sectors

def sector_hero_image(key):
    """Dedicated hero if generated (dist/assets/sectors/{key}-hero.webp), else the card image."""
    from pathlib import Path
    if Path(f'dist/assets/sectors/{key}-hero.webp').exists():
        return f'sectors/{key}-hero', True
    image = SECTORS_BY_KEY[key]['image']
    return (f'concept-{image}' if isinstance(image, int) else image), False


def sector_hero(key, phone, tel):
    s = SECTORS_BY_KEY[key]
    image, dedicated = sector_hero_image(key)
    group = next(label for g, label, _ in GROUPS if g == s['group'])
    chips = ''.join(f'<li>{escape(c)}</li>' for c in (s['package'][0], 'Signwriting from £149', 'Designed & fitted in Norwich'))
    must = ''.join(f'<li>{escape(m)}</li>' for m in s['must'])
    return f'''<section class="sector-hero{' is-dedicated' if dedicated else ''}{' is-long' if len(s['primary']) > 24 else ''}">
    <img class="sector-hero__img" src="{asset(image)}" alt="{escape(s['alt'])}" fetchpriority="high" width="2400" height="1100">
    <div class="shell sector-hero__inner"><div class="sector-hero__copy">
    <nav class="crumb" aria-label="Breadcrumb"><a href="/">Home</a><span aria-hidden="true">/</span><a href="/sectors/">Sectors</a><span aria-hidden="true">/</span><span>{escape(s['name'])}</span></nav>
    <p class="eyebrow accent">{escape(group)} · {escape(s['name'])}</p><h1>{escape(cap(s['primary']))}<span>in Norwich &amp; Norfolk.</span></h1>
    <p class="lede">{escape(s['card'])} We design, print and fit {escape(s['secondary'][0])} and {escape(s['secondary'][1])} at our Norwich workshop.</p>
    <div class="actions"><a class="btn" href="#quote">Get a free quote{ARROW}</a><a class="btn outline" href="/design-your-van/#designer">Try the Van Designer{ARROW}</a></div>
    <ul class="sector-hero__chips">{chips}</ul></div></div>
    <div class="sector-hero__bar"><div class="shell"><p>Your van should say</p><ul>{must}</ul></div></div></section>'''


def sector_gallery(s):
    """Use the sector's own concept images once added (assets/sectors/gallery/{key}-{n}.webp)."""
    from pathlib import Path
    from gallery_brief import G, filename
    out = []
    for n, (fallback, entry) in enumerate(zip(s['gallery'], G[s['key']]), 1):
        own = f'sectors/gallery/{filename(entry[6])}'
        out.append((own, entry[6]) if Path(f'dist/assets/{own}.webp').exists() else fallback)
    return out

def recommended_package(title):
    t = title.lower()
    hits = [(t.find(w), key) for w, key in (('fleet', 'fleet'), ('partial', 'partial'), ('full', 'full'), ('box-body', 'full'), ('signwriting', 'sign'), ('chevron', 'sign'), ('headboard', 'sign')) if w in t]
    return min(hits)[1] if hits else 'sign'

def price_cards(s):
    rec = recommended_package(s['package'][0]) if s else None
    cards = (
        ('sign', 'is-orange', 'Signwriting', 'from', '£149', 'small van', 'Logos, a service line and contact details in cut vinyl.',
         '<ul class="price-sizes"><li><span>Small van</span><b>£149</b></li><li><span>Medium van</span><b>£210</b></li><li><span>Large van</span><b>£285</b></li></ul>'),
        ('partial', 'is-cobalt', 'Partial wrap', '', 'Quoted', 'per vehicle', 'Printed panels or colour across selected areas of the van.', ''),
        ('full', 'is-dark', 'Full wrap', '', 'Quoted', 'per vehicle', 'Printed imagery or brand colours across most exterior panels.', ''),
        ('fleet', 'is-mint', 'Fleet graphics', '', 'Quoted', 'per fleet', 'One shared layout adapted for each make and model you run.', ''),
    )
    out = ''
    for key, tone, name, pre, price, per, scope, extra in cards:
        badge = f'<span class="price-badge">Recommended for {escape(s["name"].lower())}</span>' if key == rec else ''
        out += (f'<article class="price-card {tone}{" is-rec" if key == rec else ""}">{badge}<h3>{name}</h3>'
                f'<p class="price-big">{f"<small>{pre}</small>" if pre else ""}{price}<span>{per}</span></p>'
                f'<p class="price-scope">{scope}</p>{extra}<a class="price-cta" href="#quote">Get a free quote {ARROW}</a></article>')
    return f'<div class="price-cards">{out}</div>'

def sector_page(key):
    s = SECTORS_BY_KEY[key]
    name = s['name']
    pains = info_cards([(f'{i:02}', escape(a), escape(b)) for i, (a, b) in enumerate(s['pains'], 1)])
    sec = s['secondary']
    challenge = (f'<p class="core-prose">{escape(s["intro"])} Whether you need {escape(sec[1])}, {escape(sec[2])} or {escape(sec[3])}, '
                 f'the layout has to work on your vehicle as it really is.</p>') + pains
    must = '<ul class="must-list">' + ''.join(f'<li>{escape(item)}</li>' for item in s['must']) + '</ul>' + \
        '<p class="core-note">Not sure what to include? Our guide to <a href="/guides/van-signwriting-brief/">what to put on a work van</a> walks you through it.</p>'
    note = ''
    package_title, package_copy = s['package']
    package = f'<p class="core-prose">{escape(package_copy)}</p><p class="core-note"><a href="/vehicle-wraps-norwich/#comparison">Compare coverage options {ARROW}</a></p>'
    budget = price_cards(s) + '<p class="core-note">Signwriting prices are Broadland Digital’s <a href="/van-signwriting-norwich/#pricing">published fitted packages</a>. Wraps and fleets get a written quote covering your vehicle size, artwork, film, coverage and VAT.</p>'
    tips = info_cards([(f'{i:02}', escape(a), escape(b)) for i, (a, b) in enumerate(s['tips'], 1)])
    html = page_jumps((('challenge', 'The challenge'), ('must-haves', 'What to include'), ('gallery', 'Designs'), ('package', 'Package'), ('pricing', 'Prices'), ('reviews', 'Reviews'), ('faq', 'FAQs'), ('quote', 'Enquire')))
    html += ''.join([
        section(1, 'challenge', 'The challenge', 'What the job asks of your van.', challenge),
        section(2, 'must-haves', 'What to include', 'What your van must say.', must, 'tint'),
        section(3, 'gallery', 'Sector gallery', f'{escape(cap(sec[0]))} ideas.', __import__('work_gallery').work_gallery(items=__import__('work_gallery').work_for(s['key'])) + design_examples(sector_gallery(s)) + note, 'dark-section'),
        section(4, 'package', 'Recommended package', escape(package_title) + '.', package),
        section(5, 'pricing', 'Price guide', f'What {escape(s["primary"])} cost.', budget, 'tint'),
        section(6, 'design-tips', 'Design tips', 'Build the layout around the job.', tips),
        section(7, 'reviews', 'Customer reviews', 'What our customers say.', reviews(), 'tint'),
    ])
    html += designer_strip('order')
    html += section(8, 'areas', 'Where we work', 'Fitted in Norwich, serving all of Norfolk.',
                    link_tiles([(t['key'], (t['name'], f'{t["miles"]} miles')) for t in TOWN_LIST[:9]], lambda k: f'/norfolk/{k}/')
                    + '<p class="core-note"><a class="text-link" href="/norfolk/">All areas we cover ' + ARROW + '</a></p>', 'tint')
    html += section(9, 'related-sectors', 'Related sectors', 'More ideas for working vehicles.', sector_cards(s['related']))
    return html


def sectors_hub():
    jumps = page_jumps([(g, label) for g, label, _ in GROUPS] + [('quote', 'Get a quote')])
    body = ''
    for n, (g, label, blurb) in enumerate(GROUPS, 1):
        keys = [s['key'] for s in SECTOR_LIST if s['group'] == g]
        body += section(n, g, f'{len(keys)} sectors', escape(label) + '.', f'<p class="core-prose">{escape(blurb)}</p>' + sector_cards(keys), 'tint' if n % 2 == 0 else '')
    return jumps + body
