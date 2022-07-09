from urllib.request import urlopen
from lxml import etree
import csv
import json

URL = "https://csgofloat.com/db?defIndex=7&category=3&order=4&min=0.351&max=0.352"

XPATH = "/html/body/app-root/div/div[2]/app-float-db/div/div/div/mat-card/div/img"

response = urlopen(URL)
htmlparser = etree.HTMLParser()
tree = etree.parse(response, htmlparser)