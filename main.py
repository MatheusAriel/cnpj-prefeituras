"""
Script feito para pegar todos os cnpjs de prefeituras cdastradas no cnes2
"""
import requests
from bs4 import BeautifulSoup
import traceback

z = 1

def estados(url, file):
    try:
        url1 = ('https://cnes2.datasus.gov.br/' + url['href']).replace(' ', '')
        response1 = requests.get(url1)

        html1 = BeautifulSoup(response1.text, 'html.parser')
        table1 = html1.findAll("table")

        for url in table1[4].find_all('a', href=True):
            municipios(url, file)

    except:
        print('ERRO LISTA MUNICIPIOS ESTADOS', traceback.print_exc(), '\n')
        pass


def municipios(url, file):
    link_completo = ('https://cnes2.datasus.gov.br/' + url['href']).replace(' ', '')
    response2 = requests.get(link_completo)

    html2 = BeautifulSoup(response2.text, 'html.parser')
    table2 = html2.findAll("table")

    try:
        for url in table2[4].find_all('a', href=True):
            prefeituras(url, file)
    except:
        print('ERRO LISTA DE MUNICIPIOS', traceback.print_exc(), '\n')
        pass


def prefeituras(url, file):
    url = ('https://cnes2.datasus.gov.br/' + url['href']).replace(' ', '')
    if ('PREFEITURA' in url or 'PREF' in url or 'MUNICIPIO' in url) and 'FUNDO' not in url:
        try:
            global z
            print(url, z)
            z += 1
            response3 = requests.get(url)
            html3 = BeautifulSoup(response3.text, 'html.parser')
            table3 = html3.findAll("table")

            i = 0

            nome = cnpj = endereco = numero = complemento = cidade = bairro = cep = uf = ''
            for row in table3[4].findAll("tr"):
                if i == 1:
                    cnpj = row.findAll('font')[1].text
                elif i == 3:
                    endereco = row.findAll('td')[0].text.strip('\n').strip('\t')
                    numero = row.findAll('td')[1].text.strip('\n').strip('\t')
                    complemento = row.findAll('td')[2].text.strip('\n').strip('\t')
                    bairro = row.findAll('td')[3].text.strip('\n').strip('\t')
                elif i == 5:
                    cidade = row.findAll('td')[0].text.replace('\n', '')
                    nome = f"PREFEITURA MUNICIPAL DE {cidade}"
                    cep = row.findAll('td')[1].text.strip('\n').strip('\t')
                    uf = row.findAll('td')[2].text.strip('\n').strip('\t')

                    file.write(f"{nome};{nome};{cnpj};{endereco};{numero};{complemento};"
                               f"{bairro};{cidade};{cep};{uf}\n")
                    break
                i += 1
        except:
            print('ERRO AO OBTER DADOS DA PREFEITURA', traceback.print_exc(), '\n')
            pass

def get_prefeituras():
    with open('prefeituras.csv', 'w+', encoding='UTF8', newline='') as file:
        url0 = 'https://cnes2.datasus.gov.br/Lista_Tot_Es_Estado_Mantenedora.asp'
        response0 = requests.get(url0)
        html0 = BeautifulSoup(response0.text, 'html.parser')
        table0 = html0.findAll("table")

        for links0 in table0[4].find_all('a', href=True):
            estados(links0, file)


if __name__ == '__main__':
    get_prefeituras()
