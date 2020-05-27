import sqlite3
# import requests
from flask import Flask, render_template, request, redirect, url_for, send_from_directory, session
from werkzeug.utils import secure_filename
import datetime
import os
# from bs4 import BeautifulSoup

app = Flask(__name__)

# 秘密鍵
# app.secret_key = "#4Lghil9Q3bgt0Oolw"

# 画像
UPLOAD_FOLDER = './uploads'
ALLOWED_EXTENSIONS = set(['png', 'jpg', 'gif'])
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['SECRET_KEY'] = os.urandom(24)

def allowed_file(filename):
    return '.' in filename and \
        filename.rsplit('.', 1)[1] in ALLOWED_EXTENSIONS

@app.route('/login')
def log():
    if 'use_id' in session:
        return render_template('mypage.html')
    return '''
        <p>ログインしてください</p>
    '''

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        if username == 'admin':
            session['username'] = request.form['username']
            return redirect(url_for('index'))
        else:
            return '''<p>ユーザー名が違います</p>'''
    return '''
        <form action="" method="post">
            <p><input type="text" name="username">
            <p><input type="submit" value="Login">
        </form>
    '''

@app.route('/logout')
def logout():
    session.pop('user_id', None)
    return render_template("top.index.html")

@app.route('/send', methods=['GET', 'POST'])
def send():
    if request.method == 'POST':
        img_file = request.files['img_file']
        if img_file and allowed_file(img_file.filename):
            filename = secure_filename(img_file.filename)
            img_file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            img_url = '/uploads/' + filename
            return render_template('mypage.html', img_url=img_url)
        else:
            return ''' <p>許可されていない拡張子です</p> '''
    else:
        return redirect(url_for('mypage'))

@app.route('/uploads/<filename>')
def uploaded_file(filename):
    return send_from_directory(app.config['UPLOAD_FOLDER'], filename)


# # スクレイピングの準備
# r = requests.get("http://www.lgbt-kyokai.com/")
# soup = BeautifulSoup(r.content, "html.parser")

# トップ画面の表示及びスクレイピングの結果表示
@app.route("/")
def index():
    # ns = soup.find(class_="newsList").text
    # return render_template('index.html',tpl_ns=ns)
    return render_template('top_login.html')

# マイページ画面の表示
@app.route("/mypage")
def mypage():
    return render_template('mypage.html')


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

# # 掲示板機能
# @app.route("/add", methods=["GET"])
# def add_get():
#     return render_template("add.html")

# @app.route("/add", methods=["POST"])
# def add_post():
#     if "user_id" in session:
#         user_id = session["user_id"]
#     # # 入力フォームに入れられた値を習得して変数に格納
#     name = request.form.get("name")
#     task = request.form.get("task")
#     # DBに接続
#     conn = sqlite3.connect("lgbt.db")
#     c = conn.cursor()
#     #SQL文でDBに変数taskの中身を渡す
#     c.execute("insert into task values(null, ?, ?)",(task,user_id))
#     # 変更を確定して書き込み
#     conn.commit()
#     # DBばいばい
#     c.close()
#     return redirect("/list")

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
    return render_template("top_login.html")

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
        return render_template("top_login.html")

@app.route("/talk")
def talk():
    return render_template("talk.html")

@app.route("/forum")
def forum():
    # session.pop("user_id" , None)
    return render_template("forum.html")

@app.route("/rules")
def rules():
    # session.pop("user_id" , None)
    return render_template("rules.html")


# @app.route("/logout")
# def logout():
#     # session.pop("user_id" , None)
#     return render_template("logout.html")




if __name__ == "__main__":
    app.run(debug=True)