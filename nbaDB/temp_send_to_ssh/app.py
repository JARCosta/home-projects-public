#!/usr/bin/python
from flask import Flask, render_template, request
import requests
from bs4 import BeautifulSoup
import psycopg2
import psycopg2.extras
from time import sleep

app = Flask(__name__)

DB_HOST = "db.tecnico.ulisboa.pt"
DB_USER = "ist199088"
DB_PASSWORD = "jackers"
DB_CONNECTION_STRING = f"host={DB_HOST} dbname={DB_USER} user={DB_USER} password={DB_PASSWORD}"

def get_soup(url:str):  # sourcery skip: raise-specific-error
    '''get html code from the specified url'''
    r_html = requests.get(url, timeout=10).text
    soup =  BeautifulSoup(r_html,'html.parser')
    if soup.find('p').text == 'The owner of this website (www.basketball-reference.com) has banned you temporarily from accessing this website.':
        file1 = open("log.log", "w", encoding="utf-8")
        file1.write("baned from basketball-reference.com\n")
        file1.close()
        raise Exception(soup.find('p').text)
    return soup

@app.route("/table")
def table():
    return render_template("table.html")

@app.route("/")
def root():
    '''index.html'''
    db_conn = None
    cursor = None
    try:
        db_conn = psycopg2.connect(DB_CONNECTION_STRING)
        cursor = db_conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
        data = []
        cursor.execute("SELECT * FROM team;")
        data.append(len(list(cursor)))

        cursor.execute("SELECT * FROM game;")
        data.append(len(list(cursor)))

        cursor.execute("SELECT * FROM player;")
        data.append(len(list(cursor)))

        cursor.execute("SELECT * FROM game WHERE loaded = 0")
        data.append(len(list(cursor)))
        return render_template("index.html", result=data, title="Hello")
    except Exception as e:
        return str(e)  # Renders a page with the error.
    finally:
        cursor.close()
        db_conn.close()


@app.route("/teams")
def teams():
    db_conn = None
    cursor = None
    try:
        db_conn = psycopg2.connect(DB_CONNECTION_STRING)
        cursor = db_conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
        cursor.execute("SELECT name, short, color, logo FROM team ORDER BY name;")
        return render_template("teams.html", cursor=cursor)
    except Exception as e:
        return str(e)  # Renders a page with the error.
    finally:
        cursor.close()
        db_conn.close()

@app.route("/update_teams")
def update_teams():
    db_conn = None
    cursor = None
    try:
        db_conn = psycopg2.connect(DB_CONNECTION_STRING)
        cursor = db_conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
        years = range(2022,2024)
        for season in years:
            query = """insert into season (year)
                    Select %s Where not exists(select * from season where year=%s)
            """
            cursor.execute(query, (season,season))
        query,data = "START TRANSACTION;", []
        for season in years:
            url =  'https://www.basketball-reference.com/leagues/NBA_'+str(season)+'.html'
            soup = get_soup(url).find("table", {"id" : "per_game-team"}).find("tbody")
            team_list = soup.find_all('td', {"data-stat" : "team"})
            for team in team_list:
                short = team.find('a')['href'].split('/')[2]
                name = team.text
                if name[-1] == '*':
                    name = name[:-1]
                query += """
                    insert into team (name, short)
                        Select %s,%s Where not exists(select * from team where name=%s);
                """
                data.extend([name, short, name])
        cursor.execute(query+"COMMIT;", tuple(data))
        return update_team_colors()
    except Exception as e:
        return str(e)  # Renders a page with the error.
    finally:
        db_conn.commit()
        cursor.close()
        db_conn.close()

