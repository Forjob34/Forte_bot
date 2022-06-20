import requests
from bs4 import BeautifulSoup
import time


def parser_one():
    url = 'http://lom.ugmet.ru'
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')
    table = soup.find('tbody')
    prices = table.find_all('tr', {'class': 'group-3'})
    format_one = prices[4].find_all('span')[0].text
    format_two = prices[5].find_all('span')[0].text
    format_fin_one = format_one[0] + ' ' + format_one[1:]
    format_fin_two = format_two[0] + ' ' + format_two[1:]
    res_one = prices[4].find('a').text + ' = ' + format_fin_one
    res_two = prices[5].find('a').text + ' = ' + format_fin_two

    return res_one, res_two


def parser_two():
    url = 'https://www.ferratek.com/price'
    r = requests.get(url)
    soup = BeautifulSoup(r.text, 'html.parser')
    table = soup.find(
        'div', {'id': 'block-views-block-glavnaya-vygruzka-block-1'})
    price_table = table.find_all('div', {'class': 'itemContent'})
    pr_1 = price_table[18].find('div', {'class': 'priceValue'}).text.replace(
        '.', '').replace('$', '')
    pr_2 = price_table[19].find('div', {'class': 'priceBlock'}).text.replace(
        '.', '').replace('$', '')
    # pr_1 = int(pr_1)
    # pr_2 = int(pr_2)
    # if len(str(pr_1)) == 2:
    #     pr_p = (int(pr_1)*100)
    # elif len(str(pr_1)) == 3:
    #     pr_p = (int(pr_1)*10)
    # if len(str(pr_2)) == 2:
    #     pr_p_2 = (int(pr_2)*100)
    # elif len(str(pr_2)) == 3:
    #     pr_p_2 = (int(pr_2)*10)
    # price_fin = str(pr_p)[0] + ' ' + str(pr_p)[1:]
    # price_fin_2 = str(pr_p_2)[0] + ' ' + str(pr_p_2)[1:]
    result_one = price_table[18].find(
        'div', {'class': 'name'}).text + ' = ' + pr_1
    result_two = price_table[19].find(
        'div', {'class': 'name'}).text + ' = ' + pr_2
    return result_one.replace('\n', ''), result_two.replace('\n', '')


def parser_three():
    url = 'http://ruslom61.ru/zakupka-cvetnikh-metallov'
    headers = {
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 11_4) AppleWebKit/537.36 '
        '(KHTML, like Gecko) Chrome/91.0.4472.114 Safari/537.36',

        'Referer': 'http://ruslom61.ru/zakupka-cvetnikh-metallov'
    }

    r = requests.get(url, headers=headers)

    soup = BeautifulSoup(r.text, 'html.parser')
    name_one = soup.find(
        'div', {'field': 'tn_text_1517135837648'}).text
    price_one = soup.find(
        'div', {'field': 'tn_text_1517135837666'}).text
    name_two = soup.find(
        'div', {'field': 'tn_text_1611217462203'}).text
    price_two = soup.find(
        'div', {'field': 'tn_text_1611217462218'}).text
    name_three = soup.find(
        'div', {'field': 'tn_text_1508830331449'}).text
    price_three = soup.find(
        'div', {'field': 'tn_text_1576859019141'}).text
    res_one = name_one.replace('\n', '') + ' = ' + price_one.replace('\n', '')
    res_two = name_two.replace('\n', '') + ' = ' + price_two.replace('\n', '')
    res_three = name_three.replace(
        '\n', '') + ' = ' + price_three.replace('\n', '')
    return res_one, res_two, res_three


if __name__ == '__main__':
    try:
        f_3 = parser_three()
        print(f_3)
    except Exception as e:
        print(e)
    try:
        f_1 = parser_one()
        print(f_1)
    except Exception as e:
        print(e)
    try:
        f_2 = parser_two()
        print(f_2)
    except Exception as e:
        print(e)
