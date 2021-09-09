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
            abort(400)
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
    else:
        # method not allowed
        abort(405)



@app.route("/auth", methods=["POST"])
def auth():
    if request.method == "POST":
        posted_data = request.get_json()

        if ops.validate(("username", "password"), posted_data):
            if ops.user_exists(posted_data["username"]):
                if ops.compare_password(posted_data["username"], posted_data["password"]):
                    token = ops.generate_token(posted_data["username"])

                    print(f"Token {token} generated for {posted_data['username']}")
                    return jsonify({"username": posted_data["username"], "token": token})
                else:
                    # unauthorized
                    abort(401)
            else:
                # user not found
                abort(404, f"user {posted_data['username']} not found")
        else:
            # bad request
            abort(400)

    else:
        # method not allowed
        abort(405)


@app.route("/deauth", methods=["POST"])
def sign_out():
    if request.method == "POST":
        return
    else:
        # method not allowed
        abort(405)

if __name__ == "__main__":
    app.run(debug=True)