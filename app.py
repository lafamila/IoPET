from config import query
from flask import Flask, request, session, redirect, render_template, url_for
from flask_socketio import SocketIO, send
import json
import os
import copy
app = Flask(__name__)
socket = SocketIO(app)

@app.route('/chat', methods=['POST'])
def chat():
    
	return render_template('chat.html', hospt_id=session["hospital_id"])


@socket.on("message")
def message(msg):
    req = json.loads(msg)
    print("message : " + msg)
    result = dict()
    if req["type"] == "connect":
        print(req["id"])
        result['message'] = 'New User'
        result['type'] = 'connect'
    else:
        result['message'] = msg
        result['type'] = 'normal'
    send(result, broadcast=True)

@app.route('/login', methods=['POST'])
def login():
    user_id = request.form.get('username')
    user_pw = request.form.get('password')
    q = "SELECT * FROM `hospital` WHERE `HOSPITAL_USER_ID` = %s AND `HOSPITAL_USER_PW` = %s"
    data = query(q, True, False, user_id, user_pw)
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

    return query(q, False, True, pet_id, hospt_id)

@app.route('/load_personal', methods=['POST'])
def personal():
    pet_id = request.form.get('pet_id');
    q = "SELECT * FROM `pet` WHERE `PET_ID` = %s";

    return query(q, True, True, pet_id);

@app.route('/allPerson', methods=['POST'])
def allPerson():
    hospt_id = request.form.get('hospt_id')
    q = "SELECT * FROM `diagnosis` WHERE `HOSPITAL_ID` = %s ORDER BY `DIAGN_DATE` DESC"
    diags = query(q, False, False, hospt_id)

    contents = []

    cache = {}
    for diag in diags:
        pet_id = diag['PET_ID']
        if pet_id in cache:
            pet = cache[pet_id]
        else:
            q = "SELECT * FROM `pet` WHERE `HOSPITAL_ID` = %s AND `PET_ID` = %s"
            pet = query(q, True, False, hospt_id, pet_id)
            cache[pet_id] = pet

        content = copy.deepcopy(pet)
        content['DIAGN_DATE'] = diag['DIAGN_DATE']
        content['DIAGN_NAME'] = diag['DIAGN_NAME']
        contents.append(content)
    return json.dumps(contents)


@app.route('/main', methods=['GET'])
def main():
    if "hospital_id" in session:

        hospt_id = session["hospital_id"];
        q = "SELECT * FROM `hospital` WHERE `HOSPITAL_ID` = %s";
        data = query(q, True, False, hospt_id)

        if data:
            hospt_name = data["HOSPITAL_NAME"]
            pet_id = request.args.get('pet')
            return render_template("main.html", hospt_name=hospt_name, pet_id=pet_id, hospt_id=hospt_id)

    return redirect('/index')

@app.route('/')
def index():
    return render_template("index.html")

@app.route('/load_disease', methods=['POST'])
def disease():
    s = set()
    words = request.form.getlist('word[]')

    for word in words:
        result = query("SELECT * FROM disease_symptom WHERE `SYMPTOME_NAME` LIKE %s", False, False, "%{}%".format(word))
        if len(s) > 0:
            s = s.intersection({r["DISEASE_ID"] for r in result})
        else:
            s = {r["DISEASE_ID"] for r in result}
    return query("SELECT * FROM disease WHERE DISEASE_ID = %s" + " OR DISEASE_ID = %s" * (len(s) - 1), isOne=False, isJson=True, *tuple(s))


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





@app.route('/diag')
def diag():
    return render_template('diag.html')

@app.route('/person')
def person():
    return render_template('person.html', hospt_id=session["hospital_id"])

if __name__ == "__main__":
    app.secret_key = 'A0Zr98j/3yX R~XHH!jmN]LWX/,?RT'
    #app.run(host="0.0.0.0", port=5000)
    # socket.run(app, port=5000, host='0.0.0.0')
    socket.run(app)