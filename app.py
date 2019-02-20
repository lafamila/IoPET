from config import query
from flask import Flask, request, session, redirect, render_template, url_for
from flask_socketio import SocketIO, emit, join_room, leave_room
import json
import os
import copy
app = Flask(__name__)

app.secret_key = 'A0Zr98j/3yX R~XHH!jmN]LWX/,?RT'
app.config['UPLOAD_FOLDER'] = "./static/picture/"
app.config['SESSION_TYPE'] = 'filesystem'

socket = SocketIO(app)
import colorsys
from PIL import Image
from math import *

TYPE1 = [2, 0, 3, 5, 4, 4, 3, 1, 3]
TYPE2 = [4, 0, 2, 2, 2, 3, 3, 3, 3]
TYPE3 = [3, 1, 4, 2, 1, 4, 3, 3, 3]
TYPE4 = [0, 2, 3, 5, 4, 1, 1, 3, 3]
TYPE5 = [1, 4, 0, 3, 4, 1, 1, 1, 3]
TYPES = [TYPE1, TYPE2, TYPE3, TYPE4, TYPE5]


def getHSV(img):
    h, s, v = 0, 0, 0
    for i in range(22, 32):
        for j in range(22, 32):
            rr, gg, bb = img.getpixel((i, j))
            hh, ss, vv = colorsys.rgb_to_hsv(rr / 255., gg / 255., bb / 255.)
            h += hh
            s += ss
            v += vv
    h = h / 100
    s = s / 100
    v = v / 100
    return 100 * h, 100 * s, 100 * v


def getCropped(name):
    img = Image.open(name)

    area = (900, 100, 3132, 2924)
    crop = img.crop(area)

    p = 165
    sx = 150
    sy = 585
    ty = 55
    tx = 75
    # blank = (tx+p)/2 + 15
    col = []

    for j in range(9):
        row = []
        for i in range(3):
            row.append(crop.crop((sx, sy, sx + p, sy + p)).crop((p / 3, p / 3, 2 * p / 3, 2 * p / 3)))
            sx = sx + p + tx

        sx = sx + 2 * p
        for i in range(3):
            row.append(crop.crop((sx, sy, sx + p, sy + p)).crop((p / 3, p / 3, 2 * p / 3, 2 * p / 3)))
            sx = sx + p + tx

        col.append(row)
        sx = 150
        sy = sy + p + ty
    return col


def getCenter(name):
    img = Image.open(name)

    area = (1984, 265, 2098, 2924)
    crop = img.crop(area)
    col = []
    sy = 0
    for i in range(9):
        col.append(crop.crop((0, sy, 114, sy + 171)))
        sy += 251
    return col


def getCode(res, col):
    code = []
    for i in range(9):
        diff = []
        for j in range(6):
            diff.append(abs(getHSV(res[i])[0] - getHSV(col[i][j])[0]))

        code.append(diff.index(min(diff)))
    return code


def square_rooted(x):
    return round(sqrt(sum([a * a for a in x])), 3)


def cosine_similarity(x, y):
    numerator = sum(a * b for a, b in zip(x, y))
    denominator = square_rooted(x) * square_rooted(y)
    return round(numerator / float(denominator), 3)


def getType(x):
    res = []
    for t in TYPES:
        res.append(cosine_similarity(x, t))
    return res.index(max(res))


@app.route('/petType', methods=['POST'])
def petType():

    file = request.files["lafamila"]
    filename = "tmp"
    print(os.path.join(app.config['UPLOAD_FOLDER'], filename))
    file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
    name = os.path.join(app.config['UPLOAD_FOLDER'], filename)
    col = getCropped(name)
    res = getCenter(name)
    x = getCode(res, col)
    return x

@app.route('/petJoin', methods=['POST'])
def petJoin():
    user_id = request.form.get("id").encode('utf-8')
    user_pw = request.form.get("pw").encode('utf-8')
    pet = request.form.get("pet").encode('utf-8')
    name = request.form.get("name").encode('utf-8')
    phone = request.form.get("phone").encode('utf-8')
    hospital = request.form.get("hospital").encode('utf-8')

    if "-" not in phone:
        st = 0
        ed = len(phone) % 4
        result = []
        while ed < len(phone):
            result.append(phone[st:ed])
            st = ed
            ed += 4
        result.append(phone[st:ed])
        phone = "-".join(result)
    q = "SELECT PET_ID FROM `pet` WHERE PET_NAME = %s AND PET_PERSON = %s AND PET_CONTACT = %s AND HOSPITAL_ID = %s"
    result = query(q, True, True, False, pet, name, phone, hospital)
    if not result:
        return "pet"


    pet_id = result["PET_ID"]

    q = "SELECT * FROM `user` WHERE PET_ID = %s"
    result = query(q, True, True, False, pet_id)
    if result:
        return "already"

    q = "INSERT INTO `user` VALUES (%s, %s, %s)"
    try:
        diag_id = query(q, False, False, False, user_id, user_pw, pet_id)
    except:
        return "already"
    return pet_id

