from django.db import models
from django.contrib.auth.models import User
from django.core.exceptions import ObjectDoesNotExist

from decimal import *

import datetime
import util.aim_utilities

#
# Stock
#

class Symbol(models.Model):
        name        = models.CharField(max_length=10, unique=True, db_index=True)
        description = models.CharField(max_length=50, blank=True)

        def __unicode__(self):
            return self.name

        def CurrentPrice(self):
                try:
                        #figure out what the last price was.
                        return self.price_set.all()[0].close
                except:
                        # and if we don't have any prices, just return 0 for now.
                        return 0
        
#        def price_now(self):
#                # figure out if we have today's price in the system, if not, download it.
#                try:
#                        p = self.price_set.get(date=datetime.date.today().__str__() )
#                except ObjectDoesNotExist:
#                        # well, that didn't work, so lets get it from Yahoo and save it in the DB
#                        yahoo_quote = aim_utilities.StockPrice(self.symbol)
#                        p = Price(stock=self,
#                                  date = yahoo_quote['date'],
#                                  high = yahoo_quote['high'],
#                                  low  = yahoo_quote['low'],
#                                  close = yahoo_quote['price'],
#                                  volume = yahoo_quote['volume']
#                                )
#                        p.save()
#
#                return p
#
#        def GetHistorical(self):
#                # gets a years worth of historical prices, yippie.
#                i_prices = aim_utilities.HistoricalStockPrice(self.symbol,
#                                                         datetime.date.today() - datetime.timedelta(days=365),
#                                                         datetime.date.today()
#                                                         )
#                # each entry in the list is a date, starting with the header
#
#                # get a 'copy' of all the prices for this stock, so we only query it once, i hope
#                db_prices = self.price_set.all()
#
#                # run through all the prices from Yahoo and see if they are already there, if not, add them to DB, this
#                # will be painfull if all the prices are not there, well, atcually, it will be painfull regardless :)
#                for dayprice in i_prices[1:]:
#                        try:
#                                db_prices.get(date=dayprice[0])
#                        except ObjectDoesNotExist:
#                                p = Price(stock=self,
#                                          date = dayprice[0],
#                                          high = dayprice[2],
#                                          low  = dayprice[3],
#                                          close = dayprice[4],
#                                          volume = dayprice[5]
#                                        )
#                                p.save()
#
                        

#
# Price - Stock prices
#
class Price(models.Model):
        symbol = models.ForeignKey(Symbol)
        date   = models.DateField(db_index=True)
        high   = models.DecimalField(max_digits=7, decimal_places=3)
        low    = models.DecimalField(max_digits=7, decimal_places=3)
        close  = models.DecimalField(max_digits=7, decimal_places=3)
        volume = models.IntegerField()
        
        def __unicode__(self):
                return "%s %s %s" % (self.symbol.name, self.date, self.close)

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

# Types of AIM programs
AIM_TYPES = (
        ("Standard", "Standard"),
)
class Holding(models.Model):
        portfolio    = models.ForeignKey(Portfolio)
        symbol       = models.ForeignKey(Symbol)
        aimtype      = models.CharField(max_length=10, choices=AIM_TYPES, default="Standard")

        def getAim(self):
                if self.aimtype == "Standard":
                        return self.aimstandard
        aim = property(getAim)
        
        def save(self, force_insert=False, force_update=False):
                if self.id == None:
                        # New record, so lets save a new AIM record too.
                        super(Holding, self).save(force_insert, force_update)
                        
                        # JFM, figure out what AIM we need, for now, all we have is AimStandard
                        if self.aimtype == "Standard":
                                a = AimStandard(holding=self)
                                a.save()
                else:
                        super(Holding, self).save(force_insert, force_update)

        def __unicode__(self):
                return "[%s in %s]" % (self.symbol.name, self.portfolio)

        
        def shares(self):
                # figure out how many shares's we have
                s = 0
                for t in self.transaction_set.all():
                        s = s + t.shares
                return s
        
        def value(self):
                return self.shares() * self.symbol.CurrentPrice()
                
                
        def NextBuy(self):
                # JFM, move all the AIM stuff to the AIM object we have
                return self.aim.NextBuy()

        def NextSell(self):
                # JFM - MOve all the AIM stuff to the AIM object
                return self.aim.NextSell()
                

