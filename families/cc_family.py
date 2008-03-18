# -*- coding: utf-8  -*-

import family

# The official Mozilla Wiki. #Put a short project description here.

class Family(family.Family):
    def __init__(self):
        family.Family.__init__(self)
        self.name = 'cc' #Set the family name; this should be the same as in the filename.
        self.langs = {
            'en': 'wiki.creativecommons.org', #Put the hostname here.
            }
        self.namespaces[4] = {
            '_default': u'CcWiki', #Specify the project namespace here. Other
            }                               #namespaces will be set to MediaWiki default.
        
        self.namespaces[5] = {
            '_default': u'CcWiki talk',
            }
        
    def version(self, code):
        return "1.11.2"  #The MediaWiki version used. Not very important in most cases.
    
    def path(self, code):
        return '/index.php' #The path of index.php

    def apipath(self, code):
        return '/api.php'
