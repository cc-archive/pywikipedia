import sys
import os
assert 'PYWIKIPEDIA_PATH' in os.environ
sys.path.append(os.environ['PYWIKIPEDIA_PATH'])

import wikipedia
import catlib
import pagegenerators
import re
import time

def for_category_member(category_name, function):
    site = wikipedia.getSite()
    cat = catlib.Category(site, category_name)
    gen = pagegenerators.CategorizedPageGenerator(cat)
    for page in gen:
        function(page)

def cd_fix_page(page):
    text = page.get(get_redirect = False)
    if '{{ContentDirectory' in text:
        assert text.count('{{') == 1
        print 'old', text
        print 'new', cd_fix_text(text)
        page.put(cd_fix_text(text), 'Asheesh bot: fixing ContentDirectories to use comma-separated formats')
        print 'Processed one page.'
        time.sleep(2)

def cd_fix_text(text):
    template, rest = text.split('}}', 1) # This assumes that we are the first
                                         # template in use on the page
    template += '}}' # put back what we took away...

    assert template.strip().startswith('{{ContentDirectory') # so this
                                                            # asserts it!

    lines = template.split('|')
    keep_lines = []
    formats = []
    for line in lines:
        if re.search('format\d=', line):
            this_format = line.split('=')[1].strip()
            this_format = this_format.replace('}}', '').strip()
            if this_format:
                formats.append(this_format)
        else:
            keep_lines.append(line)
    # Great!
    if formats: # if the list has any entries,
                # we actually have to insert a fresh 'format=' line
        print keep_lines
        keep_lines.insert(1, 'format=' + ','.join(formats))
        fixed_template = '|'.join(keep_lines)
        if '}}' not in fixed_template:
            fixed_template += '}}'
        return fixed_template + rest
    else:
        return text # Nothing to do

def update_contentdirectory_template():
    category_name = 'Content_Directory'
    for_category_member(category_name, cd_fix_page)
