from html import escape
import re
import json
from pathlib import Path

from guides_content import FULL_GUIDES
from guide_page import guide_body, guide_schema
from core_content import CONTENT, FEATURED_SECTORS, GUIDES, MODELS, SECTOR_CARDS, SECTORS, TOWNS
from core_pages import brand_page, core_sections, enquiry, sector_cards, support_page, vehicle_picker
from areas import TOWN_LIST, TOWNS_BY_KEY
from sector_data import GROUPS, SECTOR_LIST, SECTORS_BY_KEY, cap, sector_meta
from core_content import VAN_BRANDS
from local_pages import sector_hero, sector_hero_image, sector_page, sectors_hub, town_page, town_questions, workshop_map
import home_sections as H
from designer_page import FAQ as DESIGNER_FAQ, designer_page, designer_promo

OUT = Path('dist')
ORIGIN = 'https://van-graphics-website.justin-b8f.workers.dev'  # preview host; change to the live domain at launch
QUOTE = 'https://broadlanddigital.co.uk/get-a-quote/'
PHONE = '01603 407786'
TEL = 'tel:+441603407786'
EMAIL = 'production@broadlanddigital.co.uk'
ARROW = '<span class="arr" aria-hidden="true">↗</span>'
# CRM (Race Car Graphics CRM, business unit "Norwich Vehicle Graphics").
# Leads: the enquiry forms and the Van Designer post to the 'Norwich Vehicle Graphics Web Forms'
# channel. The key and secret are visible in the page source by design of the ingest endpoint;
# rotate them in the CRM if the form is abused. Leave key/secret empty to fall back to email drafts.
# Pages: pages written and published in the CRM's SEO section are pulled from the feed at build
# time and added to the site (cached in crm_feed_cache.json so offline builds keep them).
CRM = dict(
    endpoint='https://dipjypzrfigkzuarlsov.supabase.co/functions/v1/enquiry-form-ingest',
    key='318764b3-e82a-4b82-b832-dda45ab860a3',
    secret='cd2d92e600d85573dce390f2b18faf57d7c2a27f45505d3b',
    feed='https://dipjypzrfigkzuarlsov.supabase.co/functions/v1/seo-feed?key=21aed0c2-5381-44a9-8e6b-42f99b684c59',
)
DESIGNER_LEADS = dict(CRM, api='https://dipjypzrfigkzuarlsov.supabase.co/functions/v1/van-designer', render='https://dipjypzrfigkzuarlsov.supabase.co/functions/v1/van-designer-render')
SERVICES = [
    dict(slug='van-signwriting-norwich', label='Van signwriting', title='Van signwriting in Norwich',
         intro='Make it easy to spot your van and remember who to call. We design, produce and fit vinyl lettering and printed graphics for vans across Norwich and Norfolk.',
         short='Clean lettering, logos and printed graphics for vans that work as hard as you do.', image='service-copperline',
         alt='White Copperline Electrical van with blue and yellow signwriting', tag='01 / LETTERING',
         heading='Make the essentials easy to read.',
         body='For a trades van, your name, main service and phone number often do most of the work. We plan those around doors, handles and panel seams so the design reads from the pavement and from behind.',
         options=[('Cut vinyl lettering','A tidy way to add your name, website, phone number and a simple logo.'),('Printed logos and panels','Useful for multicolour branding, gradients and artwork that needs more detail.'),('Side and rear graphics','Plan the sides for passing traffic and the back for drivers who see you at junctions.')],
         questions=[('What should I put on my van?','Start with your business name, what you do and the contact detail you want customers to use. Your logo, colours and website can help tie it to your other branding.'),('Can you work from my own artwork?','Yes. Share what you have when you enquire. A vector logo is useful if available, and we can discuss what needs preparing before production.')]),
    dict(slug='vehicle-wraps-norwich', label='Vehicle wraps', title='Vehicle wraps in Norwich',
         intro='Change the look of a car or give a commercial vehicle more space for your brand. We design and fit partial and full wraps in Norwich.',
         short='From a bold partial wrap to full coverage for cars, vans and commercial vehicles.', image='service-tidelark',
         alt='Tidelark Surf Co. van with a full blue wave wrap and coral lettering', tag='02 / PARTIAL & FULL',
         heading='Choose how much of the vehicle to wrap.',
         body='The original paint colour can be part of the design. A partial wrap can use that colour to make graphics feel integrated. Full coverage gives you more room for imagery, large colour blocks or a more dramatic transformation.',
         options=[('Partial wraps','Use selected panels, a rear section or a large sweep of colour across the sides.'),('Full wraps','Give a vehicle a coordinated finish across the main exterior panels.'),('Printed wrap designs','Bring together photos, illustrations and brand colours for promotional vehicles, vans and trailers.')],
         questions=[('What affects the cost of a wrap?','Vehicle size, panel shape, coverage, materials and artwork all affect the quote. Photos and your make and model help us give you a more accurate estimate.'),('Can you wrap over damaged paint?','Send clear photos of any damage, corrosion or repairs. The team can assess the surface before agreeing the scope of work.')]),
    dict(slug='fleet-graphics-norwich', label='Fleet graphics', title='Fleet graphics in Norwich',
         intro='Give your cars, vans and commercial vehicles one recognisable look, even when body styles and sizes vary. Designed, produced and fitted in Norwich.',
         short='A consistent look across work vans, company cars and commercial fleets.', image='service-juniper',
         alt='Juniper Property Care vans and car with matching green and copper graphics', tag='03 / MULTI-VEHICLE',
         heading='One identity across different vehicles.',
         body='We adapt the layout to each vehicle so key details stay visible around doors, trims and windows. Start with the vehicles you have today and discuss how the same design could work on future additions.',
         options=[('Mixed vehicles','Carry the same colours, typography and message from compact vans to cars and larger vehicles.'),('Phased fitting','Share which vehicles need to stay on the road and we can discuss how to schedule the work.'),('New additions and replacements','Use the approved design as a reference for future vehicles or panels that need replacing.')],
         questions=[('What do you need to quote a fleet?','Send the vehicle count, makes and models, photos if available and any brand guidelines. Tell us which vehicles need graphics first.'),('Can you match our existing fleet graphics?','Share photos and any artwork you have. We can review how closely the layout and colours can be matched before you approve a design.')]),
]
AREAS = ['Norwich', 'Wymondham', 'Dereham', 'Great Yarmouth', 'King’s Lynn', 'Aylsham', 'North Walsham', 'Cromer', 'Thetford', 'Across Norfolk']

def button(label, url, cls=''):
    return f'<a class="btn {cls}" href="{url}">{label}{ARROW}</a>'

def brand():
    return '<a class="brand brand--logo" href="/" aria-label="Wrapt home"><img src="/assets/wrapt-logo.webp" alt="Wrapt" width="566" height="120"></a>'


def mega(label, href, columns, intro):
    """Full-width dropdown: an intro panel and link columns. columns = [(heading or '', [(name, url, note?)])]."""
    title, blurb, cta, cta_href = intro
    cols = ''
    for heading, items in columns:
        links = ''.join(f'<li><a href="{it[1]}">{escape(it[0])}' + (f'<small>{escape(it[2])}</small>' if len(it) > 2 else '') + '</a></li>' for it in items)
        cols += f'<div>{f"<p>{escape(heading)}</p>" if heading else ""}<ul>{links}</ul></div>'
    return (f'<div class="nav-item"><a href="{href}" class="nav-top" aria-haspopup="true">{label}</a><div class="mega"><div class="mega-inner">'
            f'<div class="mega-intro"><strong>{escape(title)}</strong><span>{escape(blurb)}</span><a href="{cta_href}">{escape(cta)} →</a></div>'
            f'<div class="mega-cols" style="--cols:{len(columns)}">{cols}</div></div></div></div>')

SHORT_GROUPS = {'trades': 'Trades & home', 'mobile': 'Mobile services', 'transport': 'Transport & fleets', 'land': 'Land & water', 'leisure': 'Retail & leisure'}

