from iopet_db import init_db, sess
from iopet_models import *

from config import query
from flask import Flask, request, session, redirect, render_template, url_for
from flask_socketio import SocketIO, emit, join_room, leave_room
import json
import os
import copy

app = Flask(__name__)
socket = SocketIO(app)

@app.route('/login', methods=['POST'])
def login():
    user_id = request.form.get('username')
    user_pw = request.form.get('password')
    data = sess.query(Hospital)\
        .filter(Hospital.hospital_user_id==user_id)\
        .filter(Hospital.hospital_user_pw==user_pw)\
        .one()

    if data:
        session['hospital_id'] = data.hospital_id
        return "true"
    else:
        return "false"

@app.route('/main', methods=['GET'])
def main():
    if "hospital_id" in session:

        hospt_id = session["hospital_id"];
        data = sess.query(Hospital) \
            .filter(Hospital.hospital_id == hospt_id) \
            .one()

        hospt_name = data.hospital_name
        pet_id = request.args.get('pet')
        if pet_id:
            return render_template("main.html", hospt_name=hospt_name, pet_id=pet_id, hospt_id=hospt_id)
        else:
            return render_template("main.html", hospt_name=hospt_name, pet_id=1, hospt_id=hospt_id)
    return redirect('/')




@app.route('/petLogin', methods=['POST'])
def petLogin():
    pet_id = request.form.get('pet_id')

    q = "SELECT ROOM_ID FROM `pet` join `chat_room` on pet.PET_ID = chat_room.PET_ID and pet.HOSPITAL_ID = chat_room.HOSPITAL_ID WHERE pet.PET_ID = %s";
    result = query(q, True, True, False, pet_id)

    if result:
        return result["ROOM_ID"], 200

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
    q = "SELECT * FROM `pet` join `chat_room` on pet.PET_ID = chat_room.PET_ID and pet.HOSPITAL_ID = chat_room.HOSPITAL_ID WHERE pet.HOSPITAL_ID = %s AND (pet.PET_NAME LIKE %s or pet.PET_PERSON LIKE %s)"
    result = query(q, True, False, True, hospt_id, "%{}%".format(search), "%{}%".format(search))
    return result if result else ""

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
    if page is None:
        page = 0
    elif type(page) != type(1):
        page = int(page) - 1
    page = page * 12
    q = "SELECT * FROM `diagnosis` a, `pet` b WHERE a.`HOSPITAL_ID` = %s AND b.`HOSPITAL_ID` = %s AND b.`PET_ID` = a.`PET_ID` ORDER BY `DIAGN_DATE` DESC LIMIT  %s, 12"
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




@app.route('/')
def index():
    return render_template("index.html")

@app.route('/insert_diagn', methods=['POST'])
def insertDiagn():
    ks = []
    vs = []
    for k in request.form:
        ks.append("`" + k + "`")
        vs.append(request.form.get(k))
    ks.append("`DIAGN_DATE`")
    ks = ",".join(ks)
    q = "INSERT INTO `diagnosis`({}) VALUES (%s, %s, %s, %s, %s, NOW())".format(ks)
    print(ks)
    print(vs)
    diag_id = query(q, False, False, False, *tuple(vs))
    return ""

@app.route('/insert_pet', methods=['POST'])
def insertPet():
    ks = []
    vs = []
    for k in request.form:
        ks.append("`" + k + "`")
        vs.append(request.form.get(k))
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
    if len(words1) > 0:
        for word in words1:
            print(word)
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





@app.route('/search_disease', methods=['POST'])
def searchDisease():
    word = request.form.get('search')
    result = query("SELECT * FROM disease WHERE `DISEASE_NAME` LIKE %s", True, False, True,
                   "%{}%".format(word))
    if result:
        return result
    return ""

@app.route('/search_medicine', methods=['POST'])
def searchMedicine():
    word = request.form.get('search')
    result = query("SELECT * FROM medicine WHERE `MEDI_NAME` LIKE %s", True, False, True,
                   "%{}%".format(word))
    if result:
        return result
    return ""


@app.route('/load_disease', methods=['POST'])
def disease():
    s = set()
    words2 = request.form.getlist('word2[]')
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
    app.secret_key = 'A0Zr98j/3yX R~XHH!jmN]LWX/,?RT'
    # app.run(host="0.0.0.0", port=5000)
    # socket.run(app, port=5000, host='0.0.0.0')
    socket.run(app, port=5000)



