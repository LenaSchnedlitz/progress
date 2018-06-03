from flask import Flask, render_template, send_file

app = Flask(__name__)


@app.route("/")
def home():
    return render_template('main.html')


@app.route("/<dividend>/<divisor>/<palette>", methods=['GET'])
def load(dividend, divisor=100, palette='TRAFFIC_LIGHT'):
    # return send_file()
    return render_template('main.html')


if __name__ == '__main__':
    app.run()
