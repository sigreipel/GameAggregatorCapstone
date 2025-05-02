# https://docs.python.org/3/library/sqlite3.html
import sqlite3
import csv
import json
import os



def makeConnection(DB_PATH: str) -> tuple[sqlite3.Connection, sqlite3.Cursor]:
    #Connecting SQLire to the db
    con = sqlite3.connect(DB_PATH)
    cur = con.cursor()
    return con, cur


def createDB(cur: sqlite3.Cursor) -> None:
    #Creating the db
    print("Creating db")
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
    print("db created")


def populateDB(cur: sqlite3.Cursor, con: sqlite3.Connection) -> None:
    # TODO figure out how to get arrays into database. Will I need another table? for blocks/follows/genres
    #TODO split devs/genres/etc before making tables
    print("reading csv")
    data = []
    with open('game_info.csv', 'r', encoding='utf-8') as file:
        csv_reader = csv.reader(file)
        for row in csv_reader:
            data.append(row)
    # print(data[0])
    # print(data[1])

    # Inserting Developers
    developersData = set(row[17] for row in data if row[17].strip())  # Unique dev names, Exclude empty values
    # devID, devName
    for dev in developersData:
        cur.execute("INSERT OR IGNORE INTO DEVS (devName) VALUES (?)", (dev,))
    con.commit()

    # Map devName -> DevID
    cur.execute("SELECT devID, devName FROM DEVS")
    devID_map = {name: devID for devID, name in cur.fetchall()}
    # print(devID_map)

    #Inserting Games
    gamesData = [(row[2], json.dumps(row[18].split(',')), devID_map.get(row[17], None), "placeholder") for row in data]
    # gameID, gameName, genres, devID, gameImage
    #TODO figure out genres
    cur.executemany("INSERT INTO GAMES (gameName, genres, devID, gameImage) VALUES (?,?,?,?)", gamesData)

    #Insert Sample Users
    userData = [('testuser1', 'pass1hash', 'user1@email.tld', 1, 2, 1, 2,)]
    cur.executemany("INSERT INTO USERS (userName, userPass, userEmail, blockedDevs, followedDevs, blockedGames, followedGames) VALUES (?,?,?,?,?,?,?)", userData)

    #Inserting Sample News
    cur.execute("SELECT gameID, gameName FROM GAMES")
    gameID_map = {name: gameID for gameID, name in cur.fetchall()}
    
    newsData = [
    ('newsOne', 'the first game has news!', gameID_map.get("First Game Name", None)),
    ('newsTwo', 'the second game has news!', gameID_map.get("Second Game Name", None))
    ]

    cur.executemany("INSERT INTO NEWS (newsTitle, newsContent, gameID) VALUES (?,?,?)", newsData)
    con.commit()


def debugDB(cur: sqlite3.Cursor, DEBUG_MODE: bool) -> None:
    #Debugging
    if not DEBUG_MODE:
        return
    for table in ["DEVS", "GAMES", "USERS", "NEWS"]:
        res = cur.execute(f"SELECT * FROM {table}")
        print(f"{table}:", res.fetchall())


def createDeveloper(cur: sqlite3.Cursor, con: sqlite3.Connection, devName: str):
    cur.execute("INSERT OR IGNORE INTO DEVS (devName) VALUES (?)", (devName,))
    con.commit()


def fetchAllDevelopers(cur: sqlite3.Cursor) -> list:
    res = cur.execute(f"SELECT * FROM DEVS")
    return res.fetchall()


def main():
    #Getting the path to store the db inside the project dir
    BASE_DIR = os.path.dirname(os.path.abspath(__file__))
    DB_PATH = os.path.join(BASE_DIR, "placeholder.db")

    DEBUG_MODE = False
    # csv_file = os.path.join(BASE_DIR, 'game_info.csv')
    if not os.path.exists(DB_PATH):
        con, cur = makeConnection(DB_PATH)
        createDB(cur) # good
        populateDB(cur, con) #not good
        debugDB(cur, DEBUG_MODE)



if __name__ == "__main__":

    main()