# JFM - Change to a more OO version of models, use a base AIM class and then derive from there.

# AIM Models, use multiple inheritance with abstract True.
#               all functionallity for AIM should be here, not in other models.
class AimBase(models.Model):
        holding   = models.OneToOneField(Holding)        
        
        control   = models.IntegerField(default=0)           # Portfolio Control
        sellsafe  = models.IntegerField(default=10)          # SAFE for sales, a percentage value
        sellmin   = models.IntegerField(default=500)         # Minimum to sell in a transaction
        buysafe   = models.IntegerField(default=10)          # SAFE for buys
        buymin    = models.IntegerField(default=500)         # Minimum to buy
                
        # Holy Shit! I just figure out the forumla I've been using hasn't been right, and missed these figures
        # they are the percentage of value to buy / sell each time, instead of the fixed values above (buyin/sellmin).
        # Crap!
        buyperc    = models.IntegerField(default=10)          # how much percent of value to buy
        sellperc   = models.IntegerField(default=10)          # how much percent of value to sell 
        
        def __unicode__(self):
                return "Base class for Aim"
        
        def BuyPrice(self):
                return Decimal(0)
        def BuyAmount(self):
                return Decimal(0)
                
        def SellPrice(self):
                return Decimal(0)
        def SellAmount(self):
                return Decimal(0)
                
        def transaction(self, transaction=None):
                return Decimal(0)
        
        class Meta:
                abstract = True

class AimStandard(AimBase):
        def BuyPrice(self):
                if self.control <> 0:
                        # JFM, 5/3/2010 - Just realized that the above formula is WRONG!  All these years!
                        #
                        # below is the new formula from the aim-users website (http://aim-users.com/aimbrief.htm)
                        
                        # JFM, account for the minimum amount field too.
                        bm = self.holding.value() * (self.buyperc / Decimal(100) ) 
                        
                        pc = Decimal(self.control)
                        N  = Decimal(self.holding.shares())
                        ss = Decimal(self.sellsafe) / Decimal(100)
                        bs = Decimal(self.buysafe) / Decimal(100)
                        
                        return (pc - bm) / (N * ( Decimal(1) + bs) )
                        
                else:
                        return Decimal(0)

        def BuyAmount(self):
                # Normal AIM formula for buy amount is
                #
                # PC - (Current Value + (Safe * Current value) )
                #
                amount = self.control - (self.holding.value() + (self.buysafe / Decimal(100) * self.holding.value()) )
                if amount > 0:
                        return amount
                else:
                        return 0            
                        
        def SellPrice(self):                
                if self.control <> 0:
                        # JFM, 6/17/10, account for minimums too.
                        sm = self.holding.value() * (self.sellperc / Decimal(100) )
                        
                        pc = Decimal(self.control)
                        N  = Decimal(self.holding.shares() )
                        ss = Decimal(self.sellsafe) / Decimal(100)
                        bs = Decimal(self.buysafe) / Decimal(100)
                        
                        return (pc + sm) / (N * ( Decimal(1) - ss) )
                else:
                        return Decimal(0)
                        
        def SellAmount(self):
                # Normal AIM formula for sell amount is
                #
                #  PC + (Safe * Current value) - Current Value
                #
                amount = self.control + (self.sellsafe / Decimal(100) * self.holding.value() ) - self.holding.value()
                if amount < 0 :
                        return amount
                else:
                        return 0


        def transaction(self, transaction=None):
                if transaction.total() > 0:
                        if self.control == 0:
                                # we can assume a control of 0 means its not started ?
                                # if so, then start control at the total sale price.
                                self.control += transaction.total()
                        else:
                                # otherwise we only add 1/2 to the control
                                self.control += transaction.total() / 2
                                
                        self.save()

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
                return "%s %s (%s @ %s)" % (self.holding, self.date, self.shares, self.price)
                
        def total(self):
                return self.shares * self.price

        def save(self, force_insert=False, force_update=False):
                # We are only accounting for new records for now, eventually we have to acccount
                # for modify records too, no?
                if self.id == None:
                        self.holding.aim.transaction(transaction=self)
                                
                super(Transaction, self).save(force_insert, force_update)
        
        