def update_team_colors():
    '''update team colors'''
    db_conn = None
    cursor = None
    try:
        db_conn = psycopg2.connect(DB_CONNECTION_STRING)
        cursor = db_conn.cursor(cursor_factory=psycopg2.extras.DictCursor)

        url =  'https://usteamcolors.com/nba-colors/'
        soup = get_soup(url).find_all('li', {'class' : 'card'})
        team_list = [' '.join(i.find('a').text.replace('\n', '').split(' ')[:-1]) for i in soup]
        colors = [i.find('a')['style'].split(' ')[1] for i in soup]
        logos = [i.find('a').find('img')['src'] for i in soup]
        # return str(colors)
        query, data = "START TRANSACTION;", []

        for i, team in enumerate(team_list):
            query += """
                UPDATE team 
                SET color = %s, logo = %s
                WHERE team.name = %s;
            """
            data.extend(iter([colors[i], logos[i], team]))
        cursor.execute(query+"COMMIT;", tuple(data))
        return str([team_list, logos, colors])
    except Exception as e:
        return str(e)  # Renders a page with the error.
    finally:
        db_conn.commit()
        cursor.close()
        db_conn.close()


@app.route("/players")
def players():
    '''display players'''
    db_conn = None
    cursor = None
    try:
        db_conn = psycopg2.connect(DB_CONNECTION_STRING)
        cursor = db_conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
        cursor.execute("SELECT distinct(player), team.name, team.color, team.logo from contract join team on team = team.name ORDER BY player;")
        return render_template("players.html", cursor=cursor)
    except Exception as e:
        return str(e)  # Renders a page with the error.
    finally:
        cursor.close()
        db_conn.close()

def update_players_aux(cursor, game):
    '''auxiliar func to insert players into db'''
    soup = get_soup(game[5])
    tables = soup.find_all("table")
    tables = [tables[0], tables[8]]
    year = int("https://www.basketball-reference.com/boxscores/202111010ATL.html".split("boxscores/")[1][:4])

    query, data = "START TRANSACTION;", []
    for table in tables: # for each table create players
        team = str(str(table.find("caption").text).split("Basic and Advanced Stats Table", maxsplit=1)[0][:-1])
        table = table.find("tbody").find_all("tr", class_=False)
        player_list = [i.find("th", {"data-stat" : "player"}).text for i in table]
        for player in player_list: # iniciatize player
            query += """
                insert into player (name)
                    Select %s Where not exists(select * from player where name=%s);
                insert into contract(player, year, team)
                    Select %s,%s,%s Where not exists(select * from contract where player=%s and year=%s);
            """
            data.extend([player, player])
            data.extend([player,year,team,player,year])
    cursor.execute(query+"COMMIT;", data)

    query, data = "", []
    for table in tables: # for each table, add game to each player
        table = table.find("tbody").find_all("tr", class_=False)
        
        player_list = [i.find("th", {"data-stat" : "player"}).text for i in table]
        m_p = [str(i.find("td", {"data-stat" : "mp" }).text) for i in table if i.find("td", {"data-stat" : "mp" }) is not None]
        pts = [int(i.find("td", {"data-stat" : "pts"}).text) for i in table if i.find("td", {"data-stat" : "pts"}) is not None]
        trb = [int(i.find("td", {"data-stat" : "trb"}).text) for i in table if i.find("td", {"data-stat" : "trb"}) is not None]
        ast = [int(i.find("td", {"data-stat" : "ast"}).text) for i in table if i.find("td", {"data-stat" : "ast"}) is not None]
        blk = [int(i.find("td", {"data-stat" : "blk"}).text) for i in table if i.find("td", {"data-stat" : "blk"}) is not None]
        stl = [int(i.find("td", {"data-stat" : "stl"}).text) for i in table if i.find("td", {"data-stat" : "stl"}) is not None]
        tov = [int(i.find("td", {"data-stat" : "tov"}).text) for i in table if i.find("td", {"data-stat" : "tov"}) is not None]
        fg3 = [int(i.find("td", {"data-stat" : "fg3"}).text) for i in table if i.find("td", {"data-stat" : "fg3"}) is not None]
        stats = [pts,trb,ast,blk,stl,tov,fg3]

        multipliers = [1,1.2,1.5,3,3,-2,1]
        fantasy_points = [sum([int(str(stats[j][i])) * multipliers[j] for j in range(len(stats))]) for i in range(len(pts)) ]

        for i,player in enumerate(player_list):                   # add player to game
            if i < len(pts):                            # if played
                query += """
                    INSERT INTO plays (player, game, minutes_played, points, rebounds, assists, blocks, steal, turnover, triples, "fantasy points")
                        Select %s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s Where not exists(select * from plays where player=%s AND game =%s);
                """
                data.extend([player, game[5], m_p[i], stats[0][i], stats[1][i], stats[2][i], stats[3][i], stats[4][i], stats[5][i], stats[6][i], fantasy_points[i], player, game[5]])
            else:                                       # if benched
                query += """
                    INSERT INTO plays (player, game)
                        Select %s,%s Where not exists(select * from plays where player=%s AND game =%s);
                """
                data.extend([player, game[5], player, game[5]])
    query += """ UPDATE game
    SET loaded = 1
    WHERE href = %s;
    """
    data.append(game[5])
    with open("log.log", "a", encoding="utf-8") as log:
        log.write(str(game) + "\n")
    return query, data, [str(i.find("caption").text).split("Basic and Advanced Stats Table",maxsplit=1)[0] for i in tables]

