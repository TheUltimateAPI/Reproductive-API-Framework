from flask import Flask, jsonify, request
from pymongo import MongoClient

app = Flask(__name__)

# Connect to MongoDB
client = MongoClient("mongodb://localhost:27017/")
db = client["reproductive_api"]
collection = db["data"]

# Add data (POST)
@app.route('/api/store', methods=['POST'])
def store_data():
    data = request.json
    if not data:
        return jsonify({'error': 'No input provided'}), 400

    collection.insert_one(data)
    return jsonify({'message': 'Data stored successfully'}), 200

# Retrieve all data (GET)
@app.route('/api/data', methods=['GET'])  # Updated endpoint
def get_data():
    data = list(collection.find({}, {'_id': 0}))  # Exclude '_id'
    return jsonify({'data': data}), 200

# Update data (PUT)
@app.route('/api/store/<key>', methods=['PUT'])
def update_data(key):
    data = request.json
    if not data:
        return jsonify({'error': 'No input provided'}), 400

    result = collection.update_one({'key': key}, {'$set': data})
    if result.matched_count == 0:
        return jsonify({'error': 'Key not found'}), 404

    return jsonify({'message': 'Data updated successfully'}), 200

# Delete data (DELETE)
@app.route('/api/store/<key>', methods=['DELETE'])
def delete_data(key):
    result = collection.delete_one({'key': key})
    if result.deleted_count == 0:
        return jsonify({'error': 'Key not found'}), 404

    return jsonify({'message': 'Data deleted successfully'}), 200

if __name__ == "__main__":
    app.run(debug=True)