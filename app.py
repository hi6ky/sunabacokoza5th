import sqlite3
import requests
from flask import Flask, request, render_template, redirect, session
import datetime
from bs4 import BeautifulSoup

app = Flask(__name__)

# 秘密鍵
app.secret_key = "#4Lghil9Q3bgt0Oolw"

# # スクレイピングの準備
# r = requests.get("http://www.lgbt-kyokai.com/")
# soup = BeautifulSoup(r.content, "html.parser")

# トップ画面の表示及びスクレイピングの結果表示
@app.route("/")
def index():
    # ns = soup.find(class_="newsList").text
    # return render_template('index.html',tpl_ns=ns)
    return render_template('index.html')


# @app.route("/top", methods=["GET","POST"])
# def top():
#     return "ここはトップページです"

# @app.route("/user/<name>")
# def name(name):
#     return name

# @app.route("/hello/<text>")
# def hello(text):
#     return text + "さんこんにちは"

# @app.route("/temptest")
# def temptest():
#     name = "すなばこ"
#     age = 4
#     address = "沖縄県沖縄市中央1ｰ14ｰ3"
#     return render_template('index.html',tpl_name=name, tpl_age=age, tpl_address=address)

# @app.route("/weather")
# def weather():
#     weather = "さんさんいい天気！"
#     return render_template('weather.html'
#     ,tpl_weather= weather)

# @app.route("/dbtest")
# def dbtest():
#     # flasktest.dbに接続
#     conn = sqlite3.connect("flask_test.db")
#     c = conn.cursor()
#     # SQLでDBにお問い合わせ
#     c.execute("select name, age, address from users where id =1")
#     # 変数に取ってきた値を格納
#     user_info = c.fetchone()
#     # DB接続終了
#     c.close()
#     # とってきた中身を確認
#     print(user_info)
#     # HTML側から取ってきた内容をリスト形式のまま受け渡し
#     return render_template("dbtest.html", tpl_user_info = user_info)

# @app.route("/create_event", methods=["GET"])
# def crev_get():
#     return render_template("create_event.html")

# @app.route("/create_event", methods=["POST"])
# def crev_post():
#     if "user_id" in session:
#         user_id = session["user_id"]
#     # # 入力フォームに入れられた値を習得して変数に格納
#     title = request.form.get("title")
#     cont = request/form/get("content")
#     ut = datetime.datetime.now()
#     # DBに接続
#     conn = sqlite3.connect("lgbt.db")
#     c = conn.cursor()
#     #SQL文でDBに変数taskの中身を渡す
#     c.execute("insert into event values(null, ?, ?)",(event,user_id,cont))
#     # 変更を確定して書き込み
#     conn.commit()
#     # DBばいばい
#     c.close()
#     return "登録完了しました"

# @app.route("/list")
# def task_list():
#     user_id = session["user_id"]
#     conn = sqlite3.connect("flask_test.db")
#     c = conn.cursor()
#     c.execute("select name from user where id = ?", (user_id,))
#     user_name = c.fetchone()[0]
#     c.execute("select id, task from task where user_id = ?",(user_id,))
#     task_list = []
#     for row in c.fetchall():
#         # ダブル型で入ってるidとtaskを取り出してdict型に整形
#         task_list.append({"id":row[0], "task":row[1]})
#     c.close()
#     print(task_list)
#     return  render_template("task_list.html", tpl_user_name = user_name,tpl_task_list = task_list)

# @app.route("/edit/<int:id>")
# def edit(id):
#     conn = sqlite3.connect("flask_test.db")
#     c = conn.cursor()
#     c.execute("select task from task where id = ?", (id,))
#     task = c.fetchone() # ("タスク",)
#     c.close()
#     if task is not None:
#         task = task[0] #("タスク")
#     else:
#         return "存在するidを指定してください。"
#     item = {"id":id, "task":task}
#     return render_template("edit.html", tpl_item = item)

# @app.route("/edit", methods=["post"])
# def update_task():
#     task_id = request.form.get("task_id")
#     task_id = int(task_id)
#     task = request.form.get("task")
#     # SQL分でDBを書き換え
#     conn = sqlite3.connect("flask_test.db")
#     c = conn.cursor()
#     c.execute("update task set task = ? where id =?",(task,task_id))
#     conn.commit()
#     c.close()
#     return redirect("/list")

# @app.route("/del/<int:id>")
# def del_task(id):
#     conn = sqlite3.connect("flask_test.db")
#     c = conn.cursor()
#     c.execute("delete from task where id = ?", (id,))
#     conn.commit()
#     c.close()
#     return redirect("/list")
@app.route("/event_list")
def regist_eventlist():
    return render_template("event_list.html")

@app.route("/regist/", methods=["GET"])
def regist_get():
    if "user_id" in session:
        return "登録に失敗しました"
    else:
        return render_template("regist.html")

@app.route("/regist", methods=["POST"])
def regist_post():
    first = request.form.get("first_name")
    last = request.form.get("last_name")
    idname = request.form.get("id_name")
    password = request.form.get("password")
    email = request.form.get("email")
    ut = datetime.datetime.now()
    conn = sqlite3.connect("lgbt.db")
    c = conn.cursor()
    c.execute("insert into user values(null, ?, ?, ?, ?, ?, ?)", (first,last,idname,password,email,ut))
    conn.commit()
    c.close()
    return render_template("index.html")

@app.route("/login", methods=["GET"])
def login_get():
    if "user_id" in session:
        return "ログインに失敗しました"
    else:
        return render_template("login.html")

@app.route("/login", methods=["POST"])
def login_post():
    idname = request.form.get("id_name")
    password = request.form.get("password")
    conn = sqlite3.connect("lgbt.db")
    c = conn.cursor()
    # ログイン認証：入力されたnameとpassの
    # 組み合わせが存在するか確認
    c.execute("select id from user where id_name = ? and password = ?", (idname,password))
    user_id = c.fetchone()
    c.close()
    if user_id is None:
        # 存在しなければ、再度login.htmlを表示
        return "ログインに失敗しました。再度ログインをやり直してください。"
        return render_template("login.html")
    else:
        # 存在すればログイン
        # sessionを使ってcookieにuser_idを格納する
        session["user_id"] = user_id[0]
        return render_template("index.html")

# @app.route("/logout")
# def logout():
#     session.pop("user_id" , None)
#     return redirect("/login")


if __name__ == "__main__":
    app.run(debug=True)