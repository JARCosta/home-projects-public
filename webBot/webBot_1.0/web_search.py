import os
import time
import csv
import sys
import json
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from datetime import datetime
from difflib import SequenceMatcher

def get_index(weapon_name):
    with open('indexs.json', 'r') as openfile:
        indexes = json.load(openfile)
    for i in indexes:
        if(SequenceMatcher(None, i[1].lower(), weapon_name.lower()).ratio() > 0.75):
            return i
    return None


URL = "https://csgofloat.com/db?defIndex=7&category=3&order=4&min=0.351&max=0.352"
def get_url(weapon_name):
    URL_domain = URL[:34]
    URL_filters = URL[35:]
    return URL_domain + str(get_index(weapon_name)[0]) + URL_filters


def open_browser():
    options = Options()
    options.add_argument("user-data-dir=/tmp/tarun")
    chrome = webdriver.Chrome(options=options)
    return chrome

def open_url(browser, url):
    browser.get(url)


def close_browser(browser):
    browser.quit()


def read_line(browser, number):
    xpath = "/html/body/app-root/div/div[2]/app-float-db/div/div/app-float-dbtable/div/div/table/tbody/tr[" + str(number) + "]/td"
    line = browser.find_elements(By.XPATH, xpath)
    ret = [line[0].text[1:],line[1].text.split("\n")[0].split(" ")[1], line[1].text.split("\n")[1], line[2].text[:-3], line[3].text]
    try:
        link = str(line[5].find_element(By.XPATH, (xpath + "[7]/div/span/a")).get_attribute("href"))
    except:
        link = str(line[5].find_element(By.XPATH, (xpath + "[7]/div/app-steam-avatar/a")).get_attribute("href"))
    try:
        price = line[10].find_element(By.XPATH, (xpath + "[11]/div/span")).text
    except:
        price = ""
    ret += [link, price]
    return ret


def read_page(browser):
    table = []
    for i in range(30):
        try:
            table.append(read_line(browser, 1))
            print("item 1 loaded")
            break
        except:
            print("item 1 not found")
            time.sleep(1)
            continue
    i = 2
    while True:
        try:
            table.append(read_line(browser, i))
            print("item", i, "loaded")
            i += 1
            continue
        except:
            print("reached end of page")
            break
    return table


def save_csv(flag, table, weapon_name):
    with open("outs/" + weapon_name + '.csv', mode=flag) as employee_file:
        employee_writer = csv.writer(employee_file, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
        employee_writer.writerow([datetime.now().strftime("%d/%m/%Y %H:%M:%S"),])
        for i in table:
            employee_writer.writerow(i)
        for i in range(3):
            employee_writer.writerow([])




def main(LOGIN, flag, table):
    browser = open_browser()
    if LOGIN == "True":
        open_url(browser,URL)
        input("press return to resume:")
    #table = sys.argv[2:]
    for weapon_name in table:
        url = get_url(weapon_name)
        open_url(browser, url)
        start = datetime.now().strftime("%d/%m/%Y %H:%M:%S")
        table = read_page(browser)
        end = datetime.now().strftime("%d/%m/%Y %H:%M:%S")
        save_csv(flag,table,weapon_name)
    close_browser(browser)
    #time.sleep(1)
    #os.system('clear')
    #print("started search:" + start + "\nended search:" + end)
    print("")


main(sys.argv[1], sys.argv[2], sys.argv[3:])

