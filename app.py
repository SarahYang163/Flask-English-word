import requests
from flask import Flask
from flask import render_template, request
import pymysql

from constants import sql_need_display_word, sql_get_ENG
from bs4 import BeautifulSoup as bs
from utils.log import setup_logger
import logging
from config.setting import SERVER_PORT
from utils.mysql import db

app = Flask(__name__)

# connection = pymysql.connect(host='43.138.75.243', user='root', password='pjW;4ymm!tRt', database='web_online_words',
#                              cursorclass=pymysql.cursors.DictCursor)

# 设置访问日志
access_logger = setup_logger('access_logger', 'logs/access.log', level=logging.INFO)
# 设置错误日志
error_logger = setup_logger('error_logger', 'logs/error.log', level=logging.ERROR)


@app.route("/WebOnlineWords/")
def index():
    return render_template("index.html")


@app.route("/WebOnlineWords/show/<word>")
def show(word):
    return render_template("show.html", word=word)


@app.route("/WebOnlineWords/add")
def add():
    return render_template("add.html")


@app.route("/WebOnlineWords/delete")
def delete():
    return render_template("delete.html")


@app.route("/WebOnlineWords/api/word", methods=["GET", "POST", "DELETE"])
def api_word():
    offset = int(request.args.get('offset', 0))
    limit = int(request.args.get('limit', 10))
    if request.method == "GET":
        access_logger.info(f'offset: {offset}, limit:{limit}')
        chosen_word = db.select_db(sql_need_display_word.format(limit, offset))
        access_logger.info(f'chosen_word: {chosen_word}')
        return {"data": chosen_word} if chosen_word else {"data": []}
    elif request.method == "POST":
        word = request.form.get("word")
        access_logger.info(f'word: {word}')
        response = requests.get("https://dict.youdao.com/search?q={}&keyfrom=new-fanyi.smartResult".format(word))
        soup = bs(response.text, "html.parser")
        data = soup.find("div", {"class": "trans-container"})
        # explain = [i.text for i in data.find_all("li")]
        explain = data.find("li").text
        db.execute_db(
            "update `AllEnglishKnowledge` set `table_name`='ItProfessionWords' where English = {}".format(str(word)))
        db.execute_db(
            "INSERT ignore INTO `AllEnglishKnowledge` (`table_name`, `English`, `Chinese` )VALUES('ItProfessionWords', %s, %s)".format(
                str(word), str(explain)))
        return {"code": 200}
    elif request.method == "DELETE":
        word = request.form.get("word")
        db.execute_db("delete FROM AllEnglishKnowledge where English='{}'".format(word))
        access_logger.info(f'delete word: {word}')
        return {"code": 204}, 204


@app.route("/WebOnlineWords/api/get-word-data")
def api_get_word_data():
    word = request.args.get("word")
    chosen_word = db.execute_db(sql_get_ENG.format(str(word)))
    return {
        "explain": chosen_word,
        "additiona": chosen_word,
        "url": "http://dict.youdao.com"
    }


@app.route("/WebOnlineWords/api/update_score")
def api_update_score():
    word = request.args.get("word")
    size = request.args.get("size")
    db.execute_db(
        'update  AllEnglishKnowledge set score =score+{} , frequency=frequency+1 where Chinese ="{}"'.format(size,
                                                                                                             word))
    access_logger.info(f'update {word} score: {size}')
    return {"code": 200}


if __name__ == "__main__":
    app.run(debug=True, port=SERVER_PORT)
