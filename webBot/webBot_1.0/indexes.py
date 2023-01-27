from urllib.request import urlopen
from lxml import etree
import csv
import json


def extract_table_from_site():
    url =  "https://tf2b.com/itemlist.php?gid=730"
    response = urlopen(url)
    htmlparser = etree.HTMLParser()
    tree = etree.parse(response, htmlparser)
    table = []
    stop = False
    id = 1
    while not stop:
        try:
            index = str(etree.tostring(tree.xpath("/html/body/section/ul/li[" + str(id) + "]/div")[0]))[7:-7]
            name = str(etree.tostring(tree.xpath("/html/body/section/ul/li[" + str(id) + "]/em")[0]))[6:-6]
            table.append([index, name])
            id += 1
        except:
            stop = True
    return table


def store_csv(flag):
    with open('indexes.csv', mode=flag) as employee_file:
        employee_writer = csv.writer(employee_file, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
        for i in extract_table_from_site():
            employee_writer.writerow(i)

def store_json(flag):
    with open('indexes.json', mode=flag) as outfile:

        json.dump(extract_table_from_site(), outfile)
            

store_json("w")