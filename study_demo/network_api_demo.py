from flask import Flask, request, jsonify

app = Flask(__name__)

@app.route('/api/hello', methods=['GET'])
def post_example():
    return "hello"
    data = request.get_json()
    response = {
        'message': 'Data received successfully',
        'data': data
    }
    return jsonify(response)

if __name__ == '__main__':
    app.run(debug=True)