def header():
    services = [('Services', [(s['label'], f'/{s["slug"]}/') for s in SERVICES]),
                ('Plan your project', [('Van Designer', '/design-your-van/', 'Design your van online, free'), ('Van manufacturers', '/vehicles/', '29 makes covered'), ('Contact & directions', '/contact/')])]
    sector_cols = [(SHORT_GROUPS[g], [(s['name'], f'/sectors/{s["key"]}/') for s in SECTOR_LIST if s['group'] == g]) for g, _, _ in GROUPS]
    third = (len(TOWN_LIST) + 2) // 3
    by_name = sorted(TOWN_LIST, key=lambda t: t['name'])
    area_cols = [('Norfolk & Waveney' if i == 0 else '\u00a0', [(t['name'], f'/norfolk/{t["key"]}/', f'{t["miles"]} miles') for t in by_name[i*third:(i+1)*third]]) for i in range(3)]
    keys = list(GUIDES)
    half = (len(keys) + 1) // 2
    guide_cols = [('Before you order', [(GUIDES[k][0], f'/guides/{k}/') for k in keys[:half]]), ('Wraps & fleets', [(GUIDES[k][0], f'/guides/{k}/') for k in keys[half:]])]
    nav = (mega('Services', '/#services', services, ('Vehicle graphics', 'Signwriting, wraps and fleet livery, designed and fitted in Norwich.', 'Get a free quote', '/contact/#quote'))
           + ''
           + mega('Sectors', '/sectors/', sector_cols, (f'{len(SECTOR_LIST)} sectors', 'Design ideas, a recommended package and a price guide for your line of work.', 'All sectors', '/sectors/'))
           + mega('Areas', '/norfolk/', area_cols, ('Areas we cover', 'Fitted at our Norwich workshop on Vulcan Road North. Distances are driving miles.', 'All areas', '/norfolk/'))
           + mega('Guides', '/#guides', guide_cols, ('Guides', 'Costs, coverage, artwork and aftercare explained before you order.', 'Ask a question', '/contact/'))
           + '<a class="nav-top" href="/gallery/">Gallery</a><a class="nav-top" href="/contact/">Contact</a>')
    mobile = '<a href="/#services">Services</a><a href="/sectors/">Sectors</a><a href="/norfolk/">Areas we cover</a><a href="/#guides">Guides</a><a href="/gallery/">Gallery</a><a href="/contact/">Contact</a>'
    return f'''<a class="skip" href="#main">Skip to content</a>
    <div class="utility"><div class="shell"><span><i class="dot"></i> Norwich workshop · Serving Norfolk</span><a href="{TEL}">Call {PHONE}</a></div></div>
    <header class="main-head"><div class="shell">{brand()}<nav class="nav" aria-label="Main navigation">{nav}</nav>
    <details class="mobile"><summary>Menu</summary><nav aria-label="Mobile navigation"><div>{mobile}</div></nav></details><a class="head-call" href="{TEL}" aria-label="Call {PHONE}"><svg viewBox="0 0 24 24" aria-hidden="true" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M5 4h4l2 5-2.5 1.5a11 11 0 0 0 5 5L15 13l5 2v4a2 2 0 0 1-2 2A16 16 0 0 1 3 6a2 2 0 0 1 2-2"/></svg></a>{button('Get a quote', '#quote')}</div></header>'''

def footer():
    service_links = ''.join(f'<li><a href="/{s["slug"]}/">{s["label"]}</a></li>' for s in SERVICES)
    towns = ''.join(f'<li><a href="/norfolk/{t["key"]}/">{escape(t["name"])}</a></li>' for t in TOWN_LIST[:15])
    sectors = ''.join(f'<li><a href="/sectors/{k}/">{escape(SECTORS_BY_KEY[k]["name"])}</a></li>' for k in FEATURED_SECTORS)
    guides = ''.join(f'<li><a href="/guides/{k}/">{escape(v[0])}</a></li>' for k, v in GUIDES.items())
    brands = ''.join(f'<a href="{url}" target="_blank" rel="noopener" aria-label="{name} website (opens in a new tab)"><img src="/assets/group/{src}" alt="{name}" loading="lazy" height="70"{cls}></a>' if url else f'<div><img src="/assets/group/{src}" alt="{name}" loading="lazy" height="70"></div>'
                     for name, url, src, cls in (('Broadland Digital', 'https://broadlanddigital.co.uk/', 'broadland-digital-logo.svg', ''),
                                                 ('Race Car Graphics UK', 'https://racecargraphics.uk/', 'rcg-logo.png', ''),
                                                 ('Auto Opulence', 'https://autoopulence.co.uk/', 'auto-opulence-logo-white.svg', ''),
                                                 ('Norwich Web Works', 'https://norwichwebworks.co.uk/', 'norwich-web-works-logo.png', ' class="sq"'),
                                                 ('Consensus Media', '', 'consensus-media-logo.svg', '')))
    return f'''<footer class="footer"><div class="shell">
    <div class="footer-contact"><a href="{TEL}"><span class="fc-ico" aria-hidden="true">☎</span><small>Call the workshop</small><b>{PHONE}</b></a><a href="mailto:{EMAIL}"><span class="fc-ico" aria-hidden="true">✉</span><small>Email us</small><b>{EMAIL}</b></a><a href="/contact/#workshop"><span class="fc-ico" aria-hidden="true"><svg viewBox="0 0 24 24" width="20" height="20" fill="currentColor" aria-hidden="true"><path d="M12 2a7 7 0 0 0-7 7c0 5.2 7 13 7 13s7-7.8 7-13a7 7 0 0 0-7-7zm0 9.5A2.5 2.5 0 1 1 12 6.5a2.5 2.5 0 0 1 0 5z"/></svg></span><small>Visit</small><b>Vulcan House, Vulcan Road North, Norwich NR6 6AQ</b></a></div>
    <div class="footer-grid footer-grid--wide"><div>{brand()}<p>Broadland Digital Ltd<br>Vulcan House, Vulcan Road North<br>Norwich, Norfolk NR6 6AQ</p>
    <p class="footer-hours">Fitting by appointment. Call ahead to book.</p><p><a class="text-link" href="/contact/#workshop">Map &amp; directions {ARROW}</a></p></div>
    <div><h2>Services</h2><ul>{service_links}<li><a href="/design-your-van/">Van Designer</a></li><li><a href="/vehicles/">Van manufacturers</a></li><li><a href="/contact/">Contact</a></li></ul></div>
    <div><h2>Areas</h2><ul>{towns}<li><a href="/norfolk/">All areas</a></li></ul></div>
    <div><h2>Sectors</h2><ul>{sectors}<li><a href="/sectors/">All sectors</a></li></ul></div>
    <div><h2>Guides</h2><ul>{guides}</ul></div></div>
    <section class="footer-brands" aria-labelledby="footer-brands-title"><h2 id="footer-brands-title">Group brands</h2><div class="footer-brand-grid">{brands}</div></section>
    <div class="footnote"><span>© 2026 Norwich Vehicle Graphics, part of Broadland Digital Ltd</span><span><a href="https://broadlanddigital.co.uk/privacy-policy/">Privacy policy</a></span></div></div></footer>'''

def quote():
    return f'''<section class="quote" id="quote"><div class="shell quote-grid"><div><p class="eyebrow">Get a free quote</p><h2>What are you driving?</h2><p>Tell us the make and model, how many vehicles you have and the look you’re after. If you have photos or artwork, have them handy.</p><div class="actions">{button('Open our enquiry form', '/contact/#quote', 'dark')}</div></div>
    <div class="quote-contact"><p><strong>Speak to the Norwich team</strong></p><p><a href="{TEL}">{PHONE}</a></p><p><a href="mailto:{EMAIL}">{EMAIL}</a></p><p>Vulcan House, Vulcan Road North<br>Norwich NR6 6AQ</p></div></div></section>'''

def media(image, alt, caption=''):
    label = f'<div class="hero-caption"><b>↗</b>{caption}</div>' if caption else ''
    return f'<div class="hero-media"><img src="/assets/{image}.webp" alt="{escape(alt)}" fetchpriority="high"><span class="marker" aria-hidden="true"><i></i><i></i><i></i></span>{label}</div>'

