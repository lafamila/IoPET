import pymysql as db
import json



def query(q, isResult, isOne, isJson, *data):
    conn = db.connect(host='localhost', user='root', passwd='123456789', db='iopet', charset='utf8')
    curs = conn.cursor(db.cursors.DictCursor)
    curs.execute(q, data)

    if isResult:
        rows = curs.fetchall()
        conn.close()

        if not rows:
            return False

        else:
            for row in rows:
                for k, v in row.items():
                    if type(v) == type(bytes(1)):
                        v = int(v)
                    import sys
                    if sys.version_info[0] < 3:
                        if type(v) == type(unicode('x')):
                            v = v.encode('utf-8')
                    if type(v) != type(1) or type(v) != type('1'):
                        row[k] = str(v)
                        row[k] = row[k].decode('utf-8')

        if isOne:
            rows = rows[0]


        if isJson:
            return json.dumps(rows)
        else:
            return rows
    else:
        lastId = curs.lastrowid
        conn.commit()
        conn.close()
        return lastId