from flask import Flask, request
from flaskext.mysql import MySQL
import json
import random, time
import threading

mysql = MySQL()
app = Flask(__name__)
app.config['MYSQL_DATABASE_USER'] = 'root'
app.config['MYSQL_DATABASE_PASSWORD'] = '199358fgm'
app.config['MYSQL_DATABASE_DB'] = 'inst'
app.config['MYSQL_DATABASE_HOST'] = 'localhost'
mysql.init_app(app)

max = 0
min = 0
stars = []

@app.route("/")
def hello():
    return "Hello World!"


@app.route("/wximg/")
def wximg():
    interval_init()
    cursor = mysql.connect().cursor()
    name = request.args.get('name')
    # choose_star = random.choice(stars)
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
    random_star = random.sample(stars, 4)
    j = json.dumps({
        'data': {
            'name': cn_name,
            'imgurl': imgurl,
            'main_page': main_page,
            'random_star':random_star
        }
    })
    cursor.close()
    return j


def interval_init():
    global stars
    cursor = mysql.connect().cursor()
    star_sql = 'select cn_name from star'
    cursor.execute(star_sql)
    for s in cursor.fetchall():
        stars.append(s[0])
    if True:
        global max
        global min
        cursor.execute('SELECT MAX(id) FROM instagram')
        max = cursor.fetchone()[0]
        cursor.execute('SELECT MIN(id) FROM instagram')
        min = cursor.fetchone()[0]
        print 'max:', max, '=====min:', min, '=====len(stars):', str(len(stars))
#        time.sleep(3600)
    cursor.close()


def init_data():
    t = threading.Thread(target=interval_init)
    t.start()


if __name__ == '__main__':
   # init_data()
    app.run(debug=True)
