"""Monkey Patching and Bananas for running pywikipedia bots from CC svn."""

import os
import sys

import bot_monkey
    
# make sure we can import wikipedia
pywikipedia_path = None

if 'PYWIKIPEDIA_PATH' in os.environ:
    pywikipedia_path = os.environ['PYWIKIPEDIA_PATH']
else:
    # no environment variable set; see if we can figure out what to use
    pywikipedia_path = os.path.abspath( os.path.join(
            os.path.dirname(bot_monkey.__file__), '..', 'pywikipedia'
            ))

    if not os.path.exists(pywikipedia_path):
        pywikipedia_path = None

assert pywikipedia_path is not None
sys.path.append(pywikipedia_path)

# make sure the families are accessible
family_path = os.path.abspath(os.path.join(pywikipedia_path,'..','families'))
for fam_file in os.listdir(family_path):

    if fam_file[-3:] != '.py':
        continue

    if not os.path.exists(os.path.join(pywikipedia_path, 'families', fam_file)):

        os.symlink(os.path.join(family_path, fam_file),
                   os.path.join(pywikipedia_path, 'families', fam_file))

