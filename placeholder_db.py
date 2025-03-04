# https://docs.python.org/3/library/sqlite3.html
import sqlite3
import csv

con = sqlite3.connect("placeholder.db")
cur = con.cursor()

cur.execute("""
    CREATE TABLE USERS(
        userID INTEGER PRIMARY KEY AUTOINCREMENT, 
        userName TEXT, 
        userPass TEXT, 
        userEmail TEXT, 
        blockedDevs TEXT,  -- Store as JSON string or separate table
        followedDevs TEXT, -- Store as JSON string or separate table
        blockedGames TEXT, -- Store as JSON string or separate table
        followedGames TEXT -- Store as JSON string or separate table
    )
""")

cur.execute("""
    CREATE TABLE DEVS(
        devID INTEGER PRIMARY KEY AUTOINCREMENT, 
        devName TEXT UNIQUE
    )
""")

cur.execute("""
    CREATE TABLE GAMES(
        gameID INTEGER PRIMARY KEY AUTOINCREMENT, 
        gameName TEXT, 
        genres TEXT, 
        devID INTEGER,
        gameImage TEXT,
        FOREIGN KEY (devID) REFERENCES DEVS(devID)
    )
""")

cur.execute("""
    CREATE TABLE NEWS(
        newsID INTEGER PRIMARY KEY AUTOINCREMENT, 
        newsTitle TEXT, 
        newsContent TEXT, 
        gameID INTEGER,
        FOREIGN KEY (gameID) REFERENCES GAMES(gameID)
    )
""")


# TODO figure out how to get arrays into database. Will I need another table? for blocks/follows/genres
#TODO split devs/genres/etc before making tables
data = list(csv.reader(open('game_info.csv')))[1:]

developersData = set(row[17] for row in data if row[17].strip())  # Unique dev names, Exclude empty values
# devID, devName
for dev in developersData:
    cur.execute("INSERT OR IGNORE INTO DEVS (devName) VALUES (?)", (dev,))
devID_map = {name: devID for devID, name in cur.fetchall()}


gamesData = [(row[2], row[18], devID_map.get(row[17], None), "placeholder") for row in data]
# gameID, gameName, genres, devID, gameImage
#TODO figure out genres
cur.executemany("INSERT INTO GAMES (gameName, genres, devID, gameImage) VALUES (?,?,?,?)", gamesData)

#TODO make this real
userData = [('testuser1', 'pass1hash', 'user1@email.tld', 1, 2, 1, 2,)]
cur.executemany("INSERT INTO USERS (userName, userPass, userEmail, blockedDevs, followedDevs, blockedGames, followedGames) VALUES (?,?,?,?,?,?,?)", userData)


cur.execute("SELECT gameID, gameName FROM GAMES")
gameID_map = {name: gameID for gameID, name in cur.fetchall()}

newsData = [
    ('newsOne', 'the first game has news!', gameID_map.get("First Game Name", None)),
    ('newsTwo', 'the second game has news!', gameID_map.get("Second Game Name", None))
]

cur.executemany("INSERT INTO NEWS (newsTitle, newsContent, gameID) VALUES (?,?,?)", newsData)


con.commit()

res = cur.execute("SELECT * FROM DEVS")
print("Developers:", res.fetchall())

res = cur.execute("SELECT * FROM GAMES")
print("Games:", res.fetchall())

res = cur.execute("SELECT * FROM NEWS")
print("News:", res.fetchall())
