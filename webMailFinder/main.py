from os import dup, listdir
import requests
import re

url = "https://mariaadelaide.com/"
headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/105.0.0.0 Safari/537.36 Edg/105.0.1343.33'}

result = requests.get(url, headers=headers)
match = re.findall(r'https://[\w.+-]+\.[\w.-]+', result.text)

list = []
for i in match:
    if i+'/' not in list:
        list.append(i+'/')

outputFile = open('wmf_output.txt', mode="w")
for i in list:
    print(i)
    outputFile.write(i + "\n")
    temp = []
    try:
        r = requests.get(i)
        match = re.findall(r'[\w.+-]+@[\w-]+\.[\w.-]+', r.text)
        for j in match:
            if j not in temp:
                outputFile.write("\t" + j + "\n")
                temp.append(j)
    except:
        print("ERROR: ", i)