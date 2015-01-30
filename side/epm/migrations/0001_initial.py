# -*- coding: utf-8 -*-
from south.utils import datetime_utils as datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'party'
        db.create_table(u'epm_party', (
            ('party_id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('party_name', self.gf('django.db.models.fields.CharField')(unique=True, max_length=100)),
            ('party_attribute', self.gf('django.db.models.fields.IntegerField')(default=1)),
            ('member_number', self.gf('django.db.models.fields.IntegerField')(blank=True)),
            ('secretary_name', self.gf('django.db.models.fields.CharField')(max_length=50)),
            ('secretary_phone', self.gf('django.db.models.fields.CharField')(max_length=15)),
            ('responsible_name', self.gf('django.db.models.fields.CharField')(max_length=50)),
            ('responsible_phone', self.gf('django.db.models.fields.CharField')(max_length=15)),
            ('qq', self.gf('django.db.models.fields.CharField')(max_length=20, blank=True)),
            ('weixin', self.gf('django.db.models.fields.CharField')(max_length=20, blank=True)),
            ('party_email', self.gf('django.db.models.fields.EmailField')(max_length=75, blank=True)),
        ))
        db.send_create_signal(u'epm', ['party'])

        # Adding model 'enterprise'
        db.create_table(u'epm_enterprise', (
            ('enter_id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('enter_name', self.gf('django.db.models.fields.CharField')(max_length=50)),
            ('enter_address', self.gf('django.db.models.fields.CharField')(max_length=300)),
            ('enter_attribute', self.gf('django.db.models.fields.IntegerField')(default=1, blank=True)),
            ('industry_type', self.gf('django.db.models.fields.IntegerField')(default=1)),
            ('industry_nature', self.gf('django.db.models.fields.IntegerField')(default=1, blank=True)),
            ('enter_scale', self.gf('django.db.models.fields.IntegerField')(default=1, blank=True)),
            ('total_assets', self.gf('django.db.models.fields.IntegerField')(default=1, blank=True)),
            ('legal_person', self.gf('django.db.models.fields.CharField')(max_length=50)),
            ('legal_email', self.gf('django.db.models.fields.EmailField')(max_length=75)),
            ('enter_email', self.gf('django.db.models.fields.EmailField')(max_length=75, blank=True)),
            ('legal_phone', self.gf('django.db.models.fields.CharField')(max_length=50)),
            ('fixed_phone', self.gf('django.db.models.fields.CharField')(max_length=50, blank=True)),
            ('related_party', self.gf('django.db.models.fields.related.ForeignKey')(blank=True, related_name='enters', null=True, on_delete=models.SET_NULL, to=orm['epm.party'])),
        ))
        db.send_create_signal(u'epm', ['enterprise'])

        # Adding model 'member'
        db.create_table(u'epm_member', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('member_name', self.gf('django.db.models.fields.CharField')(max_length=80)),
            ('member_gender', self.gf('django.db.models.fields.IntegerField')(default=0)),
            ('member_nation', self.gf('django.db.models.fields.IntegerField')(default=1)),
            ('member_education', self.gf('django.db.models.fields.IntegerField')(default=0)),
            ('member_birth', self.gf('django.db.models.fields.DateField')(null=True, blank=True)),
            ('member_worktime', self.gf('django.db.models.fields.DateField')()),
            ('join_party_time', self.gf('django.db.models.fields.DateField')()),
            ('formal_member_time', self.gf('django.db.models.fields.DateField')(null=True, blank=True)),
            ('now_party_time', self.gf('django.db.models.fields.DateField')(null=True, blank=True)),
            ('birth_address', self.gf('django.db.models.fields.CharField')(max_length=100, null=True, blank=True)),
            ('home_address', self.gf('django.db.models.fields.CharField')(max_length=100, null=True, blank=True)),
            ('living_address', self.gf('django.db.models.fields.CharField')(max_length=100, null=True, blank=True)),
            ('member_phone', self.gf('django.db.models.fields.CharField')(max_length=11)),
            ('member_email', self.gf('django.db.models.fields.EmailField')(max_length=50)),
            ('qq', self.gf('django.db.models.fields.CharField')(max_length=15, null=True, blank=True)),
            ('weixin', self.gf('django.db.models.fields.CharField')(max_length=20, null=True, blank=True)),
            ('school', self.gf('django.db.models.fields.CharField')(max_length=80, null=True, blank=True)),
            ('id_card', self.gf('django.db.models.fields.CharField')(unique=True, max_length=30)),
            ('member_party', self.gf('django.db.models.fields.related.ForeignKey')(blank=True, related_name='membersAtParty', null=True, on_delete=models.SET_NULL, to=orm['epm.party'])),
            ('member_enter', self.gf('django.db.models.fields.related.ForeignKey')(blank=True, related_name='membersAtEnter', null=True, on_delete=models.SET_NULL, to=orm['epm.enterprise'])),
        ))
        db.send_create_signal(u'epm', ['member'])

        # Adding model 'UserProfile'
        db.create_table(u'epm_userprofile', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('user', self.gf('django.db.models.fields.related.ForeignKey')(related_name='app_user', unique=True, to=orm['auth.User'])),
            ('real_name', self.gf('django.db.models.fields.CharField')(max_length=40, null=True, blank=True)),
            ('real_idcard', self.gf('django.db.models.fields.CharField')(max_length=20, null=True, blank=True)),
            ('real_organization', self.gf('django.db.models.fields.CharField')(max_length=120, null=True, blank=True)),
            ('is_verified', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('is_manager', self.gf('django.db.models.fields.IntegerField')(default=0)),
        ))
        db.send_create_signal(u'epm', ['UserProfile'])

        # Adding model 'WorkUserProfile'
        db.create_table(u'epm_workuserprofile', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('user', self.gf('django.db.models.fields.related.ForeignKey')(related_name='worker', unique=True, to=orm['auth.User'])),
            ('has_published', self.gf('django.db.models.fields.IntegerField')(default=0)),
        ))
        db.send_create_signal(u'epm', ['WorkUserProfile'])

        # Adding model 'Pioneer'
        db.create_table(u'epm_pioneer', (
            ('pioneer_id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('title', self.gf('django.db.models.fields.CharField')(max_length=30)),
            ('date', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, blank=True)),
            ('author', self.gf('django.db.models.fields.CharField')(max_length=30)),
            ('content', self.gf('django.db.models.fields.TextField')()),
            ('int_date', self.gf('django.db.models.fields.IntegerField')(null=True, blank=True)),
        ))
        db.send_create_signal(u'epm', ['Pioneer'])

        # Adding model 'PioneerImage'
        db.create_table(u'epm_pioneerimage', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('content', self.gf('django.db.models.fields.related.ForeignKey')(related_name='img_list', to=orm['epm.Pioneer'])),
            ('pic', self.gf('django.db.models.fields.files.ImageField')(max_length=100, blank=True)),
        ))
        db.send_create_signal(u'epm', ['PioneerImage'])

        # Adding model 'LifeTips'
        db.create_table(u'epm_lifetips', (
            ('lifetips_id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('title', self.gf('django.db.models.fields.CharField')(max_length=30)),
            ('date', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, blank=True)),
            ('author', self.gf('django.db.models.fields.CharField')(max_length=30)),
            ('content', self.gf('django.db.models.fields.TextField')()),
            ('int_date', self.gf('django.db.models.fields.IntegerField')(null=True, blank=True)),
        ))
        db.send_create_signal(u'epm', ['LifeTips'])

        # Adding model 'LifeTipsImage'
        db.create_table(u'epm_lifetipsimage', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('content', self.gf('django.db.models.fields.related.ForeignKey')(related_name='img_list', to=orm['epm.LifeTips'])),
            ('pic', self.gf('django.db.models.fields.files.ImageField')(max_length=100, blank=True)),
        ))
        db.send_create_signal(u'epm', ['LifeTipsImage'])

        # Adding model 'PartyWork'
        db.create_table(u'epm_partywork', (
            ('partywork_id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('title', self.gf('django.db.models.fields.CharField')(max_length=30)),
            ('specified', self.gf('django.db.models.fields.IntegerField')(default=0)),
            ('date', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, blank=True)),
            ('author', self.gf('django.db.models.fields.CharField')(max_length=30)),
            ('content', self.gf('django.db.models.fields.TextField')()),
            ('int_date', self.gf('django.db.models.fields.IntegerField')(null=True, blank=True)),
        ))
        db.send_create_signal(u'epm', ['PartyWork'])

        # Adding M2M table for field specified_person on 'PartyWork'
        m2m_table_name = db.shorten_name(u'epm_partywork_specified_person')
        db.create_table(m2m_table_name, (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('partywork', models.ForeignKey(orm[u'epm.partywork'], null=False)),
            ('member', models.ForeignKey(orm[u'epm.member'], null=False))
        ))
        db.create_unique(m2m_table_name, ['partywork_id', 'member_id'])

        # Adding model 'PartyWorkImage'
        db.create_table(u'epm_partyworkimage', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('content', self.gf('django.db.models.fields.related.ForeignKey')(related_name='img_list', to=orm['epm.PartyWork'])),
            ('pic', self.gf('django.db.models.fields.files.ImageField')(max_length=100, blank=True)),
        ))
        db.send_create_signal(u'epm', ['PartyWorkImage'])

        # Adding model 'Notice'
        db.create_table(u'epm_notice', (
            ('notice_id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('title', self.gf('django.db.models.fields.CharField')(max_length=30)),
            ('date', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, blank=True)),
            ('author', self.gf('django.db.models.fields.CharField')(max_length=30)),
            ('content', self.gf('django.db.models.fields.TextField')()),
            ('int_date', self.gf('django.db.models.fields.IntegerField')(null=True, blank=True)),
        ))
        db.send_create_signal(u'epm', ['Notice'])

        # Adding model 'NoticeImage'
        db.create_table(u'epm_noticeimage', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('content', self.gf('django.db.models.fields.related.ForeignKey')(related_name='img_list', to=orm['epm.Notice'])),
            ('pic', self.gf('django.db.models.fields.files.ImageField')(max_length=100, blank=True)),
        ))
        db.send_create_signal(u'epm', ['NoticeImage'])

        # Adding model 'Spirit'
        db.create_table(u'epm_spirit', (
            ('spirit_id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('title', self.gf('django.db.models.fields.CharField')(max_length=30)),
            ('date', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, blank=True)),
            ('author', self.gf('django.db.models.fields.CharField')(max_length=30)),
            ('content', self.gf('django.db.models.fields.TextField')()),
            ('int_date', self.gf('django.db.models.fields.IntegerField')(null=True, blank=True)),
        ))
        db.send_create_signal(u'epm', ['Spirit'])

        # Adding model 'SpiritImage'
        db.create_table(u'epm_spiritimage', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('content', self.gf('django.db.models.fields.related.ForeignKey')(related_name='img_list', to=orm['epm.Spirit'])),
            ('pic', self.gf('django.db.models.fields.files.ImageField')(max_length=100, blank=True)),
        ))
        db.send_create_signal(u'epm', ['SpiritImage'])

        # Adding model 'Policy'
        db.create_table(u'epm_policy', (
            ('policy_id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('title', self.gf('django.db.models.fields.CharField')(max_length=30)),
            ('date', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, blank=True)),
            ('author', self.gf('django.db.models.fields.CharField')(max_length=30)),
            ('content', self.gf('django.db.models.fields.TextField')()),
            ('int_date', self.gf('django.db.models.fields.IntegerField')(null=True, blank=True)),
        ))
        db.send_create_signal(u'epm', ['Policy'])

        # Adding model 'PolicyImage'
        db.create_table(u'epm_policyimage', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('content', self.gf('django.db.models.fields.related.ForeignKey')(related_name='img_list', to=orm['epm.Policy'])),
            ('pic', self.gf('django.db.models.fields.files.ImageField')(max_length=100, blank=True)),
        ))
        db.send_create_signal(u'epm', ['PolicyImage'])

        # Adding model 'BusinessProcess'
        db.create_table(u'epm_businessprocess', (
            ('process_id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('title', self.gf('django.db.models.fields.CharField')(max_length=30)),
            ('date', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, blank=True)),
            ('process_type', self.gf('django.db.models.fields.CharField')(default='join', max_length=10)),
            ('author', self.gf('django.db.models.fields.CharField')(max_length=30)),
            ('content', self.gf('django.db.models.fields.TextField')()),
        ))
        db.send_create_signal(u'epm', ['BusinessProcess'])

        # Adding model 'Question'
        db.create_table(u'epm_question', (
            ('question_id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('question_title', self.gf('django.db.models.fields.CharField')(default=u'\u95ee\u9898\u54a8\u8be2', max_length=30)),
            ('create_time', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, blank=True)),
            ('reply_time', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, blank=True)),
            ('create_int', self.gf('django.db.models.fields.IntegerField')(default=1421998118, null=True, blank=True)),
            ('reply_int', self.gf('django.db.models.fields.IntegerField')(default=1421998118, null=True, blank=True)),
            ('question_author', self.gf('django.db.models.fields.CharField')(max_length='40')),
            ('question_type', self.gf('django.db.models.fields.IntegerField')(default=0)),
            ('question_content', self.gf('django.db.models.fields.TextField')()),
            ('question_answer', self.gf('django.db.models.fields.TextField')(null=True, blank=True)),
            ('is_published', self.gf('django.db.models.fields.BooleanField')(default=False)),
        ))
        db.send_create_signal(u'epm', ['Question'])


    def backwards(self, orm):
        # Deleting model 'party'
        db.delete_table(u'epm_party')

        # Deleting model 'enterprise'
        db.delete_table(u'epm_enterprise')

        # Deleting model 'member'
        db.delete_table(u'epm_member')

        # Deleting model 'UserProfile'
        db.delete_table(u'epm_userprofile')

        # Deleting model 'WorkUserProfile'
        db.delete_table(u'epm_workuserprofile')

        # Deleting model 'Pioneer'
        db.delete_table(u'epm_pioneer')

        # Deleting model 'PioneerImage'
        db.delete_table(u'epm_pioneerimage')

        # Deleting model 'LifeTips'
        db.delete_table(u'epm_lifetips')

        # Deleting model 'LifeTipsImage'
        db.delete_table(u'epm_lifetipsimage')

        # Deleting model 'PartyWork'
        db.delete_table(u'epm_partywork')

        # Removing M2M table for field specified_person on 'PartyWork'
        db.delete_table(db.shorten_name(u'epm_partywork_specified_person'))

        # Deleting model 'PartyWorkImage'
        db.delete_table(u'epm_partyworkimage')

        # Deleting model 'Notice'
        db.delete_table(u'epm_notice')

        # Deleting model 'NoticeImage'
        db.delete_table(u'epm_noticeimage')

        # Deleting model 'Spirit'
        db.delete_table(u'epm_spirit')

        # Deleting model 'SpiritImage'
        db.delete_table(u'epm_spiritimage')

        # Deleting model 'Policy'
        db.delete_table(u'epm_policy')

        # Deleting model 'PolicyImage'
        db.delete_table(u'epm_policyimage')

        # Deleting model 'BusinessProcess'
        db.delete_table(u'epm_businessprocess')

        # Deleting model 'Question'
        db.delete_table(u'epm_question')


    models = {
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
        u'epm.businessprocess': {
            'Meta': {'object_name': 'BusinessProcess'},
            'author': ('django.db.models.fields.CharField', [], {'max_length': '30'}),
            'content': ('django.db.models.fields.TextField', [], {}),
            'date': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'process_id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'process_type': ('django.db.models.fields.CharField', [], {'default': "'join'", 'max_length': '10'}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '30'})
        },
        u'epm.enterprise': {
            'Meta': {'object_name': 'enterprise'},
            'enter_address': ('django.db.models.fields.CharField', [], {'max_length': '300'}),
            'enter_attribute': ('django.db.models.fields.IntegerField', [], {'default': '1', 'blank': 'True'}),
            'enter_email': ('django.db.models.fields.EmailField', [], {'max_length': '75', 'blank': 'True'}),
            'enter_id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'enter_name': ('django.db.models.fields.CharField', [], {'max_length': '50'}),
            'enter_scale': ('django.db.models.fields.IntegerField', [], {'default': '1', 'blank': 'True'}),
            'fixed_phone': ('django.db.models.fields.CharField', [], {'max_length': '50', 'blank': 'True'}),
            'industry_nature': ('django.db.models.fields.IntegerField', [], {'default': '1', 'blank': 'True'}),
            'industry_type': ('django.db.models.fields.IntegerField', [], {'default': '1'}),
            'legal_email': ('django.db.models.fields.EmailField', [], {'max_length': '75'}),
            'legal_person': ('django.db.models.fields.CharField', [], {'max_length': '50'}),
            'legal_phone': ('django.db.models.fields.CharField', [], {'max_length': '50'}),
            'related_party': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'enters'", 'null': 'True', 'on_delete': 'models.SET_NULL', 'to': u"orm['epm.party']"}),
            'total_assets': ('django.db.models.fields.IntegerField', [], {'default': '1', 'blank': 'True'})
        },
        u'epm.lifetips': {
            'Meta': {'object_name': 'LifeTips'},
            'author': ('django.db.models.fields.CharField', [], {'max_length': '30'}),
            'content': ('django.db.models.fields.TextField', [], {}),
            'date': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'int_date': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'lifetips_id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '30'})
        },
        u'epm.lifetipsimage': {
            'Meta': {'object_name': 'LifeTipsImage'},
            'content': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'img_list'", 'to': u"orm['epm.LifeTips']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'pic': ('django.db.models.fields.files.ImageField', [], {'max_length': '100', 'blank': 'True'})
        },
        u'epm.member': {
            'Meta': {'object_name': 'member'},
            'birth_address': ('django.db.models.fields.CharField', [], {'max_length': '100', 'null': 'True', 'blank': 'True'}),
            'formal_member_time': ('django.db.models.fields.DateField', [], {'null': 'True', 'blank': 'True'}),
            'home_address': ('django.db.models.fields.CharField', [], {'max_length': '100', 'null': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'id_card': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '30'}),
            'join_party_time': ('django.db.models.fields.DateField', [], {}),
            'living_address': ('django.db.models.fields.CharField', [], {'max_length': '100', 'null': 'True', 'blank': 'True'}),
            'member_birth': ('django.db.models.fields.DateField', [], {'null': 'True', 'blank': 'True'}),
            'member_education': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'member_email': ('django.db.models.fields.EmailField', [], {'max_length': '50'}),
            'member_enter': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'membersAtEnter'", 'null': 'True', 'on_delete': 'models.SET_NULL', 'to': u"orm['epm.enterprise']"}),
            'member_gender': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'member_name': ('django.db.models.fields.CharField', [], {'max_length': '80'}),
            'member_nation': ('django.db.models.fields.IntegerField', [], {'default': '1'}),
            'member_party': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'membersAtParty'", 'null': 'True', 'on_delete': 'models.SET_NULL', 'to': u"orm['epm.party']"}),
            'member_phone': ('django.db.models.fields.CharField', [], {'max_length': '11'}),
            'member_worktime': ('django.db.models.fields.DateField', [], {}),
            'now_party_time': ('django.db.models.fields.DateField', [], {'null': 'True', 'blank': 'True'}),
            'qq': ('django.db.models.fields.CharField', [], {'max_length': '15', 'null': 'True', 'blank': 'True'}),
            'school': ('django.db.models.fields.CharField', [], {'max_length': '80', 'null': 'True', 'blank': 'True'}),
            'weixin': ('django.db.models.fields.CharField', [], {'max_length': '20', 'null': 'True', 'blank': 'True'})
        },
        u'epm.notice': {
            'Meta': {'object_name': 'Notice'},
            'author': ('django.db.models.fields.CharField', [], {'max_length': '30'}),
            'content': ('django.db.models.fields.TextField', [], {}),
            'date': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'int_date': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'notice_id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '30'})
        },
        u'epm.noticeimage': {
            'Meta': {'object_name': 'NoticeImage'},
            'content': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'img_list'", 'to': u"orm['epm.Notice']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'pic': ('django.db.models.fields.files.ImageField', [], {'max_length': '100', 'blank': 'True'})
        },
        u'epm.party': {
            'Meta': {'object_name': 'party'},
            'member_number': ('django.db.models.fields.IntegerField', [], {'blank': 'True'}),
            'party_attribute': ('django.db.models.fields.IntegerField', [], {'default': '1'}),
            'party_email': ('django.db.models.fields.EmailField', [], {'max_length': '75', 'blank': 'True'}),
            'party_id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'party_name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '100'}),
            'qq': ('django.db.models.fields.CharField', [], {'max_length': '20', 'blank': 'True'}),
            'responsible_name': ('django.db.models.fields.CharField', [], {'max_length': '50'}),
            'responsible_phone': ('django.db.models.fields.CharField', [], {'max_length': '15'}),
            'secretary_name': ('django.db.models.fields.CharField', [], {'max_length': '50'}),
            'secretary_phone': ('django.db.models.fields.CharField', [], {'max_length': '15'}),
            'weixin': ('django.db.models.fields.CharField', [], {'max_length': '20', 'blank': 'True'})
        },
        u'epm.partywork': {
            'Meta': {'object_name': 'PartyWork'},
            'author': ('django.db.models.fields.CharField', [], {'max_length': '30'}),
            'content': ('django.db.models.fields.TextField', [], {}),
            'date': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'int_date': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'partywork_id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'specified': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'specified_person': ('django.db.models.fields.related.ManyToManyField', [], {'symmetrical': 'False', 'to': u"orm['epm.member']", 'null': 'True', 'blank': 'True'}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '30'})
        },
        u'epm.partyworkimage': {
            'Meta': {'object_name': 'PartyWorkImage'},
            'content': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'img_list'", 'to': u"orm['epm.PartyWork']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'pic': ('django.db.models.fields.files.ImageField', [], {'max_length': '100', 'blank': 'True'})
        },
        u'epm.pioneer': {
            'Meta': {'object_name': 'Pioneer'},
            'author': ('django.db.models.fields.CharField', [], {'max_length': '30'}),
            'content': ('django.db.models.fields.TextField', [], {}),
            'date': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'int_date': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'pioneer_id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '30'})
        },
        u'epm.pioneerimage': {
            'Meta': {'object_name': 'PioneerImage'},
            'content': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'img_list'", 'to': u"orm['epm.Pioneer']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'pic': ('django.db.models.fields.files.ImageField', [], {'max_length': '100', 'blank': 'True'})
        },
        u'epm.policy': {
            'Meta': {'object_name': 'Policy'},
            'author': ('django.db.models.fields.CharField', [], {'max_length': '30'}),
            'content': ('django.db.models.fields.TextField', [], {}),
            'date': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'int_date': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'policy_id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '30'})
        },
        u'epm.policyimage': {
            'Meta': {'object_name': 'PolicyImage'},
            'content': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'img_list'", 'to': u"orm['epm.Policy']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'pic': ('django.db.models.fields.files.ImageField', [], {'max_length': '100', 'blank': 'True'})
        },
        u'epm.question': {
            'Meta': {'object_name': 'Question'},
            'create_int': ('django.db.models.fields.IntegerField', [], {'default': '1421998118', 'null': 'True', 'blank': 'True'}),
            'create_time': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'is_published': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'question_answer': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'question_author': ('django.db.models.fields.CharField', [], {'max_length': "'40'"}),
            'question_content': ('django.db.models.fields.TextField', [], {}),
            'question_id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'question_title': ('django.db.models.fields.CharField', [], {'default': "u'\\u95ee\\u9898\\u54a8\\u8be2'", 'max_length': '30'}),
            'question_type': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'reply_int': ('django.db.models.fields.IntegerField', [], {'default': '1421998118', 'null': 'True', 'blank': 'True'}),
            'reply_time': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'})
        },
        u'epm.spirit': {
            'Meta': {'object_name': 'Spirit'},
            'author': ('django.db.models.fields.CharField', [], {'max_length': '30'}),
            'content': ('django.db.models.fields.TextField', [], {}),
            'date': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'int_date': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'spirit_id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '30'})
        },
        u'epm.spiritimage': {
            'Meta': {'object_name': 'SpiritImage'},
            'content': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'img_list'", 'to': u"orm['epm.Spirit']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'pic': ('django.db.models.fields.files.ImageField', [], {'max_length': '100', 'blank': 'True'})
        },
        u'epm.userprofile': {
            'Meta': {'object_name': 'UserProfile'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_manager': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'is_verified': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'real_idcard': ('django.db.models.fields.CharField', [], {'max_length': '20', 'null': 'True', 'blank': 'True'}),
            'real_name': ('django.db.models.fields.CharField', [], {'max_length': '40', 'null': 'True', 'blank': 'True'}),
            'real_organization': ('django.db.models.fields.CharField', [], {'max_length': '120', 'null': 'True', 'blank': 'True'}),
            'user': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'app_user'", 'unique': 'True', 'to': u"orm['auth.User']"})
        },
        u'epm.workuserprofile': {
            'Meta': {'object_name': 'WorkUserProfile'},
            'has_published': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'user': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'worker'", 'unique': 'True', 'to': u"orm['auth.User']"})
        }
    }

    complete_apps = ['epm']