import logging as log
import sqlite3
import os.path
import json
import __main__

# get the path where __main__ file is
main_dir = __main__.__file__
main_dir = os.path.dirname(main_dir)
db_path = main_dir + '\\profiles.db'
print(db_path)

# get ranks json



# returns True if player exists in database and False if not
def check_player_exists(player):
    con = sqlite3.connect(db_path)
    cur = con.cursor()
    cur.execute('SELECT user_name, user_disc FROM profile WHERE user_name=? AND user_disc=?', (player.name, player.discriminator))
    if cur.fetchone():
        log.debug(f'Player: {player.name}:{player.discriminator} exists in db')
        return True
    else:
        log.debug(f'Player: {player.name}:{player.discriminator} dont exists in db')
        return False


def set_player(player):
    if not check_player_exists(player):
        con = sqlite3.connect(db_path)
        cur = con.cursor()
        log.debug(player.name + ' is now in the db')
        cur.execute('INSERT INTO profile VALUES(?, ?, 0, 0)', (player.name, player.discriminator))
        con.commit()
        con.close()
    else:
        log.debug(player.name + ' is already in the db')

def update_player(player, xp: int, coins: int):
    con = sqlite3.connect(db_path)
    con.row_factory = lambda cursor, row: row[0]
    cur = con.cursor()
    cur.execute('UPDATE profile SET xp = ? AND coins = ? WHERE user_name = ? AND user_disc = ?', (xp, coins, player.name, player.discriminator))
    con.commit()
    con.close()

def get_xp(player):
    if check_player_exists(player):
        con = sqlite3.connect(db_path)
        #con.row_factory = lambda cursor, row: row[0]
        cur = con.cursor()
        cur.execute('SELECT * FROM profile WHERE user_name = ? AND user_disc = ?', (player.name, player.discriminator))
        xp = list(cur.fetchone())[2]
        con.commit()
        con.close()
        return xp

def add_xp(player, amount: int):
    if check_player_exists(player):
        xp = get_xp(player)
        if not xp:
            xp = 0
        xp += amount
        con = sqlite3.connect(db_path)
        cur = con.cursor()
        cur.execute('UPDATE profile SET xp = ? WHERE user_name = ? AND user_disc = ?', (xp, player.name, player.discriminator))
        con.commit()
        con.close()
    else:
        set_player(player)
        add_xp(player, amount)
