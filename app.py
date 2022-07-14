from flask import Flask, render_template, request, jsonify, redirect, url_for
from pymongo import MongoClient


app = Flask(__name__)

client = MongoClient(
    'mongodb+srv://taesikyoon97:louis17467@cluster0.ncjxm.mongodb.net/Cluster0?retryWrites=true&w=majority')
db = client.dbsparta

# main 페이지 완
@app.route('/main',methods=['POST','GET'])
def main():
    token_receive = request.cookies.get('token')
    try:
        payload = jwt.decode(token_receive, SECRET_KEY, algorithms=['HS256'])
        print("토큰아이디 "+payload['email'])
        user = db.users.find_one({"email": payload["email"]})
        musical_list = list(db.musicals.find({}, {'_id': False}).limit(28))
        return render_template("main.html", musicals=musical_list, username=payload['id'])
    except jwt.ExpiredSignatureError:
        return redirect(url_for("index", msg="로그인 시간이 만료되었습니다."))
    except jwt.exceptions.DecodeError:
        return redirect(url_for("index", msg="로그인 정보가 존재하지 않습니다."))

if __name__ == '__main__':
    app.run('0.0.0.0', port=5000, debug=True)
