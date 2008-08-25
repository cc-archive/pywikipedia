import import_from_dir
import wikipedia
import datetime
import urllib

PAGE_NAME_FORMAT='Staff_updates_%Y-%m-%d'

def create_page(site, weekday_that_today_should_be=1, dry_run = False):
    # This runs in the morning.
    wednesday = next_wednesday()

    page_name = unicode(wednesday.strftime(PAGE_NAME_FORMAT))
    page_contents = unicode(wednesday.strftime('Updates for the staff call on %Y-%m-%d'))
    
    assert import_from_dir.get_page_contents(site, page_name) is None
    page = wikipedia.Page(site, page_name)

    if dry_run:
        print 'Would have put this:'
        print page_contents
    else:
        # Note: This is deliciously racey, since MW has no sense of locking or atomic transactions.  Oh well.
        page.put(newtext=page_contents,
                 comment = 'Created a staff updates page.',
                 minorEdit = False)

    return page_name

def next_wednesday(today = datetime.date.today()):
        # This runs in the morning.
    today = datetime.date.today()
    # Spin until we see a Wednesday (day==2)
    wednesday = today
    while wednesday.weekday() != 2:
        wednesday += datetime.timedelta(days=1)
    return wednesday


def generate_email(page_name):
    msg = '''Dear CC Staff,

This week's staff updates are growing at <%s>.

You should add yours <%s>.  Note that at lunchtime Pacific this Tuesday,
that page will be automatically emailed to cc-staff - so act fast!

Yours truly,

CC Staff Call Bot.
'''

    add_yours = 'http://teamspace.creativecommons.org/index.php?' + \
        urllib.urlencode({'title': page_name, 'section': 'new', 'action': 'edit'})

    normal_url = 'http://teamspace.creativecommons.org/%s' % page_name

    return msg % (normal_url, add_yours)

def get_this_weeks_staff_call_page(site):
    # This runs in the morning.
    wednesday = next_wednesday()
    page_name = unicode(wednesday.strftime(PAGE_NAME_FORMAT))
    return import_from_dir.get_page_contents(site, page_name)

def main(argv):
    site = wikipedia.getSite()
    if argv[0] == 'ask_people_to_fill_in_page':
        page_name = create_page(site, 0, dry_run = True)
        body = generate_email(page_name)
        print body
    elif argv[0] == 'send_weekly_status_updates':
        body = get_this_weeks_staff_call_page(site)
        print body

if __name__ == '__main__':
    import sys
    main(sys.argv[1:])
