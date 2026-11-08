"""Page sections for sector, location and contact routes."""

from html import escape
from urllib.parse import urlencode

from core_content import CONTENT, SECTOR_CARDS, SECTORS, TOWNS
from core_pages import ARROW, asset, case_study, info_cards, link_tiles, pricing, section, sector_cards, table
from local_content import SECTOR_DETAILS, TOWN_DETAILS

ADDRESS = 'Vulcan House, Vulcan Road North, Norwich NR6 6AQ'
MAP_QUERY = f'Broadland Digital, {ADDRESS}'


def directions(town=None):
    if town:
        return 'https://www.google.com/maps/dir/?' + urlencode(
            {'api': 1, 'origin': f'{town}, Norfolk, UK', 'destination': MAP_QUERY, 'travelmode': 'driving'})
    return 'https://www.google.com/maps/search/?' + urlencode({'api': 1, 'query': MAP_QUERY})


def workshop_map(phone, tel, email, town=None):
    source = 'https://maps.google.com/maps?' + urlencode({'q': MAP_QUERY, 'output': 'embed'})
    return f'''<div class="workshop-map"><div class="workshop-details">
    <p class="eyebrow blue">Norwich workshop</p><h3>Norwich Vehicle Graphics</h3>
    <address>Vulcan House<br>Vulcan Road North<br>Norwich, Norfolk NR6 6AQ</address>
    <p><a href="{tel}">{phone}</a><br><a href="mailto:{email}">{email}</a></p>
    <p>Call ahead to confirm your fitting appointment and drop-off arrangements.</p>
    <a class="btn dark" href="{escape(directions(town))}">{f'Directions from {escape(town)}' if town else 'Get directions'} {ARROW}</a>
    </div><iframe title="Map of the Norwich vehicle graphics workshop" src="{escape(source)}"
    width="640" height="360" loading="lazy" referrerpolicy="strict-origin-when-cross-origin" allowfullscreen></iframe></div>'''


def page_jumps(links):
    return '<nav class="page-jumps" aria-label="On this page"><div class="shell">' + ''.join(
        f'<a href="#{key}">{label}</a>' for key, label in links
    ) + '</div></nav>'


def design_examples(entries):
    return '<p class="core-note example-note">Illustrative vehicle graphics concepts.</p><div class="core-gallery">' + ''.join(
        f'<figure><img src="{asset(image)}" alt="{escape(caption)}" loading="lazy" width="840" height="473">'
        f'<figcaption><strong>{escape(caption)}</strong></figcaption></figure>'
        for image, caption in entries
    ) + '</div>'


def sector_sections(key):
    name, _ = SECTORS[key]
    intro, examples, package, package_copy, tips, project, brief, outcome, _, related = SECTOR_DETAILS[key]
    packages = (
        ('Signwriting', 'Published signwriting packages from £149', 'Logos, a service line and contact details.'),
        ('Partial wrap', 'Quoted per vehicle', 'Printed panels or colour across selected areas.'),
        ('Full wrap', 'Quoted per vehicle', 'Printed imagery or brand colours across most exterior panels.'),
        ('Fleet graphics', 'Quoted per fleet', 'A shared layout adapted for each make and model.'),
    )
    proof = f'<p class="core-prose">{escape(intro)} See our <a href="/vehicle-wraps-norwich/">van wraps in Norwich</a> for partial and full coverage options.</p>'
    budget = table(f'Price guide for {name}', ('Package', 'Price guide', 'Typical scope'), packages)
    budget += '<p class="core-note">The signwriting benchmark comes from <a href="/van-signwriting-norwich/#pricing">Broadland Digital’s published packages</a>. Ask for a fitted quote covering your vehicle size, artwork, film, coverage and VAT.</p>'
    return ''.join([
        page_jumps((('brief','Your brief'),('gallery','Designs'),('packages','Packages'),('pricing','Prices'),('case-study','Featured design'),('faq','FAQs'),('quote','Enquire'))),
        section(1,'brief','Your brief','What your vehicles need to say.',proof),
        section(2,'gallery','Sector gallery','See how the graphics could work.',design_examples(examples),'dark-section'),
        section(3,'packages','Recommended package',escape(package),f'<p class="core-prose">{escape(package_copy)}</p><p class="core-note"><a href="/vehicle-wraps-norwich/#comparison">Compare coverage options {ARROW}</a></p>'),
        section(4,'pricing','Price guide','Budget for the coverage you need.',budget,'tint'),
        section(5,'design-tips','Design tips','Build the layout around the job.',info_cards([(f'{i:02}', title, detail) for i,(title,detail) in enumerate(tips,1)])),
        section(6,'case-study','Featured design','See the brief and the layout.',case_study({'case':(project,brief,outcome,[examples[1 if key == 'automotive' else 0][0]])}),'dark-section'),
        section(7,'related-sectors','Related sectors','More ideas for working vehicles.',sector_cards(related),'tint'),
    ])


