from flask import Flask, render_template, jsonify, request, session, redirect, url_for, make_response

app = Flask(__name__)

from pymongo import MongoClient

client = MongoClient('mongodb+srv://test:sparta@cluster0.lpapihe.mongodb.net/?retryWrites=true&w=majority')
db = client.dbsparta

SECRET = "musical"

import jwt
import datetime
import hashlib

@app.route("/")
def indexRender():
  return render_template("index.html")

@app.route("/join")
def joinRender():
  return render_template("join.html")

# 토큰 있니?
@app.route("/test")
def testRender():
  token = request.cookies.get("token")
  try:
    payload = jwt.decode(token, SECRET, algorithms = ["HS256"])
    user = db.users.find_one({ "email": payload["email"] })
    print(user["email"])
    return jsonify({ "result": "success" })
  except jwt.exceptions.DecodeError:
    return jsonify({ "result": "fail" })
#

@app.route("/main")
def mainRender():
  token = request.cookies.get("token")
  try:
    payload = jwt.decode(token, SECRET, algorithms = ["HS256"])
    user = db.users.find_one({ "email": payload["email"] })
    musical_list = list(db.musical_main.find({}, {'_id': False}).limit(28))
    return render_template("main.html", musicals=musical_list, username=payload['email'])

  except jwt.exceptions.DecodeError:
    return redirect("/?error=토큰 없음")

@app.route("/auth/join", methods = ["post"])
def authJoin():
  reqEmail = request.form["email"]
  reqPassword= request.form["password"]
  hash = hashlib.sha256(reqPassword.encode("utf-8")).hexdigest()
  db.users.insert_one({ "email": reqEmail, "password": hash })
  return redirect("/")

@app.route("/auth/login", methods = ["post"])
def authLogin():
  reqEmail = request.get_json()["email"]
  reqPassword = request.get_json()["password"]
  hash = hashlib.sha256(reqPassword.encode("utf-8")).hexdigest()
  user = db.users.find_one({ "email": reqEmail, "password": hash })
  if user:
    payload = {
      "email": reqEmail,
    }
    token = jwt.encode(payload, SECRET, algorithm = "HS256" )
    return make_response(jsonify({ "result": "success", "token": token }), 200)
  else:
    return jsonify({ "result": "success", "message": "비번 불일치"})

@app.route("/auth/logout", methods = ["get"])
def authLogout():
  resp = make_response(redirect("/"))
  resp.delete_cookie("token")
  return resp

@app.route("/auth/check", methods  = ["post"])
def authCheck():
  reqEmail = request.get_json()["email"]
  check = db.users.find_one({ "email": reqEmail }, { "_id": False })
  if check:
    print("있습니다.")
    return make_response(jsonify({ "result": "exist" }), 200)
  else:
    print("없습니다.")
    return make_response(jsonify({ "result": "success" }), 200)

if __name__ == '__main__':
    app.run('0.0.0.0', port=5000, debug=True)