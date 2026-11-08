"""Service-specific editorial content and navigation for the core pages."""

MODELS = {
    'transit-custom': ('Ford Transit Custom', 'Medium van', 'Check the generation and wheelbase before laying out the sliding door. A short service line fits above the body crease, while the rear doors can carry a phone number or website.'),
    'vivaro': ('Vauxhall Vivaro', 'Medium van', 'Send the model year and a photo of both sides. Panel lengths and charging-port locations vary by generation and powertrain. Keep contact details clear of the sliding door handle.'),
    'caddy': ('Volkswagen Caddy', 'Small van', 'The compact rear quarter rewards a short message. Confirm whether it is a Caddy or Caddy Maxi before approving a proof, and flag glazing or trim that reduces the available space.'),
    'berlingo': ('Citroën Berlingo', 'Small van', 'Use the broad side panel for the brand and a short line describing your trade. On an electric Berlingo, show us where the charge flap opens so the design can work around it.'),
    'partner': ('Peugeot Partner', 'Small van', 'Photograph roof racks, ladders and both rear doors before briefing the design. Repeat one contact detail on the rear so it stays legible when equipment is loaded.'),
    'sprinter': ('Mercedes-Benz Sprinter', 'Large van', 'Confirm the wheelbase and roof height. High-roof and long-wheelbase variants offer extra space, but the handle, sliding-door runner and deep panel recesses still shape the layout.'),
    'luton': ('Luton box van', 'Box van', 'Supply the box dimensions and photos of the rear shutter or tail lift. Panel joints, rivets and the peak above the cab affect the artwork, film specification and fitting quote.'),
}

MODELS.update({
    'ford-transit': ('Ford Transit', 'Large van', 'Tell us the length and roof height. The cargo panels on a high-roof Transit offer extra space for a trade name while the rear doors can carry a short service line.'),
    'transit-connect': ('Ford Transit Connect', 'Small van', 'Use a compact side layout and check whether the rear is glazed. We can place contact details below the window line to keep them readable.'),
    'vauxhall-combo': ('Vauxhall Combo', 'Small van', 'Send the model year and wheelbase. A compact logo above the panel crease leaves room to repeat the business name on the rear doors.'),
    'vauxhall-movano': ('Vauxhall Movano', 'Large van', 'High roofs and long wheelbases give you more space for large lettering. Share photos of the actual side and rear panels before approving the layout.'),
    'vw-transporter': ('Volkswagen Transporter', 'Medium van', 'Confirm the generation and whether the rear has a tailgate or barn doors. That determines where a logo or web address can sit cleanly.'),
    'vw-crafter': ('Volkswagen Crafter', 'Large van', 'Measure around any aftermarket windows, roof accessories or ladders. A long side panel can carry a larger brand mark while keeping text clear of the sliding door hardware.'),
    'citroen-dispatch': ('Citroën Dispatch', 'Medium van', 'Send photos with the doors closed so we can lay out the lettering around the runner and handles. Include the charge flap if you have an electric model.'),
    'citroen-relay': ('Citroën Relay', 'Large van', 'Share the roof height and wheelbase. On conversion bodies, include any vents or service hatches that affect how the artwork runs across the panel.'),
    'peugeot-expert': ('Peugeot Expert', 'Medium van', 'Start with a photo of each side because door and trim layouts can vary. Keep key details above the lower moulding and away from the sliding-door handle.'),
    'peugeot-boxer': ('Peugeot Boxer', 'Large van', 'Confirm the body length and roof height when enquiring. The broad rear doors suit a clear name and one contact detail, with the seam kept clear of small lettering.'),
    'mercedes-vito': ('Mercedes-Benz Vito', 'Medium van', 'Tell us the body length and whether you have a panel van or a crew model. Extra side glazing changes how much room is available for the design.'),
    'mercedes-citan': ('Mercedes-Benz Citan', 'Small van', 'A short brand name and one contact detail work well on the compact side panels. Share a photo of the rear doors to check what can fit around the handle and number plate.'),
})

