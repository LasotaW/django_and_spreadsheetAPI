from django.db import models
from django.db.models.signals import post_save, post_delete
from django.core.signals import request_finished
from oauth2client.service_account import ServiceAccountCredentials
import gspread

class DaneArkusza(models.Model):
    scope = ['https://spreadsheets.google.com/feeds', 'https://www.googleapis.com/auth/drive']
    creds = ServiceAccountCredentials.from_json_keyfile_name('credentials.json', scope)
    client = gspread.authorize(creds)
    sheet = client.open("tut").sheet1

    Imie = models.CharField(max_length=127, null=False)
    Nazwisko = models.CharField(max_length=127, null=False)
    Email = models.CharField(max_length=127, null=True, blank=True, default=None)
    Numer_telefonu = models.CharField(max_length=9, null=True, blank=True, default=None)
    Adres = models.CharField(max_length=127, null=True, blank=True, default=None)

    def __str__(self):
        return f'{self.Imie} | {self.Nazwisko} | {self.Email} | {self.Numer_telefonu} | {self.Adres}'

    class Meta:
        verbose_name_plural = "Arkusz Google"


    def getDataFromSheet():
        post_save.disconnect(updateSheet)
        sheetData = DaneArkusza.sheet.get_all_values()[1:]
        emptyRow = ['', '', '', '', '', '']
        while emptyRow in sheetData:
            sheetData.remove(emptyRow)
            
        try:
            for i in sheetData:
                if i[0] =='':
                    record = DaneArkusza(
                        Imie = i[1],
                        Nazwisko = i[2],
                        Email = i[3],
                        Numer_telefonu = i[4],
                        Adres = i[5]
                    )
                    record.save()
                else:
                    record = DaneArkusza(
                        id = i[0],
                        Imie = i[1],
                        Nazwisko = i[2],
                        Email = i[3],
                        Numer_telefonu = i[4],
                        Adres = i[5]
                    )
                    record.save()
        except IndexError:
            pass
        
        updateSheet(DaneArkusza)
        post_save.connect(updateSheet)


class Faktura(models.Model):
    Klient = models.ForeignKey(DaneArkusza, on_delete=models.CASCADE, related_name='klient')
    Sprzedawca = models.ForeignKey(DaneArkusza, on_delete=models.CASCADE, related_name='sprzedawca')
    Kwota_faktury = models.IntegerField()
    Data_wystawienia = models.DateField()
    Opłacona = models.BooleanField()

    class Meta:
        verbose_name_plural = "Faktury"

    def __str__(self):
        return f'Faktura {self.id}'


def updateSheet(sender, **kwargs):
    data = list(DaneArkusza.objects.values_list())
    sheetData = DaneArkusza.sheet.get_all_values()[1:]
    emptyRowAsTuple = ('', '', '', '', '', '')
    elementCounter = 0
    for i in sheetData:
        if i == ['', '', '', '', '', '']:
            data.insert(elementCounter, emptyRowAsTuple)
            elementCounter += 1
        else:
            elementCounter += 1

    DaneArkusza.sheet.update('A2', data)
post_save.connect(updateSheet)


def deleteSheetData(sender, **kwargs):
    dbRecords = list(DaneArkusza.objects.values_list('id', flat=True))
    sheetData = DaneArkusza.sheet.col_values(1)[1:]
    while '' in sheetData:
        sheetData.remove('')
    sheetData = list(map(int, sheetData))
    difference = list(set(sheetData) - set(dbRecords))
    try:
        difference.remove('')
    except ValueError:
        pass
    try:
        foundDifferences = DaneArkusza.sheet.find(str(difference[0]))
        DaneArkusza.sheet.delete_row(foundDifferences.row)
    except IndexError:
        pass

post_delete.connect(deleteSheetData)

"""
def test(**kwargs):
    DaneArkusza.getDataFromSheet()

request_finished.connect(test)
"""

