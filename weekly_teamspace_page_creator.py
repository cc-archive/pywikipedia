import import_from_dir
import wikipedia
import datetime
import urllib

def create_page(site, weekday_that_today_should_be=1):
    # This runs in the morning.
    today = datetime.date.today()
    assert (today.weekday() == weekday_that_today_should_be) # 1 is Tuesday
    tomorrow = today + datetime.timedelta(days=1)

    page_name = unicode(tomorrow.strftime('Staff_updates_%Y-%m-%d'))
    page_contents = unicode(today.strftime('Updates for the week ending %Y-%m-%d'))
    
    assert import_from_dir.get_page_contents(site, page_name) is None
    page = wikipedia.Page(site, page_name)

    # Note: This is deliciously racey, since MW has no sense of locking or atomic transactions.  Oh well.
    page.put(newtext=page_contents,
             comment = 'Created a staff updates page.',
             minorEdit = False)

    return page_name

def generate_email(page_name):
    msg = '''Dear CC Staff,

This week's staff updates are growing <%s>.

You should add yours <%s>.  Note that at the end of Tuesday,
that page will be automatically emailed to cc-staff - so act fast!

Yours truly,

CC Staff Call Bot.
'''

    add_yours = 'http://teamspace.creativecommons.org/index.php?' + \
        urllib.urlencode({'title': page_name, 'section': 'new', 'action': 'edit'})

    normal_url = 'http://teamspace.creativecommons.org/%s' % page_name

    return msg % (normal_url, add_yours)

def main():
    site = wikipedia.getSite()
    page_name = create_page(site, 0)
    print generate_email(page_name)
