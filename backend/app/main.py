import json

from bson import ObjectId
from flask import Flask, jsonify, request
# from flask_restful import Resource, Api
from flask_pymongo import PyMongo

app = Flask(__name__)
# api = Api(app)

app.config['MONGO_DBNAME'] = 'freeiptv'

app.config['MONGO_URI'] = 'mongodb://localhost:27017/freeiptv'

app.config.update(
    MONGO_HOST='localhost',
    MONGO_PORT=27017,
    MONGO_USERNAME='',
    MONGO_PASSWORD='',
    MONGO_DBNAME='freeiptv'
)

mongo = PyMongo(app)


class JSONEncoder(json.JSONEncoder):
    def default(self, o):
        if isinstance(o, ObjectId):
            return str(o)
        return json.JSONEncoder.default(self, o)



@app.route('/playitems')
def playitems():

    keyword = request.args.get('keyword')

    result = []

    if keyword:

        print(keyword)

        myquery = {"tags": {"$elemMatch": {"$regex": ".*{}.*".format(keyword), "$options": "i" }}}

        result = mongo.db.playitems.find(myquery)

    else:
        result = mongo.db.playitems.find()



    output = []
    for s in result:
        output.append(s)

    return JSONEncoder().encode(output)

@app.route('/channels')
def channels():

    keyword = request.args.get('keyword')

    result = []

    if keyword:

        print(keyword)

        myquery = {"name": {"$regex": ".*{}.*".format(keyword), "$options": "i" }}

        result = mongo.db.channels.find(myquery)

    else:
        result = mongo.db.channels.find()

    output = []
    for s in result:
        output.append(s)

    return JSONEncoder().encode(output)


if __name__ == '__main__':
    app.debug = True
    app.run()