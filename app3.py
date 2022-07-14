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


# main 페이지

@app.route('/main')
def main():
    musical_list= list(db.musical_main.find({}, {'_id': False}).limit(28))
    print(musical_list)
    return render_template("main.html", musicals=musical_list)

@app.route('/detail/<title>')
def detail_title(title):

    token = request.cookies.get("token")
    try:
        payload = jwt.decode(token, SECRET, algorithms=["HS256"])
        email = db.users.find_one({"email": payload["email"]})['email']

        # 여기 왜 그냥 db.comments.find({'title':title},{'_id':False}) 이거 왜 NONE 나오는거지 ??? 다른데도 왜 논임??
        comments = list(db.comments.find({'title':title+' '}))

        musical = db.musical_main.find_one({'title':title+' '}, {'_id': False})

        detail_list = db.musical_detail.find_one({'title':title+''}, {'_id': False})


        print(comments)
        print(detail_list)
        print(musical)
        print(email)

        # musical = db.musical_main.find_one({"img":img},)
        return render_template('detail3.html',comments=comments, email=email, musical=musical, listde=detail_list)

    except(jwt.ExpiredSignatureError, jwt.exceptions.DecodeError):
        return redirect("/?error=토큰 없음")


# 디테일페이지 렌더링
@app.route("/detail")
def detailRender():
    return render_template("detail3.html")

# 댓글 저장
@app.route('/api/posting', methods=['POST'])
def posting():
    # 클라이언트에서 token받기
    token = request.cookies.get("token")
    try:
        payload = jwt.decode(token, SECRET, algorithms=["HS256"])
        user = db.users.find_one({"email": payload["email"]})
        comment_receive = request.form["comment_give"]
        musical_title_give = request.form['musical_title_give']

        doc = {
            "username": user["email"],
            "comment": comment_receive,
            'title': musical_title_give
        }
        db.comments.insert_one(doc)
        return jsonify({"result":"success", 'msg':'등록완료'})
    except(jwt.ExpiredSignatureError, jwt.exceptions.DecodeError):
        return redirect("/?error=토큰 없음")

# 댓글 불러오기
@app.route('/get_posts', methods=['GET'])
def get_posts():
    token = request.cookies.get("token")
    try:
        payload = jwt.decode(token, SECRET, algorithms=["HS256"])
        posts = list(db.comments.find({}))
        for post in posts:
            post["_id"] = str(post["_id"])
        return jsonify({"result": "success", 'msg': '등록완료', "posts": posts})
    except(jwt.ExpiredSignatureError, jwt.exceptions.DecodeError):
        return redirect("/?error=토큰 없음")

#



# 내주소창
# 여기가 답이네
@app.route('/detail/<username>')
def user(username):
    token = request.cookies.get("token")
    try:
        payload = jwt.decode(token, SECRET, algorithms=["HS256"])
        email = (payload["email"])
        status = (username == payload['email'])

        musical_list = list(db.musical_main.find({},{'_id':False}))

        detail_list = list(db.musical_detail.find({},{'_id':False}))



        # for musical in musical_list:
        #     musical["_id"] = str(musical["img"])

        # musical = db.musical_main.find_one({"img":img},)
        return render_template('detail3.html', email=email, status=status,listmu=musical_list)
    except(jwt.ExpiredSignatureError, jwt.exceptions.DecodeError):
        return redirect("/?error=토큰 없음")



@app.route("/test")
def testRender():
    token = request.args.get("token")
    print(token)
    return render_template("test.html")


# 회원가입
@app.route("/auth/join", methods=["post"])
def authJoin():
    reqEmail = request.form["email"]
    reqPassword = request.form["password"]
    hash = hashlib.sha256(reqPassword.encode("utf-8")).hexdigest()
    db.users.insert_one({"email": reqEmail, "password": hash})
    return redirect("/")


# 로그인
@app.route("/auth/login", methods=["post"])
def authLogin():
    reqEmail = request.get_json()["email"]
    reqPassword = request.get_json()["password"]
    hash = hashlib.sha256(reqPassword.encode("utf-8")).hexdigest()
    user = db.users.find_one({"email": reqEmail, "password": hash})
    if user is not None:
        payload = {
            "email": reqEmail,
        }
        token = jwt.encode(payload, SECRET, algorithm="HS256")
        print("here")

        return jsonify({ "result": "success", "token": token })
    else:
        return jsonify({"result": "fail", "message": "비번 불일치"})


# 중복확인
@app.route("/auth/check", methods=["post"])
def authCheck():
    reqEmail = request.get_json()["email"]
    check = db.users.find_one({"email": reqEmail}, {"_id": False})
    if check:
        print("있습니다.")
        return make_response(jsonify({"result": "exist"}), 200)
    else:
        print("없습니다.")
        return make_response(jsonify({"result": "success"}), 200)


if __name__ == '__main__':
    app.run('0.0.0.0', port=5000, debug=True)