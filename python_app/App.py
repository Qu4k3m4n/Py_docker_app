from flask import Flask, request, jsonify
from pymongo import MongoClient

app = Flask(__name__)
client = MongoClient('mongodb://nosql_db:27017/')
db = client['DB']
collection = db['collection']


@app.route('/api/keyvalue', methods=['POST'])
def create_key_value():
    data = request.json
    key = data.get("key")
    value = data.get("value")

    existing_data = collection.find_one({key: {"$exists": True}})
    if existing_data:
        return jsonify({"error": "Ключ-значение уже существует"}), 208

    collection.insert_one({key: value})

    return jsonify({"message": "Создано"}), 201


@app.route('/api/keyvalue/<key>', methods=['PUT'])
def update_key_value(key):
    data = request.json
    value = data.get("value")

    collection.update_one({key: {"$exists": True}}, {"$set": {key: value}}, upsert=True)

    return jsonify({"message": "Изменено"}), 200


@app.route('/api/keyvalue/<key>', methods=['GET'])
def get_key_value(key):
    data = collection.find_one({key: {"$exists": True}})
    if data:
        data.pop('_id', None)  # Удалить поле '_id' из данных
        return jsonify(data), 200
    else:
        return jsonify({"message": "Ключ не найден"}), 404


if __name__ == "__main__":
    app.run(host='0.0.0.0', port=8080)