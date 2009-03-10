import import_from_dir
import wikipedia
import datetime
import urllib
import smtplib
import email.Charset
import email.mime.text
import staff
import os

PAGE_NAME_FORMAT='Weekly_Staff_Call/%Y-%m-%d'

def new_page_contents(wednesday):
    # The easy static part up top.
    page_contents = unicode(wednesday.strftime('Updates for the staff call on %Y-%m-%d')) + '\n\n'

    # Interfacing with staff.py.
    assert os.path.exists('not-on-call')
    assert os.path.exists('phone-number-list')

    everyone = staff.list_all_staff(['Staff', 'Science Commons', 'Berlin Office', 'ccLearn'])
    randomized = staff.randomize_staff(everyone)
    formatted = staff.format_random_lists(randomized)
    page_contents += formatted
    return page_contents

def create_page(site, today = None, dry_run = False):
    # This runs on Monday morning.
    if today is None:
        today = datetime.date.today()
    wednesday = next_wednesday(today)

    page_name = unicode(wednesday.strftime(PAGE_NAME_FORMAT))
    
    assert import_from_dir.get_page_contents(site, page_name) is None
    page = wikipedia.Page(site, page_name)
    page_contents = new_page_contents(wednesday)

    if dry_run:
        print 'Would have put this:'
        print page_contents
    else:
        # Note: This is deliciously racey, since MW has no sense of locking or atomic transactions.  Oh well.
        page.put(newtext=page_contents,
                 comment = 'Created a staff updates page.',
                 minorEdit = False)

    return page_name

def next_wednesday(today):
    # This runs in the morning.
    # Spin until we see a Wednesday (day==2)
    wednesday = today
    while wednesday.weekday() != 2:
        wednesday += datetime.timedelta(days=1)
    return wednesday

def generate_email(page_name):
    msg = '''Dear CC Staff,

This week's staff updates are growing at <%s>.

You should add yours <%s>.
Note that at lunchtime Pacific this Tuesday, that page will be
automatically emailed to cc-staff - so act fast!

(That edit link takes you to an "add section" interface - just make a new section
with your name as the "Subject/headline", and fill in your updates as usual in the
main box.  Once you save, you can edit the page normally.)

Yours truly,

CC Staff Call Bot.
'''

    add_yours = 'http://teamspace.creativecommons.org/index.php?' + \
        urllib.urlencode({'title': page_name, 'section': 'new', 'action': 'edit'})

    normal_url = 'http://teamspace.creativecommons.org/%s' % page_name

    return msg % (normal_url, add_yours)

def get_this_weeks_staff_call_page(site):
    # This runs in the morning.
    wednesday = next_wednesday(datetime.date.today())
    page_name = unicode(wednesday.strftime(PAGE_NAME_FORMAT))
    return import_from_dir.get_page_contents(site, page_name)

def send_to_staff_list(subject, body, dry_run = False):
    # Create a UTF-8 quoted printable encoder
    charset = email.charset.Charset('utf-8')
    charset.header_encoding = email.charset.QP
    charset.body_encoding = email.charset.QP

    # Jam the data into msg, as binary utf-8
    msg = email.mime.text.MIMEText(body, 'plain')

    # Message class computes the wrong type from MIMEText constructor,
    # which does not take a Charset object as initializer. Reset the
    # encoding type to force a new, valid evaluation
    del msg['Content-Transfer-Encoding']
    msg.set_charset(charset) 
    print msg
    msg.set_param('format', 'flowed')

    msg.add_header('Subject', subject)
    
    SERVER='localhost'
    FROM='"Mr. Staff Call" <asheesh@creativecommons.org>'
    if dry_run:
        TO = ['asheesh@creativecommons.org']
    else:
        TO = ['cc-staff@lists.ibiblio.org']

    msg.add_header('To', TO[0])

    s = smtplib.SMTP()
    s.connect(SERVER)
    s.sendmail(FROM, TO, msg.as_string())
    s.close()
    

def main(argv):
    site = wikipedia.getSite()
    today = datetime.date.today()
    this_week_wednesday = next_wednesday(today)
    if argv[0] == 'ask_people_to_fill_in_page':
        # This creates the page for the Wednesday ca. 9d in the future
        next_week = today + datetime.timedelta(days=7)
        create_page(site, today=next_week) # Create next week's page.

        # Last week, Jen or Ani could have gone and deleted this week's page.
        # For now, we assume there is no way to cancel a staff call. FIXME.
        this_week_page_name = unicode(this_week_wednesday.strftime(PAGE_NAME_FORMAT))

        body = generate_email(this_week_page_name)
        send_to_staff_list(subject=this_week_wednesday.strftime('Fill in your updates for staff call on Wed %Y-%m-%d'),
                           body=body)
    elif argv[0] == 'send_weekly_status_updates':
        body = get_this_weeks_staff_call_page(site)
        send_to_staff_list(subject=this_week_wednesday.strftime("Staff updates for call on Wed %Y-%m-%d"),
                           body=body)

if __name__ == '__main__':
    import sys
    main(sys.argv[1:])
