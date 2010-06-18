# encoding: utf-8
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models

class Migration(SchemaMigration):

    def forwards(self, orm):
        
        # Adding model 'Stock'
        db.create_table('aim_stock', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('symbol', self.gf('django.db.models.fields.CharField')(unique=True, max_length=10)),
            ('description', self.gf('django.db.models.fields.CharField')(max_length=50, blank=True)),
        ))
        db.send_create_signal('aim', ['Stock'])

        # Adding model 'Price'
        db.create_table('aim_price', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('stock', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['aim.Stock'])),
            ('date', self.gf('django.db.models.fields.DateField')(db_index=True)),
            ('high', self.gf('django.db.models.fields.DecimalField')(max_digits=7, decimal_places=3)),
            ('low', self.gf('django.db.models.fields.DecimalField')(max_digits=7, decimal_places=3)),
            ('close', self.gf('django.db.models.fields.DecimalField')(max_digits=7, decimal_places=3)),
            ('volume', self.gf('django.db.models.fields.IntegerField')()),
        ))
        db.send_create_signal('aim', ['Price'])

        # Adding model 'Portfolio'
        db.create_table('aim_portfolio', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=50)),
            ('owner', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['auth.User'])),
            ('permission', self.gf('django.db.models.fields.CharField')(default='X', max_length=10)),
        ))
        db.send_create_signal('aim', ['Portfolio'])

        # Adding model 'Holding'
        db.create_table('aim_holding', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('portfolio', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['aim.Portfolio'])),
            ('stock', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['aim.Stock'])),
            ('aimtype', self.gf('django.db.models.fields.CharField')(default='Standard', max_length=10)),
        ))
        db.send_create_signal('aim', ['Holding'])

        # Adding model 'AimStandard'
        db.create_table('aim_aimstandard', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('holding', self.gf('django.db.models.fields.related.OneToOneField')(to=orm['aim.Holding'], unique=True)),
            ('control', self.gf('django.db.models.fields.IntegerField')(default=0)),
            ('sellsafe', self.gf('django.db.models.fields.IntegerField')(default=10)),
            ('sellmin', self.gf('django.db.models.fields.IntegerField')(default=500)),
            ('buysafe', self.gf('django.db.models.fields.IntegerField')(default=10)),
            ('buymin', self.gf('django.db.models.fields.IntegerField')(default=500)),
            ('buyperc', self.gf('django.db.models.fields.IntegerField')(default=10)),
            ('sellperc', self.gf('django.db.models.fields.IntegerField')(default=10)),
        ))
        db.send_create_signal('aim', ['AimStandard'])

        # Adding model 'Transaction'
        db.create_table('aim_transaction', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('holding', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['aim.Holding'])),
            ('date', self.gf('django.db.models.fields.DateField')()),
            ('shares', self.gf('django.db.models.fields.DecimalField')(max_digits=10, decimal_places=3)),
            ('price', self.gf('django.db.models.fields.DecimalField')(max_digits=8, decimal_places=3)),
        ))
        db.send_create_signal('aim', ['Transaction'])


    def backwards(self, orm):
        
        # Deleting model 'Stock'
        db.delete_table('aim_stock')

        # Deleting model 'Price'
        db.delete_table('aim_price')

        # Deleting model 'Portfolio'
        db.delete_table('aim_portfolio')

        # Deleting model 'Holding'
        db.delete_table('aim_holding')

        # Deleting model 'AimStandard'
        db.delete_table('aim_aimstandard')

        # Deleting model 'Transaction'
        db.delete_table('aim_transaction')


    models = {
        'aim.aimstandard': {
            'Meta': {'object_name': 'AimStandard'},
            'buymin': ('django.db.models.fields.IntegerField', [], {'default': '500'}),
            'buyperc': ('django.db.models.fields.IntegerField', [], {'default': '10'}),
            'buysafe': ('django.db.models.fields.IntegerField', [], {'default': '10'}),
            'control': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'holding': ('django.db.models.fields.related.OneToOneField', [], {'to': "orm['aim.Holding']", 'unique': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'sellmin': ('django.db.models.fields.IntegerField', [], {'default': '500'}),
            'sellperc': ('django.db.models.fields.IntegerField', [], {'default': '10'}),
            'sellsafe': ('django.db.models.fields.IntegerField', [], {'default': '10'})
        },
        'aim.holding': {
            'Meta': {'object_name': 'Holding'},
            'aimtype': ('django.db.models.fields.CharField', [], {'default': "'Standard'", 'max_length': '10'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'portfolio': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['aim.Portfolio']"}),
            'stock': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['aim.Stock']"})
        },
        'aim.portfolio': {
            'Meta': {'object_name': 'Portfolio'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '50'}),
            'owner': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['auth.User']"}),
            'permission': ('django.db.models.fields.CharField', [], {'default': "'X'", 'max_length': '10'})
        },
        'aim.price': {
            'Meta': {'object_name': 'Price'},
            'close': ('django.db.models.fields.DecimalField', [], {'max_digits': '7', 'decimal_places': '3'}),
            'date': ('django.db.models.fields.DateField', [], {'db_index': 'True'}),
            'high': ('django.db.models.fields.DecimalField', [], {'max_digits': '7', 'decimal_places': '3'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'low': ('django.db.models.fields.DecimalField', [], {'max_digits': '7', 'decimal_places': '3'}),
            'stock': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['aim.Stock']"}),
            'volume': ('django.db.models.fields.IntegerField', [], {})
        },
        'aim.stock': {
            'Meta': {'object_name': 'Stock'},
            'description': ('django.db.models.fields.CharField', [], {'max_length': '50', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'symbol': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '10'})
        },
        'aim.transaction': {
            'Meta': {'object_name': 'Transaction'},
            'date': ('django.db.models.fields.DateField', [], {}),
            'holding': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['aim.Holding']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'price': ('django.db.models.fields.DecimalField', [], {'max_digits': '8', 'decimal_places': '3'}),
            'shares': ('django.db.models.fields.DecimalField', [], {'max_digits': '10', 'decimal_places': '3'})
        },
        'auth.group': {
            'Meta': {'object_name': 'Group'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '80'}),
            'permissions': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['auth.Permission']", 'symmetrical': 'False', 'blank': 'True'})
        },
        'auth.permission': {
            'Meta': {'unique_together': "(('content_type', 'codename'),)", 'object_name': 'Permission'},
            'codename': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'content_type': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['contenttypes.ContentType']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '50'})
        },
        'auth.user': {
            'Meta': {'object_name': 'User'},
            'date_joined': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'email': ('django.db.models.fields.EmailField', [], {'max_length': '75', 'blank': 'True'}),
            'first_name': ('django.db.models.fields.CharField', [], {'max_length': '30', 'blank': 'True'}),
            'groups': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['auth.Group']", 'symmetrical': 'False', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_active': ('django.db.models.fields.BooleanField', [], {'default': 'True', 'blank': 'True'}),
            'is_staff': ('django.db.models.fields.BooleanField', [], {'default': 'False', 'blank': 'True'}),
            'is_superuser': ('django.db.models.fields.BooleanField', [], {'default': 'False', 'blank': 'True'}),
            'last_login': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'last_name': ('django.db.models.fields.CharField', [], {'max_length': '30', 'blank': 'True'}),
            'password': ('django.db.models.fields.CharField', [], {'max_length': '128'}),
            'user_permissions': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['auth.Permission']", 'symmetrical': 'False', 'blank': 'True'}),
            'username': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '30'})
        },
        'contenttypes.contenttype': {
            'Meta': {'unique_together': "(('app_label', 'model'),)", 'object_name': 'ContentType', 'db_table': "'django_content_type'"},
            'app_label': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'model': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'})
        }
    }

    complete_apps = ['aim']
