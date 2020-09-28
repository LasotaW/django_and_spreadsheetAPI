from django.db import models
from django.db.models.signals import post_save, post_delete
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
        x = DaneArkusza.sheet.get_all_values()[1:]
        try:
            for i in x:
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


def updateSheet(sender, **kwargs):
    data = list(DaneArkusza.objects.values_list())
    DaneArkusza.sheet.update('A2',data)

post_save.connect(updateSheet)


def deleteSheetData(sender, **kwargs):
    print("USUWAMY")
    x = list(DaneArkusza.objects.values_list('id', flat=True))
    y = DaneArkusza.sheet.col_values(1)[1:]
    while '' in y:
        y.remove('')
    y = list(map(int, y))
    a = list(set(y) - set(x))
    try:
        a.remove('')
    except ValueError:
        pass
   
    z = DaneArkusza.sheet.find(str(a[0]))
    DaneArkusza.sheet.delete_row(z.row)

post_delete.connect(deleteSheetData)


"""
TODO
class Faktura(models.Model):
    id = models.AutoField()
    Klient = models.ForeignKey()
    Sprzedawca = models.ForeignKey()
    Kwota_faktury = models.IntegerField()
    Data_wystawienia = models.DateField()
    Opłacona = models.BooleanField()

"""