DROP TABLE IF EXISTS plays CASCADE;
DROP TABLE IF EXISTS contract CASCADE;
DROP TABLE IF EXISTS player CASCADE;
DROP TABLE IF EXISTS game CASCADE;
DROP TABLE IF EXISTS team CASCADE;


CREATE TABLE team(
    name VARCHAR(80) NOT NULL,
    short VARCHAR(80) NOT NULL,
    color VARCHAR(80),
    logo VARCHAR(80),
    CONSTRAINT pk_team PRIMARY KEY(name)
);


CREATE TABLE game(
    date DATE NOT NULL,
    home VARCHAR(80) NOT NULL,
	home_score INTEGER NOT NULL,
    visitor VARCHAR(80) NOT NULL,
	visitor_score INTEGER NOT NULL,
	href VARCHAR(80) NOT NULL,
	loaded INTEGER NOT NULL,
    CONSTRAINT pk_game PRIMARY KEY(date, home, visitor),
    CONSTRAINT fk_home FOREIGN KEY(home) REFERENCES team(name),
    CONSTRAINT fk_visitor FOREIGN KEY(visitor) REFERENCES team(name),
    unique(href)
);


CREATE TABLE player(
    name VARCHAR(80) NOT NULL,
    CONSTRAINT pk_player PRIMARY KEY(name)
);


CREATE TABLE contract(
    player VARCHAR(80) NOT NULL,
    year INTEGER NOT NULL,
    team VARCHAR(80) NOT NULL,
    CONSTRAINT pk_contract PRIMARY KEY(player, year),
    CONSTRAINT fk_player FOREIGN KEY(player) REFERENCES player(name),
    CONSTRAINT fk_team FOREIGN KEY(team) REFERENCES team(name)
);


CREATE TABLE plays(
	player VARCHAR(80) NOT NULL,
    game VARCHAR(80) NOT NULL,
    minutes_played VARCHAR(80),
    points INTEGER,
    rebounds INTEGER,
    assists INTEGER,
    blocks INTEGER,
    steal INTEGER,
    turnover INTEGER,
    triples INTEGER,
    "fantasy points" INTEGER,
    CONSTRAINT pk_plays PRIMARY KEY(player, game),
	CONSTRAINT fk_player FOREIGN KEY(player) REFERENCES player(name),
	CONSTRAINT fk_game FOREIGN KEY(game) REFERENCES game(href)
);