def hero(title, description, image, alt, eyebrow, home=False, core=False, parent=None, call=False):
    crumb = '' if home else '<div class="crumb"><a href="/">Home</a><span aria-hidden="true">/</span><span>Vehicle graphics</span></div>'
    if parent:
        href, label = parent
        crumb = f'<nav class="crumb" aria-label="Breadcrumb"><a href="/">Home</a><span aria-hidden="true">/</span><a href="{href}">{label}</a></nav>'
    secondary = '<a class="btn outline" href="#services">Explore services <span class="arr" aria-hidden="true">↓</span></a>' if home else ''
    if core:
        secondary = '<a class="btn outline" href="#gallery">View design gallery <span class="arr" aria-hidden="true">↓</span></a>'
    if call:
        secondary = button(f'Call {PHONE}', TEL, 'outline')
    caption = ''
    return f'''<section class="hero {'' if home else 'subhero service-hero' if core else 'subhero'}"><div class="shell"><div class="hero-copy">{crumb}
    <p class="eyebrow accent">{eyebrow}</p><h1>{title}</h1><p class="lede">{description}</p><div class="actions">{button('Get a free quote','#quote')}{secondary}</div>{'<a class="text-link service-vehicle-link" href="#vehicles">Choose by brand and model ↓</a>' if core else ''}</div>{media(image,alt,caption)}</div></section>'''

def service_hero(s):
    """Full-width image hero shared with sector, town and Van Designer pages.
    Uses assets/pages/service-{slug}-hero.webp when added, otherwise the service image."""
    custom = generated(f'pages/service-{s["slug"]}-hero')
    image = custom or s['image']
    price = CONTENT[s['slug']]['pricing'][0] if s['slug'] == 'van-signwriting-norwich' else None
    chips = ''.join(f'<li>{escape(c)}</li>' for c in ([f'Signwriting {price.lower()}' if price else 'Quoted per vehicle', 'Designed & fitted in Norwich', 'Proof before print']))
    options = ''.join(f'<li>{escape(o[0])}</li>' for o in s['options'])
    title = s['title'].replace(' in Norwich', '<span>in Norwich.</span>')
    return f'''<section class="sector-hero service-hero{' is-dedicated' if custom else ''}">
    <img class="sector-hero__img" src="/assets/{image}.webp" alt="{escape(s['alt'])}" fetchpriority="high" width="2400" height="1100">
    <div class="shell sector-hero__inner"><div class="sector-hero__copy">
    <nav class="crumb" aria-label="Breadcrumb"><a href="/">Home</a><span aria-hidden="true">/</span><a href="/#services">Services</a><span aria-hidden="true">/</span><span>{escape(s['label'])}</span></nav>
    <p class="eyebrow accent">Design · Production · Fitting</p><h1>{title}</h1>
    <p class="lede">{escape(s['intro'])}</p>
    <div class="actions">{button('Get a free quote', '#quote')}<a class="btn outline" href="#gallery">View design gallery <span class="arr" aria-hidden="true">↓</span></a></div>
    <ul class="sector-hero__chips">{chips}</ul></div></div>
    <div class="sector-hero__bar"><div class="shell"><p>Options</p><ul>{options}</ul></div></div></section>'''

def cards(exclude=None):
    items = ''.join(f'''<a class="card" href="/{s["slug"]}/"><div class="card-image"><img src="/assets/{s["image"]}.webp" width="1150" height="647" loading="lazy" alt="{s["alt"]}"><span class="tag">{s["tag"]}</span></div>
    <div class="card-copy"><h3>{s["label"]}</h3><p>{s["short"]}</p><strong>Explore {s["label"].lower()} {ARROW}</strong></div></a>''' for s in SERVICES if s['slug'] != exclude)
    return f'''<section class="section" id="services"><div class="shell"><div class="section-head"><div><p class="eyebrow blue">Our services</p><h2>{'More ways to brand your vehicle.' if exclude else 'Find the right finish.'}</h2></div><p>From straightforward lettering to a full wrap, choose the coverage that suits your vehicle and what you want it to say.</p></div><div class="cards">{items}</div><div id="vehicles" class="service-vehicle-picker"><p class="eyebrow blue">Van manufacturers</p><h3>Choose by brand and model.</h3>{vehicle_picker()}</div></div></section>'''

def faq(questions, core=False):
    items = ''.join(f'<details><summary>{escape(q)}</summary><p>{escape(a)}</p></details>' for q, a in questions)
    return f'<section class="section faq" id="faq"><div class="shell faq-grid"><div><p class="eyebrow blue">{'15 / FAQ' if core else 'Before you book'}</p><h2>Good to know.</h2></div><div>{items}</div></div></section>'

def local():
    places = ''.join(f'<li>{place}</li>' for place in AREAS)
    return f'''<section class="section local"><div class="shell local-grid"><div><p class="eyebrow blue">Based in Norwich</p><h2>On the road<br>across Norfolk.</h2><p>We work with local trades, independent businesses and fleet operators from our Norwich base on Vulcan Road North.</p>{button('See areas we cover','/norfolk/','dark')}</div><ul class="places">{places}</ul></div></section>'''

def process():
    steps = [('Send your brief', 'Share the vehicle details, a few photos and any existing logos or artwork.'),('Approve your design', 'Review a visual of the layout on your vehicle so you can see how it reads before production.'),('Book your fitting', 'We make the graphics and arrange fitting in Norwich around an agreed date.')]
    items = ''.join(f'<div class="step"><b>0{i}</b><h3>{h}</h3><p>{p}</p></div>' for i,(h,p) in enumerate(steps,1))
    return f'<section class="section" id="process"><div class="shell"><div class="section-head"><div><p class="eyebrow blue">How it works</p><h2>From brief to fitting.</h2></div></div><div class="process">{items}</div></div></section>'

def showcase():
    turntable = json.loads(Path('turntable-frames.json').read_text(encoding='utf-8'))
    first_angle = turntable.index('1')
    frame_list = escape(json.dumps(turntable), quote=True)
    return f'''<section class="section dark-section road-showcase" id="examples" aria-labelledby="road-heading"><div class="shell">
    <div class="section-head"><div><p class="eyebrow accent">Graphics in action</p><h2 id="road-heading">Picture it on the road.</h2></div>
    <p>Compare the finishes, see the wrap in a coastal setting or turn the van to inspect it from different angles.</p></div>
    <div class="road-stage">
    <div class="road-studio-header"><div><p>Wrap studio <span>01</span></p><strong>Ford Transit Custom MS-RT</strong></div><div class="road-views" role="group" aria-label="Wrap studio view">
      <button type="button" data-road-view="compare" aria-controls="road-compare" aria-pressed="true">Compare</button>
      <button type="button" data-road-view="lifestyle" aria-controls="road-lifestyle" aria-pressed="false">Lifestyle view</button>
      <button type="button" data-road-view="rotate" aria-controls="road-rotate" aria-pressed="false">360° view</button>
    </div></div>
    <div id="road-compare" class="road-view">
    <div class="road-render">
      <div class="road-images" role="img" aria-label="Ford Transit Custom MS-RT at a 45-degree angle on white, comparing plain paint with a full printed wrap featuring an orange sports car and a Norfolk coastal landscape">
        <img class="road-plain" src="/assets/transit-custom-msrt-plain.webp" alt="" width="1440" height="810" loading="lazy">
        <img class="road-wrapped" src="/assets/transit-custom-msrt-printed-wrap.webp" alt="" width="1440" height="810" loading="lazy">
      </div>
      <div class="road-handle" aria-hidden="true"><span><svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="3.4" stroke-linecap="round" stroke-linejoin="round"><path d="M9.5 6.5 4 12l5.5 5.5M14.5 6.5 20 12l-5.5 5.5"/></svg></span></div>
      <label class="sr-only" for="road-reveal">Full vehicle wrap reveal</label>
      <input type="range" id="road-reveal" min="0" max="100" value="50" aria-valuetext="50% of the wrap revealed">
    </div>
    <div class="road-controls">
      <button type="button" data-reveal="0">Plain van</button>
      <div class="road-progress" aria-hidden="true"><p>Wrap revealed <span data-wrap-progress>50%</span></p><div></div></div>
      <button type="button" data-reveal="100">Full wrap</button>
    </div></div>
    <div id="road-lifestyle" class="road-view" hidden>
      <figure class="road-scene"><img src="/assets/transit-custom-msrt-lifestyle-wide.webp" alt="The wrapped Ford Transit Custom MS-RT parked on a coastal road at sunset, with Norfolk dunes and the sea in view" width="1440" height="810" loading="lazy">
        <figcaption>Norfolk coast · Lifestyle concept</figcaption>
      </figure>
    </div>
    <div id="road-rotate" class="road-view" hidden>
      <div class="road-turntable" data-frames="{frame_list}" tabindex="0" role="group" aria-label="360° wrap preview. Drag or use the left and right arrow keys to rotate.">
        <img src="/assets/transit-custom-msrt-spin-1.webp" alt="Front three-quarter view, nose to the right" width="960" height="540" loading="lazy" draggable="false">
      </div>
      <div class="road-rotate-controls">
        <button type="button" data-rotate="-1" aria-label="Rotate to previous angle">←</button>
        <p><strong data-road-angle aria-live="polite">{first_angle + 1} / {len(turntable)}</strong><span>Drag to rotate</span></p>
        <button type="button" data-rotate="1" aria-label="Rotate to next angle">→</button>
        <button type="button" data-spin aria-pressed="false">Play full turn</button>
      </div>
    </div>
    <div class="road-caption"><p><strong>Full printed wrap</strong><span>Coastal artwork · 45° studio render</span></p>
      <a class="text-link" href="/vehicle-wraps-norwich/">Explore vehicle wraps {ARROW}</a></div>
    </div></div></section>'''

