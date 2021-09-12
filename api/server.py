from flask import Flask, jsonify, request, abort
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
            ops.log_action(f"{request.remote_addr} - /create_user - bad request")
            abort(400)
        else:
            if not ops.user_exists(posted_data["username"]):
                ops.add_user(posted_data)

                ops.log_action(f"{request.remote_addr} - /create_user - user {posted_data['username']} created")
                # returns fname, lname and username as json
                return jsonify({"fname": posted_data["fname"],
                    "lname": posted_data["lname"],
                    "username": posted_data["username"]}
                )
            else:
                # if user already exists
                ops.log_action(f"{request.remote_addr} - /create_user - user {posted_data['username']} already exists")
                abort(409, f"User {posted_data['username']} already exists")
    else:
        # method not allowed
        ops.log_action(f"{request.remote_addr} - /create_user - method not allowed")
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
                    ops.log_action(f"{request.remote_addr} - /auth - token generated for {posted_data['username']}")
                    return jsonify({"username": posted_data["username"], "token": token})
                else:
                    # unauthorized
                    ops.log_action(f"{request.remote_addr} - /auth - unauthorized")
                    abort(401)
            else:
                # user not found
                ops.log_action(f"{request.remote_addr} - /auth - {posted_data['username']} not found")
                abort(404, f"user {posted_data['username']} not found")
        else:
            # bad request
            ops.log_action(f"{request.remote_addr} - /auth - bad request")
            abort(400)

    else:
        # method not allowed
        abort(405)


@app.route("/deauth", methods=["POST"])
def sign_out():
    if request.method == "POST":
        posted_data = request.get_json()

        if ops.validate(["token"], posted_data):
            if ops.token_exists(posted_data["token"]):
                ops.delete_tokens(posted_data["token"])

                ops.log_action(f"{request.remote_addr} - /deauth - signed out")
                return jsonify({"message": "You have been signed out"})
            else:
                # token does not exist
                ops.log_action(f"{request.remote_addr} - /deauth - token does not exist")
                abort(404, f"Token {posted_data['token']} does not exist")
        else:
            print(posted_data)
            ops.log_action(f"{request.remote_addr} - /deauth - bad request")
            abort(400)
    else:
        # method not allowed
        ops.log_action(f"{request.remote_addr} - /deauth - method not allowed")
        abort(405)


@app.route("/get_ip", methods=["GET"])
def get_ip():
    if request.method == "GET":
        ops.log_action(f"{request.remote_addr} - /get_ip")
        return jsonify({"ip": request.remote_addr})

    else:
        abort(405)

if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0")