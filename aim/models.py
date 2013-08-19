from django.contrib.auth.models import User
from django.db import models
from django.core.exceptions import ObjectDoesNotExist

import datetime
from decimal import Decimal

# import util.aim_utilities

#===============================================================================
# Symbol - Stock Symbol
#===============================================================================
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
                        
#===============================================================================
# Price - Stock price 1-N back to Symbol
#===============================================================================
class Price(models.Model):
    symbol = models.ForeignKey(Symbol)
    
    date   = models.DateField(db_index=True)
    high   = models.DecimalField(max_digits=12, decimal_places=3)
    low    = models.DecimalField(max_digits=12, decimal_places=3)
    close  = models.DecimalField(max_digits=12, decimal_places=3)
    volume = models.IntegerField()
    
    def __unicode__(self):
        return "%s %s %s" % (self.symbol.name, self.date, self.close)

#===============================================================================
# Portfolio 
#===============================================================================
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
            
#===============================================================================
# Holding - A stock symbol in a portfolio
#===============================================================================
class Holding(models.Model):
    portfolio    = models.ForeignKey(Portfolio)
    symbol       = models.ForeignKey(Symbol)
    
    def save(self, force_insert=False, force_update=False):
        if self.id == None:
            # New record, so lets save a new Controller record too.
            super(Holding, self).save(force_insert, force_update)
            AimController(holding = self).save()
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
            
#===============================================================================
# HoldingAlert - A static version of what the next buy / sell prices will 
#                be for a particular holding.
#                Typically generated from the controllers transaction method.
#===============================================================================
class HoldingAlert(models.Model):
    holding = models.ForeignKey(Holding)
    
    buyprice  = models.DecimalField(max_digits=10, decimal_places=3)
    sellprice = models.DecimalField(max_digits=10, decimal_places=3)

    def __unicode__(self):
        return "%s b:%s s:%s" % (self.holding, self.buyprice,self.sellprice)

    def save(self, force_insert=False, force_update=False):
        if self.id == None:
            self.buyprice = self.holding.controller.BuyPrice()
            self.sellprice = self.holding.controller.SellPrice()
            
        super(HoldingAlert, self).save(force_insert, force_update)
        

#===============================================================================
# AimBase - Base class for all transaction controllers
#===============================================================================
class AimBase(models.Model):
    holding   = models.OneToOneField(Holding, related_name="controller")

    started   = models.BooleanField()                   # is the program started?
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
    
    
#===============================================================================
# AimStandard - AIM by the book
#===============================================================================
class AimController(AimBase):
    def BuyPrice(self):
        if self.control <> 0:
            # JFM, 5/3/2010 - Just realized that the above formula is WRONG!  All these years!
            #
            # below is the new formula from the aim-users website (http://aim-users.com/aimbrief.htm)
            
            # JFM, account for the minimum amount field too.
            bm = self.holding.value() * (self.buyperc / Decimal(100) )
            # JFM, account for minimum amounts.
            bm = max(bm, self.buymin) 
            
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
            sm = max(sm, self.sellmin)
            
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
            if not self.started:
                    # we can assume a control of 0 means its not started ?
                    # if so, then start control at the total sale price.
                    self.control += transaction.total()
            else:
                    # otherwise we only add 1/2 to the control
                    self.control += transaction.total() / 2
            self.started = True
            self.save()
        
#             # now add a holding alert for the changes.
#             HoldingAlert(holding=self.holding).save()
            
            
    def save(self, force_insert=False, force_update=False):
        super(AimController, self).save(force_insert, force_update)
        
        # if the user changes the controller settings, recalc the alert
#         if self.id != None:
#             # but not if this is the first record, because the transaction will do that.
#             alert = HoldingAlert()
#             alert.holding = self.holding
#             alert.buyprice = self.BuyPrice()
#             alert.sellprice = self.SellPrice()
#             alert.save()
        HoldingAlert(holding=self.holding).save()
        

    def __unicode__(self):
        return "%s (%s)" % (self.holding, self.control)

#===============================================================================
# Transaction - Each holding has transactions
#===============================================================================
class Transaction(models.Model):
    holding        = models.ForeignKey(Holding)
    
    date           = models.DateField()
    shares         = models.DecimalField(max_digits=10, decimal_places=3)
    price          = models.DecimalField(max_digits=8, decimal_places=3)

    def __unicode__(self):
        return "%s %s (%s @ %s)" % (self.holding, self.date, self.shares, self.price)
            
    def total(self):
        return self.shares * self.price

    def save(self, force_insert=False, force_update=False):
        super(Transaction, self).save(force_insert, force_update)
        
        self.holding.controller.transaction(transaction=self)

#===============================================================================
# AimNone - A base transaction controller, no AIM, just basic add / subtract from a holding.
#===============================================================================
#class AimNone(AimBase):
#        def __unicode__(self):
#                return "Base class for Aim"
#        
#        def BuyPrice(self):
#                return Decimal(0)
#
#        def BuyAmount(self):
#                return Decimal(0)
#                
#        def SellPrice(self):
#                return Decimal(0)
#        
#        def SellAmount(self):
#                return Decimal(0)
#                
#        def transaction(self, transaction=None):
#                return Decimal(0)
#            
#        class Meta:
#            proxy = True