@app.route("/update_players")
def update_players():
    '''insert players into db'''
    db_conn = None
    cursor = None
    try:
        # update_loaded_games()
        db_conn = psycopg2.connect(DB_CONNECTION_STRING)
        cursor = db_conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
        cursor.execute('SELECT * FROM game WHERE loaded=0 ORDER BY date DESC;')
        curs = list(cursor)
        n_its = 20
        # sleep(120)
        # curs = [list(i) for i in np.array_split(curs, n_its)]
        for chunk in range(0, len(curs), n_its):
            query, data = "START TRANSACTION;", []
            for game in curs[chunk:chunk+n_its]:
                temp = update_players_aux(cursor, game)
                query += temp[0]
                data.extend(temp[1])
            cursor.execute(query + "COMMIT;", data)
            sleep(120)
        return root()
    except Exception as e:
        return str(e)  # Renders a page with the error.
    finally:
        db_conn.commit()
        cursor.close()
        db_conn.close()

@app.route("/games")
def games():
    '''display games'''
    db_conn = None
    cursor = None
    try:
        db_conn = psycopg2.connect(DB_CONNECTION_STRING)
        cursor = db_conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
        
        arg = list(request.args)
        # return str(request.args[arg[0]])
        # for arg in args:
        if not arg:
            query = """SELECT date::date, home.short, home_score, visitor.short, visitor_score, game.href, home.color, visitor.color, home.logo, visitor.logo, game.loaded
                    FROM game JOIN team home ON home = home.name JOIN team visitor ON visitor = visitor.name ORDER BY date DESC;"""
            data = []
            result = ('All games',)
        elif arg[0] == "team":
            query = """SELECT date::date, home.short, home_score, visitor.short, visitor_score, game.href, home.color, visitor.color, home.logo, visitor.logo, game.loaded
                    FROM game JOIN team home ON home = home.name
                    JOIN team visitor on visitor = visitor.name
                    WHERE home.name = %s OR visitor.name = %s;"""
            data = [request.args[arg[0]],request.args[arg[0]]]
            result = ('Games from '+request.args[arg[0]],)
        elif arg[0] == "short":
            query = """SELECT date::date, home.short, home_score, visitor.short, visitor_score, game.href, home.color, visitor.color, home.logo, visitor.logo, game.loaded
                    FROM game JOIN team home ON home = home.name
                    JOIN team visitor on visitor = visitor.name
                    WHERE home.short = %s OR visitor.short = %s;"""
            data = [request.args[arg[0]],request.args[arg[0]]]
            result = ('Games from '+request.args[arg[0]],)
        elif arg[0] == "player":
            query = """SELECT date::date, home.short, home_score, visitor.short, visitor_score, game.href, home.color, visitor.color, home.logo, visitor.logo, game.loaded
                    FROM plays
                    JOIN game on plays.game = game.href
                    join team visitor on visitor = visitor.name
                    join team home on home = home.name
                    WHERE player = %s"""
            # query = """SELECT player.name, plays.game, minutes_played, points, rebounds, assists, blocks, steal, turnover, triples, "fantasy points", opponent.name, opponent.logo, opponent.color
            #         FROM plays JOIN player ON player = player.name JOIN game ON plays.game = game.href JOIN team as opponent ON CASE WHEN team = home then visitor ELSE home END = opponent.name WHERE player.name = %s"""
            data = [request.args[arg[0]],]
            result = ('Games from '+request.args[arg[0]],)
        #TODO games_from_player_vs_team
        # query = """select *
        #         from plays
        #         join game on plays.game = game.href

        #         join team home on home = home.name
        #         join team visitor on visitor = visitor.name
        #         --join team opponent on visitor = opponent.name or home = opponent.name
        #         --join team own on not(visitor = own.name or home = own.name)
        #         where player = 'Kevin Durant' and (home.name = 'Orlando Magic' or visitor.name = 'Orlando Magic')"""

        cursor.execute(query, data)
        return render_template("games.html", cursor=cursor, result=result)
    except Exception as e:
        return str(e)  # Renders a page with the error.
    finally:
        cursor.close()
        db_conn.close()


