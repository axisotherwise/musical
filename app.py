@app.route("/main")
def mainRender():
  token = request.cookies.get("token")
  print(token)
  try:
    payload = jwt.decode(token, SECRET, algorithms = ["HS256"])
    user = db.users.find_one({ "email": payload["email"] })
    return render_template("main.html", email = user["email"])
  except jwt.exceptions.DecodeError:
    return redirect("/?error=토큰 없음")  

@app.route("/auth/login", methods = ["post"])
def authLogin():
  reqEmail = request.get_json()["email"]
  reqPassword = request.get_json()["password"]
  print(reqEmail, reqPassword)
  hash = hashlib.sha256(reqPassword.encode("utf-8")).hexdigest()
  user = db.users.find_one({ "email": reqEmail, "password": hash })
  if user:
    payload = {
      "email": reqEmail,
    }
    token = jwt.encode(payload, SECRET, algorithm = "HS256" )
    response = make_response(
      jsonify(
        { "result": "success", "token": token }
      ),
      200,
    )
    response.headers["Content-Type"] = "application/json"
    return response
  else:
    return jsonify({ "result": "fail", "message": "비번 불일치"})
