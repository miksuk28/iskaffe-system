from flask import render_template
import config

app = config.connex_app

# Read the swagger.yml file to configure endpoints
app.add_api("swagger.yml")


if __name__ == "__main__":
    app.run(port=5000, debug=True)