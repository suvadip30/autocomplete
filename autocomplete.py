import flask
import json
from flask import request, jsonify
import os.path
import redis
import pickle

app = flask.Flask(__name__)
app.config["DEBUG"] = True


@app.route('/add_word/word=<path:query>')
def api_search(query):
    result = []
    result.append(query)
    file = 'autocom.json'
    if os.path.isfile(file):
        print("if block")
        dic = {query: query}
        with open("autocom.json", "r+") as file:
            data = json.load(file)
            data.update(dic)
            file.seek(0)
            json.dump(data, file)

        if os.path.isfile('autocom.json'):
            f = open('autocom.json', )
            rd = json.load(f)
            print(rd)
            r = redis.StrictRedis(host='localhost', port=6379, db=0)
            pickled_object = pickle.dumps(rd)
            print(pickled_object)
            rds = r.set('auto_dump', pickled_object)
            ab = jsonify(rds)
            return ab
    else:
        print("else block")
        dic = {query: query}
        with open('autocom.json', 'w') as f:
            json.dump(dic, f)
        with open("autocom.json", "r+") as file:
            data = json.load(file)
            data.update(dic)
            file.seek(0)
            json.dump(data, file)

        if os.path.isfile('autocom.json'):
            f = open('autocom.json', )
            rd = json.load(f)
            print(rd)
            r = redis.StrictRedis(host='localhost', port=6379, db=0)
            pickled_object = pickle.dumps(rd)
            print(pickled_object)
            rds = r.set('auto_dump', pickled_object)
            ab = jsonify(rds)
            return ab


@app.route('/autocomplete')
def auto_complete():
    r = redis.StrictRedis(host='localhost', port=6379, db=0)
    read_dict = r.get('auto_dump')
    dic_auto = pickle.loads(read_dict)
    print(dic_auto)
    ab = jsonify(dic_auto)
    return ab


@app.route('/autocomplete/query=<path:query>')
def auto_search(query):
    print(query)
    r = redis.StrictRedis(host='localhost', port=6379, db=0, decode_responses=True)
    prefix = query
    print(prefix)
    results = []
    grabby = 50
    count = 100
    start = r.zrank('autos', prefix)
    while len(results) != count:
        ran = r.zrange('autos', start, start + grabby - 1)
        start += grabby
        if not ran or len(ran) == 0:
            break
        for e in ran:
            mini = min(len(e), len(prefix))
            if e[0:mini] != prefix[0:mini]:
                count = len(results)
                break
            if e[-1] == "%" and len(results) != count:
                results.append(e[0:-1])
    print(results)
    ab = jsonify(results)
    return ab


app.run()
