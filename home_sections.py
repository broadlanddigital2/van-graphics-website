"""Homepage sections from the scope doc's 20-section homepage build structure.

Figures shown are facts about the site itself (makes covered, towns, sectors),
not invented business stats. Swap in real numbers (vans wrapped, years trading,
Google rating) in STATS when you have them.
"""

from html import escape

from areas import TOWN_LIST
from core_content import CONTENT, FEATURED_SECTORS, GUIDES, VAN_BRANDS
from core_pages import ARROW, ICON_PATHS, asset, case_study, reviews, sector_cards, table, van_diagram
from sector_data import GROUPS, SECTOR_LIST

STATS = [
    (str(len(VAN_BRANDS)), 'van makes covered'),
    (str(len(TOWN_LIST)), 'towns served from Norwich'),
    (str(len(SECTOR_LIST)), 'sectors with design ideas'),
    ('60s', 'to design your van online'),
]

WORKSHOP = (52.6630, 1.2831)
TOWN_COORDS = {
    'norwich': (52.6274, 1.2964), 'wymondham': (52.5692, 1.1150), 'dereham': (52.6816, 0.9378),
    'great-yarmouth': (52.5982, 1.7280), 'kings-lynn': (52.7517, 0.4023), 'lowestoft': (52.4811, 1.7534),
    'thetford': (52.4129, 0.7517), 'aylsham': (52.7967, 1.2524), 'north-walsham': (52.8227, 1.3860),
    'attleborough': (52.5181, 1.0155), 'cromer': (52.9313, 1.2990), 'diss': (52.3765, 1.1084),
    'swaffham': (52.6475, 0.6875), 'fakenham': (52.8313, 0.8493), 'holt': (52.9094, 1.0867),
    'beccles': (52.4583, 1.5688), 'watton': (52.5708, 0.8280), 'downham-market': (52.6041, 0.3796),
}
# Simplified county outline (lat, lon), clockwise from King's Lynn. Stylised, not survey-accurate.
OUTLINE = [(52.75, .40), (52.94, .49), (52.97, .64), (52.96, .85), (52.96, 1.02), (52.93, 1.30), (52.88, 1.43),
           (52.82, 1.53), (52.79, 1.60), (52.71, 1.69), (52.65, 1.73), (52.60, 1.74), (52.53, 1.73), (52.48, 1.63),
           (52.46, 1.56), (52.46, 1.44), (52.40, 1.30), (52.37, 1.11), (52.41, .75), (52.45, .62), (52.47, .53),
           (52.52, .25), (52.60, .22), (52.66, .16), (52.73, .20), (52.77, .19), (52.80, .30)]
LABEL_LEFT = {'kings-lynn', 'downham-market', 'swaffham', 'thetford', 'watton', 'attleborough', 'diss', 'dereham', 'fakenham'}


def _xy(lat, lon):
    return round((lon - 0.08) * 0.606 * 400 + 70, 1), round((53.0 - lat) * 400 + 14, 1)


def trust_row():
    items = ('Designed in Norwich', 'Printed in-house', 'Premium cast vinyl', 'Proof before print', 'Fitted at our Norwich workshop')
    return '<ul class="trust-row">' + ''.join(f'<li>{i}</li>' for i in items) + '</ul>'


def stats_strip():
    return '<section class="stats-strip"><div class="shell">' + ''.join(
        f'<div><b>{n}</b><span>{escape(label)}</span></div>' for n, label in STATS) + '</div></section>'


def service_cards():
    cards = [
        ('Van signwriting', 'Lettering, logos and contact details for working vans.', '/van-signwriting-norwich/', 'service-copperline', 'From £149 fitted'),
        ('Partial wraps', 'Printed panels or colour over selected areas, using your paint as part of the design.', '/vehicle-wraps-norwich/#comparison', 'service-petalmill', 'Quoted per vehicle'),
        ('Full wraps', 'Printed imagery or a full colour change across the body.', '/vehicle-wraps-norwich/', 'service-tidelark', 'Quoted per vehicle'),
        ('Fleet graphics', 'One design adapted to every make and model, fitted in batches.', '/fleet-graphics-norwich/', 'service-juniper', 'Quoted per fleet'),
    ]
    items = ''.join(f'''<a class="svc-card" href="{href}"><img src="{asset(img)}" alt="" loading="lazy" width="840" height="473">
    <div><span class="svc-price">{price}</span><h3>{title}</h3><p>{copy}</p><strong>Explore {ARROW}</strong></div></a>''' for title, copy, href, img, price in cards)
    return f'<div class="svc-grid">{items}</div><p class="core-note">Race car liveries and motorsport graphics are handled by our sister site, <a href="https://racecargraphics.uk/">Race Car Graphics</a>.</p>'


