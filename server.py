import sqlite3
from werkzeug.security import generate_password_hash, check_password_hash

connect = sqlite3.connect('links-base.db', check_same_thread=False)
cursor = connect.cursor()

arrPr = {1: "public",
         2: "protected",
         3: "private"}


def createTables():
    cursor.execute("""CREATE TABLE IF NOT EXISTS "users" (
        "id"	INTEGER NOT NULL,	
        "login" TEXT NOT NULL,
        "password" TEXT NOT NULL,
        PRIMARY KEY("id" AUTOINCREMENT)
    );""")
    connect.commit()

    cursor.execute("""CREATE TABLE IF NOT EXISTS "links" (
        "link"	TEXT NOT NULL,
        "nick"	TEXT NOT NULL,
        "nums" INTEGER NOT NULL,
        "user_id" INTEGER NOT NULL,
        "privacy_id" INTEGER NOT NULL
    );""")
    connect.commit()

    cursor.execute("""CREATE TABLE IF NOT EXISTS "privacy" (
        "id"	INTEGER NOT NULL,
        "name"	TEXT
    );""")
    connect.commit()
    fillPrivacy(arrPr)


def fillPrivacy(arrPr):
    i = 1

    while i < (len(arrPr) + 1):
        # print(arrPr[i])
        res = cursor.execute("""SELECT privacy.name FROM privacy WHERE name=:name""",
                             {"name": arrPr[i]}).fetchone()
        if res == None:
            cursor.execute("""INSERT INTO privacy (id,name) VALUES (:id,:name)""", {"id": i, "name": arrPr[i]})
            connect.commit()
        i += 1


def Registered(login, password):
    # pass_hash=generate_password_hash(password)
    result = cursor.execute("""SELECT users.login FROM users WHERE login=:login""", {"login": login}).fetchone()
    print(result)
    if result == None:
        cursor.execute("""INSERT INTO users (login, password) VALUES (:login,:pass)""",
                       {"login": login, "pass": password})
        connect.commit()
        return True
    else:
        return False


def Autorized(login):
    result = cursor.execute("""SELECT users.password FROM users WHERE login=:login""", {"login": login}).fetchone()
    # print(result)
    return result[0]


def foundUserId(login):
    res = cursor.execute("""SELECT users.id FROM users WHERE login=:login""", {"login": login}).fetchone()
    return res[0]


def addLink(login, link, nick):
    user_id = foundUserId(login)
    result = cursor.execute(
        """INSERT INTO links (link,nick,nums,user_id,privacy_link) VALUES (:link,:nick,:nums,:user_id,:privacy)""",
        {"link": link, "nick": nick, "nums": 0, "user_id": user_id, "privacy": 1})
    connect.commit()
    # print(result)


def checkLinkforUser(login, link):
    user_id = foundUserId(login)
    result = cursor.execute("""SELECT links.link FROM links WHERE link=:link AND user_id=:user_id""",
                            {"link": link, "user_id": user_id}).fetchone()
    if result == None:
        return True
    else:
        return False

# смена никнейма ссылки
def changeNameLink(login, old_nick, new_nick):
    user_id = foundUserId(login)
    result = foundUserLink(user_id, old_nick)
    if result != None:
        cursor.execute("""UPDATE links SET nick=:new_nick WHERE nick=:old_nick""",
                       {"new_nick": new_nick, "old_nick": old_nick})
        connect.commit()
        return True
    else:
        return False


def foundUserLink(user_id, nick):
    result = cursor.execute("""SELECT links.nick FROM links WHERE nick=:nick AND user_id=:user_id""",
                            {"nick": nick, "user_id": user_id}).fetchone()
    return result[0]

def foundLink(nick):
    result = cursor.execute("""SELECT links.nick FROM links WHERE nick=:nick""",
                            {"nick": nick}).fetchone()
    if result !=None:
        return True
    else:return False

# смена приватности ссылки
def changePrivacyLink(login, nick, new_priv):
    user_id = foundUserId(login)
    result = foundUserLink(user_id, nick)
    if result != None:
        cursor.execute("""UPDATE links SET privacy_id=:new_priv WHERE nick=:nick""",
                       {"nick": nick, "new_priv": new_priv})
        connect.commit()
        return True
    else:
        return False

# получение всех ссылок юзера
def getAllUserLinks(login):
    user_id = foundUserId(login)
    res = cursor.execute("""SELECT links.nick FROM links WHERE user_id=:user_id""", {"user_id": user_id}).fetchall()
    # print(res)
    return res



def getPublicLink(nick):
    # user_id = foundUserId(login)
    res = cursor.execute("""SELECT link, privacy_id FROM links WHERE nick=:nick""", {"nick": nick}).fetchone()
    if res[1]==1:
        return res[0]
    else:
        return False

def getPrivateLink(login,nick):
    user_id = foundUserId(login)
    res = cursor.execute("""SELECT links.nick FROM links WHERE user_id=:user_id""", {"user_id": user_id}).fetchall()
    # print(res)
    return res

def getProtectedLink(login,nick):
    user_id = foundUserId(login)
    res = cursor.execute("""SELECT links.nick FROM links WHERE user_id=:user_id""", {"user_id": user_id}).fetchall()
    # print(res)
    return res

