from django.db import models
from gsheets import mixins
from uuid import uuid4

class DaneArkusza(mixins.SheetPushableMixin, models.Model):
    spreadsheet_id = '1uY7o0tmh8yFqlZucxeV8kriuo_ZOGF23pZSAXn30y9A'
    model_id_field = 'guid'
    sheet_name = 'ArkuszGoogle'
    sheet_id_field = 'id'

    guid = models.CharField(primary_key=True, max_length=255, default=uuid4)

    Imie = models.CharField(max_length=127, )
    Nazwisko = models.CharField(max_length=127)
    Email = models.CharField(max_length=127, null=True, blank=True, default=None)
    Numer_telefonu = models.CharField(max_length=9, null=True, blank=True, default=None)
    Adres = models.CharField(max_length=127, null=True, blank=True, default=None)

    def __str__(self):
        return f'{self.Imie} {self.Nazwisko} // {self.Email} {self.Numer_telefonu} {self.Adres} ({self.guid})'


    class Meta:
        verbose_name_plural = 'Dane'