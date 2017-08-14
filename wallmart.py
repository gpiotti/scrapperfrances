from __future__ import print_function
import httplib2
import os
import time
import csv

from selenium import webdriver
from bs4 import BeautifulSoup
from string import replace, strip

from apiclient import discovery
from oauth2client import client
from oauth2client import tools
from oauth2client.file import Storage

from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains

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
    delay = 10

    try:
        driver = webdriver.PhantomJS(executable_path=r'E:\PhantomJs\bin\phantomjs.exe')
        wait = WebDriverWait(driver, delay)
        driver.set_window_size(1024, 768)
        print("Getting homepage...")
        driver.set_page_load_timeout(20)
        finished = 0
        while finished == 0:
            try:
                driver.get("http://www.walmart.com.ar/")
                finished = 1
            except:
                time.sleep(5)
        
        #time.sleep(delay)
        print("Clicking select store...")
        selectStore =  driver.find_element_by_xpath('/html/body/div[3]/div/header/div/nav/div/div[1]/ul/li[4]/span[1]')
        wait.until(EC.visibility_of(selectStore))
        selectStore.click()
        print("Clicking inputbox..")
        storeInputBox =  driver.find_element_by_xpath('//*[@id="select-store-container"]/section/section[2]/div[1]/div[2]/form[1]/input')
        wait.until(EC.visibility_of(storeInputBox))
        storeInputBox.click()
        print("Sending keys...")
        storeInputBox.send_keys("1611")
        storeInputBox.send_keys(Keys.RETURN)
        
        print("Clicking store name...")
        sucursal =  driver.find_element_by_xpath('//*[@id="select-store-container"]/section/section[2]/div[3]/div[2]/div')
        wait.until(EC.visibility_of(sucursal))
        sucursal.click()


        soup = BeautifulSoup(driver.page_source, 'html.parser')
        
        #rows = soup.find_all('td')
        date = time.strftime("%d/%m/%Y")
        categoriasSoup = soup.find_all('li', 'departamento-nome')
        categorias = []
        print ("Fetching categories...")
        for link in categoriasSoup:
            if "http://www.walmart.com.ar" + link.find('a')['href'] not in categorias:
                categorias.append("http://www.walmart.com.ar" + link.find('a')['href'])
        print("done. %s categories fetched" % len(categorias))    
        #driver.get("http://www.walmart.com.ar/aceites-y-aderezos")
        
        #categorias = categorias[:1]
        # allowed = [
        # u'http://www.walmart.com.ar/marroquineria',
        # u'http://www.walmart.com.ar/marroquineria',
        # ]
 
        # for  h  in range(1,10):
        #     for index, categoria in enumerate(categorias):
        #         if categoria not in allowed:
        #                 categorias.remove(categorias[index])
        #                 print ("removed %s" % categoria)
        
        # print(categorias)


        #link item soup.find("a" , "prateleira__flags")["href"]
        #descuento soup.find("span" ,"prateleira__discount")
        #precio comun -> soup.find("span" ,"prateleira__list-price--val")
        #precio promo -> soup.find("span", "prateleira__best-price")

        #descuento int(soup.find("span" ,"prateleira__discount").string[0:-1])
        
        print("Fetching pages...")
        for  categoria in categorias:
            q_ofertas = 0
            print("Categoria %s" % categoria )
            for j in range(1,5):
                
                try:
                    driver.set_window_size(1024, 768)
                    driver.set_page_load_timeout(20)
                    while finished == 0:
                        try:
                            driver.get(categoria)
                            finished = 1
                        except:
                            time.sleep(5)
                       
 
                    #time.sleep(delay)
                    driver.execute_script ("window.document.body.scrollTop = document.body.scrollHeight")
                    #time.sleep(delay*2)
                    soup = BeautifulSoup(driver.page_source, 'html.parser')
                    cantPaginas = soup.find('ul', 'pages').find_all('li')[-2].text
                except Exception as e:
                    if e.message == "list index out of range":
                        cantPaginas = 1
                        break
                    #print (e)
                    continue
                break
            try:
                int(cantPaginas)
            except Exception as e:
                cantPaginas = 1
            ofertas = []
            for i in range(1,int(cantPaginas)+1):
                print ("Buscando en pagina %s" % i)
                q_ofertas_pagina = 0
                retry = 0
                for j in range(1,5):
                    try:
                        print ("Fetching page %s of %s for %s" % (i,int(cantPaginas), categoria))
                        driver.execute_script ("window.document.body.scrollTop = document.body.scrollHeight")
                        #time.sleep(delay*2)
                        soup = BeautifulSoup(driver.page_source, 'html.parser')
                        all_items = soup.find("div", "prateleira prat-qtd n12colunas").find_all("li")
                    except Exception as e:
                        retry += 1
                        print ("Retrying %s times..." % str(retry))
                        #print (e)
                        #print (str(e.__class__.__name__))
                        #driver.save_screenshot('error.png');
                        continue
                    break
                    
                for item in all_items:
                    if item.find("span" ,"prateleira__discount") != None:
                        discount = int(item.find("span" ,"prateleira__discount").string[0:-1])
                        flag1 = item.find("div" , "prateleira__flags--discount-hightlight").text
                        flag2 = item.find("div" , "prateleira__flags--discount-hightlight").text
                        has_flag = flag1 + flag2
                        if len(has_flag) > 1: 
                            print("tiene flag")
                        if discount * -1 > 30 or len(has_flag) > 1:
                            ofertas.append([
                            str(item.find("a" , "prateleira__flags")["href"]), 
                            str(item.find("span" ,"prateleira__list-price--val").text),
                            str(item.find("span", "prateleira__best-price").text),
                            str(discount),
                            "pagina %s" % i
                            ])
                            q_ofertas_pagina += 1
                print ("Se econtraron %s ofertas nuevas" % str(q_ofertas_pagina))
                q_ofertas += q_ofertas_pagina

                if i < int(cantPaginas):
                    for j in range(1,5):
                        try:
                            print ("Trying to click page %s..." % str(i+1)  )
                            driver.execute_script ("window.document.body.scrollTop = document.body.scrollHeight")
                            time.sleep(1)
                            driver.execute_script ("window.document.body.scrollTop = -document.body.scrollHeight")
                            time.sleep(1)
                            driver.execute_script ("window.document.body.scrollTop = document.body.scrollHeight")
                            time.sleep(1)

                            nextPage = driver.find_element_by_xpath("//li[.='%s']" % str(i+1))
                            actions = ActionChains(driver)
                            actions.move_to_element(nextPage).perform()
                            
                            wait.until(EC.visibility_of(nextPage))
                            print ("Clicking page %s..." % str(i+1)  )
                            nextPage.click()
                            
                        except Exception as e:
                                print("Retrying %s times" % j)
                                #print (e.message)
                                #print (str(e.__class__.__name__))
                                #driver.save_screenshot('error.png');

                                continue
                        break          
            if q_ofertas > 0:
                print("Writting %s.csv..." % categoria.rsplit('/', 1)[-1])
                with open("%s.csv" % categoria.rsplit('/', 1)[-1] , "wb") as f:
                    writer = csv.writer(f, delimiter =';')
                    writer.writerows(ofertas)
           

    except Exception as e:
        print(e.message)
        print (str(e.__class__.__name__))
        driver.save_screenshot('out.png');



                      
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

