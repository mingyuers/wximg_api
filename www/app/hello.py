from flask import Flask, request
from flaskext.mysql import MySQL
import json
import random, time, copy
import threading

mysql = MySQL()
app = Flask(__name__)
app.config['MYSQL_DATABASE_USER'] = 'root'
app.config['MYSQL_DATABASE_PASSWORD'] = '199358fgm'
app.config['MYSQL_DATABASE_DB'] = 'inst'
app.config['MYSQL_DATABASE_HOST'] = 'localhost'
mysql.init_app(app)

size = 20


@app.route("/")
def hello():
    return "Hello World!"


@app.route("/wximg/")
def wximg():
    global size
    cursor = mysql.connect().cursor()
    max, min, stars = interval_init(cursor)
    name = request.args.get('name')
    datas = []
    for i in range(size):
        one = get_one_data(max, min, stars, cursor)
        datas.append(one)
    j = json.dumps({
        'data': datas
    })
    cursor.close()
    return j


def get_one_data(max, min, stars, cursor):
    target_id = int((max - min) * random.random() + min)
    sql = 'SELECT name,qiniu_url,id FROM instagram WHERE id = ' + str(target_id) + ' ORDER BY id LIMIT 1;'
    cursor.execute(sql)
    result = cursor.fetchone()
    imgurl = result[1]
    en_name = result[0]
    sql2 = 'SELECT cn_name,main_page FROM star WHERE en_name = "' + en_name + '"'
    cursor.execute(sql2)
    result2 = cursor.fetchone()
    cn_name = result2[0]
    main_page = result2[1]
    small_stars = copy.copy(stars)
    small_stars.remove(cn_name)
    random_star = random.sample(small_stars, 3)
    url_type = 'mp4' if ('.mp4' in imgurl) else 'jpg'
    one = {
        'name': cn_name,
        'imgurl': imgurl,
        'main_page': main_page,
        'random_star': random_star,
        'type': url_type
    }
    return one


def interval_init(cursor):
    max = 0
    min = 0
    stars = []
    star_sql = 'select cn_name from star'
    cursor.execute(star_sql)
    for s in cursor.fetchall():
        stars.append(s[0])
    cursor.execute('SELECT MAX(id) FROM instagram')
    max = cursor.fetchone()[0]
    cursor.execute('SELECT MIN(id) FROM instagram')
    min = cursor.fetchone()[0]
    # print 'max:', max, '=====min:', min, '=====len(stars):', str(len(stars))
    return max, min, stars


if __name__ == '__main__':
    app.run(debug=True)
