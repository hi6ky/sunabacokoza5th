import os
# import os.path
# sqlite3(データベース)をimportする
import sqlite3
# flaskにをインポートしてflaskを使えるようにする
from flask import Flask, render_template, request, redirect, url_for, send_from_directory, session
from werkzeug.utils import secure_filename
# datetimeをインポート 本来なら from datetime import datetime になる?? 
import datetime
# BeautifulSoup をインポート
from bs4 import BeautifulSoup
# appにflaskを定義して使えるようにしている。flaskクラスのインスタンスを使って、appという変数に代入している。
app = Flask(__name__)

# flaskでは標準で、Flask.secret_key を設定すると、sessionを使うことができます。この時、Flaskでは session の内容を署名付きで cookie に保存する。
app.secret_key = "#4Lghil9Q3bgt0Oolw"



# ログイン前トップ画面表示のルーティング
@app.route("/")
def index():
    return render_template('top_login.html')


# GET /register => 登録画面を表示
# POST /register => 登録処理をする
@app.route("/regist/", methods=["GET"])
def regist_get():
    if "user_id" in session:
        return "登録に失敗しました。再度登録をやり直して下さい。"
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


# GET  /login => ログイン画面を表示
# POST /login => ログイン処理をする
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
    else:
        # 存在すればログイン
        # sessionを使ってcookieにuser_idを格納する
        session["user_id"] = user_id[0]
        return render_template("top_login.html")


# ログアウト処理
@app.route("/logout")
def logout():
    session.pop("user_id" , None)
    return redirect("/")


# 画像のアップローダー
@app.route('/upload', methods=["POST"])
def do_upload():
    # bbs.tplのinputタグ name="upload" をgetしてくる
    upload = request.files['upload']
    # uploadで取得したファイル名をlower()で全部小文字にして、ファイルの最後尾の拡張子が'.png', '.jpg', '.jpeg'ではない場合、returnさせる。
    if not upload.filename.lower().endswith(('.png', '.jpg', '.jpeg')):
        return 'png,jpg,jpeg形式のファイルを選択してください'
    
    # 下の def get_save_path()関数を使用して "./static/img/" パスを戻り値として取得する。
    save_path = get_save_path()
    # パスが取得できているか確認
    print(save_path)
    # ファイルネームをfilename変数に代入
    filename = upload.filename
    # 画像ファイルを./static/imgフォルダに保存。 os.path.join()は、パスとファイル名をつないで返してくれます。
    upload.save(os.path.join(save_path,filename))
    # ファイル名が取れることを確認、あとで使うよ
    print(filename)
    
    # アップロードしたユーザのIDを取得
    user_id = session['user_id']
    conn = sqlite3.connect('lgbt.db')
    c = conn.cursor()
    # update文
    # 上記の filename 変数ここで使うよ
    c.execute("update user set prof_img = ? where id=?", (filename,user_id))
    conn.commit()
    conn.close()

    return redirect ('/bbs')

def get_save_path():
    path_dir = "./static/img"
    return path_dir


# BBS（とりあえず）
@app.route('/bbs')
def bbs():
    if 'user_id' in session :
        user_id = session['user_id']
        conn = sqlite3.connect('lgbt.db')
        c = conn.cursor()
        # # DBにアクセスしてログインしているユーザ名と投稿内容を取得する
        # クッキーから取得したuser_idを使用してuserテーブルのnameを取得
        c.execute("select first_name,prof_img from user where id = ?", (user_id,))
        # fetchoneはタプル型
        user_info = c.fetchone()
        # user_infoの中身を確認

        # 課題1の答えはここ del_flagが0のものだけ表示する
        # 課題2の答えはここ 保存されているtimeも表示する
        c.execute("select id,comment,time from bbs where userid = ? and del_flag = 0 order by id", (user_id,))
        comment_list = []
        for row in c.fetchall():
            comment_list.append({"id": row[0], "comment": row[1], "time":row[2]})

        c.close()
        return render_template('bbs.html' , user_info = user_info , comment_list = comment_list)
    else:
        return redirect("/login")



@app.route('/add', methods=["POST"])
def add():
    user_id = session['user_id']

    # 課題2の答えはここ 現在時刻を取得
    time = datetime.datetime.now().strftime('%Y/%m/%d %H:%M:%S')

    # POSTアクセスならDBに登録する
    # フォームから入力されたアイテム名の取得(Python2ならrequest.form.getを使う)
    comment = request.form.get("comment")
    conn = sqlite3.connect('lgbt.db')
    c = conn.cursor()
    # 現在の最大ID取得(fetchoneの戻り値はタプル)

    # 課題1の答えはここ null,?,?,0の0はdel_flagのデフォルト値
    # 課題2の答えはここ timeを新たにinsert
    c.execute("insert into bbs values(null,?,?,0,?)", (user_id, comment,time))
    conn.commit()
    conn.close()
    return redirect('/bbs')

def get_save_path():
    path_dir = "./static/img"
    return path_dir


@app.route("/talk")
def talk():
    return render_template("talk.html")


@app.route("/forum")
def forum():
    # session.pop("user_id" , None)
    return render_template("forum.html")


# 利用規約のページのルーティング
@app.route("/rules")
def rules():
    return render_template("rules.html")


# URL間違った時にはこのメッセーシがでる
@app.errorhandler(403)
def mistake403(code):
    return 'There is a mistake in your url!'


# 404 お探しのページはみつかりません
@app.errorhandler(404)
def notfound(code):
    return render_template("404.html")

# ダメ押しのスクレイピング



# おまじない
if __name__ == "__main__":
    app.run(debug=True)