def town_questions(town):
    destination = 'in Norwich' if town == 'Norwich' else f'for businesses in {town}'
    return [
        (f'Where are vehicle graphics fitted {destination}?', f'We arrange fitting at {ADDRESS}. Call ahead to agree the appointment and drop-off.'),
        (f'Can I start my quote from {town}?', 'Yes. Send photos, the make and model, the coverage you want and your artwork if you have it. We can discuss the design before you bring the vehicle in.'),
        ('How much downtime should I plan?', 'Timing depends on the graphics, vehicle size and whether old film needs removing. We agree the fitting and collection arrangements before you book.'),
        ('Can you work around a fleet schedule?', 'Send us a list of the vehicles and their availability. We can discuss fitting in batches so you can keep the rest of your fleet working.'),
        ('Do you offer collection or fitting at my premises?', 'Standard fitting is arranged at the Norwich workshop. If you need collection or on-site fitting, tell us your postcode and requirements so we can discuss what is possible for the job.'),
    ]


def town_sections(key, services, phone, tel, email):
    town, _ = TOWNS[key]
    area, audience, tip, sectors, nearby = TOWN_DETAILS[key]
    intro = f'<div class="core-prose"><p>We design and fit <a href="/vehicle-wraps-norwich/">van wraps</a>, <a href="/van-signwriting-norwich/">van signwriting</a> and <a href="/fleet-graphics-norwich/">fleet graphics</a> for {escape(area)}. {escape(tip)}</p></div>'
    service_tiles = ''.join(f'<article id="{CONTENT[s["slug"]]["key"]}"><h3>{s["label"]}</h3><p>{s["short"]}</p><a class="text-link" href="/{s["slug"]}/">{s["label"]} in Norwich {ARROW}</a></article>' for s in services)
    design = [(SECTOR_CARDS[sector][0], SECTOR_CARDS[sector][1]) for sector in sectors[:3]]
    steps = info_cards([
        ('01','Send photos and vehicle details','Include photos of both sides and the rear. Share your logo, any existing graphics and your preferred timing.'),
        ('02','Review your proof','Approve the layout, coverage and fitting details before production.'),
        ('03','Bring the vehicle to Norwich','Check the directions and confirm drop-off and collection with the team before travelling.'),
    ])
    return ''.join([
        page_jumps((('services','Services'),('pricing','Prices'),('gallery','Designs'),('getting-here','Getting here'),('businesses','Local businesses'),('faq','FAQs'),('quote','Enquire'))),
        section(1,'intro','Area served',escape(area)+'.',intro),
        section(2,'services','Services','Choose graphics for your vehicle.',f'<div class="info-cards support-links">{service_tiles}</div>'),
        section(3,'pricing','Starting prices','What affects your quote?',pricing(CONTENT['van-signwriting-norwich'])+'<p class="core-note"><a href="/vehicle-wraps-norwich/#pricing">Wrap price guide</a> · <a href="/fleet-graphics-norwich/#pricing">Fleet quote guide</a></p>','tint'),
        section(4,'gallery','Design examples','Ideas for vans and fleets.',design_examples(design),'dark-section'),
        section(5,'getting-here','Travel &amp; fitting','Plan your workshop visit.',workshop_map(phone,tel,email,None if key == 'norwich' else town)),
        section(6,'fitting','From brief to fitting','Arrange the design before you travel.',steps,'tint'),
        section(7,'businesses','Local businesses',escape(audience)+'.',sector_cards(sectors)),
        section(8,'nearby','Nearby areas','Also serving these Norfolk towns.',link_tiles([(slug,(TOWNS[slug][0],)) for slug in nearby],lambda slug:f'/norfolk/{slug}/'),'tint'),
    ])
