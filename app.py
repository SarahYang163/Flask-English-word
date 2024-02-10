import requests
from flask import Flask
from flask import render_template, request
import pymysql

from constants import sql_need_display_word, sql_get_ENG
from bs4 import BeautifulSoup as bs

app = Flask(__name__)

connection = pymysql.connect(host='43.138.75.243', user='root', password='pjW;4ymm!tRt', database='web_online_words',
                             cursorclass=pymysql.cursors.DictCursor)


@app.route("/WebOnlineWords")
def index():
    return render_template("index.html")


@app.route("/WebOnlineWords/show/<word>")
def show(word):
    return render_template("show.html", word=word)


@app.route("/add")
def add():
    return render_template("add.html")


@app.route("/WebOnlineWords/api/word", methods=["GET", "POST", "DELETE"])
def api_word():
    offset = int(request.args.get('offset', 0))

    limit = int(request.args.get('limit', 10))
    with connection.cursor() as cursor:
        if request.method == "GET":
            cursor.execute(sql_need_display_word, (limit, offset,))
            print(offset, limit)
            chosen_word = cursor.fetchall()
            print(chosen_word)
            return {"data": chosen_word} if chosen_word else {"data": []}
        elif request.method == "POST":
            word = request.form.get("word")
            print(word)
            response = requests.get("https://dict.youdao.com/search?q={}&keyfrom=new-fanyi.smartResult".format(word))
            soup = bs(response.text, "html.parser")
            data = soup.find("div", {"class": "trans-container"})
            # explain = [i.text for i in data.find_all("li")]
            explain = data.find("li").text
            cursor.execute("update `AllEnglishKnowledge` set `table_name`='ItProfessionWords' where English = %s",
                           (str(word)))
            cursor.execute(
                "INSERT ignore INTO `AllEnglishKnowledge` (`table_name`, `English`, `Chinese` )VALUES('ItProfessionWords', %s, %s)",
                (str(word), str(explain)))
            connection.commit()
            return {"code": 200}
    # elif request.method == "DELETE":
    #     word = request.form.get("word")
    #     words_table.remove(Query().word == word)
    #     return {"code": 204}, 204


@app.route("/WebOnlineWords/api/get-word-data")
def api_get_word_data():
    with connection.cursor() as cursor:
        word = request.args.get("word")
        cursor.execute(sql_get_ENG, str(word))
        chosen_word = cursor.fetchone()
        return {
            "explain": chosen_word,
            "additiona": chosen_word,
            "url": "http://dict.youdao.com"
        }


@app.route("/WebOnlineWords/api/update_score")
def api_update_score():
    with connection.cursor() as cursor:
        word = request.args.get("word")
        size = request.args.get("size")
        cursor.execute(
            'update  AllEnglishKnowledge set score =score+{} , frequency=frequency+1 where Chinese ="{}"'.format(size,
                                                                                                                 word))
        return {"code": 200}


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=84)
