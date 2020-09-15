from django.db import models
from gsheets import mixins
from uuid import uuid4
from django.db.models.signals import post_save
from django.contrib.auth.models import User
from django.dispatch import receiver

class DaneArkusza(mixins.SheetSyncableMixin, models.Model):
    spreadsheet_id = '1uY7o0tmh8yFqlZucxeV8kriuo_ZOGF23pZSAXn30y9A'
    model_id_field = 'guid'
    sheet_name = 'ArkuszGoogle'
    sheet_id_field = 'id'

    guid = models.CharField(primary_key=True, max_length=255, default=uuid4, blank=True, editable=False)

    Imie = models.CharField(max_length=127, null=False)
    Nazwisko = models.CharField(max_length=127, null=False)
    Email = models.CharField(max_length=127, null=True, blank=True, default=None)
    Numer_telefonu = models.CharField(max_length=9, null=True, blank=True, default=None)
    Adres = models.CharField(max_length=127, null=True, blank=True, default=None)

    class Meta:
        verbose_name_plural = "Arkusz Google"

@receiver(post_save, sender = DaneArkusza)
def updateSheet(sender, **kwargs):
    DaneArkusza.push_to_sheet()