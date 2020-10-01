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
    dbRecords = list(DaneArkusza.objects.values_list())
    sheetData = DaneArkusza.sheet.get_all_values()[1:]
    emptyRow = ('', '', '', '', '', '')
    elementCounter = 0
    #----------------------

    sheetElemsIDs = DaneArkusza.sheet.col_values(1)[1:]
    while '' in y:
        sheetElemsIDs.remove('')
    sheetElemsIDs = list(map(int, sheetElemsIDs))

    elem = 0
    for e in sheetElemsIDs:
        for i in dbRecords:
            if i != emptyRow:
                try:
                    dbRecords[x] = list(DaneArkusza.objects.filter(id=e).values_list()[0])
                    elem += 1
                    break
                except IndexError:
                    pass
            else:
                elem += 1
                continue

    #----------------------
    for i in sheetData:
        if i == ['', '', '', '', '', '']:
            dbRecords.insert(elementCounter, emptyRow)
            elementCounter += 1
        else:
            elementCounter += 1

    DaneArkusza.sheet.update('A2', dbRecords)
   
   
post_save.connect(updateSheet)


def deleteSheetData(sender, **kwargs):
    recordsId = list(DaneArkusza.objects.values_list('id', flat=True))
    idsFromSheet = DaneArkusza.sheet.col_values(1)[1:]
    while '' in idsFromSheet:
        idsFromSheet.remove('')

    idsFromSheet = list(map(int, idsFromSheet))
    difference = list(set(idsFromSheet) - set(recordsId))

    try:
        difference.remove('')
    except ValueError:
        pass

    try:
        foundDifferences = DaneArkusza.sheet.find(str(difference[0]))
        x = 'A' + str(foundDifferences.row)
        i = [['', '', '', '', '', '']]
        DaneArkusza.sheet.update(x, i)
    except IndexError:
        pass


post_delete.connect(deleteSheetData)

"""
def test(**kwargs):
    DaneArkusza.getDataFromSheet()

request_finished.connect(test)
"""

