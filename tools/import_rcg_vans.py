"""Import van model families, variants and graphics prices from the Race Car Graphics site build.
Usage: python3 tools/import_rcg_vans.py /path/to/rcg-website  ->  writes rcg_vans.json
Prices are RCG's single/two/full colour graphics prices (ex VAT) per variant."""
import json, re, sys, html
from pathlib import Path

rcg = Path(sys.argv[1] if len(sys.argv) > 1 else '/home/claude/rcg-website')
products = {p['sku']: p for p in json.loads((rcg / 'source/lib/crm/products.json').read_text()) if p.get('vehicle_type') == 'van'}
out = {}
for page in sorted((rcg / 'dist/product').glob('*-van-graphics/index.html')):
    h = page.read_text(errors='ignore')
    group = None
    for m in re.finditer(r'<script type="application/ld\+json"[^>]*>(.*?)</script>', h, re.S):
        try: d = json.loads(m.group(1))
        except Exception: continue
        if isinstance(d, dict) and d.get('@type') == 'ProductGroup': group = d; break
    if not group: continue
    variants = []
    for v in group.get('hasVariant', []):
        p = products.get(v.get('sku'))
        if not p: continue
        variants.append(dict(sku=p['sku'], model=p['model'], body=p.get('body_style') or 'Van',
                             prices={k: p['prices'][k] for k in ('single', 'two', 'full') if k in (p.get('prices') or {})}))
    if not variants: continue
    first = products[variants[0]['sku']]
    make, make_slug = first['make'], first['make_slug']
    name = html.unescape(group['name'])
    fam = re.sub(r'\s+Van Graphics.*$', '', name)
    fam = re.sub(r'^' + re.escape(make) + r'\s+', '', fam, flags=re.I).strip() or variants[0]['model']
    slug = page.parent.name[:-len('-van-graphics')]
    imgs = [i for i in group.get('image', []) if i.endswith('.webp')][:4]
    out.setdefault(make_slug, {'make': make, 'families': []})['families'].append(dict(
        name=fam, slug=slug, rcg_url=group.get('url'), images=imgs, variants=variants))
import shutil
dest = Path('dist/assets/vehicles/rcg')
for b in out.values():
    for f in b['families']:
        local = []
        for url in f['images']:
            name = url.rsplit('/', 1)[-1]
            src = rcg / 'dist' / url.split('racecargraphics.uk/', 1)[-1]
            if src.exists():
                (dest / f['slug']).mkdir(parents=True, exist_ok=True)
                shutil.copyfile(src, dest / f['slug'] / name)
                local.append(f'/assets/vehicles/rcg/{f["slug"]}/{name}')
        f['images'] = local
Path('rcg_vans.json').write_text(json.dumps(out, ensure_ascii=False, indent=1))
print(sum(len(b['families']) for b in out.values()), 'families,', sum(len(f['variants']) for b in out.values() for f in b['families']), 'variants,', len(out), 'makes')
