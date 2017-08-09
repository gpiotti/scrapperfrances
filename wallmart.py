from __future__ import print_function
import httplib2
import os
import time

from selenium import webdriver
from bs4 import BeautifulSoup
from string import replace, strip

from apiclient import discovery
from oauth2client import client
from oauth2client import tools
from oauth2client.file import Storage

try:
    import argparse
    flags = argparse.ArgumentParser(parents=[tools.argparser]).parse_args()
except ImportError:
    flags = None

# If modifying these scopes, delete your previously saved credentials
# at ~/.credentials/sheets.googleapis.com-python-quickstart.json
SCOPES = 'https://www.googleapis.com/auth/spreadsheets'
CLIENT_SECRET_FILE = r'C:\Users\kingsun\workspace\scrapper\client_id.json'
APPLICATION_NAME = 'Google Sheets API Python Quickstart'


def get_credentials():
    """Gets valid user credentials from storage.

    If nothing has been stored, or if the stored credentials are invalid,
    the OAuth2 flow is completed to obtain the new credentials.

    Returns:
        Credentials, the obtained credential.
    """
    home_dir = os.path.expanduser('~')
    credential_dir = os.path.join(home_dir, '.credentials')
    if not os.path.exists(credential_dir):
        os.makedirs(credential_dir)
    credential_path = os.path.join(credential_dir,
                                   'sheets.googleapis.com-python-quickstart.json')

    store = Storage(credential_path)
    credentials = store.get()
    if not credentials or credentials.invalid:
        flow = client.flow_from_clientsecrets(CLIENT_SECRET_FILE, SCOPES)
        flow.user_agent = APPLICATION_NAME
        if flags:
            credentials = tools.run_flow(flow, store, flags)
        else: # Needed only for compatibility with Python 2.6
            credentials = tools.run(flow, store)
        print('Storing credentials to ' + credential_path)
    return credentials

def main(values):
    """Shows basic usage of the Sheets API.

    Creates a Sheets API service object and prints the names and majors of
    students in a sample spreadsheet:
    https://docs.google.com/spreadsheets/d/1BxiMVs0XRA5nFMdKvBdBZjgmUUqptlbs74OgvE2upms/edit
    """

    credentials = get_credentials()
    http = credentials.authorize(httplib2.Http())
    discoveryUrl = ('https://sheets.googleapis.com/$discovery/rest?'
                    'version=v4')
    service = discovery.build('sheets', 'v4', http=http,
                              discoveryServiceUrl=discoveryUrl)

    spreadsheetId = '1zgBWhjySjHctt33I6CVs49XNIxCEhJt4i8UDmMJ_FQg'
    rangeName = 'NamedRange1'

    payload = []
    payload.append(values)
    body = {
        'values': payload
    }

    result = service.spreadsheets().values().append(
        spreadsheetId=spreadsheetId, range=rangeName,
        valueInputOption='RAW', body=body).execute()


def getData():

    driver = webdriver.PhantomJS(executable_path=r'E:\PhantomJs\bin\phantomjs.exe')
    driver.get("http://www.walmart.com.ar/")
    # time.sleep(3)
    soup = BeautifulSoup(driver.page_source, 'html.parser')
    #rows = soup.find_all('td')
    date = time.strftime("%d/%m/%Y")
    categoriasSoup = soup.find_all('li', 'departamento-nome')
    categorias = []
    print ("Fetching categories...")
    for link in categoriasSoup:
        categorias.append("http://www.walmart.com.ar" + link.find('a')['href'])
    print("done. %s categories fetched" % len(categorias))    
    #driver.get("http://www.walmart.com.ar/aceites-y-aderezos")
    
    


    #link item soup.find("a" , "prateleira__flags")["href"]
    #descuento soup.find("span" ,"prateleira__discount")
    #precio comun -> soup.find("span" ,"prateleira__list-price--val")
    #precio promo -> soup.find("span", "prateleira__best-price")

    #descuento int(soup.find("span" ,"prateleira__discount").string[0:-1])
    ofertas = []
    print("Fetching pages...")
    for categoria in categorias:
        print("Categoria %s" % categoria )
        driver.set_window_size(1024, 768)
        driver.get(categoria)
        print(categoria)
        soup = BeautifulSoup(driver.page_source, 'html.parser')
        #time.sleep(10)

        cantPaginas = soup.find('ul', 'pages').find_all('li')[-2].text
        for i in range(1,int(cantPaginas)):
            print ("Fetching page %s of %s for %s" % (i,int(cantPaginas), categoria))
            driver.execute_script ("window.document.body.scrollTop = document.body.scrollHeight")
            time.sleep(20)
            soup = BeautifulSoup(driver.page_source, 'html.parser')
            all_items = soup.find("div", "prateleira prat-qtd n12colunas").find_all("ul")
            
            for item in all_items:
                if item.find("span" ,"prateleira__discount") != None:
                    discount = int(item.find("span" ,"prateleira__discount").string[0:-1])
                    if discount * -1 > 30:
                        ofertas.append([
                        item.find("a" , "prateleira__flags")["href"], 
                        item.find("span" ,"prateleira__list-price--val"),
                        item.find("span", "prateleira__best-price"),
                        discount
                        ])
            if i < int(cantPaginas):
                driver.execute_script ("window.document.body.scrollTop = document.body.scrollHeight")
                time.sleep(20)
                print ("Clicking page %s..." % str(i+1)  )
                driver.save_screenshot('out.png');
                driver.find_element_by_xpath("//li[.='%s']" % str(i+1)).click()
                time.sleep(5)
                
                
                


        #print("Ofertas encontradas...")
        for oferta in ofertas:
            print(oferta[0])  
        time.sleep(5)

                      
    # cotizaciones = [0] * 5
    # cotizaciones[0] = date

    # for row in rows:
    #     if strip(row.text) == 'FBA RenDoA':
    #         cotizaciones[1] = str(
    #             float(replace(row.findNext('td').findNext('td').findNext('td').text, ',', '.')) / 1000)
    #     elif strip(row.text) == 'FBA BonAA':
    #         cotizaciones[2] = str(
    #             float(replace(row.findNext('td').findNext('td').findNext('td').text, ',', '.')) / 1000)
    #     elif strip(row.text) == 'FBA AhorPA':
    #         cotizaciones[3] = str(
    #             float(replace(row.findNext('td').findNext('td').findNext('td').text, ',', '.')) / 1000)
    #     elif strip(row.text) == 'FBA CalifA':
    #         cotizaciones[4] = str(
    #             float(replace(row.findNext('td').findNext('td').findNext('td').text, ',', '.')) / 1000)

    #print(cotizaciones)
    driver.close()

    #main(ofertas)


if __name__ == '__main__':
 
        #print ("zzzz...")
        
    print("Starting...")
    getData()