def generated(name):
    """Path stem of a generated hero (see the Hero images brief) if the file has been added."""
    return name if (OUT / 'assets' / f'{name}.webp').exists() else None

_IMG_SIZES = {'/assets/group/broadland-digital-logo.svg': (178, 108), '/assets/group/auto-opulence-logo-white.svg': (289, 94), '/assets/group/consensus-media-logo.svg': (312, 156)}
def sized_images(html):
    """Give every local <img> a width and height so the page doesn't jump as images load."""
    from PIL import Image as _Im
    def fix(m):
        tag = m.group(0)
        if ' width=' in tag:
            return tag
        src = re.search(r'src="([^"?]+)', tag)
        if not src or not src.group(1).startswith('/'):
            return tag
        size = _IMG_SIZES.get(src.group(1))
        if not size:
            try:
                with _Im.open('dist' + src.group(1)) as im:
                    size = im.size
            except Exception:
                return tag
        tag = re.sub(r'\sheight="\d+"', '', tag)
        return tag[:-1].rstrip('/') + f' width="{size[0]}" height="{size[1]}">'
    return re.sub(r'<img\b[^>]*>', fix, html)

_KW = json.loads(Path('page_keywords.json').read_text(encoding='utf-8'))
def page_keywords(path):
    """The SEO optimiser's keywords for a page (exported from the CRM), or the ones our templates target."""
    key = '/' + path.strip('/') if path != '/' else '/'
    if key in _KW:
        return _KW[key]['p'], _KW[key]['s']
    parts = key.strip('/').split('/')
    if parts[0] == 'sectors' and len(parts) == 2 and parts[1] in SECTORS_BY_KEY:
        sec = SECTORS_BY_KEY[parts[1]]
        return sec['primary'], sec['secondary'][:3]
    if parts[0] == 'norfolk' and len(parts) == 2 and parts[1] in TOWNS_BY_KEY:
        n = TOWNS_BY_KEY[parts[1]]['name'].lower()
        return f'van graphics {n}', [f'van signwriting {n}', f'vehicle wraps {n}', f'fleet graphics {n}']
    if parts[0] == 'vehicles' and len(parts) == 2 and parts[1] in dict(VAN_BRANDS):
        l = dict(VAN_BRANDS)[parts[1]].lower()
        return f'{l} van graphics norwich', [f'{l} van wraps', f'{l} van signwriting', f'{l} vehicle graphics norfolk']
    return None

_PROPER = None
def _cap(t):
    """Sentence case, with place, brand and model names capitalised."""
    global _PROPER
    if _PROPER is None:
        from core_content import MODELS
        names = ['Norwich', 'Norfolk', 'Broads', 'Chapter', 'EV', 'VW', 'L200', 'Luton'] + [t['name'] for t in TOWN_LIST] + [l for _, l in VAN_BRANDS] + [m[0] for m in MODELS.values()]
        _PROPER = {}
        for n in names:
            for w in n.split():
                _PROPER[w.lower()] = w
    out = _proper(t)
    return out[:1].upper() + out[1:]

def _proper(t):
    if _PROPER is None:
        _cap('x')
    return ' '.join(_PROPER.get(w, w) for w in t.split(' '))

def keyword_band(path, content):
    """A short section that uses the page's main search phrase and gives each related phrase its own subheading."""
    kw = page_keywords(path)
    if not kw or path in ('/', '/404/'):
        return content
    primary, sec = kw
    sec = [x for x in sec if x][:3]
    if len(sec) < 3:
        return content
    if path.startswith('/guides/'):
        cards = ''.join(f'<article><h3>{escape(_cap(x))}</h3><p>{escape(t)}</p></article>' for x, t in zip(sec, (
            'The sections above cover the essentials. For advice on your own vehicle, call or send photos and we will talk it through.',
            'Every vehicle is different, so we confirm the details with a free design visual and a written, fitted price.',
            'Our Norwich team answers these questions every day for businesses across Norfolk.')))
        P = escape(_proper(primary))
        head = f'More on {P}.'
        intro = f'Still have questions about {P}? Here are the related topics customers ask us about most. If your question is about {P} for a specific vehicle, send us the make and model.'
    else:
        cards = ''.join(f'<article><h3>{escape(_cap(x))}</h3><p>{escape(t)}</p></article>' for x, t in zip(sec, (
            'Designed around your exact vehicle, with your name, services and contact details laid out to read clearly from the road.',
            'Printed in-house on quality cast film and fitted at our Norwich workshop on Vulcan Road North.',
            'Every job starts with a free design visual, so you can see the result before anything is printed.')))
        head = f'{escape(_cap(primary))}.'
        P, S0, S1 = (escape(_proper(x)) for x in (primary, sec[0], sec[1]))
        intro = (f'Looking for {P}? We design, print and fit {S0} and {S1} at our Norwich workshop for businesses across Norfolk. '
                 f'Every {P} project starts with a free design visual and a written, fitted price.')
    band = (f'<section class="section kw-band"><div class="shell"><div class="section-head"><div><p class="eyebrow blue">Norwich workshop</p><h2>{head}</h2></div>'
            f'<p>{intro}</p></div><div class="info-cards">{cards}</div></div></section>')
    for marker in ('<section class="section faq"', '<section class="quote"'):
        if marker in content:
            return content.replace(marker, band + marker, 1)
    return content + band

def keyword_alt(content, primary):
    """Make sure the page's main image is described with its search phrase."""
    def fix(m):
        tag = m.group(0)
        if re.search(r'logo|icon|/assets/brands/|/assets/group/', tag, re.I):
            return tag
        alt = re.search(r'alt="([^"]*)"', tag)
        if not alt:
            return tag
        if primary.lower() in alt.group(1).lower():
            return tag
        new = escape(_cap(primary)) + (': ' + alt.group(1) if alt.group(1) else '')
        return tag.replace(alt.group(0), f'alt="{new}"', 1)
    done = [False]
    def once(m):
        if done[0]:
            return m.group(0)
        new = fix(m)
        if new != m.group(0) or (primary.lower() in m.group(0).lower() and not re.search(r'logo|/assets/brands/', m.group(0))):
            done[0] = True
        return new
    return re.sub(r'<img\b[^>]*>', once, content)

def job_strip(primary):
    from work_gallery import WORK
    picks = [WORK[0], WORK[1], WORK[3]]
    tiles = ''.join(f'<a class="work-tile" href="/assets/work/{f}.webp" data-caption="{escape(c)}: {escape(cap)}"><img src="/assets/work/{f}.webp" alt="{escape(alt)}" loading="lazy"><span><b>{escape(c)}</b>{escape(cap)}</span></a>'
                    for f, c, cap, alt, _ in picks)
    return (f'<section class="section dark-section"><div class="shell"><div class="work-gallery"><div class="work-head"><p class="eyebrow accent">Recent work</p><p>Vans we have designed, printed and fitted in Norwich.</p></div>'
            f'<div class="work-grid work-grid--3">{tiles}</div><p class="core-note"><a class="text-link" href="/gallery/">See the full gallery {ARROW}</a></p></div></div></section>')

