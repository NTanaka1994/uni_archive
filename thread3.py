from flask import Flask, redirect, render_template, request, session
from werkzeug.security import generate_password_hash as gph
from werkzeug.security import check_password_hash as cph
import sqlite3 as sql
from datetime import timedelta, datetime
import html
import secrets

app = Flask("__main__")
app.secret_key = "abc"
app.permanent_session_lifetime = timedelta(minutes=1200)

@app.route("/")
def route():
    return redirect("signup")

@app.route("/signup", methods=["GET", "POST"])
def singup():
    if request.method == "GET":
        addr = request.remote_addr
        now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        con = sql.connect("data.db")
        cur = con.cursor()
        cur.execute("INSERT INTO log (ip, email, uri, method, time) VALUES (?, ?, ?, ?, ?)", (addr, "Null", "/signup", "GET", now))
        con.commit()
        con.close()
        return render_template("signup.html")
    elif request.method == "POST":
        passwd = request.form["passwd"]
        email = request.form["email"]
        con = sql.connect("data.db")
        cur = con.cursor()
        cur.execute("SELECT email FROM users WHERE email=?", (email,))
        data = []
        for user in cur:
            data.append(user)
        con.close()
        if len(data) == 0:
           con = sql.connect("data.db")
           cur = con.cursor()
           cur.execute("INSERT INTO users (email, passwd) VALUES (?, ?)", (email, gph(passwd)))
           con.commit()
           con.close()
           addr = request.remote_addr
           now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
           con = sql.connect("data.db")
           cur = con.cursor()
           cur.execute("INSERT INTO log (ip, email, uri, method, time) VALUES (?, ?, ?, ?, ?)", (addr, "Null", "/signup", "POST", now))
           con.commit()
           con.close()
           return redirect("login-select")
        else:
            con.close()
            return render_template("signup.html", error="重複")
@app.route("/login")
def login():
    return redirect("login-select")

@app.route("/login-select")
def login_select():
    addr = request.remote_addr
    now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    con = sql.connect("data.db")
    cur = con.cursor()
    cur.execute("INSERT INTO log (ip, email, uri, method, time) VALUES (?, ?, ?, ?, ?)", (addr, "Null", "/login-select", "GET", now))
    con.commit()
    con.close()
    return render_template("login_select.html")

@app.route("/get-login")
def get_login():
    if request.args.get("email") is not None and request.args.get("passwd") is not None:
        passwd = request.args.get("passwd")
        email = request.args.get("email")
        con = sql.connect("data.db")
        cur = con.cursor()
        cur.execute("SELECT passwd FROM users WHERE email=?",(email,))
        data = []
        for hashpass in cur:
            data.append(hashpass)
        con.close()
        if len(data) == 0:
            return render_template("get_login2.html", error="ユーザが存在しません")
        if cph(data[0][0], passwd):
            session["email"] = email
            addr = request.remote_addr
            now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            con = sql.connect("data.db")
            cur = con.cursor()
            cur.execute("INSERT INTO log (ip, email, uri, method, time) VALUES (?, ?, ?, ?, ?)", (addr, session["email"], "/get-login", "GET", now))
            con.commit()
            con.close()
            return redirect("get-success")
        else:
            return render_template("get_login2.html", error="間違っています")
    else:
        addr = request.remote_addr
        now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        con = sql.connect("data.db")
        cur = con.cursor()
        cur.execute("INSERT INTO log (ip, email, uri, method, time) VALUES (?, ?, ?, ?, ?)", (addr, "Null", "/get-login", "GET", now))
        con.commit()
        con.close()
        return render_template("get_login2.html")

@app.route("/post-login", methods=["GET", "POST"])
def post_login():
    if request.method == "POST":
        passwd = request.form["passwd"]
        email = request.form["email"]
        con = sql.connect("data.db")
        cur = con.cursor()
        cur.execute("SELECT passwd FROM users WHERE email=?",(email,))
        data = []
        for hashpass in cur:
            data.append(hashpass)
        con.close()
        if len(data) == 0:
            return render_template("post_login2.html", error="ユーザが存在しません")
        if cph(data[0][0], passwd):
            session["email"] = email
            addr = request.remote_addr
            now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            con = sql.connect("data.db")
            cur = con.cursor()
            cur.execute("INSERT INTO log (ip, email, uri, method, time) VALUES (?, ?, ?, ?, ?)", (addr, session["email"], "/post-login", "POST", now))
            con.commit()
            con.close()
            return redirect("post-success")
        else:
            return render_template("post_login2.html", error="間違っています")
    else:
        addr = request.remote_addr
        now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        con = sql.connect("data.db")
        cur = con.cursor()
        cur.execute("INSERT INTO log (ip, email, uri, method, time) VALUES (?, ?, ?, ?, ?)", (addr, "Null", "/post-login", "GET", now))
        con.commit()
        con.close()
        return render_template("post_login2.html")

@app.route("/get-success", methods=["GET"])
def get_success():
    return render_template("get_success.html")
    

@app.route("/post-success", methods=["GET"])
def post_success():
    return render_template("post_success.html")