def comparison_table():
    """Three option cards. Uses assets/pages/compare-{key}.webp (1200x800) when added, else the coverage diagram."""
    from pathlib import Path
    options = [
        ('signwriting', 'graphics', 'Van signwriting', 'is-orange', 'From', '£149', 'small van', 1, 'Clear and professional',
         [('Coverage', 'Cut letters and logos'), ('Lead time', 'Often fitted in a day'), ('Best for', 'Trades, sole traders and tight budgets')], '/van-signwriting-norwich/'),
        ('partial', 'partial', 'Partial wrap', 'is-cobalt', '', 'Quoted', 'per vehicle', 2, 'Bold colour',
         [('Coverage', 'Selected panels, about a third to two thirds'), ('Lead time', 'Confirmed with your quote'), ('Best for', 'Stronger colour without a full wrap')], '/vehicle-wraps-norwich/#comparison'),
        ('full', 'full', 'Full wrap', 'is-dark', '', 'Quoted', 'per vehicle', 3, 'Maximum impact',
         [('Coverage', 'Most exterior panels'), ('Lead time', 'Confirmed with your quote'), ('Best for', 'Photo liveries and colour changes')], '/vehicle-wraps-norwich/'),
    ]
    cards = ''
    for key, diagram, name, tone, pre, price, per, impact, impact_label, specs, href in options:
        img = f'pages/compare-{key}'
        media = (f'<img src="/assets/{img}.webp" alt="{name} example on a van" loading="lazy" width="1200" height="800">'
                 if Path(f'dist/assets/{img}.webp').exists() else van_diagram(diagram))
        meter = ''.join(f'<i class="{"on" if n <= impact else ""}"></i>' for n in (1, 2, 3))
        rows = ''.join(f'<li><span>{k}</span><b>{v}</b></li>' for k, v in specs)
        cards += (f'<article class="option-card {tone}"><div class="option-card__media">{media}</div><div class="option-card__body">'
                  f'<h3>{name}</h3><p class="price-big">{f"<small>{pre}</small>" if pre else ""}{price}<span>{per}</span></p>'
                  f'<div class="option-impact"><span>Impact</span><span class="meter" aria-label="Impact {impact} of 3">{meter}</span><b>{impact_label}</b></div>'
                  f'<ul class="option-specs">{rows}</ul><a class="btn{" dark" if tone == "is-orange" else ""}" href="{href}">Explore {name.lower()} {ARROW}</a></div></article>')
    return (f'<div class="option-cards">{cards}</div>'
            + f'<p class="core-note">All options use quality cast vinyl that lasts several years with good care. Read the guide: <a href="/guides/partial-vs-full-wrap/">partial wrap vs full wrap {ARROW}</a></p>')


def home_gallery(limit=18):
    group_label = {g: label for g, label, _ in GROUPS}
    by_group = {g: [] for g, _, _ in GROUPS}
    for sec in SECTOR_LIST:
        for img, cap in sec['gallery']:
            by_group[sec['group']].append((img, cap, group_label[sec['group']]))
    seen, picks = set(), []
    while len(picks) < limit and any(by_group.values()):
        for g in by_group:
            pool = by_group[g]
            while pool:
                img, cap, group = pool.pop(0)
                if str(img) not in seen:
                    seen.add(str(img)); picks.append((img, cap, group)); break
            if len(picks) >= limit:
                break
    options = ''.join(f'<option>{escape(label)}</option>' for _, label, _ in GROUPS)
    figures = ''.join(f'<figure data-model="{escape(group)}"><img src="{asset(img)}" alt="{escape(cap)}" loading="lazy" width="840" height="473">'
                      f'<figcaption><strong>{escape(cap)}</strong><small>{escape(group)}</small></figcaption></figure>' for img, cap, group in picks)
    from work_gallery import work_gallery
    return work_gallery() + (f'<div class="gallery-toolbar"><label>Filter by sector <select id="gallery-model"><option value="">All sectors</option>{options}</select></label>'
            f'<span id="gallery-count" aria-live="polite"></span></div><div class="core-gallery">{figures}</div>'
            f'<p class="core-note"><a class="text-link" href="/sectors/">Browse all {len(SECTOR_LIST)} sectors {ARROW}</a></p>')


