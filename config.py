import pymysql as db
import json

def query(q, isOne, isJson, *data):
    conn = db.connect(host='localhost', user='root', passwd='123456789', db='iopet', charset='utf8')
    curs = conn.cursor(db.cursors.DictCursor)
    curs.execute(q, data)

    rows = curs.fetchall()
    conn.close()

    if not rows:
        return False
    elif isOne:
        rows = rows[0]

    if isJson:
        return json.dumps(rows)
    else:
        return rows