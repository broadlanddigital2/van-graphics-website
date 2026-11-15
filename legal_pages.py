"""Privacy policy and cookie policy for getitwrapt.co.uk."""
UPDATED = '15 November 2026'
CONTROLLER = 'Broadland Digital Ltd, trading as Wrapt'
ADDRESS = 'Consensus House, St Faiths Rd, Norwich NR6 7BW'

def _section(h, body):
    return f'<h2>{h}</h2>{body}'

def privacy_html(email, phone):
    s = [
        ('Who we are', f'<p>This website is run by {CONTROLLER} ("Wrapt", "we", "us"), {ADDRESS}. We are the data controller for personal information collected through getitwrapt.co.uk. Contact us about privacy at <a href="mailto:{email}">{email}</a> or on {phone}.</p>'),
        ('What we collect', '<ul><li><b>Enquiries and quote requests:</b> your name, email address, phone number, vehicle details, postcode and anything you write in the message.</li><li><b>Van Designer:</b> the logo, text, colours and vehicle you choose, and your contact details if you ask us to quote the design.</li><li><b>Chat assistant:</b> the messages you send, and your name, email and mobile if you choose to leave them.</li><li><b>Website use:</b> pages visited, device and browser type and how you reached the site, only if you allow analytics cookies.</li></ul>'),
        ('How we use it', '<ul><li>To reply to your enquiry and prepare a quote (steps you ask us to take before a contract).</li><li>To design, print and fit your graphics and manage your booking (contract).</li><li>To keep business and tax records (legal obligation).</li><li>To understand how the site is used and improve it, only with your consent.</li><li>To send occasional news or offers, only if you opt in. You can unsubscribe at any time.</li></ul>'),
        ('Who we share it with', '<p>We use trusted suppliers to run the site and our customer system: Cloudflare (website hosting), Supabase (our customer and enquiry database) and email and AI service providers that power notifications and the chat assistant. They process data only on our instructions. We may share details within the Broadland Digital group of businesses where it helps deliver your job. We never sell your data.</p>'),
        ('International transfers', '<p>Some suppliers may process data outside the UK. Where they do, we rely on UK adequacy regulations or the UK International Data Transfer Agreement or Addendum to protect it.</p>'),
        ('How long we keep it', '<p>Enquiries that do not go ahead are kept for up to 24 months. Customer and job records are kept for 6 years after the job for tax and legal reasons. Analytics data is kept for up to 14 months.</p>'),
        ('Your rights', '<p>You can ask to see, correct or delete your data, to restrict or object to how we use it, or to receive a copy in a portable format. Where we rely on consent, you can withdraw it at any time, including through <a href="#cookie-settings" data-cookie-settings>cookie settings</a>. Email us to make a request. If you are unhappy with how we handle your data you can complain to the Information Commissioner’s Office at <a href="https://ico.org.uk" target="_blank" rel="noopener">ico.org.uk</a>.</p>'),
        ('Cookies', '<p>See our <a href="/cookie-policy/">cookie policy</a> for the cookies and similar storage we use and how to control them.</p>'),
        ('Changes', f'<p>We may update this policy. The latest version will always be on this page. Last updated {UPDATED}.</p>'),
    ]
    return ''.join(_section(h, b) for h, b in s)

def cookie_html():
    rows = [
        ('wrapt-cookie-consent', 'Strictly necessary', 'Remembers your cookie choices.', '12 months', 'Local storage'),
        ('Van Designer drafts', 'Strictly necessary', 'Keeps your design while you work on it.', 'Until cleared', 'Local storage'),
        ('nvg_source', 'Analytics', 'Remembers how you found us (for example a Google search or ad) so we can attribute enquiries.', '90 days', 'Local storage'),
        ('Chat assistant', 'Functional', 'Keeps your chat conversation open as you move between pages.', 'Session', 'Local storage'),
        ('_ga, _ga_*', 'Analytics', 'Google Analytics: counts visits and shows how the site is used. Set only if analytics is turned on.', 'Up to 13 months', 'Cookie'),
    ]
    table = ''.join(f'<tr><td><code>{n}</code></td><td>{c}</td><td>{p}</td><td>{d}</td><td>{t}</td></tr>' for n, c, p, d, t in rows)
    return (f'<h2>What cookies are</h2><p>Cookies and similar technologies such as local storage are small files a website saves on your device. Some are needed for the site to work; others help us understand how it is used. We only use non-essential cookies if you agree.</p>'
            f'<h2>Your choices</h2><p>When you first visit we ask which cookies you are happy with. You can change your mind at any time: <button type="button" class="btn small" data-cookie-settings>Open cookie settings</button></p>'
            f'<h2>Cookies we use</h2><div class="legal-table"><table><thead><tr><th>Name</th><th>Type</th><th>Purpose</th><th>Lasts</th><th>Storage</th></tr></thead><tbody>{table}</tbody></table></div>'
            f'<h2>Controlling cookies in your browser</h2><p>You can also block or delete cookies in your browser settings. Blocking strictly necessary storage may stop parts of the site, such as the Van Designer, from working.</p>'
            f'<h2>More information</h2><p>See our <a href="/privacy-policy/">privacy policy</a> for how we handle personal data. Last updated {UPDATED}.</p>')
