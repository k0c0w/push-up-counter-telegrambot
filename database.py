import sqlite3
from pathlib import Path

import dayscalculater

AIM = 10000

def init():
    db = Path("./database.db")
    try:
        db.resolve(strict=True)
        print("Database is found")
    except FileNotFoundError:
        print("Database not found, trying to create a new one.")
        try:
            init_sqlite()
        except Exception as e:
            print("Error when creating database : ", e.__repr__(), e.args)
            pass
        else:
            print("Success.")

def sqlite_connect():
    conn = sqlite3.connect("database.db", check_same_thread=False)
    conn.execute("pragma journal_mode=wal;")
    return conn

def updatebase(user_id:int, name:str):
    try:
        conn = sqlite_connect()
        curs = conn.cursor()
        exists = curs.execute(f"SELECT * FROM userinfo WHERE user_id = {user_id}").fetchone()
        if not exists:
            create_user(user_id, name, conection=conn, cursor=curs)
    except sqlite3.Error:
        print("Произошла ошибка в апдейте юзеров: " + str(user_id))
    finally:
        if conn:
            conn.close()
            print("Конец updatebase")

def create_user(user_id:int, name:str, conection, cursor):
    try:
        cursor.execute("BEGIN TRANSACTION")
        #TODO: цель заменить на 10000/остаток дней
        cursor.execute("INSERT INTO userinfo (user_id, name, total, aim, done) VALUES (?, ?, ?, ?,?)",
                       (user_id, name, 0, AIM // dayscalculater.DaysLeft, 0))
        conection.commit()
    except sqlite3.Error:
        print("Ошибка добавления в Users!")
        conection.rollback()
        return
    try:
        cursor.execute("BEGIN TRANSACTION")
        cursor.execute("INSERT INTO maillist (user_id, permission) VALUES (?,?)",
                       (user_id,1))
        conection.commit()
    except sqlite3.Error:
        print("Ошибка добавления в maillist!")
        conection.rollback()


def init_sqlite():
    conn = sqlite_connect()
    c = conn.cursor()
    c.execute('''CREATE TABLE userinfo (id integer primary key, user_id integer, name text, total integer, aim integer, done integer)''')
    c.execute('''CREATE TABLE maillist (id integer primary key, user_id integer, permission integer)''')
    c.execute('''CREATE TABLE achievements (id integer primary key, ach_hash integer, user_id integer)''')
    c.execute('''CREATE TABLE achievementDescription (id integer primary key, ach_name text, ach_description)''')
    conn.commit()
    conn.close()

def get_users_for_mailing():
    try:
        conn = sqlite_connect()
        curs = conn.cursor()
        curs.execute(f"SELECT user_id FROM maillist WHERE permission = 1")
        user = curs.fetchone()
        while user:
            yield int(user[0])
            user = curs.fetchone()
    except sqlite3.Error as e:
        if conn:
            print("Ошибка при работе с SQLite в  mainlist", e)
    finally:
        if conn:
            conn.close()
            print("Соединение c maillist закрыто")

def remove_from_mailing(users: list):
    try:
        conn = sqlite_connect()
        curs = conn.cursor()
        for user_id in users:
            try:
                curs.execute("BEGIN TRANSACTION")
                curs.execute(f"UPDATE maillist SET permission = 0 WHERE user_id = {user_id}")
                conn.commit()
            except sqlite3.Error:
                conn.rollback()
                print("Ошибка update в maillist с юзером: " + user_id)
    except sqlite3.Error as e:
        if conn:
            print("Ошибка при работе с SQLite в  mainlist", e)
    finally:
        if conn:
            conn.close()
            print("Соединение c maillist закрыто")

def switch_notifications(user_id: int):
    try:
        connection = sqlite_connect()
        curs = connection.cursor()
        curs.execute(f"SELECT permission FROM maillist WHERE user_id = {user_id}")
        permission = int(curs.fetchone()[0])
        curs.execute("BEGIN TRANSACTION")
        if permission == 0:
            permission = 1
            curs.execute(f"UPDATE maillist SET permission = 1 WHERE user_id = {user_id}")
        else:
            permission = 0
            curs.execute(f"UPDATE maillist SET permission = 0 WHERE user_id = {user_id}")
        connection.commit()
    except sqlite3.Error:
        if connection:
            print("Ошибка при изменении уведомлений: ", user_id)
            connection.rollback()
    finally:
        if connection:
            connection.close()
            print("Соединение maillist закрыто.")
    return bool(permission)


def getPushupsCount(user_id:int):
    try:
        connection = sqlite_connect()
        curs = connection.cursor()
        exists = curs.execute(f"SELECT total,done,aim FROM userinfo WHERE user_id = {user_id}").fetchone()
        if not exists:
            result = None
        else:
            result = (int(exists[0]), int(exists[1]), int(exists[2]))
    except sqlite3.Error as e:
            print("Ошибка при работе с SQLite при поиске оджиманий", e)
    finally:
        if connection:
            curs.close()
            print("Соединение userinfo закрыто")
    return result

#обновляет количество отжиманий
def update_pushups(user_id: int, pushups:int, pushupsperday: int):
    try:
        connection = sqlite_connect()
        curs = connection.cursor()
        curs.execute("BEGIN TRANSACTION")
        curs.execute(f"UPDATE userinfo SET total = {pushups}, done = {pushupsperday} WHERE user_id = {user_id}")
        connection.commit()
    except sqlite3.Error as e:
        if connection:
            connection.rollback()
            print("Ошибка при работе с SQLite: обновление отжиманий", e)
    finally:
        if connection:
            connection.close()
            print("Соединение userinfo закрыто")

def get_users_from_userinfo(cursor):
    user = cursor.execute("SELECT user_id FROM userinfo").fetchone()
    while user:
        yield int(user[0])
        user = cursor.fetchone()

def update_users_aim():
    try:
        connection = sqlite_connect()
        curs = connection.cursor()

        for user in get_users_from_userinfo(curs):
            curs.execute(f"SELECT total FROM userinfo WHERE user_id = {user}")
            total = int(curs.fetchone()[0])
            try:
                curs.execute("BEGIN TRANSACTION")
                curs.execute(f"UPDATE userinfo SET aim = {(10000 - total)//dayscalculater.DaysLeft}, done = 0 WHERE user_id = {user}")
                connection.commit()
            except sqlite3.Error:
                if connection:
                    connection.rollback()
                    print("Ошибка обновления цели:",user)
    except sqlite3.Error:
        print("Ошибка подключения")
    finally:
        if connection:
            connection.close()
            print("Обновление целей завершено.")

def get_user_result(user_id:int):
    try:
        connection = sqlite_connect()
        curs = connection.cursor()
        curs.execute(f"SELECT total FROM userinfo WHERE user_id = {user_id}")
        result = int(curs.fetchone()[0])
    except sqlite3.Error:
        print("Ошибка при чтении результата у: ",str(user_id))
    finally:
        if connection:
            connection.close()
            print("Соединение с userinfo закрыто")
    return result

def get_top():
    try:
        connection = sqlite_connect()
        curs = connection.cursor()
        curs.execute(f"SELECT name, total FROM userinfo ORDER BY total DESC LIMIT 3")
        result = list()
        current = curs.fetchone()
        while current:
            result.append(current)
            current = curs.fetchone()
    except sqlite3.Error:
        print("Ошибка при выборки топ 3х в userinfo")
    finally:
        if connection:
            connection.close()
            print("Соединение с userinfo закрыто")
    return result