CRUMB_NAMES = {'norfolk': 'Areas we cover', 'sectors': 'Sectors', 'vehicles': 'Van manufacturers', 'guides': 'Guides'}
def page_schema(path, title, desc, image, schema):
    """Every page gets a WebPage with a picture and breadcrumbs, merged into any schema it already has."""
    if path in ('/', '/404/'):
        return schema
    url = ORIGIN + path
    parts = [p for p in path.strip('/').split('/') if p]
    crumbs = [{'@type': 'ListItem', 'position': 1, 'name': 'Home', 'item': ORIGIN + '/'}]
    for i, part in enumerate(parts, 2):
        last = i == len(parts) + 1
        name = title.split(' | ')[0] if last else CRUMB_NAMES.get(part, part.replace('-', ' ').title())
        crumbs.append({'@type': 'ListItem', 'position': i, 'name': name, 'item': ORIGIN + '/' + '/'.join(parts[:i - 1]) + '/'})
    extra = [{'@type': 'WebPage', '@id': url + '#webpage', 'url': url, 'name': title, 'description': desc, 'inLanguage': 'en-GB',
              'primaryImageOfPage': {'@type': 'ImageObject', 'url': f'{ORIGIN}/assets/{image}.webp'}, 'about': {'@id': ORIGIN + '/#business'}},
             {'@type': 'BreadcrumbList', 'itemListElement': crumbs}]
    if not schema:
        return {'@context': 'https://schema.org', '@graph': extra}
    graph = schema.get('@graph') or [{k: v for k, v in schema.items() if k != '@context'}]
    types = {g.get('@type') for g in graph if isinstance(g, dict)}
    graph = graph + [e for e in extra if e['@type'] not in types]
    return {'@context': 'https://schema.org', '@graph': graph}

def fit_title(t, limit=60):
    """Keep titles inside what Google shows: drop the brand suffix, then shorten the middle part."""
    if len(t) <= limit:
        return t
    for suffix in (' | Norwich Vehicle Graphics', ' | NVG'):
        if t.endswith(suffix) and len(t[:-len(suffix)]) <= limit:
            return t[:-len(suffix)]
    t = t.replace(' | Norwich Vehicle Graphics', '')
    parts = t.split(' | ')
    while len(' | '.join(parts)) > limit and len(parts) > 1:
        parts.pop()
    t = ' | '.join(parts)
    return t if len(t) <= limit else t[:limit].rsplit(' ', 1)[0]

def fit_desc(d, limit=158):
    """Trim meta descriptions to whole sentences (or a clause) under the limit."""
    if len(d) <= limit:
        return d
    sentences = re.split(r'(?<=[.!?])\s+', d)
    out = ''
    for sn in sentences:
        if len((out + ' ' + sn).strip()) > limit:
            break
        out = (out + ' ' + sn).strip()
    if len(out) >= 90:
        return out
    cut = d[:limit - 1]
    for sep in (', ', ' and ', ' '):
        if sep in cut:
            cut = cut.rsplit(sep, 1)[0]
            break
    return cut.rstrip(' ,;:') + '.'

def page(path, title, desc, content, image='hero', schema=None, quote_block=None, hero_image=None):
    kw = page_keywords(path)
    title, desc = fit_title(title), fit_desc(desc)
    content = keyword_band(path, content)
    if kw and path != '/':
        content = keyword_alt(content, kw[0])
        if len([t for t in re.findall(r'<img\b[^>]*>', content) if not re.search(r'logo|/assets/brands/|/assets/group/', t)]) < 3 and path.startswith('/vehicles/') and path != '/vehicles/':
            content = content.replace('<section class="section faq"', job_strip(kw[0]) + '<section class="section faq"', 1)
    if kw:
        content = content.replace('<h2>Good to know.</h2>', f'<h2>{escape(_cap(kw[0]))}: your questions.</h2>', 1)
    url = ORIGIN + path
    hero_image = generated(hero_image) if hero_image else None
    if hero_image and '<section class="support-hero' in content:
        content = content.replace('<section class="support-hero', f'<section class="has-image support-hero', 1)
        content = re.sub(r'(<section class="has-image support-hero[^"]*">)', rf'\1<img class="support-hero__img" src="/assets/{hero_image}.webp" alt="{escape(_cap(kw[0]) if kw else title.split(" | ")[0])}" fetchpriority="high" width="2400" height="1100">', content, count=1)
        image = hero_image
    if image == 'hero' and generated('pages/social-share'):
        image = 'pages/social-share'
    schema = page_schema(path, title, desc, image, schema)
    structured = f'<script type="application/ld+json">{json.dumps(schema, ensure_ascii=False)}</script>' if schema else ''
    html = f'''<!doctype html>
    <html lang="en-GB"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width, initial-scale=1">
    <title>{escape(title)}</title><meta name="description" content="{escape(desc)}"><link rel="canonical" href="{url}">
    <meta property="og:type" content="website"><meta property="og:title" content="{escape(title)}"><meta property="og:description" content="{escape(desc)}"><meta property="og:url" content="{url}"><meta property="og:image" content="{ORIGIN}/assets/{image}.webp"><meta name="theme-color" content="#111b31"><link rel="icon" href="/assets/icon.svg" type="image/svg+xml">
    <link rel="stylesheet" href="/assets/site.css">{structured}</head><body data-crm-endpoint="{escape(CRM['endpoint'])}" data-crm-key="{escape(CRM['key'])}" data-crm-secret="{escape(CRM['secret'])}">{header()}<main id="main">{content}{quote_block if quote_block is not None else quote()}</main>{footer()}<script src="/assets/site.js" defer></script></body></html>'''
    target = OUT / path.strip('/') / 'index.html'
    target.parent.mkdir(parents=True, exist_ok=True)
    html = sized_images(html)
    target.write_text(html, encoding='utf-8')

business = {'@context':'https://schema.org','@type':'LocalBusiness','@id':ORIGIN+'/#business','name':'Norwich Vehicle Graphics','url':ORIGIN,'telephone':'+44 1603 407786','email':EMAIL,
            'address':{'@type':'PostalAddress','streetAddress':'Vulcan House, Vulcan Road North','addressLocality':'Norwich','addressRegion':'Norfolk','postalCode':'NR6 6AQ','addressCountry':'GB'},
            'areaServed':['Norwich','Norfolk'],'image':ORIGIN+'/assets/hero.webp','logo':ORIGIN+'/assets/wrapt-logo.png',
            'geo':{'@type':'GeoCoordinates','latitude':52.6610201,'longitude':1.2806856},'hasMap':'https://www.google.com/maps/place/Broadland+Digital,+Signs+%26+Graphics/@52.6610201,1.2806856,17z/'}

home_faq = [('How much do vehicle graphics cost?','It depends on the vehicle, the amount of coverage and whether the artwork is ready to use. Send the make and model and a description of what you want so we can quote for the job.'),
            ('Can you help design my graphics?','Yes. Our Norwich team can design a livery from your brief or work with existing branding. We’ll discuss what you want drivers and pedestrians to see first.'),
            ('Where are vehicle graphics fitted?','Fitting is arranged in Norwich. Call 01603 407786 before travelling so the team can confirm the fitting location and your appointment.'),
            ('Can you do a single van or a whole fleet?','Yes. We work on individual cars and vans as well as multi-vehicle graphics. Tell us the vehicle types and how many you need to brand.')]

from core_pages import section as numbered
home_hero = hero('Vehicle graphics &amp; van wraps<span>in Norwich, Norfolk.</span>', 'Van signwriting, partial and full wraps and fleet graphics, designed, printed and fitted in-house at our Norwich workshop.', 'hero','Orange and blue wrapped van on a UK circuit','Vehicle graphics · Norwich, Norfolk',True)
home_hero = home_hero.replace('<a class="btn outline" href="#services">Explore services <span class="arr" aria-hidden="true">↓</span></a>', button('Design your van', '/design-your-van/#designer', 'outline'), 1)
home_hero = home_hero.replace('<section class="hero ', '<section class="hero home-hero ', 1)
home_hero = home_hero.replace('</div></div><div class="hero-media">', '</div>' + H.trust_row() + '</div><div class="hero-media">', 1)
home_schema = {'@context':'https://schema.org','@graph':[{k:v for k,v in business.items() if k!='@context'},
    {'@type':'FAQPage','mainEntity':[{'@type':'Question','name':q,'acceptedAnswer':{'@type':'Answer','text':a}} for q,a in H.HOME_FAQ]}]}
