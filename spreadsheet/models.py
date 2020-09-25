from django.db import models
from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
from oauth2client.service_account import ServiceAccountCredentials
import gspread


class DaneArkusza(models.Model):
    scope = ['https://spreadsheets.google.com/feeds', 'https://www.googleapis.com/auth/drive']
    creds = ServiceAccountCredentials.from_json_keyfile_name('credentials.json', scope)
    client = gspread.authorize(creds)
    sheet = client.open("tut").sheet1

    Imie = models.CharField(max_length=127, null=False, primary_key=True)
    Nazwisko = models.CharField(max_length=127, null=False)
    Email = models.CharField(max_length=127, null=True, blank=True, default=None)
    Numer_telefonu = models.CharField(max_length=9, null=True, blank=True, default=None)
    Adres = models.CharField(max_length=127, null=True, blank=True, default=None)

    def __str__(self):
        return f'{self.Imie} | {self.Nazwisko} | {self.Email} | {self.Numer_telefonu} | {self.Adres}'

    class Meta:
        verbose_name_plural = "Arkusz Google"


    def getDataFromSheet():
        x = DaneArkusza.sheet.get_all_values()[1:]
        for i in x:
            record = DaneArkusza(
            Imie = i[0],
            Nazwisko = i[1],
            Email = i[2],
            Numer_telefonu = i[3],
            Adres = i[4]
            )
            record.save()

@receiver(post_save, sender = DaneArkusza)
def updateSheet(sender, **kwargs):
   data = list(DaneArkusza.objects.values_list())
   DaneArkusza.sheet.update('A2',data)

@receiver(post_delete, sender = DaneArkusza)
def deleteSheetData(sender, **kwargs):
    DaneArkusza.sheet.delete_row(2)

