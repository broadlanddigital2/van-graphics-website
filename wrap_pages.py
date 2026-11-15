"""Dedicated partial wrap and full wrap pages. /vehicle-wraps-norwich/ stays as the overview linking to both."""
from html import escape

G = '/assets/sectors/gallery/norwich-vehicle-graphics-'
W = '/assets/work/norwich-vehicle-graphics-'

WRAP_PAGES = [
    dict(
        key='partial', slug='partial-van-wraps-norwich', label='Partial wraps', short='Printed colour on selected panels, with the paint doing the rest.',
        title='Partial van wraps in Norwich', h1='Partial van wraps<span>in Norwich.</span>',
        meta_title='Partial Van Wraps Norwich | Half Wraps & Panel Graphics',
        meta_desc='Partial and half van wraps in Norwich: printed colour on the rear half, lower sides or a bold sweep, using your paint as part of the design. Quoted per vehicle.',
        hero=G + 'heating-engineer-partial-wrap-with-flame-and-water-swoosh.webp', hero_alt='Silver van with a red and blue partial wrap sweeping along the side for a heating engineer',
        lede='Printed colour where it counts, with your van’s own paint doing the rest. A partial wrap gives you wrap-level impact for a fraction of the coverage.',
        chips=['Quoted per vehicle', 'Uses your paint colour', 'Proof before print'],
        bar=['Rear half', 'Lower sides', 'Colour sweeps', 'Panels plus lettering'],
        what_title='Where a partial wrap goes.',
        what_intro='A partial wrap covers part of the van in printed vinyl and leaves the rest in its original colour. Done well, the two read as one design: the paint becomes the background, and the printed area carries the colour, imagery and brand.',
        layouts=[
            ('Rear half', 'From behind the side door back over the rear arch, corner and doors. The most popular layout, and the side most people see when parked or in traffic.'),
            ('Lower sides and doors', 'A band of colour along the sills and lower panels, with lettering above on the paint. Good for vans with racking or ladders on the roof.'),
            ('Colour sweep', 'A curved or angled sweep that runs the length of the van, often from the front wheel to the back corner. Bold without covering everything.'),
            ('Bonnet, roof or pillars', 'Accent panels in a brand colour that tie the van together, paired with cut vinyl for the details.'),
        ],
        gallery=[
            (W + 'window-door-doctor-kia-pv5-partial-wrap-side.webp', 'Window & Door Doctor', 'Green and black partial wrap on a Kia PV5', True),
            (G + 'kitchen-fitter-partial-wrap-with-copper-detail.webp', 'Kitchen fitter', 'Copper rear corner on a navy van', False),
            (G + 'landscaper-partial-wrap-with-a-leaf-motif.webp', 'Landscaper', 'Leaf motif across the rear half', False),
            (G + 'dog-groomer-partial-wrap-with-paw-prints.webp', 'Dog groomer', 'Paw-print sweep with lettering on the paint', False),
            (G + 'flat-roofing-partial-wrap-below-the-racks.webp', 'Roofer', 'Lower-side wrap that stays clear of the roof racks', False),
            (G + 'detailing-van-partial-wrap.webp', 'Detailer', 'Gloss black rear section with a colour flash', False),
        ],
        compare_focus='partial',
        good_for=[
            ('You want more than lettering', 'Signwriting gets your name and number across. A partial wrap adds colour and character so the van is remembered, not just read.'),
            ('Your van is already a good colour', 'White, silver, black and many fleet colours make a strong base. The wrap is designed to work with the paint, not hide it.'),
            ('You run several vans', 'Less vinyl per vehicle keeps a fleet roll-out affordable, and the layout adapts easily between makes.'),
            ('The van is leased', 'Less coverage means less to remove when the lease ends, using films designed to come off cleanly.'),
        ],
        price_focus=('half',),
        price_note='Partial wraps are quoted per vehicle because the coverage varies so much. Most quotes come down to the van size, how much of it is covered, how detailed the artwork is and whether old graphics need removing first. Signwriting packages are shown alongside, because many partial wraps include cut vinyl lettering on the painted areas.',
        steps=[
            ('Send photos', 'A photo of each side and the back, your logo and the words you want. Or start in the free Van Designer.'),
            ('Approve the layout', 'We mark up where the printed area starts and stops on your exact van, and send a visual to approve.'),
            ('Print and laminate', 'Printed on cast wrap film and laminated in-house, then cut to the panel shapes.'),
            ('Fit and collect', 'Fitted indoors at our St Faiths Road workshop. Most partial wraps are a one-day job.'),
        ],
        notes=[
            ('Paint condition matters', 'Vinyl sits on top of the paint, so chips, rust and flaking lacquer show through or lift. Send photos and we’ll tell you what needs sorting first; we can arrange panel repairs too.'),
            ('Colour matching', 'We match printed colours to your paint and brand as closely as print allows, and show you on the proof where the wrap meets the paint.'),
            ('Removal', 'Partial wraps can be removed professionally. How cleanly they come off depends on the paint underneath, the film and how long it has been on.'),
        ],
        faq=[
            ('How much of the van does a partial wrap cover?', 'Anything from a single sweep to roughly half the van. The most common layout is the rear half, from behind the side door back to the rear doors.'),
            ('Is a partial wrap cheaper than a full wrap?', 'Yes. You are paying for less printed film and less fitting time. The exact saving depends on the van and how much is covered, which is why we quote each one.'),
            ('Can you match the wrap to my van’s colour?', 'We design the printed area to sit alongside your paint colour and match it as closely as print allows. The proof shows exactly where the two meet.'),
            ('Can I add lettering on the painted part?', 'Yes, and most partial wraps do. Cut vinyl lettering on the paint keeps the name and number crisp while the wrap carries the colour.'),
            ('How long does fitting take?', 'Most partial wraps are fitted in a day at our Norwich workshop. Larger vans or extra prep can add time; we confirm it when you book.'),
            ('Will it damage the paint?', 'Applied to sound factory paint and removed professionally, it should not. Resprayed or damaged panels carry more risk, so we check photos before quoting.'),
        ],
        related=[('Full van wraps', '/full-van-wraps-norwich/'), ('Van signwriting', '/van-signwriting-norwich/'), ('All vehicle wraps', '/vehicle-wraps-norwich/'), ('Partial wrap vs full wrap', '/guides/partial-wrap-vs-full-wrap/')],
    ),
    dict(
        key='full', slug='full-van-wraps-norwich', label='Full wraps', short='Printed vinyl over almost every painted panel for a complete transformation.',
        title='Full van wraps in Norwich', h1='Full van wraps<span>in Norwich.</span>',
        meta_title='Full Van Wraps Norwich | Printed & Colour Change Wraps',
        meta_desc='Full van wraps in Norwich: printed imagery or a colour change over almost every painted panel, designed, printed and fitted in-house. Quoted per vehicle.',
        hero=G + 'conservation-charity-full-wrap.webp', hero_alt='Blue van fully wrapped with a coastal seal scene for a conservation charity',
        lede='Turn the whole van into your advert. Printed imagery or a complete colour change across almost every painted panel, designed around your exact model.',
        chips=['Quoted per vehicle', 'Bonnet to rear doors', 'Proof before print'],
        bar=['Printed imagery', 'Colour change', 'Bumpers & mirrors', 'Lease-friendly films'],
        what_title='What a full wrap covers.',
        what_intro='A full wrap covers the painted body of the van in printed or coloured vinyl: bonnet, roof where needed, sides, doors, rear and usually the bumpers and mirror caps. Nothing of the original paint colour is left on show, so the design has the whole van to work with.',
        layouts=[
            ('Printed imagery', 'Photos, illustrations and brand graphics printed edge to edge. The biggest canvas a van offers, ideal for food, events and visitor-facing businesses.'),
            ('Colour change', 'A new body colour in gloss, satin or matt, with lettering on top. A cleaner alternative to a respray that can come off later.'),
            ('Brand livery', 'Your colours, shapes and logo carried round every panel, so the van looks the same from every angle.'),
            ('Box bodies and Lutons', 'Full coverage of the box sides and front, where the flat panels make the most of a printed design.'),
        ],
        gallery=[
            (W + 'gs-pro-clean-ford-transit-custom-printed-wrap.webp', 'GS Pro Clean', 'Printed blue and white wrap on a black Transit Custom', True),
            (G + 'electric-van-full-brand-wrap.webp', 'Energy installer', 'Blue to green gradient full wrap on an electric van', False),
            (G + 'luton-removals-van-full-wrap.webp', 'Removals', 'Full box body wrap on a Luton', False),
            (G + 'full-wrap-for-an-ev-charger-installer.webp', 'EV charger installer', 'Green and white livery with a charging cable graphic', False),
            (G + 'coffee-van-wrap-with-bean-pattern.webp', 'Coffee van', 'All-over bean pattern wrap', False),
            (G + 'furniture-store-delivery-van-wrap.webp', 'Furniture store', 'Lifestyle imagery across the delivery van', False),
        ],
        compare_focus='full',
        good_for=[
            ('You want maximum impact', 'A fully wrapped van is impossible to miss on the road and on a driveway, and gives you room for imagery that signwriting can’t carry.'),
            ('The van’s colour doesn’t suit your brand', 'Change the whole colour without a respray, and keep the original paint protected underneath.'),
            ('You sell something visual', 'Food, events, home improvement and retail all benefit from showing the product, not just naming it.'),
            ('You want to protect the paint', 'A full wrap covers the paintwork from light scratches and stone chips while it’s on.'),
        ],
        price_focus=('full',),
        price_note='Full wraps are quoted per vehicle. Van size, roof and bumper coverage, the film (printed, colour change or specialist finish), artwork preparation and any old graphics or paint repairs all affect the price. Signwriting packages are shown for comparison.',
        steps=[
            ('Brief and photos', 'Tell us about the van and the look you want. Send photos of every side, plus any artwork or images you’d like to use.'),
            ('Design and proof', 'We lay the design out on a template of your exact model, so you see how it wraps round doors, handles and curves.'),
            ('Print and laminate', 'Printed on conformable cast wrap film and laminated in-house for protection.'),
            ('Prep, fit and check', 'The van is cleaned and decontaminated, then fitted indoors at our St Faiths Road workshop. Allow two to three days for most full wraps.'),
        ],
        notes=[
            ('Prep makes the finish', 'Wax, road film and old adhesive stop vinyl bonding. Every full wrap starts with a deep clean; Auto Opulence can add a clay bar decontamination or polish first.'),
            ('Leased vans', 'Check your lease terms before fitting. Full wraps can be removed professionally at the end of the lease; how cleanly depends on the paint and how long the wrap has been on.'),
            ('Aftercare', 'Hand wash with a vinyl-safe shampoo, keep pressure washers away from edges and avoid waxes made for paint. Our wrap aftercare guide covers the details.'),
        ],
        faq=[
            ('What does a full wrap cover?', 'The painted body of the van: bonnet, sides, doors, rear and usually bumpers and mirror caps. The roof is included where it shows, for example on high-roof vans.'),
            ('How long does a full wrap take to fit?', 'Allow two to three days at our Norwich workshop for most vans, including prep. Larger vehicles and box bodies can take longer.'),
            ('Can you change the colour of my van?', 'Yes. A colour change wrap gives the whole van a new gloss, satin or matt colour without a respray, and can be removed later.'),
            ('Does a full wrap protect the paint?', 'It covers the paint from light scratches, stone chips and fading while it is on. It won’t fix existing damage, so we check the paint first.'),
            ('Can I use my own photos?', 'Yes, if they are high resolution and you have the rights to use them. We’ll tell you if an image is too small to print at van size.'),
            ('Is a full wrap worth it over a partial?', 'If you want imagery, a colour change or the most impact, yes. If your paint colour already works with your brand, a partial wrap often gives a similar result for less.'),
        ],
        related=[('Partial van wraps', '/partial-van-wraps-norwich/'), ('Van signwriting', '/van-signwriting-norwich/'), ('All vehicle wraps', '/vehicle-wraps-norwich/'), ('How to look after a wrap', '/guides/vehicle-wrap-aftercare/')],
    ),
]

