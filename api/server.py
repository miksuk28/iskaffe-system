from os import abort
from flask import Flask, json, jsonify, request, abort
# non-flask endpoints hidden away in seperate file
import operations as ops

# creating Flask instance
app = Flask(__name__)

@app.route("/create_user", methods=["POST"])
def create_user():
    if request.method == "POST":
        posted_data = request.get_json()
        
        # checks if all fields are there and are not None
        if not ops.validate(("fname", "lname", "username", "password"), posted_data):
            abort(400, "Bad request")
        else:
            if not ops.user_exists(posted_data["username"]):
                ops.add_user(posted_data)

                # returns fname, lname and username as json
                return jsonify({"fname": posted_data["fname"],
                    "lname": posted_data["lname"],
                    "username": posted_data["username"]}
                )
            else:
                # if user already exists
                abort(409, f"User {posted_data['username']} already exists")



if __name__ == "__main__":
    app.run(debug=True)