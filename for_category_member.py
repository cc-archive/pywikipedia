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
        new = my_regex_sub(r'{{ContentDirectory.*?}}', text, cd_fix_text)
        if text != new:
            print 'old', text
            print 'new', new
            page.put(new, 'Asheesh bot: fixing ContentDirectories to use comma-separated formats')
            print 'Processed one page.'
            time.sleep(2)

def my_regex_sub(regex, instring, function):
    compiled = re.compile(regex, re.DOTALL)
    match = compiled.search(instring)
    if match is None:
        return instring
    
    # So we have a match!
    before = instring[:match.start()]
    exciting = instring[match.start():match.end()]
    after = instring[match.end():]

    # So let's fix up the "exciting" part...
    new_exciting = function(exciting)
    if exciting != new_exciting:
        print "Fixed one."
    return before + new_exciting + after

def cd_fix_text(template):
    assert '{{ContentDirectory' in template # so this
    assert template.count('{{') == 1        # asserts it

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
        if not fixed_template.endswith('}}'):
            assert '}}' not in fixed_template
            fixed_template += '}}'
        return fixed_template
    else:
        return template # Nothing to do

def update_contentdirectory_template():
    category_name = 'Content_Directory'
    for_category_member(category_name, cd_fix_page)
