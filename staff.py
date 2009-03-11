from lxml import etree
import urllib2
from lxml.cssselect import CSSSelector
import random

def list_all_staff(headings = ('Staff',)):
    document_fd = urllib2.urlopen('http://creativecommons.org/about/people')
    parser = etree.HTMLParser()
    document = etree.parse(document_fd, parser)
    tree = document.getroot()
    sel = CSSSelector('.people')
    people_lists = sel(tree)
    result = []

    for people_list in people_lists:
        heading_selected = people_list.getprevious()
        heading_text = heading_selected.text or heading_selected.findtext('*')
        assert heading_text
        if heading_text in headings:
            result.extend([thing.text or thing.findtext('*') for thing in people_list])

    assert 'Mike Linksvayer' in result
    return result

def randomize_staff(everyone, n_groups=4, not_on_call_list = None):
    # FIXME: Handle the people who aren't allowed to be note takers
    if not_on_call_list is None:   
        not_on_call_list = [dude.strip() for dude in open('not-on-call')]

    just_call_people = [k for k in everyone if k not in not_on_call_list]
    groups = [ [] for k in range(n_groups) ]
    random.shuffle(just_call_people)
    for i, person in enumerate(just_call_people):
        groups[i%n_groups].append(person)

    return groups

def format_random_lists(random_lists, phone_number_list = None):
    if phone_number_list is None:
        phone_number_list = [number.strip() for number in open('phone-number-list')]

    out_lines = []
    for i, l in enumerate(random_lists):
        note_taker = l[0]
        out_lines.append('= Group %d =' % (i + 1))
        out_lines.append(unicode(phone_number_list[i]))

        for person in sorted(l):
            if person == note_taker:
                person += ' (note-taker)'
            out_lines.append('* ' + person)
        out_lines.append('[[/Group %d notes]]' % (i + 1))

    return '\n'.join(out_lines)

