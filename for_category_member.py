import wikipedia
import catlib
import pagegenerators
import re

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
        page.put(cd_fix_text(text), 'Asheesh bot: fixing ContentDirectories to use comma-separated formats')
        print 'Processed one page.'

def cd_fix_text(text):
    template, rest = text.split('}}') # This asserts that there is only one
                                      # template in use on the page
    template += '}}' # put back what we took away...

    lines = template.split('|')
    keep_lines = []
    formats = []
    for line in lines:
        if re.search('format\d=', line):
            this_format = line.split('=')[1].strip()
            if this_format:
                formats.append(this_format)
        else:
            keep_lines.append(line)
    # Great!
    if formats: # if the list has any entries,
                # we actually have to insert a fresh 'format=' line
        keep_lines.insert(-1, '\n  format=' + ','.join(formats))
        fixed_template = '|'.join(keep_lines)
        return fixed_template
    else:
        return text # Nothing to do

def update_contentdirectory_template():
    category_name = 'Content_Directory'
    for_category_member(category_name, cd_fix_page)
