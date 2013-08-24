# Create your views here.
from django.core.exceptions import ObjectDoesNotExist
from django.http import HttpResponse
from django.db import transaction

import logging
import csv
import datetime

from aim.models import Symbol, Price
from loader.models import Exchange, ExchangePrice

# Get an instance of a logger
logger = logging.getLogger(__name__)

@transaction.commit_on_success
def ImportPrices(f):
    """
    Import a file f into the prices table.
    """
    dialect = csv.Sniffer().sniff( f.read(1024) )
    f.seek(0)
    reader = csv.reader(f, dialect)
        
    header = reader.next()

    if not header[0] == "Symbol" or not header[1] == "Date":
        raise Exception("Error - Header line in looks wrong, %s" % header)

    for csvline in reader:

        # skip the header.
        if csvline[0] == "Symbol":
            continue

        d = datetime.datetime.strptime(csvline[1], "%d-%b-%Y").date()
        
        # assume all the records are here and the exceptions add them
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
            
            # check if this price upload is 'newer' than the symbols current price
            if sym.currentprice == None or p.date > sym.currentprice.date:
                sym.currentprice = p
                sym.save()

        except:
            print "Problem with %s" % csvline 
        
def LoadPrices(request):

    count = 0    
    for e in ExchangePrice.objects.filter(loaded=False):
        # we have an exchange that hasn't been loaded.
        
        # sniff it out and load it into Symbols.
        ImportPrices(e.file)

        e.loaded = True
        e.save()
        count += 1

    return HttpResponse("Loaded %s Prices" % count)


@transaction.commit_on_success
def ImportExchange(f):
    dialect = csv.Sniffer().sniff( f.read(1024) )
    f.seek(0)
    reader = csv.reader(f, dialect)
    
    header = reader.next()
    
    if not header[0] == "Symbol" or not header[1] == "Description":
        raise Exception("Error - Header line in %s looks wrong" % header)

    for csvline in reader:
        # assume all the records are here and the exceptions add them
        try:
            Symbol(name = csvline[0],description = csvline[1]).save()
        except:
            print "problem on %s" % (csvline)

def LoadExchange(request):
    logger.info("Load Exchange()")
    count = 0
    
    for e in Exchange.objects.filter(loaded=False):
        # we have an exchange that hasn't been loaded.
        
        # sniff it out and load it into Symbols.
        ImportExchange(e.file)

        e.loaded = True
        e.save()
        
        count += 1

    return HttpResponse("%s Exchanges Loaded" % count)