def process_steps():
    steps = [('Consult', 'Call, send photos or start in the Van Designer. Free, no obligation.', 'Usually a same-day reply'),
             ('Design & proof', 'We lay your branding out on your exact vehicle and send a visual to approve.', 'Changes before anything is printed'),
             ('Print', 'Printed, laminated and cut in-house on quality cast vinyl.', 'Produced in Norwich'),
             ('Fit', 'Fitted at our Norwich workshop by our own team.', 'Lettering often in a day; wraps take longer')]
    icons = ['design', 'proof', 'film', 'fit']
    return '<ol class="home-process">' + ''.join(
        f'<li><svg viewBox="0 0 24 24" aria-hidden="true" fill="none" stroke="currentColor" stroke-width="1.7" stroke-linecap="round" stroke-linejoin="round">{ICON_PATHS[icon]}</svg>'
        f'<b>0{i}</b><h3>{escape(t)}</h3><p>{escape(d)}</p><small>{escape(when)}</small></li>'
        for i, ((t, d, when), icon) in enumerate(zip(steps, icons), 1)) + '</ol>'


def sectors_grid():
    return sector_cards(FEATURED_SECTORS) + f'<p class="core-note"><a class="text-link" href="/sectors/">See all {len(SECTOR_LIST)} sectors {ARROW}</a></p>'


def areas_map():
    outline = ' '.join(f'{x},{y}' for x, y in (_xy(*p) for p in OUTLINE))
    wx, wy = _xy(*WORKSHOP)
    pins = ''
    for t in TOWN_LIST:
        x, y = _xy(*TOWN_COORDS[t['key']])
        left = t['key'] in LABEL_LEFT
        lx, anchor = (x - 7, 'end') if left else (x + 7, 'start')
        pins += (f'<a href="/norfolk/{t["key"]}/"><title>{escape(t["name"])}: {t["miles"]} miles, {t["time"]}</title>'
                 f'<circle cx="{x}" cy="{y}" r="4.5"/><text x="{lx}" y="{y + 3.5}" text-anchor="{anchor}">{escape(t["name"])}</text></a>')
    svg = (f'<svg class="area-map" viewBox="0 0 580 270" role="img" aria-label="Map of the Norfolk towns we serve from our Norwich workshop">'
           f'<polygon class="area-map__county" points="{outline}"/>'
           + ''.join(f'<line class="area-map__ray" x1="{wx}" y1="{wy}" x2="{_xy(*TOWN_COORDS[t["key"]])[0]}" y2="{_xy(*TOWN_COORDS[t["key"]])[1]}"/>' for t in TOWN_LIST)
           + pins + f'<g class="area-map__hq"><rect x="{wx - 6}" y="{wy - 6}" width="12" height="12" transform="rotate(45 {wx} {wy})"/></g></svg>')
    towns = ''.join(f'<li><a href="/norfolk/{t["key"]}/">{escape(t["name"])}<small>{t["miles"]} mi</small></a></li>' for t in TOWN_LIST)
    return (f'<div class="areas-grid"><figure class="area-map-wrap">{svg}<figcaption><i class="hq-key"></i>Our workshop, Vulcan Road North, Norwich. '
            f'Lines show the towns we serve. Simplified map.</figcaption></figure><div><ul class="area-list">{towns}</ul>'
            f'<p class="core-note"><a class="text-link" href="/norfolk/">All areas we cover {ARROW}</a></p></div></div>')


