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
cur.execute("delete from thread")
con.commit()