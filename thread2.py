from flask import Flask, redirect, render_template, request, session
from werkzeug.security import generate_password_hash as gph
from werkzeug.security import check_password_hash as cph
import sqlite3 as sql
from datetime import timedelta
import html

app = Flask("__main__")
app.secret_key = "abc"
app.permanent_session_lifetime = timedelta(minutes=1200)

@app.route("/")
def route():
    return redirect("signup")

@app.route("/signup", methods=["GET", "POST"])
def singup():
    if request.method == "GET":
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
           return redirect("login-select")
        else:
            con.close()
            return render_template("signup.html", error="重複")
@app.route("/login")
def login():
    return redirect("login-select")

@app.route("/login-select")
def login_select():
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
            return redirect("get-success")
        else:
            return render_template("get_login2.html", error="間違っています")
    else:
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
            return redirect("post-success")
        else:
            return render_template("post_login2.html", error="間違っています")
    else:
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
            return render_template("home.html", res=res, email=session["email"])
        elif request.method == "POST":
            title = request.form["title"]
            con = sql.connect("data.db")
            cur = con.cursor()
            cur.execute("INSERT INTO thread (title) VALUES (?)", (title,))
            con.commit()
            con.close()
            return redirect("home")
    else:
        return redirect("login-select")

@app.route("/thread", methods=["GET", "POST"])
def thread():
    if "email" in session:
        if request.method == "GET":
           
            thread_id = request.args.get("id")
            con = sql.connect("data.db")
            cur = con.cursor()
            cur.execute("SELECT team, num FROM comment WHERE thread_id=?", (thread_id,))
            res = ""
            for team, num in cur:
                res += html.escape(team) +"  "+ html.escape(str(num)) + "<br>"
            con.close()
            return render_template("thread.html", res=res, id=thread_id)
        elif request.method == "POST":
            thread_id = request.form["id"]
            team = request.form["team"]
            num = request.form["num"]
            con = sql.connect("data.db")
            cur = con.cursor()
            cur.execute("INSERT INTO comment (thread_id, team, num) VALUES (?, ?, ?)", (thread_id, team, num))
            con.commit()
            return redirect("thread?id="+html.escape(thread_id))
    else:
        return redirect("login-select")

@app.route("/logout")
def logout():
    session.pop("email", None)
    return redirect("login")

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=80)