page('/', 'Vehicle Graphics & Van Wraps Norwich | Norwich Vehicle Graphics',
     'Van graphics, full and partial van wraps and fleet livery across Norwich and Norfolk. Designed, printed and fitted in-house. Design your van online or get a free quote.',
     home_hero
     + designer_promo(button)
     + showcase()
     + numbered(4, 'services', 'Our services', 'Find the right finish.', H.service_cards())
     + H.stats_strip()
     + numbered(6, 'compare', 'Compare your options', 'Signwriting, partial or full wrap?', H.comparison_table(), 'tint')
     + numbered(7, 'gallery', 'Gallery', 'Recent work and design ideas.', __import__('work_gallery').work_gallery(limit=5) + H.home_gallery(limit=8, work=False), 'dark-section')
     + numbered(8, 'process', 'How it works', 'From first call to fitted.', H.process_steps())
     + numbered(9, 'sectors', 'Sectors', 'Graphics for your line of work.', H.sectors_grid(), 'tint')
     + numbered(10, 'vehicles', 'Vehicles we wrap', 'Choose by brand and model.', vehicle_picker())
     + numbered(11, 'areas', 'Areas we cover', 'From Norwich across Norfolk.', H.areas_map(), 'local')
     + numbered(12, 'why-us', 'Why choose us', 'Done properly, start to finish.', H.why_us())
     + numbered(13, 'reviews', 'Reviews', 'What customers say.', H.home_reviews(), 'tint')
     + H.motorsport_strip()
     + numbered(14, 'guides', 'Guides', 'Get ready for your project.', H.guides_teaser())
     + faq(H.HOME_FAQ),
     schema=home_schema, quote_block=enquiry(None,SERVICES,PHONE,TEL,EMAIL,QUOTE,context='Homepage'))

page('/design-your-van/', 'Free Van Designer | Design Van Graphics & Wraps Online | Norwich Vehicle Graphics',
     'Design your van graphics or full wrap online in 60 seconds. Add your logo and details, spin it in 360° and request a quote from the Norwich team.',
     designer_page(button, media, faq, PHONE, TEL, EMAIL, DESIGNER_LEADS), 'transit-custom-msrt-printed-wrap',
     {'@context':'https://schema.org','@graph':[
        {'@type':'WebApplication','name':'Van Designer','url':ORIGIN+'/design-your-van/','applicationCategory':'DesignApplication','operatingSystem':'Any','offers':{'@type':'Offer','price':'0','priceCurrency':'GBP'},'provider':{'@id':ORIGIN+'/#business'}},
        {'@type':'FAQPage','mainEntity':[{'@type':'Question','name':q,'acceptedAnswer':{'@type':'Answer','text':a}} for q,a in DESIGNER_FAQ]}]})

ribbon = '<div class="ribbon"><div class="shell"><div><b>01</b> Designed in Norwich</div><div><b>02</b> Produced in-house</div><div><b>03</b> Fitted locally</div></div></div>'
support_urls = []

for s in SERVICES:
    data = CONTENT[s['slug']]
    title = s['title'].replace(' in Norwich','<span>in Norwich.</span>')
    path = '/' + s['slug'] + '/'
    questions = s['questions'] + data['faq']
    schema = {'@context':'https://schema.org','@graph':[
        {'@type':'Service','name':s['label'],'url':ORIGIN+path,'description':s['intro'],'provider':{'@id':ORIGIN+'/#business'},'areaServed':['Norwich','Norfolk']},
        {'@type':'FAQPage','mainEntity':[{'@type':'Question','name':q,'acceptedAnswer':{'@type':'Answer','text':a}} for q,a in questions]},
    ]}
    page(path,s['title']+' | Norwich Vehicle Graphics',s['intro'],
         service_hero(s)
         + ribbon + core_sections(s, lambda rows: faq(rows, core=True)),
         s['image'],schema,enquiry(s,SERVICES,PHONE,TEL,EMAIL,QUOTE))

for key,(name,category,description) in MODELS.items():
    path = f'/vehicles/{key}/'
    support_urls.append(path)
    heading = f'{name} graphics and wraps'
    price = {'Small van': '£149', 'Medium van': '£210', 'Large van': '£285'}.get(category)
    size = category.lower()
    opts = [('Signwriting', f'Cut vinyl lettering for your name, services and contact details, laid out around the {name} doors, handles and panel lines.' + (f' Our published fitted price for a {size} starts from {price}.' if price else ' Priced to the size of the body.')),
            ('Partial wrap', f'Printed panels or colour over selected areas of the {name}, usually the rear half or lower sides, using the paint as part of the design.'),
            ('Full wrap', f'Printed imagery or a colour change across most of the {name}, including the bonnet, doors and bumpers where the film can be fitted cleanly.')]
    extra = (f'<h2>Graphics options for the {escape(name)}</h2><div class="info-cards">' + ''.join(f'<article><h3>{t}</h3><p>{escape(d)}</p></article>' for t, d in opts) + '</div>'
             + f'<h2>Planning your {escape(name)} layout</h2><div class="core-prose"><p>Every {escape(size)} has its own panel shapes, so we plan the layout on your exact model rather than a generic template. '
             + f'We check where the sliding door gap, handles, swage lines, rear glazing and any roof racks fall, then place your name and phone number where they stay readable from the pavement and in traffic.</p>'
             + f'<p>If you are not sure what suits your {escape(name)}, try the free <a href="/design-your-van/">Van Designer</a> or send us photos of both sides and the rear and we will suggest a layout with a fitted price.</p></div>')
    model_faq = [(f'How much does signwriting cost on a {name}?', (f'Signwriting on a {size} starts from {price} fitted, using our published packages. ' if price else 'The price depends on the body size and coverage. ') + 'Wraps are quoted per vehicle once we know the coverage and artwork.'),
                 (f'Can you wrap a leased {name}?', 'Usually, with your lease company’s agreement. We use removable cast film and can remove the graphics before the vehicle goes back.'),
                 (f'What do you need to quote for my {name}?', 'The model year, wheelbase and roof height, photos of both sides and the rear, your logo and the wording you want on the van.')]
    model_desc = f'{name} graphics and wraps: signwriting, partial and full wraps laid out on your exact model and fitted at our Norwich workshop. Free design and quote.'
    page(path,heading+' | Norwich Vehicle Graphics',model_desc,
         support_page('Vehicle model · '+category,heading,[description,'Send the model year, wheelbase and photos from both sides and the rear. That gives us a starting point for the proof and helps us spot any existing accessories or damage.'],SERVICES, extra=extra) + faq(model_faq),
         schema={'@context':'https://schema.org','@type':'FAQPage','mainEntity':[{'@type':'Question','name':q,'acceptedAnswer':{'@type':'Answer','text':a}} for q,a in model_faq]})

from core_content import VAN_BRANDS
for key,label in VAN_BRANDS:
    path = f'/vehicles/{key}/'
    support_urls.append(path)
    bfaq = [(f'Do you fit graphics to all {label} vans?', f'Yes. We fit signwriting, partial wraps and full wraps to {label} vans, pickups and commercial vehicles, laid out on your exact model.'),
            (f'How much are {label} van graphics in Norwich?', 'Signwriting starts from £149 for a small van, £210 for a medium van and £285 for a large van, fitted. Wraps are quoted per vehicle.'),
            (f'Can you match my {label} to the rest of my fleet?', 'Yes. We adapt one master layout to each make and model, so a mixed fleet still looks like one business.')]
    page(path, f'{label} Van Graphics Norwich | Norwich Vehicle Graphics',
         f'{label} van graphics Norwich: signwriting, {label} van wraps and fleet graphics designed around your model and fitted at our workshop. Free quote.',
         brand_page(key) + faq(bfaq),
         schema={'@context':'https://schema.org','@type':'FAQPage','mainEntity':[{'@type':'Question','name':q,'acceptedAnswer':{'@type':'Answer','text':a}} for q,a in bfaq]})
