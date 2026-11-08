"""Full guide page layout: hero, quick answer, sections, checklist, services, next guides."""
from html import escape
from core_pages import ARROW
from core_content import CONTENT, GUIDES
from sector_data import SECTORS_BY_KEY

def render_block(b):
    kind, data = b[0], (b[1] if len(b) == 2 else b[1:])
    if kind == 'p':
        return f'<p class="guide-p">{data}</p>'
    if kind == 'tip':
        return f'<div class="guide-tip"><b>Tip</b><p>{escape(data)}</p></div>'
    if kind == 'steps':
        return '<div class="guide-steps">' + ''.join(f'<div class="guide-step"><span>{n}</span><h3>{escape(t)}</h3><p>{escape(d)}</p></div>' for n, (t, d) in enumerate(data, 1)) + '</div>'
    if kind == 'zones':
        from core_pages import van_diagram
        pins = '<i class="pin p1">1</i><i class="pin p2">2</i><i class="pin p3">3</i>'
        cards = ''.join(f'<div class="guide-zone"><span class="zone-n">{n}</span><h3>{escape(t)}</h3><small>{escape(sub)}</small><ul>' + ''.join(f'<li>{escape(x)}</li>' for x in items) + '</ul></div>'
                        for n, (t, sub, items) in zip((1, 2, 3), data))
        return f'<div class="guide-zones"><div class="zone-van">{van_diagram("graphics")}{pins}</div><div class="zone-cards">{cards}</div></div>'
    if kind == 'compare':
        (yt, yes), (nt, no) = data
        return (f'<div class="guide-compare"><div class="is-yes"><h3>{escape(yt)}</h3><ul>' + ''.join(f'<li>{escape(x)}</li>' for x in yes) + '</ul></div>'
                f'<div class="is-no"><h3>{escape(nt)}</h3><ul>' + ''.join(f'<li>{escape(x)}</li>' for x in no) + '</ul></div></div>')
    if kind == 'mistakes':
        return '<div class="guide-mistakes">' + ''.join(f'<div class="guide-mistake"><h3>{escape(t)}</h3><p>{escape(why)}</p><p class="fix"><b>Fix:</b> {escape(fix)}</p></div>' for t, why, fix in data) + '</div>'
    return ''

def guide_body(key, g, services):
    toc = ''.join(f'<li><a href="#s{i}">{escape(h)}</a></li>' for i, (h, _) in enumerate(g['sections'], 1))
    alt, img = g['image']
    figure = f'<figure class="guide-figure"><img src="/assets/sectors/gallery/{img}.webp" alt="{escape(alt)}" loading="lazy" width="1680" height="946"><figcaption>{escape(alt)}.</figcaption></figure>'
    body = ''
    for i, (h, blocks) in enumerate(g['sections'], 1):
        body += f'<section class="guide-section" id="s{i}"><div class="guide-section__head"><span class="guide-num">{i:02}</span><h2>{escape(h)}</h2></div>' + ''.join(render_block(b) for b in blocks) + '</section>'
        if i == 2:
            body += figure
    checklist = ''.join(f'<li>{escape(c)}</li>' for c in g['checklist'])
    svc = {s['slug']: s for s in services}
    service_cards = ''.join(f'<a class="guide-card" href="/{slug}/"><small>Service</small><b>{svc[slug]["label"]}</b><span>{escape(svc[slug]["short"])}</span><em>View service {ARROW}</em></a>' for slug in g['services'])
    service_cards += f'<a class="guide-card is-accent" href="/design-your-van/#designer"><small>Free tool</small><b>Van Designer</b><span>See your layout on your exact van in about a minute.</span><em>Start designing {ARROW}</em></a>'
    sector_links = ' · '.join(f'<a href="/sectors/{k}/">{escape(SECTORS_BY_KEY[k]["name"])}</a>' for k in g['sectors'])
    nxt = ''.join(f'<a class="guide-card" href="/guides/{k}/"><small>Guide</small><b>{escape(GUIDES[k][0])}</b><span>{escape(GUIDES[k][1][:120])}…</span><em>Read guide {ARROW}</em></a>' for k in g['next'])
    return f'''<section class="support-hero guide-hero"><div class="shell"><nav class="crumb" aria-label="Breadcrumb"><a href="/">Home</a><span aria-hidden="true">/</span><a href="/#guides">Guides</a><span aria-hidden="true">/</span><span>{escape(GUIDES[key][0])}</span></nav>
    <p class="eyebrow accent">{escape(g["topic"])} · {g["read"]} minute read</p><h1>{escape(g["h1"])}</h1><p class="lede">{escape(g["summary"])}</p>
    <div class="actions"><a class="btn" href="#quote">Get a free quote {ARROW}</a><a class="btn outline" href="/design-your-van/#designer">Try the Van Designer {ARROW}</a></div></div></section>
    <section class="guide-stats"><div class="shell"><p class="guide-stats__label">At a glance</p><div class="guide-stats__grid">{''.join(f'<div class="guide-stat"><b>{escape(n)}</b><span>{escape(t)}</span></div>' for n, t in g.get('takeaways', []))}</div></div></section>
    <section class="section guide-layout"><div class="shell guide-grid">
      <aside class="guide-toc"><p>In this guide</p><ol>{toc}</ol><a class="btn dark" href="#quote">Get a free quote {ARROW}</a></aside>
      <article class="guide-article"><div class="guide-answer"><p class="guide-answer__label">Quick answer</p><p>{escape(g["answer"])}</p></div>{body}
        <div class="guide-checklist"><h2>What to have ready for your quote</h2><ul>{checklist}</ul></div>
        <p class="guide-sectors">Ideas by trade: {sector_links}</p></article>
    </div></section>
    <section class="section tint"><div class="shell"><div class="section-head"><div><p class="eyebrow blue">Next step</p><h2>Turn it into a design.</h2></div></div><div class="guide-cards">{service_cards}</div></div></section>
    <section class="section"><div class="shell"><div class="section-head"><div><p class="eyebrow blue">Keep reading</p><h2>More van graphics guides.</h2></div></div><div class="guide-cards">{nxt}</div></div></section>'''

def guide_schema(origin, key, g, business_id):
    url = f'{origin}/guides/{key}/'
    return {'@context': 'https://schema.org', '@graph': [
        {'@type': 'Article', 'headline': GUIDES[key][0], 'description': g['summary'], 'url': url, 'mainEntityOfPage': url,
         'image': f'{origin}/assets/sectors/gallery/{g["image"][1]}.webp', 'author': {'@id': business_id}, 'publisher': {'@id': business_id}, 'inLanguage': 'en-GB'},
        {'@type': 'FAQPage', 'mainEntity': [{'@type': 'Question', 'name': q, 'acceptedAnswer': {'@type': 'Answer', 'text': a}} for q, a in g['faq']]},
        {'@type': 'BreadcrumbList', 'itemListElement': [
            {'@type': 'ListItem', 'position': 1, 'name': 'Home', 'item': origin + '/'},
            {'@type': 'ListItem', 'position': 2, 'name': 'Guides', 'item': origin + '/guides/'},
            {'@type': 'ListItem', 'position': 3, 'name': GUIDES[key][0], 'item': url}]}]}
