"""Sector "ideas" gallery: three concepts per sector.
Each entry: (vehicle, coverage, fictional brand, colours, design notes, setting, caption).
Images go in dist/assets/sectors/gallery/{filename(caption)}.webp and swap in automatically."""
import re

def filename(caption):
    return "norwich-vehicle-graphics-" + re.sub(r"[^a-z0-9]+", "-", caption.lower().replace("&", "and")).strip("-")


G = {
'trades': [
    ('Ford Transit Custom, white', 'Signwriting', 'Hartwell Building Services', 'Navy and safety yellow', 'Bold name across the side, a three-trade service line (building, extensions, repairs), phone and website on the rear doors.', 'Parked on a new-build drive with a skip behind', 'Cut-vinyl signwriting for a general builder'),
    ('Volkswagen Transporter, dark grey', 'Partial wrap', 'Keel & Co Property Maintenance', 'Charcoal van, orange and white graphics', 'Angled orange panel sweeping from the rear wheel arch, white logo, icons for plumbing, carpentry and decorating.', 'Residential street, morning light', 'Partial wrap with trade icons'),
    ('Renault Trafic LWB, white', 'Signwriting', 'Brightline Decorators', 'White, teal and soft grey', 'Large paint-roller stripe motif along the lower side, clean wordmark, "Interior & exterior" strapline.', 'Outside a Victorian terrace with scaffold-free frontage', 'Decorator van with a paint-stroke stripe'),
],
'plumbers-heating': [
    ('Ford Transit Custom, white', 'Signwriting', 'Wensum Plumbing & Heating', 'Royal blue and white', 'Name on the upper side, "Boilers · Bathrooms · Repairs" service line, blank accreditation badge space, phone large on rear.', 'Suburban driveway', 'Plumbing van with a clear service line'),
    ('Vauxhall Vivaro, silver', 'Partial wrap', 'Flowright Heating', 'Silver van, red-to-orange gradient flame and blue water swoosh', 'Dual swoosh across the rear half showing heat and water, logo on the front door.', 'Industrial estate car park', 'Heating engineer partial wrap with flame and water swoosh'),
    ('Citroën Berlingo, white', 'Signwriting', 'Drip Stop Emergency Plumber', 'White, bright red and black', '"24/7 emergency" banner along the top, giant phone number on the side and rear, simple tap icon.', 'Night-time street under a streetlamp', 'Emergency plumber van built around the phone number'),
],
'electricians': [
    ('Ford Transit Connect, white', 'Signwriting', 'Kestrel Electrical', 'White, electric yellow and black', 'Lightning-bolt underline beneath the name, "Domestic · Commercial · EV chargers", blank accreditation badge space.', 'Outside a modern semi with a wall charger', 'Electrician van with a lightning underline'),
    ('Volkswagen Transporter, black', 'Partial wrap', 'Volt & Wire', 'Black van, neon green circuit lines', 'Circuit-board traces running from the rear lights forward, green logo, website across the back.', 'Urban street at dusk', 'Circuit-board partial wrap for an electrical contractor'),
    ('Renault Kangoo E-Tech, white', 'Full wrap', 'Greenspark EV Installs', 'Deep green with white', 'Plug-and-cable graphic wrapping around the van, "EV charger installation" headline.', 'Car park next to an EV charging bay', 'Full wrap for an EV charger installer'),
],
'roofers': [
    ('Ford Ranger double cab, white', 'Signwriting', 'Ridgeway Roofing', 'White, slate grey and red', 'Roofline outline above the name on the doors, services on the tailgate, ladder-rack friendly placement.', 'Outside a house with scaffold and new tiles', 'Pickup signwriting for a roofing firm'),
    ('Ford Transit LWB, white', 'Partial wrap', 'Norfolk Flat Roofs', 'White van, charcoal and orange', 'Large angled charcoal block with orange edge, "GRP · EPDM · Felt" list, placed below the roof rack line.', 'Builders\' merchant yard', 'Flat roofing partial wrap below the racks'),
    ('Iveco Daily dropside, white', 'Signwriting', 'Pantile Roofing Co', 'Terracotta and cream', 'Cab doors and headboard lettering, pantile pattern strip along the dropside boards.', 'Rural lane with a barn conversion', 'Dropside graphics with a pantile pattern'),
],
'scaffolders': [
    ('Isuzu dropside lorry, white cab', 'Cab and headboard graphics', 'Upright Scaffolding', 'White, high-vis yellow and black', 'Huge name on the headboard, phone on cab doors, yellow-black chevron strip on the rear.', 'Scaffold yard with tubes stacked', 'Scaffolding lorry headboard graphics'),
    ('Ford Transit dropside, white', 'Signwriting', 'Brace Access Ltd', 'Royal blue and white', 'Bold lettering across the cab, blank accreditation badge spaces, boards lettered with the website.', 'City-centre site entrance', 'Dropside signwriting for an access company'),
    ('Toyota Hilux, grey', 'Partial wrap', 'Tubeline Scaffold', 'Grey truck, yellow tube pattern', 'Diagonal scaffold tube-and-clip pattern on the rear doors and bed sides.', 'Muddy site access road', 'Pickup partial wrap with a scaffold tube pattern'),
],
'landscapers-gardeners': [
    ('Ford Transit Custom, white', 'Partial wrap', 'Fernbrook Landscapes', 'White van, leaf greens', 'Overlapping leaf shapes sweeping from the rear, logo mid-panel, "Design · Build · Maintain".', 'Large garden with fresh turf', 'Landscaper partial wrap with a leaf motif'),
    ('Isuzu D-Max with trailer, white', 'Signwriting', 'Oakleaf Tree Care', 'Forest green and white', 'Tree silhouette logo on doors, matching trailer side panels with phone number.', 'Country lane, autumn trees', 'Tree surgeon pickup and trailer graphics'),
    ('Renault Master tipper, white', 'Signwriting', 'Greenway Garden Maintenance', 'Lime green and charcoal', 'Mower-stripe pattern along the lower cab, name on doors, tipper sides lettered.', 'Business park grounds', 'Garden maintenance tipper with mowing stripes'),
],
'carpenters-joiners': [
    ('Volkswagen Crafter, white', 'Signwriting', 'Grainline Joinery', 'Walnut brown and cream', 'Wood-grain band along the lower side, elegant serif wordmark, "Kitchens · Staircases · Bespoke".', 'Outside a period home', 'Joinery van with a wood-grain band'),
    ('Ford Transit Custom, dark blue', 'Partial wrap', 'Dovetail Kitchens', 'Navy van, copper accents', 'Copper dovetail-joint graphic on the rear quarter, minimal logo, website on rear.', 'Showroom forecourt', 'Kitchen fitter partial wrap with copper detail'),
    ('Citroën Relay, white', 'Signwriting', 'Mill Lane Carpentry', 'Forest green and white', 'Simple saw-tooth line under the name, list of services, phone on bonnet edge.', 'Village street', 'Carpenter van with simple saw-tooth detail'),
],
'cleaning': [
    ('Toyota Aygo X, white', 'Signwriting', 'Sparkle Lane Cleaning', 'White, teal and aqua', 'Bubble cluster on the rear door, name across both doors, phone on rear window.', 'Residential cul-de-sac', 'Small car graphics for a domestic cleaner'),
    ('Peugeot Partner, white', 'Partial wrap', 'ProClean Commercial', 'White van, deep blue and lime', 'Diagonal blue sweep with lime edge, "Offices · Schools · End of tenancy".', 'Office park car park', 'Commercial cleaning van partial wrap'),
    ('Fleet of two Fiat 500s, white', 'Fleet graphics', 'Fresh & Co Cleaners', 'White with soft pink and grey', 'Matching layout across both cars, numbered fleet ID on rear.', 'Side by side outside a small office', 'Matching small-car fleet graphics'),
],
'window-cleaners': [
    ('Ford Transit Connect, white, water-fed pole system visible', 'Signwriting', 'Clearview Window Cleaning', 'White, sky blue and navy', 'Name above the window line, squeegee-swipe graphic, services kept clear of the rear doors.', 'Residential street, bright day', 'Window cleaner van with a squeegee swipe'),
    ('Renault Kangoo, white', 'Partial wrap', 'Gleam Exterior Cleaning', 'White van, blue water splash', 'Water splash wrapping the rear corner, "Windows · Gutters · Fascias".', 'Bungalow with clean conservatory', 'Exterior cleaning partial wrap with water splash'),
    ('Toyota Hilux with water tank, silver', 'Signwriting', 'Pure Pole Window Care', 'Silver truck, white and blue', 'Door lettering, tank wrap band with phone number.', 'Commercial building frontage', 'Water-fed pole pickup and tank band'),
],
'pest-control': [
    ('Vauxhall Combo, white', 'Signwriting', 'Shieldguard Pest Solutions', 'Dark green and silver', 'Shield badge logo, discreet layout on the doors only, phone on rear.', 'Restaurant service yard', 'Discreet pest control signwriting'),
    ('Ford Transit Custom, white', 'Partial wrap', 'Burrow & Wing Pest Control', 'White van, charcoal and amber', 'Abstract hexagon pattern from the rear quarter, no pests pictured, "Commercial contracts".', 'Industrial unit', 'Pest control partial wrap with abstract pattern'),
    ('Nissan Townstar, white', 'Signwriting', 'Hedgerow Wildlife & Pest', 'Earthy green and cream', 'Leaf-and-shield badge, "Humane wildlife solutions" line.', 'Countryside farmhouse', 'Wildlife control van signwriting'),
],
'dog-groomers': [
    ('Mercedes Sprinter conversion, white', 'Full wrap', 'Pawfect Mobile Grooming', 'Lavender, white and pastel yellow', 'Playful paw-print trail, cartoon-style (original) dog silhouette, bubbles, "We come to you".', 'Driveway with a happy owner and dog nearby', 'Playful full wrap for a mobile dog groomer'),
    ('Citroën Berlingo, white', 'Partial wrap', 'Scruffs to Fluffs', 'White van, coral and teal', 'Coral wave panel with paw prints, phone large on rear door.', 'Village green', 'Dog groomer partial wrap with paw prints'),
    ('Fiat Ducato, grey', 'Signwriting', 'The Groom Room Norwich', 'Grey van, white and mint lettering', 'Elegant script name, scissors-and-comb icon, booking website.', 'Smart town street', 'Refined signwriting for a grooming salon van'),
],
'mobile-mechanics': [
    ('Ford Transit Custom, black', 'Partial wrap', 'Torque Mobile Mechanics', 'Black van, red and silver', 'Spanner-and-piston graphic on the rear quarter, red racing stripe, "Servicing at your door".', 'Customer driveway with a car bonnet open', 'Mobile mechanic partial wrap'),
    ('Volkswagen Caddy, white', 'Signwriting', 'Fix-It Tyres Mobile', 'White, yellow and black', 'Tyre tread pattern band along the sills, huge phone number, "24hr mobile tyre fitting".', 'Supermarket car park', 'Mobile tyre fitting van with tread band'),
    ('Iveco Daily recovery truck, white', 'Signwriting', 'Swift Recovery Norfolk', 'White, high-vis orange and blue', 'Chevrons on the rear, bold name on cab, phone on bed sides.', 'Roadside lay-by, safe position', 'Recovery truck graphics with rear chevrons'),
],
'mobile-bars': [
    ('Converted vintage horsebox trailer, cream', 'Full wrap', 'The Bubbly Box', 'Cream, dusty pink and gold', 'Art-deco gold frame around the hatch, script name, "Prosecco & cocktails" above the serving window.', 'Wedding marquee lawn with festoon lights', 'Horsebox prosecco bar with gold art-deco detail'),
    ('Piaggio Ape three-wheeler, white', 'Full wrap', 'Little Tap Co', 'Teal and copper', 'Copper tap icon, wood-panel effect, chalkboard-style menu panel.', 'Outdoor festival, golden hour', 'Mini three-wheeler bar wrap'),
    ('Citroën H van replica, grey', 'Partial wrap', 'Gin & Juniper Mobile Bar', 'Grey van, botanical green illustrations', 'Hand-drawn juniper and citrus illustrations around the hatch, script logo.', 'Garden party at a country house', 'Mobile gin bar with botanical illustrations'),
],
'food-drink': [
    ('Converted food truck (Ford Transit base), black', 'Full wrap', 'Smoke & Ember Street Kitchen', 'Matte black, flame orange and copper', 'Flames rising from the lower body, big wordmark beside the serving hatch, menu board panel.', 'Street food market at dusk with festoon lights', 'Printed full wrap for a street food truck'),
    ('Piaggio Ape coffee conversion, white', 'Full wrap', 'Little Roast Coffee', 'Cream and espresso brown', 'Coffee bean pattern, steaming cup logo, hatch framed with menu.', 'Park path, morning', 'Coffee van wrap with bean pattern'),
    ('Catering trailer, white', 'Partial wrap', 'Nonna\'s Wood-Fired Pizza', 'White, Italian green and red', 'Tricolore sweep along the base, script name, wood-fired oven illustration.', 'Village fete field', 'Pizza trailer partial wrap'),
],
'events': [
    ('Luton box van, white', 'Full wrap', 'Big Top Marquee Hire', 'Navy with white and gold', 'Photographic marquee scene across the box, name and phone on the cab.', 'Showground with marquees going up', 'Box-body wrap for marquee hire'),
    ('Ford Transit Custom, white', 'Partial wrap', 'Echo Sound & Light', 'White van, purple and cyan stage beams', 'Stage-light beams fanning from the rear, logo in the beam.', 'Venue loading dock at night', 'Event production van with light beam graphics'),
    ('Exhibition trailer, white', 'Full wrap', 'Roadshow Live', 'Bright yellow and black', 'Large campaign headline panels, QR code area, swap-ready panel layout.', 'Town square promotion', 'Roadshow trailer with campaign panels'),
],
'care-healthcare': [
    ('Toyota Yaris hybrid, white', 'Signwriting', 'Kindred Home Care', 'Soft teal and white', 'Heart-and-house logo on doors, "Care in your own home", phone on rear.', 'Quiet residential street', 'Small car graphics for a home care company'),
    ('Fleet of three Kia Picantos, white', 'Fleet graphics', 'Broadland Community Carers', 'White with purple and lilac', 'Identical layouts, fleet numbers, discreet but recognisable.', 'Lined up outside a care office', 'Matching care company fleet'),
    ('Peugeot e-Expert, white', 'Partial wrap', 'Riverside Community Health', 'White van, calm clinical blue', 'Calm blue wave, clinic name, "Mobile health clinic".', 'Village hall car park', 'Community health van partial wrap'),
],
'charities': [
    ('Ford Transit minibus, white', 'Partial wrap', 'Norfolk Friends Community Transport', 'White, sunshine yellow and blue', 'Wave with smiling people silhouettes (simple shapes), "Community transport", sponsor strip.', 'Outside a community centre', 'Community minibus with sponsor strip'),
    ('Renault Trafic, white', 'Signwriting', 'Harbour Food Bank', 'Green and orange', 'Name, "Donations welcome" with website, sponsor logos panel (blank placeholders).', 'Supermarket collection point', 'Charity van with sponsor panels'),
    ('Citroën Relay, white', 'Full wrap', 'Wild Coast Conservation Trust', 'Ocean blue with seal and wave illustration', 'Illustrated coastline scene, campaign message, donate QR area.', 'Coastal car park near dunes', 'Conservation charity full wrap'),
],
'delivery': [
    ('Ford Transit LWB high roof, white', 'Partial wrap', 'Swiftline Couriers', 'White van, electric blue speed lines', 'Speed lines along the side, logo at the front, "Same-day delivery" headline.', 'Business park delivery bay', 'Courier van with speed lines'),
    ('Fleet of three Vauxhall Vivaros, white', 'Fleet graphics', 'Parcelpoint Logistics', 'White with orange and dark grey', 'Shared layout across three vans, fleet numbers on the rear and roof.', 'Depot yard lined up', 'Logistics fleet livery'),
    ('DAF LF rigid truck, white', 'Cab graphics and curtain-side', 'Eastern Counties Haulage', 'Deep red and white', 'Cab doors and roof spoiler lettering, curtain-side with big name.', 'A47 lay-by', 'Haulage truck cab and curtain graphics'),
],
'removals': [
    ('Luton box van, white', 'Full wrap', 'Homeward Removals', 'Teal and white', 'Photographic packed boxes and sofa scene across the box, "Local & national moves".', 'Terraced street during a move', 'Luton removals van full wrap'),
    ('Mercedes Sprinter, white', 'Signwriting', 'Two Hands Man & Van', 'White, orange and charcoal', 'Name, "Man & van · House clearances", phone huge on rear.', 'Student flat entrance', 'Man-and-van signwriting'),
    ('Box van fleet of two, white', 'Fleet graphics', 'Stowaway Norfolk Storage', 'Navy and yellow', 'Matching box sides with stacked-box icon, storage unit address.', 'Self-storage site', 'Storage company box van fleet'),
],
'fleets-corporate': [
    ('Fleet of four Ford Transit Customs, white', 'Fleet graphics', 'Anglian Utilities Services', 'White with green and navy', 'Consistent layout, fleet numbers, rear high-vis chevrons.', 'Depot yard, aerial three-quarter view', 'Corporate van fleet livery'),
    ('Two Skoda Octavia estates, grey', 'Signwriting', 'Northgate Surveyors', 'Grey cars with white and gold lettering', 'Subtle door lettering and website on the rear.', 'Office car park', 'Subtle company car graphics'),
    ('Volkswagen ID. Buzz Cargo, white', 'Full wrap', 'Brightwave Energy', 'Gradient blue to green', 'Clean gradient wrap with logo and "Powering Norfolk".', 'Modern office plaza', 'Electric van full brand wrap'),
],
'highways-chapter-8': [
    ('Ford Transit Custom, white, roof beacons', 'Signwriting plus rear chevrons', 'Highway Safe Services', 'White, red and yellow chevrons', 'Chapter 8-style red/yellow rear chevron kit, side contour markings, name on doors.', 'Roadworks coned off on an A-road', 'Rear chevron kit on a highways van'),
    ('Isuzu tipper, white', 'Chevrons and side markings', 'Roadline Maintenance', 'White, high-vis orange', 'Full rear chevron board, reflective side stripe, cab lettering.', 'Depot yard', 'Highways tipper with chevrons and side stripe'),
    ('Toyota Land Cruiser Commercial, white', 'Battenburg-style side markings (non-emergency colours)', 'Traffic Control Norfolk', 'Yellow and blue (non-emergency)', 'Side block pattern, rear chevrons, roof lightbar visible.', 'Motorway hard-standing, safe position', 'Traffic management vehicle markings'),
],
'construction': [
    ('Ford Ranger double cab, white', 'Signwriting', 'Stonegate Construction', 'Charcoal and safety orange', 'Bold name on doors, website on tailgate, fleet number.', 'Large building site with cranes', 'Construction pickup signwriting'),
    ('Volvo tipper truck, white', 'Cab graphics', 'Groundworx Civils', 'White cab, yellow and black', 'Cab door and visor lettering, rear chevrons.', 'Groundworks site with excavator', 'Groundworks tipper cab graphics'),
    ('Vauxhall Movano crew van, white', 'Partial wrap', 'Keystone Developments', 'White van, navy and gold', 'Architectural line drawing of houses across the rear half, "Building quality homes".', 'Show home development', 'Developer van with architectural line drawing'),
],
'agriculture': [
    ('Toyota Hilux, white', 'Signwriting', 'Wensum Valley Farms', 'Barley gold and deep green', 'Wheat-ear logo on doors, estate name on tailgate.', 'Farm track beside a barley field', 'Farm pickup signwriting'),
    ('Agricultural contractor tractor and trailer, green', 'Trailer graphics', 'Marsh Lane Contracting', 'White and gold on green', 'Large trailer side lettering with phone number.', 'Harvest field at sunset', 'Contractor trailer graphics'),
    ('Land Rover Defender Hard Top, grey', 'Partial wrap', 'Saltmarsh Estate', 'Grey with heritage green', 'Heritage crest on doors, estate pinstripe.', 'Estate gateway with parkland', 'Estate vehicle heritage graphics'),
],
'marine-boatyards': [
    ('Ford Transit Custom, white', 'Partial wrap', 'Broadwater Marine Engineering', 'White van, navy and sea blue waves', 'Wave panel along the lower side, anchor logo, "Engines · Rigging · Repairs".', 'Boatyard on the Broads with moored cruisers', 'Marine engineer van with wave panel'),
    ('Mitsubishi L200 with boat trailer, white', 'Signwriting', 'Reedham Boat Hire', 'Navy and white', 'Name on doors and matching trailer mudguard panels.', 'Slipway at a river', 'Boat hire pickup and trailer graphics'),
    ('Citroën Berlingo, white', 'Signwriting', 'Saltmarsh Sailmakers', 'Red and navy nautical', 'Sail icon, rope-line divider under the name.', 'Harbour quayside', 'Sailmaker van with nautical rope detail'),
],
'retail': [
    ('Citroën e-Berlingo, white', 'Partial wrap', 'Petal & Stem Florist', 'White van, blush pink and sage floral illustration', 'Flower bouquet illustration on rear quarter, script name.', 'High street outside a florist shop', 'Florist van with floral illustration'),
    ('Ford Transit Connect, dark green', 'Signwriting', 'Larder & Loaf Deli', 'Green van, cream lettering', 'Traditional shopfront-style lettering with a gold keyline.', 'Market town square', 'Deli van with shopfront-style lettering'),
    ('Renault Trafic, white', 'Full wrap', 'Hearth & Home Furnishings', 'Warm grey with lifestyle photo', 'Photographic living room scene, "Free local delivery".', 'Retail park', 'Furniture store delivery van wrap'),
],
'tourism-holiday-lets': [
    ('Volkswagen Caddy, white', 'Signwriting', 'Coastline Cottages', 'Sea blue and sand', 'Beach hut row graphic along the sill, booking website.', 'Seaside village street', 'Holiday cottage changeover van'),
    ('Ford Transit minibus, white', 'Full wrap', 'Broads Explorer Tours', 'Green and sky blue scenic', 'Photographic windmill and river scene, "Guided tours".', 'Outside a windmill', 'Tour minibus scenic full wrap'),
    ('Fiat Doblo, white', 'Partial wrap', 'Sandpiper Housekeeping', 'White van, teal and coral', 'Sandpiper bird silhouette, "Holiday let cleaning & linen".', 'Holiday let courtyard', 'Holiday let cleaning van partial wrap'),
],
'automotive': [
    ('Volkswagen Transporter, black', 'Partial wrap', 'Mirror Finish Detailing', 'Gloss black, silver and red', 'Reflection-style silver swoosh, "Ceramic coating · Valeting".', 'Car dealership forecourt', 'Detailing van partial wrap'),
    ('Fleet of courtesy cars (two Ford Fiestas), white', 'Fleet graphics', 'Kingsway Motors', 'White with dark blue and red', 'Dealer name, "Courtesy car" on rear, website.', 'Garage forecourt', 'Courtesy car fleet graphics'),
    ('Ford Transit Custom, grey', 'Signwriting', 'Precision Auto Repairs', 'Grey van, orange lettering', 'Gear-and-wrench icon, MOT and servicing list, phone on rear.', 'Workshop yard with lifts visible', 'Garage van signwriting'),
],
}