@app.route('/petLoginApp', methods=['POST'])
def petLoginAPP():
    user_id = request.form.get("id").encode('utf-8')
    user_pw = request.form.get("pw").encode('utf-8')

    q = "SELECT * FROM `user` WHERE USER_ID = %s AND USER_PW = %s"
    result = query(q, True, True, False, user_id, user_pw)
    if not result:
        q = "SELECT * FROM `doctor` WHERE DOCTOR_ID = %s AND DOCTOR_PW = %s"
        result = query(q,True, True, False, user_id, user_pw)
        if not result:
            return "error"
        else:
            return "0"
    pet_id = result["PET_ID"]
    return pet_id

@app.route('/petChatApp', methods=['POST'])
def petChatApp():
    pet_id = request.form.get('pet_id')
    result = query("SELECT `PET_ID` FROM `chat_room` WHERE ROOM_ID = %s", True, True, False, pet_id)
    if result:
        pet_id = result["PET_ID"]
    else:
        return "6", 200
    q = "UPDATE `pet` SET PET_CHAT = PET_CHAT + 1 WHERE PET_ID = %s";
    query(q, False, False, False, pet_id)
    q = "SELECT PET_CHAT FROM `pet` WHERE PET_ID = %s";
    result = query(q, True, True, False, pet_id)
    if result:
        return result["PET_CHAT"], 200
    else:
        return "6", 200

    return ""
@app.route('/petLogin', methods=['POST'])
def petLogin():
    pet_id = request.form.get('pet_id');
    q = "SELECT ROOM_ID FROM `pet` join `chat_room` on pet.PET_ID = chat_room.PET_ID and pet.HOSPITAL_ID = chat_room.HOSPITAL_ID WHERE pet.PET_ID = %s";
    result = query(q, True, True, False, pet_id)

    if result:
        return result["ROOM_ID"], 200
    elif int(pet_id) == 0:
        return "0", 200
    return "", 404

@app.route('/chatList', methods=['POST'])
def getChat():
    room_id = request.form.get('room_id')
    q = "SELECT * FROM `chat` WHERE `ROOM_ID` = %s ORDER BY `CHAT_DATETIME`"
    result = query(q, True, False, True, room_id)
    if result:
        return result, 200
    else:
        return "", 404

@app.route('/chat_search', methods=['POST'])
def getChatSearched():
    hospt_id = session["hospital_id"]
    search = request.form.get('keyword')
    if search:
        search = search.encode('utf-8')
    q = "SELECT * FROM `pet` join `chat_room` on pet.PET_ID = chat_room.PET_ID and pet.HOSPITAL_ID = chat_room.HOSPITAL_ID WHERE pet.HOSPITAL_ID = %s AND (pet.PET_NAME LIKE %s or pet.PET_PERSON LIKE %s)"
    result = query(q, True, False, True, hospt_id, "%{}%".format(search), "%{}%".format(search))
    return result if result else ""

@app.route('/uploadImage', methods=['POST', 'GET'])
def uploadImage():
    file = request.files["lafamila"]
    filename = file.filename.split("/")[-1]
    filename = secure_filename(filename)
    print(os.path.join(app.config['UPLOAD_FOLDER'], filename))
    file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
    return os.path.join(app.config['UPLOAD_FOLDER'], filename)

@app.route('/memo', methods=['GET'])
def memo():
    iid = request.args.get('id')
    if iid != '0':

        result = query('SELECT * FROM stock WHERE `STOCK_ID` = %s', True, True, False, iid)
        return render_template('memo.html', iid=iid, title=result["STOCK_NAME"], content=result["STOCK_PRICE"], types=result["STOCK_TYPE"])
    else:
        return render_template('memo.html')