@app.route("/update_games")
def update_games():
    '''insert game into db'''
    db_conn = None
    cursor = None
    try:
        db_conn = psycopg2.connect(DB_CONNECTION_STRING)
        cursor = db_conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
        # if curs == []:
        #     years = range(2020,2024)
        # else:
        #     last_game_date = [int(i) for i in str(curs[0][0]).split(" ")[0].split("-")[::-1]]
        #     years = [last_game_date[1],]
        #     if last_game_date[1] > 4:
        #         years.append(last_game_date[1]+1)
        years = range(2022,2024)
        for year in years:
            url = 'https://www.basketball-reference.com/leagues/NBA_'+str(year)+'_games.html'
            soup = get_soup(url)
            rest_months_href = ["https://www.basketball-reference.com"+i.find("a")["href"] for i in soup.find("div", {"class" : "filter"}).find_all("div")[1:]]
            soups = [soup,]
            soups.extend([get_soup(i) for i in rest_months_href])
            query, data = "START TRANSACTION;", []
            for soup in soups: # for each month
                for row in soup.find('tbody').find_all('tr', class_ = False):
                    if len(row.find('td', {'data-stat':'home_pts'}))==0:
                        break
                    date = row.find('th', {'data-stat':'date_game'}).text
                    home = row.find('td', {'data-stat':'home_team_name'}).text
                    h_points = row.find('td', {'data-stat':'home_pts'}).text
                    visitor = row.find('td', {'data-stat':'visitor_team_name'}).text
                    v_points = row.find('td', {'data-stat':'visitor_pts'}).text
                    href = 'https://www.basketball-reference.com' + row.find('td', {'data-stat':'box_score_text'}).find('a')['href']
                    query += """
                        INSERT INTO game (date, home, home_score, visitor, visitor_score, href, loaded)
                            SELECT %s,%s,%s,%s,%s,%s,0 WHERE NOT EXISTS(SELECT * FROM game WHERE date=%s AND home=%s AND visitor=%s);
                    """
                    data.extend([date, home, h_points, visitor, v_points, href, date, home, visitor])
            cursor.execute(query+"COMMIT;", data)
            sleep(60)
        return games()
    except Exception as e:
        return str(e)  # Renders a page with the error.
    finally:
        db_conn.commit()
        cursor.close()
        db_conn.close()


@app.route("/show_game")
def show_game():
    '''display specific game'''
    db_conn = None
    cursor = None
    try:
        db_conn = psycopg2.connect(DB_CONNECTION_STRING)
        cursor = db_conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
        href = request.args["href"]
        query = "select * from plays join player on player = player.name where plays.game =%s"
        cursor.execute(query, (href,))
        return render_template("show_game.html", cursor=cursor)
    except Exception as e:
        return str(e)  # Renders a page with the error.
    finally:
        cursor.close()
        db_conn.close()

@app.route("/clear")
def clear():
    '''clear db'''
    db_conn = None
    cursor = None
    try:
        db_conn = psycopg2.connect(DB_CONNECTION_STRING)
        cursor = db_conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
        query = """
            DELETE FROM plays WHERE 1=1;
            DELETE FROM player WHERE 1=1;
            DELETE FROM game WHERE 1=1;
            DELETE FROM team WHERE 1=1;
        """
        cursor.execute(query)
        return query
    except Exception as e:
        return str(e)  # Renders a page with the error.
    finally:
        db_conn.commit()
        cursor.close()
        db_conn.close()