def why_us():
    points = [('design', 'In-house design', 'Our own designers lay out your branding on your exact vehicle, and you approve a visual before anything is printed.'),
              ('film', 'Premium cast vinyl', 'Quality cast films and laminates that conform to curves and last for years with good care.'),
              ('shield', 'Clear warranty terms', 'We tell you which manufacturer and installation terms apply to your film and vehicle before you book.'),
              ('fit', 'Workshop fitting', 'Fitted indoors at our Norwich workshop, where temperature and lighting are controlled for a better finish.'),
              ('proof', 'Fleet rollouts', 'One master design for every make and model, fitted in batches so your fleet keeps working.'),
              ('care', 'Lease-friendly', 'Quality vinyl removes cleanly from sound factory paint, which suits leased vans and company cars.')]
    return '<div class="info-cards why-grid">' + ''.join(
        f'<article><svg class="core-icon" viewBox="0 0 24 24" aria-hidden="true" fill="none" stroke="currentColor" stroke-width="1.7" stroke-linecap="round" stroke-linejoin="round">{ICON_PATHS[k]}</svg><h3>{t}</h3><p>{d}</p></article>'
        for k, t, d in points) + '</div>'


def home_reviews():
    return reviews(CONTENT['van-signwriting-norwich'])


def home_case_study():
    return case_study({'case': (
        'One livery across a courier fleet',
        'A growing courier firm wanted vans of different sizes to look like one company in the depot yard and on residential streets, with fleet numbers depot staff could find quickly.',
        'A purple base with a high-contrast yellow sweep, a large wordmark repeated at the same height on every model, and a fixed position for fleet IDs. Fitted in batches so deliveries carried on.',
        ['service-swiftloom', 25, 27, 'service-loadbridge', 'service-packwell', 53])}) + \
        f'<p class="core-note"><a href="/sectors/delivery/">More on delivery and fleet graphics {ARROW}</a></p>'


def motorsport_strip():
    return ('<section class="motorsport-strip"><div class="shell"><p><b>Race car liveries?</b> Motorsport graphics, race numbers and full liveries are made by our sister site.</p>'
            f'<a class="btn" href="https://racecargraphics.uk/">Visit Race Car Graphics {ARROW}</a></div></section>')


def guides_teaser():
    keys = ['graphics-costs', 'partial-vs-full-wrap', 'wrap-vs-paint']
    return '<div class="info-cards guide-cards">' + ''.join(
        f'<article><b class="core-index">Guide</b><h3>{escape(GUIDES[k][0])}</h3><p>{escape(GUIDES[k][1])}</p><a class="text-link" href="/guides/{k}/">Read the guide {ARROW}</a></article>'
        for k in keys) + '</div>'


HOME_FAQ = [
    ('How much do vehicle graphics cost?', 'Signwriting packages start from £149 fitted. Partial and full wraps are quoted per vehicle, because size, coverage, artwork and film all change the price. Send your make and model, or use the Van Designer, for a quote.'),
    ('How long does it take?', 'Simple lettering is often fitted in a day. Partial and full wraps take longer, depending on the vehicle and whether old graphics need removing. We confirm timings with your quote.'),
    ('Can you put graphics on a leased van?', 'Yes. Quality vinyl removes cleanly from sound factory paint, which is why it suits leased vehicles. Check your lease terms and tell us when the van is due back.'),
    ('Will vinyl damage my paint?', 'Not on sound factory paint. Vinyl can lift poor-quality resprays or damaged paint, so send photos of any repairs and we will check before fitting.'),
    ('How long does a wrap last?', 'A quality cast vinyl with laminate lasts several years with good care. We give you aftercare advice for the film we fit.'),
    ('Can you help design my graphics?', 'Yes. Our team designs from your brief or works with your existing branding. You can also start with the free Van Designer and we will refine it.'),
    ('Where are vehicle graphics fitted?', 'At our workshop on Vulcan Road North, Norwich NR6 6AQ. Call 01603 407786 to book a fitting appointment.'),
    ('Can you do a whole fleet?', 'Yes. We create one master design, adapt it to each make and model, and fit in batches so the fleet keeps working.'),
    ('What areas do you cover?', f'We work with businesses across Norfolk and the Waveney valley, from King’s Lynn to Lowestoft. Fitting is at our Norwich workshop.'),
]
