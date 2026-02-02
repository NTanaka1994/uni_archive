import sqlite3 as sql

con = sql.connect("data.db")
cur = con.cursor()
#cur.execute("drop table comment")
#cur.execute("""
#                 create table comment(
#                     id INTEGER PRIMARY KEY AUTOINCREMENT,
#                     thread_id int,
#                     team text,
#                     num text
#                     )
#                 """)
#con.commit()

#-----------ここ必ずやる---------------
#cur.execute("delete from thread")
#cur.execute("delete from comment")
#cur.execute("delete from users")
#cur.execute("delete from log")
#-----------------------------------

#cur.execute("drop table log")
#cur.execute("CREATE TABLE log(ip text, email text, uri text, method text, time datetime)")


#cur.execute("SELECT ip, email, uri, method, time FROM log")
#for ip, email, uri, method, time in cur:
#    print(ip, email, uri, method, time)
con.commit()
con.close()