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
    ret = []
    #ret += [line[0].text[1:],] #rank
    #ret += [line[1].text.split("\n")[0][9:],] # weapon
    ret += [line[1].text.split("\n")[1],] # skin name
    ret += [line[2].text[:-3],] # float
    #ret += [line[3].text,] # seed

    try:
        link = str(line[5].find_element(By.XPATH, (xpath + "[7]/div/span/a")).get_attribute("href"))
    except:
        link = str(line[5].find_element(By.XPATH, (xpath + "[7]/div/app-steam-avatar/a")).get_attribute("href"))
    try:
        price = line[10].find_element(By.XPATH, (xpath + "[11]/div/span")).text
    except:
        price = ""
    
    link_split = link.split("_")
    link_split = link_split[len(link_split)-1].split("|")
    skin_id = link_split[len(link_split)-1]

    ret += [skin_id, link, price]
    return ret


def read_page(browser, stopping_weapon, VERBOSE: bool):
    try:
        stopping_weapon_id = stopping_weapon[len(stopping_weapon)-3]
    except:
        stopping_weapon_id = None
    table = []
    new_items = True
    for i in range(30):
        try:
            line = read_line(browser, 1)
            if VERBOSE:
                print(stopping_weapon_id, line[len(line)-3])
            if line[len(line)-3] == stopping_weapon_id:
                update = False
                for j in range(len(stopping_weapon)):
                    if line[j] != stopping_weapon[j]:
                        update = True
                if update:
                    table.append(line)
                new_items = False
                break
            table.append(line)
            print("item 1 loaded")
            break
        except:
            print("item 1 not found")
            time.sleep(1)
            continue
    i = 2
    while new_items:
        try:
            line = read_line(browser, i)
            if VERBOSE:
                print(i, stopping_weapon_id, line[len(line)-3])
            if line[len(line)-3] == stopping_weapon_id:
                new_items = False
                break
            table.append(line)
            print("item", i, "loaded")
            i += 1
            continue
        except:
            print("reached end of page")
            new_items = False
            break
    return table


def save_csv(flag, table, weapon_name):
    try:
        employee_file = open("outs/" + weapon_name + '.csv', mode="r")
        content = employee_file.read()
        employee_file.close()
    except FileNotFoundError:
        temp = True
    employee_file = open("outs/" + weapon_name + '.csv', mode="w")
    employee_writer = csv.writer(employee_file, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
    employee_writer.writerow([datetime.now().strftime("%d/%m/%Y %H:%M:%S"),])
    for i in table:
        employee_writer.writerow(i)
    employee_writer.writerow([])
    try:
        employee_file.write(content)
    except UnboundLocalError:
        temp = True




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

def browse(LOGIN, url, stopping_weapon, VERBOSE: bool):
    browser = open_browser()
    if LOGIN == True:
        open_url(browser,url)
        useless = input("press return to resume:")
    #table = sys.argv[2:]
    #time.sleep(1)
    while True:
        try:
            browser.get(url)
            break
        except:
            continue

    table = read_page(browser, stopping_weapon, VERBOSE)
    #close_browser(browser)
    return table

#main(sys.argv[1], sys.argv[2], sys.argv[3:])
