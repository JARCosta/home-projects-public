import argparse
import difflib
import csv
from posixpath import split
from cairo import FILTER_GAUSSIAN
import pandas
from datetime import datetime
import indexes
import web

LOGIN_URL = "https://store.steampowered.com/login"

parser = argparse.ArgumentParser(description='Export and analyse CSGOFloat.com')
parser.add_argument('-f', type=float, dest='float', help='floats to look for')
parser.add_argument('-w', type=str, dest='weapon', help='weapon to look for')

parser.add_argument('--indexes', action='store_true', dest='indexes', help='update indexes')
parser.add_argument('--login', action='store_true', dest='login', help='open login before running')

others = parser.add_mutually_exclusive_group()
others.add_argument('-st', action='store_true', dest='stattrak', help='only StatTrak™ skins')
others.add_argument('-so', action='store_true', dest='souvenir', help='only Souvenir skins')
others.add_argument('-n', action='store_true', dest='normal', help='only normal skins')

sorts = parser.add_mutually_exclusive_group()
sorts.add_argument('-hf', action='store_true', dest='byHighFloat', help='sort by highest float')
sorts.add_argument('-up', action='store_true', dest='byUpdated', help='sort by last updated float')
sorts.add_argument('-ni', action='store_true', dest='byNewID', help='sort by newst ID float')
sorts.add_argument('-oi', action='store_true', dest='byOldID', help='sort by oldest ID float')

group = parser.add_mutually_exclusive_group()
group.add_argument('-v', action='store_true', dest='verbose',help='Verbosity on/off')
args = parser.parse_args()
WEAPON: list = None #[index, name]
CATEGORY: int = None
STATTRAK: bool= False
SOUVENIR: bool = False
FLOAT: float = None
SORT: int = None

LOGIN: bool = False
UPDATE_INDEXES: bool = False

def filter_link(weapon: str, category: int, float: list, sort: int):
    filter_link = "https://csgofloat.com/db?"
    if weapon:
        filter_link += "defIndex=" + str(WEAPON[0]) + "&"
    if category:
        filter_link += "category=" + str(category) + "&"
    if sort:
        filter_link += "order=" + str(sort) + "&"
    if float:
        filter_link += "min=" + float[0] + "&max=" + float[1] + "&"
    return filter_link[:-1]


def get_min_max_floats(float):
    strin = str(float)
    last = strin[len(strin)-1]
    return [str(float), str(strin[:-1] + str(int(last)+1))]

if __name__ == '__main__':
    start = datetime.now()
    verbose = "Searching for: "
    quiet = ""

    args_start = datetime.now()
    if args.stattrak:
        quiet += "StatTrak™"
        verbose += "StatTrak™"
        STATTRAK = True
        CATEGORY = 2
    elif args.souvenir:
        quiet += "Souvenir"
        verbose += "Souvenir"
        SOUVENIR = True
        CATEGORY = 3
    elif args.normal:
        CATEGORY = 1

    if args.weapon:
        weapon = indexes.get_weapon(args.weapon)
        verbose += " " + weapon[1]
        quiet += " " + weapon[1]
        WEAPON = weapon # [index, name]

    if args.byHighFloat:
        SORT = -1
    elif args.byNewID:
        SORT = 2
    elif args.byOldID:
        SORT = 3
    elif args.byUpdated:
        SORT = 4

    if args.float:
        min_max = get_min_max_floats(args.float)
        verbose += " with float between " + min_max[0] + " and " + min_max[1]
        quiet += ", " + min_max[0] + " < float < " + min_max[1]
        FLOAT = [min_max[0],min_max[1]]
    if args.login:
        LOGIN = args.login
    if args.indexes:
        UPDATE_INDEXES = args.indexes
    url_start = args_end = datetime.now()
    filter_url = filter_link(WEAPON,CATEGORY,FLOAT,SORT)
    if args.verbose:
        print(filter_url)
    url_end = datetime.now()
    web_start = datetime.now()
    top_skins = web.browse(LOGIN, filter_url, indexes.get_first_weapon(WEAPON[1]), args.verbose)
    verbose += ", " + str(len(top_skins)) + " items found"
    quiet += ", " + str(len(top_skins)) + " items"
    web.save_csv("w",top_skins,WEAPON[1])
    web_end = datetime.now()
    end = datetime.now()
    if args.verbose:
        print("args getter:",args_end - args_start, "\nurl  finder:", url_end - url_start, "\ntotal:", end - start)

    if args.verbose:
        print(verbose)
    else:
        if quiet != "":
            print(quiet)