@app.route('/chat', methods=['GET'])
def chat():
    hospt_id = session["hospital_id"]
    pet_id = request.args.get('pet')
    q = "SELECT * FROM `pet` join `chat_room` on pet.PET_ID = chat_room.PET_ID and pet.HOSPITAL_ID = chat_room.HOSPITAL_ID WHERE pet.HOSPITAL_ID = %s";
    result = query(q, True, False, False, hospt_id)

    if result:
        room_id = None
        for i in result:
            last = query("SELECT * FROM `chat` WHERE `ROOM_ID` = %s ORDER BY `CHAT_DATETIME` DESC LIMIT 1", True, True, False, i["ROOM_ID"])
            i["LAST"] = last["CHAT_MESSAGE"] if last else ""
            if last:
                if last["CHAT_SEND"] == "0":
                    i["NEW"] = False
                elif last["CHAT_READ"] == "1":
                    i["NEW"] = True
                else:
                    i["NEW"] = False
            else:
                i["NEW"] = False
            if i["PET_ID"] == pet_id:
                room_id = i["ROOM_ID"]
        return render_template('chat.html', hospt_id=session["hospital_id"], rooms=result, room_id=room_id)
    else:
        return "<h1>Wrong Pet ID</h1>"

@socket.on('join')
def on_join(data):
    room = data['room_id']
    receive = 1 if data["sender"] == "hospt" else 0
    print(room)
    print(receive)
    last = query(
        "SELECT `CHAT_DATETIME` FROM `chat` WHERE `CHAT_SEND` = %s AND `ROOM_ID` = %s ORDER BY `CHAT_DATETIME` DESC LIMIT 1",
        True, True, False, receive, room)
    if last:
        query("UPDATE `chat` SET `CHAT_READ` = 0 WHERE `ROOM_ID` = %s AND `CHAT_DATETIME` <= %s", False, False, False, room, last["CHAT_DATETIME"])
    join_room(room)


@socket.on('leave')
def on_leave(data):
    room = data['room_id']
    leave_room(room)


@socket.on("message")
def message(data):
    q = "INSERT INTO `chat`(`ROOM_ID`, `CHAT_SEND`, `CHAT_TYPE`, `CHAT_MESSAGE`, `CHAT_DATETIME`) VALUES (%s, %s, %s, %s, now())"
    room_id = data["room_id"]
    sender = 0 if data["sender"] == 'hospt' else 1
    text = 0 if data["type"] == 'text' else 1
    query(q, False, False, False, room_id, sender, text, data["message"])
    if sender == 0:
        emit('received', data, room=room_id, broadcast=True)
    else:
        emit('received', data, broadcast=True)

@app.route('/login', methods=['POST'])
def login():
    user_id = request.form.get('username').encode('utf-8')
    user_pw = request.form.get('password').encode('utf-8')
    q = "SELECT * FROM `hospital` WHERE `HOSPITAL_USER_ID` = %s AND `HOSPITAL_USER_PW` = %s"
    data = query(q, True, True, False, user_id, user_pw)
    if data:
        session['hospital_id'] = data["HOSPITAL_ID"]
        return "true";
    else:
        return "false";


@app.route('/load_diagnosis', methods=['POST'])
def diagnosis():
    pet_id = request.form.get('pet_id')
    hospt_id = request.form.get('hospt_id')
    q = "SELECT * FROM `diagnosis` WHERE `PET_ID` = %s AND `HOSPITAL_ID` = %s"
    result = query(q, True, False, True, pet_id, hospt_id)
    return result if result else ""


@app.route('/load_personal', methods=['POST'])
def personal():
    pet_id = request.form.get('pet_id');
    q = "SELECT * FROM `pet` WHERE `PET_ID` = %s";
    result = query(q, True, True, True, pet_id)
    return result if result else ""


@app.route('/allPerson', methods=['POST'])
def allPerson():
    hospt_id = request.form.get('hospt_id')
    page = request.form.get('page')
    search = request.form.get('search')
    if search:
        search = search.encode('utf-8')
    if page is None:
        page = 0
    elif type(page) != type(1):
        page = int(page) - 1
    page = page * 12

    qs = ""
    if search is not None:
        qs = "(b.`PET_NAME` LIKE %s OR b.`PET_PERSON` LIKE %s OR b.`PET_SPEC` LIKE %s) AND "
    print(qs)
    print(search)
    if request.form.get('ltype') == "in":
        q = "SELECT * FROM `diagnosis` a, `pet` b WHERE "+qs+"a.`HOSPITAL_ID` = %s AND b.`HOSPITAL_ID` = %s AND b.`PET_ID` = a.`PET_ID` AND b.`PET_ADMS`=1 ORDER BY `DIAGN_DATE` DESC LIMIT  %s, 12"
    else:
        q = "SELECT * FROM `diagnosis` a, `pet` b WHERE "+qs+"a.`HOSPITAL_ID` = %s AND b.`HOSPITAL_ID` = %s AND b.`PET_ID` = a.`PET_ID` ORDER BY `DIAGN_DATE` DESC LIMIT  %s, 12"
    if search is not None:
        diags = query(q, True, False, False, "%{}%".format(search), "%{}%".format(search), "%{}%".format(search), hospt_id, hospt_id, page)
    else:
        diags = query(q, True, False, False, hospt_id, hospt_id, page)
    if diags:
        # if request.form.get('num'):
        #     size = len(query("SELECT * FROM `diagnosis` WHERE `HOSPITAL_ID` = %s", True, False, False, hospt_id))
        #     contents.append(size)
        return json.dumps(diags)
    return json.dumps([])


