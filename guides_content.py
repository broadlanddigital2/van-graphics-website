"""Full guide pages, following the guides brief (Race Car Graphics style).
Guides not listed here still render as the short support page."""

FULL_GUIDES = {
'van-signwriting-brief': {
    'topic': 'Plan & budget',
    'read': 6,
    'title': 'What to Put on a Work Van | Van Signwriting Layout Guide',
    'h1': 'What to put on a work van.',
    'summary': 'What to include in your van signwriting, where it should go and what to leave off, so people can read it and remember it.',
    'answer': ('Put three things on every work van: your business name, what you do and one clear way to contact you. '
               'Add a website, social handles or accreditations only if there is room for people to read them at a glance.'),
    'takeaways': [('3', 'things every van needs'), ('3', 'sides, each with its own job'), ('1', 'contact detail to push')],
    'sections': [
        ('The three things every van needs', [
            ('p', 'Most people see your van for a few seconds, often while they are driving or walking past. In that time they need to take in who you are, what you do and how to reach you. Everything else is a bonus.'),
            ('steps', [('Your business name', 'The biggest thing on the van, placed high where nothing breaks it up.'),
                       ('What you do', 'A short service line in plain words, such as "Plumbing · Heating · Bathrooms".'),
                       ('One way to contact you', 'Usually a phone number for trades, or a website if most work is booked online.')]),
            ('tip', 'Write your van signwriting layout with just these three first. Only add more if the van still reads clearly from across the road.'),
        ]),
        ('Where each detail goes', [
            ('p', 'Each side of a van is seen in a different way, so each one has a different job. Plan the layout panel by panel rather than copying the same thing everywhere.'),
            ('zones', [('Sides', 'Read from the pavement and the drive', ['Name high on the panel, above swage lines and handles', 'Service line close to the name', 'Phone or website lower down, for people nearby', 'Nothing important across the sliding-door gap']),
                       ('Back doors', 'Read in traffic, often for minutes', ['Phone number or website as large as the doors allow', 'Name and logo repeated', 'Plan around windows, plate, lights and handles', 'Check racks and ladders will not hide it']),
                       ('Front & bonnet', 'Read in mirrors and by oncoming traffic', ['Logo or name only', 'Keep it simple and bold', 'No contact details: nobody can note a number from an oncoming van'])]),
        ]),
        ('Accreditations, socials and extras', [
            ('p', 'Extras can build trust, but each one takes space from the details that win you work. Use this as a quick filter.'),
            ('compare', ('Worth adding', ['Trade badges you are approved to show (Gas Safe, NICEIC, TrustMark)', 'Social handles on the back doors', 'A QR code, if you park where customers can walk up to it', 'Your town or "Serving Norfolk" to show you are local']),
                        ('Usually leave off', ['Prices: they change and date quickly', 'Long lists of every service you offer', 'Slogans that do not say what you do', 'Small text that cannot be read at a distance'])),
        ]),
        ('Common van lettering mistakes', [
            ('mistakes', [('Too much text', 'Every extra line makes the important ones smaller.', 'Cut to name, service line and one contact.'),
                          ('Low contrast', 'Pale lettering on a white van, or dark on a dark van, disappears at distance.', 'Pick colours that stand out from the paint.'),
                          ('Hard-to-read fonts', 'Script and thin fonts look stylish close up but blur from across the road.', 'Use a bold, simple font for the key details.'),
                          ('Ignoring the van shape', 'Lettering across door gaps, handles or deep panel lines breaks up.', 'Lay it out on your exact model first.'),
                          ('Different details each side', 'A different number or name on each side is hard to remember.', 'Keep name, number and colours the same everywhere.'),
                          ('Hidden by racks or ladders', 'Graphics behind a roof rack or ladder are wasted.', 'Tell us what is fitted to the van.')]),
        ]),
    ],
    'checklist': [
        'Your business name exactly as you want it shown',
        'A short service line (three or four words at most)',
        'The one contact detail you want people to remember',
        'Your logo as a vector file, if you have one',
        'Brand colours or the colour of your van',
        'Any trade badges you are approved to display',
        'Roof racks, ladders or tool boxes that could hide graphics',
        'Van make, model and wheelbase',
    ],
    'image': ('Ford Transit Custom with clear signwriting showing a business name and service line', 'norwich-vehicle-graphics-cut-vinyl-signwriting-for-a-general-builder'),
    'services': ['van-signwriting-norwich', 'vehicle-wraps-norwich'],
    'sectors': ['trades', 'plumbers-heating', 'electricians'],
    'next': ['artwork-for-van-graphics', 'graphics-costs', 'partial-vs-full-wrap'],
    'faq': [
        ('How big should the phone number be on a van?', 'As big as the panel allows while keeping it on one line. On the back doors it should be readable from a car behind you in traffic. We size it to your van and show you a visual before anything is printed.'),
        ('Should I put my prices on my van?', 'Usually not. Prices change, and a van that shows out-of-date prices can put people off. Send people to your website or phone instead, where you can give a current quote.'),
        ('Do I need my logo on every side?', 'It helps people recognise you from any angle, but your name matters more than the logo. If space is tight, put the logo on the sides and back and keep the front simple.'),
        ('Can you help if I don\'t know what to put on my van?', 'Yes. Tell us what you do and who your customers are, and we will suggest a layout. You can also try the free Van Designer to see ideas on your exact van first.'),
    ],
},
}

from guides_more import MORE_GUIDES
FULL_GUIDES.update(MORE_GUIDES)
