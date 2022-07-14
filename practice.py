from flask import Flask, render_template, jsonify, request, session, redirect, url_for, make_response

app = Flask(__name__)

from pymongo import MongoClient

client = MongoClient("mongodb+srv://thelapssql:musical@cluster0.efos6wv.mongodb.net/Cluster0?retryWrites=true&w=majority")
db = client.musical

SECRET = "musical"

import jwt
import datetime
import hashlib
from bson.objectid import ObjectId

# {% if status %}


@app.route('/detail/<musical_title>/<user_email>', methods=['GET'])
def movie(musical_title, user_email):
    musicals = list(db.musical_main.find({'_id': ObjectId(musical_title)}))
    musical_in = {'musical_id': musicals[0]['_id'],
                  'title': musicals[0]['title'],

                  'img': musicals[0]['url'],
                    'date': musicals[0]['date'],
                  'place': musicals[0]['place']}
    comments = list(db.posts.find({'username': musical_title}))

    compare = []
    for comment in comments:
        _id = comment['_id']
        comment_id = comment['user_email']
        id_id = user_email
        musical_id = comment['musical_id']
        posts = comment['comment']

        compare.append({'_id': _id,
                        'id_id': id_id,
                         'comment_id': comment_id,
                         'musical_id': musical_id,

                         'posts': posts
                         })

    return render_template("detail.html", musical=musical_in, user_email=user_email, comments=comments, compare=compare)