@app.route("/home", methods=["GET", "POST"])
def home():
    if "email" in session:
        if request.method == "GET":
            addr = request.remote_addr
            now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            con = sql.connect("data.db")
            cur = con.cursor()
            cur.execute("INSERT INTO log (ip, email, uri, method, time) VALUES (?, ?, ?, ?, ?)", (addr, session["email"], "/home", "GET", now))
            con.commit()
            con.close()
            token = secrets.token_hex()
            session["home"] = token
            con = sql.connect("data.db")
            cur = con.cursor()
            if request.args.get("word") is None:
                cur.execute("SELECT id, title FROM thread ORDER BY id DESC")
            else:
                word = request.args.get("word")
                cur.execute("SELECT id, title FROM thread WHERE title like ? ORDER BY id DESC",("%"+word+"%",))
            res = ""
            for ids, title in cur:
                res += "<a href=thread?id=" + str(ids) +">"+ html.escape(title) + "</a><br>"
            con.close()
            if session["email"] == "aaa@gmail.com":
                return render_template("home.html", res=res, token=token, log="<a href=\"log\">ログ</a>")
            else:
                return render_template("home.html", res=res, token=token)
        elif request.method == "POST":
            if request.form["home"] == session["home"]:
                addr = request.remote_addr
                now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                con = sql.connect("data.db")
                cur = con.cursor()
                cur.execute("INSERT INTO log (ip, email, uri, method, time) VALUES (?, ?, ?, ?, ?)", (addr, session["email"], "/home", "POST", now))
                con.commit()
                con.close()
                title = request.form["title"]
                con = sql.connect("data.db")
                cur = con.cursor()
                cur.execute("INSERT INTO thread (title) VALUES (?)", (title,))
                con.commit()
                con.close()
                return redirect("home")
            else:
                return "<h1>不正なアクセスです</h1>"
    else:
        return redirect("login-select")

@app.route("/thread", methods=["GET", "POST"])
def thread():
    if "email" in session:
        if request.method == "GET":
            addr = request.remote_addr
            now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            con = sql.connect("data.db")
            cur = con.cursor()
            cur.execute("INSERT INTO log (ip, email, uri, method, time) VALUES (?, ?, ?, ?, ?)", (addr, session["email"], "/thread", "GET", now))
            con.commit()
            con.close()
            token = secrets.token_hex()
            session["thread"] = token
            thread_id = request.args.get("id")
            con = sql.connect("data.db")
            cur = con.cursor()
            cur.execute("SELECT team, num FROM comment WHERE thread_id=?", (thread_id,))
            res = ""
            for team, num in cur:
                res += html.escape(team) +"  "+ html.escape(str(num)) + "<br>"
            con.close()
            return render_template("thread.html", res=res, id=thread_id, token=token)
        elif request.method == "POST":
            if request.form["thread"] == session["thread"]:
                addr = request.remote_addr
                now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                con = sql.connect("data.db")
                cur = con.cursor()
                cur.execute("INSERT INTO log (ip, email, uri, method, time) VALUES (?, ?, ?, ?, ?)", (addr, session["email"], "/thread", "POST", now))
                con.commit()
                con.close()
                thread_id = request.form["id"]
                team = request.form["team"]
                num = request.form["num"]
                con = sql.connect("data.db")
                cur = con.cursor()
                cur.execute("INSERT INTO comment (thread_id, team, num) VALUES (?, ?, ?)", (thread_id, team, num))
                con.commit()
                return redirect("thread?id="+html.escape(thread_id))
            else:
                return "<h1>不正なアクセスです</h1>"
    else:
        return redirect("login-select")

@app.route("/logout")
def logout():
    addr = request.remote_addr
    now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    con = sql.connect("data.db")
    cur = con.cursor()
    cur.execute("INSERT INTO log (ip, email, uri, method, time) VALUES (?, ?, ?, ?, ?)", (addr, session["email"], "/logout", "GET", now))
    con.commit()
    con.close()
    session.pop("email", None)
    return redirect("login")

@app.route("/log")
def log():
    if session["email"] == "aaa@gmail.com":
        if request.args.get("ip") is None:
            res = ""
            con = sql.connect("data.db")
            cur = con.cursor()
            cur.execute("SELECT ip FROM log GROUP BY ip")
            for ip in cur:
                res = res + html.escape(str(ip[0])) + "<br>"
            con.close()
            return render_template("log.html", res=res)
        else:
            res = "<table border=\"1\">\n"
            addr = request.args.get("ip")
            con = sql.connect("data.db")
            cur = con.cursor()
            cur.execute("SELECT ip, email, uri, time FROM log WHERE ip LIKE ? ORDER BY time",(addr,))
            for ip, email, uri, time in cur:
                res = res + "<tr><td>" + html.escape(ip) + "</td>\n"
                res = res + "<td>" + html.escape(email) + "</td>\n"
                res = res + "<td>" + html.escape(uri) + "</td>\n"
                res = res + "<td>" + html.escape(time) + "</td></tr>\n"
            res = res + "</table>"
            return render_template("log.html", res=res)
    else:
        return redirect("home")

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=80)
