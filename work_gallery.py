"""Real fitted jobs. Images in dist/assets/work/, named with our brand and job keywords."""
from html import escape

WORK = [
    ('norwich-vehicle-graphics-gs-pro-clean-ford-transit-custom-printed-wrap', 'GS Pro Clean', 'Printed wrap on a black Ford Transit Custom', 'GS Pro Clean window cleaning van with a printed blue and white wrap on a black Ford Transit Custom'),
    ('norwich-vehicle-graphics-window-door-doctor-kia-pv5-partial-wrap-side', 'Window & Door Doctor', 'Partial wrap and signwriting on a Kia PV5', 'Window & Door Doctor Kia PV5 van with a green and black partial wrap and service list'),
    ('norwich-vehicle-graphics-gs-pro-clean-window-cleaning-van-graphics-side', 'GS Pro Clean', 'Window cleaning van graphics, side panel', 'Side of the GS Pro Clean van showing window cleaning, residential and commercial, fully insured graphics'),
    ('norwich-vehicle-graphics-window-door-doctor-van-signwriting-rear-quarter', 'Window & Door Doctor', 'Rear quarter with phone numbers', 'Rear quarter of the Window & Door Doctor van with green phone number lettering'),
    ('norwich-vehicle-graphics-gs-pro-clean-van-wrap-rear', 'GS Pro Clean', 'Rear doors with phone and website', 'Rear of the GS Pro Clean Ford Transit Custom with phone number, website and pure water technology graphics'),
    ('norwich-vehicle-graphics-window-door-doctor-van-rear-door-graphics', 'Window & Door Doctor', 'Rear doors with website and services', 'Rear doors of the Window & Door Doctor van with website, phone numbers and services in lime green'),
]

def work_gallery(limit=None, heading=True):
    items = WORK[:limit] if limit else WORK
    figs = ''.join(f'<a class="work-tile" href="/assets/work/{f}.webp" data-caption="{escape(client)}: {escape(cap)}">'
                   f'<img src="/assets/work/{f}.webp" alt="{escape(alt)}" loading="lazy" width="1066" height="1600">'
                   f'<span><b>{escape(client)}</b>{escape(cap)}</span></a>' for f, client, cap, alt in items)
    head = '<div class="work-head"><p class="eyebrow accent">Recent work</p><p>Real vans, fitted at our Norwich workshop. Tap a photo to enlarge.</p></div>' if heading else ''
    return f'<div class="work-gallery">{head}<div class="work-grid">{figs}</div></div>'
