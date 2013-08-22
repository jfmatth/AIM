
from loadcsv import EOD_LoadPrices, EOD_LoadSymbols

import os

def main():

    print "Importing Symbols"
    # load all the symbols first
    import os
    for root, dirs, files  in os.walk('data/symbols'):
        for name in files:
            # these should all be symbols files, lets import them
            fullpath = os.path.normcase(os.path.normpath(os.path.join(root,name) ) ) # c:/dir/dir/filename

            print "Importing %s" % fullpath

            EOD_LoadSymbols(fullpath)

            # once it's loaded, remove it
            os.remove(fullpath)


    print
    print "Importing Prices"
    import os
    for root, dirs, files  in os.walk('data/prices'):
        for name in files:
            # these should all be symbols files, lets import them
            fullpath = os.path.normcase(os.path.normpath(os.path.join(root,name) ) ) # c:/dir/dir/filename

            print "Importing %s" % fullpath

            EOD_LoadPrices(fullpath)

            # once it's loaded, remove it
            os.remove(fullpath)

if __name__ == "__main__":
    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "aimWeb.settings")

    main()