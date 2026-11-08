"""Real fitted jobs. Images in dist/assets/work/, named with our brand and job keywords."""
from html import escape

WORK = [  # (file, client, caption, alt, sectors)
    ('norwich-vehicle-graphics-gs-pro-clean-ford-transit-custom-printed-wrap', 'GS Pro Clean', 'Printed wrap on a black Ford Transit Custom', 'GS Pro Clean window cleaning van with a printed blue and white wrap on a black Ford Transit Custom', ('window-cleaners', 'cleaning')),
    ('norwich-vehicle-graphics-acdc-norfolk-electrician-ford-transit-custom-van-graphics', 'ACDC Norfolk Electrician', 'Signwriting on a Ford Transit Custom', 'ACDC Norfolk Electrician Ford Transit Custom with green lettering and a lightning plug graphic', ('electricians', 'trades')),
    ('norwich-vehicle-graphics-window-door-doctor-kia-pv5-partial-wrap-side', 'Window & Door Doctor', 'Partial wrap and signwriting on a Kia PV5', 'Window & Door Doctor Kia PV5 van with a green and black partial wrap and service list', ('trades',)),
    ('norwich-vehicle-graphics-reliable-garden-ford-transit-custom-van-graphics', 'Reliable Garden', 'Graphics on a red Ford Transit Custom', 'Reliable Garden and Property Maintenance red Ford Transit Custom with printed logo and services list', ('landscapers-gardeners', 'trades')),
    ('norwich-vehicle-graphics-benissimo-mercedes-sprinter-van-signwriting', 'Benissimo', 'Signwriting on a Mercedes Sprinter', 'Benissimo catering Mercedes Sprinter with black script logo and illustration on the bonnet and sides', ('food-drink',)),
    ('norwich-vehicle-graphics-gs-pro-clean-window-cleaning-van-graphics-side', 'GS Pro Clean', 'Window cleaning van graphics, side panel', 'Side of the GS Pro Clean van showing window cleaning, residential and commercial, fully insured graphics', ('window-cleaners', 'cleaning')),
    ('norwich-vehicle-graphics-acdc-norfolk-electrician-van-signwriting-side', 'ACDC Norfolk Electrician', 'Side panel with contact details', 'Side of the ACDC Norfolk Electrician van with phone, email, website and social icons', ('electricians',)),
    ('norwich-vehicle-graphics-reliable-garden-property-maintenance-van-livery', 'Reliable Garden', 'Rear three-quarter livery', 'Rear three-quarter view of the Reliable Garden van livery with phone number and services', ('landscapers-gardeners',)),
    ('norwich-vehicle-graphics-window-door-doctor-van-signwriting-rear-quarter', 'Window & Door Doctor', 'Rear quarter with phone numbers', 'Rear quarter of the Window & Door Doctor van with green phone number lettering', ('trades',)),
    ('norwich-vehicle-graphics-benissimo-sprinter-van-graphics-rear', 'Benissimo', 'Rear doors and side lettering', 'Rear of the Benissimo Sprinter with logo, website, phone and catering strapline', ('food-drink',)),
    ('norwich-vehicle-graphics-acdc-norfolk-electrician-van-rear-doors', 'ACDC Norfolk Electrician', 'Rear doors with logo and contact details', 'Rear doors of the ACDC Norfolk Electrician van with large logo, phone and website', ('electricians',)),
    ('norwich-vehicle-graphics-gs-pro-clean-van-wrap-rear', 'GS Pro Clean', 'Rear doors with phone and website', 'Rear of the GS Pro Clean Ford Transit Custom with phone number, website and pure water technology graphics', ('window-cleaners', 'cleaning')),
    ('norwich-vehicle-graphics-reliable-garden-van-rear-decals', 'Reliable Garden', 'Rear window and door decals', 'Rear of the red Reliable Garden van with printed rear window, phone number and website', ('landscapers-gardeners',)),
    ('norwich-vehicle-graphics-window-door-doctor-van-rear-door-graphics', 'Window & Door Doctor', 'Rear doors with website and services', 'Rear doors of the Window & Door Doctor van with website, phone numbers and services in lime green', ('trades',)),
    ('norwich-vehicle-graphics-benissimo-van-bonnet-logo', 'Benissimo', 'Bonnet logo close-up', 'Close-up of the Benissimo script logo and chef illustration on a Mercedes Sprinter bonnet', ('food-drink',)),
]

def work_for(sector):
    return [w for w in WORK if sector in w[4]]

def work_gallery(limit=None, heading=True, items=None):
    items = items if items is not None else (WORK[:limit] if limit else WORK)
    if not items:
        return ''
    figs = ''.join(f'<a class="work-tile" href="/assets/work/{f}.webp" data-caption="{escape(client)}: {escape(cap)}">'
                   f'<img src="/assets/work/{f}.webp" alt="{escape(alt)}" loading="lazy" width="1066" height="1600">'
                   f'<span><b>{escape(client)}</b>{escape(cap)}</span></a>' for f, client, cap, alt, _ in items)
    head = '<div class="work-head"><p class="eyebrow accent">Recent work</p><p>Real vans, fitted at our Norwich workshop. Tap a photo to enlarge.</p></div>' if heading else ''
    return f'<div class="work-gallery">{head}<div class="work-grid">{figs}</div></div>'
