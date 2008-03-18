import wikipedia
import catlib
import pagegenerators

def for_category_member(category_name, function):
    site = wikipedia.getSite()
    cat = catlib.Category(site, category_name)
    gen = pagegenerators.CategorizedPageGenerator(cat)
    for page in gen:
        function(page)

