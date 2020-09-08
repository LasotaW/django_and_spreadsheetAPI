from django.shortcuts import render
import gspread
from oauth2client.service_account import ServiceAccountCredentials

def index(request):
    scope = ['https://spreadsheets.google.com/feeds', 'https://www.googleapis.com/auth/drive']
    creds = ServiceAccountCredentials.from_json_keyfile_name('credentials.json', scope)
    client = gspread.authorize(creds)

    sheet = client.open("SheetCopy").sheet1

    kontekst = {
            'cell':sheet.get_all_values(),
        }

    return render(request, 'index.html', kontekst)