BRANDS = {
    'ford': ('Ford', ('transit-custom', 'ford-transit', 'transit-connect')),
    'vauxhall': ('Vauxhall', ('vivaro', 'vauxhall-combo', 'vauxhall-movano')),
    'volkswagen': ('Volkswagen', ('caddy', 'vw-transporter', 'vw-crafter')),
    'citroen': ('Citroën', ('berlingo', 'citroen-dispatch', 'citroen-relay')),
    'peugeot': ('Peugeot', ('partner', 'peugeot-expert', 'peugeot-boxer')),
    'mercedes': ('Mercedes-Benz', ('sprinter', 'mercedes-vito', 'mercedes-citan')),
}

# Every van manufacturer shown in the brand grid (same list as Race Car Graphics). Images: logo tiles
# from the RCG brand set, or a van photo where no logo tile exists. BRANDS above holds model pages.
ISUZU_IMG = 'https://s3-eu-west-1.amazonaws.com/pitchprint.io/previews/5b1407e9a9b8172db628a8e529ca92ba_1.jpg'
LDV_IMG = 'https://s3-eu-west-1.amazonaws.com/pitchprint.io/previews/c46429a14f0629a2a633da4f630f4df1_1.jpg'
VAN_BRANDS = [
    ('aixam', 'Aixam'), ('citroen', 'Citroën'), ('dacia', 'Dacia'), ('daihatsu', 'Daihatsu'), ('dodge', 'Dodge'),
    ('fiat', 'Fiat'), ('ford', 'Ford'), ('holden', 'Holden'), ('hyundai', 'Hyundai'), ('isuzu', 'Isuzu'),
    ('iveco', 'Iveco'), ('kgm', 'KGM'), ('land-rover', 'Land Rover'), ('ldv', 'LDV'), ('levc', 'LEVC'),
    ('man', 'MAN'), ('maxus', 'Maxus'), ('mazda', 'Mazda'), ('mercedes', 'Mercedes-Benz'), ('mini', 'Mini'),
    ('mitsubishi', 'Mitsubishi'), ('modec', 'Modec'), ('nissan', 'Nissan'), ('peugeot', 'Peugeot'), ('renault', 'Renault'),
    ('ssangyong', 'SsangYong'), ('toyota', 'Toyota'), ('vauxhall', 'Vauxhall'), ('volkswagen', 'Volkswagen'),
]
BRAND_PHOTOS = {'aixam', 'holden', 'isuzu', 'iveco', 'kgm', 'land-rover', 'ldv', 'levc', 'man', 'maxus', 'modec'}


def brand_image(key):
    return {'isuzu': ISUZU_IMG, 'ldv': LDV_IMG}.get(key, f'/assets/brands/{key}.webp')


SECTORS = {
    'trades': ('Trades & home services', 'Use the side to say what you do and the rear for your number. A single service line is usually easier to read than a list of everything you offer. Flag ladder racks and existing accreditation marks.'),
    'delivery': ('Delivery & logistics', 'Make the brand recognisable from the back at a loading bay, and place fleet IDs where depot teams can find them. Tell us about doors, shutters and vehicle availability before we plan fitting.'),
    'construction': ('Construction & property', 'Crew vans, pickups and tippers need a layout that works across different body shapes. Share site visibility requirements and any existing safety markings when asking for a quote.'),
    'food-drink': ('Food & drink', 'Work the design around serving hatches, tail lifts and doors. Check that the name stays visible with the hatch open and leave prices or menus on a surface you can update separately.'),
    'events': ('Events & leisure', 'Put the campaign message where people will see it when the van or trailer is parked. Identify which artwork is seasonal and which elements need to stay on the vehicle.'),
    'automotive': ('Automotive & detailing', 'Use concise graphics on courtesy cars and service vans, with a separate treatment for the demonstrator. Let us know if a vehicle has a coating or existing film that could affect adhesion.'),
    'retail': ('Retail & local services', 'Carry the shopfront colours onto local delivery vehicles and keep one clear route to contact or order. Product photography can work well as a printed panel where there is enough space to read it.'),
}