support_urls.append('/vehicles/')
page('/vehicles/', 'Van Graphics by Manufacturer | Norwich Vehicle Graphics',
     'Choose your van manufacturer to explore graphics and wraps for Ford, Vauxhall, Volkswagen, Citroën, Peugeot, Mercedes-Benz, Renault, Toyota, Nissan, Iveco and more, fitted in Norwich.',
     '<section class="support-hero"><div class="shell"><nav class="crumb" aria-label="Breadcrumb"><a href="/">Home</a><span aria-hidden="true">/</span><span>Van manufacturers</span></nav><p class="eyebrow accent">Van graphics by manufacturer</p><h1>Select your van brand.</h1></div></section>'
     + '<section class="section core-section"><div class="shell">' + vehicle_picker()
     + '<div class="core-prose" style="margin-top:36px"><h2>Graphics planned around your model.</h2><p>Every van has its own panel shapes, door gaps, handles and glazing, so we lay out signwriting and wraps on your exact make and model. Choose your manufacturer above to see the models we work with most, from small vans like the Caddy and Berlingo to large vans such as the Sprinter, Transit and Crafter, and Luton box vans.</p>'
     + '<p>If your van is not listed, we can still help. Send the make, model, year and wheelbase with photos of both sides and the rear, and we will plan the layout and send a fitted price.</p></div></div></section>'
     + faq([('Do you fit graphics to every van make?', 'Yes. We fit signwriting and wraps to vans from all the main manufacturers, plus pickups, cars, minibuses and box vans.'),
            ('Does the price change between models?', 'Signwriting is priced by van size, from £149 for a small van. Wraps are quoted per vehicle because coverage and panel shapes vary between models.'),
            ('Can you match graphics across different models in my fleet?', 'Yes. We create one master layout and adapt it to each make and model, so every vehicle looks like the same business.')]), hero_image='pages/vehicles-hub-hero')

def location_schema(path, heading, description, parent, questions, town=None, county='Norfolk'):
    parent_path, parent_name = parent
    area = {'@type':'City','name':town,'containedInPlace':{'@type':'AdministrativeArea','name':county}} if town else {'@type':'AdministrativeArea','name':'Norfolk'}
    graph = [
        {'@type':'WebPage','@id':ORIGIN+path,'url':ORIGIN+path,'name':heading,'description':description,'about':{'@id':ORIGIN+path+'#service'}},
        {'@type':'Service','@id':ORIGIN+path+'#service','name':heading,'url':ORIGIN+path,'description':description,'serviceType':'Vehicle graphics and wraps',
         'provider':{'@id':ORIGIN+'/#business'},'areaServed':area},
        {'@type':'FAQPage','mainEntity':[{'@type':'Question','name':q,'acceptedAnswer':{'@type':'Answer','text':a}} for q,a in questions]},
        {'@type':'BreadcrumbList','itemListElement':[
            {'@type':'ListItem','position':position,'name':label,'item':ORIGIN+url}
            for position,(url,label) in enumerate((('/', 'Home'), (parent_path,parent_name), (path,town or heading)), 1)
        ]},
        {k:v for k,v in business.items() if k!='@context'},
    ]
    return {'@context':'https://schema.org','@graph':graph}


sector_parent = ('/sectors/', 'Sectors')
area_parent = ('/norfolk/', 'Areas we cover')
for sector in SECTOR_LIST:
    key, name = sector['key'], sector['name']
    path = f'/sectors/{key}/'
    support_urls.append(path)
    heading = cap(sector['primary'])
    meta_title, description = sector_meta(sector)
    questions = sector['faqs']
    image, _ = sector_hero_image(key)
    page(path, meta_title, description,
         sector_hero(key, PHONE, TEL)
         + sector_page(key) + faq(questions), image,
         location_schema(path, heading, description, sector_parent, questions),
         enquiry(None, SERVICES, PHONE, TEL, EMAIL, QUOTE, context=name))

for town in TOWN_LIST:
    key, name = town['key'], town['name']
    path = f'/norfolk/{key}/'
    support_urls.append(path)
    heading = f'Van graphics in {name}'
    questions = town_questions(town)
    image = SECTORS_BY_KEY[town['focus'][0]]['image']
    image = f'concept-{image}' if isinstance(image, int) else image
    town_title = f'Van Graphics {name} | Signwriting & Wraps | Norwich Vehicle Graphics'
    if len(town_title) > 66: town_title = f'Van Graphics {name} | Signwriting & Wraps'
    town_desc = f'Van graphics in {name}: van signwriting, vehicle wraps and fleet graphics, designed in-house and fitted at our Norwich workshop, {town["miles"]} miles away. Free quote.'
    page(path, town_title, town_desc,
         town_page(key, PHONE, TEL, EMAIL) + faq(questions), image,
         location_schema(path, heading, town_desc, area_parent, questions, name, town['county']),
         enquiry(None, SERVICES, PHONE, TEL, EMAIL, QUOTE, context=name))

for key,(name,summary,detail) in GUIDES.items():
    path = f'/guides/{key}/'
    support_urls.append(path)
    related = [s for s in SERVICES if key in CONTENT[s['slug']]['guides']]
    if key in FULL_GUIDES:
        g = FULL_GUIDES[key]
        page(path, g['title'], g['summary'], guide_body(key, g, SERVICES) + faq(g['faq']),
             schema=guide_schema(ORIGIN, key, g, business['@id']), hero_image=f'pages/guide-{key}-hero',
             quote_block=enquiry(None, SERVICES, PHONE, TEL, EMAIL, QUOTE, context=f'Guide: {name}'))
        continue
    page(path,name+' | Norwich Vehicle Graphics',summary,
         support_page('Vehicle graphics guide',name,[summary,detail],related), hero_image=f'pages/guide-{key}-hero')

places = ''.join(f'<li><a href="/norfolk/{t["key"]}/">{escape(t["name"])} <small>{t["miles"]} mi · {t["time"]}</small></a></li>' for t in TOWN_LIST)
coverage = f'''<section class="section local"><div class="shell local-grid"><div><p class="eyebrow blue">Our service area</p><h2>From Norwich into Norfolk.</h2><p>We design remotely and fit at our Norwich workshop on Vulcan Road North. Distances below are driving routes to the workshop. If you are arranging several vehicles, tell us where they are based and which dates work for you.</p><a class="text-link" href="https://www.google.com/maps/search/?api=1&amp;query=Broadland+Digital+Vulcan+Road+North+NR6+6AQ">Directions to the Norwich workshop {ARROW}</a></div><ul class="places places-wide">{places}</ul></div></section>'''
page('/norfolk/','Vehicle Graphics Across Norfolk | Norwich Vehicle Graphics',
     'Van graphics, wraps and fleet livery for businesses across Norfolk and Waveney: Norwich, King’s Lynn, Great Yarmouth, Lowestoft, Thetford, Dereham, Cromer and more.',
     hero('Vehicle graphics<span>across Norfolk.</span>','Our Norwich team works with businesses across Norfolk and the Waveney valley. Bring us one work van or talk to us about graphics for a fleet.',generated('pages/norfolk-hub-hero') or 'fleet','Three branded vans on a Norfolk country road' if generated('pages/norfolk-hub-hero') else 'Branded car and van with coordinated graphics','Areas we cover')+coverage+cards(),generated('pages/norfolk-hub-hero') or 'fleet')

page('/sectors/','Van Graphics by Sector | Norwich Vehicle Graphics',
     f'Van wraps, signwriting and fleet graphics for {len(SECTOR_LIST)} sectors, from plumbers and electricians to removals, care teams, farms and boatyards across Norfolk.',
     '<section class="support-hero"><div class="shell"><nav class="crumb" aria-label="Breadcrumb"><a href="/">Home</a><span aria-hidden="true">/</span><span>Sectors</span></nav><p class="eyebrow accent">Vehicle graphics by sector</p><h1>Van graphics for your line of work.</h1>'
     + f'<p class="lede">{len(SECTOR_LIST)} sectors, each with design ideas, a recommended package and a price guide.</p></div></section>'
     + sectors_hub(), hero_image='sectors/sectors-hub-hero')

