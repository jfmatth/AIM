from aim.models import Symbol, Price
from django.core.exceptions import ObjectDoesNotExist

import csv
import datetime

"""
Loads a CSV file into the stock and price tables from EODDATA
"""

def EOD_LoadPrices(filename):
    import os

    if not os.path.exists(filename):
        raise Exception("File %s does not exist for importing" % filename)


    cr = csv.reader(open(filename,"r"))
    header = cr.next()

    if not header[0] == "Symbol" or not header[1] == "Date":
        raise Exception("Error - Header line in %s looks wrong" % filename)

    for csvline in cr:

        # skip the header.
        if csvline[0] == "Symbol":
            continue

        # assume all the records are here and the exceptions add them
        try:
            # need to convert first
            d = datetime.datetime.strptime(csvline[1], "%d-%b-%Y")

            p = Price.objects.get(symbol__name=csvline[0],
                                  date=d
                                  )
        except ObjectDoesNotExist:

            try:
                sym = Symbol.objects.get(name=csvline[0])

                p = Price()
                p.symbol = sym
                p.date = d
                p.open = csvline[2]
                p.high = csvline[3]
                p.low  = csvline[4]
                p.close = csvline[5]
                p.volume = csvline[6]

                p.save()

            except ObjectDoesNotExist :
                pass
            except:
                print "problem importing %s" % csvline


def EOD_LoadSymbols(filename):
    # load symbols from an EOD Symbols file into the Stock model.
    import os

    if os.path.exists(filename):
        # open a CSV with tabs.
        cr = csv.reader(open(filename,"r"), dialect="excel-tab")

        header = cr.next()

        if not header[0] == "Symbol" or not header[1] == "Description":
            raise Exception("Error - Header line in %s looks wrong" % filename)

        for csvline in cr:
            # assume all the records are here and the exceptions add them
            try:
                s = Symbol.objects.get_or_create( name        = csvline[0],
                                                  description = csvline[1]
                                                )
            except :
                print "problem on %s" % csvline

    else:
        raise Exception("File %s does not exist for importing" % filename)