SECTOR_CARDS = {
    'trades': ('service-copperline', 'Copperline Electrical work van', 'Legible signwriting for vans that work from one address to the next.'),
    'delivery': ('service-swiftloom', 'Matching Swiftloom courier vans', 'Consistent graphics for courier vans, delivery fleets and haulage vehicles.'),
    'construction': (8, 'Ridgeway construction vans and pickup', 'Branding that carries across site vans, pickups and crew vehicles.'),
    'food-drink': ('service-emberpeak', 'Emberpeak Coffee Luton with a printed coffee wrap', 'Printed wraps for food trucks, catering vans and drinks deliveries.'),
    'events': (37, 'EventWorks van and branded trailer', 'Standout graphics for promotional vehicles, trailers and mobile events.'),
    'automotive': ('hero', 'Orange and blue wrapped van on a circuit', 'Vehicle graphics for courtesy cars, service vans and demonstrators.'),
    'retail': ('service-petalmill', 'Petalmill florist van with a floral partial wrap', 'Carry shopfront branding onto delivery vans and mobile services.'),
}

TOWNS = {
    'norwich': ('Norwich', 'Our Norwich workshop is on Vulcan Road North at NR6 6AQ. If the vehicle does city-centre deliveries, leave a clear contact detail on the rear doors where customers can read it while the van is parked.'),
    'wymondham': ('Wymondham', 'If your vehicle runs between Wymondham and Norwich, tell us which days it is already off the road so the fitting appointment can work around your route.'),
    'dereham': ('Dereham', 'For a van used around Dereham and the surrounding villages, give us a short description of what customers should remember when they only see the vehicle briefly.'),
    'aylsham': ('Aylsham', 'If your work takes you between Aylsham and rural North Norfolk, send photos showing any racks, toolboxes or rear steps that may interrupt the layout.'),
    'north-walsham': ('North Walsham', 'If your vans cover North Walsham and the coast, tell us about their mileage and cleaning routine so we can discuss the appropriate film and care.'),
    'attleborough': ('Attleborough', 'If your vans run between Attleborough and Norwich, share vehicle availability in advance. We can discuss fitting around a changeover or planned downtime.'),
    'great-yarmouth': ('Great Yarmouth', 'For vehicles working around Great Yarmouth, tell us about coastal exposure, pressure washing and daily mileage when we discuss film and aftercare.'),
}