@app.route('/join', methods=['GET'])
def join():
    if "hospital_id" in session:
        hospt_id = session["hospital_id"];
        return render_template("join.html", hospt_id=hospt_id)

    return redirect('/')


@app.route('/main', methods=['GET'])
def main():
    if "hospital_id" in session:

        hospt_id = session["hospital_id"];
        q = "SELECT * FROM `hospital` WHERE `HOSPITAL_ID` = %s";
        data = query(q, True, True, False, hospt_id)

        if data:
            hospt_name = data["HOSPITAL_NAME"]
            pet_id = request.args.get('pet')
            if pet_id:
                return render_template("main.html", hospt_name=hospt_name, pet_id=pet_id, hospt_id=hospt_id)
            else:
                return render_template("main.html", hospt_name=hospt_name, pet_id=1, hospt_id=hospt_id)
    return redirect('/')


@app.route('/')
def index():
    return render_template("index.html")

@app.route('/insert_memo', methods=['POST'])
def insertMemo():
    title = request.form.get("title").encode('utf-8')
    type = request.form.get("type").encode('utf-8')
    content = request.form.get("content").encode('utf-8')
    q = "INSERT INTO `stock`(`STOCK_TYPE`, `STOCK_NAME`, `STOCK_PRICE`, `STOCK_TIME`) VALUES (%s, %s, %s, DATE(NOW()))"
    diag_id = query(q, False, False, False, type, title, content)
    return ""


@app.route('/update_memo', methods=['POST'])
def updateMemo():
    iid = request.form.get("iid")
    title = request.form.get("title").encode('utf-8')
    type = request.form.get("type").encode('utf-8')
    content = request.form.get("content").encode('utf-8')
    q = "UPDATE `stock` SET `STOCK_TYPE`=%s, `STOCK_NAME`=%s, `STOCK_PRICE`=%s, `STOCK_TIME`=DATE(NOW()) WHERE `STOCK_ID`=%s"

    diag_id = query(q, False, False, False, type, title, content, iid)
    return ""

@app.route('/insert_diagn', methods=['POST'])
def insertDiagn():
    ks = []
    vs = []
    for k in request.form:
        ks.append("`" + k + "`")
        vs.append(request.form.get(k).encode('utf-8'))
    ks.append("`DIAGN_DATE`")
    ks = ",".join(ks)
    q = "INSERT INTO `diagnosis`({}) VALUES (%s, %s, %s, %s, %s, NOW())".format(ks)
    diag_id = query(q, False, False, False, *tuple(vs))
    return ""

@app.route('/insert_pet', methods=['POST'])
def insertPet():
    ks = []
    vs = []
    for k in request.form:
        ks.append("`" + k + "`")
        vs.append(request.form.get(k).encode('utf-8'))
    ks = ",".join(ks)
    q = "INSERT INTO `pet`({}) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)".format(ks)
    pet_id = query(q, False, False, False, *tuple(vs))

    q = "INSERT INTO `chat_room`(`HOSPITAL_ID`, `PET_ID`) VALUES (%s, %s)"
    chat_room = query(q, False, False, False, vs[9], pet_id)
    return "success"

@app.route('/load_medicine_by_id', methods=['POST'])
def medicineID():
    iid = request.form.get('iid')


    result = query("SELECT * FROM medicine WHERE MEDI_ID = %s",
                   True, True, True, iid)
    return result if result else ""


@app.route('/load_medicine', methods=['POST'])
def medicine():
    s = set()
    words1 = request.form.getlist('word1[]')
    words1 = [w.encode('utf-8') for w in words1]
    corpus = set()



    if len(words1) > 0:
        for word in words1:
            result = query("SELECT * FROM disease_medicine WHERE `DISEASE_ID` = %s", True, False, False, word)
            if result:
                if len(s) > 0:
                    s = s.union({r["MEDI_ID"] for r in result})
                else:
                    s = {r["MEDI_ID"] for r in result}
            else:
                continue
        result = query("SELECT * FROM medicine WHERE MEDI_ID = %s" + " OR MEDI_ID = %s" * (len(s) - 1),
                       True, False, True, *tuple(s))
        return result if result else ""

    return ""