COMPARE = [('signwriting', 'Van signwriting', 'Cut vinyl name, logo and contact details on the paint.', '/van-signwriting-norwich/', 'From £149 + VAT'),
           ('partial', 'Partial wrap', 'Printed colour on selected panels, lettering on the rest.', '/partial-van-wraps-norwich/', 'Quoted per vehicle'),
           ('full', 'Full wrap', 'Printed or coloured vinyl over almost every painted panel.', '/full-van-wraps-norwich/', 'Quoted per vehicle')]


def wrap_hero(p, button):
    chips = ''.join(f'<li>{escape(c)}</li>' for c in p['chips'])
    bar = ''.join(f'<li>{escape(b)}</li>' for b in p['bar'])
    return f'''<section class="sector-hero service-hero is-dedicated wrap-hero">
    <img class="sector-hero__img" src="{p['hero']}" alt="{escape(p['hero_alt'])}" fetchpriority="high" width="1680" height="946">
    <div class="shell sector-hero__inner"><div class="sector-hero__copy">
    <nav class="crumb" aria-label="Breadcrumb"><a href="/">Home</a><span aria-hidden="true">/</span><a href="/vehicle-wraps-norwich/">Vehicle wraps</a><span aria-hidden="true">/</span><span>{escape(p['label'])}</span></nav>
    <p class="eyebrow accent">Design · Print · Fitting in Norwich</p><h1>{p['h1']}</h1>
    <p class="lede">{escape(p['lede'])}</p>
    <div class="actions">{button('Get a free quote', '#quote')}<a class="btn outline" href="#examples">See examples</a></div>
    <ul class="sector-hero__chips">{chips}</ul></div></div>
    <div class="sector-hero__bar"><div class="shell"><p>Options</p><ul>{bar}</ul></div></div></section>'''