GUIDES = {
    'van-signwriting-brief': ('What to put on a work van', 'Start with who you are, what you do and how to contact you. A short trade line, a clear number or web address and strong contrast are the essentials.', 'Walk around the van in normal parking position and decide which sides get seen. Send photos with doors shut and with any ladders or racks fitted.'),
    'graphics-costs': ('What affects the cost of van graphics?', 'Panel count, vehicle size, artwork preparation, film type and fitting time are the main variables. Supply-only and fitted packages serve different needs.', 'For a comparable quote, ask which panels are covered, whether design time and removal are included, and whether the price includes VAT.'),
    'artwork-for-van-graphics': ('Preparing artwork for vehicle graphics', 'Send your vector logo, colour references and the exact wording. Where the design uses photography, send the original image at the largest available resolution.', 'Check the proof for phone numbers, spelling, spacing around panel joins and what appears on each side before approving.'),
    'partial-vs-full-wrap': ('Partial wrap vs full wrap', 'A partial wrap covers agreed panels and can make the original paint part of the design. A full wrap changes the appearance of most exterior body panels.', 'Look at both side and rear views before choosing. Confirm which trims, bumpers, roof sections and door shuts are included in the written quote.'),
    'wrap-vs-paint': ('Vehicle wrap vs paint', 'Wrap film changes the appearance of a sound surface and can carry printed branding. Paint is a bodywork finish and may be the better option where the underlying finish needs repair.', 'Show us chips, flaking or repaired areas before agreeing the work. Discuss removal and expectations if the vehicle is leased or likely to be sold.'),
    'wrap-aftercare': ('How to look after a vehicle wrap', 'Follow the care sheet for your exact film. Use a mild wash, keep abrasive tools away from the film and deal with bird droppings and road grime promptly.', 'If an edge lifts or a panel is damaged, take a photo and contact the fitter before attempting repairs or using a pressure washer near the area.'),
    'planning-fleet-graphics': ('Planning a fleet graphics rollout', 'List every vehicle, model year, body size, depot and availability. Group similar vehicles and decide which ones should go first.', 'Approve a master design and proofs for each body type. Keep a reference for approved colours, film choices, vehicle numbers and any later repairs.'),
    'lease-vehicle-graphics': ('Graphics on leased vehicles', 'Ask the lease provider what materials and coverage it allows and what it expects at return. Keep the agreement with the vehicle record.', 'Document the paint condition, check for previous repairs and book professional removal before handback. Ask the fitter to flag any areas that need extra care.'),
    'fleet-artwork-consistency': ('Keeping fleet graphics consistent', 'Agree a master set of colours, type sizes and logo positions. Allow for variation between a small car, a high-roof van and a box truck.', 'Review a proof for each body style and keep the approved layouts for new vehicles. Check printed colours against the original sample before ordering replacements.'),
}