@app.route('/search_stock', methods=['POST'])
def searchStock():
    word = request.form.get('search')
    word = word.encode('utf-8')
    types = request.form.get('type')
    types = types.encode('utf-8')

    if types == "0":
        q = " WHERE 1 "
    elif types == "1":
        q = " WHERE `STOCK_TYPE` = 1 "
    else:
        q = " WHERE `STOCK_TYPE` = 0 "

    if len(word) == 0:
        result = query('SELECT * FROM stock' + q + 'ORDER BY `STOCK_TIME` DESC', True, False, True)
    else :
        result = query('SELECT * FROM stock' + q + 'AND (`STOCK_NAME` LIKE %s OR `STOCK_PRICE` LIKE %s) ORDER BY `STOCK_TIME` DESC', True, False, True, "%{}%".format(word), "%{}%".format(word))
    return result if result else "{}"
@app.route('/delete_stock', methods=['POST'])
def deleteStock():
    iid = request.form.get('id')
    print(iid)
    query('DELETE FROM stock WHERE `STOCK_ID` = %s', False, False, False, iid)
    return "success"

@app.route('/search_disease', methods=['POST'])
def searchDisease():
    word = request.form.get('search')
    word = word.encode('utf-8')
    result = query("SELECT * FROM disease WHERE `DISEASE_NAME` LIKE %s", True, False, True,
                   "%{}%".format(word))
    if result:
        return result
    return ""

# @app.route('/search_symptom', methods=['POST'])
# def searchSymptom():
#     word = request.form.get('search')
#     word = word.encode('utf-8')
#     corpus = []
#     try:
#         for i in similar_words(word):
#             corpus.append(i[0])
#         return json.dumps(corpus)
#     except:
#         return ""


@app.route('/search_medicine', methods=['POST'])
def searchMedicine():
    word = request.form.get('search')
    word = word.encode('utf-8')
    result = query("SELECT * FROM medicine WHERE `MEDI_NAME` LIKE %s", True, False, True,
                   "%{}%".format(word))
    if result:
        return result
    return ""


@app.route('/load_disease', methods=['POST'])
def disease():
    s = set()
    words2 = request.form.getlist('word2[]')
    words2 = [w.encode('utf-8') for w in words2]

    if len(words2) > 0:
        for word in words2:
            result = query("SELECT * FROM disease_symptom WHERE `SYMPTOME_NAME` LIKE %s", True, False, False,
                           "%{}%".format(word))
            if result:
                if len(s) > 0:
                    s = s.intersection({r["DISEASE_ID"] for r in result})
                else:
                    s = {r["DISEASE_ID"] for r in result}
            else:
                continue
        result = query("SELECT * FROM disease WHERE DISEASE_ID = %s" + " OR DISEASE_ID = %s" * (len(s) - 1), True,
                       False, True, *tuple(s))
        return result if result else ""
    return ""


@app.context_processor
def override_url_for():
    return dict(url_for=dated_url_for)


def dated_url_for(endpoint, **values):
    if endpoint == 'static':
        filename = values.get('filename', None)
        if filename:
            file_path = os.path.join(app.root_path,
                                     endpoint, filename)
            values['q'] = int(os.stat(file_path).st_mtime)
    return url_for(endpoint, **values)


@app.route('/diag', methods=['GET'])
def diag():
    if "hospital_id" in session:

        hospt_id = session["hospital_id"];
        q = "SELECT * FROM `hospital` WHERE `HOSPITAL_ID` = %s";
        data = query(q, True, True, False, hospt_id)

        if data:
            hospt_name = data["HOSPITAL_NAME"]
            pet_id = request.args.get('pet')
            return render_template('diag.html', hospt_name=hospt_name, pet_id=pet_id, hospt_id=hospt_id)

    return redirect('/')
@app.route('/disease', methods=['POST'])
def diseaseByID():
    disease_id = request.form.get('disease_id')
    q = "SELECT * FROM `disease` WHERE `DISEASE_ID` = %s";
    data = query(q, True, True, True, disease_id)
    return data if data else ""


@app.route('/person')
def person():
    return render_template('person.html', hospt_id=session["hospital_id"])


if __name__ == "__main__":
    # app.run(host="0.0.0.0", port=5000)
    # socket.run(app, port=5000, host='127.0.0.1')
    socket.run(app, port=5000, host='0.0.0.0')
    # socket.run(app, debug=True)
