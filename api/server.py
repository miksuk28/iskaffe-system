from flask import Flask, json, jsonify, request

# creating Flask instance
app = Flask(__name__)

@app.route("/ping", methods=["POST"])
def pong():
    if request.method == "POST":
        posted_data = request.get_json()
        print(request.get("name"))
        
        return jsonify(posted_data)


if __name__ == "__main__":
    app.run(debug=True)