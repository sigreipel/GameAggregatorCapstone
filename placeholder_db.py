# https://docs.python.org/3/library/sqlite3.html
import sqlite3

con = sqlite3.connect("placeholder.db")
cur = con.cursor()

cur.execute("CREATE TABLE USERS(userID, userName, userPass, userEmail, blockedDevs, followedDevs, blockedGames, followedGames)")
cur.execute("CREATE TABLE DEVS(devID, devName)")
cur.execute("CREATE TABLE GAMES(gameID, gameName, genres, devID, gameImage)")
cur.execute("CREATE TABLE NEWS(newsID, newsTitle, newsContent, gameID)")

# TODO figure out how to get arrays into database. Will I need another table? for blocks/follows/genres
cur.execute("""
    INSERT INTO USERS VALUES
        (111111111, 'firstuser', 'pass1hash', 'user1@email.tld', 101010101, 202020202, 100100100, 200200200),
        (222222222, 'seconduser', 'pass2hash', 'user2@email.tld', 202020202, 101010101, 200200200, 100100100)
""")

cur.execute("""
    INSERT INTO DEVS VALUES
        (101010101, 'devZero'),
        (202020202, 'devOne')
""")

cur.execute("""
    INSERT INTO GAMES VALUES
        (100100100, 'gameZero', 'horror', 101010101, 'game1img'),
        (200200200, 'gameOne', 'jrpg', 202020202, 'game2img')
""")

cur.execute("""
    INSERT INTO NEWS VALUES
        (100000001, 'newsOne', 'the first game has news!', 100100100),
        (200000002, 'newsTwo', 'the second game has news!', 200200200)
""")

con.commit()

res = cur.execute("SELECT userPass FROM USERS")
print(res.fetchall())
res = cur.execute("SELECT devID FROM DEVS")
print(res.fetchall())
res = cur.execute("SELECT gameName FROM GAMES")
print(res.fetchall())
res = cur.execute("SELECT newsContent FROM NEWS")
print(res.fetchall())