page('/gallery/', 'Van Graphics Gallery | Norwich Vehicle Graphics',
     'Van signwriting, vehicle wraps and fleet graphics fitted at our Norwich workshop, plus design ideas for every kind of business in Norfolk.',
     '<section class="support-hero"><div class="shell"><nav class="crumb" aria-label="Breadcrumb"><a href="/">Home</a><span aria-hidden="true">/</span><span>Gallery</span></nav><p class="eyebrow accent">Van graphics gallery</p><h1>Our van graphics work.</h1>'
     + '<p>Real vans fitted at our Norwich workshop, and design ideas by sector. Tap a photo to enlarge.</p><div class="actions">' + button('Get a free quote','#quote') + button('Try the Van Designer','/design-your-van/','outline') + '</div></div></section>'
     + '<section class="section core-section dark-section" id="work"><div class="shell">' + __import__('work_gallery').work_gallery() + '</div></section>'
     + '<section class="section core-section" id="ideas"><div class="shell"><div class="section-head"><div><p class="eyebrow blue">Design ideas</p><h2>Ideas by sector.</h2></div></div>' + H.home_gallery(limit=200, work=False) + '</div></section>',
     quote_block=enquiry(None,SERVICES,PHONE,TEL,EMAIL,QUOTE,context='Gallery'), hero_image='pages/gallery-hero')
support_urls.append('/gallery/')

CONTACT_FAQ = [('How quickly will you reply?', 'We aim to reply the same working day, with questions about your vehicle or a first idea of the layout and price.'),
       ('Can I visit without an appointment?', 'Please call ahead. Fitting is by appointment, so we can make sure someone is free to talk through your project and look at your vehicle.'),
       ('Do you work with businesses outside Norwich?', 'Yes. We work with businesses across Norfolk and Waveney. Design and quotes can be done remotely, and vehicles are fitted at our Norwich workshop.'),
       ('What should I send with my enquiry?', 'Your vehicle make, model and year, photos of both sides and the rear, your logo if you have one and the wording you want on the van.')]
page('/contact/','Contact & Directions | Norwich Vehicle Graphics',
     'Contact Norwich Vehicle Graphics for signwriting, wraps and fleet graphics. Find the workshop on Vulcan Road North, get directions or ask for a quote.',
     '<section class="support-hero contact-hero"><div class="shell"><a class="crumb" href="/">← Home</a><p class="eyebrow accent">Norwich, Norfolk</p><h1>Contact us.</h1>'
     + '<p>Ask about van signwriting, vehicle wraps, fleet graphics or an upcoming fitting.</p>'
     + '<div class="actions">' + button('Ask a question','#quote') + button('Find the workshop','#workshop','outline') + '</div></div></section>'
     + enquiry(None,SERVICES,PHONE,TEL,EMAIL,QUOTE,contact=True)
     + '<section class="section core-section" id="workshop"><div class="shell"><div class="section-head"><div><p class="eyebrow blue">Find us</p><h2>Visit the Norwich workshop.</h2></div></div>'
     + workshop_map(PHONE,TEL,EMAIL) + '</div></section>'
     + '<section class="section tint"><div class="shell"><div class="section-head"><div><p class="eyebrow blue">What happens next</p><h2>From enquiry to fitted van.</h2></div></div><div class="info-cards">'
     + ''.join(f'<article><h3>{t}</h3><p>{d}</p></article>' for t, d in [
         ('1. Tell us about the vehicle', 'Send the make, model and year, what the van is used for and the coverage you have in mind: signwriting, a partial wrap or a full wrap.'),
         ('2. Design and price', 'We draw your layout on the exact model and send a visual with a written, fitted price. Changes are made before anything is printed.'),
         ('3. Print and book in', 'Once you approve the proof we print in-house and book a fitting slot that suits your diary.'),
         ('4. Fit and collect', 'Your vehicle is fitted at our Norwich workshop on Vulcan Road North, with aftercare advice when you collect it.')])
     + '</div></div></section>' + faq(CONTACT_FAQ),
     schema={'@context':'https://schema.org','@type':'ContactPage','name':'Contact Norwich Vehicle Graphics','url':ORIGIN+'/contact/','mainEntity':{'@id':business['@id']}},quote_block='', hero_image='pages/contact-hero')

def crm_feed():
    """Pages published in the CRM's SEO section. Falls back to the last good copy."""
    cache = Path('crm_feed_cache.json')
    try:
        import urllib.request
        with urllib.request.urlopen(CRM['feed'], timeout=15) as r:
            data = json.loads(r.read().decode('utf-8'))
        data.pop('generatedAt', None)  # keep the cache stable so unchanged builds don't commit
        cache.write_text(json.dumps(data, ensure_ascii=False), encoding='utf-8')
        print(f"CRM feed: {len(data.get('pages', []))} page(s)")
        return data
    except Exception as error:
        if cache.exists():
            print(f'CRM feed unavailable ({error}); using crm_feed_cache.json')
            return json.loads(cache.read_text(encoding='utf-8'))
        print(f'CRM feed unavailable ({error}); no CRM pages added')
        return {}

feed = crm_feed() if CRM.get('feed') else {}
crm_urls = []
existing = {str(p.parent.relative_to(OUT)).replace('\\', '/') for p in OUT.rglob('index.html')}
for item in feed.get('pages', []):
    route = '/' + item['path'].strip('/') + '/'
    if route.strip('/') in existing or route == '//':
        print('CRM page skipped (the site already builds this address):', route)
        continue
    body = (f'<style>{feed.get("css", "")}</style><div class="crm-page" style="{escape(feed.get("vars", ""), quote=True)}">{item["html"]}</div>')
    page(route, item.get('metaTitle') or item.get('title', ''), item.get('metaDescription', ''), body, 'hero', item.get('schema'))
    crm_urls.append(route)
if feed.get('llms'):
    llms = feed['llms']
    if llms.get('override'):
        text = llms['override']
    else:
        lines = [f"# {llms.get('name', 'Norwich Vehicle Graphics')}", '', f"> {llms.get('summary', '')}", ''] + [f'- {d}' for d in llms.get('details', [])]
        lines += ['', '## Key pages', f'- [Van signwriting]({ORIGIN}/van-signwriting-norwich/)', f'- [Vehicle wraps]({ORIGIN}/vehicle-wraps-norwich/)',
                  f'- [Fleet graphics]({ORIGIN}/fleet-graphics-norwich/)', f'- [Free Van Designer]({ORIGIN}/design-your-van/)', f'- [Contact]({ORIGIN}/contact/)']
        text = '\n'.join(lines) + '\n'
    (OUT / 'llms.txt').write_text(text, encoding='utf-8')

page('/404/', 'Page not found | Norwich Vehicle Graphics', 'This page could not be found.',
     '<section class="support-hero"><div class="shell"><a class="crumb" href="/">← Home</a><p class="eyebrow accent">Error 404</p><h1>We can’t find that page.</h1></div></section>'
     + '<section class="section core-section"><div class="shell core-prose"><p>The address may have changed. Try our <a href="/van-signwriting-norwich/">van signwriting</a>, <a href="/vehicle-wraps-norwich/">vehicle wraps</a> or <a href="/fleet-graphics-norwich/">fleet graphics</a> pages, or <a href="/design-your-van/">design your van</a> online.</p></div></section>')
(OUT / '404' / 'index.html').replace(OUT / '404.html'); (OUT / '404').rmdir()

urls = ['/', '/design-your-van/', '/norfolk/', '/sectors/', '/contact/'] + ['/'+s['slug']+'/' for s in SERVICES] + support_urls + crm_urls
(OUT/'sitemap.xml').write_text('<?xml version="1.0" encoding="UTF-8"?><urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">' + ''.join(f'<url><loc>{ORIGIN}{path}</loc></url>' for path in urls) + '</urlset>\n')
(OUT/'robots.txt').write_text(f'User-agent: *\nAllow: /\nSitemap: {ORIGIN}/sitemap.xml\n')

# Cache-bust CSS/JS: assets are cached for a day, so every page links them with a content hash.
import hashlib
for name in ('site.css', 'site.js', 'designer.css', 'designer.js'):
    digest = hashlib.sha1((OUT / 'assets' / name).read_bytes()).hexdigest()[:10]
    for html_file in OUT.rglob('*.html'):
        text = html_file.read_text(encoding='utf-8')
        new = re.sub(rf'/assets/{re.escape(name)}(\?v=[0-9a-f]+)?"', f'/assets/{name}?v={digest}"', text)
        if new != text:
            html_file.write_text(new, encoding='utf-8')
