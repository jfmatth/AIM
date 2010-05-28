from django.db import models
from django.contrib.auth.models import User
from django.core.exceptions import ObjectDoesNotExist

from decimal import *

import datetime
import aim_utilities

#
# Stock
#

class Stock(models.Model):
        symbol      = models.CharField(max_length=10, unique=True)
        description = models.CharField(max_length=50, blank=True)

        def current_price(self):
                try:
                        #figure out what the last price was.
                        return self.price_set.all()[0].close
                except:
                        # and if we don't have any prices, just return 0 for now.
                        return 0
        
        def price_now(self):
                # figure out if we have today's price in the system, if not, download it.
                
                try:
                        p = self.price_set.get(date=datetime.date.today().__str__() )
                        
                except ObjectDoesNotExist:
                        # well, that didn't work, so lets get it from Yahoo and save it in the DB
                        yahoo_quote = aim_utilities.StockPrice(self.symbol)
                        p = Price(stock=self,
                                  date = yahoo_quote['date'],
                                  high = yahoo_quote['high'],
                                  low  = yahoo_quote['low'],
                                  close = yahoo_quote['price'],
                                  volume = yahoo_quote['volume']
                                )
                        p.save()
                
                return p
                        
        def GetHistorical(self):
                # gets a years worth of historical prices, yippie.
                i_prices = aim_utilities.HistoricalStockPrice(self.symbol,
                                                         datetime.date.today() - datetime.timedelta(days=365),
                                                         datetime.date.today()
                                                         )
                # each entry in the list is a date, starting with the header
                
                # get a 'copy' of all the prices for this stock, so we only query it once, i hope
                db_prices = self.price_set.all()
                
                # run through all the prices from Yahoo and see if they are already there, if not, add them to DB, this
                # will be painfull if all the prices are not there, well, atcually, it will be painfull regardless :)
                for dayprice in i_prices[1:]:
                        try:
                                db_prices.get(date=dayprice[0])                        
                        except ObjectDoesNotExist:
                                p = Price(stock=self,
                                          date = dayprice[0],
                                          high = dayprice[2],
                                          low  = dayprice[3],
                                          close = dayprice[4],
                                          volume = dayprice[5]
                                        )
                                p.save()

                        
        def __unicode__(self):
                return self.symbol

#
# Price - Stock prices
#
class Price(models.Model):
        stock  = models.ForeignKey(Stock)
        date   = models.DateField(db_index=True)
        high   = models.DecimalField(max_digits=7, decimal_places=3)
        low    = models.DecimalField(max_digits=7, decimal_places=3)
        close  = models.DecimalField(max_digits=7, decimal_places=3)
        volume = models.IntegerField()
        
        def __unicode__(self):
                return "%s %s %s" % (self.stock.symbol, self.date, self.close)

        class Meta:
                ordering = ["-date"]

#
# Portfolio
#
portfolio_perms=(
        ("X", "None - Owner only"),
        ("V", "View-Only"),
)
class Portfolio(models.Model):
        name  = models.CharField(max_length=50)
        owner = models.ForeignKey(User)
        permission = models.CharField(max_length=10, choices=portfolio_perms, default="X")              
        
        def __unicode__(self):
                return self.name


class Holding(models.Model):
        portfolio    = models.ForeignKey(Portfolio)
        stock        = models.ForeignKey(Stock)

        def save(self, force_insert=False, force_update=False):
                if self.id == None:
                        # New record, so lets save a new AIM record too.
                        super(Holding, self).save(force_insert, force_update)
                        a = Aim(holding=self)
                        a.save()
                else:
                        super(Holding, self).save(force_insert, force_update)
                        

        def __unicode__(self):
                return "[%s in %s]" % (self.stock.symbol, self.portfolio)

        
        def shares(self):
                # figure out how many shares's we have
                s = 0 
                for t in self.transaction_set.all():
                        s = s + t.shares
                return s

        def NextBuy(self):
                # textbook AIM
                if self.aim.control <> 0:
                        pc = Decimal(self.aim.control)
                        sm = Decimal(self.aim.sellmin)
                        bm = Decimal(self.aim.buymin)
                        N  = Decimal(self.shares() )
                        ss = Decimal(self.aim.sellsafe) / Decimal(100)
                        bs = Decimal(self.aim.buysafe) / Decimal(100)
                        
                        return (pc - bm) / (N * ( Decimal(1) + bs) )
                else:
                        return 0

        def NextSell(self):
                # textbook AIM
                if self.aim.control <> 0:
                        pc = Decimal(self.aim.control)
                        sm = Decimal(self.aim.sellmin)
                        bm = Decimal(self.aim.buymin)
                        N  = Decimal(self.shares() )
                        ss = Decimal(self.aim.sellsafe) / Decimal(100)
                        bs = Decimal(self.aim.buysafe) / Decimal(100)
                        
                        return (pc + sm) / (N * ( Decimal(1) - ss) )
                else:
                        return 0
        

#
# Aim - Keeps track of all the AIM settings we've created over time, for a particular holding.
#
AIM_TYPES = (
        ("None", "None"),
        ("Standard", "Standard"),
)
class Aim(models.Model):
        holding   = models.OneToOneField(Holding)
        
        type      = models.CharField(max_length=10, choices=AIM_TYPES, default="Standard")
        control   = models.IntegerField(default=0)           # Portfolio Control
        sellsafe  = models.IntegerField(default=10)          # SAFE for sales, a percentage value
        sellmin   = models.IntegerField(default=500)         # Minimum to sell in a transaction
        buysafe   = models.IntegerField(default=10)          # SAFE for buys
        buymin    = models.IntegerField(default=500)         # Minimum to buy
        
        def __unicode__(self):
                return "%s (%s)" % (self.holding, self.control)

#
# Transaction - Pretty obvious, each stock trade is recorded as a transaction
#        
class Transaction(models.Model):
        holding        = models.ForeignKey(Holding)
        date           = models.DateField()
        shares         = models.DecimalField(max_digits=10, decimal_places=3)
        price          = models.DecimalField(max_digits=8, decimal_places=3)

        #class Meta:
        #        ordering = ["-date"]

        def __unicode__(self):
                return "%s %s (%s @ %s)" % (self.holding,self.date, self.shares,self.price)
                
        def total(self):
                return self.shares * self.price


        def save(self, force_insert=False, force_update=False):
                # for transactions, we have to account for new records, and update the AIM values accordingly.
                if self.id == None:

                        # we'll be working on the AIM object, so lets keep that in a var.
                        working_aim = self.holding.aim
                        
                        if working_aim.type == "Standard":
                                
                                if self.total() > 0:    
                                        if working_aim.control == 0:
                                                # we can assume a control of 0 means its not started ?
                                                # if so, then start control at the total sale price.
                                                working_aim.control += self.total()
                                        else:
                                                # otherwise we only add 1/2 to the control
                                                working_aim.control += self.total() / 2
                                                
                                        working_aim.save()
        
                super(Transaction, self).save(force_insert, force_update)
        
        