def wrap_body(p, section, price_matrix, price_quote_form, care_upsell, repair_block, faq):
    layouts = ''.join(f'<article><h3>{escape(t)}</h3><p>{escape(d)}</p></article>' for t, d in p['layouts'])
    what = f'<div class="core-prose wrap-intro"><p>{escape(p["what_intro"])}</p></div><div class="info-cards wrap-layouts">{layouts}</div>'

    figs = ''.join(f'<figure class="{"is-real" if real else ""}"><img src="{src}" alt="{escape(client)}: {escape(cap)}" loading="lazy" width="1680" height="946">'
                   f'<figcaption><b>{escape(client)}</b><small>{escape(cap)}{" · fitted job" if real else " · design idea"}</small></figcaption></figure>'
                   for src, client, cap, real in p['gallery'])
    gallery = f'<div class="core-gallery wrap-gallery">{figs}</div><p class="core-note">Fitted jobs are marked; the rest are design ideas to show what each layout can look like. <a class="text-link" href="/gallery/">See the full gallery</a></p>'

    cmp = ''.join(f'<a class="wrap-compare__card{" is-current" if k == p["compare_focus"] else ""}" href="{href}"{" aria-current=\"page\"" if k == p["compare_focus"] else ""}>'
                  f'<img src="/assets/pages/compare-{k}.webp" alt="{escape(name)} on a Ford Transit Custom" loading="lazy" width="1200" height="800">'
                  f'<span class="wrap-compare__body"><b>{escape(name)}</b><small>{escape(desc)}</small><em>{escape(price)}</em>'
                  f'{"<i>You are here</i>" if k == p["compare_focus"] else "<i>Compare</i>"}</span></a>' for k, name, desc, href, price in COMPARE)
    compare = f'<div class="wrap-compare">{cmp}</div>'

    good = ''.join(f'<article><h3>{escape(t)}</h3><p>{escape(d)}</p></article>' for t, d in p['good_for'])
    good = f'<div class="info-cards wrap-good">{good}</div>'

    price = (price_matrix(p['price_focus']) + f'<p class="core-note">{escape(p["price_note"])}</p>'
             + '<div class="pm-quote"><div class="pm-quote__aside"><h3>Get an exact price</h3><p>Send the make, model and year with a photo of each side, and we’ll come back with a fitted price in writing, VAT shown.</p>'
             + '<ul class="quote-ticks"><li>Free design visual on your exact van</li><li>Prices shown + VAT</li><li>Designed, printed and fitted in Norwich</li></ul></div>'
             + price_quote_form(p['label'].rstrip('s')) + '</div>')

    steps = ''.join(f'<li><b>{n:02}</b><h3>{escape(t)}</h3><p>{escape(d)}</p></li>' for n, (t, d) in enumerate(p['steps'], 1))
    steps = f'<ol class="timeline wrap-steps">{steps}</ol>'

    notes = ''.join(f'<article><h3>{escape(t)}</h3><p>{escape(d)}</p></article>' for t, d in p['notes'])
    notes = f'<div class="info-cards wrap-notes">{notes}</div>'

    related = ''.join(f'<a class="btn outline" href="{h}">{escape(t)}</a>' for t, h in p['related'])

    return ''.join([
        section(1, 'what', 'The layout', p['what_title'], what),
        section(2, 'examples', 'Examples', 'Fitted jobs and design ideas.', gallery, 'dark-section'),
        section(3, 'compare', 'Compare', 'Signwriting, partial or full wrap?', compare, 'tint'),
        section(4, 'good-for', 'Is it right for you?', f'When a {p["label"].lower().rstrip("s")} makes sense.', good),
        section(5, 'pricing', 'Price guide', 'What affects the price.', price, 'tint'),
        section(6, 'process', 'How it works', 'From photos to fitted.', steps),
        section(7, 'notes', 'Good to know', 'Before you book.', notes, 'tint'),
        care_upsell('van'),
        repair_block('van'),
        faq(p['faq']),
        f'<section class="section wrap-related"><div class="shell"><p class="eyebrow blue">Keep exploring</p><div class="wrap-related__links">{related}</div></div></section>',
    ])
