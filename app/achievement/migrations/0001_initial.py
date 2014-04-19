# -*- coding: utf-8 -*-
from south.utils import datetime_utils as datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'Difficulty'
        db.create_table(u'achievement_difficulty', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=30)),
            ('description', self.gf('django.db.models.fields.TextField')(blank=True)),
            ('points', self.gf('django.db.models.fields.PositiveIntegerField')()),
        ))
        db.send_create_signal('achievement', ['Difficulty'])

        # Adding model 'Badge'
        db.create_table(u'achievement_badge', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=50)),
            ('description', self.gf('django.db.models.fields.TextField')(blank=True)),
        ))
        db.send_create_signal('achievement', ['Badge'])

        # Adding model 'Method'
        db.create_table(u'achievement_method', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=100)),
            ('description', self.gf('django.db.models.fields.TextField')(blank=True)),
            ('callablemethod', self.gf('django.db.models.fields.CharField')(max_length=50)),
            ('argument_type', self.gf('django.db.models.fields.CharField')(max_length=50, null=True, blank=True)),
        ))
        db.send_create_signal('achievement', ['Method'])

        # Adding model 'Qualifier'
        db.create_table(u'achievement_qualifier', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=100)),
            ('description', self.gf('django.db.models.fields.TextField')(blank=True)),
            ('callablemethod', self.gf('django.db.models.fields.CharField')(max_length=50)),
            ('argument_type', self.gf('django.db.models.fields.CharField')(max_length=50, null=True, blank=True)),
            ('return_type', self.gf('django.db.models.fields.CharField')(max_length=50, null=True, blank=True)),
        ))
        db.send_create_signal('achievement', ['Qualifier'])

        # Adding model 'Quantifier'
        db.create_table(u'achievement_quantifier', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=100)),
            ('description', self.gf('django.db.models.fields.TextField')(blank=True)),
            ('callablemethod', self.gf('django.db.models.fields.CharField')(max_length=50)),
            ('argument_type', self.gf('django.db.models.fields.CharField')(max_length=50, null=True, blank=True)),
        ))
        db.send_create_signal('achievement', ['Quantifier'])

        # Adding model 'ConditionType'
        db.create_table(u'achievement_conditiontype', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=100)),
            ('description', self.gf('django.db.models.fields.TextField')(blank=True)),
            ('custom', self.gf('django.db.models.fields.BooleanField')(default=False)),
        ))
        db.send_create_signal('achievement', ['ConditionType'])

        # Adding model 'CustomCondition'
        db.create_table(u'achievement_customcondition', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('event_type', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['services.Event'])),
            ('description', self.gf('django.db.models.fields.TextField')(blank=True)),
            ('condition_type', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['achievement.ConditionType'])),
            ('method', self.gf('django.db.models.fields.CharField')(max_length=100)),
        ))
        db.send_create_signal('achievement', ['CustomCondition'])

        # Adding model 'ValueCondition'
        db.create_table(u'achievement_valuecondition', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('event_type', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['services.Event'])),
            ('description', self.gf('django.db.models.fields.TextField')(blank=True)),
            ('condition_type', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['achievement.ConditionType'])),
            ('method', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['achievement.Method'])),
            ('attribute', self.gf('django.db.models.fields.CharField')(max_length=200)),
            ('value', self.gf('django.db.models.fields.CharField')(max_length=200)),
            ('qualifier', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['achievement.Qualifier'], null=True, blank=True)),
            ('quantifier', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['achievement.Quantifier'], null=True, blank=True)),
        ))
        db.send_create_signal('achievement', ['ValueCondition'])

        # Adding model 'AttributeCondition'
        db.create_table(u'achievement_attributecondition', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('event_type', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['services.Event'])),
            ('description', self.gf('django.db.models.fields.TextField')(blank=True)),
            ('condition_type', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['achievement.ConditionType'])),
            ('method', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['achievement.Method'])),
            ('attributes', self.gf('jsonfield.fields.JSONField')(default={})),
        ))
        db.send_create_signal('achievement', ['AttributeCondition'])

        # Adding M2M table for field qualifiers on 'AttributeCondition'
        m2m_table_name = db.shorten_name(u'achievement_attributecondition_qualifiers')
        db.create_table(m2m_table_name, (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('attributecondition', models.ForeignKey(orm['achievement.attributecondition'], null=False)),
            ('qualifier', models.ForeignKey(orm['achievement.qualifier'], null=False))
        ))
        db.create_unique(m2m_table_name, ['attributecondition_id', 'qualifier_id'])

        # Adding model 'AchievementType'
        db.create_table(u'achievement_achievementtype', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=50)),
            ('custom', self.gf('django.db.models.fields.BooleanField')(default=True)),
        ))
        db.send_create_signal('achievement', ['AchievementType'])

        # Adding model 'AchievementCondition'
        db.create_table(u'achievement_achievementcondition', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('object_id', self.gf('django.db.models.fields.PositiveIntegerField')()),
            ('content_type', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['contenttypes.ContentType'])),
        ))
        db.send_create_signal('achievement', ['AchievementCondition'])

        # Adding M2M table for field achievements on 'AchievementCondition'
        m2m_table_name = db.shorten_name(u'achievement_achievementcondition_achievements')
        db.create_table(m2m_table_name, (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('achievementcondition', models.ForeignKey(orm['achievement.achievementcondition'], null=False)),
            ('achievement', models.ForeignKey(orm['achievement.achievement'], null=False))
        ))
        db.create_unique(m2m_table_name, ['achievementcondition_id', 'achievement_id'])

        # Adding model 'Achievement'
        db.create_table(u'achievement_achievement', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=100)),
            ('description', self.gf('django.db.models.fields.TextField')(blank=True)),
            ('active', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('difficulty', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['achievement.Difficulty'])),
            ('achievement_type', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['achievement.AchievementType'])),
            ('badge', self.gf('django.db.models.fields.related.OneToOneField')(blank=True, related_name='achievement', unique=True, null=True, to=orm['achievement.Badge'])),
            ('creator', self.gf('django.db.models.fields.related.ForeignKey')(blank=True, related_name='created_achievements', null=True, to=orm['achievement.UserProfile'])),
            ('grouping', self.gf('django.db.models.fields.CharField')(default='__and__', max_length=10)),
        ))
        db.send_create_signal('achievement', ['Achievement'])

        # Adding M2M table for field upvoters on 'Achievement'
        m2m_table_name = db.shorten_name(u'achievement_achievement_upvoters')
        db.create_table(m2m_table_name, (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('achievement', models.ForeignKey(orm['achievement.achievement'], null=False)),
            ('userprofile', models.ForeignKey(orm['achievement.userprofile'], null=False))
        ))
        db.create_unique(m2m_table_name, ['achievement_id', 'userprofile_id'])

        # Adding M2M table for field downvoters on 'Achievement'
        m2m_table_name = db.shorten_name(u'achievement_achievement_downvoters')
        db.create_table(m2m_table_name, (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('achievement', models.ForeignKey(orm['achievement.achievement'], null=False)),
            ('userprofile', models.ForeignKey(orm['achievement.userprofile'], null=False))
        ))
        db.create_unique(m2m_table_name, ['achievement_id', 'userprofile_id'])

        # Adding model 'UserAchievement'
        db.create_table(u'achievement_userachievement', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('earned_at', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, blank=True)),
            ('achievement', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['achievement.Achievement'])),
            ('user', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['achievement.UserProfile'])),
        ))
        db.send_create_signal('achievement', ['UserAchievement'])

        # Adding model 'UserProfile'
        db.create_table(u'achievement_userprofile', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('user', self.gf('django.db.models.fields.related.OneToOneField')(related_name='profile', unique=True, to=orm['auth.User'])),
            ('moderator', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('points', self.gf('django.db.models.fields.PositiveIntegerField')(default=0)),
            ('attributes', self.gf('jsonfield.fields.JSONField')(default={})),
        ))
        db.send_create_signal('achievement', ['UserProfile'])

        # Adding M2M table for field badges on 'UserProfile'
        m2m_table_name = db.shorten_name(u'achievement_userprofile_badges')
        db.create_table(m2m_table_name, (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('userprofile', models.ForeignKey(orm['achievement.userprofile'], null=False)),
            ('badge', models.ForeignKey(orm['achievement.badge'], null=False))
        ))
        db.create_unique(m2m_table_name, ['userprofile_id', 'badge_id'])


    def backwards(self, orm):
        # Deleting model 'Difficulty'
        db.delete_table(u'achievement_difficulty')

        # Deleting model 'Badge'
        db.delete_table(u'achievement_badge')

        # Deleting model 'Method'
        db.delete_table(u'achievement_method')

        # Deleting model 'Qualifier'
        db.delete_table(u'achievement_qualifier')

        # Deleting model 'Quantifier'
        db.delete_table(u'achievement_quantifier')

        # Deleting model 'ConditionType'
        db.delete_table(u'achievement_conditiontype')

        # Deleting model 'CustomCondition'
        db.delete_table(u'achievement_customcondition')

        # Deleting model 'ValueCondition'
        db.delete_table(u'achievement_valuecondition')

        # Deleting model 'AttributeCondition'
        db.delete_table(u'achievement_attributecondition')

        # Removing M2M table for field qualifiers on 'AttributeCondition'
        db.delete_table(db.shorten_name(u'achievement_attributecondition_qualifiers'))

        # Deleting model 'AchievementType'
        db.delete_table(u'achievement_achievementtype')

        # Deleting model 'AchievementCondition'
        db.delete_table(u'achievement_achievementcondition')

        # Removing M2M table for field achievements on 'AchievementCondition'
        db.delete_table(db.shorten_name(u'achievement_achievementcondition_achievements'))

        # Deleting model 'Achievement'
        db.delete_table(u'achievement_achievement')

        # Removing M2M table for field upvoters on 'Achievement'
        db.delete_table(db.shorten_name(u'achievement_achievement_upvoters'))

        # Removing M2M table for field downvoters on 'Achievement'
        db.delete_table(db.shorten_name(u'achievement_achievement_downvoters'))

        # Deleting model 'UserAchievement'
        db.delete_table(u'achievement_userachievement')

        # Deleting model 'UserProfile'
        db.delete_table(u'achievement_userprofile')

        # Removing M2M table for field badges on 'UserProfile'
        db.delete_table(db.shorten_name(u'achievement_userprofile_badges'))


    models = {
        'achievement.achievement': {
            'Meta': {'object_name': 'Achievement'},
            'achievement_type': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['achievement.AchievementType']"}),
            'active': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'badge': ('django.db.models.fields.related.OneToOneField', [], {'blank': 'True', 'related_name': "'achievement'", 'unique': 'True', 'null': 'True', 'to': "orm['achievement.Badge']"}),
            'creator': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'created_achievements'", 'null': 'True', 'to': "orm['achievement.UserProfile']"}),
            'description': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'difficulty': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['achievement.Difficulty']"}),
            'downvoters': ('django.db.models.fields.related.ManyToManyField', [], {'blank': 'True', 'related_name': "'disapproval_votes'", 'null': 'True', 'symmetrical': 'False', 'to': "orm['achievement.UserProfile']"}),
            'grouping': ('django.db.models.fields.CharField', [], {'default': "'__and__'", 'max_length': '10'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'upvoters': ('django.db.models.fields.related.ManyToManyField', [], {'blank': 'True', 'related_name': "'approval_votes'", 'null': 'True', 'symmetrical': 'False', 'to': "orm['achievement.UserProfile']"})
        },
        'achievement.achievementcondition': {
            'Meta': {'object_name': 'AchievementCondition'},
            'achievements': ('django.db.models.fields.related.ManyToManyField', [], {'related_name': "'conditions'", 'symmetrical': 'False', 'to': "orm['achievement.Achievement']"}),
            'content_type': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['contenttypes.ContentType']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'object_id': ('django.db.models.fields.PositiveIntegerField', [], {})
        },
        'achievement.achievementtype': {
            'Meta': {'object_name': 'AchievementType'},
            'custom': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '50'})
        },
        'achievement.attributecondition': {
            'Meta': {'object_name': 'AttributeCondition'},
            'attributes': ('jsonfield.fields.JSONField', [], {'default': '{}'}),
            'condition_type': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['achievement.ConditionType']"}),
            'description': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'event_type': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['services.Event']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'method': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['achievement.Method']"}),
            'qualifiers': ('django.db.models.fields.related.ManyToManyField', [], {'symmetrical': 'False', 'to': "orm['achievement.Qualifier']", 'null': 'True', 'blank': 'True'})
        },
        'achievement.badge': {
            'Meta': {'object_name': 'Badge'},
            'description': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '50'})
        },
        'achievement.conditiontype': {
            'Meta': {'object_name': 'ConditionType'},
            'custom': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'description': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'})
        },
        'achievement.customcondition': {
            'Meta': {'object_name': 'CustomCondition'},
            'condition_type': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['achievement.ConditionType']"}),
            'description': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'event_type': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['services.Event']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'method': ('django.db.models.fields.CharField', [], {'max_length': '100'})
        },
        'achievement.difficulty': {
            'Meta': {'ordering': "['points']", 'object_name': 'Difficulty'},
            'description': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '30'}),
            'points': ('django.db.models.fields.PositiveIntegerField', [], {})
        },
        'achievement.method': {
            'Meta': {'object_name': 'Method'},
            'argument_type': ('django.db.models.fields.CharField', [], {'max_length': '50', 'null': 'True', 'blank': 'True'}),
            'callablemethod': ('django.db.models.fields.CharField', [], {'max_length': '50'}),
            'description': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'})
        },
        'achievement.qualifier': {
            'Meta': {'object_name': 'Qualifier'},
            'argument_type': ('django.db.models.fields.CharField', [], {'max_length': '50', 'null': 'True', 'blank': 'True'}),
            'callablemethod': ('django.db.models.fields.CharField', [], {'max_length': '50'}),
            'description': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'return_type': ('django.db.models.fields.CharField', [], {'max_length': '50', 'null': 'True', 'blank': 'True'})
        },
        'achievement.quantifier': {
            'Meta': {'object_name': 'Quantifier'},
            'argument_type': ('django.db.models.fields.CharField', [], {'max_length': '50', 'null': 'True', 'blank': 'True'}),
            'callablemethod': ('django.db.models.fields.CharField', [], {'max_length': '50'}),
            'description': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'})
        },
        'achievement.userachievement': {
            'Meta': {'object_name': 'UserAchievement'},
            'achievement': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['achievement.Achievement']"}),
            'earned_at': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'user': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['achievement.UserProfile']"})
        },
        'achievement.userprofile': {
            'Meta': {'object_name': 'UserProfile'},
            'attributes': ('jsonfield.fields.JSONField', [], {'default': '{}'}),
            'badges': ('django.db.models.fields.related.ManyToManyField', [], {'blank': 'True', 'related_name': "'users'", 'null': 'True', 'symmetrical': 'False', 'to': "orm['achievement.Badge']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'moderator': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'points': ('django.db.models.fields.PositiveIntegerField', [], {'default': '0'}),
            'user': ('django.db.models.fields.related.OneToOneField', [], {'related_name': "'profile'", 'unique': 'True', 'to': u"orm['auth.User']"})
        },
        'achievement.valuecondition': {
            'Meta': {'object_name': 'ValueCondition'},
            'attribute': ('django.db.models.fields.CharField', [], {'max_length': '200'}),
            'condition_type': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['achievement.ConditionType']"}),
            'description': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'event_type': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['services.Event']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'method': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['achievement.Method']"}),
            'qualifier': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['achievement.Qualifier']", 'null': 'True', 'blank': 'True'}),
            'quantifier': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['achievement.Quantifier']", 'null': 'True', 'blank': 'True'}),
            'value': ('django.db.models.fields.CharField', [], {'max_length': '200'})
        },
        u'auth.group': {
            'Meta': {'object_name': 'Group'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '80'}),
            'permissions': ('django.db.models.fields.related.ManyToManyField', [], {'to': u"orm['auth.Permission']", 'symmetrical': 'False', 'blank': 'True'})
        },
        u'auth.permission': {
            'Meta': {'ordering': "(u'content_type__app_label', u'content_type__model', u'codename')", 'unique_together': "((u'content_type', u'codename'),)", 'object_name': 'Permission'},
            'codename': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'content_type': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['contenttypes.ContentType']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '50'})
        },
        u'auth.user': {
            'Meta': {'object_name': 'User'},
            'date_joined': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'email': ('django.db.models.fields.EmailField', [], {'max_length': '75', 'blank': 'True'}),
            'first_name': ('django.db.models.fields.CharField', [], {'max_length': '30', 'blank': 'True'}),
            'groups': ('django.db.models.fields.related.ManyToManyField', [], {'symmetrical': 'False', 'related_name': "u'user_set'", 'blank': 'True', 'to': u"orm['auth.Group']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_active': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'is_staff': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'is_superuser': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'last_login': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'last_name': ('django.db.models.fields.CharField', [], {'max_length': '30', 'blank': 'True'}),
            'password': ('django.db.models.fields.CharField', [], {'max_length': '128'}),
            'user_permissions': ('django.db.models.fields.related.ManyToManyField', [], {'symmetrical': 'False', 'related_name': "u'user_set'", 'blank': 'True', 'to': u"orm['auth.Permission']"}),
            'username': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '30'})
        },
        u'contenttypes.contenttype': {
            'Meta': {'ordering': "('name',)", 'unique_together': "(('app_label', 'model'),)", 'object_name': 'ContentType', 'db_table': "'django_content_type'"},
            'app_label': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'model': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'})
        },
        u'services.event': {
            'Meta': {'object_name': 'Event'},
            'attributes': ('jsonfield.fields.JSONField', [], {'default': '{}'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '90'}),
            'payload': ('jsonfield.fields.JSONField', [], {'default': '{}'}),
            'service': ('django.db.models.fields.CharField', [], {'max_length': '90'})
        }
    }

    complete_apps = ['achievement']