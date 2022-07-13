from flask import Flask, render_template, request, jsonify, redirect, url_for
from pymongo import MongoClient


app = Flask(__name__)

client = MongoClient(
    'mongodb+srv://taesikyoon97:louis17467@cluster0.ncjxm.mongodb.net/Cluster0?retryWrites=true&w=majority')
db = client.dbsparta

# main 페이지
@app.route('/main')
def main():
    musical_list= list(db.musicals.find({}, {'_id': False}).limit(28))
    return render_template("main.html", musicals=musical_list)


if __name__ == '__main__':
    app.run('0.0.0.0', port=5000, debug=True)
