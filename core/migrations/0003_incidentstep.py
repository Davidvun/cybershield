# Generated by Django 5.2.4 on 2025-07-24 19:53

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0002_incident_affected_systems_incident_severity'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='IncidentStep',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('step', models.CharField(choices=[('triage', 'Initial Triage & Validation'), ('containment', 'Containment'), ('investigation', 'Investigation'), ('eradication', 'Eradication'), ('recovery', 'Recovery'), ('closure', 'Documentation & Closure')], max_length=20)),
                ('notes', models.TextField()),
                ('completed', models.BooleanField(default=False)),
                ('completed_at', models.DateTimeField(blank=True, null=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('incident', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='steps', to='core.incident')),
                ('responder', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'unique_together': {('incident', 'step')},
            },
        ),
    ]