CONTENT = {
    'van-signwriting-norwich': {
        'key': 'signwriting',
        'gallery': [
            ('service-pipecraft','Ford Transit Custom','Pipecraft plumbing signwriting'),
            (28,'Ford Transit Custom','Decorating van with a branded side panel'),
            ('service-voltlane','Vauxhall Vivaro','Voltlane electrical signwriting on a grey van'),
            ('service-keyforge','Volkswagen Caddy','Keyforge locksmith lettering'),
            (73,'Citroën Berlingo','Two-colour pest control graphics'),
            ('service-glassfinch','Peugeot Partner','Glassfinch window cleaning signwriting'),
            ('service-copperline','Ford Transit Custom','Copperline electrical signwriting'),
            (25,'Panel van concept','Side lettering for same-day deliveries'),
            (19,'Panel van concept','Property maintenance graphics'),
            (77,'Compact van concept','One-colour plumbing lettering'),
        ],
        'intro': [
            'Van signwriting gives people a quick way to recognise your business and know who to call. At our Norwich workshop, we design, produce and fit cut vinyl lettering and printed van graphics for tradespeople, local deliveries and service businesses across Norfolk. It works on everything from a compact service van with a logo and phone number to a long-wheelbase van with a larger design across both sides and the rear.',
            'Start with the details you want someone to read at a glance. Your business name, main service and one contact detail usually give the design a clear order. We lay the artwork out around handles, recesses and door joins, taking the original paint colour into account. If your logo needs several colours or contains a gradient, we can discuss printing it as a graphic instead of building it from separate colours of cut film.',
            'Send the make, model, year and photos of each side. We can advise on coverage, show you a proof and arrange fitting in Norwich after you approve the design.',
        ],
        'pricing': ['From £149', 'From £210', 'From £285 for large vans¹', 'Quote required'],
        'price_note': 'Local benchmark from Broadland Digital’s published fitted Basic packages. Confirm current prices with the Norwich Vehicle Graphics team. ¹The source groups large vans together. Confirm the price for your specific LWB vehicle and whether VAT is included.',
        'price_factor': 'Panel count, artwork preparation, printed colour, existing vinyl removal and access to the bodywork.',
        'materials': 'Cut lettering suits simple colours and shapes. Printed film can reproduce complex logos or gradients. Specify the finish against the body colour, including how it reads under overcast light.',
        'timing': ('Allow one or more working days for the proof and feedback.', 'A straightforward set can often be fitted in part of a day. Complex work or stripping old graphics takes longer.'),
        'guides': ['van-signwriting-brief','graphics-costs','artwork-for-van-graphics'],
        'case': ('Clear lettering for two trades', 'Copperline Electrical and Pipecraft Plumbing illustrate how a trade name can read at a glance on a work van.', 'Both layouts put a short trade line beneath the name and use high-contrast lettering over the original white paint.', ['service-copperline', 'service-pipecraft']),
        'reviews': [('Adam R', 'Praised the design work, finish and communication on their vehicle graphics.', 'Broadland Digital · vehicle graphics', 'https://broadland-digital-signs.localo.site/'),
                    ('Jack G', 'Reported good communication throughout and compliments on their new van signwriting.', 'Race Car Graphics · van signwriting', 'https://racecargraphics.uk/'),
                    ('Simon B', 'Highlighted a quick installation and a good-looking result on their van.', 'Race Car Graphics · van graphics', 'https://racecargraphics.uk/')],
        'faq': [
            ('What is the difference between cut vinyl and printed graphics?', 'Cut vinyl uses shapes and letters cut from a coloured film. Printed graphics can reproduce gradients, photos and more complex branding.'),
            ('Can I signwrite just the rear doors?', 'Yes. Tell us which panels you want covered. A rear-only design can focus on a phone number, website or short trade description.'),
            ('How should I prepare my van?', 'Tell us about wax, coatings, existing stickers and paint repairs before the fitting. Follow the workshop’s preparation instructions when confirming your slot.'),
            ('Can old lettering be removed first?', 'Send photos of the existing film and the paint around it. Removal and any adhesive cleanup can be priced separately after inspection.'),
            ('Can you add my logo to a coloured van?', 'Yes. We can check contrast against the actual body colour and advise on a suitable film or a backing panel if the logo needs it.'),
            ('Do you offer graphics for one van?', 'Yes. A single work van can be quoted and fitted in Norwich. Tell us which sides and doors you want to use.'),
            ('Will I see the design before fitting?', 'Yes. Review the layout on a proof and check your contact details, colours and artwork placement before approving it.'),
            ('Can signwriting be removed before a lease return?', 'Ask the lease provider first. Film can generally be removed professionally, with the result depending on the paint condition, film and its age.'),
        ],
    },
    'vehicle-wraps-norwich': {
        'key': 'wraps',
        'gallery': [
            ('service-tidelark','Panel van concept','Tidelark surf van with a full wave wrap'),
            (37,'Van and trailer concept','Coordinated event wrap'),
            (105,'Sports saloon concept','Satin colour-change wrap'),
            ('service-petalmill','Long van concept','Petalmill floral partial wrap'),
            ('service-barkmint','Ford Transit Custom','Barkmint mobile grooming partial wrap'),
            ('service-packwell','Box lorry concept','Packwell removals box wrap'),
            ('service-emberpeak','Luton box van','Emberpeak coffee wrap with printed imagery'),
            (42,'Compact van concept','Florist graphics with a printed floral panel'),
            (67,'Coffee van concept','Printed coverage around a serving hatch'),
            (7,'Electric panel van concept','Partial brewery livery wrap'),
        ],
        'intro': [
            'Vehicle wraps use specialist vinyl film to change the appearance of a car, van or commercial vehicle. From our Norwich workshop, we design and fit partial and full wraps for Norfolk businesses that want more room for their branding and for drivers planning a colour change. A partial wrap uses selected panels or a section of the body. A full wrap covers most exterior body panels, with trims and door shuts agreed in the quote.',
            'A printed wrap gives you room for photos, custom colours or a large illustration. A solid colour-change film is a different specification and is chosen for its colour and finish. We review the shape and condition of the bodywork before agreeing which film and coverage make sense. Send us photos of any stone chips, repairs or existing film so we can discuss preparation before booking.',
            'If the van is a working vehicle, tell us which days it can be off the road and what the graphics need to do. We’ll show the planned coverage on a proof and confirm what is included before fitting in Norwich.',
        ],
        'pricing': ['Quote required'] * 4,
        'price_note': 'Partial and full wraps are quoted individually. We confirm the panels, roof or bumper coverage, materials and VAT on your written quote.',
        'price_factor': 'Coverage, film and finish, body recesses, surface preparation, artwork, existing vinyl removal and fitting time.',
        'materials': 'Cast wrap film is suited to complex curves and recesses. Printed wraps typically use compatible print film and laminate. Ask about the life of the specific product on the roof, bonnet and vertical panels.',
        'timing': ('Allow several working days for the design and proof, subject to revisions.', 'Allow roughly one to two fitting days for many partial wraps and several days for a full wrap. Confirm the booking after inspection.'),
        'guides': ['partial-vs-full-wrap','wrap-vs-paint','wrap-aftercare'],
        'case': ('Full wraps that use the whole vehicle', 'Tidelark Surf Co. and Emberpeak Coffee illustrate how product imagery can help customers recognise a business from a distance.', 'The surf concept carries wave imagery around the bonnet and sides. The coffee concept uses the broad box panels for close-up photography.', ['service-tidelark', 'service-emberpeak']),
        'reviews': [('Andy', 'Praised the team’s advice on selecting a wrap and the service through to fitting.', 'Race Car Graphics · wrap fitting', 'https://racecargraphics.uk/'),
                    ('Maurice H', 'Highlighted the customer service and quality of their wrap.', 'Race Car Graphics · vehicle wrap', 'https://racecargraphics.uk/'),
                    ('Chris R', 'Described a quick, professional service on a trailer wrap.', 'Race Car Graphics · trailer wrap', 'https://racecargraphics.uk/')],
        'faq': [
            ('Can you wrap a van without doing the whole body?', 'Yes. A partial wrap can cover selected panels or a larger section of the vehicle. We confirm exactly what is covered on the proof and quote.'),
            ('Are door shuts and trims included in a full wrap?', 'Coverage varies. Door shuts, roof, bumpers, textured trims and badges are discussed before you approve the quote.'),
            ('What paint condition do you need for a wrap?', 'The film needs a sound, suitable surface. Send photos of flaking paint, rust, damage or repairs so we can inspect and advise.'),
            ('How long should I allow for a full wrap?', 'Plan for several fitting days as a guide. Vehicle size, film, prep and the number of panels affect the appointment length.'),
            ('Is wrap vinyl the same as paint protection film?', 'They are different products. Decorative vinyl changes appearance and adds a layer over covered paint. For stone-chip resistance, ask about paint protection film.'),
            ('Can I wrap a leased vehicle?', 'Ask your lease provider for written permission and check its handback requirements before booking. Discuss professional removal and any paint repairs with us.'),
            ('How long will a vehicle wrap last?', 'The life depends on the exact film, finish, panel angle, weather exposure, use and maintenance. Ask for the film specification and its applicable terms.'),
            ('How do I wash a wrapped vehicle?', 'Follow the care sheet for the fitted film. Use mild products and take extra care around edges and seams. Ask the fitter before using a pressure washer.'),
        ],
    },
    'fleet-graphics-norwich': {
        'key': 'fleet',
        'gallery': [
            ('service-juniper','Mixed car and van','Juniper Property Care fleet graphics'),
            (17,'Citroën Berlingo and cars','Cleaning fleet with a consistent design'),
            ('service-swiftloom','Electric panel vans','Swiftloom courier fleet graphics'),
            (64,'Luton box van and panel van','Removals vehicles in matching graphics'),
            ('service-kindred','Mixed cars','Kindred Path Care door branding'),
            ('service-loadbridge','Tractor units','Loadbridge haulage cab graphics'),
            ('service-oakspur','Pickup and crew van','Oakspur tree care fleet graphics'),
            (92,'Mixed car and van','Coordinated vans and company car concept'),
            (8,'Ford Transit and pickup','Construction company mixed fleet'),
            (98,'Mixed trade vans','Placement ideas across service vans'),
        ],
        'intro': [
            'Fleet graphics give vans, cars and commercial vehicles a recognisable identity across your business. Our Norwich team designs, produces and fits fleet graphics for companies running local service vehicles, delivery vans and mixed fleets across Norfolk. A rollout can start with a couple of vehicles or be spread over several fitting dates, depending on which vans need to stay on the road.',
            'We start with a list of makes, models, model years and body sizes, then plan how your colours, logo and contact details will carry across them. What works on the long side of a Luton needs a different layout on a car door. A master design gives the fleet a shared look while proofs for each vehicle type show how it fits around doors, windows, trims and equipment.',
            'Tell us which vehicles are being replaced first, where they are based and whether any already carry graphics. That helps us discuss removal, fitting batches and how new vehicles can match the approved artwork. If you run leased vehicles, include the handback requirements in the brief.',
        ],
        'pricing': ['Fleet quote required'] * 4,
        'price_note': 'Fleet work is quoted per rollout. For budgeting, use the fitted single-van signwriting guide as a reference and ask for a separate fleet quote.',
        'price_factor': 'Vehicle count, mix of body styles, coverage, old graphic removal, design adaptation and phased fitting.',
        'materials': 'Specify film, finish and colour across the master design. Keep an approved print sample and note which vehicles use a different film because of panel shape, use or removal requirements.',
        'timing': ('Allow several working days for the master design and proofs across vehicle types.', 'Agree fitting days by vehicle and batch. Different body types and removal work change how many can be fitted per day.'),
        'guides': ['planning-fleet-graphics','lease-vehicle-graphics','fleet-artwork-consistency'],
        'case': ('A consistent look across a fleet', 'Juniper Property Care uses a mix of body shapes, while Swiftloom illustrates a fleet of similar courier vans.', 'Each concept carries its own colour palette and logo across the vehicles, with artwork sized for the available panels.', ['service-juniper', 'service-swiftloom']),
        'reviews': [('Luke R', 'Praised the design service and quick responses on work for a van and a truck.', 'Race Car Graphics · van and truck', 'https://racecargraphics.uk/'),
                    ('Andrew S', 'Described professional work across three vans and several signs.', 'Race Car Graphics · multiple vans', 'https://racecargraphics.uk/'),
                    ('Daniel W', 'Highlighted attention to detail and on-time delivery across several personal, customer and motorsport vehicles.', 'Race Car Graphics · repeat vehicle work', 'https://racecargraphics.uk/')],
        'faq': [
            ('Can you start with a small fleet?', 'Yes. Give us the vehicle count and which ones need graphics first. The layout can be planned for future additions.'),
            ('Do all vehicles need to be the same model?', 'No. We adapt the approved design to each body style and agree the placement on separate proofs where needed.'),
            ('Can you fit in stages?', 'Tell us which vehicles are available and when. We can plan fitting dates around agreed batches at the Norwich workshop.'),
            ('Can you match film already on our fleet?', 'Send the existing artwork, film references and recent photos. Ageing and weathering can change colour, so we discuss how closely new work can match.'),
            ('What information do you need to price the fleet?', 'Send the vehicle count, makes, models, wheelbases or body sizes, photos and existing artwork. Mention removal work or special markings up front.'),
            ('Can individual fleet numbers be included?', 'Yes. Include the number list and preferred positions in the brief so we can plan a consistent layout and check each proof.'),
            ('How can I prepare for lease handback?', 'Check each vehicle’s terms and book removal in advance. Share the condition of the paint and any repairs so we can advise before fitting or removal.'),
            ('Can you replace graphics on one damaged panel?', 'Send a photo of the damage and the original artwork if you have it. We can assess whether a panel replacement or a larger section is needed for a consistent finish.'),
        ],
    },
}
