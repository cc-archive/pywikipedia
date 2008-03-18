'''This module will take a directory of files ending in .mw
and for each such file:
if a page of such name exists:
   Download that page, and store it as $pagename.mw.online
else:
   Create the page and insert the contents of $pagename.mw into it
   Create a local empty $pagename.mw.uploaded file to record the success'''

import glob
import wikipedia

def get_page_contents(site, pagename):
    assert type(pagename) == unicode
    page = wikipedia.Page(site, pagename)
    try:
        text = page.get(get_redirect = False)
        return text
    except wikipedia.NoPage:
        return None

def main():
    site =wikipedia.getSite()
    directory = raw_input("What directory holds the .mw files? > ")
    process_directory(site, directory)

def process_directory(site, directory):
    files = glob.glob("*.mw")
    for filename in files:
        pagename = filename[:-len('.mw')]
        unipagename = unicode(pagename, 'utf-8')
        page = wikipedia.Page(site, unipagename)
        existing_page_contents = get_page_contents(site, unipagename)
        if existing_page_contents is None:
            # Great!
            page.put(newtext=open(filename).read(),
                     comment='Imported file ' + unipagename + '.mw',
                     minorEdit=False)
            fd = open(pagename + '.uploaded', 'w')
            fd.close()
        else:
            fd = open(pagename + '.online', 'w')
            fd.write(existing_page_contents)
            fd.close()
            
if __name__ == '__main__':
    main()
